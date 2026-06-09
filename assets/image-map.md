# Balaji Udhyog — Image Map

> Maps every website section/page to its image type, dimensions, filename, and the prompt that
> generates it. This is the single source of truth that the HTML `<img>` `src` paths follow.
> Prompts live in [`ai-image-prompts.md`](ai-image-prompts.md). Optimisation rules live in
> [`images/README.md`](images/README.md).

All paths are relative to `project/assets/images/`. In the HTML the `src` is prefixed by the page's
depth:

| Page location | Prefix to add before `assets/images/...` |
|---|---|
| `project/Balaji Udhyog.html` (home) | `assets/images/…` |
| `project/pages/*.html` | `../assets/images/…` |
| `project/pages/hubs/*.html`, `project/pages/products/*.html` | `../../assets/images/…` |

---

## 1. Filename & folder conventions

```
assets/images/
├─ hero/          homepage hero panels
├─ categories/    the 7 product-category hero stills (reused sitewide)
├─ products/<category>/   per-SKU closeups + per-page gallery strip
├─ hubs/<hub>/    aerial + interior atmosphere shots
├─ export/        logistics, warehouse, packaging, documentation
├─ gallery/       homepage gallery mosaic
├─ team/          leadership portraits + office exteriors
└─ blog/          journal feature + theme banners
```

**Naming rule** — lowercase, hyphen-separated, descriptive, no spaces/underscores:

```
<context>-<subject>[-<variant>].webp
```

- Category stills: `categories/<category>-hero.webp`
- SKU closeups: `products/<category>/<sku-code>-<slug>.webp` (e.g. `products/brassware/sku-401-decorative-brass-pots.webp`)
- Gallery strip (every product page): `products/<category>/gallery-{hero|detail-1|detail-2|lifestyle|packaging|container}.webp`
- Hub aerial: `hubs/<hub>/<hub>-aerial.webp`; interiors `hubs/<hub>/<hub>-<subject>.webp`
- Slug = label text lowercased, `& , / ' . ( )` removed, spaces → hyphens.

**`<category>` folder keys:** `brassware`, `metal-art-ware`, `furniture-hardware`, `locks-hardware`,
`bathroom-hardware`, `glassware`, `home-decor`.
**`<hub>` folder keys:** `moradabad`, `aligarh`, `firozabad` (site copy spells it "Muradabad").

---

## 2. Recommended dimensions per image type

Generate/upscale at the **master** size, then produce responsive variants per
[`images/README.md`](images/README.md). Aspect ratio is what matters; the container crops via CSS
`object-fit:cover`.

| Image type | Aspect | Master (px) | Notes |
|---|---|---|---|
| Homepage hero panel | 4:5 | 1080 × 1350 | Also export 16:9 crop; navy scrim overlaid |
| Category hero (large tile) | 16:10 | 1600 × 1000 | Brassware & Metal Art on home grid |
| Category hero (standard) | 4:5 | 1080 × 1350 | Other 5 categories on home grid |
| Product SKU closeup | 4:3 | 1200 × 900 | Square-ish crop in `.show .it .ph` |
| Product gallery hero | 16:10 | 1600 × 1000 | `.gal .gi.a` |
| Product gallery cell | 4:3 / 1:1 | 1200 × 900 | mosaic cells |
| Hub aerial banner | 4:3 | 1600 × 1200 | full-bleed on hub page |
| Hub interior | 4:3 | 1200 × 900 | atmosphere grid |
| Logistics / warehouse | 16:9 | 1600 × 900 | wide |
| Packaging / documentation | 4:3 | 1200 × 900 | |
| Gallery mosaic (home) | varies | 1200 × 900 | tall cells 4:5 |
| Leadership portrait | 4:5 | 1000 × 1250 | |
| Office exterior | 4:3 | 1200 × 900 | |
| Blog feature banner | 16:9 | 1600 × 900 | |
| Blog theme banner | 16:9 | 1280 × 720 | 4:3 crop for home journal |

---

## 3. Page-by-page map

### 3.1 `Balaji Udhyog.html` (Homepage)

| Section | Element | Image file | Prompt |
|---|---|---|---|
| Hero | `.h-img.left` | `hero/hero-brass-foundry-left.webp` | A1 |
| Hero | `.h-img.right` | `hero/hero-export-port-right.webp` | A2 |
| Categories | `.cat` Brassware | `categories/brassware-hero.webp` | B1 |
| Categories | `.cat` Metal Art Ware | `categories/metal-art-ware-hero.webp` | B2 |
| Categories | `.cat` Furniture Hardware | `categories/furniture-hardware-hero.webp` | B3 |
| Categories | `.cat` Locks & Hardware | `categories/locks-hardware-hero.webp` | B4 |
| Categories | `.cat` Bathroom Hardware | `categories/bathroom-hardware-hero.webp` | B5 |
| Categories | `.cat` Glassware | `categories/glassware-hero.webp` | B6 |
| Categories | `.cat` Home Decor | `categories/home-decor-hero.webp` | B7 |
| Hubs | `.hub-img` Muradabad | `hubs/moradabad/moradabad-aerial.webp` | C1.0 |
| Hubs | `.hub-img` Aligarh | `hubs/aligarh/aligarh-aerial.webp` | C2.0 |
| Hubs | `.hub-img` Firozabad | `hubs/firozabad/firozabad-aerial.webp` | C3.0 |
| Gallery | `.gi.a` brassware | `gallery/brassware-moradabad.webp` | B1 / C1 |
| Gallery | `.gi.b` cylinder locks | `gallery/cylinder-locks-aligarh.webp` | B4 |
| Gallery | `.gi.c` home decor | `gallery/home-decor.webp` | B7 |
| Gallery | `.gi.d` chandelier | `gallery/chandelier-firozabad.webp` | B6 / C3 |
| Gallery | `.gi.e` bathroom hardware | `gallery/bathroom-hardware.webp` | B5 |
| Gallery | `.gi.f` metal artware | `gallery/metal-artware.webp` | B2 |
| Gallery | `.gi.g` container loading | `gallery/container-loading-mundra.webp` | D1 |
| Blog | post 1 (market insight) | `blog/market-insight.webp` | I2 |
| Blog | post 2 (hub guide) | `blog/hub-guide.webp` | I2 |
| Blog | post 3 (directory) | `blog/directory.webp` | I2 |

### 3.2 `pages/Products.html`

`.visual .ph` tiles reuse the category heroes:

| Category corner | Image file | Prompt |
|---|---|---|
| 01 · Furniture Hardware | `categories/furniture-hardware-hero.webp` | B3 |
| 02 · Locks | `categories/locks-hardware-hero.webp` | B4 |
| 03 · Bathroom | `categories/bathroom-hardware-hero.webp` | B5 |
| 04 · Brassware | `categories/brassware-hero.webp` | B1 |
| 05 · Metal Art | `categories/metal-art-ware-hero.webp` | B2 |
| 06 · Glass (chandelier) | `categories/glassware-hero.webp` | B6 |
| 07 · Home Decor | `categories/home-decor-hero.webp` | B7 |

### 3.3 Product category pages (`pages/products/*.html`)

Each of the 7 pages has the same three image zones:

1. **Showcase SKU grid** (`.show .it .ph`, 9 tiles) → `products/<category>/<sku-code>-<slug>.webp`
   - Prompt: **F0 template** + the category's `{SUBJECT}` token list (F1–F7).
   - Example (Brassware): `sku-401-decorative-brass-pots.webp`, `sku-402-brass-idols-figurines.webp`,
     `sku-403-diya-oil-lamps.webp`, `sku-404-decorative-vases.webp`,
     `sku-405-candle-holders-t-light-stands.webp`, `sku-406-trays-bowls-platters.webp`,
     `sku-407-brass-tableware.webp`, `sku-408-wall-sconces-lighting.webp`,
     `sku-409-decorative-brass-animals.webp`.
2. **Gallery strip** (`.gal-grid`, 6 tiles) → `products/<category>/gallery-*.webp`
   - `gallery-hero.webp` (category prompt @16:10), `gallery-detail-1.webp`, `gallery-detail-2.webp`
     (F0 macro), `gallery-lifestyle.webp` (F7-style lifestyle), `gallery-packaging.webp` (**G1**),
     `gallery-container.webp` (**D2**).
3. **Related categories** (`.rel-row`, 3 tiles) → reuse the relevant `categories/<category>-hero.webp`.

### 3.4 Manufacturing hub pages (`pages/hubs/*.html`)

| Zone | Muradabad | Aligarh | Firozabad | Prompt |
|---|---|---|---|---|
| Aerial banner (`.cap`) | `hubs/moradabad/moradabad-aerial.webp` | `hubs/aligarh/aligarh-aerial.webp` | `hubs/firozabad/firozabad-aerial.webp` | C_.0 |
| Atmosphere 1 | `…/moradabad-foundry-pour.webp` | `…/aligarh-factory-floor.webp` | `…/firozabad-furnace.webp` | C_.1 |
| Atmosphere 2 | `…/moradabad-engraver.webp` | `…/aligarh-cylinder-assembly.webp` | `…/firozabad-chandelier-bench.webp` | C_.2 |
| Atmosphere 3 | `…/moradabad-finishing.webp` | `…/aligarh-qc-bench.webp` | `…/firozabad-crystal-cutter.webp` | C_.3 |
| Linked categories (`.lp-grid`) | reuse `categories/*-hero.webp` | same | same | B_ |

### 3.5 `pages/About.html`

| Zone | Image file | Prompt |
|---|---|---|
| Leadership · MD | `team/portrait-managing-director.webp` | H1 |
| Leadership · Operations | `team/portrait-operations-director.webp` | H1 |
| Leadership · Africa | `team/portrait-africa-head.webp` | H1 |
| Leadership · QC | `team/portrait-head-qc.webp` | H1 |
| Hub strip · Muradabad | `hubs/moradabad/moradabad-aerial.webp` | C1.0 |
| Hub strip · Aligarh | `hubs/aligarh/aligarh-aerial.webp` | C2.0 |
| Hub strip · Firozabad | `hubs/firozabad/firozabad-aerial.webp` | C3.0 |

### 3.6 `pages/Contact.html`

| Office | Image file | Prompt |
|---|---|---|
| HQ · Muradabad | `team/office-moradabad-facility.webp` | H2 |
| Export · Mundra | `team/office-mundra-warehouse.webp` | H2 |
| Africa · Lagos | `team/office-lagos.webp` | H2 |

### 3.7 `pages/Export Services.html`

| Service | Image file | Prompt |
|---|---|---|
| 01 Logistics | `export/container-loading-bay.webp` | D2 |
| 02 OEM / Private label | `export/branded-packaging-oem.webp` | G2 |
| 03 Packaging | `export/packaging-line.webp` | G3 |
| 04 Compliance | `export/documentation-desk.webp` | E2 |
| 05 Volume / consolidation | `export/consolidation-warehouse.webp` | D4 |
| 06 Last mile | `export/port-arrival-inland.webp` | D3 |

### 3.8 `pages/Blog.html`

| Slot | Image file | Prompt |
|---|---|---|
| Featured hero | `blog/feature-africa-import-shift.webp` | I1 |
| Article · Market Insight | `blog/market-insight.webp` | I2 |
| Article · Hub Guide | `blog/hub-guide.webp` | I2 |
| Article · Compliance | `blog/compliance.webp` | I2 |
| Article · Directory | `blog/directory.webp` | I2 |
| Article · Logistics | `blog/logistics.webp` | I2 |
| Article · OEM | `blog/oem.webp` | I2 |

### 3.9 `pages/Africa Market.html`

No raster images — this page renders an **inline SVG trade map**. Leave as-is. (Optional future
enhancement: a subtle `export/shipping-containers-mundra.webp` behind the dark map band.)

### 3.10 Product detail pages (`pages/products/items/*.html`)

Phase-2 product-detail pages (9 collections × 8 items = 72 SKUs) each use **1 hero + 3 detail** images:

```
assets/images/products/items/<group>/<slug>-hero.webp   (4:3, 1200×900 — PDP main + card + OG)
assets/images/products/items/<group>/<slug>-1.webp      (1:1, 600×600 — thumb / detail)
assets/images/products/items/<group>/<slug>-2.webp      (1:1, 600×600 — thumb / detail)
assets/images/products/items/<group>/<slug>-3.webp      (1:1, 600×600 — thumb / detail)
```

- `<group>` ∈ `brass-handles · cabinet-knobs · tower-bolts · door-locks · towel-holders · glass-decor ·
  wall-hooks · bathroom-accessories · furniture-hardware`
- `<slug>` = kebab-cased product name (e.g. `classic-brass-cabinet-handle`).
- **Prompt:** universal product-closeup template **F0** with `{SUBJECT}` = the product name; shoot the
  hero at 4:3 and the three details as tight macro crops (texture / finish / mounting).
- The **items index** (`pages/products/items/index.html`) and all product cards reuse each item's
  `-hero.webp`. Until generated, the gradient skeleton + `object-fit:cover` keep the layout intact.

---

## 4. Reused-image summary (generate once, reference many times)

| File | Used by |
|---|---|
| `categories/*-hero.webp` (×7) | Home category grid · Products list · product Related strips · hub Linked-category cards |
| `hubs/<hub>/<hub>-aerial.webp` (×3) | Home hub grid · About hub strip · hub page banner |
| `export/container-loading-bay.webp` | Export svc 01 · product gallery `container` slots |
| `gallery/container-loading-mundra.webp` | Home gallery wide tile |

Total **unique** images to generate ≈ **108** (7 categories + 2 hero + 9 hub + 63 SKU + 6×7−reuse
gallery + 6 export + 7 team + 7 blog + 7 gallery). Reuse keeps the real count manageable.
