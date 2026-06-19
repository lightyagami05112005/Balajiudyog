// server.js — Balaji Udyog lead-capture & inquiry-management backend
// ---------------------------------------------------------------------------
// A small, dependency-light Express service that the static export website
// posts inquiries to. It:
//   • stores leads to data/leads.json (no DB needed for this scale)
//   • notifies the export desk by email (nodemailer, optional/configurable)
//   • returns a ready WhatsApp click-to-chat link for instant follow-up
//   • serves an admin dashboard at /admin to triage the pipeline
//
// Config via environment (see .env.example): PORT, ADMIN_TOKEN, WHATSAPP_NUMBER,
// NOTIFY_EMAIL, and SMTP_* for email. Everything has safe dev defaults.
// ---------------------------------------------------------------------------

import express from 'express';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
loadEnv(path.join(__dirname, '.env'));

const PORT = process.env.PORT || 4000;
const DATA = path.join(__dirname, 'data', 'leads.json');
const ADMIN_TOKEN = process.env.ADMIN_TOKEN || 'change-me';
const WHATSAPP = (process.env.WHATSAPP_NUMBER || '919800000000').replace(/[^\d]/g, '');
const STATUSES = ['new', 'quoted', 'sample-sent', 'po', 'repeat', 'cold', 'closed'];

const app = express();
app.use(express.json({ limit: '64kb' }));

// CORS — the static site may be served from a different origin/port.
app.use((req, res, next) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, X-Admin-Token');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

/* ---------------- storage helpers (JSON file, atomic-ish) ---------------- */
function readLeads() {
  try { return JSON.parse(fs.readFileSync(DATA, 'utf8')); } catch { return []; }
}
function writeLeads(list) {
  fs.mkdirSync(path.dirname(DATA), { recursive: true });
  fs.writeFileSync(DATA, JSON.stringify(list, null, 2));
}
function id() { return 'L-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }

/* ---------------- email notification (optional) ---------------- */
async function notify(lead) {
  if (!process.env.SMTP_HOST || !process.env.NOTIFY_EMAIL) return; // not configured → skip silently
  let nodemailer;
  try { nodemailer = (await import('nodemailer')).default; }
  catch { console.warn('nodemailer not installed — skipping email notification'); return; }
  const t = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT || 587),
    secure: String(process.env.SMTP_SECURE) === 'true',
    auth: process.env.SMTP_USER ? { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS } : undefined,
  });
  const rows = Object.entries(lead.fields || {}).map(([k, v]) => `${k}: ${v}`).join('\n');
  await t.sendMail({
    from: process.env.SMTP_FROM || process.env.SMTP_USER,
    to: process.env.NOTIFY_EMAIL,
    subject: `New export inquiry — ${lead.company || lead.name || 'unknown'} (${lead.country || '—'})`,
    text: `New inquiry via ${lead.page || 'website'} [${lead.source || 'web'}]\n\n${rows}\n\nWhatsApp: ${lead.whatsapp}\nReceived: ${lead.ts}`,
  }).catch(e => console.warn('email notify failed:', e.message));
}

/* ---------------- WhatsApp click-to-chat link ---------------- */
function waLink(lead) {
  const f = lead.fields || {};
  const msg = `Hello Balaji Udyog — inquiry from ${f.Company || f['Full Name'] || 'a buyer'} (${f.Country || lead.country || ''}). `
    + `Product: ${f['Product Interest'] || f['Product interest'] || f.Finish || '—'}. `
    + `Volume: ${f['Order Volume / Notes'] || f['Volume / Notes'] || f['Quantity / Volume'] || '—'}.`;
  return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`;
}

/* ---------------- routes ---------------- */
// Public: capture an inquiry from any site form
app.post('/api/inquiry', async (req, res) => {
  const b = req.body || {};
  const fields = b.fields && typeof b.fields === 'object' ? b.fields : b;
  // minimal validation: need some way to reply
  const email = fields.Email || fields.email || b.email;
  const phone = fields['WhatsApp / Phone'] || fields['WhatsApp'] || fields.phone;
  if (!email && !phone) return res.status(400).json({ ok: false, error: 'email or phone required' });

  const lead = {
    id: id(), ts: new Date().toISOString(), status: 'new',
    source: b.source || 'website', page: b.page || '',
    company: fields.Company || fields.company || '',
    name: fields['Full Name'] || fields.name || '',
    country: fields.Country || fields.country || '',
    email: email || '', phone: phone || '',
    fields,
  };
  lead.whatsapp = waLink(lead);

  const list = readLeads();
  list.push(lead);
  writeLeads(list);
  notify(lead); // fire-and-forget

  res.json({ ok: true, id: lead.id, whatsapp: lead.whatsapp });
});

// Admin auth (token via header or query)
function auth(req, res, next) {
  const tok = req.get('X-Admin-Token') || req.query.token;
  if (tok !== ADMIN_TOKEN) return res.status(401).json({ ok: false, error: 'unauthorized' });
  next();
}
app.get('/api/leads', auth, (req, res) => res.json({ ok: true, leads: readLeads().reverse() }));
app.patch('/api/leads/:id', auth, (req, res) => {
  const { status } = req.body || {};
  if (!STATUSES.includes(status)) return res.status(400).json({ ok: false, error: 'bad status' });
  const list = readLeads();
  const lead = list.find(l => l.id === req.params.id);
  if (!lead) return res.status(404).json({ ok: false, error: 'not found' });
  lead.status = status;
  writeLeads(list);
  res.json({ ok: true });
});

app.get('/admin', (req, res) => res.sendFile(path.join(__dirname, 'admin.html')));
app.get('/health', (req, res) => res.json({ ok: true, leads: readLeads().length }));
app.get('/', (req, res) => res.redirect('/admin'));

app.listen(PORT, () => {
  console.log(`\n  Balaji Udyog lead backend running on http://localhost:${PORT}`);
  console.log(`  Admin: http://localhost:${PORT}/admin   (token: ${ADMIN_TOKEN === 'change-me' ? 'change-me — SET ADMIN_TOKEN!' : 'set'})`);
  console.log(`  Inquiry endpoint: POST http://localhost:${PORT}/api/inquiry`);
  if (!process.env.SMTP_HOST) console.log('  Email notifications: OFF (set SMTP_* in .env to enable)');
});

/* ---------------- tiny .env loader (no dependency) ---------------- */
function loadEnv(file) {
  try {
    if (!fs.existsSync(file)) return;
    for (const raw of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
      const line = raw.trim(); if (!line || line.startsWith('#')) continue;
      const m = line.match(/^([A-Za-z0-9_]+)\s*=\s*(.*)$/); if (!m) continue;
      if (!(m[1] in process.env)) process.env[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
    }
  } catch { /* ignore */ }
}
