# Leonardo AI Image Pipeline — Balaji Udhyog

Automated image generation for the whole site. The pipeline reads creative prompts from
`../assets/ai-image-prompts.md`, scans every page for the image paths it references (the filenames
defined in `../assets/image-map.md`), generates each one with the Leonardo REST API, and writes
optimised **WebP** into the correct `../assets/images/...` folder.

```
scripts/
├─ leonardo-config.js          # API key (from .env), models, engines, retry/poll, sizes
├─ prompt-enhancer.js          # premium realism + cinematic modifiers, anti-AI negatives
├─ download-generated-assets.js# download → resize/cover → WebP (sharp); standalone re-download
├─ generate-leonardo-images.js # orchestrator: parse → resolve → batch generate → download
├─ package.json                # deps (sharp) + npm scripts
├─ .env                        # YOUR KEY (gitignored — never commit)
└─ .env.example
```

---

## 1. Setup (once)

```bash
cd project/scripts
npm install            # installs sharp (for WebP conversion + resizing)
cp .env.example .env   # then paste your LEONARDO_API_KEY  (a key may already be present)
```

Get a key at **app.leonardo.ai → Settings → API Access**. The pipeline needs an **API**
subscription/credits (the website plan credits are separate from API credits).

> ⚠ **Security:** `.env` is gitignored. If a key was shared in chat, rotate it in the Leonardo
> dashboard. Never commit `.env`.

---

## 2. Validate before spending credits

```bash
npm run dry-run        # parses prompts, resolves a prompt for every image, prints the plan
```

This makes **no API calls**. It writes the full resolved plan to `.leonardo-plan.json` and prints a
rough credit estimate. Always dry-run first.

---

## 3. Run the generation

Generate **everything** (skips images that already exist on disk):

```bash
npm run generate
```

Generate **by priority** (recommended — fits a limited credit balance, gets the most visible images
first):

```bash
npm run p1     # Priority 1: hero, brassware, locks, bathroom, export logistics  (~8 images)
npm run p2     # Priority 2: hubs, product closeups, warehouse, packaging         (bulk)
npm run p3     # Priority 3: blog banners, gallery, team/factory                  (~21 images)
```

Re-running the same command **resumes**: existing `.webp` files are skipped, so only missing/failed
images are generated. Progress, retries, failures and a final summary print to the terminal; state
is saved to `.leonardo-manifest.json`.

---

## 4. Regenerate only one category / a single image

```bash
node generate-leonardo-images.js --only=brassware     # any path containing "brassware"
node generate-leonardo-images.js --only=hubs          # all hub imagery
node generate-leonardo-images.js --only=hero          # just the homepage hero panels
node generate-leonardo-images.js --only=team          # leadership portraits + offices
node generate-leonardo-images.js --only=items         # all 288 product-detail closeups
node generate-leonardo-images.js --only=brass-handles # one product collection

# force overwrite (regenerate even if the file exists):
node generate-leonardo-images.js --only=hero --force

# cap a run:
node generate-leonardo-images.js --priority=2 --limit=20
```

`--only` matches any substring of the image path, so category folders, hub names, product groups and
single slugs all work.

---

## 5. Swap models / engines

Defaults: **PhotoReal v2 + Alchemy + Cinematic**, guidance 7, on **Leonardo Vision XL**.

Per-run via flags:

```bash
node generate-leonardo-images.js --engine=phoenix                 # Leonardo Phoenix 1.0
node generate-leonardo-images.js --engine=kino                    # Kino XL (cinematic)
node generate-leonardo-images.js --engine=photoreal --model=albedoXL
node generate-leonardo-images.js --engine=sdxl --model=diffusionXL
```

Or set defaults in `.env`:

```
LEONARDO_ENGINE=phoenix
LEONARDO_MODEL=visionXL
LEONARDO_GUIDANCE=8
LEONARDO_CONCURRENCY=3
LEONARDO_WEBP_Q=82
```

| engine | model used | notes |
|---|---|---|
| `photoreal` (default) | visionXL / diffusionXL / albedoXL | PhotoReal v2 + Alchemy — best general photoreal |
| `phoenix` | Phoenix 1.0 | uses `contrast` (3.5); excellent realism, different param set |
| `kino` | Kino XL | cinematic film look |
| `sdxl` | any SDXL model | plain SDXL + Alchemy + preset style |

Model UUIDs live in `leonardo-config.js → MODELS` — add more there if needed.

---

## 6. Estimated API usage

- The site references **441 image files** (P1 8 · P2 412 · P3 21). The bulk is **288 per-SKU
  product-detail closeups** (`products/items/**`).
- Rough estimate at default settings (PhotoReal v2 + Alchemy, 1 image/gen): **~12 credits each →
  ~5,300 credits for the full set**. Actual cost is read from the API per generation and reported in
  the summary.
- **Check your balance first:** `node -e "import('./leonardo-config.js').then(async({apiKey,baseUrl})=>{const r=await fetch(baseUrl+'/me',{headers:{authorization:'Bearer '+apiKey}});console.log(await r.json())})"`
  (the `apiPaidTokens` field is your API credit balance).

**If your balance is below the full estimate**, do one of:
- run **P1 → P3 → P2** in chunks as credits allow (reruns skip done files);
- generate only the **~108 unique core images** and skip the per-SKU closeups
  (`--only` excludes `items` if you just don't run that group);
- lower cost per image: `--engine=sdxl` or set `LEONARDO_ALCHEMY=false` (less premium, cheaper);
- generate `--num=1` (already the default).

---

## 7. Download / convert only

If a run was interrupted after generation but before download, re-fetch from the manifest:

```bash
npm run download       # re-downloads any COMPLETE manifest entry whose .webp is missing
```

WebP conversion + cover-crop to the master size uses **sharp**. If sharp isn't installed, files are
saved in their original format (JPG/PNG) with a warning — install sharp and re-run `npm run download`
to convert.

---

## 8. Image guarantees (built into every prompt)

- Ultra-realistic, cinematic, commercial-photography quality, navy + warm-gold palette.
- **No text, logos, brand names** — forced into every negative prompt.
- **No cartoon/anime/3D/illustration** — forced into every negative prompt.
- Consistent luxury export-house look across the whole site (shared style modifiers).

---

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| `No LEONARDO_API_KEY found` | Add the key to `scripts/.env` (see `.env.example`). |
| `401/403` (auth) | Key invalid/expired or no API access — regenerate in the Leonardo dashboard. The run aborts on auth errors. |
| `429` rate limited | Handled automatically (honors `Retry-After`, exponential backoff). Lower `--concurrency` if persistent. |
| `create 400 …` | Usually a model/param mismatch. PhotoReal v2 needs a base model (visionXL/diffusionXL/albedoXL) + Alchemy — keep the default engine, or switch `--engine=phoenix`. |
| Out of credits | Run fewer images (`--priority`, `--only`, `--limit`) or top up API credits. The summary shows credits used. |
| Files saved as `.jpg` not `.webp` | `sharp` isn't installed → `npm install sharp`, then `npm run download`. |
| `poll timeout` | Leonardo was slow/queued. Re-run the same command (existing files skipped) to retry just the failures. |
| Want different framing | Edit the prompt block in `../assets/ai-image-prompts.md`, then `--only=<file> --force`. |

Generation state is in `.leonardo-manifest.json` (per-file status, generationId, url, credits). Delete
it to start fully fresh.
