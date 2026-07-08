import os
import re

cat_page = r'c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages\products\Furniture Hardware and Locking Mechanism.html'
with open(cat_page, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the first occurrences of any 16x9 product link
match = re.search(r'<a href="items/[a-z0-9-]+-16x9\.html"', html)

if match:
    start_idx = match.start()
    clean_html = html[:start_idx]
    
    # Add back the closing tags and the whatsapp float button
    clean_html += '</div></div>\n<a href="https://wa.me/916290746602?text=Hello%2C%20I%27m%20interested%20in%20your%20Furniture%20Hardware%20%26%20Locking%20Mechanism%20products." target="_blank" class="wa-float">\n  <svg viewBox="0 0 32 32"><path d="M16.004 0h-.008C7.174 0 0 7.176 0 16.004c0 3.5 1.128 6.744 3.046 9.378L1.054 31.29l6.118-1.958A15.907 15.907 0 0016.004 32C24.826 32 32 24.826 32 16.004 32 7.176 24.826 0 16.004 0zm9.302 22.602c-.388 1.092-1.924 1.998-3.148 2.264-.84.178-1.936.32-5.63-1.21-4.726-1.956-7.768-6.756-8.004-7.07-.226-.314-1.904-2.536-1.904-4.836s1.204-3.432 1.632-3.902c.428-.47.936-.588 1.248-.588.312 0 .624.004.898.016.288.014.674-.11 1.054.804.388.936 1.322 3.236 1.438 3.472.116.236.194.51.038.824-.156.314-.234.51-.47.784-.234.274-.494.612-.704.822-.236.236-.482.49-.208.96.274.47 1.22 2.012 2.618 3.26 1.798 1.606 3.314 2.104 3.784 2.34.47.236.744.196 1.018-.118.274-.314 1.176-1.372 1.49-1.842.314-.47.628-.39 1.058-.234.43.156 2.726 1.286 3.196 1.522.468.236.782.352.898.548.116.196.116 1.13-.272 2.224z"/></svg>\n  Chat with us\n</a>\n</body>\n</html>'

    with open(cat_page, 'w', encoding='utf-8') as f:
        f.write(clean_html)
    print("Cleaned up the category page.")
else:
    print("No 16x9 entries found to clean.")
