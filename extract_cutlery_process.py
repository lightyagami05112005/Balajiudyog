import fitz
import os
import urllib.parse
from PIL import Image
import io

BASE = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
IMG_OUT = os.path.join(BASE, "assets", "images", "products", "items")
ITEMS_DIR = os.path.join(BASE, "pages", "products", "items")
CAT_PAGE = os.path.join(BASE, "pages", "products", "Stainless Steel and Brass Cutleries.html")

pdf_path = r'c:\Users\Shubham\Downloads\Balaji Udyog cutleries  process .pdf'
doc = fitz.open(pdf_path)

# Detailed mapping of the 60 pages of the cutleries process PDF
CUTLERY_PRODUCTS = []

# 12 Tea Spoons (Pages 0–11)
tea_spoons = [
    ("ts-101", "TS-101 Classic Tea Spoon", "TS-101"),
    ("ts-102", "TS-102 Plain Tea Spoon", "TS-102"),
    ("ts-103", "TS-103 Hammered Tea Spoon", "TS-103"),
    ("ts-104", "TS-104 Royal Tea Spoon", "TS-104"),
    ("ts-105", "TS-105 Beaded Tea Spoon", "TS-105"),
    ("ts-106", "TS-106 Floral Tea Spoon", "TS-106"),
    ("ts-107", "TS-107 Designer Tea Spoon", "TS-107"),
    ("ts-108", "TS-108 Leaf Tea Spoon", "TS-108"),
    ("ts-109", "TS-109 Slim Tea Spoon", "TS-109"),
    ("ts-110", "TS-110 Antique Tea Spoon", "TS-110"),
    ("ts-111", "TS-111 Zig Zag Tea Spoon", "TS-111"),
    ("ts-112", "TS-112 Twist Tea Spoon", "TS-112")
]

for name, title, sku in tea_spoons:
    CUTLERY_PRODUCTS.append({
        "name": name,
        "title": title,
        "sku": sku,
        "material": "Stainless Steel & Brass",
        "finish": "Mirror / Gold Polish"
    })

# 12 Table Spoons (Pages 12–23)
table_spoons = [
    ("tb-201", "TB-201 Classic Table Spoon", "TB-201"),
    ("tb-202", "TB-202 Plain Table Spoon", "TB-202"),
    ("tb-203", "TB-203 Hammered Table Spoon", "TB-203"),
    ("tb-204", "TB-204 Royal Table Spoon", "TB-204"),
    ("tb-205", "TB-205 Beaded Table Spoon", "TB-205"),
    ("tb-206", "TB-206 Floral Table Spoon", "TB-206"),
    ("tb-207", "TB-207 Designer Table Spoon", "TB-207"),
    ("tb-208", "TB-208 Leaf Table Spoon", "TB-208"),
    ("tb-209", "TB-209 Slim Table Spoon", "TB-209"),
    ("tb-210", "TB-210 Antique Table Spoon", "TB-210"),
    ("tb-211", "TB-211 Zig Zag Table Spoon", "TB-211"),
    ("tb-212", "TB-212 Twist Table Spoon", "TB-212")
]

for name, title, sku in table_spoons:
    CUTLERY_PRODUCTS.append({
        "name": name,
        "title": title,
        "sku": sku,
        "material": "Stainless Steel & Brass",
        "finish": "Mirror / Gold Polish"
    })

# 36 Brassware cutlery items (Pages 24–59)
for num in range(25, 61):
    CUTLERY_PRODUCTS.append({
        "name": f"brass-item-{num:03d}",
        "title": f"Brass Cutlery Item {num:03d}",
        "sku": f"BC-{num:03d}",
        "material": "Solid Brass",
        "finish": "Gold Plated"
    })

def make_product_page(product, category_name, category_file):
    title = product['title']
    sku = product['sku']
    img_file = product['img']
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {title} ({sku}).")
    img_path = f"../../../assets/images/products/items/{img_file}"
    material = product.get('material', 'Stainless Steel & Brass')
    finish = product.get('finish', 'Mirror / Gold Polish')
    
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
  .pdp-hero-image{{width:100%;aspect-ratio:16/9;background:var(--surface);border-radius:12px;overflow:hidden;border:1px solid var(--border);cursor:zoom-in;display:flex;align-items:center;justify-content:center}}
  .pdp-hero-image img{{max-width:100%;max-height:100%;object-fit:cover;transition:transform 0.4s ease;}}
  .pdp-hero-image:hover img{{transform:scale(1.1)}}
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
<script src="../../../assets/inquiry-modal.js" defer></script>
</body>
</html>"""
    
    filepath = os.path.join(ITEMS_DIR, product['html'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

html_items_to_inject = []

print(f"Total pages in PDF: {len(doc)}")

for i in range(len(doc)):
    page = doc[i]
    
    # Render PDF page to 16:9 widescreen uncropped image
    pix = page.get_pixmap(matrix=fitz.Matrix(1.33333333, 1.33333333))
    img = Image.open(io.BytesIO(pix.tobytes()))
    
    prod_data = CUTLERY_PRODUCTS[i]
    title = prod_data["title"]
    sku = prod_data["sku"]
    slug = prod_data["name"]
    name = f"cutlery-{slug}-16x9"
    
    img_filename = f"{name}.jpg"
    html_filename = f"{name}.html"
    
    # Save image
    img = img.convert("RGB")
    img.save(os.path.join(IMG_OUT, img_filename), quality=95)
    
    # Make product page
    product_data = {
        "html": html_filename,
        "img": img_filename,
        "title": title,
        "sku": sku,
        "material": prod_data["material"],
        "finish": prod_data["finish"]
    }
    make_product_page(product_data, "Stainless Steel & Brass Cutleries", "Stainless Steel and Brass Cutleries.html")
    
    # Add to grid items (USING aspect-ratio: 16/9, object-fit: cover for widescreen uncropped photos)
    html_items_to_inject.append(f"""
    <a href="items/{html_filename}" style="text-decoration:none;color:inherit;display:block;">
      <div class="grid-item">
        <div style="aspect-ratio:16/9;background:#f9f9f9;padding:0;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line);overflow:hidden;">
          <img src="../../assets/images/products/items/{img_filename}" alt="{title}" style="width:100%;height:100%;object-fit:cover;">
        </div>
        <div style="padding:20px;text-align:left;">
          <div style="font-size:12px;font-family:monospace;color:var(--ink-2);margin-bottom:8px;">SKU: {sku}</div>
          <h3 style="font-size:16px;font-weight:600;margin:0;color:var(--navy-deep);line-height:1.4;">{title}</h3>
        </div>
      </div>
    </a>""")

    print(f"Processed page {i}: {title}")

# Replace the grid in Stainless Steel and Brass Cutleries.html
with open(CAT_PAGE, 'r', encoding='utf-8') as f:
    cat_html = f.read()

grid_start_marker = '<div class="cat-gallery wrap"><div class="grid">'
grid_end_marker = '  </div></div>\n<a href="https://wa.me/916290746602?text=Hello%2C%20I%27m%20interested%20in%20your%20Stainless%20Steel%20%26%20Brass%20Cutleries%20products."'

try:
    start_idx = cat_html.index(grid_start_marker) + len(grid_start_marker)
    end_idx = cat_html.index(grid_end_marker)
    
    new_grid_content = "".join(html_items_to_inject)
    cat_html = cat_html[:start_idx] + new_grid_content + "\n" + cat_html[end_idx:]
    
    with open(CAT_PAGE, 'w', encoding='utf-8') as f:
        f.write(cat_html)
        
    print("Successfully replaced the grid in Stainless Steel and Brass Cutleries.html with 60 new 16:9 product cards.")
except Exception as e:
    print(f"Failed to automatically replace the grid: {e}")
