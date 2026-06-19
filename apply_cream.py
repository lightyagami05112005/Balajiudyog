import os, re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def apply_cream_white(content):
    # Change dark text heading from pure white to cream white
    content = content.replace('--dark-h: #FFFFFF;', '--dark-h: #FCFBF8;')
    
    # Change the main background 'paper' variables to cream white
    content = content.replace('--paper:#f5f2ec;', '--paper:#FCFBF8;')
    content = content.replace('--paper-2:#ebe6db;', '--paper-2:#F5F2EA;')
    
    # Also catch inline styles that might have spaced formatting
    content = content.replace('--paper: #f5f2ec;', '--paper: #FCFBF8;')
    content = content.replace('--paper-2: #ebe6db;', '--paper-2: #F5F2EA;')
    
    return content

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.css'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = apply_cream_white(content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        elif filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content
            
            # Extract inline style
            style_match = re.search(r'<style>(.*?)</style>', content, flags=re.DOTALL)
            if style_match:
                new_style = apply_cream_white(style_match.group(1))
                content = content[:style_match.start(1)] + new_style + content[style_match.end(1):]
            
            if content != orig:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
