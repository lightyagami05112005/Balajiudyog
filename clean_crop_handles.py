import os
import fitz
from PIL import Image

pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Furniture Hardware (1).pdf"
img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"

doc = fitz.open(pdf_path)
page = doc[1]

# Render at 4x for maximum quality
mat = fitz.Matrix(4.0, 4.0)
pix = page.get_pixmap(matrix=mat)
temp_path = os.path.join(img_out_dir, "temp_full_page.png")
pix.save(temp_path)

img = Image.open(temp_path)
print(f"Full page size: {img.size}")

# Scale factor
S = 4

# Column boundaries (1x PDF points) - 6 columns
cols = [
    (80, 300),    # Col 1
    (300, 520),   # Col 2
    (520, 730),   # Col 3
    (730, 940),   # Col 4
    (940, 1140),  # Col 5
    (1140, 1340)  # Col 6
]

# Row boundaries (1x PDF points) - ONLY the handle area, NO text labels
rows = [
    (80, 325),   # Row 1: stops before SKU text at y=331
    (380, 672)   # Row 2: stops before SKU text at y=678
]

# Product definitions matching the grid: Row 1 L-to-R, then Row 2 L-to-R
products = [
    # ROW 1
    {"name": "rbm-12-heavy-spoon", "title": "RBM-12 Heavy Spoon", "sku": "RBM-12", "row": 0, "col": 0},
    {"name": "rbm-cielo", "title": "RBM Cielo", "sku": "RBM-Cielo", "row": 0, "col": 1},
    {"name": "rbm-7-zen", "title": "RBM-7 Zen", "sku": "RBM-7", "row": 0, "col": 2},
    {"name": "rbm-logan", "title": "RBM Logan", "sku": "RBM-Logan", "row": 0, "col": 3},
    {"name": "rbm-8-renault", "title": "RBM-8 Renault", "sku": "RBM-8-Renault", "row": 0, "col": 4},
    {"name": "rbm-8-smart", "title": "RBM-8 Smart", "sku": "RBM-8-Smart", "row": 0, "col": 5},
    # ROW 2
    {"name": "rbm-19-roxy", "title": "RBM-19 Roxy", "sku": "RBM-19", "row": 1, "col": 0},
    {"name": "rbm-13-verna", "title": "RBM-13 Verna", "sku": "RBM-13", "row": 1, "col": 1},
    {"name": "rbm-8-nayaab", "title": "RBM-8 Nayaab", "sku": "RBM-8-Nayaab", "row": 1, "col": 2},
    {"name": "rbm-8-cedia", "title": "RBM-8 Cedia", "sku": "RBM-8-Cedia", "row": 1, "col": 3},
    {"name": "rbm-9-simple", "title": "RBM-9 Simple", "sku": "RBM-9", "row": 1, "col": 4},
    {"name": "rbm-11-niks", "title": "RBM-11 Niks", "sku": "RBM-11", "row": 1, "col": 5},
]

for p in products:
    r = rows[p["row"]]
    c = cols[p["col"]]
    
    # Scale to 4x
    left = c[0] * S
    right = c[1] * S
    top = r[0] * S
    bottom = r[1] * S
    
    cropped = img.crop((left, top, right, bottom))
    out_path = os.path.join(img_out_dir, f"{p['name']}.jpg")
    cropped.save(out_path, quality=95)
    print(f"Saved {p['name']}.jpg ({cropped.size[0]}x{cropped.size[1]})")

os.remove(temp_path)
print("\nDone! All 12 handles cropped cleanly without any text.")
