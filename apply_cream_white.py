import os
import re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def process_content(content):
    # Variables
    content = re.sub(r'--paper:\s*#[a-fA-F0-9]+;', '--paper:#FAF9F6;', content)
    content = re.sub(r'--paper-2:\s*#[a-fA-F0-9]+;', '--paper-2:#F4F1EA;', content)
    
    content = re.sub(r'--ink:\s*#[a-fA-F0-9]+;', '--ink:#1F2937;', content)
    content = re.sub(r'--ink-2:\s*rgba\([^)]+\);', '--ink-2:#4B5563;', content)
    content = re.sub(r'--grey:\s*rgba\([^)]+\);', '--grey:#6B7280;', content)

    content = re.sub(r'--dark-h:\s*#[a-fA-F0-9]+;', '--dark-h: #FFFFFF;', content)
    content = re.sub(r'--dark-p:\s*rgba\([^)]+\);', '--dark-p: rgba(255,255,255,0.85);', content)
    content = re.sub(r'--dark-muted:\s*rgba\([^)]+\);', '--dark-muted: rgba(255,255,255,0.6);', content)

    content = re.sub(r'--navy:\s*#[a-fA-F0-9]+;', '--navy:#4682B4;', content)
    content = re.sub(r'--navy-2:\s*#[a-fA-F0-9]+;', '--navy-2:#355E7C;', content)
    content = re.sub(r'--navy-deep:\s*#[a-fA-F0-9]+;', '--navy-deep:#2B4C63;', content) 

    # Less Orange (Muted)
    content = re.sub(r'--gold:\s*#[a-fA-F0-9]+;', '--gold:#C87B53;', content)
    content = re.sub(r'--gold-soft:\s*#[a-fA-F0-9]+;', '--gold-soft:#D68B63;', content)
    content = re.sub(r'--gold-dim:\s*#[a-fA-F0-9]+;', '--gold-dim:#B56942;', content)

    # Hero
    content = re.sub(r'(\.hero\{[^}]*)background:var\(--navy-deep\);color:var\(--dark-h\)', r'\1background:var(--paper);color:var(--ink)', content)
    content = re.sub(r'(\.page-hero\{[^}]*)background:var\(--navy-deep\);color:var\(--dark-h\)', r'\1background:var(--paper);color:var(--ink)', content)
    
    content = re.sub(r'(\.hero h1,\.hero h2,\.hero h3,\.hero h4)\{color:var\(--dark-h\)\}', r'\1{color:var(--navy)}', content)
    content = re.sub(r'(\.hero \.lede\{[^}]*)color:var\(--dark-p\)', r'\1color:var(--ink-2)', content)
    content = re.sub(r'(\.hero-meta \.num\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.hero-meta \.lbl\{[^}]*)color:var\(--dark-muted\)', r'\1color:var(--grey)', content)

    # Hero Gradients
    content = content.replace('linear-gradient(180deg,rgba(43,76,99,.35) 0%,rgba(43,76,99,.85) 70%,var(--navy-deep) 100%)',
                              'linear-gradient(180deg,rgba(250,249,246,.35) 0%,rgba(250,249,246,.85) 70%,var(--paper) 100%)')

    # Nav
    content = content.replace('background:rgba(43,76,99,.95)', 'background:rgba(250,249,246,.95)')
    content = content.replace('background:rgba(43,76,99,.98)', 'background:rgba(250,249,246,.98)')

    content = re.sub(r'(\.logo\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.logo-text b\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.nav-menu a:hover\{)color:var\(--gold\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.nav-menu a:hover,\.nav-menu a\.active\{)color:var\(--gold\)', r'\1color:var(--navy)', content)
    content = re.sub(r'(\.nav-menu a\{[^}]*)color:var\(--dark-p\)', r'\1color:var(--ink-2)', content)

    content = re.sub(r'(\.dropdown-panel\{[^}]*)background:var\(--navy-deep\)', r'\1background:var(--paper)', content)
    content = re.sub(r'(\.dropdown-panel a\{[^}]*)color:var\(--dark-p\)', r'\1color:var(--ink-2)', content)

    # Cards
    content = re.sub(r'(\.cat\{[^}]*)background:var\(--navy-deep\);color:var\(--dark-h\);', r'\1background:#fff;color:var(--ink);', content)
    content = re.sub(r'(\.product-card\{[^}]*)background:var\(--navy-deep\);color:var\(--dark-h\);', r'\1background:#fff;color:var(--ink);', content)
    
    content = content.replace('; border: 1px solid #F7E7D7', '')
    content = content.replace('; border: 1px solid #FFF3E8', '')

    content = re.sub(r'(\.cat-foot h3\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--ink)', content)
    content = re.sub(r'(\.product-card h4\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--ink)', content)

    # Buttons
    content = content.replace('.btn-gold{background:var(--gold);color:#fff}', '.btn-gold{background:var(--navy);color:#fff}')
    content = content.replace('.btn-gold:hover{background:var(--gold-soft)}', '.btn-gold:hover{background:var(--navy-deep)}')
    
    content = content.replace('.btn-ghost-light{border-color:var(--dark-h);color:var(--dark-h);background:transparent}', '.btn-ghost-light{border-color:var(--navy);color:var(--navy);background:transparent}')
    content = content.replace('.btn-ghost-light:hover{border-color:var(--gold);background:var(--gold);color:#fff}', '.btn-ghost-light:hover{border-color:var(--navy);background:var(--navy);color:#fff}')

    # Highlights
    content = content.replace('Premium Indian Hardware<br>&amp; <em>Decor</em> Exporter', 'Premium Indian Hardware<br>&amp; Decor Exporter')
    content = content.replace('efficient global <em>trade</em> operations', 'efficient global trade operations')
    content = content.replace('<h2>Seven categories.<br>One reliable <em>partner</em>.</h2>', '<h2>Seven categories.<br>One reliable partner.</h2>')

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
