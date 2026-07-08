import os
import fitz
from PIL import Image

pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Furniture Hardware (1).pdf"
img_out_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products\items"
doc = fitz.open(pdf_path)
page = doc[1] 
mat = fitz.Matrix(3.0, 3.0) 
pix = page.get_pixmap(matrix=mat)
img_path = os.path.join(img_out_dir, "temp_catalog.png")
pix.save(img_path)

img = Image.open(img_path)

new_products = [
    {"img": "rbm-12.jpg", "crop_rect": (186, 331, 240, 345)},
    {"img": "rbm-cielo.jpg", "crop_rect": (416, 349, 444, 362)},
    {"img": "rbm-7.jpg", "crop_rect": (623, 331, 669, 345)},
    {"img": "rbm-logan.jpg", "crop_rect": (839, 349, 874, 362)},
    {"img": "rbm-8.jpg", "crop_rect": (1035, 331, 1081, 345)}
]

for p in new_products:
    x0, y0, x1, y1 = p["crop_rect"]
    x0, y0, x1, y1 = x0*3, y0*3, x1*3, y1*3
    
    cx = (x0 + x1) / 2
    crop_w = 400
    
    left = cx - crop_w/2
    right = cx + crop_w/2
    
    # The handle is above the text, and can go all the way up to near the top of the page.
    # We will crop from exactly above the text, up to 1000 pixels (which covers the entire height up to y=0)
    top = max(0, y0 - 1000)
    bottom = y0 - 30
    
    cropped = img.crop((left, top, right, bottom))
    
    # Optional: we can autocrop white borders from this image so it's tight
    import cv2
    import numpy as np
    opencv_img = np.array(cropped)
    opencv_img = opencv_img[:, :, ::-1].copy() # RGB to BGR
    gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        pad = 20
        y1_crop = max(0, y - pad)
        y2_crop = min(opencv_img.shape[0], y + h + pad)
        x1_crop = max(0, x - pad)
        x2_crop = min(opencv_img.shape[1], x + w + pad)
        final_cropped = opencv_img[y1_crop:y2_crop, x1_crop:x2_crop]
    else:
        final_cropped = opencv_img

    out_img = os.path.join(img_out_dir, p["img"])
    cv2.imwrite(out_img, final_cropped)
    print(f"Saved {out_img} with full uncut height!")

os.remove(img_path)
