import fitz

pdf_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\Balaji Udyog Bathroom Fitting (1).pdf"
doc = fitz.open(pdf_path)

keywords = ["hook", "soap", "paper", "towel", "holder", "shelf", "dish", "accessories"]

for page_idx in range(len(doc)):
    page = doc[page_idx]
    text = page.get_text().lower()
    found = [kw for kw in keywords if kw in text]
    if found:
        print(f"Page {page_idx} contains: {found}")
