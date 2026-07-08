import fitz
import os
import urllib.parse
from PIL import Image
import io

BASE = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
IMG_OUT = os.path.join(BASE, "assets", "images", "products", "items")
ITEMS_DIR = os.path.join(BASE, "pages", "products", "items")
CAT_PAGE = os.path.join(BASE, "pages", "products", "Furniture Hardware and Locking Mechanism.html")

pdf_path = r'c:\Users\Shubham\Downloads\Balaji Udyog Furniture Hardware process .pdf'
doc = fitz.open(pdf_path)

# Detailed mapping of the 55 pages to the first 5 pages of catalog
CATALOG_PRODUCTS = [
    # Page 1 of catalog
    {"name": "rbm-12-heavy-spoon", "title": "RBM-12 Heavy Spoon", "sku": "RBM-12", "material": "Solid Brass", "finish": "Antique / Satin"},
    {"name": "rbm-cielo", "title": "RBM Cielo", "sku": "RBM-Cielo", "material": "Solid Brass", "finish": "Polished Brass / Satin Chrome"},
    {"name": "rbm-7-zen", "title": "RBM-7 Zen", "sku": "RBM-7", "material": "Solid Brass", "finish": "Satin Gold / Chrome"},
    {"name": "rbm-logan", "title": "RBM Logan", "sku": "RBM-Logan", "material": "Solid Brass", "finish": "Antique Brass"},
    {"name": "rbm-8-renault", "title": "RBM-8 Renault", "sku": "RBM-8-Renault", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-8-smart", "title": "RBM-8 Smart", "sku": "RBM-8-Smart", "material": "Solid Brass", "finish": "Satin Brass"},
    {"name": "rbm-19-roxy", "title": "RBM-19 Roxy", "sku": "RBM-19", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-13-verna", "title": "RBM-13 Verna", "sku": "RBM-13", "material": "Solid Brass", "finish": "Antique Copper / Gold"},
    {"name": "rbm-8-nayaab", "title": "RBM-8 Nayaab", "sku": "RBM-8-Nayaab", "material": "Solid Brass", "finish": "Satin Gold"},
    {"name": "rbm-8-cedia", "title": "RBM-8 Cedia", "sku": "RBM-8-Cedia", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-9-simple", "title": "RBM-9 Simple", "sku": "RBM-9", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-11-niks", "title": "RBM-11 Niks", "sku": "RBM-11", "material": "Solid Brass", "finish": "Satin Gold"},
    # Page 2 of catalog
    {"name": "rbm-19-wonder", "title": "RBM-19 Wonder", "sku": "RBM-19-Wonder", "material": "Solid Brass", "finish": "Antique Brass"},
    {"name": "rbm-11-new-venus", "title": "RBM-11 New Venus", "sku": "RBM-11-NV", "material": "Solid Brass", "finish": "Satin Gold"},
    {"name": "rbm-20-holo", "title": "RBM-20 Holo", "sku": "RBM-20", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-9-flora", "title": "RBM-9 Flora", "sku": "RBM-9-Flora", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-21-jojo", "title": "RBM-21 Jojo", "sku": "RBM-21", "material": "Solid Brass", "finish": "Satin Gold"},
    {"name": "rbm-23-estilc", "title": "RBM-23 Estilc", "sku": "RBM-23", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-24-streak", "title": "RBM-24 Streak", "sku": "RBM-24", "material": "Solid Brass", "finish": "Satin Gold"},
    {"name": "rbm-17-tavera", "title": "RBM-17 Tavera", "sku": "RBM-17", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-oval", "title": "RBM Oval", "sku": "RBM-Oval", "material": "Solid Brass", "finish": "Satin Gold"},
    {"name": "rbm-25-cute", "title": "RBM-25 Cute", "sku": "RBM-25", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-8-slim", "title": "RBM-8 Slim", "sku": "RBM-8-Slim", "material": "Solid Brass", "finish": "Satin Chrome"},
    {"name": "rbm-8-antique", "title": "RBM-8 Antique", "sku": "RBM-8-Antique", "material": "Solid Brass", "finish": "Antique Brass"},
    # Page 3 of catalog
    {"name": "rsm-1-ss-plate", "title": "RSM-1 SS Plate", "sku": "RSM-1", "material": "Stainless Steel", "finish": "Satin Finish"},
    {"name": "rsm-1-stella-gold", "title": "RSM-1 Stella Gold", "sku": "RSM-1-SG", "material": "Stainless Steel", "finish": "Gold Plated"},
    {"name": "rsm-stigma", "title": "RSM Stigma", "sku": "RSM-Stigma", "material": "Stainless Steel", "finish": "Satin Finish"},
    {"name": "rsm-1-style", "title": "RSM-1 Style", "sku": "RSM-1-Style", "material": "Stainless Steel", "finish": "Satin / Gold"},
    {"name": "rsm-2-stanley", "title": "RSM-2 Stanley", "sku": "RSM-2", "material": "Stainless Steel", "finish": "Satin Finish"},
    {"name": "dust-socket", "title": "Dust Socket", "sku": "DS-01", "material": "Brass / Steel", "finish": "Satin / Polished"},
    {"name": "door-stopper-oval", "title": "Door Stopper Oval", "sku": "DSO-01", "material": "Brass / Steel", "finish": "Satin / Polished"},
    # Page 4 of catalog
    {"name": "ph-101-classic", "title": "PH-101 Classic", "sku": "PH-101", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "ph-102-sleek", "title": "PH-102 Sleek", "sku": "PH-102", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "ph-103-luxe", "title": "PH-103 Luxe", "sku": "PH-103", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "ph-104-square", "title": "PH-104 Square", "sku": "PH-104", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "ph-105-wave", "title": "PH-105 Wave", "sku": "PH-105", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "ph-106-wooden", "title": "PH-106 Wooden", "sku": "PH-106", "material": "Zinc / Brass / Wood", "finish": "Satin / Wood"},
    {"name": "ph-107-matt-black", "title": "PH-107 Matt Black", "sku": "PH-107", "material": "Zinc / Brass", "finish": "Matt Black"},
    {"name": "ph-108-antique-brass", "title": "PH-108 Antique Brass", "sku": "PH-108", "material": "Zinc / Brass", "finish": "Antique Brass"},
    {"name": "ph-109-rose-gold", "title": "PH-109 Rose Gold", "sku": "PH-109", "material": "Zinc / Brass", "finish": "Rose Gold"},
    {"name": "ph-110-crystal", "title": "PH-110 Crystal", "sku": "PH-110", "material": "Zinc / Brass / Crystal", "finish": "Satin / Crystal"},
    {"name": "ph-111-modern", "title": "PH-111 Modern", "sku": "PH-111", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "ph-112-tapered", "title": "PH-112 Tapered", "sku": "PH-112", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    # Page 5 of catalog
    {"name": "dh-201-classic", "title": "DH-201 Classic", "sku": "DH-201", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-202-arc", "title": "DH-202 Arc", "sku": "DH-202", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-203-elite", "title": "DH-203 Elite", "sku": "DH-203", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-204-luxe", "title": "DH-204 Luxe", "sku": "DH-204", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-205-square", "title": "DH-205 Square", "sku": "DH-205", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-206-wave", "title": "DH-206 Wave", "sku": "DH-206", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-207-wooden", "title": "DH-207 Wooden", "sku": "DH-207", "material": "Zinc / Brass / Wood", "finish": "Satin / Wood"},
    {"name": "dh-208-matt-black", "title": "DH-208 Matt Black", "sku": "DH-208", "material": "Zinc / Brass", "finish": "Matt Black"},
    {"name": "dh-209-ribbed", "title": "DH-209 Ribbed", "sku": "DH-209", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-210-crystal", "title": "DH-210 Crystal", "sku": "DH-210", "material": "Zinc / Brass / Crystal", "finish": "Satin / Crystal"},
    {"name": "dh-211-modern", "title": "DH-211 Modern", "sku": "DH-211", "material": "Zinc / Brass", "finish": "Satin Chrome"},
    {"name": "dh-212-tapered", "title": "DH-212 Tapered", "sku": "DH-212", "material": "Zinc / Brass", "finish": "Satin Chrome"},
]

def make_product_page(product, category_name, category_file):
    title = product['title']
    sku = product['sku']
    img_file = product['img']
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {title} ({sku}).")
    img_path = f"../../../assets/images/products/items/{img_file}"
    material = product.get('material', 'Solid Brass')
    finish = product.get('finish', 'Premium')
    
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

for i in range(len(doc)):
    page = doc[i]
    
    # Render PDF page to 16:9 widescreen
    pix = page.get_pixmap(matrix=fitz.Matrix(1.33333333, 1.33333333))
    img = Image.open(io.BytesIO(pix.tobytes()))
    
    prod_data = CATALOG_PRODUCTS[i]
    title = prod_data["title"]
    sku = prod_data["sku"]
    # slug name
    slug = prod_data["name"]
    name = f"{slug}-16x9"
    
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
    make_product_page(product_data, "Furniture Hardware and Locking Mechanism", "Furniture Hardware and Locking Mechanism.html")
    
    # Add to grid items (USING aspect-ratio: 16/9)
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

    print(f"Processed {title}")

# Read category page
with open(CAT_PAGE, 'r', encoding='utf-8') as f:
    cat_html = f.read()

# Inject before </div></div>
# The ending looks like:
#   </div></div>
# <a href="https://wa.me/916290746602...

injection_str = "".join(html_items_to_inject)
cat_html = cat_html.replace('  </div></div>\n<a href="https://wa.me', injection_str + '\n  </div></div>\n<a href="https://wa.me')

with open(CAT_PAGE, 'w', encoding='utf-8') as f:
    f.write(cat_html)

print(f"Injected {len(html_items_to_inject)} mapped 16:9 products into category page.")
