import os
import json

def generate_page(is_staging=False):
    target_path = 'app/src/pages/events/familymart-pikmin/staging.astro' if is_staging else 'app/src/pages/events/familymart-pikmin/index.astro'
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    staging_banner = '''<!-- Staging Environment Indicator Banner -->
    <div style="background: #FEF3C7; border-bottom: 2px solid #F59E0B; padding: 0.5rem 1rem; text-align: center; font-size: 0.875rem; font-weight: 700; color: #92400E; z-index: 50; position: relative;">
      [測試預覽環境 Staging] 此頁面用於驗證新功能，測試完畢確認無誤後將同步發布至正式版。
    </div>''' if is_staging else ''

    code = """---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import stores from '../../../data/fm_taipei_stores.json';

const title = `全家便利商店 x Pikmin Bloom 五週年巡航地圖 (台北市 696 店) | GeoSim`;
const description = `2026/11/10 ~ 12/7 Pikmin Bloom 五週年全家便利商店聯名特別地點！台北市 696 間全家門市 GPS 精準座標、12 行政區動態膠囊篩選、7 天冷卻狀態追蹤、一鍵複製巡航佇列、直接喚醒 Pikmin Bloom / GeoSim。`;

// Group stores by district
const districtOrder = [
  '中山區', '大安區', '中正區', '內湖區', '松山區',
  '信義區', '士林區', '文山區', '北投區', '萬華區',
  '大同區', '南港區'
];

const districtCounts: Record<string, number> = {};
stores.forEach(s => {
  districtCounts[s.district] = (districtCounts[s.district] || 0) + 1;
});

const districts = [
  { id: 'all', name: '全部', count: stores.length },
  ...districtOrder.map(d => ({ id: d, name: d, count: districtCounts[d] || 0 }))
];

const districtGroups = districtOrder.map(d => ({
  name: d,
  count: districtCounts[d] || 0,
  stores: stores.filter(s => s.district === d)
}));

const playStoreUrl = 'https://play.google.com/store/apps/details?id=com.kairosvector.geosim';
---

<BaseLayout
  title={title}
  description={description}
  activeNav="events"
  lang="zh-TW"
  forcedTheme="vibrant"
  hideThemeSwitcher={true}
>
  <div class="fm-page">
    """ + staging_banner + """
    <!-- Top Sticky Version & Live Update Notification Banner -->
    <div class="top-sticky-version-wrapper" id="fm-version-card" data-batch-id="1" data-store-count={stores.length}>
      <div class="top-sticky-version-inner">
        <div class="top-sticky-version-left">
          <span class="version-dot" id="version-dot" aria-hidden="true"></span>
          <span class="version-tag" id="version-badge">台北 {stores.length} 店最新</span>
          <div class="version-marquee-box" id="version-marquee-box">
            <span class="version-ticker-text" id="version-ticker">
              <span class="ticker-badge">最新</span>初始建置 · 台北市 12 行政區 {stores.length} 間全家門市
            </span>
          </div>
        </div>
        <button id="btn-force-refresh" class="btn-top-refresh" type="button" title="清除快取載入最新門市點位">
          <svg class="refresh-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="23 4 23 10 17 10"></polyline>
            <polyline points="1 20 1 14 7 14"></polyline>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
          </svg>
          <span class="refresh-label">強制重整</span>
        </button>
      </div>
    </div>

    <!-- Top Fixed Hero Header -->
    <header class="fm-hero">
      <div class="fm-hero__inner">
        <div class="fm-badge-row">
          <span class="fm-badge fm-badge--green">Pikmin Bloom x 全家便利商店</span>
          <span class="fm-badge fm-badge--blue">五週年紀念聯名 · 特別地點</span>
          <span class="fm-badge fm-badge--gold">7 款零食金色花苗</span>
        </div>

        <h1 class="fm-title">
          全家便利商店 <span class="fm-title__highlight">台北市 696 店</span> 巡航地圖
        </h1>

        <p class="fm-subtitle">
          活動期間 2026/11/10 ～ 12/07 · 向下滑動特別地點領取五週年金色花苗 · 7 天冷卻追蹤 · 一鍵導入 GeoSim 巡航
        </p>

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
              台北市 696 間門市不用手打座標。點一下「用GeoSim直飛」落點到店門口，再開遊戲領取 5 週年金色花苗，跑店快人一步。
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
              <span class="ad-note">門市卡片點「用GeoSim直飛」，未安裝將自動導向 Google Play</span>
            </div>
          </div>
        </aside>


        <!-- Stats Bar -->
        <div class="fm-stats-bar">
          <div class="fm-stat-item">
            <span class="fm-stat-val">696</span>
            <span class="fm-stat-lbl">台北市全家總數</span>
          </div>
          <div class="fm-stat-item">
            <span class="fm-stat-val">12</span>
            <span class="fm-stat-lbl">行政區完整覆蓋</span>
          </div>
          <div class="fm-stat-item">
            <span class="fm-stat-val" id="pill-cooling-count">0</span>
            <span class="fm-stat-lbl">7 天冷卻中</span>
          </div>
          <div class="fm-stat-item">
            <span class="fm-stat-val" id="pill-todo-count">696</span>
            <span class="fm-stat-lbl">尚未前往</span>
          </div>
        </div>

        <!-- Tier 1: 12 Districts Filter Pills -->
        <div class="tier-district-bar" role="tablist" aria-label="台北市行政區篩選">
          {districts.map(d => (
            <button
              class={`district-pill ${d.id === 'all' ? 'active' : ''}`}
              data-district={d.id}
              role="tab"
              aria-selected={d.id === 'all' ? 'true' : 'false'}
            >
              {d.name} <span class="pill-count">{d.count}</span>
            </button>
          ))}
        </div>

        <!-- Tier 2: Status Pills Filter -->
        <div class="tier-status-bar" role="tablist" aria-label="冷卻狀態篩選">
          <button class="status-pill active" data-status="all">全部 ({stores.length})</button>
          <button class="status-pill" data-status="todo">尚未前往 (<span id="count-todo">{stores.length}</span>)</button>
          <button class="status-pill" data-status="cooling">7 天冷卻中 (<span id="count-cooling">0</span>)</button>
          <button class="status-pill" data-status="ready">冷卻完畢 (<span id="count-ready">0</span>)</button>
        </div>

        <!-- Action Tools Bar -->
        <div class="fm-tools-bar">
          <button id="btn-copy-filtered-route" class="fm-btn fm-btn--primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span id="btn-copy-label">複製目前篩選巡航路徑 (696)</span>
          </button>

          <button id="btn-toggle-search" class="fm-btn fm-btn--outline">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <span>搜尋門市 / 關鍵字</span>
          </button>
        </div>

        <!-- Expandable Search Box -->
        <div id="fm-search-panel" class="fm-search-panel" style="display: none;">
          <div class="search-input-wrap">
            <input
              type="text"
              id="fm-search-input"
              class="fm-search-input"
              placeholder="搜尋店名（如：市民店）、地址、路名（如：南京東路）或經緯度..."
              autocomplete="off"
            />
            <button id="fm-clear-search" class="fm-clear-btn" type="button" aria-label="清除搜尋">✕</button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Store List Container -->
    <main class="fm-main">
      <div class="fm-container">
        <!-- Results Counter & Summary -->
        <div class="fm-results-bar">
          <span id="stat-summary-text" class="stat-text">顯示 696 家全家門市</span>
          <div class="fm-legend">
            <span class="legend-item"><span class="dot dot-todo"></span>尚未前往</span>
            <span class="legend-item"><span class="dot dot-cooling"></span>7天冷卻中</span>
            <span class="legend-item"><span class="dot dot-ready"></span>滿7天可再次領取</span>
          </div>
        </div>

        <!-- District Sections -->
        {districtGroups.map(group => (
          <section class="district-section" data-district-section={group.name} id={`sec-${group.name}`}>
            <div class="district-header">
              <div class="district-header__left">
                <span class="district-pin-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00A040" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></svg></span>
                <h2 class="district-title">{group.name}</h2>
                <span class="district-store-count">共 {group.count} 店</span>
              </div>
              <button
                class="btn-copy-district-route"
                data-district={group.name}
                title={`複製${group.name}所有門市座標`}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span class="btn-district-copy-label">複製【{group.name}】巡航</span>
              </button>
            </div>

            <div class="store-grid">
              {group.stores.map(store => (
                <article
                  class="store-card"
                  data-store-id={store.id}
                  data-district={store.district}
                  data-name={store.name}
                  data-short={store.shortName}
                  data-lat={store.lat}
                  data-lng={store.lng}
                  data-coords={store.coordsText}
                  data-status-state="todo"
                >
                  <!-- Card Header: Cooldown toggle & Store Name -->
                  <div class="card-head">
                    <label class="check-toggle" title="勾選標記已前往（自動啟動 7 天冷卻倒數）">
                      <input
                        type="checkbox"
                        class="check-toggle__input"
                        data-store-id={store.id}
                      />
                      <span class="check-toggle__box">
                        <svg class="check-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                          <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                      </span>
                      <span class="check-toggle__text">已造訪</span>
                    </label>

                    <div class="store-name-box">
                      <h3 class="store-name" title={store.name}>
                        {store.shortName}
                      </h3>
                      <span class="store-badge-fami">全家</span>
                    </div>
                  </div>

                  <!-- 7-Day Cooldown Notice Banner -->
                  <div class="cooldown-banner" style="display: none;">
                    <span class="cooldown-icon"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 22h14"></path><path d="M5 2h14"></path><path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22"></path><path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"></path></svg></span>
                    <span class="cooldown-text">冷卻中 · 下次可領: <strong class="next-available-date">--/-- --:--</strong></span>
                  </div>

                  <!-- Address & GPS Info -->
                  <div class="card-body">
                    <div class="addr-row">
                      <svg class="addr-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                        <circle cx="12" cy="10" r="3"></circle>
                      </svg>
                      <span class="addr-text" title={store.address}>{store.address}</span>
                    </div>

                    <div class="coord-row">
                      <span class="coord-label">GPS:</span>
                      <code class="coord-code">{store.coordsText}</code>
                      <button
                        class="btn-copy-coord"
                        data-coords={store.coordsText}
                        data-name={store.shortName}
                        title="複製這間店的經緯度座標"
                      >
                        複製
                      </button>
                    </div>
                  </div>

                  <!-- Action Buttons -->
                  <div class="card-actions">
                    <button
                      class="btn-action btn-pikmin btn-launch-pikmin"
                      data-lat={store.lat}
                      data-lng={store.lng}
                      data-name={store.shortName}
                      title="直接開啟 Pikmin Bloom 遊戲地圖"
                    >
                      <svg class="btn-svg-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 18.5l-3 -1.5l-6 3v-13l6 -3l6 3l6 -3v7.5"></path><path d="M9 4v13"></path><path d="M15 7v5.5"></path><path d="M21.121 20.121a3 3 0 1 0 -4.242 0c.418 .419 1.125 1.045 2.121 1.879c1.051 -.89 1.759 -1.516 2.121 -1.879"></path><path d="M19 18v.01"></path></svg>
                      <span>看遊戲地圖</span>
                    </button>

                    <button
                      class="btn-action btn-geosim btn-launch-geosim"
                      data-lat={store.lat}
                      data-lng={store.lng}
                      data-name={store.name}
                      data-coords={store.coordsText}
                      title="用 GeoSim 直接定位直飛"
                    >
                      <svg class="btn-svg-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path></svg>
                      <span>用GeoSim直飛</span>
                    </button>

                    <a
                      href={store.gmapUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      class="btn-action btn-gmap"
                      title="在 Google Maps 查看實體店"
                    >
                      <svg class="btn-svg-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></svg>
                      <span>地圖</span>
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))}

        <!-- No Results Fallback -->
        <div id="no-results-box" class="no-results-box" style="display: none;">
          <p class="no-results-text"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="vertical-align: middle; margin-right: 4px;"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>查無符合條件的全家門市，請嘗試清除關鍵字或切換行政區篩選。</p>
        </div>
      </div>
    </main>


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
              <h3 class="step-card__title">用GeoSim直飛（自動導向商店）</h3>
              <p>
                在手機瀏覽器點擊門市卡片上的 <strong>「用GeoSim直飛」</strong> 按鈕，系統將直接啟動 App 並定位在該門市。若尚未安裝，將自動前往 Google Play 商店下載。
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

    <!-- Floating Quick Copy Toast -->
    <div id="copy-toast" class="copy-toast" role="alert" aria-live="polite"></div>
  </div>

  <script is:inline>
    const STORAGE_KEY_PREFIX = 'fm_visited_tpe_';
    const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;
    const PLAY_STORE_URL = 'https://play.google.com/store/apps/details?id=com.kairosvector.geosim';

    let currentDistrict = 'all';
    let currentStatus = 'all';
    let currentSearch = '';

    
    // Version Polling and Force Refresh Logic
    let latestRemoteVersion = null;
    const btnForceRefresh = document.getElementById('btn-force-refresh');
    if (btnForceRefresh) {
      btnForceRefresh.addEventListener('click', function (e) {
        e.stopPropagation();
        triggerForceRefresh();
      });
    }

    function triggerForceRefresh() {
      if (btnForceRefresh) {
        btnForceRefresh.classList.add('is-refreshing');
        const label = btnForceRefresh.querySelector('.refresh-label');
        if (label) label.textContent = '載入最新中...';
      }
      showToast('正在強制清除快取並載入最新點位...');
      const u = new URL(window.location.href);
      const targetVer = latestRemoteVersion || '1.0';
      u.searchParams.set('v', targetVer);
      u.searchParams.set('t', Date.now().toString());
      setTimeout(function () {
        window.location.href = u.toString();
      }, 250);
    }

    function applyRemoteUpdateNotice(remote) {
      latestRemoteVersion = remote.version || remote.batch_id;
      const card = document.getElementById('fm-version-card');
      const dot = document.getElementById('version-dot');
      const badge = document.getElementById('version-badge');
      const ticker = document.getElementById('version-ticker');
      const btn = document.getElementById('btn-force-refresh');

      if (card) {
        card.classList.add('has-update');
        card.onclick = function() { triggerForceRefresh(); };
      }
      if (dot) dot.classList.add('has-update');
      if (badge) {
        badge.textContent = '⚡ 發現新資料！';
        badge.classList.add('has-update');
      }
      if (ticker) {
        ticker.innerHTML = '<span class="ticker-badge has-update">新發布</span><strong>' + (remote.description || '最新門市資料已更新') + '</strong> ➔ <span style="text-decoration: underline;">點此立即更新</span>';
        ticker.classList.add('has-update');
      }
      if (btn) {
        btn.classList.add('has-update');
        const label = btn.querySelector('.refresh-label');
        if (label) label.textContent = '點我立即更新 ↻';
        btn.setAttribute('title', '已有新更新發布，請點此強制重整載入最新點位！');
      }
    }

    function checkRemoteVersion() {
      const card = document.getElementById('fm-version-card');
      if (!card) return;
      const localBatch = parseInt(card.getAttribute('data-batch-id') || '0', 10);
      const localCount = parseInt(card.getAttribute('data-store-count') || '0', 10);

      fetch('/events/fm-version.json')
        .then(function (res) { return res.json(); })
        .then(function (remote) {
          if (!remote || !remote.batch_id) return;
          if (remote.batch_id > localBatch || remote.store_count > localCount) {
            applyRemoteUpdateNotice(remote);
          }
        })
        .catch(function () {});
    }

    // Smart version detection: Check once on load
    checkRemoteVersion();

    // Check when user resumes the tab (throttled to at least 60s)
    let lastVersionCheck = Date.now();
    document.addEventListener('visibilitychange', function() {
      if (!document.hidden && (Date.now() - lastVersionCheck > 60000)) {
        lastVersionCheck = Date.now();
        checkRemoteVersion();
      }
    });

    // Gentle passive interval (every 5 minutes, ONLY when tab is visible)
    setInterval(function() {
      if (!document.hidden) {
        lastVersionCheck = Date.now();
        checkRemoteVersion();
      }
    }, 300000);

    const toast = document.getElementById('copy-toast');
    let toastTimer = null;

    function showToast(msg) {
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, 2400);
    }

    // Visited & 7-Day Cooldown state in localStorage
    function getVisitedTime(storeId) {
      try {
        const val = localStorage.getItem(STORAGE_KEY_PREFIX + storeId);
        return val ? parseInt(val, 10) : 0;
      } catch (e) {
        return 0;
      }
    }

    function setVisited(storeId, isVisited) {
      try {
        if (isVisited) {
          localStorage.setItem(STORAGE_KEY_PREFIX + storeId, Date.now().toString());
        } else {
          localStorage.removeItem(STORAGE_KEY_PREFIX + storeId);
        }
      } catch (e) {}
      updateAllStoreStates();
      filterStores();
    }

    function formatDate(ms) {
      const d = new Date(ms);
      return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
    }

    function updateAllStoreStates() {
      const now = Date.now();
      let countTodo = 0;
      let countCooling = 0;
      let countReady = 0;

      document.querySelectorAll('.store-card').forEach((card) => {
        const storeId = card.getAttribute('data-store-id');
        const visitedTime = getVisitedTime(storeId);
        const checkbox = card.querySelector('.check-toggle__input');
        const banner = card.querySelector('.cooldown-banner');
        const dateSpan = card.querySelector('.next-available-date');

        if (!visitedTime) {
          card.classList.remove('is-visited', 'is-cooling', 'is-ready');
          card.setAttribute('data-status-state', 'todo');
          if (checkbox) checkbox.checked = false;
          if (banner) banner.style.display = 'none';
          countTodo++;
        } else if (now - visitedTime < SEVEN_DAYS_MS) {
          card.classList.add('is-visited', 'is-cooling');
          card.classList.remove('is-ready');
          card.setAttribute('data-status-state', 'cooling');
          if (checkbox) checkbox.checked = true;
          if (banner) {
            banner.style.display = 'flex';
            banner.className = 'cooldown-banner is-cooling-badge';
            const nextDate = visitedTime + SEVEN_DAYS_MS;
            if (dateSpan) dateSpan.textContent = formatDate(nextDate);
          }
          countCooling++;
        } else {
          card.classList.add('is-visited', 'is-ready');
          card.classList.remove('is-cooling');
          card.setAttribute('data-status-state', 'ready');
          if (checkbox) checkbox.checked = false;
          if (banner) {
            banner.style.display = 'flex';
            banner.className = 'cooldown-banner is-ready-badge';
            if (dateSpan) dateSpan.textContent = '滿 7 天可再次領取！';
          }
          countReady++;
        }
      });

      // Update Top Status Counter
      const elCoolingTop = document.getElementById('pill-cooling-count');
      const elTodoTop = document.getElementById('pill-todo-count');
      if (elCoolingTop) elCoolingTop.textContent = `${countCooling}`;
      if (elTodoTop) elTodoTop.textContent = `${countTodo}`;

      const elTodo = document.getElementById('count-todo');
      const elCooling = document.getElementById('count-cooling');
      const elReady = document.getElementById('count-ready');
      if (elTodo) elTodo.textContent = `${countTodo}`;
      if (elCooling) elCooling.textContent = `${countCooling}`;
      if (elReady) elReady.textContent = `${countReady}`;
    }

    // Launch Pikmin Bloom
    function openInPikmin(lat, lng) {
      const LAT = Number(lat).toFixed(7);
      const LNG = Number(lng).toFixed(7);
      const ua = navigator.userAgent || '';
      const isAndroid = /Android/i.test(ua);
      const isIOS = /iPhone|iPad|iPod/i.test(ua);
      const playStore = 'https://play.google.com/store/apps/details?id=com.nianticlabs.pikmin';
      const appStore = 'https://apps.apple.com/app/id1492797348';
      const fallbackUrl = isIOS ? appStore : playStore;

      showToast('正在開啟 Pikmin Bloom...');

      let appOpened = false;
      const fallbackTimer = setTimeout(() => {
        if (!appOpened && !document.hidden) {
          window.location.href = fallbackUrl;
        }
      }, 1800);

      const onVisibilityChange = () => {
        if (document.hidden) {
          appOpened = true;
          clearTimeout(fallbackTimer);
        }
      };
      window.addEventListener('visibilitychange', onVisibilityChange, { once: true });
      window.addEventListener('pagehide', onVisibilityChange, { once: true });

      if (isAndroid) {
        location.href = 'intent:///WIDE_AREA_MAP?LATITUDE=' + LAT + '&LONGITUDE=' + LNG
          + '#Intent;scheme=pikminbloom;package=com.nianticlabs.pikmin;S.browser_fallback_url=' + encodeURIComponent(playStore) + ';end';
        return;
      }
      location.href = 'pikminbloom:///WIDE_AREA_MAP?LATITUDE=' + LAT + '&LONGITUDE=' + LNG;
    }

    // Launch GeoSim (Identical to CoCo: window.AndroidGeoSim + intent://location?lat=...&lng=...&label=...)
    async function launchGeoSim(lat, lng, storeName, coordsText) {
      if (window.AndroidGeoSim && typeof window.AndroidGeoSim.setCoordinate === 'function') {
        window.AndroidGeoSim.setCoordinate(parseFloat(lat), parseFloat(lng), storeName);
        showToast(`已帶入 GeoSim: ${storeName}`);
        return;
      }
      showToast(`正在開啟 GeoSim (${storeName})...`);
      const isAndroid = /Android/i.test(navigator.userAgent);
      const encodedName = encodeURIComponent(storeName);
      const fallbackUrlEncoded = encodeURIComponent(PLAY_STORE_URL);

      if (isAndroid) {
        const intentUri = `intent://location?lat=${lat}&lng=${lng}&label=${encodedName}#Intent;scheme=geosim;package=com.kairosvector.geosim;S.browser_fallback_url=${fallbackUrlEncoded};end`;
        let appOpened = false;
        const fallbackTimer = setTimeout(() => {
          if (!appOpened && !document.hidden) {
            window.location.href = PLAY_STORE_URL;
          }
        }, 1800);

        const onVisibilityChange = () => {
          if (document.hidden) {
            appOpened = true;
            clearTimeout(fallbackTimer);
          }
        };
        window.addEventListener('visibilitychange', onVisibilityChange, { once: true });
        window.addEventListener('pagehide', onVisibilityChange, { once: true });
        window.location.href = intentUri;
      } else {
        copyToClipboard(coordsText, `已複製【${storeName}】座標，可在手機 GeoSim 中貼上定位`);
      }
    }

    function copyToClipboard(text, msg) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
          .then(() => showToast(msg || '已複製至剪貼簿'))
          .catch(() => fallbackCopy(text, msg));
      } else {
        fallbackCopy(text, msg);
      }
    }

    function fallbackCopy(text, msg) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {
        document.execCommand('copy');
      } catch (e) {}
      document.body.removeChild(ta);
      showToast(msg || '已複製至剪貼簿');
    }

    // Filter Stores Function
    function filterStores() {
      const q = currentSearch.trim().toLowerCase();
      let visibleCount = 0;

      document.querySelectorAll('.store-card').forEach((card) => {
        const district = card.getAttribute('data-district') || '';
        const name = (card.getAttribute('data-name') || '').toLowerCase();
        const shortName = (card.getAttribute('data-short') || '').toLowerCase();
        const coords = card.getAttribute('data-coords') || '';
        const state = card.getAttribute('data-status-state') || 'todo';

        const districtMatch = (currentDistrict === 'all' || district === currentDistrict);
        let statusMatch = true;
        if (currentStatus !== 'all') {
          statusMatch = (state === currentStatus);
        }

        let searchMatch = true;
        if (q) {
          searchMatch = name.includes(q) || shortName.includes(q) || coords.includes(q) || district.includes(q);
        }

        if (districtMatch && statusMatch && searchMatch) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      // Show/Hide District Sections
      document.querySelectorAll('.district-section').forEach((sec) => {
        const secDist = sec.getAttribute('data-district-section');
        const visibleCards = Array.from(sec.querySelectorAll('.store-card')).filter(c => c.style.display !== 'none');
        const anyVisible = visibleCards.length > 0;
        if (currentDistrict !== 'all' && secDist !== currentDistrict) {
          sec.style.display = 'none';
        } else {
          sec.style.display = anyVisible ? '' : 'none';
        }

        // Update district section copy button label
        const copyBtn = sec.querySelector('.btn-copy-district-route');
        if (copyBtn) {
          const btnLabel = copyBtn.querySelector('.btn-district-copy-label');
          const statusText = currentStatus === 'todo' ? '尚未前往' : (currentStatus === 'cooling' ? '冷卻中' : (currentStatus === 'ready' ? '冷卻完畢' : ''));
          if (btnLabel) {
            if (statusText) {
              btnLabel.textContent = `複製【${secDist} · ${statusText}】巡航 (${visibleCards.length})`;
            } else {
              btnLabel.textContent = `複製【${secDist}】巡航 (${visibleCards.length})`;
            }
          }
        }
      });

      // Update top copy button label
      const btnCopyLabel = document.getElementById('btn-copy-label');
      if (btnCopyLabel) {
        let label = `複製目前篩選巡航路徑 (${visibleCount})`;
        if (currentDistrict !== 'all' || currentStatus !== 'all') {
          const distLabel = currentDistrict !== 'all' ? currentDistrict : '台北市';
          const statusLabel = currentStatus === 'todo' ? '尚未前往' : (currentStatus === 'cooling' ? '冷卻中' : (currentStatus === 'ready' ? '冷卻完畢' : ''));
          label = `複製【${distLabel}${statusLabel ? ' · ' + statusLabel : ''}】巡航 (${visibleCount})`;
        }
        btnCopyLabel.textContent = label;
      }

      const statText = document.getElementById('stat-summary-text');
      if (statText) statText.textContent = `顯示 ${visibleCount} 家全家門市`;

      const noResults = document.getElementById('no-results-box');
      if (noResults) noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    function setupEventListeners() {
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

      updateAllStoreStates();

      // Checkbox click
      document.querySelectorAll('.check-toggle__input').forEach((cb) => {
        cb.addEventListener('change', (e) => {
          const storeId = e.target.getAttribute('data-store-id');
          setVisited(storeId, e.target.checked);
        });
      });

      // Launch Pikmin Bloom
      document.querySelectorAll('.btn-launch-pikmin').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const lat = parseFloat(btn.getAttribute('data-lat'));
          const lng = parseFloat(btn.getAttribute('data-lng'));
          const name = btn.getAttribute('data-name') || '';
          if (!isNaN(lat) && !isNaN(lng)) {
            openInPikmin(lat, lng);
          }
        });
      });

      // Launch GeoSim
      document.querySelectorAll('.btn-launch-geosim').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const lat = btn.getAttribute('data-lat');
          const lng = btn.getAttribute('data-lng');
          const name = btn.getAttribute('data-name');
          const coords = btn.getAttribute('data-coords');
          launchGeoSim(lat, lng, name, coords);
        });
      });

      // Copy Single Coordinate
      document.querySelectorAll('.btn-copy-coord').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const coords = btn.getAttribute('data-coords');
          const name = btn.getAttribute('data-name');
          copyToClipboard(coords, `已複製【${name}】座標 (${coords})`);
        });
      });

      // Copy District Route Button
      document.querySelectorAll('.btn-copy-district-route').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const dist = btn.getAttribute('data-district');
          const sec = document.getElementById('sec-' + dist);
          if (!sec) return;
          const visibleCards = Array.from(sec.querySelectorAll('.store-card')).filter(c => c.style.display !== 'none');
          if (visibleCards.length > 0) {
            const dynamicRoute = visibleCards.map(c => c.getAttribute('data-coords')).filter(Boolean).join('\\n');
            const statusLabel = currentStatus === 'todo' ? '尚未前往' : (currentStatus === 'cooling' ? '冷卻中' : (currentStatus === 'ready' ? '冷卻完畢' : ''));
            const desc = statusLabel ? `【${dist} · ${statusLabel}】(共 ${visibleCards.length} 店)` : `【${dist}】(共 ${visibleCards.length} 店)`;
            copyToClipboard(dynamicRoute, `已複製${desc}巡航路徑，可貼入 GeoSim`);
          } else {
            showToast(`目前【${dist}】沒有符合篩選條件的門市`);
          }
        });
      });

      // Copy Top Filtered Route Button
      const btnCopyAll = document.getElementById('btn-copy-filtered-route');
      if (btnCopyAll) {
        btnCopyAll.addEventListener('click', (e) => {
          e.preventDefault();
          const allVisible = Array.from(document.querySelectorAll('.store-card')).filter(c => c.style.display !== 'none');
          if (allVisible.length > 0) {
            const dynamicRoute = allVisible.map(c => c.getAttribute('data-coords')).filter(Boolean).join('\\n');
            const distLabel = currentDistrict !== 'all' ? currentDistrict : '台北市';
            const statusLabel = currentStatus === 'todo' ? '尚未前往' : (currentStatus === 'cooling' ? '冷卻中' : (currentStatus === 'ready' ? '冷卻完畢' : ''));
            const desc = `【${distLabel}${statusLabel ? ' · ' + statusLabel : ''}】(共 ${allVisible.length} 店)`;
            copyToClipboard(dynamicRoute, `已複製${desc}巡航路徑，可直接貼入 GeoSim 巡航佇列！`);
          } else {
            showToast('目前篩選條件下沒有任何門市');
          }
        });
      }

      // Tier 1: District Filter Pills
      document.querySelectorAll('.district-pill').forEach((btn) => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.district-pill').forEach(b => {
            b.classList.remove('active');
            b.setAttribute('aria-selected', 'false');
          });
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');
          currentDistrict = btn.getAttribute('data-district');
          filterStores();
        });
      });

      // Tier 2: Status Filter Pills
      document.querySelectorAll('.status-pill').forEach((btn) => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.status-pill').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentStatus = btn.getAttribute('data-status');
          filterStores();
        });
      });

      // Search toggle
      const btnSearchToggle = document.getElementById('btn-toggle-search');
      const searchPanel = document.getElementById('fm-search-panel');
      const searchInput = document.getElementById('fm-search-input');
      const clearBtn = document.getElementById('fm-clear-search');

      if (btnSearchToggle && searchPanel) {
        btnSearchToggle.addEventListener('click', (e) => {
          e.preventDefault();
          const isOpen = searchPanel.style.display !== 'none';
          searchPanel.style.display = isOpen ? 'none' : 'block';
          if (!isOpen && searchInput) searchInput.focus();
        });
      }

      if (searchInput) {
        searchInput.addEventListener('input', (e) => {
          currentSearch = e.target.value;
          filterStores();
        });
      }

      if (clearBtn && searchInput) {
        clearBtn.addEventListener('click', () => {
          searchInput.value = '';
          currentSearch = '';
          filterStores();
        });
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', setupEventListeners);
    } else {
      setupEventListeners();
    }
  </script>
</BaseLayout>

<style>
  /* FamilyMart Green & Blue Modern Palette */
  :root {
    --fm-green: #00A040;
    --fm-green-dark: #008234;
    --fm-green-light: #E8F5E9;
    --fm-blue: #0070C0;
    --fm-blue-dark: #005696;
    --fm-blue-light: #E1F0FA;
    --fm-text: #1E293B;
    --fm-muted: #64748B;
    --fm-border: #E2E8F0;
    --fm-card-bg: #FFFFFF;
    --fm-bg: #F8FAFC;
  }

  :global(html) {
    overflow-x: hidden !important;
    max-width: 100vw !important;
    width: 100% !important;
  }

  :global(body) {
    overflow-x: hidden !important;
    max-width: 100vw !important;
    width: 100% !important;
    position: relative;
  }

  .fm-page {
    background: var(--fm-bg);
    min-height: 100vh;
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
    padding-top: var(--nav-height, 64px);
    padding-bottom: 4rem;
    color: var(--fm-text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", sans-serif;
  }

  /* Structural containment for all sections */
  .fm-hero,
  .fm-hero__inner,
  .fm-main,
  .fm-container,
  .geosim-intro-section,
  .how-to-use-section {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  html.is-embed .fm-page {
    padding-top: 0 !important;
  }

  /* Hero Section */
  .fm-hero {
    background: linear-gradient(135deg, #00A040 0%, #008234 40%, #0070C0 100%);
    color: #FFFFFF;
    padding: 2.2rem 1rem 1.6rem;
    box-shadow: 0 4px 16px rgba(0, 160, 64, 0.18);
  }

  .fm-hero__inner {
    max-width: 1080px;
    margin: 0 auto;
  }

  .fm-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.75rem;
  }

  .fm-badge {
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.2rem 0.65rem;
    border-radius: 9999px;
    letter-spacing: 0.02em;
  }

  .fm-badge--green {
    background: rgba(255, 255, 255, 0.95);
    color: #008234;
  }

  .fm-badge--blue {
    background: rgba(0, 112, 192, 0.9);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.4);
  }

  .fm-badge--gold {
    background: #FFD700;
    color: #854D0E;
    font-weight: 800;
  }

  .fm-title {
    font-size: 1.65rem;
    font-weight: 900;
    color: #FFFFFF !important;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    margin: 0 0 0.45rem;
    line-height: 1.25;
    letter-spacing: -0.02em;
  }

  .fm-title__highlight {
    background: #FFD700;
    color: #1E293B !important;
    text-shadow: none !important;
    padding: 0.05rem 0.5rem;
    border-radius: 6px;
    margin-left: 0.2rem;
  }

  .fm-subtitle {
    font-size: 0.92rem;
    color: #FFFFFF !important;
    opacity: 0.95;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    margin: 0 0 1.2rem;
    line-height: 1.5;
  }

  /* Stats Bar */
  .fm-stats-bar {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.4rem;
    width: 100%;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 12px;
    padding: 0.65rem 0.6rem;
    margin-bottom: 1.1rem;
  }

  .fm-stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .fm-stat-val {
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.1;
    color: #FFFFFF !important;
  }

  .fm-stat-lbl {
    font-size: 0.72rem;
    color: #FFFFFF !important;
    opacity: 0.95;
    margin-top: 0.15rem;
  }

  /* Tier 1: District Filter Pills */
  .tier-district-bar {
    display: flex;
    gap: 0.45rem;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow-x: auto !important;
    overscroll-behavior-x: contain !important;
    -webkit-overflow-scrolling: touch !important;
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
  }

  .district-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.42rem 0.88rem;
    border-radius: 9999px;
    font-size: 0.9rem;
    font-weight: 700;
    border: 1px solid rgba(255, 255, 255, 0.45);
    background: rgba(255, 255, 255, 0.22);
    color: #FFFFFF !important;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s ease;
    flex-shrink: 0;
  }
  .district-pill:hover {
    background: rgba(255, 255, 255, 0.32);
  }
  .district-pill.active {
    background: #FFFFFF !important;
    color: #008234 !important;
    border-color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
  .district-pill .pill-count {
    font-size: 0.76rem;
    opacity: 0.9;
    background: rgba(0, 0, 0, 0.22);
    color: #FFFFFF !important;
    padding: 0.08rem 0.42rem;
    border-radius: 9999px;
  }
  .district-pill.active .pill-count {
    background: #E8F5E9 !important;
    color: #008234 !important;
  }

  /* Tier 2: Status Pills */
  .tier-status-bar {
    display: flex;
    gap: 0.4rem;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow-x: auto !important;
    overscroll-behavior-x: contain !important;
    padding-bottom: 0.4rem;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch !important;
    margin-bottom: 0.9rem;
  }
  .tier-status-bar::-webkit-scrollbar {
    display: none;
  }

  .status-pill {
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid rgba(255, 255, 255, 0.35);
    background: rgba(0, 0, 0, 0.25);
    color: #FFFFFF !important;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s ease;
    flex-shrink: 0;
  }
  .status-pill.active {
    background: #FFD700 !important;
    color: #1E293B !important;
    border-color: #FFD700 !important;
    font-weight: 800;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

  /* Action Tools Bar */
  .fm-tools-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    width: 100%;
    box-sizing: border-box;
  }

  @media (max-width: 520px) {
    .fm-tools-bar {
      flex-direction: column;
    }
    .fm-btn {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }

  .fm-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 1.1rem;
    border-radius: 10px;
    font-size: 0.92rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    transition: all 0.15s ease;
  }

  .fm-btn--primary {
    background: #FFFFFF;
    color: #008234;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }
  .fm-btn--primary:hover {
    background: #F8FAFC;
    transform: translateY(-1px);
  }

  .fm-btn--outline {
    background: rgba(255, 255, 255, 0.18);
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.5);
  }
  .fm-btn--outline:hover {
    background: rgba(255, 255, 255, 0.28);
  }

  /* Search Panel */
  .fm-search-panel {
    margin-top: 0.8rem;
  }
  .search-input-wrap {
    position: relative;
    display: flex;
    align-items: center;
  }
  .fm-search-input {
    width: 100%;
    padding: 0.65rem 2.2rem 0.65rem 0.95rem;
    border-radius: 10px;
    border: 1px solid #CBD5E1;
    font-size: 0.92rem;
    outline: none;
    background: #FFFFFF;
    color: #1E293B;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
  .fm-search-input:focus {
    border-color: #00A040;
    box-shadow: 0 0 0 3px rgba(0, 160, 64, 0.2);
  }
  .fm-clear-btn {
    position: absolute;
    right: 0.75rem;
    background: none;
    border: none;
    color: #94A3B8;
    cursor: pointer;
    font-size: 1rem;
    padding: 0.2rem;
  }

  /* Main Container */
  .fm-main {
    max-width: 1080px;
    margin: 0 auto;
    padding: 1.2rem 1rem 3rem;
  }

  .fm-results-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.1rem;
    font-size: 0.85rem;
    color: var(--fm-muted);
  }

  .fm-legend {
    display: flex;
    gap: 0.8rem;
  }
  .legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.78rem;
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 9999px;
  }
  .dot-todo { background: #94A3B8; }
  .dot-cooling { background: #00A040; }
  .dot-ready { background: #EAB308; }

  /* District Section */
  .district-section {
    margin-bottom: 2rem;
  }

  .district-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.55rem;
    margin-bottom: 1rem;
  }

  .district-header__left {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  .district-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0;
  }

  .district-store-count {
    font-size: 0.85rem;
    color: #64748B;
    background: #F1F5F9;
    padding: 0.15rem 0.55rem;
    border-radius: 9999px;
    font-weight: 600;
  }

  .btn-copy-district-route {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 700;
    border: 1px solid #CBD5E1;
    background: #FFFFFF;
    color: #008234;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .btn-copy-district-route:hover {
    border-color: #00A040;
    background: #F0FDF4;
  }

  /* Store Card Grid */
  .store-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 0.85rem;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }

  .store-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 0.95rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.18s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    overflow-x: hidden !important;
  }

  .store-card:hover {
    border-color: #00A040;
    box-shadow: 0 4px 12px rgba(0, 160, 64, 0.12);
    transform: translateY(-2px);
  }

  /* Card Head */
  .card-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
  }

  .check-toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 700;
    color: #64748B;
    user-select: none;
  }

  .check-toggle__input {
    display: none;
  }

  .check-toggle__box {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid #CBD5E1;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
    background: #FFFFFF;
  }

  .check-icon {
    display: none;
    color: #FFFFFF;
  }

  .check-toggle__input:checked + .check-toggle__box {
    background: #00A040;
    border-color: #00A040;
  }

  .check-toggle__input:checked + .check-toggle__box .check-icon {
    display: block;
  }

  .store-name-box {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    max-width: 65%;
  }

  .store-name {
    font-size: 1.05rem;
    font-weight: 800;
    margin: 0;
    color: #0F172A;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .store-badge-fami {
    font-size: 0.72rem;
    font-weight: 800;
    background: #E8F5E9;
    color: #008234;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    flex-shrink: 0;
  }

  /* Cooldown Banner */
  .cooldown-banner {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.65rem;
    border-radius: 6px;
    font-size: 0.78rem;
    margin-bottom: 0.6rem;
    font-weight: 600;
  }

  .is-cooling-badge {
    background: #E8F5E9;
    color: #008234;
    border: 1px solid #A7F3D0;
  }

  .is-ready-badge {
    background: #FEF3C7;
    color: #B45309;
    border: 1px solid #FDE68A;
  }

  /* Card Body */
  .card-body {
    margin-bottom: 0.8rem;
  }

  .addr-row {
    display: flex;
    align-items: flex-start;
    gap: 0.35rem;
    font-size: 0.82rem;
    color: #475569;
    margin-bottom: 0.45rem;
    line-height: 1.35;
  }

  .addr-icon {
    color: #94A3B8;
    margin-top: 0.15rem;
    flex-shrink: 0;
  }

  .addr-text {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .coord-row {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    background: #F8FAFC;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    border: 1px solid #F1F5F9;
  }

  .coord-label {
    color: #94A3B8;
    font-weight: 600;
  }

  .coord-code {
    font-family: monospace;
    font-size: 0.82rem;
    color: #334155;
    font-weight: 600;
  }

  .btn-copy-coord {
    margin-left: auto;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    font-size: 0.75rem;
    padding: 0.1rem 0.45rem;
    color: #475569;
    cursor: pointer;
    font-weight: 600;
  }
  .btn-copy-coord:hover {
    border-color: #00A040;
    color: #00A040;
  }

  /* Card Actions */
  .card-actions {
    display: grid;
    grid-template-columns: 1fr 1.2fr auto;
    gap: 0.35rem;
  }

  .btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
    padding: 0.42rem 0.55rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    text-decoration: none;
    border: 1px solid transparent;
    transition: all 0.15s ease;
  }

  .btn-pikmin {
    background: #E8F5E9;
    color: #008234;
    border-color: #C6F6D5;
  }
  .btn-pikmin:hover {
    background: #00A040;
    color: #FFFFFF;
  }

  .btn-geosim {
    background: #E0F2FE;
    color: #0284C7;
    border-color: #BAE6FD;
  }
  .btn-geosim:hover {
    background: #0284C7;
    color: #FFFFFF;
  }

  .btn-gmap {
    background: #F1F5F9;
    color: #475569;
    border-color: #E2E8F0;
    padding: 0.42rem 0.65rem;
  }
  .btn-gmap:hover {
    background: #E2E8F0;
    color: #1E293B;
  }

  /* Toast */
  .copy-toast {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: #1E293B;
    color: #FFFFFF;
    padding: 0.75rem 1.4rem;
    border-radius: 9999px;
    font-size: 0.9rem;
    font-weight: 700;
    opacity: 0;
    visibility: hidden;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
    z-index: 9999;
    max-width: 90vw;
    text-align: center;
  }
  .copy-toast.show {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
  }

  .no-results-box {
    text-align: center;
    padding: 3rem 1rem;
    color: #64748B;
  }

  @media (max-width: 640px) {
    .fm-title {
      font-size: 1.35rem;
    }
    .fm-stats-bar {
      grid-template-columns: repeat(2, 1fr);
    }
    .store-grid {
      grid-template-columns: 1fr;
    }
  }

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
    color: #334155;
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
    color: #334155;
    line-height: 1.55;
    margin: 0;
  }


  /* Top Sticky Version & Live Update Notification Banner */
  .top-sticky-version-wrapper {
    position: sticky;
    top: var(--nav-height, 64px);
    left: 0;
    right: 0;
    width: 100%;
    z-index: 990;
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    transition: all 0.25s ease;
  }

  html.is-embed .top-sticky-version-wrapper {
    top: 0 !important;
  }
  .top-sticky-version-wrapper.has-update {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%) !important;
    border-bottom: 2px solid #F59E0B !important;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(245, 158, 11, 0.25) !important;
  }

  .top-sticky-version-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0.35rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    min-height: 38px;
  }

  .top-sticky-version-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 0;
    flex: 1;
  }

  .version-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    display: inline-block;
    flex-shrink: 0;
  }
  .version-dot.has-update {
    background: #D97706 !important;
    box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.35) !important;
    animation: dot-pulse 1.2s infinite ease-in-out;
  }
  @keyframes dot-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.35); opacity: 0.7; }
  }

  .version-tag {
    background: #ECFDF5;
    color: #065F46;
    font-weight: 800;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    font-size: 0.76rem;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .version-tag.has-update {
    background: #B45309 !important;
    color: #FFFFFF !important;
    animation: tag-attention 1s infinite alternate ease-in-out;
  }
  @keyframes tag-attention {
    from { transform: scale(1); }
    to { transform: scale(1.05); }
  }

  .version-marquee-box {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .version-ticker-text {
    font-size: 0.8rem;
    color: #475569;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }
  .version-ticker-text.has-update {
    color: #92400E !important;
    font-weight: 700;
  }

  .ticker-badge {
    background: #E2E8F0;
    color: #334155;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.05rem 0.35rem;
    border-radius: 4px;
  }
  .ticker-badge.has-update {
    background: #F59E0B !important;
    color: #FFFFFF !important;
  }

  .btn-top-refresh {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    color: #334155;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.3rem 0.65rem;
    border-radius: 8px;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.15s ease;
  }
  .btn-top-refresh:hover {
    background: #E2E8F0;
    border-color: #94A3B8;
    color: #0F172A;
  }
  .btn-top-refresh.has-update {
    background: #D97706 !important;
    color: #FFFFFF !important;
    border-color: #B45309 !important;
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.4) !important;
  }
  .btn-top-refresh.is-refreshing .refresh-icon {
    animation: spin-refresh 0.8s linear infinite;
  }
  @keyframes spin-refresh {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @media (max-width: 640px) {
    .version-marquee-box {
      display: none;
    }
  }

</style>
"""

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Generated {target_path} successfully!")

if __name__ == '__main__':
    generate_page(is_staging=True)
    generate_page(is_staging=False)
