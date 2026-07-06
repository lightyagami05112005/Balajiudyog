import os, glob, re

base_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            original_content = content
            
            # 1. Update dropdown
            pattern = re.compile(r'(<a href="([^"]*?)Lighting\.html"[^>]*>.*?</a>)(\s*</div>\s*</div>\s*<a href="[^"]*Contact\.html")', re.DOTALL)
            def dropdown_repl(m):
                prefix = m.group(2)
                # Ensure we don't add it twice
                if 'Decorative Glassware.html' in m.group(1):
                    return m.group(0)
                return m.group(1) + f'\n          <a href="{prefix}Decorative Glassware.html"><span>Decorative Glassware</span><small>05</small></a>' + m.group(3)
                
            content = pattern.sub(dropdown_repl, content)

            # Let's try a different regex if the first one doesn't match
            pattern2 = re.compile(r'(<a href="([^"]*?)Lighting\.html".*?</a>)(\s*</div>)', re.DOTALL)
            def dropdown_repl2(m):
                prefix = m.group(2)
                # Ensure we don't add it twice
                if 'Decorative Glassware.html' in m.group(1):
                    return m.group(0)
                return m.group(1) + f'\n          <a href="{prefix}Decorative Glassware.html"><span>Decorative Glassware</span><small>05</small></a>' + m.group(3)
                
            # Actually, to be safe, only replace the dropdown panel if it doesn't already contain Decorative Glassware
            if 'Decorative Glassware.html' not in content:
                content = pattern2.sub(dropdown_repl2, content)
            
            # 2. Update footer
            # The footer looks like: <li><a href="products/Lighting.html">Lighting</a></li>\n      </ul></div>
            footer_pattern = re.compile(r'(<li><a href="([^"]*?)Lighting\.html"[^>]*>Lighting</a></li>)(\s*</ul>)', re.DOTALL)
            def footer_repl(m):
                prefix = m.group(2)
                if 'Decorative Glassware.html' in m.group(1):
                    return m.group(0)
                return m.group(1) + f'\n        <li><a href="{prefix}Decorative Glassware.html">Decorative Glassware</a></li>' + m.group(3)
                
            if 'Decorative Glassware' not in content.split('foot-col')[1] if 'foot-col' in content else True:
                content = footer_pattern.sub(footer_repl, content)
            
            # 3. Update Products.html category count and add article
            if os.path.basename(path) == "Products.html":
                # Update category count
                content = content.replace("Four categories.<br><em>One reliable partner.</em>", "Five categories.<br><em>One reliable partner.</em>")
                content = content.replace("04 / 04 categories", "05 / 05 categories")
                content = content.replace("<b>Categories ·</b> 4", "<b>Categories ·</b> 5")
                
                # Check if we already added Decorative Glassware to the list
                if '05 · Glassware' not in content:
                    # Find the end of the last article (Lighting)
                    article_pattern = re.compile(r'(<article class="pcat reveal".*?04 · Lighting.*?</article>)(\s*</div>\s*</section>)', re.DOTALL)
                    new_article = """
    <article class="pcat reveal">
      <div class="visual">
        <div class="ph glass"><img class="img-cover" src="../assets/images/categories/glassware-hero.jpg" alt="Decorative Glassware" width="1200" height="900" loading="lazy" decoding="async"></div>
        <span class="corner">05 · Glassware</span>
      </div>
      <div>
        <div class="mono-lbl">Category 05</div>
        <h2>Decorative Glassware<br><em>elegant designs.</em></h2>
        <p>A curated collection of decorative vases, bowls, and statement glassware crafted for global export markets.</p>
        <div class="actions">
          <a href="products/Decorative Glassware.html" class="btn btn-ghost">View category <span class="arr"></span></a>
          <a href="Contact.html" class="btn btn-gold">Request quote <span class="arr"></span></a>
        </div>
      </div>
    </article>"""
                    def article_repl(m):
                        return m.group(1) + new_article + m.group(2)
                    content = article_pattern.sub(article_repl, content)

            if content != original_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated {path}")
