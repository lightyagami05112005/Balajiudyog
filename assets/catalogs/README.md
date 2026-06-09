# Balaji Udhyog — Catalogue & Brochure System

Premium, print-ready HTML catalogues. Open in a browser and use **Print → Save as PDF**
(A4 **landscape** for the catalogue/brochure spreads; the line sheet is portrait) to produce a
luxury, WhatsApp-shareable PDF.

| File | What it is |
|---|---|
| `master-catalogue.html` | Full export catalogue — cover, 6 category spreads, export terms, back cover |
| `brassware-collection.html` | Single-category line sheet (template for per-collection PDFs) |
| `africa-export-brochure.html` | Narrative export brochure — origin, compliance, packaging, terms |
| `catalog-style.css` | Shared catalogue styling |

Images are pulled from `../images/` (the realism-graded asset set). They render once those WebP files
exist; until then the cover/spread areas show the warm paper background.

To make more collection PDFs, copy `brassware-collection.html` and swap the SKU items + images.
For WhatsApp Business, upload the exported PDFs as the in-app catalogue (see `../social-presence.md`).
