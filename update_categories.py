import os, glob, re

pages_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products"
files = glob.glob(os.path.join(pages_dir, "*.html"))

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove SKUs from meta
    content = re.sub(r'<div class="it">\s*<span>SKUs in catalogue.*?</div>', '', content, flags=re.DOTALL|re.IGNORECASE)
    
    # 2. Update .show section heading
    # We find `<section class="show">` and its `.section-head`
    pattern_head = r'(<section class="show">\s*<div class="wrap">\s*<div class="section-head reveal">)(.*?)(</div>\s*<div class="show-grid">)'
    replacement_head = r'\1\n      <div><div class="num">/ Category Range</div><h2 class="h2">Sourcing<br>Capabilities.</h2></div>\n      <p class="lede">Talk with our experts to discuss custom requirements, volume pricing, and scalable sourcing solutions for this category.</p>\n    \3'
    content = re.sub(pattern_head, replacement_head, content, flags=re.DOTALL)
    
    # 3. Clean product grid HTML inside .show-grid
    # Find everything inside <div class="show-grid"> ... </section>
    def clean_grid(match):
        grid_html = match.group(0)
        # Remove <span class="ph-tag">SKU...</span>
        grid_html = re.sub(r'<span class="ph-tag">SKU-.*?</span>', '', grid_html, flags=re.IGNORECASE)
        # Remove <small>SKU...</small>
        grid_html = re.sub(r'<small>SKU-.*?</small>', '', grid_html, flags=re.IGNORECASE)
        # Remove <div class="row">...</div>
        grid_html = re.sub(r'<div class="row">.*?</div>', '', grid_html, flags=re.DOTALL)
        return grid_html

    # Only apply to the show-grid section to avoid modifying other parts of the page by accident
    content = re.sub(r'<div class="show-grid">.*?</section>', clean_grid, content, flags=re.DOTALL)
    
    # 4. Inject script tag
    if 'inquiry-modal.js' not in content:
        content = content.replace('</body>', '  <script src="../../assets/inquiry-modal.js" defer></script>\n</body>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated all category pages!")
