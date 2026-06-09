// download-generated-assets.js
// Downloads generated images and writes them as optimised WebP into the correct
// folder. Used as a module by generate-leonardo-images.js, and runnable on its
// own to (re)download anything recorded in the manifest that is missing on disk.
//
// Conversion: resize/cover-crop to the master size for the image's aspect ratio,
// then encode WebP. If `sharp` isn't installed, it degrades gracefully by saving
// the original bytes alongside (with a warning) so nothing is lost.

import fs from 'node:fs';
import path from 'node:path';
import { IMAGES_DIR, MANIFEST, config } from './leonardo-config.js';

// sharp is optional at import time; we only hard-require it when converting.
let sharp = null;
try { sharp = (await import('sharp')).default; }
catch { /* handled per-call with a clear message */ }

export const hasSharp = !!sharp;

function ensureDir(file) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
}

/** Fetch a URL into a Buffer with a couple of quick retries for transient errors. */
export async function fetchBuffer(url, tries = 3) {
  let lastErr;
  for (let i = 0; i < tries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`download HTTP ${res.status}`);
      return Buffer.from(await res.arrayBuffer());
    } catch (e) {
      lastErr = e;
      await new Promise(r => setTimeout(r, 800 * (i + 1)));
    }
  }
  throw lastErr;
}

/**
 * Download `url` and write WebP to `outPath`, cover-cropped to {width,height}.
 * @returns {{converted:boolean, savedAs:string, bytes:number}}
 */
export async function downloadAndConvert(url, outPath, { width, height, quality = config.webp.quality } = {}) {
  ensureDir(outPath);
  const buf = await fetchBuffer(url);

  if (sharp) {
    const pipeline = sharp(buf, { failOn: 'none' });
    if (width && height) {
      pipeline.resize(width, height, { fit: 'cover', position: 'attention' });
    }
    await pipeline.webp({ quality, effort: 5 }).toFile(outPath);
    const bytes = fs.statSync(outPath).size;
    return { converted: true, savedAs: outPath, bytes };
  }

  // Fallback: save raw bytes next to the intended path so nothing is lost.
  const alt = outPath.replace(/\.webp$/i, guessExt(buf));
  fs.writeFileSync(alt, buf);
  return { converted: false, savedAs: alt, bytes: buf.length };
}

/**
 * Write an already-fetched image Buffer as optimised WebP (cover-cropped).
 * Used by the multi-variation flow after the realism checker picks the winner.
 */
export async function saveBufferAsWebp(buf, outPath, { width, height, quality = config.webp.quality } = {}) {
  ensureDir(outPath);
  if (sharp) {
    const pipeline = sharp(buf, { failOn: 'none' });
    if (width && height) pipeline.resize(width, height, { fit: 'cover', position: 'attention' });
    await pipeline.webp({ quality, effort: 5 }).toFile(outPath);
    return { converted: true, savedAs: outPath, bytes: fs.statSync(outPath).size };
  }
  const alt = outPath.replace(/\.webp$/i, guessExt(buf));
  fs.writeFileSync(alt, buf);
  return { converted: false, savedAs: alt, bytes: buf.length };
}

function guessExt(buf) {
  if (buf[0] === 0x89 && buf[1] === 0x50) return '.png';
  if (buf[0] === 0xff && buf[1] === 0xd8) return '.jpg';
  return '.img';
}

/* --------------------------------------------------------------------------
   Standalone mode: `node download-generated-assets.js`
   Re-downloads any manifest entry whose WebP is missing on disk (useful if a
   run was interrupted after generation but before/while downloading).
   -------------------------------------------------------------------------- */
async function main() {
  if (!fs.existsSync(MANIFEST)) {
    console.log('No manifest found at', MANIFEST, '— run the generator first.');
    return;
  }
  if (!sharp) {
    console.warn('⚠  sharp is not installed — files will be saved in their original format, not WebP.');
    console.warn('   Install with:  npm install sharp');
  }
  const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  const entries = Object.entries(manifest).filter(([, m]) => m.url && m.status === 'COMPLETE');
  let done = 0, skipped = 0, failed = 0;
  for (const [tail, m] of entries) {
    const outPath = path.join(IMAGES_DIR, tail);
    if (fs.existsSync(outPath)) { skipped++; continue; }
    try {
      const ms = config.master[m.ratio] || config.master['4:3'];
      const r = await downloadAndConvert(m.url, outPath, { width: ms.w, height: ms.h });
      done++;
      console.log(`✓ ${tail}  (${(r.bytes / 1024).toFixed(0)} KB)`);
    } catch (e) {
      failed++;
      console.error(`✗ ${tail}  ${e.message}`);
    }
  }
  console.log(`\nDownload pass complete — saved ${done}, already present ${skipped}, failed ${failed}.`);
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('download-generated-assets.js')) {
  main().catch(e => { console.error(e); process.exit(1); });
}
