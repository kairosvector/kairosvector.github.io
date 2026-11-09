import os

def update_buttons():
    path = 'tools/generate_fm_page.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update card button 1 (Pikmin)
    content = content.replace(
        '<span>進遊戲領苗</span>',
        '<span>看遊戲地圖</span>'
    )
    content = content.replace(
        'title="直接喚醒 Pikmin Bloom 並移動至此店座標"',
        'title="直接開啟 Pikmin Bloom 遊戲地圖"'
    )

    # 2. Update card button 2 (GeoSim)
    content = content.replace(
        '<span>導入 GeoSim</span>',
        '<span>用GeoSim直飛</span>'
    )
    content = content.replace(
        'title="導入 GeoSim 定位模擬器"',
        'title="用 GeoSim 直接定位直飛"'
    )

    # 3. Update ad and guide text references
    content = content.replace(
        '點一下「導入 GeoSim」落點到店門口',
        '點一下「用GeoSim直飛」落點到店門口'
    )
    content = content.replace(
        '門市卡片點「導入 GeoSim」，未安裝將自動導向 Google Play',
        '門市卡片點「用GeoSim直飛」，未安裝將自動導向 Google Play'
    )
    content = content.replace(
        '<h3 class="step-card__title">導入 GeoSim（自動導向商店）</h3>',
        '<h3 class="step-card__title">用GeoSim直飛（自動導向商店）</h3>'
    )
    content = content.replace(
        '在手機瀏覽器點擊門市卡片上的 <strong>「導入 GeoSim」</strong> 按鈕',
        '在手機瀏覽器點擊門市卡片上的 <strong>「用GeoSim直飛」</strong> 按鈕'
    )

    # 4. Refine CSS grid for card-actions so both buttons fit smoothly
    old_card_actions = """.card-actions {
    display: grid;
    grid-template-columns: 1.2fr 1fr auto;
    gap: 0.4rem;
  }"""
    new_card_actions = """.card-actions {
    display: grid;
    grid-template-columns: 1fr 1.2fr auto;
    gap: 0.35rem;
  }"""
    content = content.replace(old_card_actions, new_card_actions)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated button texts in tools/generate_fm_page.py")

if __name__ == '__main__':
    update_buttons()
