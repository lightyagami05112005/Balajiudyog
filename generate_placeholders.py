import os
import urllib.parse

template = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>__TITLE__ — Balaji Udyog B2B Exports</title>
<meta name="description" content="__DESC_META__">
<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__ — Balaji Udyog">
<meta property="og:description" content="__DESC_META__">
<meta property="og:image" content="__HERO_CLEAN__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../../assets/site.css?v=3">
<style>
  :root {
    --b2b-bg: #FFFFFF;
    --b2b-surface: #F9FAFB;
    --b2b-border: #E5E7EB;
    --b2b-text: #1F2937;
    --b2b-text-light: #6B7280;
    --b2b-primary: #0F172A;
    --b2b-primary-hover: #1E293B;
    --b2b-accent: #C87B53;
    --b2b-wa: #25D366;
    --b2b-wa-hover: #22BF5B;
    --b2b-shadow: 0 4px 24px rgba(0,0,0,0.06);
    --font-head: 'Montserrat', sans-serif;
    --font-body: 'Inter', sans-serif;
  }
  body { background: var(--b2b-bg); color: var(--b2b-text); font-family: var(--font-body); margin: 0; padding: 0; line-height: 1.6; }
  .wrap { max-width: 1400px; margin: 0 auto; padding: 0 40px; }
  
  /* B2B Header */
  .pdp-header { padding: 20px 0; border-bottom: 1px solid var(--b2b-border); background: #fff; position: sticky; top: 0; z-index: 100; }
  .pdp-header .wrap { display: flex; justify-content: space-between; align-items: center; }
  .pdp-logo { font-family: var(--font-head); font-weight: 700; font-size: 20px; color: var(--b2b-primary); text-decoration: none; letter-spacing: -0.02em; display:flex; align-items:center; gap:10px; }
  .pdp-logo img { height: 32px; border-radius: 4px; }
  .pdp-logo span { color: var(--b2b-accent); font-weight: 400; font-size: 13px; margin-left: 8px; letter-spacing: 0.05em; text-transform: uppercase; }
  .pdp-nav a { color: var(--b2b-text); text-decoration: none; font-size: 14px; font-weight: 500; margin-left: 24px; transition: color 0.2s; }
  .pdp-nav a:hover { color: var(--b2b-accent); }
  @media (max-width: 768px) { .pdp-nav { display: none; } }

  /* Breadcrumbs */
  .breadcrumbs { padding: 24px 0 0; font-size: 13px; color: var(--b2b-text-light); }
  .breadcrumbs a { color: var(--b2b-text); text-decoration: none; transition: color 0.2s; }
  .breadcrumbs a:hover { color: var(--b2b-accent); }
  .breadcrumbs span { margin: 0 8px; }

  /* Product Layout */
  .pdp-main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; padding: 40px 0 80px; align-items: start; }
  @media (max-width: 992px) { .pdp-main-grid { grid-template-columns: 1fr; gap: 40px; } }
  
  /* Left Side: Images */
  .pdp-gallery { display: flex; flex-direction: column; gap: 16px; position: sticky; top: 100px; }
  .pdp-hero-image { width: 100%; aspect-ratio: 4/3; background: var(--b2b-surface); border-radius: 12px; overflow: hidden; position: relative; border: 1px solid var(--b2b-border); cursor: zoom-in; display:flex; align-items:center; justify-content:center; }
  .pdp-hero-image img { max-width: 100%; max-height: 100%; object-fit: contain; transition: transform 0.4s ease; padding: 40px; }
  .pdp-hero-image:hover img { transform: scale(1.4); }
  .pdp-thumbnails { display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: none; }
  .pdp-thumbnails::-webkit-scrollbar { display: none; }
  .pdp-thumb { width: 80px; height: 80px; border-radius: 8px; background: var(--b2b-surface); border: 2px solid transparent; cursor: pointer; overflow: hidden; flex-shrink: 0; transition: border-color 0.2s; display:flex; align-items:center; justify-content:center; }
  .pdp-thumb img { max-width: 100%; max-height: 100%; object-fit: contain; padding: 8px; }
  .pdp-thumb:hover, .pdp-thumb.active { border-color: var(--b2b-primary); }

  /* Right Side: Details */
  .pdp-details { display: flex; flex-direction: column; }
  .pdp-category { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: var(--b2b-text-light); margin-bottom: 12px; }
  .pdp-title { font-family: var(--font-head); font-size: 42px; font-weight: 600; letter-spacing: -0.02em; color: var(--b2b-primary); margin: 0 0 16px 0; line-height: 1.1; }
  .pdp-sku { display: inline-block; padding: 4px 12px; background: var(--b2b-surface); border: 1px solid var(--b2b-border); border-radius: 4px; font-family: monospace; font-size: 13px; color: var(--b2b-text-light); margin-bottom: 24px; align-self: flex-start; }
  .pdp-desc { font-size: 16px; color: var(--b2b-text); margin-bottom: 32px; line-height: 1.7; }

  /* Spec Cards */
  .pdp-specs { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 40px; }
  @media (max-width: 600px) { .pdp-specs { grid-template-columns: 1fr; } }
  .spec-card { background: var(--b2b-surface); border: 1px solid var(--b2b-border); padding: 16px; border-radius: 8px; display: flex; flex-direction: column; gap: 4px; }
  .spec-label { font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: var(--b2b-text-light); }
  .spec-val { font-size: 15px; font-weight: 500; color: var(--b2b-primary); }

  /* Buttons */
  .pdp-actions { display: flex; flex-direction: column; gap: 16px; margin-bottom: 48px; }
  .btn-primary, .btn-wa { display: flex; align-items: center; justify-content: center; width: 100%; padding: 18px 32px; border-radius: 8px; font-size: 16px; font-weight: 600; text-decoration: none; transition: all 0.2s; gap: 12px; border: none; cursor: pointer; font-family: var(--font-body); }
  .btn-primary { background: var(--b2b-primary); color: #fff; }
  .btn-primary:hover { background: var(--b2b-primary-hover); transform: translateY(-2px); box-shadow: var(--b2b-shadow); }
  .btn-wa { background: var(--b2b-wa); color: #fff; }
  .btn-wa:hover { background: var(--b2b-wa-hover); transform: translateY(-2px); box-shadow: var(--b2b-shadow); }
  .btn-wa svg { width: 20px; height: 20px; fill: currentColor; }

  /* Trust Banner */
  .trust-banner { display: flex; gap: 24px; align-items: center; padding: 20px; background: var(--b2b-surface); border-radius: 8px; border: 1px solid var(--b2b-border); flex-wrap: wrap; }
  .trust-item { display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 500; color: var(--b2b-text); }
  .trust-item svg { width: 18px; height: 18px; color: var(--b2b-accent); }

  /* Sections */
  .section-title { font-family: var(--font-head); font-size: 28px; font-weight: 600; color: var(--b2b-primary); margin: 0 0 32px 0; letter-spacing: -0.01em; }
  .section { padding: 80px 0; border-top: 1px solid var(--b2b-border); }
  .section.bg-surface { background: var(--b2b-surface); border-top: none; }

  /* Form */
  .inquiry-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; }
  @media (max-width: 800px) { .inquiry-grid { grid-template-columns: 1fr; align-items: start; } }
  .form-group { margin-bottom: 20px; }
  .form-group label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 8px; color: var(--b2b-primary); }
  .form-group input, .form-group textarea { width: 100%; padding: 14px 16px; border: 1px solid var(--b2b-border); border-radius: 8px; font-family: var(--font-body); font-size: 15px; transition: border-color 0.2s; background: #fff; box-sizing: border-box; }
  .form-group input:focus, .form-group textarea:focus { outline: none; border-color: var(--b2b-primary); box-shadow: 0 0 0 3px rgba(15,23,42,0.05); }
  .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media (max-width: 600px) { .form-row { grid-template-columns: 1fr; gap: 0; } }
  
  /* Trust Section list */
  .trust-list { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 800px) { .trust-list { grid-template-columns: 1fr; } }
  .trust-list-item { display: flex; align-items: flex-start; gap: 16px; }
  .trust-icon { width: 48px; height: 48px; border-radius: 12px; background: rgba(200,123,83,0.1); color: var(--b2b-accent); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .trust-icon svg { width: 24px; height: 24px; }
  .trust-text h4 { margin: 0 0 6px 0; font-size: 16px; font-weight: 600; color: var(--b2b-primary); }
  .trust-text p { margin: 0; font-size: 14px; color: var(--b2b-text-light); }

  /* Related */
  .related-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
  @media (max-width: 992px) { .related-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 600px) { .related-grid { grid-template-columns: 1fr; } }
  .related-card { background: #fff; border: 1px solid var(--b2b-border); border-radius: 12px; overflow: hidden; text-decoration: none; color: inherit; transition: all 0.3s; display: block; }
  .related-card:hover { transform: translateY(-4px); box-shadow: var(--b2b-shadow); border-color: var(--b2b-text-light); }
  .related-img { width: 100%; aspect-ratio: 4/3; background: var(--b2b-surface); padding: 24px; border-bottom: 1px solid var(--b2b-border); display: flex; align-items: center; justify-content: center;}
  .related-img img { max-width: 100%; max-height: 100%; object-fit: contain; mix-blend-mode: multiply; }
  .related-info { padding: 20px; }
  .related-info h4 { margin: 0 0 8px 0; font-size: 15px; font-weight: 600; color: var(--b2b-primary); line-height: 1.4; }
  .related-info p { margin: 0; font-size: 13px; color: var(--b2b-text-light); font-weight: 500; }
</style>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "__TITLE__",
  "sku": "__SKU__",
  "brand": {
    "@type": "Brand",
    "name": "Balaji Udyog"
  },
  "category": "__CAT__",
  "description": "__DESC_META__",
  "image": "https://www.balajiudyog.com__HERO_CLEAN__"
}
</script>
</head>
<body>

<!-- Header -->
<header class="pdp-header">
  <div class="wrap">
    <a href="../../../Balaji Udyog.html" class="pdp-logo">
      <img src="../../../assets/images/logo.jpg" alt="Balaji Udyog Logo">
      BALAJI UDYOG <span>B2B Export</span>
    </a>
    <nav class="pdp-nav">
      <a href="../../../Balaji Udyog.html">Home</a>
      <a href="../../../pages/Products.html">Products</a>
      <a href="../../../pages/Contact.html">Contact Export Team</a>
    </nav>
  </div>
</header>

<!-- Main Product Area -->
<div class="wrap">
  <div class="breadcrumbs">
    <a href="../../../Balaji Udyog.html">Home</a> <span>/</span> 
    <a href="../../../pages/Products.html">Products</a> <span>/</span> 
    <a href="../__CAT_URL__.html">__CAT__</a> <span>/</span> 
    <strong style="color:var(--b2b-primary)">__TITLE__</strong>
  </div>

  <div class="pdp-main-grid">
    <!-- Left: Gallery -->
    <div class="pdp-gallery">
      <div class="pdp-hero-image">
        <img id="main-image" src="__HERO__" alt="__TITLE__ - Balaji Udyog Export Quality">
      </div>
      <div class="pdp-thumbnails">
        __THUMBS__
      </div>
    </div>

    <!-- Right: Details -->
    <div class="pdp-details">
      <div class="pdp-category">__CAT__</div>
      <h1 class="pdp-title">__TITLE__</h1>
      <div class="pdp-sku">SKU: __SKU__</div>
      
      <p class="pdp-desc">__DESC_HTML__</p>

      <div class="pdp-specs">
        __SPECS__
      </div>

      <div class="pdp-actions">
        <a href="#inquiry-form" class="btn-primary">Enquire About This Product</a>
        <a href="https://wa.me/916290746602?text=__WA_TEXT__" target="_blank" class="btn-wa">
          <svg viewBox="0 0 24 24"><path d="M20.5 3.5A11 11 0 0 0 3.4 17.2L2 22l4.9-1.3a11 11 0 0 0 16.6-9.4 11 11 0 0 0-3-7.8zM12 20a8.9 8.9 0 0 1-4.6-1.3l-.3-.2-2.9.8.8-2.8-.2-.3A9 9 0 1 1 12 20z"/></svg>
          Chat on WhatsApp
        </a>
      </div>

      <div class="trust-banner">
        <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> OEM Manufacturing</div>
        <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Export Quality</div>
        <div class="trust-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Reliable Delivery</div>
      </div>
    </div>
  </div>
</div>

<!-- Inquiry Form Section -->
<section id="inquiry-form" class="section bg-surface">
  <div class="wrap">
    <div class="inquiry-grid">
      <div>
        <h2 class="section-title">Request a Custom Quote</h2>
        <p style="color:var(--b2b-text-light); font-size:16px; margin-bottom:32px; max-width:400px; line-height:1.7;">
          Balaji Udyog is an international B2B exporter. Submit your requirements below, and our export team will provide a comprehensive quotation including pricing, lead times, and shipping terms to your destination port.
        </p>
      </div>
      <div>
        <form style="background:#fff; padding:40px; border-radius:12px; border:1px solid var(--b2b-border); box-shadow:var(--b2b-shadow);" onsubmit="event.preventDefault(); alert('Inquiry sent successfully. Our export team will contact you shortly.');">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name</label>
              <input type="text" required placeholder="John Doe">
            </div>
            <div class="form-group">
              <label>Company Name</label>
              <input type="text" required placeholder="Your Company Ltd.">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Country</label>
              <input type="text" required placeholder="United Kingdom">
            </div>
            <div class="form-group">
              <label>WhatsApp Number</label>
              <input type="tel" required placeholder="+44 ...">
            </div>
          </div>
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" required placeholder="john@company.com">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Product Name</label>
              <input type="text" readonly value="__TITLE__ (SKU: __SKU__)" style="background:var(--b2b-surface); color:var(--b2b-text-light);">
            </div>
            <div class="form-group">
              <label>Quantity Required</label>
              <input type="text" required placeholder="e.g. 1000 units">
            </div>
          </div>
          <div class="form-group">
            <label>Message (Optional)</label>
            <textarea rows="3" placeholder="Port of destination, custom finish requirements, private label requests..."></textarea>
          </div>
          <button type="submit" class="btn-primary" style="margin-top:16px; padding:16px;">Send Inquiry</button>
        </form>
      </div>
    </div>
  </div>
</section>

<!-- Trust Section -->
<section class="section">
  <div class="wrap">
    <h2 class="section-title" style="text-align:center; margin-bottom:56px;">Why Buy From Balaji Udyog</h2>
    <div class="trust-list">
      <div class="trust-list-item">
        <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></div>
        <div class="trust-text">
          <h4>Export Quality Products</h4>
          <p>Manufactured to meet stringent international standards for durability and finish.</p>
        </div>
      </div>
      <div class="trust-list-item">
        <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg></div>
        <div class="trust-text">
          <h4>OEM & Private Label Manufacturing</h4>
          <p>Custom branding, packaging, and product modifications tailored to your brand.</p>
        </div>
      </div>
      <div class="trust-list-item">
        <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></div>
        <div class="trust-text">
          <h4>Worldwide Shipping</h4>
          <p>FOB, CIF, and CFR terms available with seamless delivery to global ports.</p>
        </div>
      </div>
      <div class="trust-list-item">
        <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg></div>
        <div class="trust-text">
          <h4>Secure Packaging</h4>
          <p>Multi-layer export-grade packaging ensuring zero transit damage.</p>
        </div>
      </div>
      <div class="trust-list-item">
        <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg></div>
        <div class="trust-text">
          <h4>Reliable Delivery</h4>
          <p>Strict adherence to lead times with consistent production schedules.</p>
        </div>
      </div>
      <div class="trust-list-item">
        <div class="trust-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></div>
        <div class="trust-text">
          <h4>Bulk Order Support</h4>
          <p>Scalable manufacturing capacity to handle large volumes and mixed containers.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Related Products -->
<section class="section bg-surface">
  <div class="wrap">
    <h2 class="section-title">You May Also Like</h2>
    <div class="related-grid">
      __RELATED__
    </div>
  </div>
</section>

<!-- Footer -->
<footer style="background:var(--b2b-primary); color:rgba(255,255,255,0.7); padding:60px 0; font-size:14px;">
  <div class="wrap" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:24px;">
    <div>
      <b style="color:#fff; font-size:18px; font-family:var(--font-head); letter-spacing:-0.02em;">BALAJI UDYOG</b><br>
      Premium Indian hardware and decor exporter since 1998.
    </div>
    <div>
      balaji6ab@gmail.com &nbsp;|&nbsp; +91 6290 746 602<br>
      &copy; 2026 Balaji Udyog. All rights reserved.
    </div>
  </div>
</footer>

<script>
  function swapImage(src, el) {
    document.getElementById('main-image').src = src;
    document.querySelectorAll('.pdp-thumb').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
  }
</script>
</body>
</html>
"""

products = [
    {
        "filename": "premium-brass-cutlery-set.html",
        "title": "Premium Brass Cutlery Set (16 Piece)",
        "sku": "BC-16P",
        "category": "Stainless Steel and Brass Cutleries",
        "cat_url": "Stainless Steel and Brass Cutleries",
        "desc": "A complete 16-piece premium brass cutlery set designed for high-end dining experiences. Includes 4 dinner forks, 4 dinner knives, 4 dinner spoons, and 4 dessert spoons.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Solid Brass",
            "Finish": "Polished Gold",
            "Packaging": "Export Carton",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "50 Sets"
        }
    },
    {
        "filename": "gold-plated-stainless-steel-spoons.html",
        "title": "Gold Plated Stainless Steel Spoons",
        "sku": "SS-GLD-SPN",
        "category": "Stainless Steel and Brass Cutleries",
        "cat_url": "Stainless Steel and Brass Cutleries",
        "desc": "High-quality 304 grade stainless steel spoons featuring a durable titanium gold plating. Perfect for hospitality and fine dining establishments.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "304 Stainless Steel",
            "Finish": "Gold Plated",
            "Packaging": "Bulk / Retail Box",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "500 Pieces"
        }
    },
    {
        "filename": "hammered-brass-salad-servers.html",
        "title": "Hammered Brass Salad Servers",
        "sku": "HB-SAL-SRV",
        "category": "Stainless Steel and Brass Cutleries",
        "cat_url": "Stainless Steel and Brass Cutleries",
        "desc": "Handcrafted hammered brass salad serving spoons. These servers offer a rustic yet elegant appeal for modern table settings.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Brass",
            "Finish": "Hammered Antique",
            "Packaging": "Gift Box",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "100 Sets"
        }
    },
    {
        "filename": "vintage-copper-dinner-forks.html",
        "title": "Vintage Copper Dinner Forks",
        "sku": "VC-DIN-FRK",
        "category": "Stainless Steel and Brass Cutleries",
        "cat_url": "Stainless Steel and Brass Cutleries",
        "desc": "Dinner forks with an authentic vintage copper finish. Ergonomically designed for comfort and crafted for lasting durability in commercial use.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Stainless Steel",
            "Finish": "Vintage Copper",
            "Packaging": "Export Carton",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "500 Pieces"
        }
    },
    {
        "filename": "antique-brass-chandelier.html",
        "title": "Antique Brass Chandelier",
        "sku": "LT-ABC-01",
        "category": "Lighting",
        "cat_url": "Lighting",
        "desc": "A magnificent antique brass chandelier with 8 arms, suitable for grand entrance halls and luxury dining rooms. Features intricate detailing and robust construction.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Solid Brass",
            "Finish": "Antique Brass",
            "Bulb Type": "E14 / E27 Options",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "10 Pieces"
        }
    },
    {
        "filename": "industrial-pendant-lamp-shade.html",
        "title": "Industrial Pendant Lamp Shade",
        "sku": "LT-IPL-02",
        "category": "Lighting",
        "cat_url": "Lighting",
        "desc": "Vintage-inspired industrial pendant lamp shade. Ideal for modern cafes, restaurants, and loft-style interiors. Spun metal construction with a matte finish.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Iron / Aluminum",
            "Finish": "Matte Black / Custom",
            "Dimensions": "300mm Diameter",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "50 Pieces"
        }
    },
    {
        "filename": "decorative-glass-wall-sconce.html",
        "title": "Decorative Glass Wall Sconce",
        "sku": "LT-DGW-03",
        "category": "Lighting",
        "cat_url": "Lighting",
        "desc": "Elegant wall sconce featuring hand-blown textured glass and a brass backplate. Provides warm, diffused ambient lighting for hospitality corridors and bedrooms.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Brass & Glass",
            "Finish": "Polished Brass",
            "Installation": "Wall Mounted",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "30 Pieces"
        }
    },
    {
        "filename": "modern-minimalist-table-lamp.html",
        "title": "Modern Minimalist Table Lamp",
        "sku": "LT-MMT-04",
        "category": "Lighting",
        "cat_url": "Lighting",
        "desc": "A sleek, minimalist table lamp with a heavy metal base and adjustable shade. Perfect for boutique hotel desks and modern residential projects.",
        "img": "../../../assets/images/placeholder.jpg",
        "specs": {
            "Material": "Steel / Brass",
            "Finish": "Brushed Nickel",
            "Power": "110V - 240V Compatible",
            "OEM & Private Label": "Available on request",
            "Export Quality": "Premium B2B Standard",
            "MOQ": "50 Pieces"
        }
    }
]

out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"
os.makedirs(out_dir, exist_ok=True)

for p in products:
    specs_html = ""
    for k, v in p["specs"].items():
        specs_html += f'<div class="spec-card"><span class="spec-label">{k}</span><span class="spec-val">{v}</span></div>\n'
        
    thumbs_html = f'<div class="pdp-thumb active" onclick="swapImage(\'{p["img"]}\', this)"><img src="{p["img"]}" alt="Thumbnail"></div>\n'
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {p['title']} ({p['sku']}). Please share quotation, MOQ and export details.")
    
    related_html = "" # Blank for placeholders
    
    new_content = template
    new_content = new_content.replace('__TITLE__', p['title'])
    new_content = new_content.replace('__SKU__', p['sku'])
    new_content = new_content.replace('__CAT__', p['category'])
    new_content = new_content.replace('__CAT_URL__', p['cat_url'])
    new_content = new_content.replace('__DESC_META__', p['desc'].replace('"', '&quot;'))
    new_content = new_content.replace('__DESC_HTML__', p['desc'])
    new_content = new_content.replace('__HERO__', p['img'])
    new_content = new_content.replace('__HERO_CLEAN__', p['img'].replace('../../../', '/'))
    new_content = new_content.replace('__THUMBS__', thumbs_html)
    new_content = new_content.replace('__SPECS__', specs_html)
    new_content = new_content.replace('__WA_TEXT__', wa_text)
    new_content = new_content.replace('__RELATED__', related_html)

    file_path = os.path.join(out_dir, p['filename'])
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Generated {p['filename']}")

print("Placeholders generated successfully.")
