import os
import re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def process_content(content):
    # Variables
    content = re.sub(r'--dark-h:\s*#[a-fA-F0-9]+;', '--dark-h: #F7F3EA;', content)
    content = re.sub(r'--navy:\s*#[a-fA-F0-9]+;', '--navy:#4682B4;', content)
    content = re.sub(r'--navy-2:\s*#[a-fA-F0-9]+;', '--navy-2:#3A6D96;', content)
    content = re.sub(r'--navy-deep:\s*#[a-fA-F0-9]+;', '--navy-deep:#355E7C;', content)
    content = re.sub(r'--gold:\s*#[a-fA-F0-9]+;', '--gold:#E67E22;', content)
    content = re.sub(r'--gold-soft:\s*#[a-fA-F0-9]+;', '--gold-soft:#F39C12;', content)
    content = re.sub(r'--gold-dim:\s*#[a-fA-F0-9]+;', '--gold-dim:#D35400;', content)
    content = re.sub(r'--paper:\s*#[a-fA-F0-9]+;', '--paper:#F7F3EA;', content)
    content = re.sub(r'--paper-2:\s*#[a-fA-F0-9]+;', '--paper-2:#FFFDF8;', content)
    content = re.sub(r'--ink:\s*#[a-fA-F0-9]+;', '--ink:#1F2937;', content)
    content = re.sub(r'--ink-2:\s*#[a-fA-F0-9]+;', '--ink-2:#4B5563;', content)
    content = re.sub(r'--grey:\s*#[a-fA-F0-9]+;', '--grey:#6B7280;', content)

    # Hero Background & Typography
    content = re.sub(r'(\.hero\{[^}]*)background:var\(--navy-deep\);color:var\(--dark-h\)', r'\1background:var(--paper);color:var(--ink)', content)
    content = re.sub(r'(\.page-hero\{[^}]*)background:var\(--navy-deep\);color:var\(--dark-h\)', r'\1background:var(--paper);color:var(--ink)', content)
    
    content = re.sub(r'(\.hero h1,\.hero h2,\.hero h3,\.hero h4)\{color:var\(--dark-h\)\}', r'\1{color:var(--navy)}', content)
    content = re.sub(r'(\.hero \.lede\{[^}]*)color:var\(--dark-p\)', r'\1color:var(--ink-2)', content)
    content = re.sub(r'(\.hero-meta \.num\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.hero-meta \.lbl\{[^}]*)color:var\(--dark-muted\)', r'\1color:var(--grey)', content)

    # Gradients in hero
    content = content.replace('linear-gradient(180deg,rgba(6,18,42,.35) 0%,rgba(6,18,42,.85) 70%,var(--navy-deep) 100%)',
                              'linear-gradient(180deg,rgba(247,243,234,.35) 0%,rgba(247,243,234,.85) 70%,var(--paper) 100%)')
    
    # Nav updates
    content = content.replace('background:rgba(6,18,42,.82)', 'background:rgba(247,243,234,.95)')
    content = content.replace('background:rgba(6,18,42,.9)', 'background:rgba(247,243,234,.95)')
    content = content.replace('background:rgba(6,18,42,.98)', 'background:rgba(247,243,234,.98)')

    # Logo and Links
    content = re.sub(r'(\.logo\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.logo-text b\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.nav-menu a:hover\{)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.nav-menu a:hover,\.nav-menu a\.active\{)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.nav-menu a\{[^}]*)color:var\(--dark-p\)', r'\1color:var(--ink-2)', content)

    # Dropdown Menu
    content = re.sub(r'(\.dropdown-panel\{[^}]*)background:#0a1d3a', r'\1background:var(--paper)', content)
    content = re.sub(r'(\.dropdown-panel a\{[^}]*)color:var\(--dark-p\)', r'\1color:var(--ink-2)', content)

    # Buttons
    content = content.replace('.btn-gold{background:var(--gold);color:var(--navy)}', '.btn-gold{background:var(--navy);color:#fff}')
    content = content.replace('.btn-gold:hover{background:var(--gold-soft)}', '.btn-gold:hover{background:var(--gold)}')
    content = content.replace('.btn-ghost-light{border-color:var(--dark-p);color:var(--dark-h)}', '.btn-ghost-light{border-color:var(--navy);color:var(--navy);background:transparent}')
    content = content.replace('.btn-ghost-light:hover{border-color:var(--gold);background:var(--gold);color:var(--navy)}', '.btn-ghost-light:hover{border-color:var(--gold);background:var(--gold);color:#fff}')

    return content

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.css') or filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = process_content(content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
