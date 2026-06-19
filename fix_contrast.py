import os, re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def fix_css(content):
    # 1. Inject CSS variables
    if '--dark-h' not in content and ':root{' in content:
        content = content.replace(':root{', ':root{\n  --dark-h: #FFFFFF;\n  --dark-p: #E5E7EB;\n  --dark-muted: #CBD5E1;\n  --dark-gold: #D4AF37;\n  --dark-gold-light: #F5D76E;')
    
    # Update .on-dark classes
    content = re.sub(r'\.on-dark\{color:var\(--paper\)\}', '.on-dark{color:var(--dark-p)}', content)
    content = re.sub(r'\.on-dark h1,\.on-dark h2,\.on-dark h3,\.on-dark h4\{color:var\(--paper\)\}', '.on-dark h1,.on-dark h2,.on-dark h3,.on-dark h4{color:var(--dark-h)}', content)
    content = re.sub(r'\.on-dark \.lede\{color:rgba\([^)]+\)\}', '.on-dark .lede{color:var(--dark-p)}', content)
    
    # 2. Fix specific dark sections globally
    
    # Headings
    content = re.sub(r'color:var\(--paper\)(?!;[ \n]*background)', 'color:var(--dark-h)', content)
    # Be careful not to replace button text colors if we can avoid it, but btn uses --navy for text usually
    
    # Specific elements
    content = re.sub(r'color:rgba\(245,242,236,\.[0-9]+\)', 'color:var(--dark-p)', content)
    
    # Ticker
    content = re.sub(r'\.ticker-track span\{[^\}]*?color:var\(--dark-p\)[^\}]*?\}', r'.ticker-track span{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--dark-muted)}', content)
    content = re.sub(r'\.ticker-track span\{[^\}]*?color:rgba[^}]+\}', r'.ticker-track span{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--dark-muted)}', content)
    
    # Footer
    content = re.sub(r'\.foot-brand p\{[^\}]*?\}', r'.foot-brand p{color:var(--dark-p);margin-top:18px;font-size:14px;max-width:36ch;line-height:1.65}', content)
    content = re.sub(r'\.foot-col h4\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.foot-col h4{font-family:var(--mono);font-size:11px;letter-spacing:.22em;color:var(--dark-gold);text-transform:uppercase;margin-bottom:22px;font-weight:500}', content)
    content = re.sub(r'\.foot-col a\{[^\}]*?\}', r'.foot-col a{font-size:14px;color:var(--dark-p);transition:color .2s}', content)
    content = re.sub(r'\.foot-col \.addr\{[^\}]*?\}', r'.foot-col .addr{font-size:14px;color:var(--dark-p);line-height:1.7;font-style:normal}', content)
    content = re.sub(r'\.foot-bottom small\{[^\}]*?\}', r'.foot-bottom small{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;color:var(--dark-muted);text-transform:uppercase}', content)
    
    # Hubs section in Balaji Udyog
    content = re.sub(r'\.hubs\{background:var\(--navy\);color:var\(--paper\)\}', r'.hubs{background:var(--navy);color:var(--dark-p)}', content)
    content = re.sub(r'\.hubs \.section-head \.num\{color:var\(--gold\)\}', r'.hubs .section-head .num{color:var(--dark-gold)}', content)
    
    # In Balaji Udyog inline CSS, fix hubs text specifically if inherited
    if '.hubs .section-head h2' not in content and '.hubs{' in content:
        content = content.replace('.hubs{', '.hubs h2, .hubs h3, .hubs h4 { color: var(--dark-h); }\n  .hubs .lede, .hubs p { color: var(--dark-p); }\n  .hubs .hub-list li small { color: var(--dark-gold); }\n  .hubs .hub-tag { color: var(--dark-gold); border-color: var(--dark-gold); }\n  .hubs .hub-list li { border-top-color: rgba(255,255,255,0.1); }\n  .hubs{')
        
    # Inquiry band
    content = re.sub(r'\.inquiry-band h2\{[^\}]*?\}', r'.inquiry-band h2{color:var(--dark-h)}', content)
    content = re.sub(r'\.inquiry-band p\{[^\}]*?\}', r'.inquiry-band p{color:var(--dark-p);max-width:50ch;margin-top:18px;font-size:16px;line-height:1.6}', content)
    
    # About Stats
    content = re.sub(r'\.strip-stats \.item \.num\{[^\}]*?color:var\(--dark-h\)[^\}]*?\}', r'.strip-stats .item .num{font-family:var(--display);font-size:clamp(36px,3.4vw,52px);color:var(--dark-h);font-weight:500;letter-spacing:-.02em}', content)
    content = re.sub(r'\.strip-stats \.item \.num em\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.strip-stats .item .num em{color:var(--dark-gold-light);font-style:normal;font-weight:300}', content)
    content = re.sub(r'\.strip-stats \.item \.lbl\{[^\}]*?\}', r'.strip-stats .item .lbl{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--dark-muted);margin-top:6px}', content)
    
    # About Values
    content = re.sub(r'\.values h2\{[^\}]*?\}', r'.values h2{color:var(--dark-h)}', content)
    content = re.sub(r'\.val \.num\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.val .num{font-family:var(--mono);font-size:11px;letter-spacing:.22em;color:var(--dark-gold)}', content)
    content = re.sub(r'\.val h3\{[^\}]*?color:var\(--dark-h\)[^\}]*?\}', r'.val h3{color:var(--dark-h);font-size:24px;font-weight:500;letter-spacing:-.01em}', content)
    content = re.sub(r'\.val p\{[^\}]*?\}', r'.val p{color:var(--dark-p);font-size:14.5px;line-height:1.65}', content)
    
    # Export Services Docs
    content = re.sub(r'\.docs \.d \.ab\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.docs .d .ab{font-family:var(--display);font-size:32px;color:var(--dark-gold-light);font-weight:300;letter-spacing:-.02em}', content)
    content = re.sub(r'\.docs \.d h4\{[^\}]*?color:var\(--dark-h\)[^\}]*?\}', r'.docs .d h4{color:var(--dark-h);font-size:16px;font-weight:500}', content)
    content = re.sub(r'\.docs \.d p\{[^\}]*?\}', r'.docs .d p{color:var(--dark-p);font-size:13px;line-height:1.55}', content)

    # Trust India
    content = re.sub(r'\.trust-india h2\{[^\}]*?\}', r'.trust-india h2{color:var(--dark-h)}', content)
    content = re.sub(r'\.ti \.tn\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.ti .tn{font-family:var(--mono);font-size:11px;letter-spacing:.18em;color:var(--dark-gold);padding-top:3px}', content)
    content = re.sub(r'\.ti h4\{[^\}]*?color:var\(--dark-h\)[^\}]*?\}', r'.ti h4{color:var(--dark-h);font-size:17px;font-weight:500;letter-spacing:-.01em}', content)
    content = re.sub(r'\.ti p\{[^\}]*?\}', r'.ti p{color:var(--dark-p);font-size:14px;line-height:1.6;margin-top:6px}', content)

    # Hero meta / generic hero
    content = re.sub(r'\.hero h1,\.hero h2,\.hero h3,\.hero h4\{color:var\(--dark-h\)\}', r'.hero h1,.hero h2,.hero h3,.hero h4{color:var(--dark-h)}', content)
    content = re.sub(r'\.hero \.lede\{[^\}]*?\}', r'.hero .lede{font-size:clamp(16px,1.25vw,20px);max-width:60ch;color:var(--dark-p)}', content)
    content = re.sub(r'\.hero-meta \.num\{[^\}]*?color:var\(--dark-h\)[^\}]*?\}', r'.hero-meta .num{font-family:var(--display);font-size:clamp(28px,2.6vw,40px);color:var(--dark-h);font-weight:500;letter-spacing:-.02em}', content)
    content = re.sub(r'\.hero-meta \.num em\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.hero-meta .num em{color:var(--dark-gold-light);font-style:normal;font-weight:300}', content)
    content = re.sub(r'\.hero-meta \.lbl\{[^\}]*?\}', r'.hero-meta .lbl{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--dark-muted)}', content)

    # Nav
    content = re.sub(r'\.logo-text b\{[^\}]*?color:var\(--dark-h\)[^\}]*?\}', r'.logo-text b{font-family:var(--display);font-weight:600;font-size:15px;letter-spacing:.08em;color:var(--dark-h)}', content)
    content = re.sub(r'\.logo-text small\{[^\}]*?color:var\(--gold\)[^\}]*?\}', r'.logo-text small{font-family:var(--mono);font-size:9px;letter-spacing:.28em;color:var(--dark-gold);text-transform:uppercase;margin-top:2px}', content)
    content = re.sub(r'\.nav-menu a\{[^\}]*?\}', r'.nav-menu a{font-size:13px;color:var(--dark-p);letter-spacing:.03em;position:relative;padding:6px 0;transition:color .2s}', content)
    content = re.sub(r'\.nav-menu a:hover,\.nav-menu a\.active\{color:var\(--dark-h\)\}', r'.nav-menu a:hover,.nav-menu a.active{color:var(--dark-h)}', content)
    
    # Eyebrow
    content = re.sub(r'\.eyebrow\.light\{color:var\(--gold-soft\)\}', r'.eyebrow.light{color:var(--dark-gold-light)}', content)

    return content

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.css'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = fix_css(content)
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
                new_style = fix_css(style_match.group(1))
                content = content[:style_match.start(1)] + new_style + content[style_match.end(1):]
            
            # Make sure .hubs has .on-dark if we didn't add it
            content = content.replace('<section class="hubs" id="about">', '<section class="hubs on-dark" id="about">')
            
            if content != orig:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

