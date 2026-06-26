import os
import glob

pages_dir = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\pages"
html_files = glob.glob(os.path.join(pages_dir, "*.html"))
html_files.append(r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\Balaji Udyog.html")

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if filepath.endswith("Balaji Udyog.html"):
        old_logo_footer = '''<a href="../Balaji Udyog.html" class="logo">
          
          <div class="logo-text"><b>BALAJI UDYOG</b><small>Est · India · Exporters</small></div>
        </a>'''
        new_logo_footer = '''<a href="Balaji Udyog.html" class="logo">
          <img src="assets/images/logo.jpg" alt="Balaji Udyog Logo" style="height:45px; margin-right:5px; mix-blend-mode: multiply;">
          <div class="logo-text"><b>BALAJI UDYOG</b><small>Est · India · Exporters</small></div>
        </a>'''
        content = content.replace(old_logo_footer, new_logo_footer)
        
        # It already has the top logo.
    else:
        # In pages/ files, the paths go up one level (../)
        old_logo = '''<a href="../Balaji Udyog.html" class="logo">
      
      <div class="logo-text"><b>BALAJI UDYOG</b><small>Est · India · Exporters</small></div>
    </a>'''
        new_logo = '''<a href="../Balaji Udyog.html" class="logo">
      <img src="../assets/images/logo.jpg" alt="Balaji Udyog Logo" style="height:45px; margin-right:5px; mix-blend-mode: multiply;">
      <div class="logo-text"><b>BALAJI UDYOG</b><small>Est · India · Exporters</small></div>
    </a>'''
        content = content.replace(old_logo, new_logo)
        
        old_logo_footer = '''<a href="../Balaji Udyog.html" class="logo">
          
          <div class="logo-text"><b>BALAJI UDYOG</b><small>Est · India · Exporters</small></div>
        </a>'''
        new_logo_footer = '''<a href="../Balaji Udyog.html" class="logo">
          <img src="../assets/images/logo.jpg" alt="Balaji Udyog Logo" style="height:45px; margin-right:5px; mix-blend-mode: multiply;">
          <div class="logo-text"><b>BALAJI UDYOG</b><small>Est · India · Exporters</small></div>
        </a>'''
        content = content.replace(old_logo_footer, new_logo_footer)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
print("Logos updated in all pages.")
