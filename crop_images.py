import os
from PIL import Image

base_img_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\assets\images\products"
items_img_dir = os.path.join(base_img_dir, "items")
items_html_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\items"

os.makedirs(items_img_dir, exist_ok=True)

mappings = [
    {
        "source": r"brassware_steel_cutleries\page_5.jpg",
        "dest": "bc-16p.jpg",
        "html": "premium-brass-cutlery-set.html"
    },
    {
        "source": r"brassware_steel_cutleries\page_6.jpg",
        "dest": "ss-gld-spn.jpg",
        "html": "gold-plated-stainless-steel-spoons.html"
    },
    {
        "source": r"brassware_steel_cutleries\page_7.jpg",
        "dest": "hb-sal-srv.jpg",
        "html": "hammered-brass-salad-servers.html"
    },
    {
        "source": r"brassware_steel_cutleries\page_8.jpg",
        "dest": "vc-din-frk.jpg",
        "html": "vintage-copper-dinner-forks.html"
    },
    {
        "source": r"lighting\page_2.jpg",
        "dest": "lt-abc-01.jpg",
        "html": "antique-brass-chandelier.html"
    },
    {
        "source": r"lighting\page_3.jpg",
        "dest": "lt-ipl-02.jpg",
        "html": "industrial-pendant-lamp-shade.html"
    },
    {
        "source": r"lighting\page_4.jpg",
        "dest": "lt-dgw-03.jpg",
        "html": "decorative-glass-wall-sconce.html"
    },
    {
        "source": r"lighting\page_5.jpg",
        "dest": "lt-mmt-04.jpg",
        "html": "modern-minimalist-table-lamp.html"
    }
]

for m in mappings:
    src_path = os.path.join(base_img_dir, m["source"])
    if not os.path.exists(src_path):
        print(f"Source not found: {src_path}")
        continue
        
    try:
        img = Image.open(src_path)
        w, h = img.size
        # Crop center 80% to avoid margins/headers
        left = int(w * 0.1)
        top = int(h * 0.15) # slightly lower to skip headers
        right = int(w * 0.9)
        bottom = int(h * 0.85)
        
        cropped = img.crop((left, top, right, bottom))
        
        dest_path = os.path.join(items_img_dir, m["dest"])
        cropped.save(dest_path)
        print(f"Cropped and saved {m['dest']}")
        
        # Update HTML file
        html_path = os.path.join(items_html_dir, m["html"])
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
                
            # Replace placeholder image with new cropped image
            # The placeholder path was: ../../../assets/images/placeholder.jpg
            # New path: ../../../assets/images/products/items/{dest}
            new_img_src = f"../../../assets/images/products/items/{m['dest']}"
            html_content = html_content.replace("../../../assets/images/placeholder.jpg", new_img_src)
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Updated HTML: {m['html']}")
            
    except Exception as e:
        print(f"Error processing {src_path}: {e}")

# Now update the category pages to also point to the new images instead of the placeholder
cat_html_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products"
cat_files = ["Stainless Steel and Brass Cutleries.html", "Lighting.html"]

for cf in cat_files:
    cf_path = os.path.join(cat_html_dir, cf)
    if os.path.exists(cf_path):
        with open(cf_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        for m in mappings:
            # Category pages used ../../assets/images/placeholder.jpg
            new_img_src = f"../../assets/images/products/items/{m['dest']}"
            
            # Find the specific block for this product and replace its image
            # Wait, easier to just run update_category_pages.py again!
            pass 

print("Finished cropping and updating placeholders.")
