import os

def fix_district_scroll():
    path = 'tools/generate_fm_page.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS for tier-district-bar
    old_css = """.tier-district-bar {
    display: flex;
    gap: 0.45rem;
    overflow-x: auto;
    padding-bottom: 0.35rem;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
    margin-bottom: 0.55rem;
    align-items: center;
  }
  .tier-district-bar::-webkit-scrollbar {
    display: none;
  }"""

    new_css = """.tier-district-bar {
    display: flex;
    gap: 0.45rem;
    overflow-x: auto;
    padding-bottom: 0.45rem;
    -webkit-overflow-scrolling: touch;
    margin-bottom: 0.55rem;
    align-items: center;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.4) transparent;
  }
  .tier-district-bar::-webkit-scrollbar {
    height: 5px;
  }
  .tier-district-bar::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 999px;
  }
  .tier-district-bar::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.45);
    border-radius: 999px;
  }
  .tier-district-bar::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.75);
  }

  /* Desktop and Tablet: auto-wrap so all 12 districts are immediately visible without scrolling */
  @media (min-width: 768px) {
    .tier-district-bar {
      flex-wrap: wrap;
      overflow-x: visible;
      padding-bottom: 0;
    }
  }"""

    if old_css in content:
        content = content.replace(old_css, new_css)
        print("Replaced tier-district-bar CSS")
    else:
        print("WARNING: old_css not found!")

    # 2. Add Mouse Wheel Horizontal Scroll Listener in JavaScript
    wheel_listener_code = """
      // Mouse Wheel Horizontal Scroll Support on Desktop when scrollable
      const districtBar = document.querySelector('.tier-district-bar');
      if (districtBar) {
        districtBar.addEventListener('wheel', (e) => {
          if (districtBar.scrollWidth > districtBar.clientWidth) {
            if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
              e.preventDefault();
              districtBar.scrollLeft += e.deltaY;
            }
          }
        }, { passive: false });
      }
"""

    target_js = "function setupEventListeners() {"
    if target_js in content:
        content = content.replace(target_js, target_js + wheel_listener_code)
        print("Added wheel listener in JavaScript")
    else:
        print("WARNING: target_js not found!")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated tools/generate_fm_page.py successfully!")

if __name__ == '__main__':
    fix_district_scroll()
