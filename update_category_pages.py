import os
import glob
from bs4 import BeautifulSoup
import re

items_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"
cat_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products"

item_files = glob.glob(os.path.join(items_dir, "*.html"))
products_by_category = {}

for file_path in item_files:
    if os.path.basename(file_path) == "index.html":
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    title_el = soup.find('h1', class_='pdp-title')
    if not title_el:
        continue
    title = title_el.text.strip()
    
    sku_el = soup.find('div', class_='pdp-sku')
    sku = sku_el.text.replace('SKU:', '').strip() if sku_el else ""
    
    cat_el = soup.find('div', class_='pdp-category')
    cat = cat_el.text.strip() if cat_el else ""
    
    img_el = soup.find('img', id='main-image')
    img_src = img_el['src'] if img_el else ""
    
    if cat not in products_by_category:
        products_by_category[cat] = []
        
    products_by_category[cat].append({
        "title": title,
        "sku": sku,
        "img": img_src,
        "url": f"items/{os.path.basename(file_path)}"
    })

# Print found categories
print("Found categories:")
for c in products_by_category.keys():
    print(c)

# Map discovered categories to actual category files
# Known category files:
# Bathroom Fittings and Accessories.html
# Decorative Glassware.html
# Furniture Hardware and Locking Mechanism.html
# Lighting.html
# Stainless Steel and Brass Cutleries.html

# Let's define a rough mapping or just search for the closest file match.
cat_files = glob.glob(os.path.join(cat_dir, "*.html"))
cat_file_map = {}
for cf in cat_files:
    cat_file_map[os.path.basename(cf).replace('.html', '').lower()] = cf

for cat, products in products_by_category.items():
    # Try to find the matching category file
    cat_lower = cat.lower()
    matched_file = None
    
    if cat_lower == "stainless steel and brass cutleries" or "cutleries" in cat_lower:
        matched_file = os.path.join(cat_dir, "Stainless Steel and Brass Cutleries.html")
    elif cat_lower == "lighting":
        matched_file = os.path.join(cat_dir, "Lighting.html")
    elif cat_lower == "bathroom fittings and accessories" or "bathroom" in cat_lower:
        matched_file = os.path.join(cat_dir, "Bathroom Fittings and Accessories.html")
    elif cat_lower == "decorative glassware" or "glass" in cat_lower:
        matched_file = os.path.join(cat_dir, "Decorative Glassware.html")
    elif cat_lower == "furniture hardware" or "furniture" in cat_lower:
        matched_file = os.path.join(cat_dir, "Furniture Hardware and Locking Mechanism.html")
    else:
        # Fallback exact match or ignore
        if cat_lower in cat_file_map:
            matched_file = cat_file_map[cat_lower]
            
    if not matched_file or not os.path.exists(matched_file):
        print(f"Could not find category file for: {cat}")
        continue
        
    # Generate HTML grid
    grid_html = '<div class="grid">\n'
    for p in products:
        grid_html += f'''      <a href="{p['url']}" class="grid-item-link" style="text-decoration:none; color:inherit; display:block; transition: transform 0.3s;">
        <div class="grid-item" style="border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; height: 100%; display: flex; flex-direction: column;">
          <div style="aspect-ratio: 4/3; background: #f9f9f9; padding: 24px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid var(--line);">
            <img src="{p['img'].replace('../../../', '../../')}" alt="{p['title']}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
          </div>
          <div style="padding: 20px; text-align: left;">
            <div style="font-size: 12px; font-family: monospace; color: var(--ink-2); margin-bottom: 8px;">SKU: {p['sku']}</div>
            <h3 style="font-size: 16px; font-weight: 600; margin: 0; color: var(--navy-deep); line-height: 1.4;">{p['title']}</h3>
          </div>
        </div>
      </a>\n'''
    grid_html += '    </div>'
    
    with open(matched_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace the old <div class="grid"> with the new one
    # The old structure is usually: <div class="cat-gallery wrap">\n  <div class="grid"> ... </div>\n</div>
    
    pattern = r'<div class="grid">.*?</div>\s*(?=</div>)'
    new_content = re.sub(pattern, grid_html, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"Failed to replace grid in {os.path.basename(matched_file)}")
    else:
        with open(matched_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated category page: {os.path.basename(matched_file)}")

print("Category pages updated.")
