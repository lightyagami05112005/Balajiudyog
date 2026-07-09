import fitz
import os

pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Bathroom Fitting (1).pdf"
if not os.path.exists(pdf_path):
    print("PDF not found!")
    exit(1)

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

for i in range(len(doc)):
    page = doc[i]
    text = page.get_text()
    print(f"Page {i}: Text length: {len(text)}")
    if text.strip():
        print(f"--- Text page {i} ---")
        print(text[:300])
        print("-----------------------")
