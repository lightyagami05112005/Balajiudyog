import fitz
import os
import glob
from bs4 import BeautifulSoup

pdfs = glob.glob(r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\catalogs\*.pdf")
items_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"
html_files = glob.glob(os.path.join(items_dir, "*.html"))

skus = []
for file_path in html_files:
    if os.path.basename(file_path) == "index.html":
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    sku_el = soup.find(string=lambda t: t and 'SKU' in t)
    sku_text = ""
    if sku_el:
        if '·' in sku_el:
            sku_text = sku_el.split('·')[1].strip()
        else:
            sku_text = sku_el.replace('SKU:', '').strip()
    sku_div = soup.find('div', class_='pdp-sku')
    if sku_div:
        t = sku_div.text
        if '·' in t:
            sku_text = t.split('·')[1].strip()
        else:
            sku_text = t.replace('SKU:', '').strip()
            
    if sku_text:
        skus.append((sku_text, os.path.basename(file_path)))

print(f"Extracted {len(skus)} SKUs from HTMLs.")
print("Sample SKUs:", skus[:5])

# Let's search for the first 5 SKUs in the PDFs
for sku, filename in skus[:5]:
    found = False
    for pdf_file in pdfs:
        doc = fitz.open(pdf_file)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_instances = page.search_for(sku)
            if text_instances:
                print(f"Found SKU {sku} in {os.path.basename(pdf_file)} on page {page_num+1} at {text_instances[0]}")
                found = True
        if found:
            break
    if not found:
        print(f"Could NOT find SKU {sku}")
