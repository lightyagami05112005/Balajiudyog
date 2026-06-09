#!/usr/bin/env node
// generate-catalog-batch.js — cheap Flux generator for the 828 catalog-extra products.
// Reads catalog-extras.json, generates each image via Flux Schnell at compact dims
// (≈1 credit each), saves WebP to assets/images/products/items/<cat>/<slug>-hero.webp.
// Skips files that already exist; stops safely when credits run out.

import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
import { apiKey, baseUrl, MODELS, IMAGES_DIR, __dirname as SCRIPTS_DIR } from './leonardo-config.js';

const MANIFEST = path.join(SCRIPTS_DIR, 'catalog-extras.json');
const PROGRESS = path.join(SCRIPTS_DIR, '.catalog-batch-progress.json');

// Dims tuned for ~1 credit on Flux Schnell. Saved WebP upscaled to 800×800 master.
const GEN_W = 640, GEN_H = 640;
const SAVE_W = 800, SAVE_H = 800;
const CONCURRENCY = 6;            // 10 slots available; leave headroom

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const C = { d:s=>`\x1b[2m${s}\x1b[0m`, g:s=>`\x1b[33m${s}\x1b[0m`, o:s=>`\x1b[32m${s}\x1b[0m`, e:s=>`\x1b[31m${s}\x1b[0m`, b:s=>`\x1b[1m${s}\x1b[0m` };

async function api(p, opts = {}) {
  return fetch(baseUrl + p, { ...opts, headers: { accept: 'application/json', 'content-type': 'application/json', authorization: `Bearer ${apiKey}`, ...(opts.headers || {}) } });
}

async function balance() {
  const r = await api('/me'); const j = await r.json(); return j?.user_details?.[0]?.apiPaidTokens ?? 0;
}

async function createFlux(prompt) {
  const body = { modelId: MODELS.fluxSchnell, prompt: prompt.slice(0, 1400), width: GEN_W, height: GEN_H, num_images: 1, contrast: 3.0 };
  const r = await api('/generations', { method: 'POST', body: JSON.stringify(body) });
  if (r.status === 429) { const ra = Number(r.headers.get('retry-after')) || 4; await sleep(ra * 1000); return createFlux(prompt); }
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    const e = new Error(`create ${r.status}: ${t.slice(0, 160)}`); e.status = r.status;
    if (r.status === 402 || /token|credit|insufficient|quota/i.test(t)) e.fatal = 'credits';
    throw e;
  }
  const j = await r.json();
  const gid = j?.sdGenerationJob?.generationId, cost = j?.sdGenerationJob?.apiCreditCost || 0;
  if (!gid) throw new Error('no generationId');
  return { gid, cost };
}

async function poll(gid, timeoutMs = 90000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    await sleep(2500);
    const r = await api('/generations/' + gid);
    if (!r.ok) continue;
    const j = await r.json();
    const g = j?.generations_by_pk;
    if (!g) continue;
    if (g.status === 'COMPLETE') {
      const url = g.generated_images?.[0]?.url;
      if (!url) throw new Error('no image url');
      return url;
    }
    if (g.status === 'FAILED') throw new Error('generation FAILED');
  }
  throw new Error('poll timeout');
}

async function fetchBuffer(url) {
  for (let i = 0; i < 3; i++) {
    try { const r = await fetch(url); if (!r.ok) throw new Error('http ' + r.status); return Buffer.from(await r.arrayBuffer()); }
    catch (e) { if (i === 2) throw e; await sleep(800 * (i + 1)); }
  }
}

async function saveWebp(buf, outPath) {
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  await sharp(buf, { failOn: 'none' })
    .resize(SAVE_W, SAVE_H, { fit: 'cover', position: 'attention' })
    .webp({ quality: 78, effort: 5 })
    .toFile(outPath);
  return fs.statSync(outPath).size;
}

function outPathFor(p) {
  return path.join(IMAGES_DIR, 'products', 'items', p.category, p.slug + '-hero.webp');
}

async function main() {
  if (!apiKey) { console.error('No LEONARDO_API_KEY'); process.exit(1); }
  const products = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  const start = await balance();
  console.log(C.b(`\n  Catalog-extras Flux batch — ${products.length} products, start balance ${start}\n`));

  const progress = fs.existsSync(PROGRESS) ? JSON.parse(fs.readFileSync(PROGRESS, 'utf8')) : {};
  const queue = products.filter(p => {
    const out = outPathFor(p);
    if (fs.existsSync(out)) { progress[p.sku] = { status: 'EXISTS', file: path.relative(IMAGES_DIR, out) }; return false; }
    return true;
  });
  const total = products.length, already = total - queue.length;
  console.log(C.d(`  ${already} already on disk · ${queue.length} to generate · concurrency ${CONCURRENCY}\n`));

  let ok = 0, failed = 0, credits = 0, aborted = false;
  const failures = [];
  const save = () => fs.writeFileSync(PROGRESS, JSON.stringify(progress, null, 1));

  let next = 0;
  const worker = async () => {
    while (next < queue.length) {
      if (aborted) return;
      const idx = next++;
      const p = queue[idx];
      const out = outPathFor(p);
      const n = idx + 1, pct = ((ok + failed) / queue.length * 100).toFixed(0).padStart(3);
      try {
        const { gid, cost } = await createFlux(p.prompt);
        const url = await poll(gid);
        const buf = await fetchBuffer(url);
        const bytes = await saveWebp(buf, out);
        credits += cost;
        ok++;
        progress[p.sku] = { status: 'COMPLETE', cost, file: path.relative(IMAGES_DIR, out) };
        if (ok % 20 === 0) save();
        console.log(`  ${C.d('[' + (ok + failed) + '/' + queue.length + ' ' + pct + '%]')} ${C.o('✓')} ${p.sku} ${C.d(p.name)} ${C.d('(' + (bytes / 1024).toFixed(0) + 'KB, ' + cost + 'cr)')}`);
      } catch (e) {
        failed++;
        failures.push({ sku: p.sku, error: e.message });
        progress[p.sku] = { status: 'FAILED', error: e.message };
        console.log(`  ${C.e('✗')} ${p.sku} ${C.d(e.message)}`);
        if (e.fatal === 'credits' && !aborted) {
          aborted = true;
          console.error(C.e('\n  ⚠ Out of credits — stopping. ' + (queue.length - ok - failed) + ' products pending.'));
        }
      }
    }
  };

  const t0 = Date.now();
  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, queue.length) }, worker));
  save();

  const mins = ((Date.now() - t0) / 60000).toFixed(1);
  const end = await balance();
  console.log(C.b('\n  ──── Summary ────'));
  console.log(`  generated : ${ok}`);
  console.log(`  skipped (existed) : ${already}`);
  console.log(`  failed   : ${failed}`);
  console.log(`  credits  : ~${start - end} (start ${start} → end ${end})`);
  console.log(`  elapsed  : ${mins} min`);
  if (failures.length) {
    console.log(C.e('\n  Failures (re-run script to retry):'));
    failures.slice(0, 30).forEach(f => console.log(`   - ${f.sku}  ${C.d(f.error)}`));
  }
}

main().catch(e => { console.error(C.e('Fatal: ' + e.message)); process.exit(1); });
