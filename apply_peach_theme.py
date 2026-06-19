import os
import re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def process_content(content):
    # Update Variables
    # Making Steel Blue the dominant background color to support white text
    content = re.sub(r'--dark-h:\s*#[a-fA-F0-9]+;', '--dark-h: #FFFFFF;', content)
    # The previous dark-p was rgba(255,255,255,0.85) or #E5E7EB
    content = re.sub(r'--dark-p:\s*#[a-fA-F0-9]+;', '--dark-p: rgba(255,255,255,0.85);', content)
    content = re.sub(r'--dark-p:\s*rgba\([^)]+\);', '--dark-p: rgba(255,255,255,0.85);', content)
    content = re.sub(r'--dark-muted:\s*#[a-fA-F0-9]+;', '--dark-muted: rgba(255,255,255,0.6);', content)
    
    content = re.sub(r'--navy:\s*#[a-fA-F0-9]+;', '--navy:#4682B4;', content)
    content = re.sub(r'--navy-2:\s*#[a-fA-F0-9]+;', '--navy-2:#355E7C;', content)
    content = re.sub(r'--navy-deep:\s*#[a-fA-F0-9]+;', '--navy-deep:#2B4C63;', content) 
    
    # Orange Highlights
    content = re.sub(r'--gold:\s*#[a-fA-F0-9]+;', '--gold:#FF8C42;', content)
    content = re.sub(r'--gold-soft:\s*#[a-fA-F0-9]+;', '--gold-soft:#FF9F61;', content)
    content = re.sub(r'--gold-dim:\s*#[a-fA-F0-9]+;', '--gold-dim:#E57E3B;', content)
    
    # Paper variables become Steel Blue (dominant background)
    content = re.sub(r'--paper:\s*#[a-fA-F0-9]+;', '--paper:#4682B4;', content)
    content = re.sub(r'--paper-2:\s*#[a-fA-F0-9]+;', '--paper-2:#355E7C;', content)
    
    # Text colors become White/Off-white
    content = re.sub(r'--ink:\s*#[a-fA-F0-9]+;', '--ink:#FFFFFF;', content)
    content = re.sub(r'--ink-2:\s*#[a-fA-F0-9]+;', '--ink-2:rgba(255,255,255,0.85);', content)
    content = re.sub(r'--grey:\s*#[a-fA-F0-9]+;', '--grey:rgba(255,255,255,0.6);', content)
    
    # Hero (Make it Deep Steel Blue)
    content = re.sub(r'(\.hero\{[^}]*)background:var\(--paper\);color:var\(--ink\)', r'\1background:var(--navy-deep);color:var(--dark-h)', content)
    content = re.sub(r'(\.page-hero\{[^}]*)background:var\(--paper\);color:var\(--ink\)', r'\1background:var(--navy-deep);color:var(--dark-h)', content)
    
    # Hero typography colors
    content = re.sub(r'(\.hero h1,\.hero h2,\.hero h3,\.hero h4)\{color:var\(--navy\)\}', r'\1{color:var(--dark-h)}', content)
    content = re.sub(r'(\.hero \.lede\{[^}]*)color:var\(--ink-2\)', r'\1color:var(--dark-p)', content)
    content = re.sub(r'(\.hero-meta \.num\{[^}]*)color:var\(--navy\)', r'\1color:var(--dark-h)', content)
    content = re.sub(r'(\.hero-meta \.lbl\{[^}]*)color:var\(--grey\)', r'\1color:var(--dark-muted)', content)

    # Hero Gradients: fade to navy-deep instead of paper
    content = content.replace('linear-gradient(180deg,rgba(247,243,234,.35) 0%,rgba(247,243,234,.85) 70%,var(--paper) 100%)',
                              'linear-gradient(180deg,rgba(43,76,99,.35) 0%,rgba(43,76,99,.85) 70%,var(--navy-deep) 100%)')

    # Nav updates
    content = content.replace('background:rgba(247,243,234,.95)', 'background:rgba(43,76,99,.95)')
    content = content.replace('background:rgba(247,243,234,.98)', 'background:rgba(43,76,99,.98)')

    # Logo and Links in Nav
    content = re.sub(r'(\.logo\{[^}]*)color:var\(--navy\)', r'\1color:var(--dark-h)', content)
    content = re.sub(r'(\.logo-text b\{[^}]*)color:var\(--navy\)', r'\1color:var(--dark-h)', content)
    content = re.sub(r'(\.nav-menu a:hover\{)color:var\(--navy\)', r'\1color:var(--gold)', content)
    content = re.sub(r'(\.nav-menu a:hover,\.nav-menu a\.active\{)color:var\(--navy\)', r'\1color:var(--gold)', content)
    content = re.sub(r'(\.nav-menu a\{[^}]*)color:var\(--ink-2\)', r'\1color:var(--dark-p)', content)

    # Dropdown Menu
    content = re.sub(r'(\.dropdown-panel\{[^}]*)background:var\(--paper\)', r'\1background:var(--navy-deep)', content)
    content = re.sub(r'(\.dropdown-panel a\{[^}]*)color:var\(--ink-2\)', r'\1color:var(--dark-p)', content)

    # Cards (cat & product-card)
    content = re.sub(r'(\.cat\{[^}]*)background:var\(--navy\);color:var\(--dark-h\);', r'\1background:var(--navy-deep);color:var(--dark-h);', content)
    content = re.sub(r'(\.product-card\{[^}]*)background:var\(--navy\);color:var\(--dark-h\);', r'\1background:var(--navy-deep);color:var(--dark-h);', content)
    
    # Text in cards
    content = re.sub(r'(\.cat-foot h3\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--dark-h)', content)
    content = re.sub(r'(\.product-card h4\{[^}]*)color:var\(--dark-h\)', r'\1color:var(--dark-h)', content)

    # Buttons
    content = content.replace('.btn-gold{background:var(--navy);color:#fff}', '.btn-gold{background:var(--gold);color:#fff}')
    content = content.replace('.btn-gold:hover{background:var(--gold)}', '.btn-gold:hover{background:var(--gold-soft)}')
    
    content = content.replace('.btn-ghost-light{border-color:var(--navy);color:var(--navy);background:transparent}', '.btn-ghost-light{border-color:var(--dark-h);color:var(--dark-h);background:transparent}')
    content = content.replace('.btn-ghost-light:hover{border-color:var(--gold);background:var(--gold);color:#fff}', '.btn-ghost-light:hover{border-color:var(--gold);background:var(--gold);color:#fff}')

    # Apply Peach accents to features and stats to introduce the warmth.
    # We add a Peach border to .cat or .product-card
    content = re.sub(r'(\.cat\{[^}]*transition:all \.4s)', r'\1; border: 1px solid #F7E7D7', content)
    content = re.sub(r'(\.product-card\{[^}]*transition:all \.35s)', r'\1; border: 1px solid #FFF3E8', content)

    # Highlight Replacements
    content = content.replace('Premium Indian Hardware<br>&amp; Decor Exporter', 'Premium Indian Hardware<br>&amp; <em>Decor</em> Exporter')
    content = content.replace('efficient global trade operations', 'efficient global <em>trade</em> operations')
    content = content.replace('<h2>Seven categories.<br>One reliable partner.</h2>', '<h2>Seven categories.<br>One reliable <em>partner</em>.</h2>')

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
