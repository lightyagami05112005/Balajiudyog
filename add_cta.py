import os

files_to_update = [
    'Bathroom Fittings and Accessories.html',
    'Furniture Hardware and Locking Mechanism.html',
    'Stainless Steel and Brass Cutleries.html'
]
base_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products'

cta_html = '''
<div class="wa-cta-section wrap" style="margin: 60px auto; text-align: center; background: #25d366; padding: 50px 20px; border-radius: 12px; color: #fff;">
<h2 style="font-family: var(--display); font-size: 32px; font-weight: 600; margin-bottom: 15px;">Need help with pricing or shipping?</h2>
<p style="font-size: 16px; margin-bottom: 30px; opacity: 0.9;">Our export team is available on WhatsApp to answer your queries instantly.</p>
<a href="https://wa.me/916290746602" style="display: inline-flex; align-items: center; gap: 10px; background: #fff; color: #25d366; padding: 15px 30px; border-radius: 50px; font-weight: 600; font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em; text-decoration: none;" target="_blank">
<svg style="width: 24px; height: 24px; fill: currentColor;" viewbox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"></path></svg>
Chat on WhatsApp
</a>
</div>
'''

for file in files_to_update:
    path = os.path.join(base_dir, file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'wa-cta-section' not in content:
        # Find the end of the grid section, which is typically before the floating whatsapp button.
        if '<a class="wa-float"' in content:
            content = content.replace('<a class="wa-float"', cta_html + '<a class="wa-float"')
        elif 'class="wa-float"' in content:
            # specifically for bathroom fittings
            content = content.replace('<a href="https://wa.me/916290746602?text=', cta_html + '<a href="https://wa.me/916290746602?text=')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {file}')
    else:
        print(f'{file} already has CTA section')
