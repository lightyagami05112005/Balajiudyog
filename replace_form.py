import os

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content

    content = content.replace(
        '<option>Nigeria</option><option>Kenya</option><option>South Africa</option><option>Ghana</option><option>Tanzania</option>',
        '<option>USA</option><option>UK</option><option>UAE</option><option>Australia</option><option>Canada</option>'
    )
    
    content = content.replace('placeholder="e.g. Lagos, Mombasa"', 'placeholder="e.g. New York, Dubai"')
    
    content = content.replace('placeholder="+234 …"', 'placeholder="+1 …"')
    content = content.replace('placeholder="+234 ..."', 'placeholder="+1 ..."')

    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {path}')

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            process_file(os.path.join(root, f))
