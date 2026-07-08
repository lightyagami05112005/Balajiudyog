import os
import glob
from bs4 import BeautifulSoup
import fitz
import urllib.parse
from PIL import Image

# 1. Clean up old furniture hardware items
items_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"
html_files = glob.glob(os.path.join(items_dir, "*.html"))

for file_path in html_files:
    if os.path.basename(file_path) == "index.html":
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    cat_el = soup.find('div', class_='pdp-category')
    if cat_el:
        cat = cat_el.text.strip().lower()
        if "furniture hardware" in cat:
            os.remove(file_path)

# 2. Define the 12 handles and their grid boundaries
# Grid X boundaries: 90, 310, 525, 735, 940, 1135, 1340
# Grid Y boundaries: Row 1 (30 to 320), Row 2 (380 to 670)

handles = [
    # ROW 1
    {"filename": "rbm-12-heavy-spoon.html", "title": "RBM-12 Heavy Spoon", "sku": "RBM-12", "box": (90, 30, 310, 320)},
    {"filename": "rbm-cielo.html", "title": "RBM Cielo", "sku": "Cielo", "box": (310, 30, 525, 320)},
    {"filename": "rbm-7-zen.html", "title": "RBM-7 Zen", "sku": "RBM-7", "box": (525, 30, 735, 320)},
    {"filename": "rbm-logan.html", "title": "RBM Logan", "sku": "Logan", "box": (735, 30, 940, 320)},
    {"filename": "rbm-8-renault.html", "title": "RBM-8 Renault", "sku": "RBM-8-Renault", "box": (940, 30, 1135, 320)},
    {"filename": "rbm-8-smart.html", "title": "RBM-8 Smart", "sku": "RBM-8-Smart", "box": (1135, 30, 1340, 320)},
    
    # ROW 2
    {"filename": "rbm-19-roxy.html", "title": "RBM-19 Roxy", "sku": "RBM-19", "box": (90, 380, 310, 670)},
    {"filename": "rbm-13-verna.html", "title": "RBM-13 Verna", "sku": "RBM-13", "box": (310, 380, 525, 670)},
    {"filename": "rbm-8-nayaab.html", "title": "RBM-8 Nayaab", "sku": "RBM-8-Nayaab", "box": (525, 380, 735, 670)},
    {"filename": "rbm-8-cedia.html", "title": "RBM-8 Cedia", "sku": "RBM-8-Cedia", "box": (735, 380, 940, 670)},
    {"filename": "rbm-9-simple.html", "title": "RBM-9 Simple", "sku": "RBM-9", "box": (940, 380, 1135, 670)},
    {"filename": "rbm-11-niks.html", "title": "RBM-11 Niks", "sku": "RBM-11", "box": (1135, 380, 1340, 670)}
]

template = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>__TITLE__ — Balaji Udyog B2B Exports</title>
<meta name="description" content="Premium quality __TITLE__ mortise door handle.">
<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__ — Balaji Udyog">
<meta property="og:description" content="Premium quality __TITLE__ mortise door handle.">
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
  .pdp-hero-image img { max-width: 100%; max-height: 100%; object-fit: contain; transition: transform 0.4s ease; padding: 0px; }
  .pdp-hero-image:hover img { transform: scale(1.4); }
  .pdp-thumbnails { display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px; scrollbar-width: none; }
  .pdp-thumbnails::-webkit-scrollbar { display: none; }
  .pdp-thumb { width: 80px; height: 80px; border-radius: 8px; background: var(--b2b-surface); border: 2px solid transparent; cursor: pointer; overflow: hidden; flex-shrink: 0; transition: border-color 0.2s; display:flex; align-items:center; justify-content:center; }
  .pdp-thumb img { max-width: 100%; max-height: 100%; object-fit: contain; padding: 4px; }
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
</style>
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
    <a href="../Furniture Hardware and Locking Mechanism.html">Furniture Hardware and Locking Mechanism</a> <span>/</span> 
    <strong style="color:var(--b2b-primary)">__TITLE__</strong>
  </div>

  <div class="pdp-main-grid">
    <!-- Left: Gallery -->
    <div class="pdp-gallery">
      <div class="pdp-hero-image">
        <img id="main-image" src="__HERO__" alt="__TITLE__ - Balaji Udyog Export Quality">
      </div>
    </div>

    <!-- Right: Details -->
    <div class="pdp-details">
      <div class="pdp-category">Furniture Hardware and Locking Mechanism</div>
      <h1 class="pdp-title">__TITLE__</h1>
      <div class="pdp-sku">SKU: __SKU__</div>
      
      <p class="pdp-desc">Premium quality __TITLE__ mortise door handle designed for luxurious interiors and robust performance. Manufactured from high-grade solid brass for durability.</p>

      <div class="pdp-specs">
        <div class="spec-card"><span class="spec-label">Material</span><span class="spec-val">Solid Brass</span></div>
        <div class="spec-card"><span class="spec-label">Finish</span><span class="spec-val">Polished / Satin</span></div>
        <div class="spec-card"><span class="spec-label">MOQ</span><span class="spec-val">100 Sets</span></div>
        <div class="spec-card"><span class="spec-label">OEM</span><span class="spec-val">Available</span></div>
      </div>

      <div class="pdp-actions">
        <a href="#inquiry-form" class="btn-primary">Enquire About This Product</a>
        <a href="https://wa.me/916290746602?text=__WA_TEXT__" target="_blank" class="btn-wa">
          Chat on WhatsApp
        </a>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# Generate pages
for p in handles:
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {p['title']} ({p['sku']}).")
    img_path = f"../../../assets/images/products/items/{p['filename'].replace('.html', '.jpg')}"
    
    content = template.replace('__TITLE__', p['title']).replace('__SKU__', p['sku'])
    content = content.replace('__HERO__', img_path).replace('__HERO_CLEAN__', img_path.replace('../../../', '/'))
    content = content.replace('__WA_TEXT__', wa_text)

    with open(os.path.join(items_dir, p['filename']), "w", encoding="utf-8") as f:
        f.write(content)

# 3. Crop Images from PDF using Grid boxes (to preserve original cream background)
pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Furniture Hardware (1).pdf"
img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"
doc = fitz.open(pdf_path)
page = doc[1] 
mat = fitz.Matrix(3.0, 3.0) 
pix = page.get_pixmap(matrix=mat)
temp_img_path = os.path.join(img_out_dir, "temp_catalog_12.png")
pix.save(temp_img_path)

img = Image.open(temp_img_path)

for p in handles:
    l, t, r, b = p["box"]
    # Convert from 1x coords to 3x coords
    l, t, r, b = l*3, t*3, r*3, b*3
    
    cropped = img.crop((l, t, r, b))
    out_img = os.path.join(img_out_dir, p['filename'].replace('.html', '.jpg'))
    cropped.save(out_img)
    print(f"Saved {out_img}")

os.remove(temp_img_path)
print("Finished setting up 12 handles.")
