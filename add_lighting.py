import fitz
import os
import shutil

pdf_file = r"c:\Users\Shubham\Downloads\Balaji Udyog Lighting .pdf"
cat_id = "lighting"

base_img_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products"
base_cat_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs"
cat_thumb_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\categories"

out_dir = os.path.join(base_img_dir, cat_id)
os.makedirs(out_dir, exist_ok=True)
os.makedirs(base_cat_dir, exist_ok=True)
os.makedirs(cat_thumb_dir, exist_ok=True)

dest_pdf = os.path.join(base_cat_dir, os.path.basename(pdf_file))
shutil.copy(pdf_file, dest_pdf)
print(f"Copied {pdf_file} to {dest_pdf}")

try:
    doc = fitz.open(pdf_file)
    max_pages = len(doc)
    print(f"Total pages: {max_pages}")
    
    # Save thumbnail (first page) for the homepage
    try:
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        thumb_path = os.path.join(cat_thumb_dir, f"{cat_id}_thumb.jpg")
        pix.save(thumb_path)
        print(f"Saved thumbnail: {thumb_path}")
    except Exception as e:
        print(f"Error saving thumb: {e}")

    # Extract all pages for product category page
    for p in range(max_pages):
        page = doc.load_page(p)
        pix = page.get_pixmap(dpi=150)
        out_path = os.path.join(out_dir, f"page_{p+1}.jpg")
        pix.save(out_path)
    print(f"Saved {max_pages} pages to {out_dir}")
except Exception as e:
    print(f"Error processing {pdf_file}: {e}")
