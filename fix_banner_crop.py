import os
from PIL import Image

# We will just fix the top crop boundaries to avoid the "BRASS MORTICE HANDLES" banner.
# The banner is at the very top of the PDF page. 
# Row 1 handles start lower down.
# Let's adjust the Top boundary for Row 1 from 30 to 130 (at 1x scale).

handles = [
    # ROW 1 (Top changed from 30 to 130 to avoid the banner!)
    {"filename": "rbm-12-heavy-spoon.jpg", "box": (90, 130, 310, 320)},
    {"filename": "rbm-cielo.jpg", "box": (310, 130, 525, 320)},
    {"filename": "rbm-7-zen.jpg", "box": (525, 130, 735, 320)},
    {"filename": "rbm-logan.jpg", "box": (735, 130, 940, 320)},
    {"filename": "rbm-8-renault.jpg", "box": (940, 130, 1135, 320)},
    {"filename": "rbm-8-smart.jpg", "box": (1135, 130, 1340, 320)},
    
    # ROW 2 (Top can stay 380, no banner here)
    {"filename": "rbm-19-roxy.jpg", "box": (90, 380, 310, 670)},
    {"filename": "rbm-13-verna.jpg", "box": (310, 380, 525, 670)},
    {"filename": "rbm-8-nayaab.jpg", "box": (525, 380, 735, 670)},
    {"filename": "rbm-8-cedia.jpg", "box": (735, 380, 940, 670)},
    {"filename": "rbm-9-simple.jpg", "box": (940, 380, 1135, 670)},
    {"filename": "rbm-11-niks.jpg", "box": (1135, 380, 1340, 670)}
]

img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"
import fitz
pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Furniture Hardware (1).pdf"
doc = fitz.open(pdf_path)
page = doc[1] 
mat = fitz.Matrix(3.0, 3.0) 
pix = page.get_pixmap(matrix=mat)
temp_img_path = os.path.join(img_out_dir, "temp_catalog_12_fix.png")
pix.save(temp_img_path)

img = Image.open(temp_img_path)

for p in handles:
    l, t, r, b = p["box"]
    # Convert from 1x to 3x
    l, t, r, b = l*3, t*3, r*3, b*3
    
    cropped = img.crop((l, t, r, b))
    out_img = os.path.join(img_out_dir, p['filename'])
    cropped.save(out_img)
    print(f"Saved {out_img} without banner!")

os.remove(temp_img_path)
print("Finished fixing banner issue.")
