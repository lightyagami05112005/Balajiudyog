import fitz
import os

pdf_path = r"c:\Users\Shubham\Downloads\Balaji Udyog bathroom fitting process .pdf"
if not os.path.exists(pdf_path):
    print("PDF not found!")
    exit(1)

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

for i in range(len(doc)):
    page = doc[i]
    text = page.get_text()
    images = page.get_images()
    print(f"Page {i}: {page.rect.width}x{page.rect.height}, Text length: {len(text)}, Images: {len(images)}")
    if text.strip():
        print(f"--- Text page {i} ---")
        print(text[:500])
        print("-----------------------")
