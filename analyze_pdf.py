import fitz

pdf_path = r'c:\Users\Shubham\Downloads\Balaji Udyog Furniture Hardware process .pdf'
doc = fitz.open(pdf_path)
print(f'Total pages: {len(doc)}')

for i in range(min(5, len(doc))):
    page = doc[i]
    images = page.get_images(full=True)
    print(f'Page {i} images: {len(images)}')
    for img in images:
        xref = img[0]
        base_image = doc.extract_image(xref)
        pix = fitz.Pixmap(doc, xref)
        print(f'  Image {xref}: {pix.width}x{pix.height}, ext: {base_image.get("ext", "")}')
