import os, re
root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def remove_section(content, regex_pattern):
    return re.sub(regex_pattern, '', content, flags=re.DOTALL)

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
            orig = content
            
            # Remove nav links
            content = re.sub(r'\s*<a[^>]*href=\"[^\"]*Export Markets\.html\"[^>]*>Export Markets</a>', '', content)
            content = re.sub(r'\s*<li><a[^>]*href=\"[^\"]*Export Markets\.html\"[^>]*>Export Markets</a></li>', '', content)
            
            # Remove from category hero meta
            content = re.sub(r'\s*<div class=\"it\"><span>Active global markets</span><b>14</b></div>', '', content)
            
            # Remove af-rel sections in category pages
            content = re.sub(r'<section class=\"af-rel\">.*?</section>', '', content, flags=re.DOTALL)
            
            if filename == 'Balaji Udyog.html':
                # Remove sections africa and markets
                content = re.sub(r'<!-- ==================== AFRICA ==================== -->\s*<section class=\"africa\" id=\"africa\">.*?</section>', '', content, flags=re.DOTALL)
                content = re.sub(r'<!-- ==================== EXPORT MARKETS ==================== -->\s*<section id=\"markets\">.*?</section>', '', content, flags=re.DOTALL)
                
                # Remove stats
                content = re.sub(r'\s*<div class=\"stat\"><div class=\"num\">14<em>\+</em></div><div class=\"lbl\">Global Markets</div></div>', '', content)
                content = re.sub(r'\s*<div class=\"metric reveal\"[^>]*><b>14<em>\+</em></b><small>global markets served</small></div>', '', content)
                
                # Also remove the 'Download Market Guide' from anywhere else just in case it got left behind
                content = re.sub(r'\s*<a href=\"#\" class=\"btn btn-ghost-light\">Download Market Guide <span class=\"arr\"></span></a>', '', content)

                # Hero corner "India Global Trade Corridor"
                content = re.sub(r'\s*<span>India &middot; Global Trade Corridor</span>', '', content)
                content = re.sub(r'\s*<span>India · Global Trade Corridor</span>', '', content)

            if content != orig:
                with open(filepath, 'w', encoding='utf-8') as f: f.write(content)

# Delete Export Markets page
export_market_path = os.path.join(root_dir, 'pages', 'Export Markets.html')
if os.path.exists(export_market_path):
    os.remove(export_market_path)

# Delete other related market pages
for p in ['hardware-exporter-nigeria.html', 'brassware-supplier-kenya.html', 'bathroom-hardware-ghana.html', 'furniture-hardware-tanzania.html']:
    pp = os.path.join(root_dir, 'pages', p)
    if os.path.exists(pp):
        os.remove(pp)
