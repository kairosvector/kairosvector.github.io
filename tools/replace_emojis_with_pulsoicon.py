import os

def replace_emojis():
    path = 'tools/generate_fm_page.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace 🌸 in "看遊戲地圖" button with PulsoIcon `map-2` (Folded map with location marker)
    pulso_map2_svg = """<svg class="btn-svg-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 18.5l-3 -1.5l-6 3v-13l6 -3l6 3l6 -3v7.5"></path><path d="M9 4v13"></path><path d="M15 7v5.5"></path><path d="M21.121 20.121a3 3 0 1 0 -4.242 0c.418 .419 1.125 1.045 2.121 1.879c1.051 -.89 1.759 -1.516 2.121 -1.879"></path><path d="M19 18v.01"></path></svg>"""
    content = content.replace(
        '<span class="btn-icon">🌸</span>',
        pulso_map2_svg
    )

    # 2. Replace 🎯 in "用GeoSim直飛" button with PulsoIcon `plane` (Airplane flight vector)
    pulso_plane_svg = """<svg class="btn-svg-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path></svg>"""
    content = content.replace(
        '<span class="btn-icon">🎯</span>',
        pulso_plane_svg
    )

    # 3. Add PulsoIcon map pin to button 3 ("地圖")
    pulso_pin_small_svg = """<svg class="btn-svg-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></svg>"""
    content = content.replace(
        '<span>地圖</span>',
        f'{pulso_pin_small_svg}\n                      <span>地圖</span>'
    )

    # 4. Replace 📍 in district headers with PulsoIcon `map-pin`
    pulso_pin_svg = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00A040" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></svg>"""
    content = content.replace(
        '<span class="district-pin-icon">📍</span>',
        f'<span class="district-pin-icon">{pulso_pin_svg}</span>'
    )

    # 5. Replace ⏳ in cooldown banner with PulsoIcon `hourglass`
    pulso_hourglass_svg = """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 22h14"></path><path d="M5 2h14"></path><path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22"></path><path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"></path></svg>"""
    content = content.replace(
        '<span class="cooldown-icon">⏳</span>',
        f'<span class="cooldown-icon">{pulso_hourglass_svg}</span>'
    )

    # 6. Replace 🔍 in no results box
    pulso_search_svg = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="vertical-align: middle; margin-right: 4px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>"""
    content = content.replace(
        '🔍 查無符合條件的全家門市',
        f'{pulso_search_svg}查無符合條件的全家門市'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced all emojis with PulsoIcon SVGs in tools/generate_fm_page.py")

if __name__ == '__main__':
    replace_emojis()
