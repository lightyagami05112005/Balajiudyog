import os, re

root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'
balaji_html = os.path.join(root_dir, 'Balaji Udyog.html')
about_html = os.path.join(root_dir, 'pages', 'About.html')

# 1. Process Balaji Udyog.html
with open(balaji_html, 'r', encoding='utf-8') as f:
    b_content = f.read()

# Remove HTML section
html_pattern = r'<!-- ==================== OUR EXPERTISE ==================== -->\s*<section class="hubs on-dark" id="about">.*?</section>\s*'
b_content = re.sub(html_pattern, '', b_content, flags=re.DOTALL)

# Remove CSS section
css_pattern = r'/\* ---------- HUBS ---------- \*/.*?/\* ---------- WHY US ---------- \*/'
b_content = re.sub(css_pattern, '/* ---------- WHY US ---------- */', b_content, flags=re.DOTALL)

with open(balaji_html, 'w', encoding='utf-8') as f:
    f.write(b_content)


# 2. Process About.html
with open(about_html, 'r', encoding='utf-8') as f:
    a_content = f.read()

# Remove HTML section
a_pattern = r'<!-- EXPERTISE STRIP -->\s*<section style="background:var\(--paper-2\)">.*?</section>\s*'
a_content = re.sub(a_pattern, '', a_content, flags=re.DOTALL)

with open(about_html, 'w', encoding='utf-8') as f:
    f.write(a_content)

print("Removed sourcing capability sections from both pages.")
