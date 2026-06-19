import os

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content

    # Remove inline onclick from burger divs (fix double-toggle)
    content = content.replace(
        '<div class="burger" onclick="document.getElementById(\'nav\').classList.toggle(\'nav-open\')">',
        '<div class="burger">'
    )

    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {path}')

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            process_file(os.path.join(root, f))
