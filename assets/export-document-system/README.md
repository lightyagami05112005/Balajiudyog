# Balaji Udhyog — Export Document System

Premium, print-ready trade-document templates in the company's navy/gold letterhead. Open any file in a
browser and use **Print → Save as PDF** (A4) to issue a clean PDF. Highlighted (amber-dashed) fields are
the values you fill per transaction.

## Templates
| File | Use |
|---|---|
| `quotation.html` | Indicative quote (FOB/CIF), validity, terms |
| `proforma-invoice.html` | Proforma for Form M / LC opening + advance (incl. bank details) |
| `commercial-invoice.html` | Final export/commercial invoice (B/L, container, HS, CO) |
| `packing-list.html` | Carton-level packing list (qty, net/gross, dims, CBM) |
| `purchase-order.html` | Buyer-issued PO template (against proforma + approved sample) |
| `moq-sheet.html` | Category MOQ / lead time / finishes / container reckoner |
| `specification-sheet.html` | Per-SKU technical + packing + export spec |
| `doc-style.css` | Shared print/screen styling (edit brand details here once) |

## How to use
1. Open the template in a browser.
2. Edit the highlighted fields (and line items) directly in the HTML, or wire to your system.
3. Print → Save as PDF (A4). Toolbar hidden in print.
4. Keep values consistent across documents (invoice value = Form M = PAAR). One source of truth.

## Notes
- Replace placeholder IEC / GSTIN / bank / SWIFT with the real registered details before issuing.
- Conformity references (SONCAP / KEBS / SABS) per destination — see `../seo-plan.md` and the content guides.
- For automated issuance, render these templates server-side from the same product/lead data used by `/backend`.
