import os

def update_generator():
    path = 'tools/generate_fm_page.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert Compact GeoSim Card under subtitle
    compact_ad_html = """
        <!-- Compact GeoSim Recommendation Card -->
        <aside class="geosim-compact-ad" aria-label="GeoSim 下載推薦">
          <div class="ad-icon" aria-hidden="true">
            <img src="/images/geosim-icon.png" alt="GeoSim App Icon" class="ad-icon-img" width="44" height="44" />
          </div>
          <div class="ad-content">
            <div class="ad-head">
              <span class="ad-tag">跑店神器 · 免費下載</span>
              <h2 class="ad-title">人還沒到，定位先到全家門市</h2>
            </div>
            <p class="ad-desc">
              台北市 696 間門市不用手打座標。點一下「導入 GeoSim」落點到店門口，再開遊戲領取 5 週年金色花苗，跑店快人一步。
            </p>
            <div class="ad-action-line">
              <a class="ad-cta-btn" href={playStoreUrl} target="_blank" rel="noopener">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <path d="M12 3v12"></path>
                  <path d="M6.5 10.5L12 16l5.5-5.5"></path>
                  <path d="M4 20h16"></path>
                </svg>
                免費下載 GeoSim
              </a>
              <span class="ad-note">門市卡片點「導入 GeoSim」，未安裝將自動導向 Google Play</span>
            </div>
          </div>
        </aside>
"""

    target_sub = '<p class="fm-subtitle">\n          活動期間 2026/11/10 ～ 12/07 · 向下滑動特別地點領取五週年金色花苗 · 7 天冷卻追蹤 · 一鍵導入 GeoSim 巡航\n        </p>'
    if target_sub in content:
        content = content.replace(target_sub, target_sub + '\n' + compact_ad_html)
        print('Added compact ad')
    else:
        print('WARNING: target_sub not found!')

    # 2. Insert GeoSim Intro Section & How To Use before Floating Quick Copy Toast
    bottom_sections_html = """
    <!-- GeoSim Introduction Section (Product Spotlight) -->
    <section id="geosim-intro" class="geosim-intro-section">
      <div class="fm-container">
        <div class="geosim-intro-card">
          <div class="geosim-intro-header">
            <div class="geosim-intro-logo">
              <img
                src="/images/geosim-icon.png"
                alt="GeoSim App Icon"
                width="72"
                height="72"
                class="geosim-app-img"
              />
            </div>
            <div class="geosim-intro-heading">
              <span class="badge badge--geosim">推薦搭配工具</span>
              <h2 class="geosim-intro-title">GeoSim — 自由定位，探索無界限</h2>
              <p class="geosim-intro-tagline">
                專為 Android 打造的 GPS 位置模擬與路線規劃測試工具。適合遊戲玩家探索地圖、收集五週年全家飾品皮克敏，以及開發者測試位置服務。
              </p>
            </div>
          </div>

          <!-- Feature Columns for Pikmin Players -->
          <div class="geosim-features-grid">
            <div class="feature-item">
              <div class="feature-item__icon-wrap">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polygon points="12 8 8 12 12 16 16 12 12 8"></polygon>
                </svg>
              </div>
              <h3 class="feature-item__title">懸浮虛擬搖桿</h3>
              <p class="feature-item__desc">
                遊戲上方懸浮覆蓋控制面板，支援隨意拖曳與 360 度方向控制，自訂行走速度（1~24 km/h），在家也能自然散步。
              </p>
            </div>

            <div class="feature-item">
              <div class="feature-item__icon-wrap">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <h3 class="feature-item__title">依線巡航與自動折返</h3>
              <p class="feature-item__desc">
                貼入多間門市座標即可自動連成路徑，支援平滑速度前進與自動循環，輕鬆達成「走 2,000 步」地點挑戰。
              </p>
            </div>

            <div class="feature-item">
              <div class="feature-item__icon-wrap">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
                  <line x1="8" y1="2" x2="8" y2="18"></line>
                  <line x1="16" y1="6" x2="16" y2="22"></line>
                </svg>
              </div>
              <h3 class="feature-item__title">區內漫步隨機遊走</h3>
              <p class="feature-item__desc">
                在地圖選定 3 個以上頂點繪製多邊形區域，自動在範圍內隨機自然漫步，模擬最真實的戶外散步走動軌跡。
              </p>
            </div>

            <div class="feature-item">
              <div class="feature-item__icon-wrap">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                </svg>
              </div>
              <h3 class="feature-item__title">自訂書籤與純點庫</h3>
              <p class="feature-item__desc">
                支援建立景點資料夾、標籤分類與匯入匯出備份。官方更提供全台純點座標庫與每週主題巡航專欄。
              </p>
            </div>
          </div>

          <!-- Download Action Bar -->
          <div class="geosim-intro-actions">
            <a
              href={playStoreUrl}
              target="_blank"
              rel="noopener noreferrer"
              class="btn-playstore"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3.609 1.814L13.792 12 3.61 22.186a.996.996 0 01-.61-.92V2.734a1 1 0 01.609-.92zm10.89 10.893l2.302 2.302-10.937 6.333 8.635-8.635zm3.199-3.199l2.302 1.329-2.822 1.634-2.116-2.116 2.636-2.847zm-4.529-4.528L4.864 1.367 15.8 7.7l-2.63 2.88z"/>
              </svg>
              前往 Google Play 免費下載 GeoSim
            </a>
            <a href="/geosim" class="btn-geosim-outline">
              閱讀 GeoSim 完整功能介紹
            </a>
            <a href="/geosim/spot-map" class="btn-geosim-ghost">
              探索全球純點座標庫
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- How to Use Section -->
    <section id="how-to-use" class="how-to-use-section">
      <div class="fm-container">
        <div class="how-to-use-card">
          <h2 class="how-to-use__title">如何在全家活動中搭配 GeoSim 使用</h2>
          <div class="steps-grid">
            <div class="step-card">
              <div class="step-card__number">1</div>
              <h3 class="step-card__title">導入 GeoSim（自動導向商店）</h3>
              <p>
                在手機瀏覽器點擊門市卡片上的 <strong>「導入 GeoSim」</strong> 按鈕，系統將直接啟動 App 並定位在該門市。若尚未安裝，將自動前往 Google Play 商店下載。
              </p>
            </div>
            <div class="step-card">
              <div class="step-card__number">2</div>
              <h3 class="step-card__title">複製座標貼上</h3>
              <p>
                點擊卡片上的 <strong>「複製」</strong>，經緯度直接複製進剪貼簿。切換到 GeoSim 主畫面或懸浮控制器的搜尋欄即可貼上前往。
              </p>
            </div>
            <div class="step-card">
              <div class="step-card__number">3</div>
              <h3 class="step-card__title">整區巡航自動走 2,000 步</h3>
              <p>
                點擊各區頂部的 <strong>「複製巡航」</strong> 或頂部 <strong>「複製目前篩選巡航路徑」</strong>，可一次取得所有門市路徑。貼入 GeoSim 的「依線巡航」，自動掛機散步 2,000 步並依序抵達門市領花苗。
              </p>
            </div>
            <div class="step-card">
              <div class="step-card__number">4</div>
              <h3 class="step-card__title">7 天冷卻打卡記錄</h3>
              <p>
                每刷完一間門市，勾選 <strong>「已造訪」</strong>，手機會自動記錄日期並鎖定 7 天倒數，下次可刷日期一清二楚。
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
"""

    target_toast = '    <!-- Floating Quick Copy Toast -->'
    if target_toast in content:
        content = content.replace(target_toast, bottom_sections_html + '\n' + target_toast)
        print('Added bottom sections')
    else:
        print('WARNING: target_toast not found!')

    # 3. Add CSS for geosim ads and sections
    css_to_add = """
  /* Compact GeoSim Recommendation Card */
  .geosim-compact-ad {
    margin: 1rem 0 1.25rem;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    background: #FFFFFF;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    padding: 14px 16px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
    box-sizing: border-box;
    width: 100%;
    text-align: left;
  }

  .geosim-compact-ad .ad-icon {
    flex: none;
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .geosim-compact-ad .ad-icon-img {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    object-fit: cover;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  }

  .geosim-compact-ad .ad-content {
    flex: 1;
    min-width: 0;
  }

  .geosim-compact-ad .ad-head {
    margin-bottom: 4px;
  }

  .geosim-compact-ad .ad-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: #7C3AED;
    background: #F5F3FF;
    border: 1px solid #DDD6FE;
    padding: 2px 8px;
    border-radius: 999px;
    margin-bottom: 4px;
  }

  .geosim-compact-ad .ad-title {
    margin: 2px 0 4px;
    font-size: 1.05rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.35;
  }

  .geosim-compact-ad .ad-desc {
    margin: 0 0 10px;
    color: #475569;
    font-size: 13.5px;
    line-height: 1.5;
  }

  .geosim-compact-ad .ad-action-line {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  .geosim-compact-ad .ad-cta-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
    color: #FFFFFF;
    padding: 7px 16px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 13.5px;
    text-decoration: none;
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.35);
    transition: transform 0.15s ease, filter 0.15s ease, box-shadow 0.15s ease;
  }

  .geosim-compact-ad .ad-cta-btn:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.45);
  }

  .geosim-compact-ad .ad-note {
    font-size: 12px;
    color: #64748B;
  }

  @media (max-width: 520px) {
    .geosim-compact-ad {
      padding: 12px;
      gap: 10px;
    }
    .geosim-compact-ad .ad-icon,
    .geosim-compact-ad .ad-icon-img {
      width: 40px;
      height: 40px;
      border-radius: 10px;
    }
    .geosim-compact-ad .ad-title {
      font-size: 0.98rem;
    }
    .geosim-compact-ad .ad-desc {
      font-size: 12.5px;
      margin-bottom: 8px;
    }
    .geosim-compact-ad .ad-action-line {
      flex-direction: column;
      align-items: flex-start;
      gap: 6px;
    }
    .geosim-compact-ad .ad-cta-btn {
      width: 100%;
      justify-content: center;
    }
  }

  /* GeoSim Introduction Section */
  .geosim-intro-section {
    padding: 2.5rem 0;
  }

  .geosim-intro-card {
    background: #FFFFFF;
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 18px;
    padding: 2.25rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.03) 0%, rgba(0, 160, 64, 0.03) 100%);
  }

  .geosim-intro-header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
  }

  .geosim-app-img {
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
  }

  .geosim-intro-heading {
    flex: 1;
    min-width: 260px;
  }

  .badge--geosim {
    display: inline-block;
    font-size: 11.5px;
    font-weight: 800;
    color: #7C3AED;
    background: #F5F3FF;
    border: 1px solid #DDD6FE;
    padding: 2px 10px;
    border-radius: 9999px;
  }

  .geosim-intro-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0.35rem 0 0.5rem;
  }

  .geosim-intro-tagline {
    font-size: 0.95rem;
    color: #64748B;
    line-height: 1.6;
    margin: 0;
  }

  .geosim-features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
  }

  .feature-item {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  }

  .feature-item__icon-wrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(124, 58, 237, 0.1);
    color: #7C3AED;
    margin-bottom: 0.75rem;
  }

  .feature-item__title {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.35rem;
  }

  .feature-item__desc {
    font-size: 0.85rem;
    color: #64748B;
    line-height: 1.5;
    margin: 0;
  }

  .geosim-intro-actions {
    display: flex;
    gap: 0.85rem;
    flex-wrap: wrap;
    align-items: center;
  }

  .btn-playstore {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
    color: #FFFFFF;
    padding: 0.75rem 1.4rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    border: none;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
    transition: all 0.2s;
  }

  .btn-playstore:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.45);
  }

  .btn-geosim-outline {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.3rem;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.92rem;
    text-decoration: none;
    border: 1px solid #CBD5E1;
    color: #334155;
    background: #FFFFFF;
    transition: all 0.2s;
  }

  .btn-geosim-outline:hover {
    border-color: #7C3AED;
    color: #7C3AED;
    background: #F8FAFC;
  }

  .btn-geosim-ghost {
    display: inline-flex;
    align-items: center;
    padding: 0.75rem 1.2rem;
    font-weight: 700;
    font-size: 0.92rem;
    text-decoration: none;
    color: #64748B;
    transition: color 0.2s;
  }

  .btn-geosim-ghost:hover {
    color: #0F172A;
  }

  /* How to Use Section */
  .how-to-use-section {
    padding: 1.5rem 0 3rem;
  }

  .how-to-use-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  }

  .how-to-use__title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
  }

  .step-card {
    position: relative;
    padding: 1.25rem;
    background: #F8FAFC;
    border-radius: 14px;
    border: 1px solid #F1F5F9;
  }

  .step-card__number {
    position: absolute;
    top: 0.85rem;
    right: 1rem;
    font-size: 1.5rem;
    font-weight: 900;
    color: rgba(124, 58, 237, 0.25);
  }

  .step-card__title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.5rem;
    padding-right: 1.5rem;
  }

  .step-card p {
    font-size: 0.85rem;
    color: #64748B;
    line-height: 1.55;
    margin: 0;
  }
"""

    target_css = '</style>'
    if target_css in content:
        content = content.replace(target_css, css_to_add + '\n' + target_css)
        print('Added CSS')
    else:
        print('WARNING: target_css not found!')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated tools/generate_fm_page.py successfully')

if __name__ == '__main__':
    update_generator()
