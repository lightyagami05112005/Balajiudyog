// Download real Pexels stock photos for the 3 hub pages (Aligarh, Firozabad,
// Muradabad) → replaces the AI-generated images the user said look fake.
// Photos resized to existing aspect ratios and re-saved as WebP.
import fs from "node:fs/promises";
import path from "node:path";
import https from "node:https";
import sharp from "sharp";

const ROOT = path.resolve("../assets/images/hubs");

// curated Pexels photos chosen to match each hub's craft
const MAP = {
  aligarh: {
    "aligarh-aerial.webp":            { url: "https://images.pexels.com/photos/29383723/pexels-photo-29383723.jpeg", w: 1600, h: 1067 },
    "aligarh-factory-floor.webp":     { url: "https://images.pexels.com/photos/29988954/pexels-photo-29988954.jpeg", w: 1600, h: 1067 },
    "aligarh-cylinder-assembly.webp": { url: "https://images.pexels.com/photos/5846139/pexels-photo-5846139.jpeg",   w: 1200, h: 1200 },
    "aligarh-qc-bench.webp":          { url: "https://images.pexels.com/photos/6895069/pexels-photo-6895069.jpeg",   w: 1200, h: 1200 },
  },
  firozabad: {
    "firozabad-aerial.webp":           { url: "https://images.pexels.com/photos/29289936/pexels-photo-29289936.jpeg", w: 1600, h: 1067 },
    "firozabad-furnace.webp":          { url: "https://images.pexels.com/photos/220990/pexels-photo-220990.jpeg",     w: 1600, h: 1067 },
    "firozabad-crystal-cutter.webp":   { url: "https://images.pexels.com/photos/19809408/pexels-photo-19809408.jpeg", w: 1200, h: 1200 },
    "firozabad-chandelier-bench.webp": { url: "https://images.pexels.com/photos/8516783/pexels-photo-8516783.jpeg",   w: 1200, h: 1200 },
  },
  moradabad: {
    "moradabad-aerial.webp":       { url: "https://images.pexels.com/photos/33369529/pexels-photo-33369529.jpeg", w: 1600, h: 1067 },
    "moradabad-foundry-pour.webp": { url: "https://images.pexels.com/photos/19408700/pexels-photo-19408700.jpeg", w: 1600, h: 1067 },
    "moradabad-engraver.webp":     { url: "https://images.pexels.com/photos/16630111/pexels-photo-16630111.jpeg", w: 1200, h: 1200 },
    "moradabad-finishing.webp":    { url: "https://images.pexels.com/photos/25945094/pexels-photo-25945094.jpeg", w: 1200, h: 1200 },
  },
};

function download(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return download(res.headers.location).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode} ${url}`));
      const chunks = [];
      res.on("data", c => chunks.push(c));
      res.on("end", () => resolve(Buffer.concat(chunks)));
      res.on("error", reject);
    }).on("error", reject);
  });
}

let ok = 0, fail = 0;
for (const [hub, files] of Object.entries(MAP)) {
  const dir = path.join(ROOT, hub);
  await fs.mkdir(dir, { recursive: true });
  for (const [name, { url, w, h }] of Object.entries(files)) {
    const dst = path.join(dir, name);
    try {
      // back up the existing AI-generated file
      const bak = dst.replace(/\.webp$/, "-ai.webp.bak");
      if (await fs.stat(dst).catch(() => null) && !(await fs.stat(bak).catch(() => null))) {
        await fs.rename(dst, bak);
      }
      process.stdout.write(`  ↓ ${hub}/${name} ... `);
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
}
console.log(`\nDone: ${ok} ok, ${fail} failed`);
