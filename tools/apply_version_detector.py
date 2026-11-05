def apply_detector():
    path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML
    old_html = """        <!-- Version & Cache Reset Banner -->
        <div class="coco-version-card">
          <div class="coco-version-info">
            <span class="version-dot" aria-hidden="true"></span>
            <div class="version-text-group">
              <span class="version-badge">已同步最新</span>
              <span class="version-title">資料庫版本：11/05 17:25 · 全台 {stores.length} 店完整校對</span>
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
        </div>"""

    new_html = """        <!-- Version & Cache Reset Banner with Auto-Detection -->
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
        </div>"""

    if old_html in content:
        content = content.replace(old_html, new_html, 1)
        print("Updated HTML with IDs and data attributes.")
    else:
        print("Could not find old_html in staging.astro!")
        return

    # 2. Update CSS
    css_anchor = '.coco-version-card {'
    extra_css = """  /* When remote version is newer than cached HTML */
  .coco-version-card.has-update {
    background: #FFFBEB !important;
    border-color: #FCD34D !important;
    box-shadow: 0 3px 10px rgba(245, 158, 11, 0.2) !important;
  }

  .version-dot.has-update {
    background: #F59E0B !important;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.35) !important;
    animation: dot-pulse 1.2s infinite !important;
  }

  .version-badge.has-update {
    background: #FEF3C7 !important;
    color: #B45309 !important;
    border: 1px solid #FDE68A !important;
    font-weight: 800 !important;
  }

  .btn-force-refresh.has-update {
    background: linear-gradient(135deg, #E4571D 0%, #D97706 100%) !important;
    border-color: #D97706 !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(228, 87, 29, 0.4) !important;
    animation: btn-attention 1.6s infinite !important;
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
        content = content.replace(css_anchor, extra_css + css_anchor, 1)
        print("Updated CSS with has-update styles.")

    # 3. Update JS
    js_old = """    // Force refresh button logic
    const btnForceRefresh = document.getElementById('btn-force-refresh');
    if (btnForceRefresh) {
      btnForceRefresh.addEventListener('click', function () {
        btnForceRefresh.classList.add('is-refreshing');
        const label = btnForceRefresh.querySelector('.refresh-label');
        if (label) label.textContent = '正在重新載入最新資料...';
        const u = new URL(window.location.href);
        u.searchParams.set('v', '13');
        u.searchParams.set('t', Date.now().toString());
        window.location.href = u.toString();
      });
    }"""

    js_new = """    // Force refresh button logic & Remote Version Auto-Check
    const btnForceRefresh = document.getElementById('btn-force-refresh');
    if (btnForceRefresh) {
      btnForceRefresh.addEventListener('click', function () {
        btnForceRefresh.classList.add('is-refreshing');
        const label = btnForceRefresh.querySelector('.refresh-label');
        if (label) label.textContent = '正在重新載入最新資料...';
        const u = new URL(window.location.href);
        u.searchParams.set('v', '13');
        u.searchParams.set('t', Date.now().toString());
        window.location.href = u.toString();
      });
    }

    // Auto-detect if user's local cache has older data than Cloudflare server
    (function checkRemoteVersion() {
      const card = document.getElementById('coco-version-card');
      if (!card) return;
      const localBatch = parseInt(card.getAttribute('data-batch-id') || '0', 10);
      const localCount = parseInt(card.getAttribute('data-store-count') || '0', 10);

      fetch('/events/coco-version.json?_t=' + Date.now(), { cache: 'no-store' })
        .then(function (res) { return res.json(); })
        .then(function (remote) {
          if (!remote || !remote.batch_id) return;
          if (remote.batch_id > localBatch || remote.store_count > localCount) {
            card.classList.add('has-update');
            const dot = document.getElementById('version-dot');
            const badge = document.getElementById('version-badge');
            const title = document.getElementById('version-title');
            const btn = document.getElementById('btn-force-refresh');

            if (dot) dot.classList.add('has-update');
            if (badge) {
              badge.textContent = '發現新點位！';
              badge.classList.add('has-update');
            }
            if (title) {
              title.innerHTML = '<strong>已釋出最新點位（最新 ' + remote.store_count + ' 店，目前快取為 ' + localCount + ' 店）</strong>';
            }
            if (btn) {
              btn.classList.add('has-update');
              const label = btn.querySelector('.refresh-label');
              if (label) label.textContent = '點我立即更新至最新 ' + remote.store_count + ' 店';
            }
          }
        })
        .catch(function () {});
    })();"""

    if js_old in content:
        content = content.replace(js_old, js_new, 1)
        print("Updated JS with auto-check.")
    else:
        print("Could not find js_old in staging.astro!")
        return

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated staging.astro with detector!")

if __name__ == '__main__':
    apply_detector()
