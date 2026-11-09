import os

def update_fm_generator():
    path = 'tools/generate_fm_page.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML generation: Add Staging notice and top Sticky Version Banner right after <div class="fm-page">
    old_target = '<div class="fm-page">\n    <!-- Top Fixed Hero Header -->'
    
    new_html = """<div class="fm-page">
    {is_staging_banner}
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

    <!-- Top Fixed Hero Header -->"""

    # In generate_fm_page.py, replace the header
    if old_target in content:
        content = content.replace(old_target, new_html)
        print("Replaced HTML top section")
    else:
        print("WARNING: old_target not found!")

    # In generate_page() function, ensure is_staging_banner is formatted
    func_target = 'def generate_page(is_staging=False):'
    func_replacement = """def generate_page(is_staging=False):
    target_path = 'app/src/pages/events/familymart-pikmin/staging.astro' if is_staging else 'app/src/pages/events/familymart-pikmin/index.astro'
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    staging_banner = '''<!-- Staging Environment Indicator Banner -->
    <div style="background: #FEF3C7; border-bottom: 2px solid #F59E0B; padding: 0.5rem 1rem; text-align: center; font-size: 0.875rem; font-weight: 700; color: #92400E; z-index: 50; position: relative;">
      [測試預覽環境 Staging] 此頁面用於驗證新功能，測試完畢確認無誤後將同步發布至正式版。
    </div>''' if is_staging else ''"""

    if func_target in content:
        # replace the beginning of generate_page
        old_head = """def generate_page(is_staging=False):
    target_path = 'app/src/pages/events/familymart-pikmin/staging.astro' if is_staging else 'app/src/pages/events/familymart-pikmin/index.astro'
    os.makedirs(os.path.dirname(target_path), exist_ok=True)"""
        content = content.replace(old_head, func_replacement)
        print("Replaced generate_page header")

    # Replace {is_staging_banner} format in code
    content = content.replace('{is_staging_banner}', '""" + staging_banner + """')

    # 2. Add CSS for version banner
    version_css = """
  /* Top Sticky Version & Live Update Notification Banner */
  .top-sticky-version-wrapper {
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 800;
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    transition: all 0.25s ease;
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
"""

    css_target = '</style>'
    content = content.replace(css_target, version_css + '\n' + css_target)
    print("Added CSS for version banner")

    # 3. Add JavaScript for version polling and force refresh
    js_version_code = """
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
"""

    js_target = 'const toast = document.getElementById(\'copy-toast\');'
    if js_target in content:
        content = content.replace(js_target, js_version_code + '\n    ' + js_target)
        print("Added JavaScript for version polling and force refresh")
    else:
        print("WARNING: js_target not found!")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated tools/generate_fm_page.py successfully!")

if __name__ == '__main__':
    update_fm_generator()
