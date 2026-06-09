# Balaji Udhyog — SEO Plan

> Search strategy for a premium Indian hardware & decor exporter targeting African B2B importers.
> Intent is **commercial / transactional** (importers sourcing suppliers), not consumer retail.
> Priority: win "[product] exporter/supplier India → [African country]" queries with genuinely useful,
> trust-rich pages — never thin doorway/spam pages.

---

## 1. Search intent & audience

- **Who:** importers, wholesalers, distributors, chain-retail buyers, hotel/project procurement in
  Nigeria, Kenya, South Africa, Ghana, Tanzania.
- **What they type:** supplier-discovery and due-diligence queries, in English (and some French for
  West/Central Africa).
- **Where they convert:** WhatsApp + catalogue/quote request, not e-commerce checkout.
- **KPI:** qualified inquiries (form + WhatsApp), catalogue downloads, time-on-page for landing pages.

---

## 2. Target keyword clusters

**A. Exporter / supplier head terms** (high commercial intent)
- indian hardware exporter · hardware exporter india · brassware exporter india ·
  bathroom hardware supplier india · furniture hardware exporter · lock manufacturer india export ·
  glassware exporter firozabad · home decor exporter india

**B. Country-qualified** (the money cluster — one landing page each)
- hardware exporter to nigeria · indian hardware supplier nigeria · brassware supplier kenya ·
  bathroom fittings supplier ghana · furniture hardware exporter tanzania ·
  import hardware from india to [lagos/mombasa/durban/tema/dar es salaam]

**C. Hub / origin authority** (blog + hub pages)
- muradabad brass exporter · aligarh lock exporter · firozabad glassware manufacturer ·
  brass capital of india export

**D. Process / compliance long-tail** (blog, captures research-stage buyers)
- soncap certificate hardware import nigeria · kebs pvoc hardware kenya · sabs hardware south africa ·
  fcl vs lcl africa import · moq brassware india · fob vs cif india export

**E. Product + buyer modifiers** (product & category pages)
- wholesale brass cabinet handles · bulk tower bolts export · hotel bathroom accessories supplier ·
  private label hardware manufacturer india · oem brassware india

Map: A→home + Products + Export Services · B→country landing pages · C→hub pages + blog ·
D→blog · E→category + product detail pages.

---

## 3. Africa-focused strategy

- **Country landing pages** are the spearhead — one per priority market, each tied to the real
  port(s), compliance scheme, and buying behaviour for that country (not templated boilerplate).
- **Compliance content moat:** SONCAP / KEBS-PVoC / SABS / fumigation guides — high-intent,
  low-competition, and reinforces the "we clear your port" trust message.
- **French variants** (phase 2): Côte d'Ivoire, Senegal — `/fr/` or `hreflang` alternates for
  francophone West Africa.
- **Local proof:** name ports, ICDs, distributor cities; reference real lanes (Mundra→Apapa,
  Mundra→Mombasa) — specificity ranks and converts.

---

## 4. Country landing page ideas (templateable, not thin)

Build now: **Nigeria, Kenya, Ghana, Tanzania** (+ South Africa next). Each page = a real market brief,
not a keyword doorway. Required blocks:
1. Market-specific H1 + intro (port, demand, why-India-for-this-market)
2. Trust strip (years, factories, damage rate, on-time)
3. Product previews relevant to that market (product-card grid)
4. Compliance note for that country (SONCAP / KEBS / SABS / fumigation)
5. Logistics lane (origin port → destination port, transit time, terms)
6. Inquiry CTA (form + WhatsApp, pre-filled with country)
7. Internal links to categories, hubs, related blog posts

Expansion ideas: per-product-per-country (e.g. "brass handles supplier Lagos"), per-port pages
(Mombasa, Durban), per-segment (hotel hardware supplier Africa).

---

## 5. Metadata structure

**Title** (≤ 60 chars): `<Primary keyword> | Balaji Udhyog`
- Home: `Indian Hardware & Decor Exporter for Africa | Balaji Udhyog`
- Country LP: `Hardware Exporter to Nigeria — India Supplier | Balaji Udhyog`
- Category: `Brassware Exporter India — Wholesale & Export | Balaji Udhyog`
- Product: `<Product> <Finish> — Export Supplier | Balaji Udhyog`

**Meta description** (≤ 155 chars): benefit + proof + CTA.
- e.g. `Source premium brass hardware direct from India to Kenya. 600+ audited factories, KEBS-PVoC docs, Mombasa shipping. Request FOB pricing.`

**Per-page tags to add to every `<head>`:**
```html
<meta name="description" content="…">
<meta name="keywords" content="…">                <!-- light, optional -->
<link rel="canonical" href="https://www.balajiudhyog.com/…">
<meta property="og:title" content="…">
<meta property="og:description" content="…">
<meta property="og:image" content="…/assets/images/hero/…webp">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow">
```

**Structured data (JSON-LD):**
- Site/home: `Organization` + `WebSite` (+ `sameAs` socials).
- Country LP / category: `BreadcrumbList`.
- Product detail: `Product` (name, sku, brand, material) — omit fake price/rating; B2B uses
  `Offer` with `priceSpecification` "on request" or leave price out (no fabricated review schema).
- Blog: `Article` with author/publisher/datePublished.
- Contact: `LocalBusiness` for HQ.

---

## 6. Blog strategy

**Pillars** (each a hub with spokes):
1. **Sourcing from India** — hub guides (Muradabad/Aligarh/Firozabad), how to vet exporters, MOQ &
   pricing explainers.
2. **Africa import compliance** — SONCAP, KEBS-PVoC, SABS, fumigation/ISPM-15, Form M, duty structures.
3. **Logistics** — FCL vs LCL, transit times by lane, consolidation, packaging for ocean transit.
4. **Market trends** — India vs China shift, category demand by country, retail margin analysis.
5. **Product education** — finishes & materials, spec literacy, private-label playbooks.

**Cadence & format:** 2–4 posts/month, 1,200–2,000 words, one clear buyer takeaway, ends with a
catalogue/quote CTA. Title patterns: "[Compliance] explained for [country] importers",
"[Product] sourcing: what to ask before you order", "[Lane] shipping in 2026: costs & timelines".

**Conversion:** every post → contextual links to the relevant country LP, category, and an inquiry CTA.

---

## 7. Internal linking structure

```
Home ─┬─ Products ──┬─ Category (Brassware …) ──┬─ Product detail (item)
      │             │                            └─ Related products (same group + cross-category)
      │             └─ Items index (all products)
      ├─ Country LPs (Nigeria, Kenya, Ghana, Tanzania) ──► Categories + Products + relevant Blog
      ├─ Hubs (Muradabad, Aligarh, Firozabad) ◄──► Categories sourced there
      ├─ Export Services ──► Process / Packaging / Compliance ──► Country LPs
      ├─ Blog (pillars) ──► Country LPs + Categories + Hubs
      └─ Contact (inquiry) ◄── every page CTA
```

**Rules**
- Every product detail links **up** (category, hub of origin) and **across** (related products).
- Every country LP links to the **categories** most relevant to that market + 1–2 supporting blog posts.
- Category pages link **down** to product details and **across** to the hub that makes them.
- Use descriptive anchor text ("brass cabinet handles for export", not "click here").
- Footer carries: categories, markets, hubs, key services — site-wide link equity to money pages.
- Keep canonical tags clean; avoid duplicate country-doorway pages that don't add market-specific value.

---

## 8. Technical & on-page checklist

- [ ] Unique title + meta description per page (templates §5)
- [ ] One H1 per page; logical H2/H3 outline
- [ ] Descriptive `alt` on every image (done in Phase 1) — include product/market terms naturally
- [ ] Fast: WebP, lazy-load, width/height (done) — Core Web Vitals matter for ranking
- [ ] Mobile-first: country buyers are heavily mobile
- [ ] Canonical + OG + JSON-LD per §5
- [ ] XML sitemap + robots.txt (add at deploy)
- [ ] Descriptive, hyphenated URLs (e.g. `/pages/hardware-exporter-nigeria.html`)
- [ ] No keyword stuffing, no hidden text, no doorway pages — Google penalises; buyers distrust it
