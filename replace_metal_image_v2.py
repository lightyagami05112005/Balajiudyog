import os
import re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(('.html', '.js', '.md', '.css')):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace metal-art-ware-hero.webp or metal-art-ware-hero.jpg?v=... with metal-art-ware-hero.jpg?v=12345
            new_content = re.sub(r'metal-art-ware-hero\.(webp|jpg)(\?v[0-9]+)?', 'metal-art-ware-hero.jpg?v=12345', content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
