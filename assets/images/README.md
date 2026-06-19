# Balaji Udhyog — Image Assets

Production image library for the Balaji Udhyog export website. Drop optimised assets here using the
structure and naming below. Creative prompts: [`../ai-image-prompts.md`](../ai-image-prompts.md).
Section-by-section placement: [`../image-map.md`](../image-map.md).

---

## 1. Folder structure

```
assets/images/
├─ hero/                       # homepage hero panels (above the fold)
├─ categories/                 # 7 product-category hero stills (reused sitewide)
├─ products/
│  ├─ brassware/               # per-SKU closeups + gallery strip
│  ├─ metal-art-ware/
│  ├─ furniture-hardware/
│  ├─ locks-hardware/
│  ├─ bathroom-hardware/
│  ├─ glassware/
│  └─ home-decor/
├─ hubs/
│  ├─ moradabad/               # aerial + interior atmosphere shots
│  ├─ aligarh/
│  └─ firozabad/
├─ export/                     # logistics, warehouse, packaging, documentation
├─ gallery/                    # homepage gallery mosaic
├─ team/                       # leadership portraits + office exteriors
└─ blog/                       # journal feature + theme banners
```

> Site copy spells the brass city **"Muradabad"**; the folder uses the canonical **`moradabad/`**.
> Same city — don't create both.

---

## 2. Naming system

Lowercase, hyphen-separated, descriptive. No spaces, no underscores, no capitals.

```
<context>-<subject>[-<variant>].<ext>
```

| Type | Pattern | Example |
|---|---|---|
| Category hero | `categories/<category>-hero.webp` | `categories/brassware-hero.jpg?v=9999` |
| SKU closeup | `products/<category>/<sku-code>-<slug>.webp` | `products/brassware/sku-401-decorative-brass-pots.webp` |
| Gallery strip | `products/<category>/gallery-<role>.webp` | `products/glassware/gallery-lifestyle.webp` |
| Hub aerial | `hubs/<hub>/<hub>-aerial.webp` | `hubs/aligarh/aligarh-aerial.webp` |
| Hub interior | `hubs/<hub>/<hub>-<subject>.webp` | `hubs/firozabad/firozabad-furnace.webp` |
| Logistics | `export/<subject>.webp` | `export/container-loading-bay.webp` |
| Portrait | `team/portrait-<role>.webp` | `team/portrait-head-qc.webp` |
| Blog | `blog/<theme>.webp` | `blog/compliance.webp` |

**Responsive variants** (optional, recommended — see §5) append a width suffix:

```
brassware-hero.jpg?v=9999          # master / fallback (≈1600w)
brassware-hero-1280.webp     # desktop
brassware-hero-768.webp      # tablet
brassware-hero-480.webp      # mobile
```

The HTML references the master file (`brassware-hero.jpg?v=9999`). To serve smaller files on small
screens, wire up `srcset`/`sizes` once the variants exist (snippet in §5).

---

## 3. Format & compression

Order of preference: **AVIF → WebP → JPEG**. Ship **WebP** as the primary format (the HTML uses
`.webp`); keep a JPEG master for archival/fallback.

| Image kind | Format | Target quality | Typical weight (master) |
|---|---|---|---|
| Photographic (heroes, hubs, logistics, lifestyle) | WebP | q 78–82 | 120–220 KB |
| Product closeups / detail | WebP | q 80–85 | 90–160 KB |
| Portraits | WebP | q 80 | 80–140 KB |
| Blog banners | WebP | q 78 | 110–180 KB |

Hard budgets: **no single image > 250 KB** after optimisation; hero panels combined **< 450 KB**.
Strip EXIF/metadata on export. Use 4:2:0 chroma subsampling for photos. sRGB color profile only.

### Convert & compress (pick one)

**Squoosh** (GUI, no install): drag in → WebP → quality ~80 → resize → download.

**cwebp (CLI):**
```bash
cwebp -q 80 -m 6 -mt input.jpg -o output.webp
```

**Sharp (Node, batch):**
```bash
npm i -g sharp-cli
# single master → webp
sharp -i master.jpg -o out.webp --webp-quality 80
# generate responsive set
for w in 480 768 1280; do sharp -i master.jpg resize $w -o "name-$w.webp" --webp-quality 80; done
```

**ImageMagick (batch):**
```bash
magick mogrify -format webp -quality 80 -strip *.jpg
```

---

## 4. Mobile optimisation rules

- **Largest dimension caps:** hero/banner ≤ 1600px wide; tiles/closeups ≤ 1200px; portraits ≤ 1000px.
  Never ship a 4000px camera/AI master to the browser.
- **Mobile target:** the layout shows category/product tiles full-width on phones — a **480w** and
  **768w** WebP variant is enough; keep each mobile variant **< 60 KB**.
- **Lazy loading:** every below-the-fold `<img>` already carries `loading="lazy"` + `decoding="async"`.
  Only the homepage hero panels load eagerly (`fetchpriority="high"`).
- **No layout shift (CLS):** every `<img>` has explicit `width`/`height` attributes; CSS handles the
  responsive display (`object-fit:cover`). Keep AI exports at the documented aspect ratio so the crop
  is predictable.
- **Art direction:** these are background-style crops, so a single source + `object-fit:cover` is
  correct — no per-breakpoint cropping needed. Just serve a smaller file, not a different composition.
- **Don't upscale in the browser:** if a container never renders wider than ~600px on mobile, the
  480w variant is plenty.

---

## 5. Wiring up responsive variants (optional enhancement)

The HTML ships with a single, robust `<img>` per slot (always works once the master `.webp` exists).
After you generate the width variants in §2, upgrade any slot to true responsive delivery by adding
`srcset` + `sizes` — **only reference files you've actually produced**:

```html
<img class="img-cover"
     src="../../assets/images/categories/brassware-hero.jpg?v=9999"
     srcset="../../assets/images/categories/brassware-hero-480.webp 480w,
             ../../assets/images/categories/brassware-hero-768.webp 768w,
             ../../assets/images/categories/brassware-hero-1280.webp 1280w,
             ../../assets/images/categories/brassware-hero.jpg?v=9999 1600w"
     sizes="(max-width: 560px) 100vw, (max-width: 980px) 50vw, 33vw"
     alt="Handcrafted brassware from Muradabad — Balaji Udhyog export catalogue"
     width="1600" height="1000" loading="lazy" decoding="async">
```

For an AVIF + WebP + JPEG fallback chain, wrap in `<picture>`:

```html
<picture>
  <source type="image/avif" srcset="…-1280.avif 1280w, ….avif 1600w" sizes="…">
  <source type="image/webp" srcset="…-1280.webp 1280w, ….webp 1600w" sizes="…">
  <img class="img-cover" src="….jpg" alt="…" width="1600" height="1000" loading="lazy" decoding="async">
</picture>
```

---

## 6. Quality bar (before committing an asset)

- [ ] Correct path & filename per [`../image-map.md`](../image-map.md)
- [ ] WebP, sRGB, EXIF stripped, ≤ 250 KB, at the documented aspect ratio
- [ ] No text/logos/readable labels baked into the image (brand DNA rule)
- [ ] Reads as real photography, navy + warm-gold palette, premium editorial
- [ ] Subject sits clear of the navy scrim / tag chip / caption zone for that slot
