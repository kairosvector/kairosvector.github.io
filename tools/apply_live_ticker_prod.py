import re

prod_file = "app/src/pages/events/coco-pikmin.astro"

with open(prod_file, "r", encoding="utf-8") as f:
    content = f.read()

new_left_html = '''        <div class="top-sticky-version-left">
          <span class="version-dot" id="version-dot" aria-hidden="true"></span>
          <span class="version-tag" id="version-badge">{stores.length} 店最新</span>
          <div class="version-marquee-box" id="version-marquee-box">
            <span class="version-ticker-text" id="version-ticker">
              <span class="ticker-badge">最新</span>基隆海豐、三重自強、高雄萬家福 已校準！
            </span>
          </div>
        </div>'''

content = re.sub(
    r'<div class="top-sticky-version-left">.*?</div>\s*<button id="btn-force-refresh"',
    new_left_html + '\n        <button id="btn-force-refresh"',
    content,
    flags=re.DOTALL
)

new_js_block = '''    // Force refresh button logic & Real-time Live Remote Version Polling
    let latestRemoteVersion = null;
    const btnForceRefresh = document.getElementById('btn-force-refresh');
    if (btnForceRefresh) {
      btnForceRefresh.addEventListener('click', function () {
        btnForceRefresh.classList.add('is-refreshing');
        const label = btnForceRefresh.querySelector('.refresh-label');
        if (label) label.textContent = '載入最新中...';
        const u = new URL(window.location.href);
        const targetVer = latestRemoteVersion || '29';
        u.searchParams.set('v', targetVer);
        u.searchParams.set('t', Date.now().toString());
        window.location.href = u.toString();
      });
    }

    function applyRemoteUpdateNotice(remote) {
      latestRemoteVersion = remote.version || remote.batch_id;
      const card = document.getElementById('coco-version-card');
      const dot = document.getElementById('version-dot');
      const badge = document.getElementById('version-badge');
      const ticker = document.getElementById('version-ticker');
      const btn = document.getElementById('btn-force-refresh');

      if (card) card.classList.add('has-update');
      if (dot) dot.classList.add('has-update');
      if (badge) {
        badge.textContent = '🔥 發現新點位！';
        badge.classList.add('has-update');
      }
      if (ticker) {
        ticker.innerHTML = '<span class="ticker-badge has-update">新發布</span><strong>' + (remote.description || '最新門市資料已更新') + '</strong> ➔ <span class="ticker-click-hint">請按強制重整更新</span>';
        ticker.classList.add('has-update');
      }
      if (btn) {
        btn.classList.add('has-update');
        const label = btn.querySelector('.refresh-label');
        if (label) label.textContent = '點我強制重整 ↻';
        btn.setAttribute('title', '已有新更新發布，請點此強制重整載入最新點位！');
      }

      // Show floating notification prompt instructing player to click force refresh
      showLiveUpdateFloatingPrompt(remote);
    }

    function showLiveUpdateFloatingPrompt(remote) {
      let prompt = document.getElementById('live-update-float-toast');
      if (!prompt) {
        prompt = document.createElement('div');
        prompt.id = 'live-update-float-toast';
        prompt.className = 'live-update-float-toast';
        document.body.appendChild(prompt);
      }
      prompt.innerHTML = `
        <div class="live-update-float-inner">
          <div class="live-update-icon">🔔</div>
          <div class="live-update-msg">
            <div class="live-update-heading"><strong>已發布新版點位（${remote.description || ('第 ' + remote.version + ' 波')}）</strong></div>
            <div class="live-update-sub">⚠️ 畫面尚未同步，請<strong>點擊右方按鈕</strong>強制重整以取得最新地標！</div>
          </div>
          <button type="button" class="btn-float-reload" id="btn-float-reload">立即強制重整 ↻</button>
        </div>
      `;
      prompt.classList.add('is-visible');
      const floatBtn = document.getElementById('btn-float-reload');
      if (floatBtn && btnForceRefresh) {
        floatBtn.addEventListener('click', function() {
          btnForceRefresh.click();
        });
      }
    }

    function checkRemoteVersion() {
      const card = document.getElementById('coco-version-card');
      if (!card) return;
      const localBatch = parseInt(card.getAttribute('data-batch-id') || '0', 10);
      const localCount = parseInt(card.getAttribute('data-store-count') || '0', 10);

      fetch('/events/coco-version.json?_t=' + Date.now(), { cache: 'no-store' })
        .then(function (res) { return res.json(); })
        .then(function (remote) {
          if (!remote || !remote.batch_id) return;
          if (remote.batch_id > localBatch || remote.store_count > localCount) {
            applyRemoteUpdateNotice(remote);
          }
        })
        .catch(function () {});
    }

    // Run check on load, AND poll every 10 seconds for real-time live detection!
    checkRemoteVersion();
    setInterval(checkRemoteVersion, 10000);
    document.addEventListener('visibilitychange', function() {
      if (!document.hidden) checkRemoteVersion();
    });'''

content = re.sub(
    r'// Force refresh button logic & Remote Version Auto-Check.*?\}\)\(\);',
    new_js_block,
    content,
    flags=re.DOTALL
)

custom_css = '''
  /* Real-time Ticker in Sticky Header */
  .version-marquee-box {
    display: flex;
    align-items: center;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    min-width: 0;
    max-width: 580px;
  }

  .version-ticker-text {
    font-size: 0.78rem;
    color: #475569;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .ticker-badge {
    display: inline-block;
    background: #EFF6FF;
    color: #2563EB;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.05rem 0.35rem;
    border-radius: 4px;
    border: 1px solid #BFDBFE;
    margin-right: 0.35rem;
    vertical-align: middle;
  }

  .ticker-badge.has-update {
    background: #FEF3C7;
    color: #D97706;
    border-color: #FDE68A;
    animation: dot-pulse 1.2s infinite;
  }

  .ticker-click-hint {
    color: #EA580C;
    font-weight: 700;
  }

  /* Live Update Floating Prompt (Popup when background polling detects new batch) */
  .live-update-float-toast {
    position: fixed;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%) translateY(120%);
    z-index: 9999;
    width: calc(100% - 2rem);
    max-width: 600px;
    background: #FFFBEB;
    border: 2px solid #F59E0B;
    border-radius: 14px;
    box-shadow: 0 10px 25px -5px rgba(217, 119, 6, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    padding: 0.85rem 1.15rem;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
    opacity: 0;
    pointer-events: none;
  }

  .live-update-float-toast.is-visible {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
    pointer-events: auto;
  }

  .live-update-float-inner {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    justify-content: space-between;
  }

  .live-update-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
    animation: icon-bounce 1s infinite alternate;
  }

  .live-update-msg {
    flex: 1;
    min-width: 0;
    color: #78350F;
  }

  .live-update-heading {
    font-size: 0.88rem;
    color: #92400E;
    line-height: 1.3;
  }

  .live-update-sub {
    font-size: 0.75rem;
    color: #B45309;
    margin-top: 0.15rem;
  }

  .btn-float-reload {
    flex-shrink: 0;
    background: linear-gradient(135deg, #EA580C 0%, #D97706 100%);
    color: #FFFFFF;
    font-size: 0.82rem;
    font-weight: 800;
    padding: 0.5rem 0.95rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    box-shadow: 0 3px 8px rgba(234, 88, 12, 0.35);
    white-space: nowrap;
    animation: btn-attention 1.6s infinite;
  }

  .btn-float-reload:hover {
    background: linear-gradient(135deg, #C2410C 0%, #B45309 100%);
  }

  @keyframes icon-bounce {
    from { transform: translateY(0); }
    to { transform: translateY(-4px); }
  }

  @media (max-width: 640px) {
    .version-marquee-box {
      max-width: 170px;
    }
    .live-update-float-inner {
      flex-direction: column;
      align-items: stretch;
      gap: 0.6rem;
      text-align: left;
    }
    .btn-float-reload {
      width: 100%;
      text-align: center;
    }
  }
'''

content = content.replace('</style>', custom_css + '\n</style>')

with open(prod_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated coco-pikmin.astro successfully.")
