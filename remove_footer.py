import os, re
root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
            orig = content
            
            # Remove the whole Export Markets foot-col
            content = re.sub(r'<div class="foot-col"><h4>Export Markets</h4><ul>.*?</ul></div>', '', content, flags=re.DOTALL)
            
            if content != orig:
                with open(filepath, 'w', encoding='utf-8') as f: f.write(content)
