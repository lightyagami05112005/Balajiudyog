import os

# 1. Rename files
products_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products"

renames = {
    "Brassware and Steel Cutleries.html": "Stainless Steel and Brass Cutleries.html",
    "Bathroom Fitting.html": "Bathroom Fittings and Accessories.html",
    "Furniture Hardware.html": "Furniture Hardware and Locking Mechanism.html"
}

for old, new in renames.items():
    old_path = os.path.join(products_dir, old)
    new_path = os.path.join(products_dir, new)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old} to {new}")
    else:
        print(f"Not found: {old_path}")

# 2. Update Balaji Udyog.html
html_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\Balaji Udyog.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace HTML file references
html = html.replace("Brassware and Steel Cutleries.html", "Stainless Steel and Brass Cutleries.html")
html = html.replace("Bathroom Fitting.html", "Bathroom Fittings and Accessories.html")
html = html.replace("Furniture Hardware.html", "Furniture Hardware and Locking Mechanism.html")

# Replace Display Texts
html = html.replace("Brassware &amp; Steel Cutleries", "Stainless Steel &amp; Brass Cutleries")
html = html.replace("Brassware & Steel Cutleries", "Stainless Steel & Brass Cutleries")

html = html.replace(">Bathroom Fitting<", ">Bathroom Fittings &amp; Accessories<")
html = html.replace("<h3>Bathroom Fitting</h3>", "<h3>Bathroom Fittings &amp; Accessories</h3>")
html = html.replace("<span>Bathroom Fitting</span>", "<span>Bathroom Fittings &amp; Accessories</span>")

html = html.replace(">Furniture Hardware<", ">Furniture Hardware &amp; Locking Mechanism<")
html = html.replace("<h3>Furniture Hardware</h3>", "<h3>Furniture Hardware &amp; Locking Mechanism</h3>")
html = html.replace("<span>Furniture Hardware</span>", "<span>Furniture Hardware &amp; Locking Mechanism</span>")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated Balaji Udyog.html")

# 3. Update generate_pages.py
gen_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\generate_pages.py"
with open(gen_path, "r", encoding="utf-8") as f:
    gen = f.read()

gen = gen.replace('"Brassware and Steel Cutleries.html"', '"Stainless Steel and Brass Cutleries.html"')
gen = gen.replace('"Brassware & Steel Cutleries"', '"Stainless Steel & Brass Cutleries"')

gen = gen.replace('"Bathroom Fitting.html"', '"Bathroom Fittings and Accessories.html"')
gen = gen.replace('"Bathroom Fitting"', '"Bathroom Fittings & Accessories"')

gen = gen.replace('"Furniture Hardware.html"', '"Furniture Hardware and Locking Mechanism.html"')
gen = gen.replace('"Furniture Hardware"', '"Furniture Hardware & Locking Mechanism"')

with open(gen_path, "w", encoding="utf-8") as f:
    f.write(gen)
print("Updated generate_pages.py")
