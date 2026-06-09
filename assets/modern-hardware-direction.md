# Balaji Udhyog — Modern Hardware Visual Direction

> A correction to the visual identity. Balaji Udhyog is a **diversified modern hardware & bathroom
> systems exporter** — not a brass-foundry workshop. The imagery must read like a global architectural
> hardware supplier (think the *photography style* of Häfele, Hettich, Kohler, Jaquar, Grohe, TOTO,
> Roca, Hansgrohe, Geberit, Delta, Moen) — **studied for lighting, materials, framing and environment
> only; no logos, branding or copied product designs.**
>
> This document governs `scripts/realism-enhancer.js`. **Brass stays warm and heritage — but it is one
> category, not the whole company.** Every other category is modern, architectural and material-true.

---

## 0. The shift, in one line

> From *"glowing brass foundry at golden hour"* → to *"a faucet in a white-marble five-star bathroom,
> a matte-black lever on an architectural door, a brushed-steel handle on a handleless kitchen."*

**Remove across the site (except the Brassware heritage category):** dusty workshops, old furnaces,
rural craft vibes, weathered patina, ornate antique, **yellow-gold dominance**, derelict industrial.

---

## 1. Reference photography study (style only)

| Brand family | What to emulate (NOT copy) |
|---|---|
| **Kohler / TOTO / American Standard** | faucet & sanitaryware shot *in situ* in a real luxury bathroom; soft architectural daylight; marble + wood |
| **Grohe / Hansgrohe / Jaquar** | crisp chrome & brushed-metal product realism; clean reflections; water-bead detail; minimalist tile |
| **Geberit / Roca** | architectural bathroom systems in contemporary interiors; calm, neutral, engineered |
| **Häfele / Hettich** | furniture & cabinet hardware on real modern cabinetry; handleless kitchens, wardrobes, integrated light |
| **Delta / Moen** | approachable modern bathroom lifestyle; warm-neutral, not cold |

Common thread: **product shown in a believable premium interior**, photographed in soft natural or
architectural light, materials rendered honestly, frames calm and uncluttered.

---

## 2. Per-category aesthetic (each must look DIFFERENT)

| Category | Mood | Environment | Palette | Metals |
|---|---|---|---|---|
| **Bathroom hardware** | modern · hospitality luxury | 5-star hotel bathroom, white marble, backlit mirror, warm wood | white marble · charcoal · warm wood · soft neutral | **chrome · brushed nickel · matte black** |
| **Locks & hardware** | premium security · architectural | minimalist luxury apartment door, plaster wall, oak door | charcoal · warm oak · neutral | **matte black · brushed stainless** |
| **Furniture hardware** | modular · contemporary interiors | handleless kitchen, walk-in wardrobe, integrated lighting | walnut · stone grey · white | **brushed steel · matte black** (brass accents ok) |
| **Brassware** | warm · artisanal · **heritage** | refined modern studio, clean dark surface, soft warm light | warm brass · deep navy · warm neutral | **brushed brass** (restrained, never neon) |
| **Glassware** | premium lifestyle · contemporary | upscale modern living space, soft daylight | clear glass · soft neutral · charcoal | clear / coloured glass |
| **Metal art / Home decor** | contemporary decor | modern architectural interior, gallery-like | neutral · charcoal · warm wood · brushed metal | mixed, contemporary |

**Manufacturing / hubs:** show a **clean, modern precision facility** (CNC, stainless surfaces,
organised components, bright even light) — international factory, **not a dusty rural foundry**.
Brass workshop (Muradabad) may stay warm but **kept clean and professional**, not derelict.

---

## 3. Bathroom styling rules

- Shoot the fixture **installed or staged in a luxury bathroom**, not isolated on a dark slab.
- Large-format white/grey marble or microcement; warm timber vanity; backlit or framed mirror.
- Soft, even architectural daylight from a large window; gentle, realistic reflections.
- Finishes crisp and true: chrome (cool, bright but not blown), brushed nickel (soft satin), matte
  black (deep, even, non-reflective). A touch of clean water-bead realism on spouts.
- Minimalist: one hero fixture, calm negative space, no clutter, no gold dominance.

## 4. Steel / brushed-metal rendering rules

- Brushed stainless & nickel: visible **fine directional grain**, soft satin sheen, **no mirror glare**.
- Honest micro-detail (faint handling marks), but **clean and commercial-grade** — not weathered.
- Cool-neutral tone; let one warm bounce keep it from going clinical.
- Edges machined and precise; welds/joins clean. International manufacturing quality.

## 5. Chrome reflection rules

- Chrome reflects the **room**, not a studio gradient — soft window, marble, neutral surroundings.
- Reflections **broken and realistic**, never a perfect mirror or fake HDR sparkle.
- Control highlights: bright but not clipped/blown. No rainbow, no neon, no glow.

## 6. Matte black rendering rules

- Deep, even, low-reflectance; texture from form and soft shadow, not shine.
- Keep detail in the blacks (not crushed); a soft rim of light defines the edge.
- Pairs with marble, oak and brushed steel — the contemporary "architectural" look.

## 7. Interior styling direction

- Real, current premium interiors: handleless kitchens, walk-in wardrobes, hotel bathrooms,
  minimalist apartments, architectural showrooms, hospitality lobbies.
- Warm-neutral palette: white/grey stone, warm wood, charcoal, brushed metal, soft daylight.
- Calm, uncluttered, designed — Architectural-Digest-meets-trade-catalogue.

## 8. Luxury hospitality & commercial-architectural mood

- The buyer should picture these products **in their hotel, apartment block or retail fit-out.**
- Convey scale and consistency: clean repetition, engineered precision, international standard.
- Commercial-grade confidence — calm, premium, trustworthy; never rustic or novelty.

---

## 9. Global negatives for the modern set (non-brass)

`antique, rustic, dusty workshop, rural, village, derelict, old furnace, foundry fire, weathered
patina, ornate vintage, yellow-gold dominance, oversaturated gold, brass everywhere, handcraft-only,
grimy, kitsch, cluttered` — **plus** the standing anti-CGI/anti-text wall.

## 10. Regeneration priority (when a funded key is available)

1. Bathroom hardware (category + items: faucets, showers, towel holders, accessories)
2. Locks & hardware (category + door locks, tower bolts) — matte black / brushed steel, architectural
3. Furniture hardware (category + cabinet handles, knobs, hinges) — modern cabinetry
4. Modern environment shots (hero, gallery) + manufacturing hubs → clean modern facility
5. Glassware & decor → contemporary lifestyle
6. Brassware → keep, only refine to clean heritage studio (lowest priority)

```bash
# once a funded key is in scripts/.env:
cd project/scripts
node generate-leonardo-images.js --only=bathroom-hardware --force --variations=3
node generate-leonardo-images.js --only=locks-hardware --force --variations=3
node generate-leonardo-images.js --only=furniture-hardware --force --variations=3
node generate-leonardo-images.js --only=products/items/towel-holders --force --variations=3
node generate-leonardo-images.js --only=products/items/door-locks --force --variations=3
node generate-leonardo-images.js --only=hero/ --force --variations=3
node realism-curator.js          # re-audit consistency afterwards
```

**Goal:** the site reads as a *diversified modern export company* — luxury bathroom systems,
architectural fittings, hospitality hardware and contemporary interiors — with brass as one warm
heritage line, not the whole identity.
