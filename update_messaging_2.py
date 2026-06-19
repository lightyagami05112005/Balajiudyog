import os, re
root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    # Catch any leftover Origin tags
    content = re.sub(r'Origin India &amp; Muradabad', 'Origin India', content)
    content = re.sub(r'Origin India &amp; Aligarh', 'Origin India', content)
    content = re.sub(r'Origin India &amp; Firozabad', 'Origin India', content)
    content = re.sub(r'Origin India & Muradabad', 'Origin India', content)
    content = re.sub(r'Origin India & Aligarh', 'Origin India', content)
    content = re.sub(r'Origin India & Firozabad', 'Origin India', content)
    
    # <b>Aligarh</b>, <b>Muradabad</b>, <b>Firozabad</b> inside pdp-chip
    content = re.sub(r'<b>Aligarh</b>', '<b>India</b>', content)
    content = re.sub(r'<b>Muradabad</b>', '<b>India</b>', content)
    content = re.sub(r'<b>Firozabad</b>', '<b>India</b>', content)

    # Any random mentions
    content = re.sub(r'\bMuradabad\b', 'India', content)
    content = re.sub(r'\bAligarh\b', 'India', content)
    content = re.sub(r'\bFirozabad\b', 'India', content)

    # Clean up awkward phrases caused by replacement like "India's most senior master artisans" (already good)
    # "India — India's hardware capital" -> "trusted Indian manufacturers"
    content = re.sub(r'India — India\'s hardware capital', 'trusted Indian manufacturers', content)
    # "Origin India &amp; Delhi NCR" -> "Origin India"
    content = re.sub(r'Origin India &amp; Delhi NCR', 'Origin India', content)
    
    # "India has been making locks since 1870."
    content = re.sub(r'India has been making locks since 1870\. A 154-year-old craft ecosystem.*?\.', 'We partner with established manufacturing ecosystems across India, sourcing direct from BIS-certified factories to ensure premium quality.', content)

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            process_file(os.path.join(dirpath, filename))
