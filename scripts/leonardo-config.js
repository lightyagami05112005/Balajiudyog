// leonardo-config.js
// Central configuration for the Balaji Udyog Leonardo AI image pipeline.
// - Loads the API key from the environment (or a local, gitignored .env).
// - Defines model/engine presets, aspect-ratio + master-size presets,
//   retry / rate-limit / polling behaviour, and the generation-body builder.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const PROJECT_ROOT = path.resolve(__dirname, '..');           // .../project
export const IMAGES_DIR = path.join(PROJECT_ROOT, 'assets', 'images');
export const PROMPTS_MD = path.join(PROJECT_ROOT, 'assets', 'ai-image-prompts.md');
export const IMAGE_MAP_MD = path.join(PROJECT_ROOT, 'assets', 'image-map.md');
export const MANIFEST = path.join(__dirname, '.leonardo-manifest.json');

/* --------------------------------------------------------------------------
   Minimal .env loader (no dependency). Looks in cwd, the scripts dir, and the
   project dir. Does NOT overwrite variables already set in the environment.
   -------------------------------------------------------------------------- */
function loadEnv() {
  const candidates = [
    path.join(process.cwd(), '.env'),
    path.join(__dirname, '.env'),
    path.join(PROJECT_ROOT, '.env'),
  ];
  for (const file of candidates) {
    try {
      if (!fs.existsSync(file)) continue;
      for (const raw of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
        const line = raw.trim();
        if (!line || line.startsWith('#')) continue;
        const m = line.match(/^([A-Za-z0-9_]+)\s*=\s*(.*)$/);
        if (!m) continue;
        const key = m[1];
        let val = m[2].trim().replace(/^["']|["']$/g, '');
        if (!(key in process.env)) process.env[key] = val;
      }
    } catch { /* ignore unreadable .env */ }
  }
}
loadEnv();

export const apiKey = (process.env.LEONARDO_API_KEY || '').trim();
export const baseUrl = process.env.LEONARDO_BASE_URL || 'https://cloud.leonardo.ai/api/rest/v1';

/* --------------------------------------------------------------------------
   Model catalogue. UUIDs are stable Leonardo platform model IDs.
   PhotoReal v2 must pair with one of: visionXL / diffusionXL / albedoXL.
   -------------------------------------------------------------------------- */
export const MODELS = {
  visionXL:     '5c232a9e-9061-4777-980a-ddc8e65647c6', // Leonardo Vision XL
  diffusionXL:  '1e60896f-3c26-4296-8ecc-53e2afecc132', // Leonardo Diffusion XL
  kinoXL:       'aa77f04e-3eec-4034-9c07-d0f619684628', // Leonardo Kino XL (cinematic)
  albedoXL:     '2067ae52-33fd-4a82-bb92-c2c55e7d2786', // AlbedoBase XL
  phoenix:      'de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3', // Leonardo Phoenix 1.0
  lightningXL:  'b24e16ff-06e3-43eb-8d33-4416c2d75876', // Leonardo Lightning XL (fast)
  lucidRealism: '05ce0082-2d80-4a2d-8653-4d1c85e2418e', // Lucid Realism (Leonardo's photoreal)
  fluxSchnell:  '1dd50843-d653-4516-a8e3-f0238ee453ff', // Flux Schnell (fast, cheap ~1–2 credits)
  fluxDev:      'b2614463-296c-462a-9586-aafdb8f00e36', // Flux Dev (better, costlier)
};

/* --------------------------------------------------------------------------
   Tunable runtime config. Anything here can also be overridden by CLI flags
   (see generate-leonardo-images.js) or environment variables.
   -------------------------------------------------------------------------- */
export const config = {
  // engine: 'photoreal' (PhotoReal v2 + Alchemy, best general photoreal),
  //         'phoenix'   (Leonardo Phoenix 1.0, uses `contrast`),
  //         'kino'      (Kino XL cinematic), 'sdxl' (plain SDXL model).
  engine: process.env.LEONARDO_ENGINE || 'sdxl',
  // base model used by photoreal / sdxl engines (key in MODELS):
  model: process.env.LEONARDO_MODEL || 'visionXL',

  guidanceScale: clampNum(process.env.LEONARDO_GUIDANCE, 7, 1, 20),
  numImages: clampNum(process.env.LEONARDO_NUM, 1, 1, 8),
  // Multi-variation: generate N candidates per slot, keep the most realistic one.
  variations: clampNum(process.env.LEONARDO_VARIATIONS, 3, 1, 5),
  // Reject a generation whose best candidate scores below this (0–100). One regen retry.
  realismThreshold: clampNum(process.env.LEONARDO_REALISM_MIN, 50, 0, 100),
  alchemy: process.env.LEONARDO_ALCHEMY !== 'false', // Alchemy on (improves coherence)
  // Natural / documentary look — minimise stylisation. Per-image preset is set by
  // realism-enhancer.js; this is the fallback. (UNPROCESSED/RAW/NEUTRAL ≈ no "beauty" grade.)
  presetStyle: process.env.LEONARDO_STYLE || 'PHOTOGRAPHY',
  contrast: 3.0,        // Phoenix engine (1.0–4.5)
  highContrast: false,  // OFF — natural exposure, not punchy "AI" contrast

  concurrency: clampNum(process.env.LEONARDO_CONCURRENCY, 3, 1, 8),
  retry: { retries: 4, baseDelayMs: 2500, maxDelayMs: 45000 },
  poll:  { intervalMs: 4000, timeoutMs: 240000 },
  webp:  { quality: clampNum(process.env.LEONARDO_WEBP_Q, 80, 40, 100) },

  // Rough credit estimate per image (PhotoReal v2 + Alchemy, ~1 MP).
  // Used only for the dry-run cost preview — actual cost is read from the API.
  estCreditsPerImage: 24,

  // Generation dimensions sent to the API (must be multiples of 8).
  aspect: {
    '16:10':     { w: 1280, h: 800 },
    '16:9':      { w: 1280, h: 720 },
    '4:5':       { w: 1024, h: 1280 },
    '4:3':       { w: 1200, h: 896 },
    '1:1':       { w: 1024, h: 1024 },
    'heropanel': { w: 1024, h: 1280 },
  },

  // Smaller dims for Flux engine — keeps per-image cost at ~1–2 credits.
  // Sharp resizes to the master size on save, so display quality is unaffected.
  aspectFlux: {
    '16:10':     { w: 1024, h: 640 },
    '16:9':      { w: 1024, h: 576 },
    '4:5':       { w: 768,  h: 960 },
    '4:3':       { w: 1024, h: 768 },
    '1:1':       { w: 896,  h: 896 },
    'heropanel': { w: 768,  h: 960 },
  },

  // Final on-disk WebP master sizes (we resize/cover-crop to these).
  master: {
    '16:10':     { w: 1600, h: 1000 },
    '16:9':      { w: 1600, h: 900 },
    '4:5':       { w: 1080, h: 1350 },
    '4:3':       { w: 1200, h: 900 },
    '1:1':       { w: 1000, h: 1000 },
    'heropanel': { w: 1080, h: 1350 },
  },
};

function clampNum(v, dflt, min, max) {
  const n = Number(v);
  if (!Number.isFinite(n)) return dflt;
  return Math.min(max, Math.max(min, n));
}

export function masterSize(ratio) {
  return config.master[ratio] || config.master['4:3'];
}

/* --------------------------------------------------------------------------
   Build the POST /generations request body for a resolved job.
   Branches per engine so each model receives valid parameters.
   -------------------------------------------------------------------------- */
export function buildGenerationBody(job) {
  const dims = config.aspect[job.ratio] || config.aspect['4:3'];
  const base = {
    prompt: job.prompt,
    negative_prompt: job.negative,
    width: dims.w,
    height: dims.h,
    // 1 image per call — variations are requested as separate generations in the
    // worker, because Alchemy caps images-per-generation at higher resolutions.
    num_images: 1,
  };

  switch (config.engine) {
    case 'phoenix':
      // Phoenix 1.0 uses `contrast` (not guidance_scale).
      return {
        ...base,
        modelId: MODELS.phoenix,
        contrast: config.contrast,
        alchemy: config.alchemy,
        enhancePrompt: false,
      };

    case 'kino':
      return {
        ...base,
        modelId: MODELS.kinoXL,
        guidance_scale: config.guidanceScale,
        alchemy: config.alchemy,
        presetStyle: job.presetStyle || config.presetStyle,
        highContrast: config.highContrast,
      };

    case 'sdxl':
      return {
        ...base,
        modelId: MODELS[config.model] || MODELS.visionXL,
        guidance_scale: config.guidanceScale,
        alchemy: config.alchemy,
        presetStyle: job.presetStyle || config.presetStyle,
        highContrast: config.highContrast,
      };

    case 'flux': {
      // Flux Schnell — cheapest (~1–2 credits). No alchemy/photoReal/presetStyle.
      // Flux endpoints do NOT accept negative_prompt — bake the most important
      // negatives into the positive prompt as "avoid: …".
      const fd = config.aspectFlux[job.ratio] || config.aspectFlux['4:3'];
      const negTail = job.negative ? ' Avoid: ' + job.negative.slice(0, 420) : '';
      const fluxPrompt = (job.prompt + negTail).slice(0, 1480);
      return {
        modelId: MODELS[config.model === 'fluxDev' ? 'fluxDev' : 'fluxSchnell'],
        prompt: fluxPrompt,
        width: fd.w,
        height: fd.h,
        num_images: 1,
        contrast: 3.0,
      };
    }

    case 'lucid': {
      // Lucid Realism — Leonardo's modern photoreal model. Mid-priced (~3–5 credits).
      return {
        ...base,
        modelId: MODELS.lucidRealism,
        guidance_scale: config.guidanceScale,
        contrast: config.contrast,
      };
    }

    case 'photoreal':
    default:
      // PhotoReal v2 — requires alchemy:true, a base modelId and a presetStyle.
      return {
        ...base,
        modelId: MODELS[config.model] || MODELS.visionXL,
        guidance_scale: config.guidanceScale,
        photoReal: true,
        photoRealVersion: 'v2',
        alchemy: true,
        presetStyle: job.presetStyle || config.presetStyle,
        highContrast: config.highContrast,
      };
  }
}
