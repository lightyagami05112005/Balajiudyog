/* Balaji Udyog — lead capture client.
   Intercepts every .form submit and posts it to the lead backend
   (POST /api/inquiry). If the backend is unreachable, it falls back to a
   WhatsApp / email prompt so an inquiry is never lost in front of the buyer.

   Configure a non-default backend before this script loads:
     <script>window.BU_LEAD_API = 'https://api.balajiudyog.com';</script>
*/
(function () {
  var API = (window.BU_LEAD_API || 'http://localhost:4000').replace(/\/$/, '');

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function collect(form) {
    var fields = {};
    form.querySelectorAll('.field').forEach(function (f) {
      var label = f.querySelector('label');
      var ctrl = f.querySelector('input, select, textarea');
      if (label && ctrl && ctrl.value) {
        fields[label.textContent.trim().replace(/\s+/g, ' ')] = ctrl.value;
      }
    });
    return fields;
  }

  function note(form, html, ok) {
    var box = document.createElement('div');
    box.className = 'lead-note';
    box.style.cssText = 'margin-top:16px;padding:14px 16px;font-family:var(--mono,monospace);' +
      'font-size:12.5px;line-height:1.6;border:1px solid ' + (ok ? 'rgba(30,184,88,.5)' : 'rgba(200,165,91,.65)') +
      ';background:' + (ok ? 'rgba(30,184,88,.08)' : 'rgba(200,165,91,.08)') + ';color:var(--ink,#14171c)';
    box.innerHTML = html;
    form.appendChild(box);
  }

  function handler(e) {
    e.preventDefault();
    var form = e.currentTarget;
    var btn = form.querySelector('button[type=submit]');
    if (btn) { btn.disabled = true; btn.dataset._t = btn.textContent; btn.textContent = 'Sending…'; }

    var payload = collect(form);
    payload.access_key = '9a9dd082-db55-46ac-ac3d-861c7d2ca98e'; // Web3Forms access key
    payload.subject = 'New Inquiry from ' + (document.title || 'website').slice(0, 120);
    payload.page_url = location.pathname;

    fetch('https://api.web3forms.com/submit', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .then(function (d) {
        if (!d || !d.success) throw new Error((d && d.message) || 'bad response');
        form.querySelectorAll('.field, .actions, .form-note, .form-row').forEach(function (el) { el.style.display = 'none'; });
        note(form,
          'Thank you — your inquiry has reached our Global desk. We respond within one business day.',
          true);
      })
      .catch(function () {
        var wa = 'https://wa.me/916290746602?text=' + encodeURIComponent('Hello Balaji Udyog — I would like to send an export inquiry.');
        note(form,
          'We could not reach the inquiry desk just now. Please contact us directly:<br>' +
          'WhatsApp: <a href="' + wa + '" target="_blank" rel="noopener" style="color:#1eb858;font-weight:700">message us</a> &middot; ' +
          'Email: <a href="mailto:export@balajiudyog.com" style="color:var(--gold-dim,#8a7340);font-weight:700">export@balajiudyog.com</a>',
          false);
      })
      .finally(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset._t || 'Send inquiry'; } });
  }

  ready(function () {
    document.querySelectorAll('form.form').forEach(function (form) {
      form.onsubmit = null;                 // drop the inline alert handler
      form.addEventListener('submit', handler);
    });
  });
})();
