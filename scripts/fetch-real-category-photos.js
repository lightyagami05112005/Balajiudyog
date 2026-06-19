// Replace 7 category hero images with real Pexels photos (current ones are AI).
// Backs up the AI originals as <name>-ai.webp.bak in the same folder.
import fs from "node:fs/promises";
import path from "node:path";
import https from "node:https";
import sharp from "sharp";

const ROOT = path.resolve("../assets/images/categories");

const PHOTOS = {
  "brassware-hero.jpg?v=9999":          { url: "https://images.pexels.com/photos/14127692/pexels-photo-14127692.jpeg", w: 1600, h: 1000 },
  "metal-art-ware-hero.jpg?v=12345?v=999":     { url: "https://images.pexels.com/photos/5028727/pexels-photo-5028727.jpeg",   w: 1600, h: 1000 },
  "furniture-hardware-hero.jpg?v=999": { url: "https://images.pexels.com/photos/35287566/pexels-photo-35287566.jpeg", w: 1000, h: 1250 },
  "locks-hardware-hero.jpg?v=999":     { url: "https://images.pexels.com/photos/36740854/pexels-photo-36740854.jpeg", w: 1000, h: 1250 },
  "bathroom-hardware-hero.webp":  { url: "https://images.pexels.com/photos/30560253/pexels-photo-30560253.jpeg", w: 1000, h: 1250 },
  "glassware-hero.jpg?v=99999":          { url: "https://images.pexels.com/photos/7809813/pexels-photo-7809813.jpeg",   w: 1000, h: 1250 },
  "home-decor-hero.webp":         { url: "https://images.pexels.com/photos/10903296/pexels-photo-10903296.jpeg", w: 1000, h: 1250 },
};

function download(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return download(res.headers.location).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
      const chunks = [];
      res.on("data", c => chunks.push(c));
      res.on("end", () => resolve(Buffer.concat(chunks)));
      res.on("error", reject);
    }).on("error", reject);
  });
}

let ok = 0, fail = 0;
for (const [name, { url, w, h }] of Object.entries(PHOTOS)) {
  const dst = path.join(ROOT, name);
  try {
    const bak = dst.replace(/\.webp$/, "-ai.webp.bak");
    if (await fs.stat(dst).catch(() => null) && !(await fs.stat(bak).catch(() => null))) {
      await fs.rename(dst, bak);
    }
    process.stdout.write(`  ↓ categories/${name} ... `);
    const buf = await download(url);
    await sharp(buf)
      .resize(w, h, { fit: "cover", position: "center" })
      .webp({ quality: 82, effort: 5 })
      .toFile(dst);
    console.log("ok");
    ok++;
  } catch (e) {
    console.log("FAIL —", e.message);
    fail++;
  }
}
console.log(`\nDone: ${ok} ok, ${fail} failed`);
