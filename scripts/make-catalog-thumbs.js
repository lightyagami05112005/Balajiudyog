// Create 300x300 thumbnails for catalog PDF embedding (keeps PDF size sane).
// Writes <slug>-thumb.webp alongside <slug>-hero.webp in each category dir.
import fs from "node:fs/promises";
import path from "node:path";
import sharp from "sharp";

const ROOT = path.resolve("../assets/images/products/items");
const SIZE = 240;
const Q = 78;

const dirs = await fs.readdir(ROOT);
let total = 0, done = 0, skipped = 0, failed = 0;
const tasks = [];
for (const d of dirs) {
  const dir = path.join(ROOT, d);
  const stat = await fs.stat(dir).catch(() => null);
  if (!stat?.isDirectory()) continue;
  const files = await fs.readdir(dir);
  for (const f of files) {
    if (!f.endsWith("-hero.webp")) continue;
    total++;
    const src = path.join(dir, f);
    const dst = src.replace(/-hero\.webp$/, "-thumb.webp");
    tasks.push({ src, dst });
  }
}

const CONC = 8;
let i = 0;
async function worker() {
  while (i < tasks.length) {
    const { src, dst } = tasks[i++];
    try {
      // skip if dst exists and newer
      const ds = await fs.stat(dst).catch(() => null);
      if (ds) { skipped++; continue; }
      await sharp(src)
        .resize(SIZE, SIZE, { fit: "cover", position: "center" })
        .webp({ quality: Q, effort: 4 })
        .toFile(dst);
      done++;
      if (done % 50 === 0) process.stdout.write(`  ${done}/${total}\r`);
    } catch (e) {
      failed++;
      console.error("FAIL", src, e.message);
    }
  }
}
await Promise.all(Array.from({ length: CONC }, worker));
console.log(`\nDone: generated=${done} skipped=${skipped} failed=${failed} total=${total}`);
