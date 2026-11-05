def relocate_to_top_sticky():
    path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the sticky bar from inside coco-controls-section
    old_sticky_bar = """        <!-- Sticky Top Version & Force Refresh Strip -->
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

    if old_sticky_bar in content:
        content = content.replace(old_sticky_bar, "", 1)
        print("Removed old sticky bar from coco-controls-section.")
    elif old_sticky_bar.replace('\n', '\r\n') in content:
        content = content.replace(old_sticky_bar.replace('\n', '\r\n'), "", 1)
        print("Removed old sticky bar (CRLF) from coco-controls-section.")
    else:
        print("Warning: old_sticky_bar not found, checking...")

    # 2. Insert at the VERY TOP of <main class="coco-page"> (before Breadcrumb and Hero)
    top_anchor = '<!-- In-App Browser (LINE / FB) Guidance Bar -->'
    new_top_banner = """<!-- Top Sticky Version & Force Refresh Banner (Pinned at absolute top) -->
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
    </div>

    """

    if top_anchor in content:
        content = content.replace(top_anchor, new_top_banner + top_anchor, 1)
        print("Inserted new_top_banner before In-App browser bar / Breadcrumb.")
    else:
        print("Error: Could not find top_anchor!")
        return

    # 3. Add CSS for top-sticky-version-wrapper
    css_anchor = '/* Clean Compact Hero */'
    top_css = """  /* Top Sticky Version Banner (Absolute Top under Navbar) */
  .top-sticky-version-wrapper {
    position: sticky;
    top: var(--nav-height, 64px);
    z-index: 45;
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    padding: 0.35rem 0;
    transition: all 0.2s ease;
  }

  :global(html[data-theme="vibrant"]) .top-sticky-version-wrapper {
    background: #FFFFFF;
    border-bottom-color: #E2E8F0;
  }

  .top-sticky-version-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .top-sticky-version-left {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    color: #475569;
    flex-wrap: nowrap;
    overflow: hidden;
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
    white-space: nowrap;
  }

  .version-info-text strong {
    color: #E4571D;
    font-weight: 800;
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
    padding: 0.25rem 0.55rem;
    border-radius: 6px;
    cursor: pointer;
    flex-shrink: 0;
    white-space: nowrap;
    transition: all 0.15s ease;
  }

  .btn-top-refresh:hover {
    background: #EDE9FE;
    border-color: #C4B5FD;
    color: #6D28D9;
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

  /* Stack sticky controls below the top version bar */
  .coco-controls-section {
    top: calc(var(--nav-height, 64px) + 38px) !important;
  }

  @media (max-width: 640px) {
    .version-info-text {
      font-size: 0.75rem;
    }
  }

"""
    if css_anchor in content:
        content = content.replace(css_anchor, top_css + css_anchor, 1)
        print("Added top_css.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done relocating to top sticky banner!")

if __name__ == '__main__':
    relocate_to_top_sticky()
