# Balaji Udhyog — Visual Direction & Color-Grading System

> The single visual standard every image on the site must meet. The goal is one consistent
> **documentary / industrial / commercial** look — as if a real ₹100+ crore Indian export house
> hired one photographer with one camera kit and one grade for the whole shoot.
>
> This document drives `scripts/realism-enhancer.js` (what we ask for) and
> `scripts/realism-curator.js` (what we reject). If you change the look, change it here first.
>
> **Category direction (important):** the palette below describes the *base* grade. Each product
> category now has its own modern, distinct look — see **[`modern-hardware-direction.md`](modern-hardware-direction.md)**.
> Brass/gold is the **Brassware heritage line only**; bathroom, locks and furniture hardware are
> modern (chrome / brushed steel / matte black, architectural interiors), not brass-toned.

---

## 0. The one-line brief

> *"An honest, unretouched photograph from a working Indian factory, warehouse or port —
> shot on a full-frame camera in available light, lightly graded, never glossy."*

**Reference look:** Architectural Digest industrial features · luxury hardware trade catalogues ·
documentary manufacturing photography · premium export brochures · real logistics/port photography.
**Never:** cinematic AI art · glossy 3D renders · hyperfake luxury · synthetic HDR · fantasy lighting.

---

## 1. Target colour palette

The brand palette stays (navy + warm gold + paper) but appears as **real-world materials and
ambient light**, not as a colour filter.

| Role | Where it comes from | Hex anchor | Rule |
|---|---|---|---|
| Deep navy | shadows, painted steel, dusk sky | `#0a1d3a` / `#06122a` | from real shadow & material, not a blue filter |
| Warm gold / brass | the metal itself, tungsten work-lights | `#c8a55b` | **muted, true brass** — never neon, never uniform gold cast |
| Warm paper / neutral | kraft cartons, concrete, daylight | `#f5f2ec` / `#ebe6db` | the neutral base; keeps whites honest |
| Steel / grey | machinery, racking, asphalt | `#6b7280` | grounds the frame, stops "all-gold" look |

- **White balance:** neutral-to-slightly-warm (≈ 5200–5600K). Whites read white, not amber.
- **Saturation:** restrained. Target overall HSV saturation **0.18–0.40**. Gold must read as *metal*,
  not as a saturated colour. The curator flags `satMean > 0.42` and `goldFrac > 0.22`.
- **No global colour wash.** Navy and gold come from objects and light, not a LUT over everything.

---

## 2. Exposure rules

- **Natural, neutral exposure.** Mid-tones open and readable; nothing "crushed for mood".
- **Protect highlights:** no blown specular on metal/glass. Brass highlights roll off, they don't clip.
  Curator flags `hiFrac > 0.05` (blown highlights / fake gloss).
- **Protect shadows:** shadows retain a little detail; no inky black holes. Curator flags `loFrac > 0.10`.
- **Dynamic range:** medium. **High-contrast / synthetic-HDR is OFF** in generation.

---

## 3. Contrast & grade

- **Contrast:** moderate, film-like. A gentle S-curve at most — not punchy "AI pop".
- **Grade:** a light, consistent warm-neutral grade across the whole site. Think a single subtle
  print profile, not per-image stylisation.
- **No teal-orange, no heavy vignette, no glow/bloom, no lens-flare.**

---

## 4. Grain & sharpness rules

- **Grain:** fine, organic sensor/film grain present in every image. Zero grain = "rendered".
- **Sharpness:** natural optical sharpness with **mild lens softness**. **No over-sharpening, no
  halos, no crunchy micro-contrast.** Curator flags `lapVar > 240` (over-sharpened) and
  `lapVar < 14` (too smooth / plasticky).
- Acceptable detail band (192px Laplacian variance proxy): **~14–240**.

---

## 5. Realism rules (the non-negotiables)

1. Must look **photographed**, not generated: real optics, real falloff, believable perspective.
2. **Natural, slightly imperfect framing** — documentary, candid, slight asymmetry. Avoid dead-centre
   hyper-symmetry.
3. **No text, logos, brand names, readable labels or signage** anywhere.
4. **No fantasy/sci-fi lighting, no god-rays, no surreal glow.**
5. Every frame carries at least one honest imperfection (see §6).

---

## 6. Texture & material realism

- **Surfaces show history:** fingerprints, fine scratches, dust specks, uneven edges, faded paint,
  light grease, wear at contact points.
- **Cardboard/kraft:** matte, slightly fibrous, imperfect/creased edges — never crisp CGI boxes.
- **Concrete/asphalt:** scuffed, stained, real aggregate; warehouse floors slightly dusty.
- **Fabric/clothing:** real weave and creases.

## 7. Metal rendering rules (critical — brass is the brand)

- Brass & copper: **brushed / satin**, warm but **muted**; visible **machining marks, lathe lines,
  casting texture**, faint patina. **Not** mirror-chrome, **not** liquid-gold, **not** uniform glow.
- Reflections are **soft and broken up** by surface texture — never perfect mirror reflections or
  fake studio gradients. Curator flags "fake-metal" via high gold-cast + blown highlights together.
- Steel/stainless: cool neutral grey with realistic brushed grain and fingerprints.
- Glass: real refraction with minor imperfections; no rainbow oversaturation, no synthetic sparkle.

## 8. Warehouse / factory / logistics atmosphere

- **Working spaces, not showrooms:** racking, pallets, stacked cartons, cabling, tools, minor clutter.
- **Light:** mixed daylight from windows + overhead industrial fixtures; soft, uneven, real.
- **Air:** faint dust haze; honest grime and wear on floors and walls.
- **Containers/ports:** weathered containers (scuffs, dents, rust streaks), faded yard markings,
  flat overcast sky; loading crew/workers at natural distance.

## 9. Human presence rules

- Real Indian workers — warehouse staff, packaging workers, loading crew, inspectors, artisans.
- **Candid, side or three-quarter angle, mid-task, usually not facing camera.**
- **Hands and faces must be anatomically correct** — the most common AI failure. Forced negatives:
  extra/fused fingers, malformed hands, distorted face, uncanny smile, asymmetric eyes, mannequin.
- Ordinary work clothing with real creases; relaxed, unposed; no staged corporate smiles.

---

## 10. Consistency checklist (per image, before it ships)

- [ ] Reads as a real photograph from the same shoot as its neighbours
- [ ] White balance neutral-warm (~5400K); whites are white
- [ ] Saturation restrained; gold reads as metal, not colour
- [ ] No blown highlights / crushed shadows; medium dynamic range
- [ ] Fine grain present; not over-sharpened; mild lens softness
- [ ] At least one honest imperfection (scratch/dust/wear/crease)
- [ ] Brass is brushed & muted, not glossy/chrome
- [ ] If people: candid, side-angle, correct hands/face
- [ ] No text/logos/AI artifacts/surreal lighting
- [ ] Realism score ≥ 75 in `realism-curator.js` (and consistent with the site median)
