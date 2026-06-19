(function() {
  if (document.getElementById('bu-inquiry-modal')) return; // already injected

  const style = document.createElement('style');
  style.innerHTML = `
    .bu-modal-overlay {
      position: fixed; inset: 0; z-index: 10000;
      background: rgba(6, 18, 42, 0.85); backdrop-filter: blur(8px);
      display: flex; align-items: center; justify-content: center;
      opacity: 0; visibility: hidden; transition: all 0.4s ease;
      padding: 20px;
    }
    .bu-modal-overlay.active { opacity: 1; visibility: visible; }
    .bu-modal {
      background: #fff; width: 100%; max-width: 520px;
      box-shadow: 0 40px 80px rgba(0,0,0,0.3);
      position: relative; transform: translateY(30px) scale(0.95);
      transition: all 0.4s cubic-bezier(0.2, 0.7, 0.2, 1);
      border: 1px solid rgba(200, 165, 91, 0.3);
      max-height: 90vh; overflow-y: auto;
    }
    .bu-modal-overlay.active .bu-modal { transform: translateY(0) scale(1); }
    .bu-modal-close {
      position: absolute; top: 20px; right: 24px;
      font-size: 28px; color: rgba(10, 29, 58, 0.4); cursor: pointer;
      line-height: 1; transition: color 0.3s; z-index: 2;
    }
    .bu-modal-close:hover { color: #0a1d3a; }
    .bu-modal-header {
      padding: 40px 40px 24px; background: #06122a; color: #FCFBF8;
      border-bottom: 3px solid #c8a55b;
    }
    .bu-modal-header h2 { font-size: 28px; color: #FCFBF8; margin-bottom: 12px; }
    .bu-modal-header p { font-size: 15px; color: #E5E7EB; line-height: 1.6; }
    .bu-modal-body { padding: 32px 40px 40px; }
    .bu-modal .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
    .bu-modal .form-row.full { grid-template-columns: 1fr; }
    .bu-modal .field label { display: block; font-family: 'JetBrains Mono', monospace; font-size: 10.5px; letter-spacing: 0.18em; color: #8a7340; text-transform: uppercase; margin-bottom: 8px; }
    .bu-modal .field input, .bu-modal .field textarea {
      width: 100%; border: 0; border-bottom: 1px solid rgba(10, 29, 58, 0.15);
      background: transparent; padding: 10px 0; font-family: 'Inter', sans-serif; font-size: 15px;
      color: #14171c; outline: none; transition: border-color 0.25s;
    }
    .bu-modal .field input:focus, .bu-modal .field textarea:focus { border-bottom-color: #c8a55b; }
    .bu-modal .field textarea { resize: none; min-height: 60px; }
    .bu-modal-actions { display: flex; gap: 14px; margin-top: 32px; flex-wrap: wrap; }
    .bu-modal-btn {
      display: inline-flex; align-items: center; gap: 12px; padding: 14px 24px;
      font-weight: 500; font-size: 14px; letter-spacing: 0.04em;
      text-transform: uppercase; border: 1px solid transparent;
      cursor: pointer; transition: all 0.3s;
    }
    .bu-modal-btn-primary { background: #0a1d3a; color: #FCFBF8; }
    .bu-modal-btn-primary:hover { background: #c8a55b; color: #0a1d3a; }
    .bu-modal-btn-wa { background: #1eb858; color: #fff; }
    .bu-modal-btn-wa:hover { background: #17a04b; }
    @media(max-width: 560px) {
      .bu-modal .form-row { grid-template-columns: 1fr; }
      .bu-modal-header { padding: 32px 24px 20px; }
      .bu-modal-body { padding: 24px 24px 32px; }
    }
  `;
  document.head.appendChild(style);

  const modalHtml = `
    <div class="bu-modal-overlay" id="bu-inquiry-modal">
      <div class="bu-modal" onclick="event.stopPropagation()">
        <div class="bu-modal-close" id="bu-modal-close">&times;</div>
        <div class="bu-modal-header">
          <h2>Talk With Our Experts</h2>
          <p>Our team will help you find the right products, pricing and sourcing solutions for your business.</p>
        </div>
        <div class="bu-modal-body">
          <form id="bu-modal-form" onsubmit="event.preventDefault(); document.getElementById('bu-modal-close').click(); alert('Inquiry sent! Our global export team will respond shortly.');">
            <div class="form-row">
              <div class="field"><label>Full Name</label><input type="text" required placeholder="Your name"></div>
              <div class="field"><label>Company Name</label><input type="text" required placeholder="Company name"></div>
            </div>
            <div class="form-row">
              <div class="field"><label>Country</label><input type="text" required placeholder="Your country"></div>
              <div class="field"><label>WhatsApp Number</label><input type="tel" required placeholder="+1 ..."></div>
            </div>
            <div class="form-row full">
              <div class="field"><label>Email Address</label><input type="email" required placeholder="you@company.com"></div>
            </div>
            <div class="form-row full">
              <div class="field"><label>Product Requirement</label><textarea required placeholder="What products are you looking for? Target volumes?"></textarea></div>
            </div>
            <div class="bu-modal-actions">
              <button type="submit" class="bu-modal-btn bu-modal-btn-primary">Send Inquiry</button>
              <a href="#" id="bu-modal-wa" class="bu-modal-btn bu-modal-btn-wa" target="_blank">Chat on WhatsApp</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);

  const modal = document.getElementById('bu-inquiry-modal');
  const closeBtn = document.getElementById('bu-modal-close');
  const waBtn = document.getElementById('bu-modal-wa');

  // WhatsApp click handler
  waBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const msg = encodeURIComponent("Hello Balaji Udyog, I am interested in your products and would like to discuss sourcing options.");
    window.open(\`https://wa.me/916290746602?text=\${msg}\`, '_blank');
  });

  // Close logic
  closeBtn.addEventListener('click', () => modal.classList.remove('active'));
  modal.addEventListener('click', () => modal.classList.remove('active'));

  // Attach to existing elements dynamically
  function attachTriggers() {
    // Select all product grid items, gallery items, and category cards
    const targets = document.querySelectorAll('.show .it, .gal .gi, .cat, .rel-row .r');
    targets.forEach(t => {
      // Prevent anchor link navigation if it's an <a> tag
      t.addEventListener('click', (e) => {
        // Only prevent default if we're not clicking on a "View Category" button inside it explicitly
        e.preventDefault();
        e.stopPropagation();
        modal.classList.add('active');
      });
      // Make it look clickable
      t.style.cursor = 'pointer';
    });
  }

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachTriggers);
  } else {
    attachTriggers();
  }
})();
