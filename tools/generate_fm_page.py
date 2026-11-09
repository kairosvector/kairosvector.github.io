# -*- coding: utf-8 -*-
"""
Generator for FamilyMart Pikmin 5th Anniversary Event Page
Features:
1. Recommended Hot High-Density Routes (6 major commercial swarm clusters in Taipei)
2. Complete Taipei City Store Directory (696 stores across 12 districts)
3. Advanced Search & 7-Day Cooldown Tracker
4. One-click Route Queue Copy & GeoSim Direct Teleport
"""
import os
import sys

def generate_page(is_staging=True):
    target_path = 'app/src/pages/events/familymart-pikmin/staging.astro' if is_staging else 'app/src/pages/events/familymart-pikmin/index.astro'

    staging_banner = '''<!-- Staging Environment Indicator Banner -->
    <div style="background: #FEF3C7; border-bottom: 2px solid #F59E0B; padding: 0.5rem 1rem; text-align: center; font-size: 0.875rem; font-weight: 700; color: #92400E; z-index: 50; position: relative;">
      [測試預覽環境 Staging] 此頁面用於驗證新功能，測試完畢確認無誤後將同步發布至正式版。
    </div>''' if is_staging else ''

    code = """---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import stores from '../../../data/fm_taipei_stores.json';
import hotRoutes from '../../../data/fm_hot_routes.json';

const title = `全家便利商店 x Pikmin Bloom 五週年黃金巡航地圖 (台北市 696 店) | GeoSim`;
const description = `2026/11/10 ~ 12/7 Pikmin Bloom 五週年全家便利商店聯名特別地點！精選台北市 6 大高密度黃金刷苗圈、696 間門市 GPS 精準座標、12 行政區篩選、7 天冷卻狀態追蹤、一鍵複製巡航佇列、直接喚醒 Pikmin Bloom / GeoSim。`;

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
    <!-- Top Sticky Version & Live Update Notification Banner (Fixed right below Title Bar) -->
    <div class="top-sticky-version-wrapper" id="fm-version-card" data-batch-id="1" data-store-count={stores.length}>
      <div class="top-sticky-version-inner">
        <div class="top-sticky-version-left">
          <span class="version-dot" id="version-dot" aria-hidden="true"></span>
          <span class="version-tag" id="version-badge">台北 {stores.length} 店最新</span>
          <div class="version-marquee-box" id="version-marquee-box">
            <span class="version-ticker-text" id="version-ticker">
              <span class="ticker-badge">最新</span>初始建置 · 台北市 12 行政區 {stores.length} 間全家門市座標全齊
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
    <div class="top-sticky-spacer" aria-hidden="true"></div>
    """ + staging_banner + """

    <!-- Top Fixed Hero Header -->
    <header class="fm-hero">
      <div class="fm-hero__inner">
        <div class="fm-badge-row">
          <span class="fm-badge fm-badge--green">Pikmin Bloom x 全家便利商店</span>
          <span class="fm-badge fm-badge--blue">五週年紀念聯名 · 特別地點</span>
          <span class="fm-badge fm-badge--gold">7 款零食金色花苗</span>
        </div>
        <h1 class="fm-hero__title">
          全家便利商店 x Pikmin Bloom <span class="fm-title-gradient">五週年巡航地圖</span>
        </h1>
        <p class="fm-hero__desc">
          2026/11/10 ~ 12/7 期間，全家便利商店門市皆有金色花苗特別地點！為您精算<strong>台北市 6 大高密度黃金巡航圈</strong>與 <strong>696 間門市精準座標</strong>，支援一鍵複製巡航、7 天冷卻倒數與 GeoSim 一鍵直飛。
        </p>
      </div>
    </header>

    <!-- SECTION 1: Recommended Hot High-Density Routes -->
    <section class="hot-routes-section" id="hot-routes">
      <div class="container hot-routes-container">
        <div class="hot-routes-header">
          <div class="hot-routes-title-box">
            <span class="hot-routes-kicker">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 23c-4.97 0-9-4.03-9-9 0-3.8 2.37-7.06 5.75-8.35.5-.19.98.24.91.77-.47 3.51 1.7 4.96 2.34 5.34.4.24.92-.02.94-.49.07-2.1.8-4.52 2.76-6.44.38-.37 1-.16 1.11.35.7 3.25 2.62 4.41 3.19 5.32C20.67 11.66 21 12.8 21 14c0 4.97-4.03 9-9 9z"/></svg>
              效率專區
            </span>
            <h2 class="hot-routes-title">推薦熱門高密度巡航路線</h2>
          </div>
          <p class="hot-routes-subdesc">
            全家門市眾多，不用盲目奔波！由演算法依最短路徑規劃出台北市密度最高、站距最近的 6 條黃金刷苗圈，一鍵複製隊列直接開刷：
          </p>
        </div>

        <div class="hot-routes-grid">
          {hotRoutes.map((route, rIdx) => (
            <div class="hot-route-card" data-route-id={route.id}>
              <div class="hot-route-top">
                <div class="hot-route-badge-row">
                  <span class="hot-route-tag" style={`background: ${route.tagColor}15; color: ${route.tagColor}; border: 1px solid ${route.tagColor}35;`}>
                    {route.tag}
                  </span>
                  <span class="hot-route-rank">TOP {rIdx + 1}</span>
                </div>
                <h3 class="hot-route-title">{route.title}</h3>
                <p class="hot-route-subtitle">{route.subtitle}</p>
              </div>

              <!-- Stats Bar -->
              <div class="hot-route-stats">
                <div class="stat-col">
                  <span class="stat-val stat-val--green">{route.storeCount}</span>
                  <span class="stat-lbl">間全家門市</span>
                </div>
                <div class="stat-sep"></div>
                <div class="stat-col">
                  <span class="stat-val">{route.totalKm}</span>
                  <span class="stat-lbl">公里總長</span>
                </div>
                <div class="stat-sep"></div>
                <div class="stat-col">
                  <span class="stat-val">{route.avgGapMeters}m</span>
                  <span class="stat-lbl">平均站距</span>
                </div>
              </div>

              <p class="hot-route-desc">{route.desc}</p>

              <!-- Sample Stores Pill Bar -->
              <div class="hot-route-samples">
                <span class="samples-title">精選途經：</span>
                <div class="samples-pills">
                  {route.sampleStores.map(name => (
                    <span class="sample-pill">{name}</span>
                  ))}
                  <span class="sample-more">...等 {route.storeCount} 店</span>
                </div>
              </div>

              <!-- Actions -->
              <div class="hot-route-actions">
                <button
                  type="button"
                  class="btn-copy-hot-route"
                  data-route={route.routeText}
                  data-title={route.title}
                  data-count={route.storeCount}
                  title="一鍵複製本路線所有門市座標隊列"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                  <span>複製這條巡航隊列</span>
                </button>

                <button
                  type="button"
                  class="btn-hot-geosim btn-launch-geosim"
                  data-lat={route.firstStore.lat}
                  data-lng={route.firstStore.lng}
                  data-name={route.firstStore.name}
                  data-coords={route.firstStore.coordsText}
                  title="用 GeoSim 直接定位直飛這條路線起點"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path></svg>
                  <span>直飛起點</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>

    <!-- SECTION 2: Complete Taipei City Store Directory & Filter -->
    <main class="fm-main">
      <div class="container">
        <!-- Section Title -->
        <div class="directory-section-header">
          <div class="directory-title-wrap">
            <span class="directory-badge">全區查詢</span>
            <h2 class="directory-title">台北市全區門市查詢與冷卻追蹤</h2>
          </div>
          <p class="directory-desc">
            台北市共 12 行政區、696 間門市。支援店名/地址模糊搜尋、冷卻狀態打勾記錄與行政區一鍵巡航複製：
          </p>
        </div>

        <!-- Sticky Controls Bar -->
        <div class="fm-controls-card">
          <!-- Search Row -->
          <div class="fm-search-row">
            <div class="fm-search-wrap">
              <svg class="fm-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <input
                type="text"
                id="fm-search-input"
                class="fm-search-input"
                placeholder="搜尋門市名稱、街道地址（例：市民、中山北路、西門）..."
                autocomplete="off"
              />
              <button id="fm-clear-search" class="fm-clear-btn" type="button" aria-label="清除搜尋" style="display: none;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          </div>

          <!-- Tier 1: District Filter Pills (Horizontal Scroll on Mobile) -->
          <div class="tier-district-bar" role="tablist" aria-label="台北市行政區篩選">
            {districts.map(d => (
              <button
                class={`district-pill ${d.id === 'all' ? 'active' : ''}`}
                data-district={d.id}
                role="tab"
                aria-selected={d.id === 'all' ? 'true' : 'false'}
              >
                <span>{d.name}</span>
                <span class="pill-count">{d.count}</span>
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
              <svg class="fm-btn-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              <span id="btn-copy-label">複製目前篩選巡航路徑 ({stores.length})</span>
            </button>

            <button id="btn-mark-all-cooling" class="fm-btn fm-btn--outline" title="將目前篩選的門市全部標記為已造訪進入 7 天冷卻">
              <svg class="fm-btn-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>
              <span>目前篩選全部打勾</span>
            </button>

            <button id="btn-reset-cooldown" class="fm-btn fm-btn--ghost" title="重置本機所有門市的冷卻狀態">
              <svg class="fm-btn-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
              <span>重置冷卻記錄</span>
            </button>
          </div>
        </div>

        <!-- Store Groups List (By District) -->
        {districtGroups.map(group => (
          <section class="district-section" data-district-section={group.name}>
            <div class="district-section__header">
              <div class="district-title-wrap">
                <h2 class="district-title">{group.name}</h2>
                <span class="district-count-tag">{group.count} 間門市</span>
              </div>
              <button
                type="button"
                class="btn-copy-district-route"
                data-district-name={group.name}
                title={`複製【${group.name}】目前門市巡航隊列`}
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                <span class="btn-district-copy-label">複製【{group.name}】巡航 ({group.count})</span>
              </button>
            </div>

            <div class="store-grid">
              {group.stores.map(store => (
                <article
                  class="store-card"
                  data-store-id={store.id}
                  data-district={store.district}
                  data-name={store.name}
                  data-address={store.address}
                  data-lat={store.lat}
                  data-lng={store.lng}
                >
                  <!-- Card Header -->
                  <div class="store-card__header">
                    <div class="store-name-box">
                      <h3 class="store-name" title={store.name}>
                        {store.shortName}
                      </h3>
                      <span class="store-badge-fami">全家</span>
                    </div>

                    <!-- 7-Day Cooldown Toggle Checkbox -->
                    <label class="check-toggle" title="標記已造訪並開始 7 天冷卻倒數">
                      <input
                        type="checkbox"
                        class="check-toggle__input"
                        data-store-id={store.id}
                        aria-label={`記錄造訪 ${store.shortName} 並啟動 7 天冷卻`}
                      />
                      <span class="check-toggle__label">
                        <span class="check-box-icon">
                          <svg class="check-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        </span>
                        <span class="check-text">7天冷卻</span>
                      </span>
                    </label>
                  </div>

                  <!-- 7-Day Cooldown Notice Banner -->
                  <div class="cooldown-banner" style="display: none;">
                    <span class="cooldown-icon"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 22h14"></path><path d="M5 2h14"></path><path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22"></path><path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"></path></svg></span>
                    <span class="cooldown-text">7 天冷卻中（剩餘 6 天 23 小時）</span>
                  </div>

                  <!-- Card Body -->
                  <div class="card-body">
                    <div class="addr-row" title={store.address}>
                      <svg class="addr-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                      <span class="addr-text">{store.address}</span>
                    </div>

                    <div class="coord-row">
                      <span class="coord-tag">GPS</span>
                      <code class="coord-val">{store.coordsText}</code>
                      <button
                        type="button"
                        class="btn-copy-single"
                        data-coords={store.coordsText}
                        data-name={store.shortName}
                        title="複製這間門市的經緯度座標"
                      >
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <span>複製</span>
                      </button>
                    </div>
                  </div>

                  <!-- Card Actions (Direct Launch & Navigation) -->
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
          <div class="no-results-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          </div>
          <h3>找不到符合的台北市全家門市</h3>
          <p>請嘗試其他關鍵字（例如捷運站名或街道名），或清除搜尋關鍵字。</p>
          <button id="btn-clear-search-fallback" class="fm-btn fm-btn--outline" type="button">清除篩選條件</button>
        </div>
      </div>
    </main>

    <!-- Floating Quick Copy Toast -->
    <div id="copy-toast" class="copy-toast" role="alert" aria-live="polite"></div>
  </div>

  <!-- Client Script -->
  <script is:inline>
    const STORAGE_KEY_PREFIX = 'fm_visited_tpe_';
    const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;
    const PLAY_STORE_URL = 'https://play.google.com/store/apps/details?id=com.kairosvector.geosim';

    let currentDistrict = 'all';
    let currentStatus = 'all';
    let currentSearch = '';

    // ==========================================================================
    // Force Refresh & Version Checking Logic
    // ==========================================================================
    function triggerForceRefresh() {
      const btn = document.getElementById('btn-force-refresh');
      if (btn) btn.classList.add('is-refreshing');

      const url = new URL(window.location.href);
      url.searchParams.set('_t', Date.now().toString());

      if ('caches' in window) {
        caches.keys().then((names) => {
          return Promise.all(names.map((n) => caches.delete(n)));
        }).catch(() => {}).finally(() => {
          window.location.replace(url.toString());
        });
      } else {
        window.location.replace(url.toString());
      }
    }

    function showUpdateBanner(remote) {
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
        badge.textContent = '發現新資料！';
        badge.classList.add('has-update');
      }
      if (ticker) {
        ticker.innerHTML = '<span class="ticker-badge has-update">新發布</span><strong>' + (remote.description || '最新門市資料已更新') + '</strong> &rarr; <span style="text-decoration: underline;">點此立即更新</span>';
        ticker.classList.add('has-update');
      }
      if (btn) {
        btn.classList.add('has-update');
        const label = btn.querySelector('.refresh-label');
        if (label) label.textContent = '點我立即更新';
        btn.setAttribute('title', '已有新更新發布，請點此強制重整載入最新點位！');
      }
    }

    function checkRemoteVersion() {
      const card = document.getElementById('fm-version-card');
      if (!card) return;
      const localBatch = parseInt(card.getAttribute('data-batch-id') || '0', 10);
      const localCount = parseInt(card.getAttribute('data-store-count') || '0', 10);

      fetch('/events/fm-meta.json?t=' + Date.now(), { cache: 'no-cache' })
        .then((res) => {
          if (!res.ok) throw new Error('No remote meta');
          return res.json();
        })
        .then((remote) => {
          if (remote.batchId > localBatch || remote.storeCount > localCount) {
            showUpdateBanner(remote);
          }
        })
        .catch(() => {});
    }

    // ==========================================================================
    // Toast Notification
    // ==========================================================================
    let toastTimer = null;
    function showToast(msg) {
      const toast = document.getElementById('copy-toast');
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add('show');
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, 3000);
    }

    // ==========================================================================
    // Filter Stores Function
    // ==========================================================================
    function filterStores() {
      let visibleCount = 0;
      const term = currentSearch.toLowerCase().trim();

      document.querySelectorAll('.district-section').forEach((sec) => {
        const secDist = sec.getAttribute('data-district-section');
        const isDistMatch = (currentDistrict === 'all' || currentDistrict === secDist);

        let distVisibleCount = 0;
        const visibleCards = [];

        sec.querySelectorAll('.store-card').forEach((card) => {
          const sName = (card.getAttribute('data-name') || '').toLowerCase();
          const sAddr = (card.getAttribute('data-address') || '').toLowerCase();
          const sStatus = card.getAttribute('data-status-state') || 'todo';

          const isSearchMatch = !term || sName.includes(term) || sAddr.includes(term) || secDist.includes(term);
          const isStatusMatch = (currentStatus === 'all' || currentStatus === sStatus);

          if (isDistMatch && isSearchMatch && isStatusMatch) {
            card.style.display = 'flex';
            distVisibleCount++;
            visibleCount++;
            visibleCards.push(card);
          } else {
            card.style.display = 'none';
          }
        });

        if (distVisibleCount > 0) {
          sec.style.display = 'block';
        } else {
          sec.style.display = 'none';
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

      // No results fallback
      const noResults = document.getElementById('no-results-box');
      if (noResults) {
        noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      }
    }

    // ==========================================================================
    // Update Cooldown State for Store Card
    // ==========================================================================
    function updateCardState(card, storeId) {
      const recordStr = localStorage.getItem(STORAGE_KEY_PREFIX + storeId);
      const cb = card.querySelector('.check-toggle__input');
      const banner = card.querySelector('.cooldown-banner');
      const bannerText = card.querySelector('.cooldown-text');

      if (!recordStr) {
        card.setAttribute('data-status-state', 'todo');
        if (cb) cb.checked = false;
        if (banner) banner.style.display = 'none';
        return 'todo';
      }

      const visitedTime = parseInt(recordStr, 10);
      const now = Date.now();
      const elapsed = now - visitedTime;

      if (elapsed < SEVEN_DAYS_MS) {
        card.setAttribute('data-status-state', 'cooling');
        if (cb) cb.checked = true;
        if (banner) {
          banner.style.display = 'flex';
          banner.className = 'cooldown-banner is-cooling-badge';
          const remainingMs = SEVEN_DAYS_MS - elapsed;
          const remainingDays = Math.floor(remainingMs / (24 * 60 * 60 * 1000));
          const remainingHours = Math.floor((remainingMs % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));
          if (bannerText) {
            bannerText.textContent = `7 天冷卻中（剩餘 ${remainingDays} 天 ${remainingHours} 小時）`;
          }
        }
        return 'cooling';
      } else {
        card.setAttribute('data-status-state', 'ready');
        if (cb) cb.checked = true;
        if (banner) {
          banner.style.display = 'flex';
          banner.className = 'cooldown-banner is-ready-badge';
          if (bannerText) {
            bannerText.textContent = `冷卻完畢！可再次前往領取`;
          }
        }
        return 'ready';
      }
    }

    function updateAllStoreStates() {
      let countTodo = 0;
      let countCooling = 0;
      let countReady = 0;

      document.querySelectorAll('.store-card').forEach((card) => {
        const sid = card.getAttribute('data-store-id');
        const st = updateCardState(card, sid);
        if (st === 'todo') countTodo++;
        else if (st === 'cooling') countCooling++;
        else if (st === 'ready') countReady++;
      });

      const elTodo = document.getElementById('count-todo');
      const elCooling = document.getElementById('count-cooling');
      const elReady = document.getElementById('count-ready');

      if (elTodo) elTodo.textContent = `${countTodo}`;
      if (elCooling) elCooling.textContent = `${countCooling}`;
      if (elReady) elReady.textContent = `${countReady}`;
    }

    // ==========================================================================
    // Event Handlers Setup
    // ==========================================================================
    function setupEventHandlers() {
      // 1. Copy Hot Route Queue Button
      document.querySelectorAll('.btn-copy-hot-route').forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const route = btn.getAttribute('data-route') || '';
          const title = btn.getAttribute('data-title') || '熱門路線';
          const count = btn.getAttribute('data-count') || '';
          if (!route) return;
          navigator.clipboard.writeText(route).then(() => {
            showToast(`已成功複製【${title}】${count} 間全家巡航隊列！`);
          }).catch(() => {
            showToast('複製失敗，請手動複製');
          });
        });
      });

      // 2. Cooldown Checkbox toggle
      document.querySelectorAll('.check-toggle__input').forEach((cb) => {
        cb.addEventListener('change', (e) => {
          const sid = cb.getAttribute('data-store-id');
          const card = cb.closest('.store-card');
          if (cb.checked) {
            localStorage.setItem(STORAGE_KEY_PREFIX + sid, Date.now().toString());
          } else {
            localStorage.removeItem(STORAGE_KEY_PREFIX + sid);
          }
          if (card) updateCardState(card, sid);
          updateAllStoreStates();
          filterStores();
        });
      });

      // 3. Search Input
      const searchInput = document.getElementById('fm-search-input');
      const clearBtn = document.getElementById('fm-clear-search');
      if (searchInput) {
        searchInput.addEventListener('input', () => {
          currentSearch = searchInput.value;
          if (clearBtn) clearBtn.style.display = currentSearch ? 'inline-flex' : 'none';
          filterStores();
        });
      }
      if (clearBtn && searchInput) {
        clearBtn.addEventListener('click', () => {
          searchInput.value = '';
          currentSearch = '';
          clearBtn.style.display = 'none';
          filterStores();
          searchInput.focus();
        });
      }

      // 4. District Pill Click
      document.querySelectorAll('.district-pill').forEach((btn) => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.district-pill').forEach((b) => {
            b.classList.remove('active');
            b.setAttribute('aria-selected', 'false');
          });
          btn.classList.add('active');
          btn.setAttribute('aria-selected', 'true');
          currentDistrict = btn.getAttribute('data-district') || 'all';
          filterStores();
        });
      });

      // 5. Status Pill Click
      document.querySelectorAll('.status-pill').forEach((btn) => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('.status-pill').forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');
          currentStatus = btn.getAttribute('data-status') || 'all';
          filterStores();
        });
      });

      // 6. Copy Filtered Route
      const btnCopyFiltered = document.getElementById('btn-copy-filtered-route');
      if (btnCopyFiltered) {
        btnCopyFiltered.addEventListener('click', () => {
          const coordsList = [];
          document.querySelectorAll('.store-card').forEach((card) => {
            if (card.style.display !== 'none') {
              const lat = card.getAttribute('data-lat');
              const lng = card.getAttribute('data-lng');
              if (lat && lng) coordsList.push(`${lat},${lng}`);
            }
          });
          if (coordsList.length === 0) {
            showToast('目前篩選無門市可複製');
            return;
          }
          const text = coordsList.join(' ');
          navigator.clipboard.writeText(text).then(() => {
            showToast(`已複製目前篩選的 ${coordsList.length} 間全家門市巡航隊列！`);
          }).catch(() => {
            showToast('複製失敗，請手動複製');
          });
        });
      }

      // 7. District Header Copy Route
      document.querySelectorAll('.btn-copy-district-route').forEach((btn) => {
        btn.addEventListener('click', () => {
          const sec = btn.closest('.district-section');
          if (!sec) return;
          const distName = btn.getAttribute('data-district-name') || '';
          const coordsList = [];
          sec.querySelectorAll('.store-card').forEach((card) => {
            if (card.style.display !== 'none') {
              const lat = card.getAttribute('data-lat');
              const lng = card.getAttribute('data-lng');
              if (lat && lng) coordsList.push(`${lat},${lng}`);
            }
          });
          if (coordsList.length === 0) {
            showToast(`【${distName}】目前篩選無門市可複製`);
            return;
          }
          const text = coordsList.join(' ');
          navigator.clipboard.writeText(text).then(() => {
            showToast(`已複製【${distName}】${coordsList.length} 間門市巡航隊列！`);
          }).catch(() => {
            showToast('複製失敗，請手動複製');
          });
        });
      });

      // 8. Single Copy Button
      document.querySelectorAll('.btn-copy-single').forEach((btn) => {
        btn.addEventListener('click', () => {
          const coords = btn.getAttribute('data-coords') || '';
          const name = btn.getAttribute('data-name') || '';
          navigator.clipboard.writeText(coords).then(() => {
            showToast(`已複製【${name}】座標 (${coords})`);
          }).catch(() => {
            showToast('複製失敗');
          });
        });
      });

      // 9. Launch Pikmin Bloom
      document.querySelectorAll('.btn-launch-pikmin').forEach((btn) => {
        btn.addEventListener('click', () => {
          const lat = btn.getAttribute('data-lat');
          const lng = btn.getAttribute('data-lng');
          const name = btn.getAttribute('data-name');
          launchPikminBloom(lat, lng, name);
        });
      });

      // 10. Launch GeoSim Direct
      document.querySelectorAll('.btn-launch-geosim').forEach((btn) => {
        btn.addEventListener('click', () => {
          const lat = btn.getAttribute('data-lat');
          const lng = btn.getAttribute('data-lng');
          const name = btn.getAttribute('data-name');
          const coords = btn.getAttribute('data-coords');
          launchGeoSim(lat, lng, name, coords);
        });
      });

      // 11. Mark All Currently Filtered as Visited
      const btnMarkAll = document.getElementById('btn-mark-all-cooling');
      if (btnMarkAll) {
        btnMarkAll.addEventListener('click', () => {
          const visible = [];
          document.querySelectorAll('.store-card').forEach((card) => {
            if (card.style.display !== 'none') {
              visible.push(card.getAttribute('data-store-id'));
            }
          });
          if (visible.length === 0) {
            showToast('目前無可標記之門市');
            return;
          }
          if (confirm(`確定要將目前篩選出的 ${visible.length} 間門市全部標記為「已造訪（進入 7 天冷卻）」嗎？`)) {
            const now = Date.now().toString();
            visible.forEach((sid) => {
              localStorage.setItem(STORAGE_KEY_PREFIX + sid, now);
            });
            updateAllStoreStates();
            filterStores();
            showToast(`已將 ${visible.length} 間門市全部標記為 7 天冷卻中！`);
          }
        });
      }

      // 12. Reset All Cooldown Records
      const btnReset = document.getElementById('btn-reset-cooldown');
      if (btnReset) {
        btnReset.addEventListener('click', () => {
          if (confirm('確定要清空所有門市的 7 天冷卻打勾記錄嗎？（清空後全部恢復為尚未前往）')) {
            Object.keys(localStorage).forEach((key) => {
              if (key.startsWith(STORAGE_KEY_PREFIX)) {
                localStorage.removeItem(key);
              }
            });
            updateAllStoreStates();
            filterStores();
            showToast('已清空所有門市冷卻記錄！');
          }
        });
      }

      // 13. Fallback clear filter
      const btnClearFallback = document.getElementById('btn-clear-search-fallback');
      if (btnClearFallback) {
        btnClearFallback.addEventListener('click', () => {
          if (searchInput) searchInput.value = '';
          currentSearch = '';
          if (clearBtn) clearBtn.style.display = 'none';
          currentDistrict = 'all';
          currentStatus = 'all';
          document.querySelectorAll('.district-pill').forEach((b) => {
            b.classList.toggle('active', b.getAttribute('data-district') === 'all');
          });
          document.querySelectorAll('.status-pill').forEach((b) => {
            b.classList.toggle('active', b.getAttribute('data-status') === 'all');
          });
          filterStores();
        });
      }

      // 14. Force Refresh Button
      const btnForceRefresh = document.getElementById('btn-force-refresh');
      if (btnForceRefresh) {
        btnForceRefresh.addEventListener('click', triggerForceRefresh);
      }
    }

    // ==========================================================================
    // App Launchers (GeoSim & Pikmin Bloom)
    // ==========================================================================
    function launchPikminBloom(lat, lng, name) {
      const encodedName = encodeURIComponent(name);
      const uri = `intent://geo:${lat},${lng}?q=${lat},${lng}(${encodedName})#Intent;scheme=geo;package=com.nianticlabs.pikmin;end`;
      const fallbackUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;

      const now = Date.now();
      window.location.href = uri;

      setTimeout(() => {
        if (Date.now() - now < 1500) {
          window.open(fallbackUrl, '_blank');
        }
      }, 1000);
    }

    function launchGeoSim(lat, lng, name, coords) {
      // 1. Android GeoSim WebView Bridge
      if (window.AndroidGeoSim && typeof window.AndroidGeoSim.setCoordinate === 'function') {
        try {
          window.AndroidGeoSim.setCoordinate(parseFloat(lat), parseFloat(lng), name);
          showToast(`已成功傳送【${name}】座標給 GeoSim！`);
          return;
        } catch (e) {
          console.warn('AndroidGeoSim bridge error:', e);
        }
      }

      // 2. Standard Deep Link via Android IntentFilter
      const encodedName = encodeURIComponent(name);
      const fallbackUrlEncoded = encodeURIComponent(PLAY_STORE_URL);
      const intentUri = `intent://location?lat=${lat}&lng=${lng}&label=${encodedName}#Intent;scheme=geosim;package=com.kairosvector.geosim;S.browser_fallback_url=${fallbackUrlEncoded};end`;

      // Copy coordinate to clipboard as backup
      if (coords) {
        navigator.clipboard.writeText(coords).catch(() => {});
      }

      const start = Date.now();
      window.location.href = intentUri;

      setTimeout(() => {
        if (Date.now() - start < 1500) {
          showToast(`已複製座標 (${coords})，若未安裝 GeoSim 將開啟商店下載`);
        }
      }, 1200);
    }

    // ==========================================================================
    // Initialization
    // ==========================================================================
    document.addEventListener('DOMContentLoaded', () => {
      updateAllStoreStates();
      setupEventHandlers();
      filterStores();
      checkRemoteVersion();
    });
  </script>
</BaseLayout>

<style>
  :global(html), :global(body) {
    overflow-x: hidden !important;
    max-width: 100vw !important;
  }

  .fm-page {
    min-height: 100vh;
    background: #F8FAFC;
    color: #0F172A;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding-bottom: 5rem;
    overflow-x: hidden !important;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    width: 100%;
    box-sizing: border-box;
  }

  /* Top Sticky Version & Live Update Notification Banner (Fixed right below Title Bar) */
  .top-sticky-version-wrapper {
    position: fixed !important;
    top: var(--nav-height, 64px) !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    height: 38px !important;
    z-index: 990 !important;
    background: #FFFFFF !important;
    border-bottom: 1px solid #E2E8F0 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
    display: flex !important;
    align-items: center !important;
    transition: background-color 0.2s ease, border-color 0.2s ease !important;
  }

  .top-sticky-spacer {
    height: 38px;
    width: 100%;
  }

  :global(html[data-theme="vibrant"]) .top-sticky-version-wrapper {
    background: #FFFFFF !important;
    border-bottom-color: #E2E8F0 !important;
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
    width: 100%;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 0.75rem !important;
    height: 100% !important;
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
  }

  .version-tag {
    font-size: 0.72rem;
    font-weight: 700;
    color: #047857;
    background: #D1FAE5;
    padding: 0.1rem 0.45rem;
    border-radius: 999px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .version-tag.has-update {
    background: #D97706 !important;
    color: #FFFFFF !important;
  }

  .version-marquee-box {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    min-width: 0;
    font-size: 0.78rem;
    color: #64748B;
  }

  .ticker-badge {
    background: #3B82F6;
    color: #FFFFFF;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
    margin-right: 0.35rem;
  }
  .ticker-badge.has-update {
    background: #EF4444 !important;
    animation: pulse-badge 1.5s infinite;
  }

  .btn-top-refresh {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    color: #334155;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.15s ease;
  }
  .btn-top-refresh:hover {
    background: #E2E8F0;
    color: #0F172A;
  }
  .btn-top-refresh.is-refreshing .refresh-icon {
    animation: spin 0.8s linear infinite;
  }
  .btn-top-refresh.has-update {
    background: #D97706 !important;
    color: #FFFFFF !important;
    border-color: #B45309 !important;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  /* Hero Header */
  .fm-hero {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 2.2rem 1rem 1.8rem;
    text-align: center;
  }

  .fm-hero__inner {
    max-width: 820px;
    margin: 0 auto;
  }

  .fm-badge-row {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.85rem;
  }

  .fm-badge {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
  }

  .fm-badge--green {
    background: #E8F5E9;
    color: #008234;
    border: 1px solid #A5D6A7;
  }

  .fm-badge--blue {
    background: #E1F5FE;
    color: #0077C8;
    border: 1px solid #81D4FA;
  }

  .fm-badge--gold {
    background: #FFF8E1;
    color: #B78103;
    border: 1px solid #FFE082;
  }

  .fm-hero__title {
    font-size: clamp(1.4rem, 4vw, 2.2rem);
    font-weight: 900;
    line-height: 1.25;
    letter-spacing: -0.02em;
    color: #0F172A;
    margin: 0.2rem 0 0.8rem;
  }

  .fm-title-gradient {
    background: linear-gradient(135deg, #008234 0%, #0077C8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .fm-hero__desc {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #475569;
    margin: 0;
  }

  /* SECTION 1: Recommended Hot Routes Section */
  .hot-routes-section {
    padding: 2rem 0;
    background: linear-gradient(180deg, #F1F5F9 0%, #F8FAFC 100%);
    border-bottom: 2px solid #E2E8F0;
  }

  .hot-routes-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  .hot-routes-header {
    margin-bottom: 1.5rem;
  }

  .hot-routes-title-box {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 0.4rem;
  }

  .hot-routes-kicker {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #FEE2E2;
    color: #DC2626;
    border: 1px solid #FECACA;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
  }

  .hot-routes-title {
    font-size: 1.45rem;
    font-weight: 900;
    color: #0F172A;
    margin: 0;
  }

  .hot-routes-subdesc {
    font-size: 0.88rem;
    color: #475569;
    margin: 0;
    line-height: 1.55;
  }

  .hot-routes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1.25rem;
  }

  .hot-route-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }

  .hot-route-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    border-color: #94A3B8;
  }

  .hot-route-top {
    margin-bottom: 0.85rem;
  }

  .hot-route-badge-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.45rem;
  }

  .hot-route-tag {
    font-size: 0.72rem;
    font-weight: 800;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    letter-spacing: 0.02em;
  }

  .hot-route-rank {
    font-size: 0.72rem;
    font-weight: 800;
    color: #64748B;
    background: #F1F5F9;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
  }

  .hot-route-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 0.2rem;
  }

  .hot-route-subtitle {
    font-size: 0.82rem;
    color: #64748B;
    margin: 0;
  }

  .hot-route-stats {
    display: flex;
    align-items: center;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 0.6rem 0.75rem;
    margin-bottom: 0.85rem;
  }

  .stat-col {
    flex: 1;
    text-align: center;
    display: flex;
    flex-direction: column;
  }

  .stat-val {
    font-size: 1.15rem;
    font-weight: 900;
    color: #0F172A;
    line-height: 1.2;
  }

  .stat-val--green {
    color: #008234;
  }

  .stat-lbl {
    font-size: 0.68rem;
    color: #64748B;
    font-weight: 600;
    margin-top: 0.1rem;
  }

  .stat-sep {
    width: 1px;
    height: 24px;
    background: #E2E8F0;
  }

  .hot-route-desc {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.45;
    margin: 0 0 0.85rem;
  }

  .hot-route-samples {
    margin-bottom: 1rem;
    font-size: 0.75rem;
  }

  .samples-title {
    color: #64748B;
    font-weight: 700;
    margin-bottom: 0.35rem;
    display: block;
  }

  .samples-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    align-items: center;
  }

  .sample-pill {
    background: #E8F5E9;
    color: #008234;
    border: 1px solid #C8E6C9;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    font-weight: 600;
  }

  .sample-more {
    color: #94A3B8;
    font-style: italic;
    font-size: 0.72rem;
  }

  .hot-route-actions {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0.5rem;
    margin-top: auto;
  }

  .btn-copy-hot-route {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    background: #008234;
    color: #FFFFFF;
    border: none;
    padding: 0.65rem 0.85rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-copy-hot-route:hover {
    background: #006829;
    box-shadow: 0 2px 8px rgba(0, 130, 52, 0.3);
  }

  .btn-hot-geosim {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    background: #E1F5FE;
    color: #0284C7;
    border: 1px solid #BAE6FD;
    padding: 0.65rem 0.85rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s ease;
  }

  .btn-hot-geosim:hover {
    background: #BAE6FD;
    color: #0369A1;
  }

  /* SECTION 2: Directory Section */
  .fm-main {
    padding: 2rem 0;
  }

  .directory-section-header {
    margin-bottom: 1.25rem;
  }

  .directory-title-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
  }

  .directory-badge {
    background: #E0E7FF;
    color: #4338CA;
    font-size: 0.72rem;
    font-weight: 800;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
  }

  .directory-title {
    font-size: 1.45rem;
    font-weight: 900;
    color: #0F172A;
    margin: 0;
  }

  .directory-desc {
    font-size: 0.88rem;
    color: #475569;
    margin: 0;
  }

  /* Controls Card */
  .fm-controls-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    margin-bottom: 2rem;
  }

  .fm-search-row {
    margin-bottom: 1rem;
  }

  .fm-search-wrap {
    position: relative;
    width: 100%;
  }

  .fm-search-icon {
    position: absolute;
    left: 0.85rem;
    top: 50%;
    transform: translateY(-50%);
    color: #94A3B8;
    pointer-events: none;
  }

  .fm-search-input {
    width: 100%;
    box-sizing: border-box;
    padding: 0.75rem 2.5rem 0.75rem 2.6rem;
    font-size: 0.95rem;
    color: #0F172A;
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    outline: none;
    transition: all 0.15s ease;
  }

  .fm-search-input:focus {
    background: #FFFFFF;
    border-color: #008234;
    box-shadow: 0 0 0 3px rgba(0, 130, 52, 0.15);
  }

  .fm-clear-btn {
    position: absolute;
    right: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #94A3B8;
    cursor: pointer;
    padding: 0.25rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .fm-clear-btn:hover {
    color: #475569;
  }

  /* District Pills (Tier 1) */
  .tier-district-bar {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    overflow-x: auto;
    overscroll-behavior-x: contain !important;
    padding-bottom: 0.65rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid #F1F5F9;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
  }

  .district-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 0.85rem;
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    color: #475569;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.15s ease;
  }

  .district-pill:hover {
    background: #E2E8F0;
    color: #0F172A;
  }

  .district-pill.active {
    background: #008234;
    border-color: #008234;
    color: #FFFFFF;
    box-shadow: 0 2px 6px rgba(0, 130, 52, 0.25);
  }

  .pill-count {
    font-size: 0.72rem;
    background: rgba(0, 0, 0, 0.08);
    padding: 0.1rem 0.4rem;
    border-radius: 999px;
  }

  .district-pill.active .pill-count {
    background: rgba(255, 255, 255, 0.25);
    color: #FFFFFF;
  }

  /* Status Pills (Tier 2) */
  .tier-status-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    overflow-x: auto;
    overscroll-behavior-x: contain !important;
    padding-bottom: 0.65rem;
    margin-bottom: 1rem;
    scrollbar-width: thin;
    -webkit-overflow-scrolling: touch;
  }

  .status-pill {
    padding: 0.35rem 0.85rem;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    color: #64748B;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
    transition: all 0.15s ease;
  }

  .status-pill:hover {
    background: #F8FAFC;
    border-color: #94A3B8;
  }

  .status-pill.active {
    background: #0077C8;
    border-color: #0077C8;
    color: #FFFFFF;
    box-shadow: 0 2px 6px rgba(0, 119, 200, 0.25);
  }

  /* Tools Bar */
  .fm-tools-bar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.65rem;
    padding-top: 0.5rem;
  }

  .fm-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 1rem;
    font-size: 0.85rem;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
    border: none;
  }

  .fm-btn--primary {
    background: #008234;
    color: #FFFFFF;
  }
  .fm-btn--primary:hover {
    background: #006829;
    box-shadow: 0 2px 8px rgba(0, 130, 52, 0.3);
  }

  .fm-btn--outline {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    color: #334155;
  }
  .fm-btn--outline:hover {
    background: #F1F5F9;
    border-color: #94A3B8;
  }

  .fm-btn--ghost {
    background: transparent;
    color: #64748B;
  }
  .fm-btn--ghost:hover {
    background: #F1F5F9;
    color: #0F172A;
  }

  /* District Section */
  .district-section {
    margin-bottom: 2.5rem;
  }

  .district-section__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #E2E8F0;
  }

  .district-title-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .district-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0;
  }

  .district-count-tag {
    font-size: 0.75rem;
    font-weight: 700;
    background: #E8F5E9;
    color: #008234;
    border: 1px solid #A5D6A7;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
  }

  .btn-copy-district-route {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    color: #008234;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.35rem 0.7rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .btn-copy-district-route:hover {
    background: #E8F5E9;
    border-color: #008234;
  }

  /* Store Grid */
  .store-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1rem;
  }

  @media (max-width: 640px) {
    .store-grid {
      grid-template-columns: 1fr;
    }
    .hot-routes-grid {
      grid-template-columns: 1fr;
    }
  }

  /* Store Card */
  .store-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  }

  .store-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    border-color: #94A3B8;
  }

  .store-card__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
  }

  .store-name-box {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .store-name {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0;
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

  /* Checkbox Toggle */
  .check-toggle {
    display: inline-flex;
    align-items: center;
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
  }

  .check-toggle__input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }

  .check-toggle__label {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.55rem;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748B;
    transition: all 0.15s ease;
  }

  .check-box-icon {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    border: 1.5px solid #94A3B8;
    background: #FFFFFF;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
  }

  .check-svg {
    display: none;
    stroke: #FFFFFF;
  }

  .check-toggle__input:checked + .check-toggle__label {
    background: #E8F5E9;
    border-color: #81C784;
    color: #008234;
  }

  .check-toggle__input:checked + .check-toggle__label .check-box-icon {
    background: #008234;
    border-color: #008234;
  }

  .check-toggle__input:checked + .check-toggle__label .check-svg {
    display: block;
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
    padding: 0.3rem 0.5rem;
    border-radius: 6px;
    border: 1px solid #E2E8F0;
  }

  .coord-tag {
    font-weight: 800;
    color: #64748B;
    font-size: 0.7rem;
  }

  .coord-val {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    color: #334155;
    font-weight: 600;
    flex: 1;
  }

  .btn-copy-single {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    color: #475569;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.12s ease;
  }

  .btn-copy-single:hover {
    background: #F1F5F9;
    color: #0F172A;
  }

  /* Card Actions */
  .card-actions {
    display: grid;
    grid-template-columns: 1fr 1fr auto;
    gap: 0.4rem;
    margin-top: auto;
  }

  .btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    padding: 0.5rem 0.6rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s ease;
    border: 1px solid transparent;
    white-space: nowrap;
  }

  .btn-pikmin {
    background: #E8F5E9;
    color: #008234;
    border-color: #C8E6C9;
  }
  .btn-pikmin:hover {
    background: #C8E6C9;
  }

  .btn-geosim {
    background: #E1F5FE;
    color: #0284C7;
    border-color: #BAE6FD;
  }
  .btn-geosim:hover {
    background: #BAE6FD;
  }

  .btn-gmap {
    background: #F1F5F9;
    color: #475569;
    border-color: #E2E8F0;
    padding: 0.5rem 0.65rem;
  }
  .btn-gmap:hover {
    background: #E2E8F0;
    color: #0F172A;
  }

  /* No Results Box */
  .no-results-box {
    text-align: center;
    padding: 3rem 1rem;
    background: #FFFFFF;
    border-radius: 12px;
    border: 1px dashed #CBD5E1;
    margin-top: 1.5rem;
  }
  .no-results-icon {
    margin-bottom: 0.75rem;
  }
  .no-results-box h3 {
    margin: 0 0 0.5rem;
    font-size: 1.15rem;
    color: #0F172A;
  }
  .no-results-box p {
    color: #64748B;
    font-size: 0.9rem;
    margin: 0 0 1.25rem;
  }

  /* Toast */
  .copy-toast {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    background: rgba(15, 23, 42, 0.94);
    color: #FFFFFF;
    padding: 0.75rem 1.4rem;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    opacity: 0;
    pointer-events: none;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    white-space: nowrap;
    backdrop-filter: blur(8px);
  }

  .copy-toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
</style>
"""

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Generated {target_path} successfully!")

if __name__ == '__main__':
    generate_page(is_staging=True)
    generate_page(is_staging=False)
