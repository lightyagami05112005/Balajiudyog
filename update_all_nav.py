import os
import glob
import re

pages_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages"
html_files = glob.glob(os.path.join(pages_dir, "*.html"))

old_dropdown = """<div class="dropdown-panel">
          <a href="products/Furniture Hardware.html"><span>Furniture Hardware</span><small>01</small></a>
          <a href="products/Locks - Hardware.html"><span>Locks &amp; Hardware</span><small>02</small></a>
          <a href="products/Bathroom Hardware.html"><span>Bathroom Hardware</span><small>03</small></a>
          <a href="products/Brassware.html"><span>Brassware</span><small>04</small></a>
          <a href="products/Metal Art Ware.html"><span>Metal Art Ware</span><small>05</small></a>
          <a href="products/Glassware.html"><span>Glassware</span><small>06</small></a>
          <a href="products/Home Decor.html"><span>Home Decor</span><small>07</small></a>
        </div>"""

new_dropdown = """<div class="dropdown-panel">
          <a href="products/Stainless Steel and Brass Cutleries.html"><span>Stainless Steel &amp; Brass Cutleries</span><small>01</small></a>
          <a href="products/Bathroom Fittings and Accessories.html"><span>Bathroom Fittings &amp; Accessories</span><small>02</small></a>
          <a href="products/Furniture Hardware and Locking Mechanism.html"><span>Furniture Hardware &amp; Locking Mechanism</span><small>03</small></a>
        </div>"""

old_footer = """<div class="foot-col"><h4>Product Categories</h4><ul>
        <li><a href="products/Furniture Hardware.html">Furniture Hardware</a></li><li><a href="products/Locks - Hardware.html">Locks &amp; Hardware</a></li><li><a href="products/Bathroom Hardware.html">Bathroom Hardware</a></li><li><a href="products/Brassware.html">Brassware</a></li><li><a href="products/Metal Art Ware.html">Metal Art Ware</a></li><li><a href="products/Glassware.html">Glassware</a></li><li><a href="products/Home Decor.html">Home Decor</a></li>
      </ul></div>"""

new_footer = """<div class="foot-col"><h4>Product Categories</h4><ul>
        <li><a href="products/Stainless Steel and Brass Cutleries.html">Stainless Steel &amp; Brass Cutleries</a></li>
        <li><a href="products/Bathroom Fittings and Accessories.html">Bathroom Fittings &amp; Accessories</a></li>
        <li><a href="products/Furniture Hardware and Locking Mechanism.html">Furniture Hardware &amp; Locking Mechanism</a></li>
      </ul></div>"""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace dropdown and footer
    content = content.replace(old_dropdown, new_dropdown)
    content = content.replace(old_footer, new_footer)
    
    # Special replacements for Products.html
    if os.path.basename(filepath) == "Products.html":
        content = content.replace("Seven categories.<br><em>One reliable partner.</em>", "Three categories.<br><em>One reliable partner.</em>")
        content = content.replace("07 / 07 categories", "03 / 03 categories")
        content = content.replace("<b>Categories ·</b> 7", "<b>Categories ·</b> 3")
        
        # Replace the entire <section class="pcat-list">...</section>
        new_pcat_list = """<section class="pcat-list">
  <div class="wrap">
    <article class="pcat reveal">
      <div class="visual">
        <div class="ph paper bright"><img class="img-cover" src="../assets/images/categories/brassware_cutlery_hero.png" alt="Stainless Steel & Brass Cutleries" width="1200" height="900" loading="lazy" decoding="async"></div>
        <span class="corner">01 · Cutleries</span>
      </div>
      <div>
        <div class="mono-lbl">Category 01</div>
        <h2>Stainless Steel &amp; Brass Cutleries<br><em>premium range.</em></h2>
        <p>High-quality cutleries manufactured with precision. Perfect for hospitality and premium retail markets globally.</p>
        <div class="actions">
          <a href="products/Stainless Steel and Brass Cutleries.html" class="btn btn-ghost">View category <span class="arr"></span></a>
          <a href="Contact.html" class="btn btn-gold">Request quote <span class="arr"></span></a>
        </div>
      </div>
    </article>

    <article class="pcat reveal">
      <div class="visual">
        <div class="ph dark"><img class="img-cover" src="../assets/images/categories/bathroom_fittings_hero.png" alt="Bathroom Fittings & Accessories" width="1200" height="900" loading="lazy" decoding="async"></div>
        <span class="corner">02 · Bath</span>
      </div>
      <div>
        <div class="mono-lbl">Category 02</div>
        <h2>Bathroom Fittings &amp; Accessories<br><em>luxury finish.</em></h2>
        <p>Premium bathroom hardware and accessories. Sourced from the finest brass foundries in India for global export.</p>
        <div class="actions">
          <a href="products/Bathroom Fittings and Accessories.html" class="btn btn-ghost">View category <span class="arr"></span></a>
          <a href="Contact.html" class="btn btn-gold">Request quote <span class="arr"></span></a>
        </div>
      </div>
    </article>

    <article class="pcat reveal">
      <div class="visual">
        <div class="ph glass"><img class="img-cover" src="../assets/images/categories/furniture_hardware_hero.png" alt="Furniture Hardware & Locking Mechanism" width="1200" height="900" loading="lazy" decoding="async"></div>
        <span class="corner">03 · Hardware</span>
      </div>
      <div>
        <div class="mono-lbl">Category 03</div>
        <h2>Furniture Hardware &amp; Locking Mechanism<br><em>reliable security.</em></h2>
        <p>Robust and durable hardware for cabinetry, doors, and furniture. Precision engineered for international standards.</p>
        <div class="actions">
          <a href="products/Furniture Hardware and Locking Mechanism.html" class="btn btn-ghost">View category <span class="arr"></span></a>
          <a href="Contact.html" class="btn btn-gold">Request quote <span class="arr"></span></a>
        </div>
      </div>
    </article>
  </div>
</section>"""
        # use regex to replace the block
        content = re.sub(r'<section class="pcat-list">.*?</section>', new_pcat_list, content, flags=re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated navigation, footer, and Products.html layout!")
