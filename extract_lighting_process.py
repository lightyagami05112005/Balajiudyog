import fitz
import os
import urllib.parse
from PIL import Image
import io
from bs4 import BeautifulSoup

BASE = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
IMG_OUT = os.path.join(BASE, "assets", "images", "products", "items")
ITEMS_DIR = os.path.join(BASE, "pages", "products", "items")
CAT_PAGE = os.path.join(BASE, "pages", "products", "Lighting.html")

os.makedirs(IMG_OUT, exist_ok=True)
os.makedirs(ITEMS_DIR, exist_ok=True)

pdf_path = r'c:\Users\Shubham\Downloads\Balaji Udyog Lighting process .pdf'
doc = fitz.open(pdf_path)

LIGHTING_PRODUCTS = [
    {"sku": "LT-001", "name": "lt-001", "title": "LT-001 Amber Glass Candle Chandelier", "material": "Glass & Brass", "finish": "Antique Gold"},
    {"sku": "LT-002", "name": "lt-002", "title": "LT-002 Ribbed Amber Glass Chandelier", "material": "Glass & Brass", "finish": "Polished Gold"},
    {"sku": "LT-003", "name": "lt-003", "title": "LT-003 Grand Multi-Tiered Crystal Chandelier", "material": "Premium Crystal & Brass", "finish": "Rich Gold"},
    {"sku": "LT-004", "name": "lt-004", "title": "LT-004 Grand Silver Crystal Chandelier", "material": "Premium Crystal & Brass", "finish": "Chrome Finish"},
    {"sku": "LT-005", "name": "lt-005", "title": "LT-005 Bell-Shaped Crystal Cascade Chandelier", "material": "Premium Crystal & Brass", "finish": "Chrome Finish"},
    {"sku": "LT-006", "name": "lt-006", "title": "LT-006 Classic Bronze Candelabra Chandelier", "material": "Premium Crystal & Iron", "finish": "Antique Bronze"},
    {"sku": "LT-007", "name": "lt-007", "title": "LT-007 Modern Crown Amber Glass Chandelier", "material": "Glass & Brass", "finish": "Polished Gold"},
    {"sku": "LT-008", "name": "lt-008", "title": "LT-008 Ornate Linear Brass Chandelier", "material": "Premium Crystal & Brass", "finish": "Rich Gold"},
    {"sku": "LT-009", "name": "lt-009", "title": "LT-009 Amber Glass Table Lamp Set", "material": "Glass, Brass & Fabric", "finish": "Amber Gold"},
    {"sku": "LT-010", "name": "lt-010", "title": "LT-010 Grand Crystal Candelabra Floor Lamp", "material": "Premium Crystal & Brass", "finish": "Rich Gold"},
    {"sku": "LT-011", "name": "lt-011", "title": "LT-011 Curved Glass Twin Wall Sconce", "material": "Premium Crystal & Glass", "finish": "Gold Finish"},
    {"sku": "LT-012", "name": "lt-012", "title": "LT-012 Classic Triple-Light Crystal Sconce", "material": "Premium Crystal & Glass", "finish": "Chrome Finish"},
    {"sku": "LT-013", "name": "lt-013", "title": "LT-013 Cylindrical Shade Crystal Wall Sconce", "material": "Glass, Brass & Fabric", "finish": "Gold Finish"},
    {"sku": "LT-014", "name": "lt-014", "title": "LT-014 Elegant Crystal Candelabra Table Lamp", "material": "Premium Crystal & Brass", "finish": "Gold Finish"},
    {"sku": "LT-015", "name": "lt-015", "title": "LT-015 Antique Filigree Brass Wall Sconce", "material": "Premium Crystal & Brass", "finish": "Rich Brass"},
    {"sku": "LT-016", "name": "lt-016", "title": "LT-016 Elegant Pleated Sconce with Black Tassel", "material": "Glass, Brass & Fabric", "finish": "Gold Finish"},
    {"sku": "LT-017", "name": "lt-017", "title": "LT-017 Urn Glass Table Lamp with Woven Shade", "material": "Glass, Brass & Fabric", "finish": "Amber Gold"},
    {"sku": "LT-018", "name": "lt-018", "title": "LT-018 Ribbed Amber Glass Table Lamp", "material": "Glass, Brass & Fabric", "finish": "Amber Gold"},
    {"sku": "LT-019", "name": "lt-019", "title": "LT-019 Faceted Crystal Drum Table Lamp", "material": "Premium Crystal & Fabric", "finish": "Gold Finish"},
    {"sku": "LT-020", "name": "lt-020", "title": "LT-020 Modern Frosted Tulip Petal Chandelier", "material": "Glass & Brass", "finish": "Gold Finish"},
    {"sku": "LT-021", "name": "lt-021", "title": "LT-021 Art-Deco Glass Accent Pendant Light", "material": "Glass, Brass & Fabric", "finish": "Gold Finish"},
    {"sku": "LT-022", "name": "lt-022", "title": "LT-022 Grand White Shade Crystal Chandelier", "material": "Premium Crystal, Brass & Fabric", "finish": "Chrome Finish"},
]

def make_product_page(product, category_name, category_file):
    title = product['title']
    sku = product['sku']
    img_file = product['img']
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {title} ({sku}).")
    img_path = f"../../../assets/images/products/items/{img_file}"
    material = product.get('material', 'Premium Crystal & Brass')
    finish = product.get('finish', 'Polished Gold')
    
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
        <div class="spec-card"><span class="spec-label">MOQ</span><div class="spec-val">10 Pcs</div></div>
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
    
    # Render PDF page to 16:9 widescreen image (Matrix zoom is 1.33333333 for 1440x810 to render at high quality)
    pix = page.get_pixmap(matrix=fitz.Matrix(1.33333333, 1.33333333))
    img = Image.open(io.BytesIO(pix.tobytes()))
    
    prod_data = LIGHTING_PRODUCTS[i]
    title = prod_data["title"]
    sku = prod_data["sku"]
    slug = prod_data["name"]
    name = f"lighting-{slug}-16x9"
    
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
    make_product_page(product_data, "Lighting", "Lighting.html")
    
    # Add to grid items
    html_items_to_inject.append(f"""
    <a href="items/{html_filename}" style="text-decoration:none;color:inherit;display:block;">
      <div class="grid-item" style="border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; height: 100%; display: flex; flex-direction: column;">
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

# Replace the grid in Lighting.html using BeautifulSoup
with open(CAT_PAGE, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

grid_div = soup.find('div', class_='grid')
if grid_div:
    grid_div.clear()
    for item_html in html_items_to_inject:
        card_soup = BeautifulSoup(item_html, 'html.parser')
        grid_div.append(card_soup)
    
    # Save Lighting.html back
    with open(CAT_PAGE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Successfully updated the grid in Lighting.html using BeautifulSoup.")
else:
    print("Error: Could not find <div class='grid'> in Lighting.html.")
