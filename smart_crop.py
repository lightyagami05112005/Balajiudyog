import fitz
import os
import cv2
import numpy as np

pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Furniture Hardware (1).pdf"
img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"

doc = fitz.open(pdf_path)
page = doc[1]
mat = fitz.Matrix(3.0, 3.0) 
pix = page.get_pixmap(matrix=mat)

temp_img_path = os.path.join(img_out_dir, "temp_catalog.png")
pix.save(temp_img_path)

img = cv2.imread(temp_img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Connect parts
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

bounding_boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    area = w * h
    if area > 5000: # Lowered threshold
        bounding_boxes.append((x, y, w, h, area))

print(f"Found {len(bounding_boxes)} large contours.")

text_rects = {
    "rbm-12.jpg": (186*3, 331*3), 
    "rbm-cielo.jpg": (416*3, 349*3),
    "rbm-7.jpg": (623*3, 331*3),
    "rbm-logan.jpg": (839*3, 349*3),
    "rbm-8.jpg": (1035*3, 331*3)
}

for filename, (tx, ty) in text_rects.items():
    best_box = None
    min_dist = float('inf')
    
    for x, y, w, h, area in bounding_boxes:
        box_center_x = x + w/2
        box_bottom_y = y + h
        dist = ((box_center_x - tx)**2 + (box_bottom_y - ty)**2)**0.5
        
        # Less strict constraint: the bottom of the handle should be near the text top
        if box_bottom_y < ty + 300: 
            if dist < min_dist:
                min_dist = dist
                best_box = (x, y, w, h)
                
    if best_box:
        x, y, w, h = best_box
        pad = 40
        y1 = max(0, y - pad)
        y2 = min(img.shape[0], y + h + pad)
        x1 = max(0, x - pad)
        x2 = min(img.shape[1], x + w + pad)
        
        cropped = img[y1:y2, x1:x2]
        out_path = os.path.join(img_out_dir, filename)
        cv2.imwrite(out_path, cropped)
        print(f"Properly cropped and saved {filename} with size {w}x{h}")
    else:
        print(f"Failed to find box for {filename}")

os.remove(temp_img_path)
