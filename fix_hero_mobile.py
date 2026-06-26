import re

filepath = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\Balaji Udyog.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_slider_html = """<!-- ==================== HERO SLIDER ==================== -->
<div class="hero-slider" id="home" style="background:var(--navy-deep);position:relative;width:100%;height:80vh;min-height:500px;overflow:hidden;">
  <div class="hero-slide active" style="position:absolute;inset:0;background-image: url('assets/images/banners/banner1.png');background-size:cover;background-position:center;opacity:1;transition:opacity 1s ease-in-out;z-index:2;"></div>
  <div class="hero-slide" style="position:absolute;inset:0;background-image: url('assets/images/banners/banner2.png');background-size:cover;background-position:center;opacity:0;transition:opacity 1s ease-in-out;z-index:1;"></div>
  <div class="hero-slide" style="position:absolute;inset:0;background-image: url('assets/images/banners/banner3.png');background-size:cover;background-position:center;opacity:0;transition:opacity 1s ease-in-out;z-index:1;"></div>
</div>"""

new_slider_html = """<!-- ==================== HERO SLIDER ==================== -->
<style>
  .hero-slider {
    background: var(--navy-deep);
    position: relative;
    width: 100%;
    height: 80vh;
    min-height: 500px;
    overflow: hidden;
  }
  .hero-slide {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    transition: opacity 1s ease-in-out;
  }
  @media (max-width: 880px) {
    .hero-slider {
      height: 40vh;
      min-height: 250px;
      /* If the background-size is contain, it will show fully */
    }
    .hero-slide {
      background-size: contain;
      background-position: center center;
    }
  }
  @media (max-width: 500px) {
    .hero-slider {
      height: 30vh;
      min-height: 200px;
    }
  }
</style>
<div class="hero-slider" id="home">
  <div class="hero-slide active" style="background-image: url('assets/images/banners/banner1.png'); opacity:1; z-index:2;"></div>
  <div class="hero-slide" style="background-image: url('assets/images/banners/banner2.png'); opacity:0; z-index:1;"></div>
  <div class="hero-slide" style="background-image: url('assets/images/banners/banner3.png'); opacity:0; z-index:1;"></div>
</div>"""

if old_slider_html in content:
    content = content.replace(old_slider_html, new_slider_html)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Hero slider updated successfully!")
else:
    print("Could not find the exact hero slider HTML to replace. Searching with regex...")
    # fallback regex
    pattern = re.compile(r'<!-- ==================== HERO SLIDER ==================== -->.*?</div>', re.DOTALL)
    content = pattern.sub(new_slider_html, content, count=1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Hero slider updated using regex!")
