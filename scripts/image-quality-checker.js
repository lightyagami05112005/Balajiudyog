// image-quality-checker.js
// ---------------------------------------------------------------------------
// Heuristic realism scorer. No ML model — it uses fast pixel statistics (via
// sharp) that correlate with the tell-tale signs of over-"AI"/over-processed
// images, and produces a 0–100 realism score plus human-readable flags.
//
// Signals penalised:
//   • oversaturation              (AI gold/teal pop)
//   • oversaturated GOLD cast     (the brief's specific complaint)
//   • blown highlights            (fake glossy specular / synthetic HDR)
//   • crushed shadows             (overprocessed look)
//   • too smooth / plasticky      (low micro-detail → "rendered")
//   • over-sharpened / haloed     (very high micro-contrast → "AI crisp")
//
// Used to (a) rank the N variations of a generation and keep the most realistic,
// and (b) reject a generation whose best candidate is still clearly synthetic.
// ---------------------------------------------------------------------------

let sharp = null;
try { sharp = (await import('sharp')).default; } catch { /* scoring disabled */ }

export const hasSharp = !!sharp;

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
// penalty that ramps from 0 at `lo` to `max` at `hi`
const ramp = (v, lo, hi, max) => v <= lo ? 0 : v >= hi ? max : ((v - lo) / (hi - lo)) * max;

/**
 * Score an image buffer for "realism".
 * @returns {Promise<{score:number, flags:string[], metrics:object}>}
 */
export async function scoreImageBuffer(buf) {
  if (!sharp) return { score: 50, flags: ['no-sharp'], metrics: {} };

  // small grayscale-ish raw sample for fast per-pixel math
  const N = 192;
  const { data, info } = await sharp(buf)
    .resize(N, N, { fit: 'fill' })
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const px = info.width * info.height;
  const lum = new Float32Array(px);
  let satSum = 0, hiClip = 0, loClip = 0, goldCount = 0;

  for (let i = 0, p = 0; i < data.length; i += 3, p++) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
    const l = 0.299 * r + 0.587 * g + 0.114 * b;
    lum[p] = l;
    satSum += mx === 0 ? 0 : (mx - mn) / mx;        // HSV saturation
    if (l > 247) hiClip++;
    if (l < 6) loClip++;
    // warm "gold" cast: red & green high, blue low, and saturated
    if (r > 165 && g > 120 && b < 110 && (mx - mn) > 60) goldCount++;
  }
  const satMean = satSum / px;
  const hiFrac = hiClip / px;
  const loFrac = loClip / px;
  const goldFrac = goldCount / px;

  // micro-detail via Laplacian variance on luminance (texture realism)
  let lapSum = 0, lapSq = 0, n = 0;
  const W = info.width, H = info.height;
  for (let y = 1; y < H - 1; y++) {
    for (let x = 1; x < W - 1; x++) {
      const idx = y * W + x;
      const lap = 4 * lum[idx] - lum[idx - 1] - lum[idx + 1] - lum[idx - W] - lum[idx + W];
      lapSum += lap; lapSq += lap * lap; n++;
    }
  }
  const lapVar = lapSq / n - (lapSum / n) ** 2;

  // ---- scoring ----
  const flags = [];
  let score = 100;

  // oversaturation (natural commercial photos sit ~0.15–0.40)
  const pSat = ramp(satMean, 0.42, 0.70, 26);
  if (pSat > 6) flags.push(`oversaturated(${satMean.toFixed(2)})`);
  score -= pSat;

  // oversaturated gold cast (explicit brief complaint)
  const pGold = ramp(goldFrac, 0.22, 0.55, 22);
  if (pGold > 5) flags.push(`gold-cast(${(goldFrac * 100).toFixed(0)}%)`);
  score -= pGold;

  // blown highlights → fake glossy / synthetic HDR
  const pHi = ramp(hiFrac, 0.05, 0.20, 22);
  if (pHi > 5) flags.push(`blown-highlights(${(hiFrac * 100).toFixed(0)}%)`);
  score -= pHi;

  // crushed shadows → overprocessed
  const pLo = ramp(loFrac, 0.10, 0.35, 12);
  if (pLo > 4) flags.push(`crushed-shadows(${(loFrac * 100).toFixed(0)}%)`);
  score -= pLo;

  // micro-detail band: too low = plasticky/rendered, too high = over-sharpened.
  // (Alchemy photos legitimately carry strong micro-detail; only flag genuinely
  //  crunchy/haloed output above ~520 on the 192px Laplacian-variance proxy.)
  if (lapVar < 14) { score -= ramp(14 - lapVar, 0, 12, 18); flags.push(`too-smooth(${lapVar.toFixed(0)})`); }
  else if (lapVar > 520) { score -= ramp(lapVar - 520, 0, 500, 16); flags.push(`over-sharpened(${lapVar.toFixed(0)})`); }

  score = Math.round(clamp(score, 0, 100));
  return {
    score,
    flags,
    metrics: {
      satMean: +satMean.toFixed(3), goldFrac: +goldFrac.toFixed(3),
      hiFrac: +hiFrac.toFixed(3), loFrac: +loFrac.toFixed(3), lapVar: +lapVar.toFixed(1),
    },
  };
}

/**
 * Pick the most realistic candidate from a list of image buffers.
 * @returns {Promise<{index:number, score:number, scores:object[]}>}
 */
export async function pickBest(buffers) {
  const scores = [];
  for (const b of buffers) scores.push(await scoreImageBuffer(b));
  let best = 0;
  for (let i = 1; i < scores.length; i++) if (scores[i].score > scores[best].score) best = i;
  return { index: best, score: scores[best].score, scores };
}
