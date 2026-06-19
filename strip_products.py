import os, glob, re

pages_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products"
files = glob.glob(os.path.join(pages_dir, "*.html"))

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove cat-intro through bulk
    pattern_middle = r'<section class="cat-intro">.*?</section>\s*<section class="inquiry-band">'
    content = re.sub(r'<section class="cat-intro">.*?(?=<section class="inquiry-band">)', '', content, flags=re.DOTALL)
    
    # Remove rel (Related categories)
    content = re.sub(r'<section class="rel">.*?</section>\s*<footer>', '<footer>', content, flags=re.DOTALL)
    
    # Update hero actions
    hero_actions_pattern = r'<div class="actions reveal" data-d="3">.*?</div>'
    hero_actions_replacement = r'<div class="actions reveal" data-d="3">\n          <a href="https://wa.me/916290746602?text=Hello%20Balaji%20Udyog%2C%20I%20would%20like%20to%20request%20the%20catalogue." target="_blank" class="btn btn-wa">Request Catalogue on WhatsApp</a>\n        </div>'
    content = re.sub(hero_actions_pattern, hero_actions_replacement, content, flags=re.DOTALL)
    
    # Update inquiry-band actions and text
    inquiry_band_pattern = r'<section class="inquiry-band">.*?</section>'
    
    inquiry_band_replacement = """<section class="inquiry-band">
  <div class="wrap">
    <div>
      <div class="eyebrow light">WhatsApp \u00b7 24/7</div>
      <h2 class="h2" style="margin-top:14px">Request the full catalogue.</h2>
      <p>Our export team responds in minutes on WhatsApp with the complete product catalogue, pricing, and MOQ details.</p>
    </div>
    <div class="actions">
      <a href="https://wa.me/916290746602?text=Hello%20Balaji%20Udyog%2C%20I%20would%20like%20to%20request%20the%20catalogue." target="_blank" class="btn btn-wa">Request Catalogue on WhatsApp</a>
    </div>
  </div>
</section>"""
    
    content = re.sub(inquiry_band_pattern, inquiry_band_replacement, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Stripped product pages down to hero and WhatsApp catalogue request.")
