import os
import re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(('.html', '.js', '.md', '.css')):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace .webp with .jpg, and handle the v=... query param
            new_content = re.sub(r'furniture-hardware-hero\.webp(\?v[0-9]+)?', 'furniture-hardware-hero.jpg?v=999', content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
