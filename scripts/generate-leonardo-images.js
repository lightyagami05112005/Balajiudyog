#!/usr/bin/env node
// generate-leonardo-images.js
// ---------------------------------------------------------------------------
// Automated Leonardo AI image generation for the Balaji Udhyog export website.
//
//   1. Parses prompt blocks from  assets/ai-image-prompts.md
//   2. Scans every page for the image paths it references (these ARE the
//      filenames defined in assets/image-map.md)
//   3. Resolves the right prompt for each file, enhances it, and generates it
//      via the Leonardo REST API (async batch + retry + rate-limit + polling)
//   4. Downloads each result and writes it as optimised .webp into the folder
//
// Usage:
//   node generate-leonardo-images.js [flags]
//     --dry-run            parse + resolve everything, print the plan, no API calls
//     --priority=1|2|3     only generate that priority group (default: all, in order)
//     --only=<substr>      only files whose path contains <substr> (e.g. brassware, hero, hubs)
//     --group=<substr>     alias of --only
//     --limit=N            cap the number of images this run
//     --force              regenerate even if the .webp already exists
//     --concurrency=N      parallel generations (default 3)
//     --engine=photoreal|phoenix|kino|sdxl
//     --model=visionXL|diffusionXL|albedoXL|kinoXL|phoenix
//     --num=N              images per generation (we keep the first)
// ---------------------------------------------------------------------------

import fs from 'node:fs';
import path from 'node:path';
import {
  config, apiKey, baseUrl, buildGenerationBody, masterSize,
  PROJECT_ROOT, IMAGES_DIR, PROMPTS_MD, MANIFEST, MODELS,
} from './leonardo-config.js';
import { buildRealism } from './realism-enhancer.js';
import { scoreImageBuffer } from './image-quality-checker.js';
import { downloadAndConvert, saveBufferAsWebp, fetchBuffer, hasSharp } from './download-generated-assets.js';

/* ===================== CLI ===================== */
function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t.startsWith('--')) {
      const [k, v] = t.slice(2).split('=');
      if (v !== undefined) a[k] = v;
      else if (argv[i + 1] && !argv[i + 1].startsWith('--')) a[k] = argv[++i];
      else a[k] = true;
    } else a._.push(t);
  }
  return a;
}
const args = parseArgs(process.argv.slice(2));
const DRY = !!args['dry-run'];
const FORCE = !!args.force;
if (args.engine) config.engine = String(args.engine);
if (args.model) config.model = String(args.model);
if (args.num) config.numImages = Math.max(1, Number(args.num) || 1);
if (args.variations) config.variations = Math.max(1, Math.min(5, Number(args.variations) || 3));
if (args.concurrency) config.concurrency = Math.max(1, Number(args.concurrency) || 3);
const REALISM_RETRIES = args['realism-retries'] !== undefined ? Number(args['realism-retries']) : 1;
const ONLY = (args.only || args.group || '').toString().toLowerCase();
const EXCLUDE = (args.exclude || '').toString().toLowerCase();
const PRIORITY = args.priority ? Number(args.priority) : null;
const LIMIT = args.limit ? Number(args.limit) : null;

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const C = { dim: s => `\x1b[2m${s}\x1b[0m`, gold: s => `\x1b[33m${s}\x1b[0m`, ok: s => `\x1b[32m${s}\x1b[0m`, err: s => `\x1b[31m${s}\x1b[0m`, b: s => `\x1b[1m${s}\x1b[0m` };

/* ===================== Prompt markdown parser ===================== */
function parsePrompts(md) {
  const text = fs.readFileSync(md, 'utf8');
  const lines = text.split(/\r?\n/);
  const blocks = {};
  let globalNegative = '';

  // Global negative base (### 1.1 ... fenced block)
  const gnIdx = lines.findIndex(l => /Global Negative Prompt/i.test(l));
  if (gnIdx >= 0) {
    const fence = grabFence(lines, gnIdx);
    if (fence) globalNegative = fence.replace(/\s+/g, ' ').trim();
  }

  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^###\s+([A-Z]\d+(?:\.\d+)?)\s+[—\-–]/);
    if (!m) continue;
    const code = m[1];
    // collect lines until the next ### / ## header
    let j = i + 1;
    const body = [];
    for (; j < lines.length; j++) {
      if (/^###?\s/.test(lines[j])) break;
      body.push(lines[j]);
    }
    const segment = body.join('\n');
    const main = grabFence(body, 0) || '';
    const neg = matchAfter(segment, /\*\*Negative Prompt\*\*/i, /`([^`]+)`/);
    const ratio = (segment.match(/\*\*Aspect Ratio\*\*[^\n]*?\b(16:10|16:9|4:5|4:3|1:1)\b/i) || [])[1] || '';
    blocks[code] = {
      main: main.replace(/\s+/g, ' ').trim(),
      negative: (neg || '').replace(/\s+/g, ' ').trim(),
      ratio,
    };
    i = j - 1;
  }
  return { blocks, globalNegative };
}
function grabFence(arr, fromIdx) {
  let start = -1;
  for (let i = fromIdx; i < arr.length; i++) {
    if (arr[i].trim().startsWith('```')) { start = i; break; }
    if (i > fromIdx + 8 && /^###?\s/.test(arr[i])) break;
  }
  if (start < 0) return '';
  const out = [];
  for (let i = start + 1; i < arr.length; i++) {
    if (arr[i].trim().startsWith('```')) break;
    out.push(arr[i]);
  }
  return out.join(' ');
}
function matchAfter(segment, marker, capture) {
  const idx = segment.search(marker);
  if (idx < 0) return '';
  const tail = segment.slice(idx);
  const m = tail.match(capture);
  return m ? m[1] : '';
}

/* ===================== Scan pages for required images ===================== */
function scanImageTargets() {
  const tails = new Set();
  const walk = (dir) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) { if (e.name !== 'node_modules' && e.name !== 'images') walk(p); }
      else if (e.name.endsWith('.html')) {
        const t = fs.readFileSync(p, 'utf8');
        const re = /assets\/images\/([A-Za-z0-9._\/-]+\.webp)/g;
        let m;
        while ((m = re.exec(t))) tails.add(m[1]);
      }
    }
  };
  walk(PROJECT_ROOT);
  return [...tails].sort();
}

/* ===================== Resolve a prompt for each file ===================== */
const CAT_BLOCK = { brassware: 'B1', 'metal-art-ware': 'B2', 'furniture-hardware': 'B3', 'locks-hardware': 'B4', 'bathroom-hardware': 'B5', glassware: 'B6', 'home-decor': 'B7' };
const HUB_AERIAL = { moradabad: 'C1.0', aligarh: 'C2.0', firozabad: 'C3.0' };
const HUB_INTERIOR = {
  'foundry-pour': 'C1.1', 'engraver': 'C1.2', 'finishing': 'C1.3',
  'factory-floor': 'C2.1', 'cylinder-assembly': 'C2.2', 'qc-bench': 'C2.3',
  'furnace': 'C3.1', 'chandelier-bench': 'C3.2', 'crystal-cutter': 'C3.3',
};
const EXPORT_BLOCK = {
  'container-loading-bay': 'D2', 'branded-packaging-oem': 'G2', 'packaging-line': 'G3',
  'documentation-desk': 'E2', 'consolidation-warehouse': 'D4', 'port-arrival-inland': 'D3',
  'shipping-containers-mundra': 'D1', 'warehouse-operations': 'E1',
};
const GALLERY_BLOCK = {
  'brassware-moradabad': 'B1', 'cylinder-locks-aligarh': 'B4', 'home-decor': 'B7',
  'chandelier-firozabad': 'B6', 'bathroom-hardware': 'B5', 'metal-artware': 'B2',
  'container-loading-mundra': 'D1',
};
const BLOG_THEME = {
  'market-insight': 'market momentum across premium brass and steel export goods',
  'hub-guide': 'a moody Indian craft-district sourcing guide',
  'compliance': 'export compliance — neat unmarked documents and a brass stamp on a navy desk',
  'directory': 'an organised array of hardware samples on a dark grid surface',
  'logistics': 'shipping logistics — a single shipping container detail at golden hour',
  'oem': 'OEM private label — elegant blank premium packaging on navy',
};
const PORTRAIT_ROLE = {
  'managing-director': 'managing director, a mature Indian businessman',
  'operations-director': 'operations director, an Indian businesswoman',
  'africa-head': 'Africa desk head, a West African businesswoman, Lagos office backdrop',
  'head-qc': 'head of quality control, an Indian man, in a factory backdrop',
};
const OFFICE_PLACE = {
  'moradabad-facility': 'premium brassware-house headquarters building in an Indian industrial district in Moradabad',
  'mundra-warehouse': 'port-side export warehouse facility near Mundra',
  'lagos': 'sleek Africa-desk office building on a Lagos boulevard',
};
const humanize = (s) => s.replace(/-/g, ' ').trim();

function resolve(tail) {
  const seg = tail.split('/');
  const name = seg[seg.length - 1].replace(/\.webp$/, '');

  if (tail.startsWith('hero/'))
    return { code: name.includes('brass') ? 'A1' : 'A2', ratio: 'heropanel' };

  if (tail.startsWith('categories/')) {
    const cat = name.replace('-hero', '');
    return { code: CAT_BLOCK[cat] || 'B1', ratio: (cat === 'brassware' || cat === 'metal-art-ware') ? '16:10' : '4:5' };
  }

  if (tail.startsWith('hubs/')) {
    const hub = seg[1];
    if (name.endsWith('-aerial')) return { code: HUB_AERIAL[hub] || 'C1.0', ratio: '4:3' };
    const stem = name.replace(hub + '-', '');
    return { code: HUB_INTERIOR[stem] || HUB_AERIAL[hub] || 'C1.1', ratio: '4:5' };
  }

  if (tail.startsWith('export/'))
    return { code: EXPORT_BLOCK[name] || 'D1', ratio: (name === 'documentation-desk' || name === 'branded-packaging-oem') ? '4:3' : '16:9' };

  if (tail.startsWith('gallery/'))
    return { code: GALLERY_BLOCK[name] || 'B1', ratio: name.includes('container') ? '16:9' : '4:3' };

  if (tail.startsWith('blog/')) {
    if (name.includes('feature')) return { code: 'I1', ratio: '16:9' };
    return { code: 'I2', subject: BLOG_THEME[name] || humanize(name), ratio: '16:9' };
  }

  if (tail.startsWith('team/')) {
    if (name.startsWith('portrait-'))
      return { code: 'H1', subject: PORTRAIT_ROLE[name.replace('portrait-', '')] || humanize(name), ratio: '4:5' };
    return { code: 'H2', subject: OFFICE_PLACE[name.replace('office-', '')] || humanize(name), ratio: '4:3' };
  }

  if (tail.startsWith('products/items/')) {
    const slug = name.replace(/-(hero|1|2|3)$/, '');
    return { code: 'F0', subject: `a ${humanize(slug)}, premium export-grade Indian product`, ratio: name.endsWith('-hero') ? '4:3' : '1:1' };
  }

  if (tail.startsWith('products/')) {
    const cat = seg[1];
    if (/^sku-\d+/.test(name))
      return { code: 'F0', subject: humanize(name.replace(/^sku-\d+-/, '')), ratio: '4:3' };
    if (name.startsWith('gallery-')) {
      const role = name.replace('gallery-', '');
      if (role === 'hero') return { code: CAT_BLOCK[cat] || 'B1', ratio: '16:10' };
      if (role === 'packaging') return { code: 'G1', ratio: '4:3' };
      if (role === 'container') return { code: 'D2', ratio: '4:3' };
      if (role === 'lifestyle') return { code: CAT_BLOCK[cat] || 'B7', ratio: '4:3' };
      return { code: 'F0', subject: `${humanize(cat)} close-up texture and finish detail`, ratio: '4:3' };
    }
  }
  return null;
}

function priorityOf(tail) {
  if (tail.startsWith('hero/')) return 1;
  if (/^categories\/(brassware|locks-hardware|bathroom-hardware)-hero/.test(tail)) return 1;
  if (/^export\/(container-loading-bay|shipping-containers-mundra|port-arrival-inland|consolidation-warehouse)/.test(tail)) return 1;
  if (tail.startsWith('hubs/') || tail.startsWith('products/') || tail.startsWith('export/') || tail.startsWith('categories/')) return 2;
  if (tail.startsWith('blog/') || tail.startsWith('gallery/') || tail.startsWith('team/')) return 3;
  return 2;
}

/* ===================== Build job list ===================== */
function buildJobs(blocks, globalNegative) {
  const tails = scanImageTargets();
  const jobs = [];
  const unresolved = [];
  for (const tail of tails) {
    const r = resolve(tail);
    if (!r) { unresolved.push(tail); continue; }
    const block = blocks[r.code];
    if (!block || !block.main) { unresolved.push(`${tail} (no prompt block ${r.code})`); continue; }
    const { prompt, negative, presetStyle, kind } = buildRealism({
      main: block.main, subject: r.subject, code: r.code, tail: tail, blockNegative: block.negative,
    });
    jobs.push({
      tail,
      outPath: path.join(IMAGES_DIR, tail),
      ratio: r.ratio || block.ratio || '4:3',
      code: r.code,
      priority: priorityOf(tail),
      prompt, negative, presetStyle, kind,
    });
  }
  return { jobs, unresolved };
}

/* ===================== Leonardo API ===================== */
async function api(pathname, opts = {}) {
  return fetch(baseUrl + pathname, {
    ...opts,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`,
      ...(opts.headers || {}),
    },
  });
}

async function withRetry(fn, label, onRetry) {
  let attempt = 0;
  for (;;) {
    try { return await fn(); }
    catch (e) {
      if (e.status === 401 || e.status === 403 || e.fatal) throw e; // auth / out-of-credits — never retry
      attempt++;
      if (attempt > config.retry.retries) throw e;
      let delay = e.retryAfter || Math.min(config.retry.maxDelayMs, config.retry.baseDelayMs * 2 ** (attempt - 1));
      delay += Math.floor(Math.random() * 600);
      if (onRetry) onRetry(label, attempt, delay, e.message);
      await sleep(delay);
    }
  }
}

async function createGeneration(body) {
  const res = await api('/generations', { method: 'POST', body: JSON.stringify(body) });
  if (res.status === 429) {
    const ra = Number(res.headers.get('retry-after'));
    const e = new Error('rate limited (429)'); e.status = 429;
    if (Number.isFinite(ra) && ra > 0) e.retryAfter = ra * 1000;
    throw e;
  }
  if (!res.ok) {
    const txt = await res.text().catch(() => '');
    const e = new Error(`create ${res.status}: ${txt.slice(0, 180)}`); e.status = res.status;
    if (res.status === 402 || (res.status === 400 && /token|credit|insufficient|quota|balance|subscription/i.test(txt))) e.fatal = 'credits';
    throw e;
  }
  const j = await res.json();
  const gid = j?.sdGenerationJob?.generationId;
  const cost = j?.sdGenerationJob?.apiCreditCost || 0;
  if (!gid) throw new Error('no generationId in API response');
  return { gid, cost };
}

async function pollGeneration(gid) {
  const start = Date.now();
  while (Date.now() - start < config.poll.timeoutMs) {
    await sleep(config.poll.intervalMs);
    const res = await api('/generations/' + gid);
    if (res.status === 429) { await sleep(config.retry.baseDelayMs); continue; }
    if (!res.ok) continue; // transient — keep polling
    const j = await res.json();
    const g = j?.generations_by_pk;
    if (!g) continue;
    if (g.status === 'COMPLETE') {
      const urls = (g.generated_images || []).map(im => im.url).filter(Boolean);
      if (!urls.length) throw new Error('generation COMPLETE but returned no image url');
      return urls;
    }
    if (g.status === 'FAILED') throw new Error('generation FAILED on Leonardo');
  }
  throw new Error('poll timeout');
}

/* ===================== Pool ===================== */
async function runPool(jobs, worker, concurrency) {
  let next = 0;
  const lanes = Array.from({ length: Math.min(concurrency, jobs.length) }, async () => {
    while (next < jobs.length) {
      const idx = next++;
      await worker(jobs[idx], idx);
    }
  });
  await Promise.all(lanes);
}

/* ===================== Main ===================== */
async function main() {
  console.log(C.b('\n  Balaji Udhyog · Leonardo image pipeline\n'));

  const { blocks, globalNegative } = parsePrompts(PROMPTS_MD);
  console.log(C.dim(`  Parsed ${Object.keys(blocks).length} prompt blocks from ai-image-prompts.md`));

  let { jobs, unresolved } = buildJobs(blocks, globalNegative);

  // filters
  if (PRIORITY) jobs = jobs.filter(j => j.priority === PRIORITY);
  if (ONLY) jobs = jobs.filter(j => j.tail.toLowerCase().includes(ONLY));
  if (EXCLUDE) jobs = jobs.filter(j => !j.tail.toLowerCase().includes(EXCLUDE));
  jobs.sort((a, b) => a.priority - b.priority || a.tail.localeCompare(b.tail));
  if (!FORCE) jobs = jobs.filter(j => !fs.existsSync(j.outPath));
  if (LIMIT) jobs = jobs.slice(0, LIMIT);

  const byPr = { 1: 0, 2: 0, 3: 0 };
  jobs.forEach(j => byPr[j.priority]++);
  console.log(C.dim(`  Targets: ${jobs.length} to generate  (P1 ${byPr[1]} · P2 ${byPr[2]} · P3 ${byPr[3]})`));
  if (unresolved.length) console.log(C.dim(`  Unresolved/ skipped: ${unresolved.length}`));
  console.log(C.dim(`  Engine: ${config.engine} · model: ${config.model} · alchemy: ${config.alchemy} · preset: ${config.presetStyle} · highContrast: ${config.highContrast}`));
  console.log(C.dim(`  Realism mode: ${config.variations} variations/slot → keep best · reject < ${config.realismThreshold} (+${REALISM_RETRIES} regen)`));
  console.log(C.dim(`  WebP via sharp: ${hasSharp ? 'yes' : 'NO (will save original format — run npm install sharp)'}\n`));

  if (DRY) {
    const plan = jobs.map(j => ({ file: j.tail, priority: j.priority, block: j.code, ratio: j.ratio, prompt: j.prompt }));
    fs.writeFileSync(path.join(path.dirname(MANIFEST), '.leonardo-plan.json'), JSON.stringify(plan, null, 2));
    console.log(C.gold('  DRY RUN — no API calls. Sample of resolved jobs:\n'));
    for (const j of jobs.slice(0, 12))
      console.log(`  ${C.gold(j.priority + '·' + j.code)}  ${j.tail}\n      ${C.dim(j.prompt.slice(0, 150) + '…')}`);
    const est = jobs.length * config.variations * config.estCreditsPerImage;
    console.log(C.dim(`\n  Full plan written to .leonardo-plan.json`));
    console.log(C.dim(`  Estimated API credits (rough): ~${est.toLocaleString()} for ${jobs.length} images`));
    if (unresolved.length) { console.log(C.dim('\n  Unresolved:')); unresolved.slice(0, 20).forEach(u => console.log('   ', u)); }
    return;
  }

  if (!apiKey) {
    console.error(C.err('  ✗ No LEONARDO_API_KEY found. Add it to scripts/.env (see .env.example).'));
    process.exit(1);
  }
  if (!jobs.length) { console.log(C.ok('  Nothing to do — all targeted images already exist (use --force to regenerate).')); return; }

  const manifest = fs.existsSync(MANIFEST) ? JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) : {};
  const counters = { ok: 0, failed: 0, rejected: 0 };
  const failures = [];
  let creditsUsed = 0, completed = 0, realismSum = 0, aborted = false;
  const total = jobs.length;
  const t0 = Date.now();
  const saveManifest = () => fs.writeFileSync(MANIFEST, JSON.stringify(manifest, null, 2));

  const reportPending = () => {
    const pend = jobs.filter(j => !(manifest[j.tail] && manifest[j.tail].status === 'COMPLETE'));
    const byArea = {};
    for (const j of pend) {
      const a = j.tail.startsWith('products/items') ? 'products/items' : j.tail.split('/')[0];
      byArea[a] = (byArea[a] || 0) + 1;
    }
    console.log(C.gold(`\n  Pending categories (${pend.length} images not yet generated):`));
    Object.entries(byArea).sort().forEach(([a, n]) => console.log(`   - ${a.padEnd(20)} ${n}`));
    console.log(C.dim('  Re-run the same command with a funded key — finished files are skipped.'));
  };

  const onRetry = (label, attempt, delay, msg) =>
    console.log(`      ${C.gold('↻')} retry ${attempt}/${config.retry.retries} in ${(delay / 1000).toFixed(1)}s — ${C.dim(msg)}`);

  const worker = async (job) => {
    if (aborted) return;                 // credits/auth gone — drain the pool quietly
    const idxNum = completed + counters.failed + 1;
    const pct = `${((completed / total) * 100).toFixed(0)}%`.padStart(4);
    console.log(`  ${C.dim('[' + idxNum + '/' + total + ' ' + pct + ']')} ${C.gold('▸')} ${job.tail} ${C.dim('(' + job.code + '/' + job.kind + ', ' + job.ratio + ', x' + config.variations + ')')}`);
    let chosen = null;
    try {
      for (let attempt = 0; attempt <= REALISM_RETRIES; attempt++) {
        // Request N variations as separate single-image generations (Alchemy caps
        // images-per-generation at higher resolutions), then score + keep the best.
        const urls = [];
        for (let v = 0; v < config.variations; v++) {
          const { us, cost } = await withRetry(async () => {
            const { gid, cost } = await createGeneration(buildGenerationBody(job));
            const us = await pollGeneration(gid);
            return { us, cost };
          }, job.tail, onRetry);
          creditsUsed += cost || 0;
          urls.push(...us);
        }

        // download every candidate, score each for realism, keep the best
        const scored = [];
        for (const u of urls) {
          try { const buf = await fetchBuffer(u); const s = await scoreImageBuffer(buf); scored.push({ url: u, buf, score: s.score, flags: s.flags }); }
          catch { /* skip a candidate that failed to download */ }
        }
        if (!scored.length) throw new Error('no candidates downloaded');
        scored.sort((a, b) => b.score - a.score);
        const best = scored[0];
        counters.rejected += scored.length - 1;
        console.log(`      ${C.dim('realism')} ${scored.map(s => s.score).join('/')} ${C.dim('→ keep ' + best.score)}${best.flags.length ? C.dim(' [' + best.flags.join(' ') + ']') : ''}`);
        if (!chosen || best.score > chosen.score) chosen = best;
        if (best.score >= config.realismThreshold) break;
        if (attempt < REALISM_RETRIES) console.log(`      ${C.gold('↻')} realism ${best.score} < ${config.realismThreshold} — regenerating variation set`);
      }

      const ms = masterSize(job.ratio);
      const dl = await saveBufferAsWebp(chosen.buf, job.outPath, { width: ms.w, height: ms.h });
      manifest[job.tail] = { status: 'COMPLETE', code: job.code, ratio: job.ratio, kind: job.kind, realism: chosen.score, flags: chosen.flags, savedAs: path.relative(PROJECT_ROOT, dl.savedAs) };
      counters.ok++; completed++; realismSum += chosen.score;
      console.log(`      ${C.ok('✓')} ${path.basename(dl.savedAs)} ${C.dim((dl.bytes / 1024).toFixed(0) + ' KB · realism ' + chosen.score + (dl.converted ? '' : ' · NOT webp (install sharp)'))}`);
    } catch (e) {
      counters.failed++;
      failures.push({ tail: job.tail, error: e.message });
      manifest[job.tail] = { status: 'FAILED', code: job.code, ratio: job.ratio, error: e.message };
      console.log(`      ${C.err('✗')} failed — ${C.dim(e.message)}`);
      if (e.fatal === 'credits' && !aborted) {
        aborted = true;
        console.error(C.err('\n  ⚠ Out of Leonardo API credits — stopping safely (pipeline did not crash).'));
        saveManifest(); reportPending();
      } else if ((e.status === 401 || e.status === 403) && !aborted) {
        aborted = true; process.exitCode = 1;
        console.error(C.err('\n  Authentication failed — check your LEONARDO_API_KEY. Aborting.'));
        saveManifest();
      }
    }
    saveManifest();
  };

  await runPool(jobs, worker, config.concurrency);
  saveManifest();

  const mins = ((Date.now() - t0) / 60000).toFixed(1);
  const avg = counters.ok ? Math.round(realismSum / counters.ok) : 0;
  console.log(C.b('\n  ──────── Summary ────────'));
  console.log(`  ${C.ok('✓ generated')} : ${counters.ok}  (avg realism ${avg}/100)`);
  console.log(`  ${C.dim('rejected variations')} : ${counters.rejected}`);
  console.log(`  ${C.err('✗ failed')}    : ${counters.failed}`);
  console.log(`  credits used : ~${creditsUsed.toLocaleString()}`);
  console.log(`  elapsed      : ${mins} min`);
  console.log(`  manifest     : ${path.relative(PROJECT_ROOT, MANIFEST)}`);
  if (aborted) {
    console.log(C.gold('\n  Run stopped before completion — see the pending queue above. Re-run with a funded key.'));
  } else if (failures.length) {
    console.log(C.err('\n  Failed images (re-run to retry — existing files are skipped):'));
    failures.slice(0, 40).forEach(f => console.log(`   - ${f.tail}  ${C.dim(f.error)}`));
  } else {
    console.log(C.ok('\n  Done. The site now references the selected, realism-scored assets.'));
  }
}

main().catch(e => { console.error(C.err('\nFatal: ' + (e?.stack || e))); process.exit(1); });
