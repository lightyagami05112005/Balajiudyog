import os, glob

pages_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products"
files = glob.glob(os.path.join(pages_dir, "*.html"))

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the "Sourcing Capabilities" heading with "Product Showcase"
    content = content.replace(
        '<h2 class="h2">Sourcing<br>Capabilities.</h2>',
        '<h2 class="h2">Explore Our<br>Collection.</h2>'
    )
    # Also adjust the lede text to remove "scalable sourcing solutions"
    content = content.replace(
        '<p class="lede">Talk with our experts to discuss custom requirements, volume pricing, and scalable sourcing solutions for this category.</p>',
        '<p class="lede">Talk with our experts to discuss custom requirements, volume pricing, and detailed product specifications for this category.</p>'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Fixed Sourcing Capabilities wording in product pages.")
