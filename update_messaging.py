import os, re
root_dir = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    # 1. Update Hero Description (Home page usually)
    content = re.sub(
        r'Direct from the manufacturing hubs of Muradabad, Aligarh and Firozabad, delivering quality products to international markets.',
        'Trusted sourcing and export partner for importers, wholesalers and distributors. Delivering quality products through a reliable supplier network and efficient global trade operations.',
        content
    )
    content = re.sub(
        r'Direct from the manufacturing hubs of Muradabad, Aligarh and Firozabad.*?</p>',
        'Trusted sourcing and export partner for importers, wholesalers and distributors. Delivering quality products through a reliable supplier network and efficient global trade operations.</p>',
        content
    )

    # 2. General removals of specific city hubs globally
    content = content.replace('Origin Muradabad', 'Origin India')
    content = content.replace('Origin Aligarh', 'Origin India')
    content = content.replace('Origin Firozabad', 'Origin India')
    content = content.replace('Origin Aligarh &amp; Delhi NCR', 'Origin India')
    content = content.replace('Origin Aligarh & Delhi NCR', 'Origin India')

    content = content.replace('Category 05 · Muradabad', 'Category 05 · Sourced in India')
    content = content.replace('Category 02 · Aligarh', 'Category 02 · Sourced in India')
    content = content.replace('Category 06 · Firozabad', 'Category 06 · Sourced in India')
    content = content.replace('Category 01 · Aligarh', 'Category 01 · Sourced in India')
    content = content.replace('Category 04 · Muradabad', 'Category 04 · Sourced in India')
    content = content.replace('Category 03 · Aligarh', 'Category 03 · Sourced in India')
    
    content = re.sub(r'<span>Source hub</span><b>Muradabad</b>', '<span>Sourcing</span><b>India</b>', content)
    content = re.sub(r'<span>Source hub</span><b>Aligarh</b>', '<span>Sourcing</span><b>India</b>', content)
    content = re.sub(r'<span>Source hub</span><b>Firozabad</b>', '<span>Sourcing</span><b>India</b>', content)

    content = content.replace('crafted in Muradabad', 'crafted in India')
    content = content.replace('manufactured in Aligarh', 'manufactured in India')
    content = content.replace('crafted in Firozabad', 'crafted in India')
    content = content.replace('hand-finished in Muradabad', 'hand-finished in India')
    content = content.replace('hand-finished in Aligarh', 'hand-finished in India')
    content = content.replace('hand-finished in Firozabad', 'hand-finished in India')
    content = content.replace('from Muradabad', 'from India')
    content = content.replace('from Aligarh', 'from India')
    content = content.replace('from Firozabad', 'from India')

    content = re.sub(r'brassware from Muradabad, locks from Aligarh and chandeliers from Firozabad', 'hardware, decor, and glassware from across India', content)
    content = content.replace("foundries and lock houses of India's craft hubs", "certified manufacturing partners across India")
    content = content.replace("We work with Muradabad's most senior master artisans", "We work with India's most senior master artisans")

    # Product category specific replacements
    content = re.sub(r'from precision-engineering units in Aligarh and the NCR', 'from precision-engineering units across India', content)
    content = re.sub(r'Aligarh has been making locks since 1870\. A 154-year-old craft ecosystem of foundries, key-cutters, and precision-engineering units packed into a 12 km radius — producing more than 75% of India\'s annual lock exports\. We source direct from twelve BIS-certified factories there\.', 'We partner with established manufacturing ecosystems across India, sourcing direct from BIS-certified factories to ensure premium quality.', content)
    content = re.sub(r'Aligarh — India\'s hardware capital\.', 'trusted Indian manufacturers.', content)
    
    content = re.sub(r'<em>from Aligarh\.</em>', '<em>from India.</em>', content)
    content = re.sub(r'<em>from Muradabad\.</em>', '<em>from India.</em>', content)
    content = re.sub(r'<em>from Firozabad\.</em>', '<em>from India.</em>', content)

    # 3. Update About Section
    if filename == 'About.html':
        content = content.replace("Relationships with foundries, not on commission.", "Built on a strong supplier network, not on commission.")
        content = content.replace("factory partnerships in three Indian craft hubs", "a strong supplier network and vendor management expertise")
        content = content.replace("'06 Aligarh ties", "'06 Vendor Network")
        content = content.replace("Direct supply agreements with twelve Aligarh lock manufacturers. Adds hardware to the product line.", "Direct supply agreements with leading hardware manufacturers. Adds hardware to the product line.")
        content = content.replace("'14 Firozabad glass", "'14 Glassware Expansion")
        
        # Replace the entire Hub Strip
        hub_strip_replacement = """<!-- EXPERTISE STRIP -->
<section style="background:var(--paper-2)">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <div class="num">05 / Our Expertise</div>
        <h2 class="h2">Strong supplier network<br>and sourcing.</h2>
      </div>
      <p class="lede">We partner with trusted manufacturers across India, ensuring quality, reliability, and scale for our global buyers.</p>
    </div>

    <div class="hub-strip">
      <div class="hs reveal">
        <div class="ph navy"><img class="img-cover" src="../assets/images/hubs/moradabad/moradabad-aerial.webp?v2026053001" alt="Quality Assurance" width="1200" height="900" loading="lazy" decoding="async"><span class="ph-tag">01</span></div>
        <div class="body"><h4><small>Export Standard</small>Quality Assurance</h4><p>Comprehensive product inspection and testing to meet international standards.</p></div>
      </div>
      <div class="hs reveal" data-d="1">
        <div class="ph dark"><img class="img-cover" src="../assets/images/hubs/aligarh/aligarh-aerial.webp?v2026053001" alt="Product Sourcing Expertise" width="1200" height="900" loading="lazy" decoding="async"><span class="ph-tag">02</span></div>
        <div class="body"><h4><small>Vendor Network</small>Product Sourcing</h4><p>Deep industry knowledge to match buyers with the right manufacturing partners.</p></div>
      </div>
      <div class="hs reveal" data-d="2">
        <div class="ph brass"><img class="img-cover" src="../assets/images/hubs/firozabad/firozabad-aerial.webp?v2026053001" alt="Export Logistics Capabilities" width="1200" height="900" loading="lazy" decoding="async"><span class="ph-tag">03</span></div>
        <div class="body"><h4><small>Supply Chain</small>Export Logistics</h4><p>End-to-end shipment management and documentation for seamless delivery.</p></div>
      </div>
    </div>
  </div>
</section>"""
        content = re.sub(r'<!-- HUB STRIP -->.*?<!-- CTA BAND -->', hub_strip_replacement + '\n\n<!-- CTA BAND -->', content, flags=re.DOTALL)
        
    # 4. Update Export Services section
    if filename == 'Export Services.html':
        content = re.sub(r'<div class="mono-lbl">Logistics</div>\s*<h2>Container shipping.*?</h2>\s*<ul class="feats">.*?</ul>', r'<div class="mono-lbl">Logistics</div><h2>Logistics<br><em>Support.</em></h2><ul class="feats"><li>Ocean freight &amp; container loading</li><li>Direct vessels to global ports</li><li>Transhipment management</li><li>FOB &middot; CIF &middot; CFR terms</li><li>USD &amp; EUR invoicing</li></ul>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mono-lbl">Private Label</div>\s*<h2>OEM.*?</h2>\s*<ul class="feats">.*?</ul>', r'<div class="mono-lbl">Sourcing</div><h2>Product<br><em>Sourcing.</em></h2><ul class="feats"><li>Extensive supplier network</li><li>Vendor coordination</li><li>Price negotiation &amp; locking</li><li>Sampling within 14 days</li><li>Exclusive territory contracts</li></ul>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mono-lbl">Packaging</div>\s*<h2>Export-grade.*?</h2>\s*<ul class="feats">.*?</ul>', r'<div class="mono-lbl">Packaging</div><h2>Packaging<br><em>Solutions.</em></h2><ul class="feats"><li>Corrugated 5-ply outers</li><li>Humidity-resistant linings</li><li>Anti-rust treatment on metals</li><li>Foam &amp; air-cell for glass</li><li>FUMIGATED wooden crates</li><li>ISPM-15 compliant</li></ul>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mono-lbl">Compliance</div>\s*<h2>Documentation.*?</h2>\s*<ul class="feats">.*?</ul>', r'<div class="mono-lbl">Compliance</div><h2>Export<br><em>Documentation.</em></h2><ul class="feats"><li>Commercial invoice &amp; packing list</li><li>Bill of Lading (clean / received)</li><li>Certificate of Origin</li><li>Quality Inspection &amp; Certification</li><li>Fumigation certificates</li><li>Pre-shipment inspection reports</li></ul>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mono-lbl">Volume</div>\s*<h2>Bulk order.*?</h2>\s*<ul class="feats">.*?</ul>', r'<div class="mono-lbl">Vendor</div><h2>Vendor<br><em>Coordination.</em></h2><ul class="feats"><li>Multi-factory consolidation</li><li>Mixed-category containers</li><li>Single PO across network</li><li>Quality Inspection routines</li><li>Production timeline tracking</li><li>Inventory hold &amp; release</li></ul>', content, flags=re.DOTALL)
        content = re.sub(r'<div class="mono-lbl">Last Mile</div>\s*<h2>International.*?</h2>\s*<ul class="feats">.*?</ul>', r'<div class="mono-lbl">Shipment</div><h2>Shipment<br><em>Management.</em></h2><ul class="feats"><li>Port-to-warehouse delivery</li><li>Customs clearance support</li><li>In-country liaison teams</li><li>Door-to-door tracking</li><li>Inland freight management</li><li>Insurance &amp; claims handling</li></ul>', content, flags=re.DOTALL)
        
        # Replace the descriptive paragraphs next to these to match
        content = re.sub(r'<p class="desc">Build your house brand on Indian manufacturing.*?</div>', r'<p class="desc">Connect with trusted manufacturing partners across India. We coordinate the entire vendor network, from initial sampling to final production runs, ensuring quality and consistency.</p><div class="visual ph paper"><img class="img-cover" src="../assets/images/export/branded-packaging-oem.webp" alt="Product Sourcing &amp; Vendor Coordination" width="1200" height="900" loading="lazy" decoding="async"><span class="ph-tag">Sourcing</span></div>', content, flags=re.DOTALL)
        content = re.sub(r'<p class="desc">One PO can include hardware, decor, and glassware from across India.*?</div>', r'<p class="desc">We handle all vendor coordination for you. Consolidate your shipments from multiple factories into a single full-container load, managed under one PO and a unified tracking system.</p><div class="visual ph brass"><img class="img-cover" src="../assets/images/export/consolidation-warehouse.webp" alt="Consolidation warehouse for full-container loads" width="1600" height="900" loading="lazy" decoding="async"><span class="ph-tag">Vendor</span></div>', content, flags=re.DOTALL)

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            process_file(os.path.join(dirpath, filename))
