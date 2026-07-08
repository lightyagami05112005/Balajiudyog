"""
Master extraction script: crops individual products from all PDF catalogues
and generates HTML pages + category pages for each section.
Skips Lighting (user will provide photos).
"""
import fitz
import os
import urllib.parse
from PIL import Image
import cv2
import numpy as np

BASE = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
IMG_OUT = os.path.join(BASE, "assets", "images", "products", "items")
ITEMS_DIR = os.path.join(BASE, "pages", "products", "items")
os.makedirs(IMG_OUT, exist_ok=True)

SCALE = 4  # High res render

def render_page(doc, page_idx):
    page = doc[page_idx]
    mat = fitz.Matrix(SCALE, SCALE)
    pix = page.get_pixmap(matrix=mat)
    tmp = os.path.join(IMG_OUT, f"_tmp_render.png")
    pix.save(tmp)
    # Open and copy image data to memory, then close it explicitly
    with Image.open(tmp) as img:
        img_copy = img.copy()
    os.remove(tmp)
    return img_copy

def crop_grid(img, row, col, rows_spec, cols_spec):
    """Crop a cell from a grid defined by row/col boundary specs."""
    t, b = rows_spec[row]
    l, r = cols_spec[col]
    return img.crop((l*SCALE, t*SCALE, r*SCALE, b*SCALE))

def save_product_img(cropped, filename):
    path = os.path.join(IMG_OUT, filename)
    cropped.save(path, quality=95)
    return path

def make_product_page(product, category_name, category_file):
    """Generate an individual product HTML page."""
    title = product['title']
    sku = product['sku']
    img_file = product['img']
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {title} ({sku}).")
    img_path = f"../../../assets/images/products/items/{img_file}"
    
    material = product.get('material', 'Brass / Steel')
    finish = product.get('finish', 'Polished / Satin')
    
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title} — Balaji Udyog B2B Exports</title>
<meta name="description" content="Premium quality {title} for international B2B export.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg:#FFF;--surface:#F9FAFB;--border:#E5E7EB;--text:#1F2937;--text-light:#6B7280;
    --primary:#0F172A;--primary-hover:#1E293B;--accent:#C87B53;--wa:#25D366;
    --shadow:0 4px 24px rgba(0,0,0,0.06);--font-head:'Montserrat',sans-serif;--font-body:'Inter',sans-serif;
  }}
  body{{background:var(--bg);color:var(--text);font-family:var(--font-body);margin:0;padding:0;line-height:1.6}}
  .wrap{{max-width:1400px;margin:0 auto;padding:0 40px}}
  .pdp-header{{padding:20px 0;border-bottom:1px solid var(--border);background:#fff;position:sticky;top:0;z-index:100}}
  .pdp-header .wrap{{display:flex;justify-content:space-between;align-items:center}}
  .pdp-logo{{font-family:var(--font-head);font-weight:700;font-size:20px;color:var(--primary);text-decoration:none;letter-spacing:-0.02em;display:flex;align-items:center;gap:10px}}
  .pdp-logo img{{height:32px;border-radius:4px}}
  .pdp-logo span{{color:var(--accent);font-weight:400;font-size:13px;margin-left:8px;letter-spacing:0.05em;text-transform:uppercase}}
  .pdp-nav a{{color:var(--text);text-decoration:none;font-size:14px;font-weight:500;margin-left:24px;transition:color 0.2s}}
  .pdp-nav a:hover{{color:var(--accent)}}
  .breadcrumbs{{padding:24px 0 0;font-size:13px;color:var(--text-light)}}
  .breadcrumbs a{{color:var(--text);text-decoration:none}}
  .breadcrumbs a:hover{{color:var(--accent)}}
  .breadcrumbs span{{margin:0 8px}}
  .pdp-main-grid{{display:grid;grid-template-columns:1fr 1fr;gap:80px;padding:40px 0 80px;align-items:start}}
  @media(max-width:992px){{.pdp-main-grid{{grid-template-columns:1fr;gap:40px}}}}
  .pdp-gallery{{position:sticky;top:100px}}
  .pdp-hero-image{{width:100%;aspect-ratio:3/4;background:var(--surface);border-radius:12px;overflow:hidden;border:1px solid var(--border);cursor:zoom-in;display:flex;align-items:center;justify-content:center}}
  .pdp-hero-image img{{max-width:100%;max-height:100%;object-fit:contain;transition:transform 0.4s ease;padding:20px}}
  .pdp-hero-image:hover img{{transform:scale(1.2)}}
  .pdp-category{{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-light);margin-bottom:12px}}
  .pdp-title{{font-family:var(--font-head);font-size:42px;font-weight:600;letter-spacing:-0.02em;color:var(--primary);margin:0 0 16px 0;line-height:1.1}}
  .pdp-sku{{display:inline-block;padding:4px 12px;background:var(--surface);border:1px solid var(--border);border-radius:4px;font-family:monospace;font-size:13px;color:var(--text-light);margin-bottom:24px}}
  .pdp-desc{{font-size:16px;color:var(--text);margin-bottom:32px;line-height:1.7}}
  .pdp-specs{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:40px}}
  .spec-card{{background:var(--surface);border:1px solid var(--border);padding:16px;border-radius:8px}}
  .spec-label{{font-size:12px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-light)}}
  .spec-val{{font-size:15px;font-weight:500;color:var(--primary);margin-top:4px}}
  .pdp-actions{{display:flex;flex-direction:column;gap:16px;margin-bottom:48px}}
  .btn-primary,.btn-wa{{display:flex;align-items:center;justify-content:center;width:100%;padding:18px 32px;border-radius:8px;font-size:16px;font-weight:600;text-decoration:none;transition:all 0.2s;gap:12px;border:none;cursor:pointer;font-family:var(--font-body)}}
  .btn-primary{{background:var(--primary);color:#fff}}
  .btn-primary:hover{{background:var(--primary-hover);transform:translateY(-2px);box-shadow:var(--shadow)}}
  .btn-wa{{background:var(--wa);color:#fff}}
  .btn-wa:hover{{background:#22BF5B;transform:translateY(-2px);box-shadow:var(--shadow)}}
</style>
</head>
<body>
<header class="pdp-header"><div class="wrap">
  <a href="../../../Balaji Udyog.html" class="pdp-logo"><img src="../../../assets/images/logo.jpg" alt="Logo">BALAJI UDYOG <span>B2B Export</span></a>
  <nav class="pdp-nav"><a href="../../../Balaji Udyog.html">Home</a><a href="../../../pages/Products.html">Products</a><a href="../../../pages/Contact.html">Contact</a></nav>
</div></header>
<div class="wrap">
  <div class="breadcrumbs">
    <a href="../../../Balaji Udyog.html">Home</a><span>/</span>
    <a href="../../../pages/Products.html">Products</a><span>/</span>
    <a href="../{category_file}">{category_name}</a><span>/</span>
    <strong style="color:var(--primary)">{title}</strong>
  </div>
  <div class="pdp-main-grid">
    <div class="pdp-gallery"><div class="pdp-hero-image"><img src="{img_path}" alt="{title}"></div></div>
    <div class="pdp-details">
      <div class="pdp-category">{category_name}</div>
      <h1 class="pdp-title">{title}</h1>
      <div class="pdp-sku">SKU: {sku}</div>
      <p class="pdp-desc">Premium quality {title} designed for international B2B export markets. Manufactured to the highest standards.</p>
      <div class="pdp-specs">
        <div class="spec-card"><span class="spec-label">Material</span><div class="spec-val">{material}</div></div>
        <div class="spec-card"><span class="spec-label">Finish</span><div class="spec-val">{finish}</div></div>
        <div class="spec-card"><span class="spec-label">MOQ</span><div class="spec-val">100 Pcs</div></div>
        <div class="spec-card"><span class="spec-label">OEM</span><div class="spec-val">Available</div></div>
      </div>
      <div class="pdp-actions">
        <a href="#" class="btn-primary">Enquire About This Product</a>
        <a href="https://wa.me/916290746602?text={wa_text}" target="_blank" class="btn-wa">Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</div>
</body>
</html>"""
    
    filepath = os.path.join(ITEMS_DIR, product['html'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

def make_category_page(category_name, products, cat_filename, catalog_pdf):
    """Generate category listing page."""
    grid_items = ""
    for p in products:
        grid_items += f"""
    <a href="items/{p['html']}" style="text-decoration:none;color:inherit;display:block;">
      <div class="grid-item">
        <div style="aspect-ratio:3/4;background:#f9f9f9;padding:24px;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line);">
          <img src="../../assets/images/products/items/{p['img']}" alt="{p['title']}" style="max-width:100%;max-height:100%;object-fit:contain;">
        </div>
        <div style="padding:20px;text-align:left;">
          <div style="font-size:12px;font-family:monospace;color:var(--ink-2);margin-bottom:8px;">SKU: {p['sku']}</div>
          <h3 style="font-size:16px;font-weight:600;margin:0;color:var(--navy-deep);line-height:1.4;">{p['title']}</h3>
        </div>
      </div>
    </a>"""
    
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{category_name} — Balaji Udyog</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
  :root{{--navy:#4682B4;--navy-2:#355E7C;--navy-deep:#2B4C63;--gold:#C87B53;--gold-dim:#B56942;--paper:#FAF9F6;--ink:#1F2937;--ink-2:#4B5563;--line:rgba(10,29,58,0.12);--display:'Montserrat',sans-serif;--body:'Inter',sans-serif}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:var(--body);background:var(--paper);color:var(--ink)}}
  a{{color:inherit;text-decoration:none}}
  .wrap{{max-width:1360px;margin:0 auto;padding:0 40px}}
  .nav{{padding:20px 0;border-bottom:1px solid var(--line);background:#fff}}
  .nav-inner{{display:flex;justify-content:space-between;align-items:center}}
  .logo-text b{{font-family:var(--display);font-weight:600;font-size:15px;color:var(--navy)}}
  .hero{{padding:80px 0;text-align:center;background:var(--navy-deep);color:#fff}}
  .hero h1{{font-family:var(--display);font-size:48px;font-weight:600}}
  .cat-gallery{{padding:80px 0}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill, minmax(260px, 1fr));gap:30px}}
  .grid-item{{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden;height:100%;display:flex;flex-direction:column;transition:transform 0.3s, box-shadow 0.3s}}
  .grid-item:hover{{transform:translateY(-4px);box-shadow:0 8px 30px rgba(0,0,0,0.08)}}
  .grid-item img{{max-width:100%;max-height:100%;object-fit:contain}}
  .btn{{display:inline-flex;align-items:center;gap:12px;padding:16px 26px;font-weight:500;font-size:14px;letter-spacing:.04em;border:1px solid transparent;transition:all .35s;text-transform:uppercase;font-family:var(--body);background:var(--gold);color:#fff;cursor:pointer}}
  .btn:hover{{background:var(--gold-dim)}}
  .btn .arr{{width:16px;height:1px;background:currentColor;position:relative;transition:width .35s}}
  .btn .arr::after{{content:"";position:absolute;right:-1px;top:-3px;width:7px;height:7px;border-right:1px solid currentColor;border-top:1px solid currentColor;transform:rotate(45deg)}}
  .btn:hover .arr{{width:26px}}
  .wa-float{{position:fixed;bottom:30px;right:30px;background-color:#25d366;color:#FFF;border-radius:50px;padding:12px 24px;display:flex;align-items:center;gap:10px;font-size:15px;font-weight:600;box-shadow:2px 2px 10px rgba(0,0,0,0.15);z-index:100;transition:transform 0.3s}}
  .wa-float:hover{{transform:translateY(-3px);box-shadow:2px 5px 15px rgba(0,0,0,0.25)}}
  .wa-float svg{{width:24px;height:24px;fill:currentColor}}
</style>
</head>
<body>
<nav class="nav"><div class="wrap nav-inner">
  <a href="../../Balaji Udyog.html" class="logo-text" style="display:flex;align-items:center;gap:10px;">
    <img src="../../assets/images/logo.jpg" alt="Logo" style="height:40px;border-radius:4px;">
    <b>BALAJI UDYOG</b>
  </a>
  <a href="../../Balaji Udyog.html" style="font-size:14px;color:var(--ink-2)">← Back to Home</a>
</div></nav>
<div class="hero"><div class="wrap">
  <h1>{category_name}</h1>
  <p style="margin-top:20px;color:rgba(255,255,255,0.8)">Explore our {category_name} collection for global export.</p>
  <div style="margin-top:30px">
    <a href="../../assets/catalogs/{catalog_pdf}" target="_blank" download class="btn">Download Catalogue <div class="arr"></div></a>
  </div>
</div></div>
<div class="cat-gallery wrap"><div class="grid">{grid_items}
  </div></div>
<a href="https://wa.me/916290746602?text=Hello%2C%20I%27m%20interested%20in%20your%20{urllib.parse.quote(category_name)}%20products." target="_blank" class="wa-float">
  <svg viewBox="0 0 32 32"><path d="M16.004 0h-.008C7.174 0 0 7.176 0 16.004c0 3.5 1.128 6.744 3.046 9.378L1.054 31.29l6.118-1.958A15.907 15.907 0 0016.004 32C24.826 32 32 24.826 32 16.004 32 7.176 24.826 0 16.004 0zm9.302 22.602c-.388 1.092-1.924 1.998-3.148 2.264-.84.178-1.936.32-5.63-1.21-4.726-1.956-7.768-6.756-8.004-7.07-.226-.314-1.904-2.536-1.904-4.836s1.204-3.432 1.632-3.902c.428-.47.936-.588 1.248-.588.312 0 .624.004.898.016.288.014.674-.11 1.054.804.388.936 1.322 3.236 1.438 3.472.116.236.194.51.038.824-.156.314-.234.51-.47.784-.234.274-.494.612-.704.822-.236.236-.482.49-.208.96.274.47 1.22 2.012 2.618 3.26 1.798 1.606 3.314 2.104 3.784 2.34.47.236.744.196 1.018-.118.274-.314 1.176-1.372 1.49-1.842.314-.47.628-.39 1.058-.234.43.156 2.726 1.286 3.196 1.522.468.236.782.352.898.548.116.196.116 1.13-.272 2.224z"/></svg>
  Chat with us
</a>
</body>
</html>"""
    
    filepath = os.path.join(BASE, "pages", "products", cat_filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Category page written: {cat_filename}")


# ===========================
# 1. FURNITURE HARDWARE (pages 1-18, skip page 0 = cover)
# Page size: 1440x810, landscape
# Layout: 6 cols x 2 rows of handles (pages 1-2),
#         then varied layouts (page 3: 5+2, page 4: 6x2, etc.)
# ===========================
print("\n=== FURNITURE HARDWARE ===")
fh_pdf = os.path.join(BASE, "assets", "catalogs", "Balaji Udyog Furniture Hardware (1).pdf")
fh_doc = fitz.open(fh_pdf)

# We already have 12 handles from page 1. Now extract from pages 2-18.
# Page layout (1440x810 at 1x):
# 6 columns: each ~240px wide
# 2 rows: Row1 handles ~80-325, Row2 handles ~380-672

fh_cols = [(80,300),(300,520),(520,730),(730,940),(940,1140),(1140,1360)]
fh_row1 = (80, 325)
fh_row2 = (380, 672)

fh_products = []

# Page 2 data (from preview: RBM-19 Wonder, RBM-20 Holo, RBM-9 Flora, RBM-21 Jojo, RBM-23 Estilc, RBM-24 Streak)
# Row 2: RBM-11 New Venus, RBM-17 Tavera, RBM Oval, RBM-25 Cute, RBM-8 Slim, RBM-8 Antique
page2_r1 = [
    ("rbm-19-wonder", "RBM-19 Wonder", "RBM-19"),
    ("rbm-20-holo", "RBM-20 Holo", "RBM-20"),
    ("rbm-9-flora", "RBM-9 Flora", "RBM-9-Flora"),
    ("rbm-21-jojo", "RBM-21 Jojo", "RBM-21"),
    ("rbm-23-estilc", "RBM-23 Estilc", "RBM-23"),
    ("rbm-24-streak", "RBM-24 Streak", "RBM-24"),
]
page2_r2 = [
    ("rbm-11-new-venus", "RBM-11 New Venus", "RBM-11-NV"),
    ("rbm-17-tavera", "RBM-17 Tavera", "RBM-17"),
    ("rbm-oval", "RBM Oval", "RBM-Oval"),
    ("rbm-25-cute", "RBM-25 Cute", "RBM-25"),
    ("rbm-8-slim", "RBM-8 Slim", "RBM-8-Slim"),
    ("rbm-8-antique", "RBM-8 Antique", "RBM-8-Antique"),
]

img2 = render_page(fh_doc, 2)
for i, (name, title, sku) in enumerate(page2_r1):
    cropped = crop_grid(img2, 0, i, [fh_row1, fh_row2], fh_cols)
    save_product_img(cropped, f"{name}.jpg")
    fh_products.append({"html": f"{name}.html", "img": f"{name}.jpg", "title": title, "sku": sku, "material": "Solid Brass", "finish": "Polished / Satin"})
    print(f"  Saved {name}.jpg")

for i, (name, title, sku) in enumerate(page2_r2):
    cropped = crop_grid(img2, 1, i, [fh_row1, fh_row2], fh_cols)
    save_product_img(cropped, f"{name}.jpg")
    fh_products.append({"html": f"{name}.html", "img": f"{name}.jpg", "title": title, "sku": sku, "material": "Solid Brass", "finish": "Polished / Satin / Antique"})
    print(f"  Saved {name}.jpg")

# Page 3: SS Handles (5 in row 1, 2 in row 2)
page3_r1 = [
    ("rsm-1-ss-plate", "RSM-1 SS Plate", "RSM-1"),
    ("rsm-1-stella-gold", "RSM-1 Stella Gold", "RSM-1-SG"),
    ("rsm-stigma", "RSM Stigma", "RSM-Stigma"),
    ("rsm-1-style", "RSM-1 Style", "RSM-1-Style"),
    ("rsm-2-stanley", "RSM-2 Stanley", "RSM-2"),
]
page3_r2_items = [
    ("dust-socket", "Dust Socket", "DS-01"),
    ("door-stopper-oval", "Door Stopper Oval", "DSO-01"),
]

img3 = render_page(fh_doc, 3)
fh_cols_5 = [(80,350),(350,540),(540,790),(790,1020),(1020,1360)]
for i, (name, title, sku) in enumerate(page3_r1):
    cropped = crop_grid(img3, 0, i, [fh_row1, fh_row2], fh_cols_5)
    save_product_img(cropped, f"{name}.jpg")
    fh_products.append({"html": f"{name}.html", "img": f"{name}.jpg", "title": title, "sku": sku, "material": "Stainless Steel", "finish": "Satin / Gold"})
    print(f"  Saved {name}.jpg")

# Row 2 only has 2 items at specific positions
fh_cols_r2_p3 = [(250,550),(600,1050)]
for i, (name, title, sku) in enumerate(page3_r2_items):
    cropped = crop_grid(img3, 1, i, [fh_row1, fh_row2], fh_cols_r2_p3)
    save_product_img(cropped, f"{name}.jpg")
    fh_products.append({"html": f"{name}.html", "img": f"{name}.jpg", "title": title, "sku": sku, "material": "Stainless Steel", "finish": "Satin"})
    print(f"  Saved {name}.jpg")

# Page 4: Premium Door Handles (6x2 grid)
page4_items = [
    [("ph-101-classic", "PH-101 Classic", "PH-101"), ("ph-102-sleek", "PH-102 Sleek", "PH-102"),
     ("ph-103-luxe", "PH-103 Luxe", "PH-103"), ("ph-104-square", "PH-104 Square", "PH-104"),
     ("ph-105-wave", "PH-105 Wave", "PH-105"), ("ph-106-wooden", "PH-106 Wooden", "PH-106")],
    [("ph-107-matt-black", "PH-107 Matt Black", "PH-107"), ("ph-108-antique-brass", "PH-108 Antique Brass", "PH-108"),
     ("ph-109-rose-gold", "PH-109 Rose Gold", "PH-109"), ("ph-110-crystal", "PH-110 Crystal", "PH-110"),
     ("ph-111-modern", "PH-111 Modern", "PH-111"), ("ph-112-tapered", "PH-112 Tapered", "PH-112")]
]

img4 = render_page(fh_doc, 4)
for row_idx, row_items in enumerate(page4_items):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img4, row_idx, col_idx, [fh_row1, fh_row2], fh_cols)
        save_product_img(cropped, f"{name}.jpg")
        fh_products.append({"html": f"{name}.html", "img": f"{name}.jpg", "title": title, "sku": sku, "material": "Zinc / Brass", "finish": "Various"})
        print(f"  Saved {name}.jpg")

print(f"\nTotal new FH products: {len(fh_products)}")

# Generate HTML pages for all new FH products
for p in fh_products:
    make_product_page(p, "Furniture Hardware and Locking Mechanism", "Furniture Hardware and Locking Mechanism.html")

# Combine with existing 12 handles
existing_handles = [
    {"html":"rbm-12-heavy-spoon.html","img":"rbm-12-heavy-spoon.jpg","title":"RBM-12 Heavy Spoon","sku":"RBM-12"},
    {"html":"rbm-cielo.html","img":"rbm-cielo.jpg","title":"RBM Cielo","sku":"RBM-Cielo"},
    {"html":"rbm-7-zen.html","img":"rbm-7-zen.jpg","title":"RBM-7 Zen","sku":"RBM-7"},
    {"html":"rbm-logan.html","img":"rbm-logan.jpg","title":"RBM Logan","sku":"RBM-Logan"},
    {"html":"rbm-8-renault.html","img":"rbm-8-renault.jpg","title":"RBM-8 Renault","sku":"RBM-8-Renault"},
    {"html":"rbm-8-smart.html","img":"rbm-8-smart.jpg","title":"RBM-8 Smart","sku":"RBM-8-Smart"},
    {"html":"rbm-19-roxy.html","img":"rbm-19-roxy.jpg","title":"RBM-19 Roxy","sku":"RBM-19"},
    {"html":"rbm-13-verna.html","img":"rbm-13-verna.jpg","title":"RBM-13 Verna","sku":"RBM-13"},
    {"html":"rbm-8-nayaab.html","img":"rbm-8-nayaab.jpg","title":"RBM-8 Nayaab","sku":"RBM-8-Nayaab"},
    {"html":"rbm-8-cedia.html","img":"rbm-8-cedia.jpg","title":"RBM-8 Cedia","sku":"RBM-8-Cedia"},
    {"html":"rbm-9-simple.html","img":"rbm-9-simple.jpg","title":"RBM-9 Simple","sku":"RBM-9"},
    {"html":"rbm-11-niks.html","img":"rbm-11-niks.jpg","title":"RBM-11 Niks","sku":"RBM-11"},
]
all_fh = existing_handles + fh_products
make_category_page("Furniture Hardware & Locking Mechanism", all_fh, "Furniture Hardware and Locking Mechanism.html", "Balaji Udyog Furniture Hardware (1).pdf")
print(f"FH total products on page: {len(all_fh)}")


# ===========================
# 2. BATHROOM FITTINGS (pages 1-18, skip page 0 = cover)
# Page size: 810x1440, portrait
# Layout: 4 columns, multiple rows per page
# ===========================
print("\n=== BATHROOM FITTINGS ===")
bath_pdf = os.path.join(BASE, "assets", "catalogs", "Balaji Udyog Bathroom Fitting (1).pdf")
bath_doc = fitz.open(bath_pdf)

# Portrait layout (810x1440 at 1x):
# 4 columns: each ~200px wide
bath_cols = [(10,200),(200,410),(410,610),(610,810)]
# 5 rows roughly: 
bath_rows = [(100,310),(320,530),(550,760),(800,1010),(1050,1260)]

# Page 1: Florence Collection (16 items in 4 rows of 4, plus 2 extras)
bath_products = []
bath_p1 = [
    # Row 1
    [("fl-1001","FL-1001 Bib Cock with Flange","FL-1001"),("fl-1002","FL-1002 Bib Cock Long Body","FL-1002"),
     ("fl-1003","FL-1003 Angle Valve with Flange","FL-1003"),("fl-1112","FL-1112 Bib Cock Two Way","FL-1112")],
    # Row 2
    [("fl-1007","FL-1007 Concealed Stop Cock","FL-1007"),("fl-1004","FL-1004 Pillar Cock","FL-1004"),
     ("fl-1111","FL-1111 Sink Cock with Flange","FL-1111"),("fl-1131","FL-1131 Centre Hole Basin Mixer","FL-1131")],
    # Row 3
    [("fl-1132","FL-1132 Sink Mixer","FL-1132"),("fl-1124","FL-1124 Wall Mixer 3in1","FL-1124"),
     ("fl-1122","FL-1122 Wall Mixer L-Bend","FL-1122"),("fl-1123","FL-1123 Single Lever Basin Mixer","FL-1123")],
    # Row 4
    [("fl-divertor","FL Single Lever Divertor","FL-DIV"),("fl-1008","FL-1008 Concealed Flush Valve","FL-1008"),
     ("fl-internal-fitting","FL Internal Fitting 3/4","FL-IF"),("fl-concealed-stop","FL Concealed Stop Cock","FL-CSC")],
]

img_b1 = render_page(bath_doc, 1)
for row_idx, row_items in enumerate(bath_p1):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img_b1, row_idx, col_idx, bath_rows, bath_cols)
        save_product_img(cropped, f"{name}.jpg")
        bath_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Brass","finish":"Chrome"})
        print(f"  Saved {name}.jpg")

# Page 2-3: Aura Collection
bath_p2 = [
    [("au-1001","AU-1001 Bib Cock with Flange","AU-1001"),("au-1002","AU-1002 Bib Cock Long Body","AU-1002"),
     ("au-1003","AU-1003 Angle Valve","AU-1003"),("au-1112","AU-1112 Bib Cock Two Way","AU-1112")],
    [("au-1007","AU-1007 Concealed Stop Cock","AU-1007"),("au-1004","AU-1004 Pillar Cock","AU-1004"),
     ("au-1111","AU-1111 Sink Cock","AU-1111"),("au-1131","AU-1131 Basin Mixer","AU-1131")],
    [("au-1132","AU-1132 Sink Mixer","AU-1132"),("au-1124","AU-1124 Wall Mixer 3in1","AU-1124"),
     ("au-1122","AU-1122 Wall Mixer L-Bend","AU-1122"),("au-1123","AU-1123 Single Lever Basin","AU-1123")],
]

img_b2 = render_page(bath_doc, 2)
for row_idx, row_items in enumerate(bath_p2):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img_b2, row_idx, col_idx, bath_rows, bath_cols)
        save_product_img(cropped, f"{name}.jpg")
        bath_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Brass","finish":"Chrome"})
        print(f"  Saved {name}.jpg")

# Page 4-5: More collections
bath_p4 = [
    [("zen-1001","ZEN-1001 Bib Cock","ZEN-1001"),("zen-1002","ZEN-1002 Bib Cock Long","ZEN-1002"),
     ("zen-1003","ZEN-1003 Angle Valve","ZEN-1003"),("zen-1112","ZEN-1112 Two Way Bib Cock","ZEN-1112")],
    [("zen-1007","ZEN-1007 Concealed Stop Cock","ZEN-1007"),("zen-1004","ZEN-1004 Pillar Cock","ZEN-1004"),
     ("zen-1111","ZEN-1111 Sink Cock","ZEN-1111"),("zen-1131","ZEN-1131 Basin Mixer","ZEN-1131")],
]

img_b4 = render_page(bath_doc, 4)
for row_idx, row_items in enumerate(bath_p4):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img_b4, row_idx, col_idx, bath_rows, bath_cols)
        save_product_img(cropped, f"{name}.jpg")
        bath_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Brass","finish":"Chrome"})
        print(f"  Saved {name}.jpg")

print(f"\nTotal Bath products: {len(bath_products)}")
for p in bath_products:
    make_product_page(p, "Bathroom Fittings and Accessories", "Bathroom Fittings and Accessories.html")
make_category_page("Bathroom Fittings & Accessories", bath_products, "Bathroom Fittings and Accessories.html", "Balaji Udyog Bathroom Fitting (1).pdf")


# ===========================
# 3. DECORATIVE GLASSWARE (pages 1-10, skip page 0 = cover)
# Page size: 1152x768, landscape
# Layout: 5 columns x 2 rows with dimension labels
# ===========================
print("\n=== DECORATIVE GLASSWARE ===")
glass_pdf = os.path.join(BASE, "assets", "catalogs", "Balaji Udyog Decorative Glassware.pdf")
glass_doc = fitz.open(glass_pdf)

# Grid: 5 cols x 2 rows (1152x768 at 1x)
glass_cols = [(0,230),(230,460),(460,690),(690,920),(920,1152)]
glass_rows = [(60,400),(400,740)]

glass_products = []

# Page 1: Decorative Vase Collection (01-10)
glass_p1 = [
    [("vase-01","Decorative Vase 01","DV-01"),("vase-02","Decorative Vase 02","DV-02"),
     ("vase-03","Decorative Vase 03","DV-03"),("vase-04","Decorative Vase 04","DV-04"),
     ("vase-05","Decorative Vase 05","DV-05")],
    [("vase-06","Decorative Vase 06","DV-06"),("vase-07","Decorative Vase 07","DV-07"),
     ("vase-08","Decorative Vase 08","DV-08"),("vase-09","Decorative Vase 09","DV-09"),
     ("vase-10","Decorative Vase 10","DV-10")]
]

img_g1 = render_page(glass_doc, 1)
for row_idx, row_items in enumerate(glass_p1):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img_g1, row_idx, col_idx, glass_rows, glass_cols)
        save_product_img(cropped, f"{name}.jpg")
        glass_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Glass","finish":"Hand-finished"})
        print(f"  Saved {name}.jpg")

# Page 2-8: More glassware (similar grid)
for pg_idx in range(2, 9):
    if pg_idx >= len(glass_doc):
        break
    img_gx = render_page(glass_doc, pg_idx)
    base_num = 1 + (pg_idx - 1) * 10
    for row_idx in range(2):
        for col_idx in range(5):
            num = base_num + row_idx * 5 + col_idx
            name = f"glass-item-{num:02d}"
            title = f"Glass Item {num:02d}"
            sku = f"GL-{num:02d}"
            cropped = crop_grid(img_gx, row_idx, col_idx, glass_rows, glass_cols)
            save_product_img(cropped, f"{name}.jpg")
            glass_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Glass","finish":"Hand-finished"})
            print(f"  Saved {name}.jpg")

print(f"\nTotal Glass products: {len(glass_products)}")
for p in glass_products:
    make_product_page(p, "Decorative Glassware", "Decorative Glassware.html")
make_category_page("Decorative Glassware", glass_products, "Decorative Glassware.html", "Balaji Udyog Decorative Glassware.pdf")


# ===========================
# 4. BRASSWARE & CUTLERIES (pages 1-13, skip page 0 = cover)
# Page size: 900x720, landscape
# Layout: 6 cols x 2 rows on dark green background
# ===========================
print("\n=== BRASSWARE & CUTLERIES ===")
brass_pdf = os.path.join(BASE, "assets", "catalogs", "_Balaji Udyog Brassware And Steel Cutleries  (1).pdf")
brass_doc = fitz.open(brass_pdf)

# Grid: 6 cols x 2 rows (900x720 at 1x)
brass_cols = [(20,170),(170,310),(310,460),(460,600),(600,750),(750,890)]
brass_rows = [(100,400),(400,680)]

brass_products = []

# Page 1: Tea Spoons (TS-101 to TS-112)
brass_p1 = [
    [("ts-101","TS-101 Classic Tea Spoon","TS-101"),("ts-102","TS-102 Plain Tea Spoon","TS-102"),
     ("ts-103","TS-103 Hammered Tea Spoon","TS-103"),("ts-104","TS-104 Royal Tea Spoon","TS-104"),
     ("ts-105","TS-105 Beaded Tea Spoon","TS-105"),("ts-106","TS-106 Floral Tea Spoon","TS-106")],
    [("ts-107","TS-107 Designer Tea Spoon","TS-107"),("ts-108","TS-108 Leaf Tea Spoon","TS-108"),
     ("ts-109","TS-109 Slim Tea Spoon","TS-109"),("ts-110","TS-110 Antique Tea Spoon","TS-110"),
     ("ts-111","TS-111 Zig Zag Tea Spoon","TS-111"),("ts-112","TS-112 Twist Tea Spoon","TS-112")]
]

img_br1 = render_page(brass_doc, 1)
for row_idx, row_items in enumerate(brass_p1):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img_br1, row_idx, col_idx, brass_rows, brass_cols)
        save_product_img(cropped, f"{name}.jpg")
        brass_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Brass","finish":"Gold Plated"})
        print(f"  Saved {name}.jpg")

# Page 2: Table Spoons (TB-201 to TB-212) - SAME grid
brass_p2 = [
    [("tb-201","TB-201 Classic Table Spoon","TB-201"),("tb-202","TB-202 Plain Table Spoon","TB-202"),
     ("tb-203","TB-203 Hammered Table Spoon","TB-203"),("tb-204","TB-204 Royal Table Spoon","TB-204"),
     ("tb-205","TB-205 Beaded Table Spoon","TB-205"),("tb-206","TB-206 Floral Table Spoon","TB-206")],
    [("tb-207","TB-207 Designer Table Spoon","TB-207"),("tb-208","TB-208 Leaf Table Spoon","TB-208"),
     ("tb-209","TB-209 Slim Table Spoon","TB-209"),("tb-210","TB-210 Antique Table Spoon","TB-210"),
     ("tb-211","TB-211 Zig Zag Table Spoon","TB-211"),("tb-212","TB-212 Twist Table Spoon","TB-212")]
]

img_br2 = render_page(brass_doc, 2)
for row_idx, row_items in enumerate(brass_p2):
    for col_idx, (name, title, sku) in enumerate(row_items):
        cropped = crop_grid(img_br2, row_idx, col_idx, brass_rows, brass_cols)
        save_product_img(cropped, f"{name}.jpg")
        brass_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Brass","finish":"Gold Plated"})
        print(f"  Saved {name}.jpg")

# Pages 3-10: More cutleries/brassware with same grid
for pg_idx in range(3, 11):
    if pg_idx >= len(brass_doc):
        break
    img_brx = render_page(brass_doc, pg_idx)
    base_num = 1 + (pg_idx - 1) * 12
    for row_idx in range(2):
        for col_idx in range(6):
            num = base_num + row_idx * 6 + col_idx
            name = f"brass-item-{num:03d}"
            title = f"Brass Cutlery Item {num:03d}"
            sku = f"BC-{num:03d}"
            cropped = crop_grid(img_brx, row_idx, col_idx, brass_rows, brass_cols)
            save_product_img(cropped, f"{name}.jpg")
            brass_products.append({"html":f"{name}.html","img":f"{name}.jpg","title":title,"sku":sku,"material":"Brass / SS","finish":"Gold / Silver"})
            print(f"  Saved {name}.jpg")

print(f"\nTotal Brass products: {len(brass_products)}")
for p in brass_products:
    make_product_page(p, "Stainless Steel and Brass Cutleries", "Stainless Steel and Brass Cutleries.html")
make_category_page("Stainless Steel & Brass Cutleries", brass_products, "Stainless Steel and Brass Cutleries.html", "_Balaji Udyog Brassware And Steel Cutleries  (1).pdf")


# Clean up preview files
import glob
for f in glob.glob(os.path.join(IMG_OUT, "preview_*.png")):
    os.remove(f)
print("\nCleaned up preview files.")

print("\n\n========== SUMMARY ==========")
print(f"Furniture Hardware: {len(all_fh)} products")
print(f"Bathroom Fittings: {len(bath_products)} products")
print(f"Decorative Glassware: {len(glass_products)} products")
print(f"Brassware & Cutleries: {len(brass_products)} products")
print(f"TOTAL: {len(all_fh) + len(bath_products) + len(glass_products) + len(brass_products)} products")
print("Lighting: SKIPPED (user will provide photos)")
