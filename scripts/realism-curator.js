#!/usr/bin/env node
// realism-curator.js
// ---------------------------------------------------------------------------
// Site-wide image curation + visual-consistency audit.
//   • scans every generated .webp under assets/images
//   • scores each for realism (image-quality-checker) and measures tone
//     (white-balance warmth, brightness, saturation) for consistency
//   • flags over-AI / oversaturated / fake-metal / over-sharpened / too-smooth
//   • ranks sections, lists the weakest images + ones needing replacement
//   • computes a consistency score and an overall commercial-credibility score
//   • writes assets/final-visual-audit.md and prints a regeneration recommendation
//
// Read-only (never deletes or rewrites images). Run after a generation pass:
//     node realism-curator.js                 # audit + write report
//     node realism-curator.js --reject=72     # also list images below 72 to redo
// ---------------------------------------------------------------------------

import fs from 'node:fs';
import path from 'node:path';
import { IMAGES_DIR, PROJECT_ROOT } from './leonardo-config.js';
import { scoreImageBuffer, hasSharp } from './image-quality-checker.js';

let sharp = null;
try { sharp = (await import('sharp')).default; } catch { /* stats degrade */ }

const args = Object.fromEntries(process.argv.slice(2).map(a => {
  const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true];
}));
const REJECT = Number(args.reject ?? 72);          // "needs replacement" threshold
const WEAK = 75;                                    // "weak" threshold
const AUDIT = path.join(PROJECT_ROOT, 'assets', 'final-visual-audit.md');

const median = (a) => { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const mean = (a) => a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0;
const stdev = (a) => { if (a.length < 2) return 0; const m = mean(a); return Math.sqrt(mean(a.map(x => (x - m) ** 2))); };
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

function listWebp(dir) {
  const out = [];
  (function w(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) w(p);
      else if (e.name.toLowerCase().endsWith('.webp')) out.push(p);
    }
  })(dir);
  return out.sort();
}
function sectionOf(rel) {
  if (rel.startsWith('products/items')) return 'products/items';
  if (rel.startsWith('products/')) return 'products/showcase';
  return rel.split('/')[0];
}

async function analyse(file) {
  const buf = fs.readFileSync(file);
  const q = await scoreImageBuffer(buf);
  let warmth = 0, lum = 0;
  if (sharp) {
    try {
      const st = await sharp(buf).stats();
      const [r, g, b] = st.channels.map(c => c.mean);
      warmth = r - b;                       // >0 = warm white balance
      lum = 0.299 * r + 0.587 * g + 0.114 * b;
    } catch { /* ignore */ }
  }
  return {
    rel: path.relative(IMAGES_DIR, file).replace(/\\/g, '/'),
    score: q.score, flags: q.flags, m: q.metrics, warmth, lum,
  };
}

async function main() {
  if (!hasSharp) console.warn('⚠  sharp not installed — scoring is limited. Run: npm install sharp\n');
  const files = listWebp(IMAGES_DIR);
  if (!files.length) { console.log('No .webp images found yet — run the generator first.'); return; }

  console.log(`Auditing ${files.length} images…`);
  const rows = [];
  for (const f of files) rows.push(await analyse(f));

  // ---- aggregates ----
  const scores = rows.map(r => r.score);
  const med = Math.round(median(scores));
  const avg = Math.round(mean(scores));
  const warmthStd = stdev(rows.map(r => r.warmth));
  const lumStd = stdev(rows.map(r => r.lum));
  const satStd = stdev(rows.map(r => r.m.satMean ?? 0));

  // consistency score: lower spread in WB / brightness / saturation = higher
  const consistency = Math.round(clamp(100 - warmthStd * 1.6 - lumStd * 0.45 - satStd * 130, 0, 100));

  // flag buckets
  const has = (r, kw) => r.flags.some(f => f.startsWith(kw));
  const buckets = {
    oversaturated: rows.filter(r => has(r, 'oversaturated')).length,
    'gold-cast': rows.filter(r => has(r, 'gold-cast')).length,
    'blown-highlights': rows.filter(r => has(r, 'blown')).length,
    'crushed-shadows': rows.filter(r => has(r, 'crushed')).length,
    'over-sharpened': rows.filter(r => has(r, 'over-sharpened')).length,
    'too-smooth': rows.filter(r => has(r, 'too-smooth')).length,
  };
  // "fake metal" heuristic: gold cast AND blown highlights together
  const fakeMetal = rows.filter(r => has(r, 'gold-cast') && has(r, 'blown')).length;

  const flaggedFrac = rows.filter(r => r.flags.length > 0).length / rows.length;
  const credibility = Math.round(0.5 * med + 0.3 * consistency + 0.2 * (100 * (1 - flaggedFrac)));

  // sections
  const bySection = {};
  for (const r of rows) (bySection[sectionOf(r.rel)] ??= []).push(r.score);
  const sectionRows = Object.entries(bySection)
    .map(([s, a]) => ({ s, n: a.length, avg: Math.round(mean(a)) }))
    .sort((x, y) => y.avg - x.avg);

  const weak = rows.filter(r => r.score < WEAK).sort((a, b) => a.score - b.score);
  const replace = rows.filter(r => r.score < REJECT).sort((a, b) => a.score - b.score);

  // ---- report ----
  const grade = (s) => s >= 85 ? 'excellent' : s >= 75 ? 'strong' : s >= 65 ? 'acceptable' : 'needs work';
  const lines = [];
  lines.push('# Balaji Udyog — Final Visual Audit', '');
  lines.push(`> Auto-generated by \`scripts/realism-curator.js\` · ${new Date().toISOString().slice(0, 10)} · ${files.length} images analysed.`, '');
  lines.push('## Scores', '');
  lines.push('| Metric | Value | Read |', '|---|---|---|');
  lines.push(`| **Commercial credibility** | **${credibility}/100** | ${grade(credibility)} |`);
  lines.push(`| Realism (median) | ${med}/100 | ${grade(med)} |`);
  lines.push(`| Realism (mean) | ${avg}/100 | |`);
  lines.push(`| Visual consistency | ${consistency}/100 | ${grade(consistency)} |`);
  lines.push(`| Images flagged | ${Math.round(flaggedFrac * 100)}% | lower is better |`, '');
  lines.push('### Consistency spread (lower = more uniform across the site)');
  lines.push(`- White-balance warmth σ: ${warmthStd.toFixed(1)}`);
  lines.push(`- Brightness σ: ${lumStd.toFixed(1)}`);
  lines.push(`- Saturation σ: ${satStd.toFixed(3)}`, '');

  lines.push('## Realism by section (strongest first)', '', '| Section | Images | Avg realism |', '|---|---|---|');
  for (const s of sectionRows) lines.push(`| ${s.s} | ${s.n} | ${s.avg} — ${grade(s.avg)} |`);
  lines.push('');

  lines.push('## Flag summary', '', '| Issue | Count |', '|---|---|');
  for (const [k, v] of Object.entries(buckets)) lines.push(`| ${k} | ${v} |`);
  lines.push(`| fake-metal (gold-cast + blown) | ${fakeMetal} |`, '');

  lines.push(`## Images needing replacement (realism < ${REJECT}) — ${replace.length}`, '');
  if (!replace.length) lines.push('_None — every image is above the replacement threshold._', '');
  else { replace.slice(0, 60).forEach(r => lines.push(`- \`${r.rel}\` — **${r.score}** ${r.flags.length ? '· ' + r.flags.join(', ') : ''}`)); lines.push(''); }

  lines.push(`## Weak images (realism < ${WEAK}) — ${weak.length}`, '');
  if (!weak.length) lines.push('_None._', '');
  else { weak.slice(0, 60).forEach(r => lines.push(`- \`${r.rel}\` — ${r.score} ${r.flags.length ? '· ' + r.flags.join(', ') : ''}`)); lines.push(''); }

  lines.push('## Strongest images', '');
  rows.slice().sort((a, b) => b.score - a.score).slice(0, 12).forEach(r => lines.push(`- \`${r.rel}\` — ${r.score}`));
  lines.push('');

  lines.push('## Recommended next regeneration batch', '');
  if (replace.length) {
    const secs = [...new Set(replace.map(r => sectionOf(r.rel)))];
    lines.push('Regenerate the flagged sections with the realism pipeline (best-pick), e.g.:', '', '```bash');
    secs.slice(0, 8).forEach(s => {
      const only = s === 'products/showcase' ? 'products/' : s === 'products/items' ? 'products/items' : s + '/';
      lines.push(`node generate-leonardo-images.js --only=${only} --force --variations=3`);
    });
    lines.push('```', '');
  } else lines.push('_No regeneration required — the site meets the realism bar._', '');

  lines.push('---', `\n_Thresholds: weak < ${WEAK}, replace < ${REJECT}. Tune in realism-curator.js / visual-direction.md._`);

  fs.writeFileSync(AUDIT, lines.join('\n'));

  // ---- console summary ----
  console.log(`\n  Commercial credibility : ${credibility}/100 (${grade(credibility)})`);
  console.log(`  Realism median/mean    : ${med} / ${avg}`);
  console.log(`  Visual consistency     : ${consistency}/100`);
  console.log(`  Flagged                : ${Math.round(flaggedFrac * 100)}%  ·  needs-replacement: ${replace.length}`);
  console.log(`  Section averages       : ${sectionRows.map(s => s.s + ' ' + s.avg).join(' · ')}`);
  console.log(`\n  Report written: ${path.relative(PROJECT_ROOT, AUDIT)}`);
  if (args.reject !== undefined && replace.length)
    console.log(`\n  Below ${REJECT} (regenerate):\n` + replace.map(r => '   - ' + r.rel + ' (' + r.score + ')').join('\n'));
}

main().catch(e => { console.error('Fatal:', e?.stack || e); process.exit(1); });
