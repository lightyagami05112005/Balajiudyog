import os
import glob
import re

base_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project"
html_files = glob.glob(os.path.join(base_dir, "pages", "*.html"))
html_files.append(os.path.join(base_dir, "Balaji Udyog.html"))

for filepath in html_files:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove Blog link in navbar
    content = re.sub(r'<a href="Blog\.html">Blog</a>\s*', '', content)
    content = re.sub(r'<a href="pages/Blog\.html">Blog</a>\s*', '', content)
    content = re.sub(r'<a href="Blog\.html" class="active">Blog</a>\s*', '', content)

    # Remove Blog link in footer Quick Links
    content = re.sub(r'<li><a href="Blog\.html">Blog</a></li>\s*', '', content)
    content = re.sub(r'<li><a href="pages/Blog\.html">Blog</a></li>\s*', '', content)

    # Check for a Blog section in the body
    # It might look like <section id="blog">...</section> or <section class="blog">...</section>
    # To be safe, I'll print out any sections that mention "Blog" or "Insights".
    matches = re.finditer(r'<section[^>]*>.*?</section>', content, flags=re.DOTALL)
    for m in matches:
        sec = m.group(0)
        if 'blog-grid' in sec or 'post-img' in sec:
            print(f"Found blog section in {os.path.basename(filepath)}, removing it...")
            content = content.replace(sec, '')
            break
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Delete Blog.html
blog_path = os.path.join(base_dir, "pages", "Blog.html")
if os.path.exists(blog_path):
    os.remove(blog_path)
    print("Deleted Blog.html")

print("Blog section removed from all pages.")
