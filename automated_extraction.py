import fitz
import os
import glob
from bs4 import BeautifulSoup
import cv2
import numpy as np

items_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"
img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"
pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\master-export-catalogue-2026.pdf"

os.makedirs(img_out_dir, exist_ok=True)
html_files = glob.glob(os.path.join(items_dir, "*.html"))

def crop_product(img_path, out_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold: anything darker than 250 is considered object
    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Morphological closing to merge broken parts of the product
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        best_box = None
        max_area = 0
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            if area > max_area:
                max_area = area
                best_box = (x, y, w, h)
                
        if best_box:
            x, y, w, h = best_box
            pad = 40
            y1 = max(0, y - pad)
            y2 = min(img.shape[0], y + h + pad)
            x1 = max(0, x - pad)
            x2 = min(img.shape[1], x + w + pad)
            cropped = img[y1:y2, x1:x2]
            cv2.imwrite(out_path, cropped)
            return True
            
    # Fallback to saving original if no crop found
    cv2.imwrite(out_path, img)
    return False

# Open the master catalogue
doc = fitz.open(pdf_path)

total_processed = 0

for file_path in html_files:
    if os.path.basename(file_path) == "index.html":
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        
    sku_div = soup.find('div', class_='pdp-sku')
    if not sku_div:
        continue
        
    sku_text = sku_div.text.replace('SKU:', '').strip()
    
    # Search for SKU in PDF
    found_page = -1
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        instances = page.search_for(sku_text)
        if instances:
            found_page = page_num
            break
            
    if found_page != -1:
        page = doc.load_page(found_page)
        # Render page
        mat = fitz.Matrix(2.0, 2.0) # 2x zoom for high quality
        pix = page.get_pixmap(matrix=mat)
        
        temp_img_path = os.path.join(img_out_dir, f"temp_{sku_text}.png")
        pix.save(temp_img_path)
        
        # New image path
        base_name = os.path.basename(file_path).replace('.html', '.jpg')
        final_img_path = os.path.join(img_out_dir, base_name)
        
        # Crop
        crop_product(temp_img_path, final_img_path)
        
        # Remove temp
        os.remove(temp_img_path)
        
        # Update HTML
        new_img_src = f"../../../assets/images/products/items/{base_name}"
        
        # We need to replace the src of the hero image and thumbnail
        # Let's use BeautifulSoup or simple string replace if we know the structure.
        # But wait, earlier I used `generate_image` or the script created `.webp` images!
        # The AI generated ones look like: <img id="main-image" src="../../../assets/images/products/items/adjustable-furniture-leg-hero.webp" ...>
        # Let's do a regex or simple replace
        
        # Find the main image src
        img_el = soup.find('img', id='main-image')
        if img_el:
            old_src = img_el['src']
            html_content = html_content.replace(old_src, new_img_src)
            # Also replace in the thumbnail
            thumb_el = soup.find('div', class_='pdp-thumb')
            if thumb_el:
                thumb_img = thumb_el.find('img')
                if thumb_img:
                    old_thumb_src = thumb_img['src']
                    html_content = html_content.replace(old_thumb_src, new_img_src)
                    
            # Also replace in the swapImage onclick
            html_content = html_content.replace(f"swapImage('{old_src}'", f"swapImage('{new_img_src}'")
            
            # Save HTML
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            print(f"Extracted and updated: {sku_text} -> {base_name}")
            total_processed += 1
    else:
        print(f"SKU {sku_text} not found in master catalogue.")

print(f"Finished extracting {total_processed} items.")
