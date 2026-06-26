import os
import glob
import re

base_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
# recursively find all .html files
html_files = glob.glob(os.path.join(base_dir, "**", "*.html"), recursive=True)

for filepath in html_files:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to match <li><a href="...Export Services.html"...>Export Services</a></li>
    content = re.sub(r'<li><a href="[^"]*Export Services\.html"[^>]*>Export Services</a></li>\s*', '', content)
    
    # Regex to match <a href="...Export Services.html"...>Export Services</a> (when it is not in an li, like the navbar)
    content = re.sub(r'<a href="[^"]*Export Services\.html"[^>]*>Export Services</a>\s*', '', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Delete Export Services.html
export_path = os.path.join(base_dir, "pages", "Export Services.html")
if os.path.exists(export_path):
    os.remove(export_path)
    print("Deleted Export Services.html")

print(f"Export Services links removed from {len(html_files)} HTML files.")
