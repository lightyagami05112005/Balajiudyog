# Balaji Udhyog — Export Buyer Portal (Concept)

> A private, login-gated area where an African importer manages their relationship with Balaji Udhyog:
> quotations, orders, shipments, documents and payments — in one place. This document is the product
> brief and information architecture for that portal. Aesthetic: the same navy/gold/paper export-house
> design language, calm and document-led — **a ledger, not a SaaS dashboard.**

---

## 1. Who it serves & why

- **User:** a verified importer / distributor / chain-retail buyer with an account manager.
- **Job:** track what they've asked for, what's in production, what's shipped, what they owe, and pull
  the documents their customs and bank need — without emailing the desk for every update.
- **Business value:** fewer status emails, faster reorders, stickier accounts, visible trust.

Access is **invite-only** (the account manager issues credentials after the first order). This keeps it
exclusive and premium — not a public sign-up funnel.

---

## 2. Modules

### 2.1 Quotation tracking
- List of quotations: `Q-2026-0142 · Brassware + Bathroom · 1×40' · FOB Mundra · USD 18,400 · valid to 12 Jun`.
- States: **Draft → Sent → Under review → Revised → Accepted → Converted to PO → Expired.**
- One-click **"Accept & convert to proforma"** and **"Request revision"** (notes the desk).
- Each quote shows the line items, finishes, MOQ, carton/container math and validity.

### 2.2 Order history
- All purchase orders with status, value, hub origin, and the named manager.
- Filters by category, year, destination port. Reorder button clones a past PO into a new quote.
- Per-order document drawer: proforma, commercial invoice, packing list, B/L, CO, inspection report.

### 2.3 Shipment updates / container tracking
- Timeline per shipment mapped to the six-stage process: **Inquiry → Selection → Production →
  Packaging/QC → Shipment → Delivery.**
- Container card: container no. (masked), seal no., vessel, ETD Mundra, ETA destination port, B/L no.,
  current milestone, last-mile status.
- Document manifest + the **container photo manifest** taken at door-close on dispatch day.
- Optional carrier-tracking deep link (Maersk / MSC / CMA CGM) by container/B/L number.

### 2.4 Catalogue access
- The latest master catalogue + per-category line sheets + the buyer's **custom shortlist**.
- Private-label buyers see their own branded line sheets (NDA-gated).
- "Add to inquiry" builds a draft quote the desk receives.

### 2.5 Payment workflow
- Per-order ledger: advance %, balance, terms (T/T 30% advance / 70% against B/L copy, or L/C at sight).
- Bank details on file (masked), proforma-linked, with a "mark advance paid / upload SWIFT copy" action.
- Status: **Advance due → Advance received → Balance due → Paid → Closed.** No card payments — this is
  T/T and L/C trade finance, shown like a statement of account.
- Downloadable statement of account per period.

### 2.6 Messages / account manager
- A single thread with the named manager (mirrors WhatsApp). Document requests, revisions, queries.
- "Request a call" with the Africa desk; timezone-aware.

---

## 3. Information architecture

```
/portal
├─ Overview      (open quotes · in-production · in-transit · balance due)
├─ Quotations    (track · accept · revise)
├─ Orders        (history · documents · reorder)
├─ Shipments     (timeline · container tracking · photo manifest)
├─ Catalogue     (master · collections · my shortlist · private label)
├─ Payments      (per-order ledger · statement of account)
├─ Documents     (all PDFs, searchable)
└─ Messages      (account manager thread)
```

---

## 4. Data model (minimum)

```
Buyer        { id, company, country, port, manager_id, terms, created }
Quotation    { id, buyer_id, items[], incoterm, total_usd, valid_to, status }
PurchaseOrder{ id, quote_id, buyer_id, value, hub, status, created }
Shipment     { id, po_id, container_no, seal, vessel, etd, eta, bl_no, milestone, photos[] }
Document     { id, po_id, type, url, issued }     // proforma|invoice|packing|bl|co|inspection
Payment      { id, po_id, advance_pct, advance_status, balance_status, terms }
Message      { id, buyer_id, from, body, ts }
```

---

## 5. Build phasing (realistic)

1. **Phase 1 (static + manual):** read-only portal, the desk uploads PDFs and updates statuses. 80% of
   the trust value with 20% of the build. (Pairs directly with the lead-capture backend in `/backend`.)
2. **Phase 2:** buyer self-service — accept quotes, reorder, upload SWIFT copies.
3. **Phase 3:** live carrier tracking integration + statement automation.

Keep it document-led and quiet. The portal should feel like a private ledger the importer trusts —
not a noisy app.
