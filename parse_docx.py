import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"c:\Users\Shubham\Downloads\document 4 pages.docx"
if not os.path.exists(docx_path):
    print("File not found")
    exit(1)

try:
    with zipfile.ZipFile(docx_path) as docx:
        xml_content = docx.read('word/document.xml')
        root = ET.fromstring(xml_content)
        
        # Extract text from docx xml
        paragraphs = []
        for elem in root.iter():
            if elem.tag.endswith('t'):
                paragraphs.append(elem.text)
                
        full_text = " ".join(paragraphs)
        print("Text Length:", len(full_text))
        print("First 1000 characters:")
        print(full_text[:1000])
except Exception as e:
    print("Error:", e)
