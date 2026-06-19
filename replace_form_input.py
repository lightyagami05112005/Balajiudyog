import os

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content

    # Replace old select
    old_select_1 = '<select required><option value="">Select country</option><option>Nigeria</option><option>Kenya</option><option>South Africa</option><option>Ghana</option><option>Tanzania</option><option>Other</option></select>'
    # Replace new select
    old_select_2 = '<select required><option value="">Select country</option><option>USA</option><option>UK</option><option>UAE</option><option>Australia</option><option>Canada</option><option>Other</option></select>'
    
    new_input = '<input type="text" placeholder="Your country" required>'
    
    content = content.replace(old_select_1, new_input)
    content = content.replace(old_select_2, new_input)

    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {path}')

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            process_file(os.path.join(root, f))
