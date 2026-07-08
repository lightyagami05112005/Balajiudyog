import os
import glob
from bs4 import BeautifulSoup
import fitz
import urllib.parse
from PIL import Image

# 1. Clean up old furniture hardware items
items_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"
html_files = glob.glob(os.path.join(items_dir, "*.html"))

deleted_count = 0
for file_path in html_files:
    if os.path.basename(file_path) == "index.html":
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    cat_el = soup.find('div', class_='pdp-category')
    if cat_el:
        cat = cat_el.text.strip().lower()
        if "furniture" in cat or "lock" in cat:
            os.remove(file_path)
            deleted_count += 1
print(f"Deleted {deleted_count} old furniture hardware products.")


# 2. Generate new 5 items
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
    <a href="../__CAT_URL__.html">__CAT__</a> <span>/</span> 
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
          Chat on WhatsApp
        </a>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

new_products = [
    {
        "filename": "rbm-12-heavy-spoon.html",
        "title": "RBM-12 Heavy Spoon Mortise Handle",
        "sku": "RBM-12",
        "category": "Furniture Hardware and Locking Mechanism",
        "cat_url": "Furniture Hardware and Locking Mechanism",
        "desc": "Premium solid brass mortise door handle with an elegant, heavy spoon design and polished gold finish.",
        "img": "../../../assets/images/products/items/rbm-12.jpg",
        "specs": {"Material": "Solid Brass", "Finish": "Polished Gold", "OEM": "Available", "MOQ": "100 Sets"},
        "crop_rect": (186, 331, 240, 345)
    },
    {
        "filename": "rbm-cielo.html",
        "title": "RBM Cielo Mortise Handle",
        "sku": "Cielo",
        "category": "Furniture Hardware and Locking Mechanism",
        "cat_url": "Furniture Hardware and Locking Mechanism",
        "desc": "Sleek and modern Cielo mortise handle crafted from solid brass with a brilliant polished finish.",
        "img": "../../../assets/images/products/items/rbm-cielo.jpg",
        "specs": {"Material": "Solid Brass", "Finish": "Polished Gold", "OEM": "Available", "MOQ": "100 Sets"},
        "crop_rect": (416, 349, 444, 362)
    },
    {
        "filename": "rbm-7-zen.html",
        "title": "RBM-7 Zen Mortise Handle",
        "sku": "RBM-7",
        "category": "Furniture Hardware and Locking Mechanism",
        "cat_url": "Furniture Hardware and Locking Mechanism",
        "desc": "Minimalist Zen style mortise handle offering clean lines and robust brass construction.",
        "img": "../../../assets/images/products/items/rbm-7.jpg",
        "specs": {"Material": "Solid Brass", "Finish": "Polished Gold", "OEM": "Available", "MOQ": "100 Sets"},
        "crop_rect": (623, 331, 669, 345)
    },
    {
        "filename": "rbm-logan.html",
        "title": "RBM Logan Mortise Handle",
        "sku": "Logan",
        "category": "Furniture Hardware and Locking Mechanism",
        "cat_url": "Furniture Hardware and Locking Mechanism",
        "desc": "Ergonomic Logan mortise handle finished in premium nickel/silver for contemporary interiors.",
        "img": "../../../assets/images/products/items/rbm-logan.jpg",
        "specs": {"Material": "Solid Brass", "Finish": "Satin Nickel", "OEM": "Available", "MOQ": "100 Sets"},
        "crop_rect": (839, 349, 874, 362)
    },
    {
        "filename": "rbm-8-renault.html",
        "title": "RBM-8 Renault Mortise Handle",
        "sku": "RBM-8",
        "category": "Furniture Hardware and Locking Mechanism",
        "cat_url": "Furniture Hardware and Locking Mechanism",
        "desc": "Classic Renault mortise handle featuring sweeping curves and a luxurious gold finish.",
        "img": "../../../assets/images/products/items/rbm-8.jpg",
        "specs": {"Material": "Solid Brass", "Finish": "Polished Gold", "OEM": "Available", "MOQ": "100 Sets"},
        "crop_rect": (1035, 331, 1081, 345)
    }
]

for p in new_products:
    specs_html = "".join([f'<div class="spec-card"><span class="spec-label">{k}</span><span class="spec-val">{v}</span></div>' for k,v in p["specs"].items()])
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {p['title']} ({p['sku']}).")
    
    new_content = template.replace('__TITLE__', p['title']).replace('__SKU__', p['sku'])
    new_content = new_content.replace('__CAT__', p['category']).replace('__CAT_URL__', p['cat_url'])
    new_content = new_content.replace('__DESC_META__', p['desc']).replace('__DESC_HTML__', p['desc'])
    new_content = new_content.replace('__HERO__', p['img']).replace('__HERO_CLEAN__', p['img'].replace('../../../', '/'))
    new_content = new_content.replace('__SPECS__', specs_html).replace('__WA_TEXT__', wa_text)

    with open(os.path.join(items_dir, p['filename']), "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Generated {p['filename']}")

# 3. Crop Images from PDF
pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Furniture Hardware (1).pdf"
img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"
doc = fitz.open(pdf_path)
page = doc[1] # Page 1 (0-indexed 1) where they are located
mat = fitz.Matrix(3.0, 3.0) # Render at 3x for high resolution
pix = page.get_pixmap(matrix=mat)
img_path = os.path.join(img_out_dir, "temp_catalog.png")
pix.save(img_path)

img = Image.open(img_path)
for p in new_products:
    # crop_rect is in 1x scale points (x0, y0, x1, y1)
    # We rendered at 3x scale
    x0, y0, x1, y1 = p["crop_rect"]
    x0, y0, x1, y1 = x0*3, y0*3, x1*3, y1*3
    
    # The image is ABOVE the text. So crop from y0-650 to y0.
    # And horizontally, center around text.
    cx = (x0 + x1) / 2
    crop_w = 350
    crop_h = 750
    
    left = cx - crop_w/2
    right = cx + crop_w/2
    top = y0 - crop_h
    bottom = y0 + 10 # slightly below text to capture anything near it, maybe text too? Actually let's exclude text
    
    # Wait, RBM logo is below the text?
    # No, look at the uploaded image: Handle is at top, text "RBM-12" is at bottom.
    # Let's crop from y0-750 to y0-10
    bottom = y0 - 30
    
    cropped = img.crop((left, top, right, bottom))
    out_img = os.path.join(img_out_dir, os.path.basename(p["img"]))
    cropped.save(out_img)
    print(f"Saved {out_img}")

os.remove(img_path)
print("Finished setting up handles.")
