# Balaji Udhyog — Leonardo AI Image Prompt Library

> Premium AI image generation pipeline for the Balaji Udhyog export website.
> Every prompt is engineered to read as a **real international trade-house photoshoot** —
> not stock photography, not "AI art". Photoreal, cinematic, editorial.

---

## 0. How to use this file

1. Open **Leonardo AI** → Image Generation.
2. Pick the model named in each block (default: **Leonardo Phoenix 1.0**, or **Photoreal v2** for product closeups).
3. Paste the **Main Prompt** and the **Negative Prompt**.
4. Set the **Aspect Ratio** and apply the **Suggested Leonardo Settings**.
5. Generate 4 variations, pick the strongest, run **Universal Upscaler (High-Res / Crisp, 2×)**.
6. Export, then follow the optimisation rules in [`images/README.md`](images/README.md) (convert to WebP, resize per breakpoint, compress).
7. Save into the path given under **Placement** — filenames are listed exhaustively in [`image-map.md`](image-map.md).

> **City spelling note:** the live site uses the spelling *"Muradabad"* throughout its copy. The
> canonical / international spelling is *"Moradabad"* — image folders use `moradabad/`. Both refer to
> the same brass city in Uttar Pradesh. Keep prompt text as written below.

---

## 1. Brand DNA (the style anchor in every prompt)

Every prompt is built on this shared visual signature. If you write new prompts, keep this spine:

- **Aesthetic:** luxury Indian export house · premium editorial industrial · international trade atmosphere
- **Palette:** deep navy (#0a1d3a / #06122a), warm brushed gold & brass (#c8a55b), warm paper neutrals (#f5f2ec)
- **Light:** cinematic, directional, soft key + warm rim light; golden-hour or controlled studio; gentle volumetric haze
- **Texture:** real material grain — hammered brass, cut crystal, brushed steel, kraft packaging, weathered concrete, ocean-container steel
- **Mood:** confident, established, craftsmanship-meets-scale, quietly expensive
- **Camera language:** full-frame DSLR / medium-format look, 35mm–85mm primes, shallow-to-medium depth of field, natural perspective
- **Never:** logos, brand names, readable text, flags, faces of real people, garish saturation, plastic CGI sheen, generic stock-photo staging

### 1.1 Global Negative Prompt (reusable base)

Append the per-prompt negatives to this base every time:

```
text, words, letters, typography, watermark, logo, brand name, signage, label,
caption, signature, UI, frame border, deformed, distorted, disfigured, mutated,
extra fingers, extra limbs, bad anatomy, low quality, lowres, blurry, out of focus,
jpeg artifacts, noise, oversaturated, neon colors, HDR halo, overexposed, plastic skin,
waxy, CGI, 3d render, video game, illustration, cartoon, anime, painting, sketch,
stock photo overlay, cluttered, messy, dirty lens, duplicate, cropped subject, tiling
```

### 1.2 Global Leonardo baseline (override per block)

| Setting | Baseline value |
|---|---|
| Model | Leonardo Phoenix 1.0 (closeups: Photoreal v2) |
| Preset Style | Cinematic |
| Generation Mode | Quality |
| Contrast | Medium–High |
| Guidance / CFG | 7 |
| Alchemy | On (off for Phoenix) |
| PromptMagic | Off |
| Upscale | Universal Upscaler · Crisp · 2× |
| Images per run | 4 |

---

# A. HOMEPAGE HERO

### A1 — Hero · Left panel (brass foundry / craftsmanship)
**Main Prompt**
```
Cinematic wide editorial photograph inside a premium Indian brass foundry at golden hour,
master artisan hands lifting a glowing hand-cast brass vessel with long tongs, sparks and warm
molten light, deep navy shadows pooling in the background, brushed gold highlights on hammered
metal, soft volumetric haze, shafts of warm directional light through high factory windows,
shallow depth of field, full-frame 35mm look, rich contrast, luxury industrial trade-house mood,
photoreal, ultra detailed material texture
```
**Negative Prompt** — *base +* `cold blue tint, modern factory robots, clean sci-fi lab, watermark`
**Aspect Ratio** — 4:5 (portrait panel) · also export a 16:9 crop
**Leonardo Settings** — Phoenix 1.0 · Cinematic · Contrast High · CFG 7 · Upscale 2× · 4 images
**Placement** — Homepage `Balaji Udhyog.html`, hero background `.h-img.left` → `assets/images/hero/hero-brass-foundry-left.webp`. Has a navy gradient scrim on top, so keep the lit subject in the upper-left third.

### A2 — Hero · Right panel (export port / containers)
**Main Prompt**
```
Cinematic wide photograph of an Indian export seaport at blue-hour dusk, stacks of shipping
containers in deep navy and warm amber, a gantry crane silhouette, distant cargo vessel, faint
golden dock lights reflecting on still water, layered atmospheric haze, premium international
trade atmosphere, controlled cool-warm color contrast with gold accents, full-frame wide lens,
photoreal, high dynamic range handled naturally, editorial industrial grandeur
```
**Negative Prompt** — *base +* `daytime harsh sun, busy crowds, readable container codes, text on containers, oversaturated sky`
**Aspect Ratio** — 4:5 (portrait panel) · also export 16:9
**Leonardo Settings** — Phoenix 1.0 · Cinematic · Contrast High · CFG 6.5 · Upscale 2× · 4 images
**Placement** — Homepage hero `.h-img.right` → `assets/images/hero/hero-export-port-right.webp`. This panel is hidden on mobile; keep composition readable when cropped vertically.

> **Sub-page heroes** (`.cat-hero`, `.page-hero`, `.hub-hero`) are textured navy gradients by design and stay as-is. If you later want a photographic hero behind them, reuse the matching category/hub image at low opacity behind the existing dark scrim — see `image-map.md`.

---

# B. PRODUCT CATEGORIES (homepage tiles + reused sitewide)

These seven images are the spine of the catalogue. The same file is reused on the homepage category grid, the Products listing, the related-category strips, and hub "products from here" cards — so shoot them as definitive category hero stills.

### B1 — Brassware (signature)
**Main Prompt**
```
Editorial product hero photograph of a curated arrangement of handcrafted Indian brassware —
an engraved brass surahi pot, an oil lamp and a hammered bowl — on a dark brushed-stone surface,
deep navy backdrop, single warm key light raking across the engraving to reveal texture, soft
gold reflections, museum-grade still-life lighting, shallow depth of field, full-frame 85mm,
photoreal, luxury catalogue quality, warm brass tones against navy
```
**Negative Prompt** — *base +* `religious iconography focus, cheap gift-shop staging, harsh flash, white seamless studio`
**Aspect Ratio** — 16:10 (large tile) — see image-map for crops
**Leonardo Settings** — Photoreal v2 · Cinematic · Contrast High · CFG 7 · Upscale 2×
**Placement** — `assets/images/categories/brassware-hero.jpg?v=9999`

### B2 — Metal Art Ware
**Main Prompt**
```
Editorial photograph of a sculptural handcrafted metal wall-art piece and a freestanding brass
sculpture in a luxury gallery setting, warm directional gallery lighting, deep navy plastered
wall, brushed gold and patinated copper tones, fine hand-worked metal texture, soft shadow play,
full-frame 50mm, shallow depth of field, premium hospitality decor mood, photoreal, ultra detailed
```
**Negative Prompt** — *base +* `mass-produced look, cluttered shelf, plastic, neon`
**Aspect Ratio** — 16:10
**Leonardo Settings** — Photoreal v2 · Cinematic · Contrast Medium-High · CFG 7 · Upscale 2×
**Placement** — `assets/images/categories/metal-art-ware-hero.jpg?v=12345?v=999`

### B3 — Furniture Hardware
**Main Prompt**
```
Premium macro-leaning product photograph of precision furniture hardware — solid bar pull handles,
a soft-close cabinet hinge and brushed-brass knobs arranged on a warm walnut and concrete surface,
deep navy background, crisp directional studio light catching the brushed-metal grain, engineering
elegance, shallow depth of field, full-frame 100mm macro look, photoreal, catalogue-grade, warm
gold and steel against navy
```
**Negative Prompt** — *base +* `cheap plastic fittings, blister pack, hardware-store clutter, readable packaging`
**Aspect Ratio** — 4:5 (standard tile)
**Leonardo Settings** — Photoreal v2 · Cinematic · Contrast High · CFG 7 · Upscale 2×
**Placement** — `assets/images/categories/furniture-hardware-hero.jpg?v=999`

### B4 — Locks & Hardware
**Main Prompt**
```
Cinematic product photograph of premium security hardware — a precision-engineered brass cylinder
lock, a heavy mortise lockset and a polished padlock arranged on dark brushed steel, deep navy
backdrop, dramatic single-source rim light defining the machined edges, exposed pin detail, cool
metal with warm gold accents, shallow depth of field, full-frame 85mm, photoreal, industrial luxury,
ultra detailed machining texture
```
**Negative Prompt** — *base +* `toy lock, plastic, rusty cheap padlock, readable brand stamp, keys with text`
**Aspect Ratio** — 4:5
**Leonardo Settings** — Photoreal v2 · Cinematic · Contrast High · CFG 7 · Upscale 2×
**Placement** — `assets/images/categories/locks-hardware-hero.jpg?v=999`

### B5 — Bathroom Hardware
**Main Prompt**
```
Luxury editorial photograph of premium bathroom hardware — a single-lever basin faucet and matching
towel bar in brushed gold and matte black, mounted in a refined dark-stone bathroom vignette, soft
diffused daylight with a warm key, water-bead realism on the spout, deep navy and warm neutral tones,
shallow depth of field, full-frame 50mm, photoreal, five-star hotel sanitaryware mood, ultra detailed
finish
```
**Negative Prompt** — *base +* `cheap chrome, plastic faucet, builder-grade fittings, water spots as dirt, readable label`
**Aspect Ratio** — 4:5
**Leonardo Settings** — Photoreal v2 · Cinematic · Contrast Medium-High · CFG 7 · Upscale 2×
**Placement** — `assets/images/categories/bathroom-hardware-hero.webp`

### B6 — Glassware
**Main Prompt**
```
Editorial photograph of a hand-blown crystal chandelier and cut-glass decanter catching warm
backlight, deep navy darkroom backdrop, light refracting through faceted crystal into soft gold
sparkle, controlled flare, jewel-like clarity, shallow depth of field, full-frame 85mm, photoreal,
Firozabad luxury glass mood, ultra detailed refraction and caustics
```
**Negative Prompt** — *base +* `plastic glass, cheap pressed glass, foggy, dirty, broken edges, rainbow oversaturation`
**Aspect Ratio** — 4:5
**Leonardo Settings** — Photoreal v2 · Cinematic · Contrast High · CFG 6.5 · Upscale 2×
**Placement** — `assets/images/categories/glassware-hero.jpg?v=99999`

### B7 — Home Decor
**Main Prompt**
```
Warm editorial lifestyle photograph of a curated home-decor vignette — a framed mirror, brass
candle holders and a decorative bowl styled on a console against a deep navy plastered wall, soft
golden-hour window light, layered warm neutral textures, refined and uncluttered, shallow depth of
field, full-frame 35mm, photoreal, premium retail styling, quietly expensive
```
**Negative Prompt** — *base +* `cluttered shelf, dollar-store props, busy patterns, plastic flowers, readable text`
**Aspect Ratio** — 4:5
**Leonardo Settings** — Phoenix 1.0 · Cinematic · Contrast Medium-High · CFG 7 · Upscale 2×
**Placement** — `assets/images/categories/home-decor-hero.webp`

---

# C. MANUFACTURING HUBS

Each hub needs **one aerial establishing shot** (reused on homepage hub grid, About hub-strip, and the hub page banner) plus **three interior atmosphere shots** for the hub page's "factory floor" section.

## C1 — Moradabad (brass capital)

### C1.0 — Aerial establishing shot
**Main Prompt**
```
Cinematic aerial photograph at golden hour over a dense historic Indian brass-craft district in
Uttar Pradesh, low-rise foundry rooftops with thin chimney haze, warm terracotta and brass-gold
tones bleeding into deep navy evening shadow, layered atmospheric depth, established craft-city
scale, drone perspective, photoreal, editorial documentary grandeur, no readable signage
```
**Negative Prompt** — *base +* `modern skyscrapers, western city, clean industrial park, readable signs, crowds`
**Aspect Ratio** — 4:3 (banner / card)
**Leonardo Settings** — Phoenix 1.0 · Cinematic · Contrast High · CFG 6.5 · Upscale 2×
**Placement** — `assets/images/hubs/moradabad/moradabad-aerial.webp`

### C1.1 — Foundry · molten brass pour
**Main Prompt**
```
Dramatic editorial photograph of a molten brass pour inside a traditional Indian foundry, glowing
orange-gold liquid metal streaming into a sand mould, artisan hands and tools in deep navy shadow,
sparks and warm volumetric light, intense material realism, shallow depth of field, full-frame 35mm,
photoreal, cinematic industrial craftsmanship
```
**Negative Prompt** — *base +* `cold lighting, modern automated factory, safety-poster look, readable text`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/moradabad/moradabad-foundry-pour.webp`

### C1.2 — Engraver at workstation
**Main Prompt**
```
Intimate editorial photograph of a master engraver hand-chasing a fine decorative pattern into a
brass vessel at a worn wooden workbench, warm focused task light, brass shavings, deeply textured
hands and metal, deep navy surrounding shadow, shallow depth of field, full-frame 85mm, photoreal,
heritage craftsmanship, dignified and premium
```
**Negative Prompt** — *base +* `staged model, clean studio, gloves with logos, readable text`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/moradabad/moradabad-engraver.webp`

### C1.3 — Finishing & polishing line
**Main Prompt**
```
Editorial photograph of a brass finishing and polishing line, rows of gleaming hand-buffed brass
pieces catching warm light, soft motion of polishing wheels, deep navy industrial backdrop with
gold highlights, atmospheric dust haze, shallow depth of field, full-frame 50mm, photoreal,
craftsmanship-at-scale, luxury export quality
```
**Negative Prompt** — *base +* `messy clutter, cold fluorescent, plastic bins with text`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/moradabad/moradabad-finishing.webp`

## C2 — Aligarh (lock & hardware capital)

### C2.0 — Aerial establishing shot
**Main Prompt**
```
Cinematic aerial photograph at golden hour over a dense Indian hardware-manufacturing district in
Aligarh, low-rise lock factories and workshops, warm metallic-grey and gold tones into deep navy
evening shadow, industrial craft-city scale, thin haze, drone perspective, photoreal, editorial
documentary mood, no readable signage
```
**Negative Prompt** — *base +* `glass skyscrapers, western suburb, readable signs`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/aligarh/aligarh-aerial.webp`

### C2.1 — Lock factory floor
**Main Prompt**
```
Editorial photograph of an Indian precision lock-manufacturing floor, rows of brass and steel
lock bodies on work trays, machinist hands at a lathe in soft focus, warm key light with cool
steel ambiance, deep navy shadows and gold metal glints, shallow depth of field, full-frame 35mm,
photoreal, engineering-grade industrial craftsmanship
```
**Negative Prompt** — *base +* `cold sterile lab, robots only, readable machine text, clutter`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/aligarh/aligarh-factory-floor.webp`

### C2.2 — Cylinder pin assembly
**Main Prompt**
```
Macro editorial photograph of a brass pin-tumbler cylinder lock being hand-assembled, tiny precision
pins and springs, tweezers, machined brass detail razor-sharp in focus, warm directional light, deep
navy bokeh background, full-frame 100mm macro, photoreal, precision-engineering luxury, ultra detailed
```
**Negative Prompt** — *base +* `oversized cartoon parts, plastic, dirty grease smear, readable text`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/aligarh/aligarh-cylinder-assembly.webp`

### C2.3 — QC pick-test bench
**Main Prompt**
```
Editorial photograph of a quality-control bench testing finished locks, a technician's hands working
a key in a polished lockset under bright focused inspection light, measuring tools and reference
samples, warm-neutral palette with steel and gold, deep navy surround, shallow depth of field,
full-frame 50mm, photoreal, meticulous export QC atmosphere
```
**Negative Prompt** — *base +* `messy bench, cold lab, readable forms and text, clutter`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/aligarh/aligarh-qc-bench.webp`

## C3 — Firozabad (city of glass)

### C3.0 — Aerial establishing shot
**Main Prompt**
```
Cinematic aerial photograph at dusk over the Indian glass-furnace city of Firozabad, glowing
furnace chimneys with warm orange light against deep navy twilight, low-rise glassworks rooftops,
thin atmospheric haze catching the glow, established industrial craft-city scale, drone perspective,
photoreal, editorial documentary grandeur, no readable signage
```
**Negative Prompt** — *base +* `modern skyline, daytime flat light, readable signs, smoke pollution focus`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/firozabad/firozabad-aerial.webp`

### C3.1 — Furnace · molten glass
**Main Prompt**
```
Dramatic editorial photograph of a glassblower gathering glowing molten glass from a furnace mouth,
intense orange-white heat glow, warm sparks, artisan silhouette in deep navy shadow, blow-pipe and
warm volumetric haze, material realism, shallow depth of field, full-frame 35mm, photoreal, cinematic
glass-craft intensity
```
**Negative Prompt** — *base +* `cold lighting, factory machine glass, readable text, safety-poster look`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/firozabad/firozabad-furnace.webp`

### C3.2 — Chandelier assembly bench
**Main Prompt**
```
Editorial photograph of artisans assembling a multi-tier crystal chandelier on a workbench, hundreds
of cut-glass drops catching warm light into gold sparkle, deep navy backdrop, refined craftsmanship,
controlled flare and caustics, shallow depth of field, full-frame 50mm, photoreal, luxury lighting
atelier mood, ultra detailed crystal
```
**Negative Prompt** — *base +* `plastic crystals, cheap fixture, cluttered, readable text, rainbow oversaturation`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/firozabad/firozabad-chandelier-bench.webp`

### C3.3 — Crystal cutter at work
**Main Prompt**
```
Intimate macro editorial photograph of a craftsman hand-cutting facets into crystal glass on a
spinning cutting wheel, fine water spray and glass dust catching warm light, razor-sharp faceted
detail, deep navy bokeh, full-frame 100mm macro, photoreal, heritage glass craftsmanship, dignified
and premium
```
**Negative Prompt** — *base +* `blurry subject, plastic, dirty, readable text, harsh flash`
**Aspect Ratio** — 4:3 · **Placement** — `assets/images/hubs/firozabad/firozabad-crystal-cutter.webp`

---

# D. AFRICA EXPORT LOGISTICS

### D1 — Shipping containers (port stacks)
**Main Prompt**
```
Cinematic photograph of neatly stacked shipping containers at a major export terminal at blue-hour,
deep navy and warm amber palette, gantry cranes and a distant cargo ship, dock lights glowing,
atmospheric haze, sense of global trade scale, wide full-frame lens, photoreal, premium logistics
grandeur, controlled contrast with gold accents, no readable container markings
```
**Negative Prompt** — *base +* `readable container codes, company logos, daytime harsh sun, crowds, text`
**Aspect Ratio** — 16:9 · **Placement** — `assets/images/export/shipping-containers-mundra.webp` (homepage gallery wide tile + reused on Export pages)

### D2 — Container loading bay
**Main Prompt**
```
Editorial photograph of export cartons being block-and-braced loaded into an open 40-foot shipping
container at an inland container depot, neat stacked kraft cartons, a forklift in soft focus, warm
work light against deep navy dusk, dust haze, sense of careful premium export handling, full-frame
35mm, photoreal, industrial trade atmosphere, no readable text on cartons
```
**Negative Prompt** — *base +* `chaotic warehouse, damaged boxes, readable labels and codes, messy`
**Aspect Ratio** — 16:9 · **Placement** — `assets/images/export/container-loading-bay.webp` (Export Services svc 01)

### D3 — Port arrival / inland transit (last mile)
**Main Prompt**
```
Cinematic photograph of a container truck on an open highway at golden hour heading inland from an
African port, warm dust-gold light, long shadows, distant port cranes behind, sense of last-mile
delivery across the continent, wide full-frame lens, photoreal, premium logistics journey mood,
no readable text
```
**Negative Prompt** — *base +* `traffic jam, broken road focus, readable plates and signage, crowds`
**Aspect Ratio** — 16:9 · **Placement** — `assets/images/export/port-arrival-inland.webp` (Export Services svc 06)

### D4 — Consolidation warehouse (mixed FCL)
**Main Prompt**
```
Editorial photograph of an organised export consolidation warehouse, palletised mixed cartons in
neat rows under warm high-bay light, a wide aisle leading to an open loading dock with golden
daylight, deep navy steel structure, sense of scale and order, full-frame 24mm, photoreal, premium
logistics operations, no readable signage
```
**Negative Prompt** — *base +* `messy clutter, empty derelict warehouse, readable labels, dim and dirty`
**Aspect Ratio** — 16:9 · **Placement** — `assets/images/export/consolidation-warehouse.webp`

---

# E. WAREHOUSE OPERATIONS

### E1 — Warehouse operations (general)
**Main Prompt**
```
Wide editorial photograph of a premium export warehouse in operation, staff in soft focus moving
palletised goods, warm high-bay lighting with golden daylight from dock doors, tall neat racking,
deep navy steel and warm paper-toned cartons, layered depth, full-frame 24mm, photoreal, organised
trade-house scale, dignified and clean, no readable text
```
**Negative Prompt** — *base +* `cluttered, dim, dirty floor, readable labels, forklifts with logos`
**Aspect Ratio** — 16:9 · **Placement** — `assets/images/export/warehouse-operations.webp`

### E2 — Documentation desk (compliance)
**Main Prompt**
```
Editorial photograph of a calm export documentation desk, neat stacks of unmarked paperwork, a
laptop and a desk lamp casting warm light, brass desk accessories, deep navy office wall, blurred
shelving behind, shallow depth of field, full-frame 50mm, photoreal, premium back-office trade
atmosphere, no readable text on documents or screen
```
**Negative Prompt** — *base +* `readable documents, readable screen, messy desk, clutter, harsh light`
**Aspect Ratio** — 16:9 · **Placement** — `assets/images/export/documentation-desk.webp` (Export Services svc 04)

---

# F. PRODUCT CLOSEUPS (per-category SKU stills)

Each product page shows 9 SKU tiles plus a 6-image gallery strip. Rather than 60+ near-duplicate
prompts, use the **category closeup template** below and swap the `{SUBJECT}` token per SKU. Filenames
for every SKU are listed in [`image-map.md`](image-map.md).

### F0 — Universal product-closeup template
**Main Prompt**
```
Premium editorial product photograph of {SUBJECT}, single hero object centered on a dark brushed
surface, deep navy backdrop, one warm directional key light plus soft fill revealing fine material
texture, shallow depth of field, full-frame 85–100mm look, photoreal, luxury export-catalogue
quality, warm gold accents against navy, ultra detailed, clean negative space for cropping
```
**Negative Prompt** — *base +* `multiple cluttered objects, busy props, white seamless studio, readable label, plastic`
**Aspect Ratio** — 4:3 (SKU tile) · **Leonardo Settings** — Photoreal v2 · Cinematic · Contrast High · CFG 7 · Upscale 2×

### F1 — Brassware `{SUBJECT}` tokens (`products/brassware/`)
decorative brass pots (surahi & lota) · brass idols & figurines · brass diya & oil lamps ·
engraved decorative brass vases · brass candle holders & t-light stands · hammered brass trays,
bowls & platters · brass serving tableware · brass wall sconces & lighting · cast decorative brass animals

### F2 — Metal Art Ware `{SUBJECT}` tokens (`products/metal-art-ware/`)
decorative metal wall art · freestanding metal sculptures · metal planters · decorative metal
bookends · metal trinket boxes & jewellery cases · large metal installations · decorative metal
screens & dividers · metal mirrors & frames · garden art & exterior metal pieces

### F3 — Furniture Hardware `{SUBJECT}` tokens (`products/furniture-hardware/`)
soft-close cabinet hinges · ball-bearing drawer slides · solid bar pull handles · cabinet knobs &
pulls · furniture brackets · gas struts & lift mechanisms · concealed bed fittings · wardrobe
accessories · kitchen organizer hardware
*(Use Photoreal v2 + macro 100mm; emphasise brushed-metal grain and machined edges.)*

### F4 — Locks & Hardware `{SUBJECT}` tokens (`products/locks-hardware/`)
heavy-duty padlocks · mortise lock sets · brass cylinder locks · door closers · smart / digital
locks · tower bolts & door bolts · aldrops & latches · hasps & staples · lever handles & locksets
*(Cool steel ambiance + warm rim light; show machined precision.)*

### F5 — Bathroom Hardware `{SUBJECT}` tokens (`products/bathroom-hardware/`)
single-lever basin faucets · concealed shower systems · towel bars & rings · robe hooks & valets ·
soap dishes & holders · health faucets & jet sprays · bath waste & traps · toilet roll holders ·
complete bath accessory sets
*(Brushed gold / matte black finishes; a touch of water-bead realism.)*

### F6 — Glassware `{SUBJECT}` tokens (`products/glassware/`)
crystal chandeliers · decorative glass vases · decanters & barware · glass bowls, platters &
centrepieces · glass pendant lights & lamps · decorative glass panels · stained / coloured glass ·
glass wall art · custom hospitality lighting
*(Backlight for refraction; control flare; jewel-like clarity.)*

### F7 — Home Decor `{SUBJECT}` tokens (`products/home-decor/`)
wall & standing mirrors · decorative photo frames · candle holders & lanterns · decorative bowls &
trays · room fragrances & diffusers · seasonal decor collections · decorative cushions & textiles ·
wall hangings & dreamcatchers · curated gift hampers
*(Lean lifestyle/styled rather than isolated object where it suits the piece.)*

### F9 — Product detail items (Phase 2 · `products/items/<group>/`)
The 72 product-detail pages each need **1 hero (4:3) + 3 macro details (1:1)**. Use the **F0 template**
with `{SUBJECT}` = the exact product name (e.g. *"a solid brass knurled drawer handle"*). Shoot:
- `<slug>-hero.webp` — the full product, hero lighting, 4:3
- `<slug>-1/-2/-3.webp` — tight macro crops: surface finish, edge/joint, and mounting/back detail
Keep the same navy + warm-gold studio look so all 72 read as one catalogue. Filenames & folders are
listed in [`image-map.md`](image-map.md) §3.10.

### F8 — Per-category gallery strip (6 images each)
Every product page has a gallery: **hero · detail · detail · lifestyle · packaging · container**.
Reuse these prompt intents (swap the category material):
- **hero** — the category template at 16:10, the strongest single piece
- **detail** ×2 — extreme macro of texture/finish/joint
- **lifestyle** — the product styled in a real African retail / hotel / home setting, warm and aspirational
- **packaging** — see section G
- **container** — reuse `export/container-loading-bay.webp` intent

---

# G. EXPORT PACKAGING

### G1 — Export packaging (kraft / protective)
**Main Prompt**
```
Editorial photograph of premium export packaging in progress, an unbranded kraft carton open to
reveal a brass piece nested in tissue and protective foam, neat anti-rust wrapping, warm soft light
on a clean workbench, deep navy background, sense of meticulous care, shallow depth of field,
full-frame 50mm, photoreal, luxury export-grade packing, no readable text on cartons
```
**Negative Prompt** — *base +* `readable shipping labels, barcodes, brand print, messy, damaged box`
**Aspect Ratio** — 4:3 · **Placement** — product gallery `packaging` slots → `assets/images/products/{category}/gallery-packaging.webp`

### G2 — Branded packaging mockups (OEM / private label)
**Main Prompt**
```
Editorial photograph of elegant unbranded premium packaging concepts — a rigid gift box, a kraft
sleeve and tissue wrap in navy and warm gold tones arranged on a dark surface, soft studio light,
blank label areas with no text, sense of bespoke private-label development, shallow depth of field,
full-frame 50mm, photoreal, luxury OEM presentation, deliberately blank branding zones
```
**Negative Prompt** — *base +* `any readable logo or text, busy graphics, cheap printing, clutter`
**Aspect Ratio** — 4:3 · **Placement** — Export Services svc 02 → `assets/images/export/branded-packaging-oem.webp`

### G3 — Packaging line (QC stage)
**Main Prompt**
```
Editorial photograph of an export packaging line, workers in soft focus wrapping and boxing finished
goods in neat sequence, warm task lighting, rolls of protective material, deep navy industrial
backdrop with paper-toned cartons, organised and clean, full-frame 35mm, photoreal, premium QC and
packing atmosphere, no readable text
```
**Negative Prompt** — *base +* `chaotic line, dirty, readable labels, harsh fluorescent`
**Aspect Ratio** — 16:9 · **Placement** — Export Services svc 03 → `assets/images/export/packaging-line.webp`

---

# H. TEAM / FACTORY (people & offices)

> Use neutral, dignified figures. **No real or recognisable faces, no logos on clothing.** Three-quarter
> or environmental framing works best and avoids the uncanny-valley headshot look.

### H1 — Leadership portrait template (4 portraits)
**Main Prompt**
```
Premium editorial environmental portrait of a {ROLE} of an Indian export company, confident and
approachable, dressed in refined business attire, standing in a warm-lit office or factory setting
with deep navy and gold tones, soft directional key light, shallow depth of field, full-frame 85mm,
photoreal, dignified corporate editorial, natural skin texture, no logo on clothing
```
`{ROLE}` values → managing director (mature Indian businessman) · operations director (Indian
businesswoman) · Africa desk head (West African businesswoman, Lagos office backdrop) · head of
quality control (Indian man, factory backdrop)
**Negative Prompt** — *base +* `waxy skin, plastic, exaggerated features, name tag with text, logo on shirt, harsh flash`
**Aspect Ratio** — 4:5 (portrait) · **Leonardo Settings** — Phoenix 1.0 · Cinematic · Contrast Medium · CFG 6 · Upscale 2×
**Placement** — About leadership grid → `assets/images/team/portrait-managing-director.webp`, `...-operations-director.webp`, `...-africa-head.webp`, `...-head-qc.webp`

### H2 — Office / facility exteriors (3, for Contact)
**Main Prompt**
```
Editorial architectural photograph of a {PLACE}, warm golden-hour light on a clean modern-but-warm
building facade, deep navy and gold tones, refined and established, slight low angle for stature,
full-frame 24mm, photoreal, premium corporate location, no readable signage
```
`{PLACE}` values → premium brassware-house headquarters building in an Indian industrial district
(Moradabad) · a port-side export warehouse facility (Mundra) · a sleek Africa-desk office building
on a Lagos boulevard
**Negative Prompt** — *base +* `readable signs, billboards, run-down, cluttered street, text`
**Aspect Ratio** — 4:3 · **Placement** — Contact offices grid → `assets/images/team/office-moradabad-facility.webp`, `office-mundra-warehouse.webp`, `office-lagos.webp`

---

# I. BLOG / JOURNAL BANNERS

> One feature banner + one image per editorial theme. Themes repeat across articles, so a strong image
> per theme covers the whole journal. Keep these atmospheric/conceptual, never with readable headlines.

### I1 — Feature banner (Africa import shift)
**Main Prompt**
```
Cinematic conceptual editorial banner photograph evoking India-to-Africa hardware trade — a split
sense of an Indian brass workshop warmth on one side and an African port horizon on the other,
joined by warm golden light, deep navy palette with gold accents, atmospheric and aspirational,
wide full-frame lens, photoreal, premium trade-journalism mood, no text, no maps with labels
```
**Negative Prompt** — *base +* `readable map labels, flags, text headlines, collage seams, clutter`
**Aspect Ratio** — 16:9 (wide feature) · **Placement** — Blog featured hero → `assets/images/blog/feature-africa-import-shift.webp`

### I2 — Theme banners (one each)
Use the template, swap `{THEME}`:
**Main Prompt**
```
Editorial conceptual banner photograph for a trade journal article about {THEME}, atmospheric and
premium, deep navy and warm gold palette, cinematic directional light, shallow depth of field,
full-frame look, photoreal, sophisticated business-editorial mood, no readable text
```
`{THEME}` values & files:
- **market insight** — abstract close-up of brass and steel goods with a sense of market momentum → `blog/market-insight.webp`
- **hub guide** — a moody Moradabad/Firozabad craft-district detail → `blog/hub-guide.webp`
- **compliance** — neat unmarked export documents and a brass stamp on a navy desk → `blog/compliance.webp`
- **directory** — an organised array of hardware samples on a dark grid surface → `blog/directory.webp`
- **logistics** — a single shipping container detail at golden hour → `blog/logistics.webp`
- **oem** — elegant blank private-label packaging on navy → `blog/oem.webp`
**Negative Prompt** — *base +* `readable text, charts with numbers, flags, clutter`
**Aspect Ratio** — 16:9 (homepage 4:3 crop also exported) · **Leonardo Settings** — Phoenix 1.0 · Cinematic · Contrast Medium-High · CFG 7 · Upscale 2×

---

## J. Consistency checklist (run before exporting any image)

- [ ] Reads as a real photograph, not "AI art" (natural light, real material grain, believable optics)
- [ ] Navy + warm gold palette present; no garish saturation
- [ ] **No text, logos, brand names, flags, or readable labels** anywhere in frame
- [ ] No distorted hands/faces; no recognisable real people
- [ ] Composition leaves clean space where a gradient scrim / caption / tag chip sits (see `image-map.md`)
- [ ] Exported at the listed aspect ratio, upscaled 2×, then optimised per `images/README.md`
- [ ] Saved to the exact path/filename in `image-map.md`
