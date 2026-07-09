import fitz
import os
import urllib.parse
from PIL import Image
import io

BASE = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
IMG_OUT = os.path.join(BASE, "assets", "images", "products", "items")
ITEMS_DIR = os.path.join(BASE, "pages", "products", "items")
CAT_PAGE = os.path.join(BASE, "pages", "products", "Bathroom Fittings and Accessories.html")

pdf_path = r'c:\Users\Shubham\Downloads\Balaji Udyog bathroom fitting process .pdf'
doc = fitz.open(pdf_path)

# Detailed mapping of the 57 pages of the bathroom fitting process PDF
BATH_PRODUCTS = [
    # FLORENCE COLLECTION (Pages 0–17)
    {"name": "fl-1001-bib-cock", "title": "FL-1001 Bib Cock with Flange", "sku": "FL-1001", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1002-bib-cock-long", "title": "FL-1002 Bib Cock Long Body with Flange", "sku": "FL-1002", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1003-angle-valve", "title": "FL-1003 Angle Valve with Flange", "sku": "FL-1003", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1112-two-way-bib-cock", "title": "FL-1112 Two Way Bib Cock with Flange", "sku": "FL-1112", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1007-concealed-stop-cock", "title": "FL-1007 Concealed Stop Cock", "sku": "FL-1007", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1004-pillar-cock", "title": "FL-1004 Pillar Cock", "sku": "FL-1004", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1111-sink-cock", "title": "FL-1111 Sink Cock with Flange", "sku": "FL-1111", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1131-basin-mixer", "title": "FL-1131 Centre Hole Basin Mixer", "sku": "FL-1131", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1132-sink-mixer", "title": "FL-1132 Sink Mixer", "sku": "FL-1132", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1124-wall-mixer-3in1", "title": "FL-1124 Wall Mixer 3in1 with L-Bend", "sku": "FL-1124", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1122-wall-mixer", "title": "FL-1122 Wall Mixer with L-Bend", "sku": "FL-1122", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1123-single-lever-basin-mixer", "title": "FL-1123 Single Lever Basin Mixer", "sku": "FL-1123", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-div-divertor", "title": "Single Lever Divertor Four Way", "sku": "FL-DIV", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-1008-flush-valve", "title": "FL-1008 H.T. Concealed Type Flush Valve", "sku": "FL-1008", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-internal-fitting-3-4", "title": "Internal Fitting 3/4\"", "sku": "FL-IF-34", "material": "Solid Brass", "finish": "Natural"},
    {"name": "fl-internal-fitting-stop-cock", "title": "Internal Fitting Concealed Stop Cock 3/4\"", "sku": "FL-IF-CSC", "material": "Solid Brass", "finish": "Natural"},
    {"name": "fl-knob-set", "title": "Knob Complete set", "sku": "FL-KS", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "fl-flange-stop-cock", "title": "Flange Concealed Stop Cock", "sku": "FL-FC", "material": "Solid Brass", "finish": "Chrome Finish"},

    # AURA COLLECTION (Pages 18–33)
    {"name": "a-1001-bib-cock", "title": "A-1001 Bib Cock with Flange", "sku": "A-1001", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1002-bib-cock-long", "title": "A-1002 Bib Cock Long Body with Flange", "sku": "A-1002", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1011-two-way-bib-cock", "title": "A-1011 Two Way Bib Cock with Flange", "sku": "A-1011", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1003-angle-valve", "title": "A-1003 Angle Valve with Flange", "sku": "A-1003", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1007-concealed-stop-cock", "title": "A-1007 Concealed Stop Cock", "sku": "A-1007", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1004-pillar-cock", "title": "A-1004 Pillar Cock", "sku": "A-1004", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1111-sink-cock", "title": "A-1111 Sink Cock with Flange", "sku": "A-1111", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1005-swan-neck", "title": "A-1005 Swan Neck with Swinging Spout", "sku": "A-1005", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1132-sink-mixer", "title": "A-1132 Sink Mixer", "sku": "A-1132", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1123-wall-mixer", "title": "A-1123 Wall Mixer non Telephonic", "sku": "A-1123", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-1124-wall-mixer-l-bend", "title": "A-1124 Wall Mixer with L-Bend", "sku": "A-1124", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-internal-fitting", "title": "Internal Fitting", "sku": "A-IF", "material": "Solid Brass", "finish": "Natural"},
    {"name": "a-internal-fitting-stop-cock", "title": "Internal Fitting Concealed Stop Cock", "sku": "A-IF-CSC", "material": "Solid Brass", "finish": "Natural"},
    {"name": "a-knob-set", "title": "Knob Complete set", "sku": "A-KS", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-knob-set-gloria", "title": "Gloria Optional Knob Complete set", "sku": "A-KS-GL", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "a-flange-stop-cock", "title": "Flange Concealed Stop Cock", "sku": "A-FC", "material": "Solid Brass", "finish": "Chrome Finish"},

    # ACCESSORIES & FLUSH VALVES (Pages 34–56)
    {"name": "overhead-shower-opal", "title": "Overhead Shower Opal", "sku": "OHS-OPAL", "material": "Solid Brass / ABS", "finish": "Chrome Finish"},
    {"name": "overhead-shower-conty", "title": "Overhead Shower Conty", "sku": "OHS-CONTY", "material": "Solid Brass / ABS", "finish": "Chrome Finish"},
    {"name": "overhead-shower-qubix", "title": "Overhead Shower Qubix 4\"", "sku": "OHS-QUBIX", "material": "Solid Brass / ABS", "finish": "Chrome Finish"},
    {"name": "health-faucet-hook", "title": "Health Faucet with 1 Mtr. CP Tube & Hook", "sku": "HF-CP1", "material": "Solid Brass / ABS", "finish": "Chrome Finish"},
    {"name": "auto-close-pillar-cock", "title": "Auto Close Pillar Cock", "sku": "AC-PC", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "auto-closing-bib-cock", "title": "Auto Closing Bib Cock", "sku": "AC-BC", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "auto-closing-angle-valve", "title": "Auto Closing Angle Valve", "sku": "AC-AV", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "concealed-flush-valve-single", "title": "Soft Touch Push Button Concealed Flush Valve 32mm SINGLE FLUSH", "sku": "CFV-32S", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "concealed-flush-valve-dual", "title": "Soft Touch Push Button Concealed Flush Valve 32mm DUAL FLUSH", "sku": "CFV-32D", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "bottle-trap-502", "title": "502 Bottle Trap 32mm with 12\" Long Discharge Pipe", "sku": "BT-502", "material": "Brass / Stainless Steel", "finish": "Chrome Finish"},
    {"name": "universal-angle-valve", "title": "UN-1027 Angle Valve Universal", "sku": "UN-1027", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "pvc-connection-heavy-duty", "title": "PVC Connection Heavy Duty", "sku": "PVC-HD", "material": "PVC / Brass", "finish": "Natural"},
    {"name": "extension-nipple", "title": "Extension Nipple", "sku": "EXT-NP", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "l-bend", "title": "L - Bend", "sku": "L-BEND", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "leg-set-basin-mixer", "title": "Leg Set of Centre Hole Basin Mixer", "sku": "LEG-CH", "material": "Solid Brass / Copper", "finish": "Natural"},
    {"name": "legs-pair-wall-mixer", "title": "Pair of Legs for Wall Mixer", "sku": "LEG-WM", "material": "Solid Brass / Chrome", "finish": "Chrome Finish"},
    {"name": "legs-pair-basin-mixer", "title": "Pair of Legs for Basin Mixer", "sku": "LEG-BM", "material": "Solid Brass / Copper", "finish": "Natural"},
    {"name": "full-thread-stop-cock-1-2", "title": "Full Thread Stop Cock / Gate Valve 1/2\"", "sku": "FT-12", "material": "Solid Brass", "finish": "Brass Finish"},
    {"name": "full-thread-stop-cock-3-4", "title": "Full Thread Stop Cock / Gate Valve 3/4\"", "sku": "FT-34", "material": "Solid Brass", "finish": "Brass Finish"},
    {"name": "metro-pole-stop-cock", "title": "Metro Pole Stop Cock", "sku": "MP-SC", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "full-thread-stop-cock-1", "title": "Full Thread Stop Cock / Gate Valve 1\"", "sku": "FT-10", "material": "Solid Brass", "finish": "Brass Finish"},
    {"name": "self-closing-push-cock", "title": "Self Closing Push Cock", "sku": "SC-PC", "material": "Solid Brass", "finish": "Chrome Finish"},
    {"name": "washing-machine-cock", "title": "Washing Machine Cock", "sku": "WM-COCK", "material": "Solid Brass", "finish": "Chrome Finish"}
]

def make_product_page(product, category_name, category_file):
    title = product['title']
    sku = product['sku']
    img_file = product['img']
    wa_text = urllib.parse.quote(f"Hello, I'm interested in {title} ({sku}).")
    img_path = f"../../../assets/images/products/items/{img_file}"
    material = product.get('material', 'Solid Brass')
    finish = product.get('finish', 'Chrome Finish')
    
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
    # Note: Bathroom fittings process PDF pages are already 1440x810 (16:9 points).
    # Using Matrix of 1.33333333, 1.33333333 scales it to 1920x1080 for crisp output.
    pix = page.get_pixmap(matrix=fitz.Matrix(1.33333333, 1.33333333))
    img = Image.open(io.BytesIO(pix.tobytes()))
    
    prod_data = BATH_PRODUCTS[i]
    title = prod_data["title"]
    sku = prod_data["sku"]
    slug = prod_data["name"]
    name = f"bath-{slug}-16x9"
    
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
    make_product_page(product_data, "Bathroom Fittings & Accessories", "Bathroom Fittings and Accessories.html")
    
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

# Replace the grid in Bathroom Fittings and Accessories.html
with open(CAT_PAGE, 'r', encoding='utf-8') as f:
    cat_html = f.read()

# Locate the grid element and replace everything inside it
# Grid starts with `<div class="grid">` and ends with the matching `</div>` before `</div></div>`
grid_start_marker = '<div class="cat-gallery wrap"><div class="grid">'
grid_end_marker = '  </div></div>\n<a href="https://wa.me'

try:
    start_idx = cat_html.index(grid_start_marker) + len(grid_start_marker)
    end_idx = cat_html.index(grid_end_marker)
    
    new_grid_content = "".join(html_items_to_inject)
    cat_html = cat_html[:start_idx] + new_grid_content + "\n" + cat_html[end_idx:]
    
    with open(CAT_PAGE, 'w', encoding='utf-8') as f:
        f.write(cat_html)
        
    print("Successfully replaced the grid in Bathroom Fittings and Accessories.html with 57 new 16:9 product cards.")
except Exception as e:
    print(f"Failed to automatically replace the grid: {e}")
