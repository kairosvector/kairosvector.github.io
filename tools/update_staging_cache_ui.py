import os

def update_staging():
    path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert HTML
    target_html = '<span class="text-gradient">全台 {stores.length} 店 GPS 座標與 7 天打卡清單</span>\n        </h1>'
    if target_html not in content:
        target_html = '<span class="text-gradient">全台 {stores.length} 店 GPS 座標與 7 天打卡清單</span>\r\n        </h1>'
    
    html_to_add = """

        <!-- Version & Cache Reset Banner -->
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

    if target_html in content:
        content = content.replace(target_html, target_html + html_to_add, 1)
        print("HTML inserted successfully.")
    else:
        print("Failed to find target_html!")
        return

    # 2. Insert CSS
    css_target = '/* Clean Compact Hero */'
    css_to_add = """  /* Version & Force Refresh Banner */
  .coco-version-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    flex-wrap: wrap;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 0.5rem 0.85rem;
    margin: 0.75rem 0 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  }

  .coco-version-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .version-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    display: inline-block;
    flex-shrink: 0;
  }

  .version-text-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    font-size: 0.8rem;
  }

  .version-badge {
    background: #ECFDF5;
    color: #065F46;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: 6px;
    font-size: 0.75rem;
  }

  .version-title {
    color: #4B5563;
    font-weight: 500;
  }

  .btn-force-refresh {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #F3F4F6;
    border: 1px solid #D1D5DB;
    color: #374151;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.35rem 0.65rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-force-refresh:hover {
    background: #EDE9FE;
    border-color: #C4B5FD;
    color: #6D28D9;
  }

  .btn-force-refresh.is-refreshing {
    opacity: 0.7;
    pointer-events: none;
  }

  .btn-force-refresh.is-refreshing .refresh-icon {
    animation: spin-refresh 0.8s linear infinite;
  }

  @keyframes spin-refresh {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  """
    if css_target in content:
        content = content.replace(css_target, css_to_add + css_target, 1)
        print("CSS inserted successfully.")
    else:
        print("Failed to find css_target!")
        return

    # 3. Insert JS
    js_target = 'const PLAY_STORE_URL ='
    js_to_add = """// Force refresh button logic
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

    """
    if js_target in content:
        content = content.replace(js_target, js_to_add + js_target, 1)
        print("JS inserted successfully.")
    else:
        print("Failed to find js_target!")
        return

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("staging.astro successfully updated!")

if __name__ == '__main__':
    update_staging()
