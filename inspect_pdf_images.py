import fitz

pdf_path = r"c:\Users\Shubham\Downloads\Balaji Udyog bathroom fitting process .pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
for i in range(len(doc)):
    page = doc[i]
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        # Get image information dictionary
        img_info = doc.extract_image(xref)
        # Let's inspect the page resource details
        rect = page.get_image_rects(xref)
        print(f"Page {i} | Image xref {xref} | size {img_info.get('size')} | rect {rect}")
