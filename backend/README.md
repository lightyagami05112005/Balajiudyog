# Balaji Udhyog — Lead-Capture & Inquiry Backend

A small Express service the export website posts inquiries to. It stores leads, emails the desk,
returns a WhatsApp follow-up link, and provides an admin dashboard to manage the pipeline. No database
— leads are kept in `data/leads.json` (fine for this scale; swap for Postgres later if needed).

## Run

```bash
cd project/backend
npm install
cp .env.example .env      # set ADMIN_TOKEN and WHATSAPP_NUMBER (and SMTP_* for email)
npm start                 # http://localhost:4000
```

- **Admin dashboard:** http://localhost:4000/admin — enter your `ADMIN_TOKEN`, see/triage inquiries,
  change status, reply on WhatsApp in one click.
- **Health:** http://localhost:4000/health

## How the website talks to it

The static site loads `assets/lead-capture.js`, which intercepts every `.form` submit and POSTs JSON to
`POST /api/inquiry`. If the backend is unreachable, the form **falls back gracefully** to a WhatsApp /
email prompt — no inquiry is ever lost in front of the buyer.

Point the site at a non-default backend by setting, before the script loads:
```html
<script>window.BU_LEAD_API = 'https://api.balajiudhyog.com';</script>
```

## API

| Method | Route | Auth | Purpose |
|---|---|---|---|
| POST | `/api/inquiry` | none | Capture a lead `{ source, page, fields:{...} }` → `{ ok, id, whatsapp }` |
| GET | `/api/leads` | `X-Admin-Token` | List leads (newest first) |
| PATCH | `/api/leads/:id` | `X-Admin-Token` | Update status (`new`→`quoted`→`sample-sent`→`po`→`repeat`/`cold`/`closed`) |
| GET | `/admin` | — | Dashboard UI (auth happens client-side via token) |

## Lead pipeline statuses

`new · quoted · sample-sent · po · repeat · cold · closed` — these mirror the WhatsApp Business labels in
`../assets/social-presence.md`, so the desk runs one consistent pipeline across channels.

## Email notifications (optional)

Set `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `NOTIFY_EMAIL` in `.env` and `npm install nodemailer`
(an optional dependency). Each new inquiry emails the export desk with the full field set and the
WhatsApp link. Leave SMTP blank to disable — capture still works.

## Production notes

- Put this behind HTTPS and a real domain; set a strong `ADMIN_TOKEN`.
- Swap the JSON store for a database and add rate-limiting / captcha on `/api/inquiry`.
- This pairs with the **buyer portal** (`../assets/buyer-portal-concept.md`) as its data source for
  Phase 1 (manual) operation.
```
