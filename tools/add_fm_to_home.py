import os

def update_home():
    path = 'app/src/pages/index.astro'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    fm_section = """
  <!-- Pikmin Bloom × FamilyMart 5th Anniversary Event Banner -->
  <section class="section fm-event-teaser" id="fm-event-section" style="padding-top: 0; padding-bottom: var(--space-6);">
    <div class="container">
      <div class="card fm-teaser-card" data-animate style="border: 1px solid rgba(0, 160, 64, 0.35); background: linear-gradient(135deg, rgba(0, 160, 64, 0.08) 0%, rgba(0, 112, 192, 0.04) 100%);">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: var(--space-6); flex-wrap: wrap;">
          <div style="max-width: 680px;">
            <div style="display: flex; align-items: center; gap: var(--space-3); margin-bottom: var(--space-3); flex-wrap: wrap;">
              <span class="badge" style="background: #00A040; color: #fff; font-weight: 800;">五週年特別活動</span>
              <span style="font-size: var(--text-xs); color: #00A040; font-weight: 700;">2026/11/10 ～ 12/07</span>
              <span class="badge" style="background: #EAB308; color: #000; font-weight: 800;">7 款金色花苗</span>
            </div>
            <h2 style="font-size: clamp(var(--text-xl), 3vw, var(--text-2xl)); font-weight: 800; margin-bottom: var(--space-2); line-height: 1.3;">
              <a href="/events/familymart-pikmin" style="color: var(--color-text); text-decoration: none;">
                全家便利商店 台北市 696 店 GPS 座標巡航地圖與打卡清單
              </a>
            </h2>
            <p style="font-size: var(--text-sm); color: var(--color-text-secondary); line-height: 1.6; margin-bottom: var(--space-4);">
              Pikmin Bloom 五週年紀念！台北市 12 行政區 696 間全家門市特別地點全數收錄。支援一鍵複製全區巡航路徑、7 天領取冷卻追蹤與直飛定位。
            </p>
            <div style="display: flex; gap: var(--space-3); flex-wrap: wrap;">
              <a href="/events/familymart-pikmin" class="btn btn--primary btn--md" style="background: linear-gradient(135deg, #00A040, #0070C0); border: none;">
                探索台北市 696 店地圖 ➔
              </a>
              <a href="/events/familymart-pikmin#how-to-use" class="btn btn--outline btn--md">
                搭配 GeoSim 使用教學
              </a>
            </div>
          </div>
          <div style="display: flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 14px; background: rgba(0, 160, 64, 0.15); color: #00A040; font-weight: 900; font-size: 1.25rem;">
            全家
          </div>
        </div>
      </div>
    </div>
  </section>
"""

    if 'id="fm-event-section"' in text:
        print('Already added')
        return

    coco_tag = 'id="coco-event-section"'
    if coco_tag in text:
        coco_idx = text.find(coco_tag)
        sec_end = text.find('</section>', coco_idx) + len('</section>')
        text = text[:sec_end] + '\n' + fm_section + text[sec_end:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print('Successfully added FamilyMart banner to homepage')
    else:
        print('Error: coco-event-section not found')

if __name__ == '__main__':
    update_home()
