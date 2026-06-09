// Create 480×480 mid-res images for line-sheet pages (1 large item per page).
// Smaller than the 800×800 -hero.webp originals → keeps PDF size sane.
// Writes <slug>-mid.webp alongside the hero in each category dir.
import fs from "node:fs/promises";
import path from "node:path";
import sharp from "sharp";

const ROOT = path.resolve("../assets/images/products/items");
const SIZE = 480;
const Q = 78;

const dirs = await fs.readdir(ROOT);
const tasks = [];
for (const d of dirs) {
  const dir = path.join(ROOT, d);
  if (!(await fs.stat(dir).catch(() => null))?.isDirectory()) continue;
  for (const f of await fs.readdir(dir)) {
    if (!f.endsWith("-hero.webp")) continue;
    tasks.push({
      src: path.join(dir, f),
      dst: path.join(dir, f.replace(/-hero\.webp$/, "-mid.webp")),
    });
  }
}

let done = 0, skipped = 0, failed = 0;
async function worker() {
  while (tasks.length) {
    const { src, dst } = tasks.shift();
    try {
      if (await fs.stat(dst).catch(() => null)) { skipped++; continue; }
      await sharp(src).resize(SIZE, SIZE, { fit: "cover" }).webp({ quality: Q }).toFile(dst);
      done++;
      if (done % 50 === 0) process.stdout.write(`  ${done}\r`);
    } catch (e) { failed++; console.error("FAIL", src, e.message); }
  }
}
await Promise.all(Array.from({ length: 8 }, worker));
console.log(`\nDone: generated=${done} skipped=${skipped} failed=${failed}`);
