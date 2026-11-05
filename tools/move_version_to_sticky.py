def move_to_sticky():
    path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove from Hero
    hero_banner = """        <!-- Version & Cache Reset Banner with Auto-Detection -->
        <div class="coco-version-card" id="coco-version-card" data-batch-id="13" data-store-count={stores.length}>
          <div class="coco-version-info">
            <span class="version-dot" id="version-dot" aria-hidden="true"></span>
            <div class="version-text-group">
              <span class="version-badge" id="version-badge">已同步最新</span>
              <span class="version-title" id="version-title">資料庫版本：11/05 17:25 · 全台 {stores.length} 店完整校對</span>
            </div>
          </div>
          <button id="btn-force-refresh" class="btn-force-refresh" type="button" title="清除本機快取並載入最新門市點位">
            <svg class="refresh-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span class="refresh-label">若點位未更新請點此強制重整</span>
          </button>
        </div>
"""
    if hero_banner in content:
        content = content.replace(hero_banner, "", 1)
        print("Removed banner from Hero.")
    else:
        # Check CRLF
        hero_banner_crlf = hero_banner.replace('\n', '\r\n')
        if hero_banner_crlf in content:
            content = content.replace(hero_banner_crlf, "", 1)
            print("Removed CRLF banner from Hero.")
        else:
            print("Warning: hero_banner not matched directly, inspecting...")

    # 2. Insert into Sticky Controls Section
    sticky_anchor = '<section class="coco-controls-section">\n      <div class="container">'
    sticky_anchor_crlf = '<section class="coco-controls-section">\r\n      <div class="container">'

    sticky_bar_html = """
        <!-- Sticky Top Version & Force Refresh Strip -->
        <div class="sticky-version-bar" id="coco-version-card" data-batch-id="13" data-store-count={stores.length}>
          <div class="sticky-version-left">
            <span class="version-dot" id="version-dot" aria-hidden="true"></span>
            <span class="version-tag" id="version-badge">最新版</span>
            <span class="version-info-text" id="version-title">點位資料庫：11/05 17:25 · 全台 <strong>{stores.length}</strong> 店已校對</span>
          </div>
          <button id="btn-force-refresh" class="btn-sticky-refresh" type="button" title="清除快取載入最新門市點位">
            <svg class="refresh-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <polyline points="23 4 23 10 17 10"></polyline>
              <polyline points="1 20 1 14 7 14"></polyline>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
            </svg>
            <span class="refresh-label">點此強制重整</span>
          </button>
        </div>"""

    if sticky_anchor in content:
        content = content.replace(sticky_anchor, sticky_anchor + sticky_bar_html, 1)
        print("Inserted sticky_bar_html into sticky controls.")
    elif sticky_anchor_crlf in content:
        content = content.replace(sticky_anchor_crlf, sticky_anchor_crlf + sticky_bar_html.replace('\n', '\r\n'), 1)
        print("Inserted sticky_bar_html (CRLF) into sticky controls.")
    else:
        print("Error: Could not find sticky_anchor!")
        return

    # 3. Update CSS
    css_anchor = '/* Clean Compact Hero */'
    new_css = """  /* Sticky Top Version & Refresh Strip */
  .sticky-version-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.35rem 0.75rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    font-size: 0.82rem;
    transition: all 0.2s ease;
  }

  :global(html[data-theme="vibrant"]) .sticky-version-bar {
    background: #FFFFFF;
    border-color: #E2E8F0;
  }

  .sticky-version-left {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    flex-wrap: wrap;
    color: #475569;
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
    font-weight: 700;
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    border: 1px solid #A7F3D0;
    flex-shrink: 0;
  }

  .version-info-text {
    font-weight: 500;
    line-height: 1.3;
  }

  .version-info-text strong {
    color: #E4571D;
    font-weight: 800;
  }

  .btn-sticky-refresh {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    color: #334155;
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.25rem 0.55rem;
    border-radius: 6px;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.15s ease;
  }

  .btn-sticky-refresh:hover {
    background: #EDE9FE;
    border-color: #C4B5FD;
    color: #6D28D9;
  }

  .btn-sticky-refresh.is-refreshing {
    opacity: 0.7;
    pointer-events: none;
  }

  .btn-sticky-refresh.is-refreshing .refresh-icon {
    animation: spin-refresh 0.8s linear infinite;
  }

  /* When remote version is newer than cached HTML */
  .sticky-version-bar.has-update {
    background: #FFFBEB !important;
    border-color: #FCD34D !important;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2) !important;
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

  .btn-sticky-refresh.has-update {
    background: linear-gradient(135deg, #E4571D 0%, #D97706 100%) !important;
    border-color: #D97706 !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 6px rgba(228, 87, 29, 0.4) !important;
    animation: btn-attention 1.6s infinite !important;
  }

  @keyframes spin-refresh {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @keyframes dot-pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.75; }
  }

  @keyframes btn-attention {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
  }

"""
    if css_anchor in content:
        content = content.replace(css_anchor, new_css + css_anchor, 1)
        print("Added new CSS.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done moving version bar to sticky section!")

if __name__ == '__main__':
    move_to_sticky()
