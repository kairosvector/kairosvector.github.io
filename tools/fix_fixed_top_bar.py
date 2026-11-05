def fix_top_bar():
    path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML
    old_html = """<!-- Top Sticky Version & Force Refresh Banner (Pinned at absolute top) -->
    <div class="top-sticky-version-wrapper" id="coco-version-card" data-batch-id="13" data-store-count={stores.length}>
      <div class="container top-sticky-version-inner">
        <div class="top-sticky-version-left">
          <span class="version-dot" id="version-dot" aria-hidden="true"></span>
          <span class="version-tag" id="version-badge">最新版</span>
          <span class="version-info-text" id="version-title">點位資料庫：11/05 17:25 · 全台 <strong>{stores.length}</strong> 店已校對</span>
        </div>
        <button id="btn-force-refresh" class="btn-top-refresh" type="button" title="清除快取載入最新門市點位">
          <svg class="refresh-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="23 4 23 10 17 10"></polyline>
            <polyline points="1 20 1 14 7 14"></polyline>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
          </svg>
          <span class="refresh-label">點此強制重整</span>
        </button>
      </div>
    </div>"""

    new_html = """<!-- Top Fixed Version & Force Refresh Banner (Fixed right below Title Bar) -->
    <div class="top-sticky-version-wrapper" id="coco-version-card" data-batch-id="13" data-store-count={stores.length}>
      <div class="container top-sticky-version-inner">
        <div class="top-sticky-version-left">
          <span class="version-dot" id="version-dot" aria-hidden="true"></span>
          <span class="version-tag" id="version-badge">{stores.length} 店最新</span>
          <span class="version-info-text" id="version-title">
            <span class="version-desktop-text">點位已校正 · 11/05 17:25</span>
            <span class="version-mobile-text">11/05 17:25</span>
          </span>
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
    <div class="top-sticky-spacer" aria-hidden="true"></div>"""

    if old_html in content:
        content = content.replace(old_html, new_html, 1)
        print("Updated HTML.")
    elif old_html.replace('\n', '\r\n') in content:
        content = content.replace(old_html.replace('\n', '\r\n'), new_html.replace('\n', '\r\n'), 1)
        print("Updated HTML (CRLF).")
    else:
        print("Failed to match old_html in content!")
        return

    # 2. Update CSS: Replace previous .top-sticky-version-wrapper block
    css_start = '/* Top Sticky Version Banner (Absolute Top under Navbar) */'
    css_end = '/* Clean Compact Hero */'
    
    idx_start = content.find(css_start)
    idx_end = content.find(css_end)

    if idx_start != -1 and idx_end != -1:
        new_css_block = """/* Top Fixed Version Banner (Fixed right below Title Bar) */
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

  .top-sticky-version-inner {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 0.5rem !important;
    height: 100% !important;
  }

  .top-sticky-version-left {
    display: flex !important;
    align-items: center !important;
    gap: 0.45rem !important;
    font-size: 0.8rem !important;
    color: #475569 !important;
    flex-shrink: 1 !important;
    min-width: 0 !important;
  }

  .version-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 0 2.5px rgba(16, 185, 129, 0.25);
    flex-shrink: 0;
  }

  .version-tag {
    background: #ECFDF5;
    color: #065F46;
    font-size: 0.72rem;
    font-weight: 800;
    padding: 0.1rem 0.45rem;
    border-radius: 4px;
    border: 1px solid #A7F3D0;
    flex-shrink: 0;
    white-space: nowrap;
  }

  .version-info-text {
    font-weight: 500;
    color: #64748B;
    white-space: nowrap;
  }

  .version-mobile-text {
    display: none;
  }

  .btn-top-refresh {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.3rem !important;
    background: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    color: #334155 !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.25rem 0.55rem !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
    transition: all 0.15s ease !important;
  }

  .btn-top-refresh:hover {
    background: #EDE9FE !important;
    border-color: #C4B5FD !important;
    color: #6D28D9 !important;
  }

  .btn-top-refresh.is-refreshing {
    opacity: 0.7;
    pointer-events: none;
  }

  .btn-top-refresh.is-refreshing .refresh-icon {
    animation: spin-refresh 0.8s linear infinite;
  }

  /* When remote version is newer than cached HTML */
  .top-sticky-version-wrapper.has-update {
    background: #FFFBEB !important;
    border-bottom-color: #FCD34D !important;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.25) !important;
  }

  .version-dot.has-update {
    background: #F59E0B !important;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.35) !important;
    animation: dot-pulse 1.2s infinite !important;
  }

  .version-tag.has-update {
    background: #FEF3C7 !important;
    color: #B45309 !important;
    border-color: #FDE68A !important;
  }

  .btn-top-refresh.has-update {
    background: linear-gradient(135deg, #E4571D 0%, #D97706 100%) !important;
    border-color: #D97706 !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 6px rgba(228, 87, 29, 0.4) !important;
    animation: btn-attention 1.6s infinite !important;
  }

  /* Fixed offset for coco-controls-section */
  .coco-controls-section {
    top: calc(var(--nav-height, 64px) + 38px) !important;
  }

  @media (max-width: 640px) {
    .version-desktop-text {
      display: none;
    }
    .version-mobile-text {
      display: inline;
    }
  }

  """
        content = content[:idx_start] + new_css_block + content[idx_end:]
        print("Updated CSS block to position: fixed.")
    else:
        print("Could not find CSS markers!")
        return

    # 3. Also update JS alert text to be concise on mobile
    old_js_alert = "title.innerHTML = '<strong>已釋出最新點位（最新 ' + remote.store_count + ' 店，目前快取為 ' + localCount + ' 店）</strong>';"
    new_js_alert = "title.innerHTML = '<strong>最新 ' + remote.store_count + ' 店已釋出</strong>';"
    if old_js_alert in content:
        content = content.replace(old_js_alert, new_js_alert)
        print("Updated JS alert to concise text.")

    old_btn_alert = "label.textContent = '點我立即更新至最新 ' + remote.store_count + ' 店';"
    new_btn_alert = "label.textContent = '更新至 ' + remote.store_count + ' 店';"
    if old_btn_alert in content:
        content = content.replace(old_btn_alert, new_btn_alert)
        print("Updated btn alert to concise text.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully finished fix_fixed_top_bar!")

if __name__ == '__main__':
    fix_top_bar()
