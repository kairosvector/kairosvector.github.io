import re

def update_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Place the floating prompt directly in the HTML template right after top-sticky-version-wrapper
    prompt_html = '''    <!-- Live Remote Update Float Toast (In-template for 100% styled popup) -->
    <div id="live-update-float-toast" class="live-update-float-toast" style="display: none;">
      <div class="live-update-float-inner">
        <div class="live-update-icon">🔔</div>
        <div class="live-update-msg">
          <div class="live-update-heading"><strong id="live-float-title">已發布新版點位！</strong></div>
          <div class="live-update-sub" id="live-float-desc">⚠️ 畫面尚未同步，請<strong>點擊右方按鈕</strong>強制重整以取得最新地標！</div>
        </div>
        <button type="button" class="btn-float-reload" id="btn-float-reload">立即強制重整 ↻</button>
      </div>
    </div>'''

    if '<div id="live-update-float-toast"' not in content:
        content = content.replace(
            '<div class="top-sticky-spacer" aria-hidden="true"></div>',
            prompt_html + '\n    <div class="top-sticky-spacer" aria-hidden="true"></div>'
        )

    # 2. Update JS to simply show this pre-existing element and populate text
    old_show_fn = re.search(r'function showLiveUpdateFloatingPrompt.*?\n    \}', content, re.DOTALL)
    new_show_fn = '''function showLiveUpdateFloatingPrompt(remote) {
      const prompt = document.getElementById('live-update-float-toast');
      if (!prompt) return;
      const titleEl = document.getElementById('live-float-title');
      const descEl = document.getElementById('live-float-desc');
      if (titleEl) {
        titleEl.textContent = '已發布第 ' + (remote.version || remote.batch_id) + ' 波新點位！';
      }
      if (descEl) {
        descEl.innerHTML = '⚠️ <strong>' + (remote.description || '最新門市資料已更新') + '</strong><br>請點擊右方「強制重整」以套用最新點位！';
      }
      prompt.style.display = 'block';
      setTimeout(function() {
        prompt.classList.add('is-visible');
      }, 50);

      const floatBtn = document.getElementById('btn-float-reload');
      if (floatBtn && btnForceRefresh) {
        floatBtn.onclick = function() {
          btnForceRefresh.click();
        };
      }
    }'''

    if old_show_fn:
        content = content.replace(old_show_fn.group(0), new_show_fn)

    # 3. Add :global CSS to ensure 100% style matching
    global_css = '''
  /* Global Unscoped Styles for Live Update Floating Toast */
  :global(.live-update-float-toast) {
    position: fixed !important;
    bottom: 2rem !important;
    left: 50% !important;
    transform: translateX(-50%) translateY(150%) !important;
    z-index: 99999 !important;
    width: calc(100% - 2rem) !important;
    max-width: 620px !important;
    background: #FFFBEB !important;
    border: 2.5px solid #F59E0B !important;
    border-radius: 16px !important;
    box-shadow: 0 12px 30px -5px rgba(217, 119, 6, 0.45), 0 8px 12px -6px rgba(0, 0, 0, 0.15) !important;
    padding: 1rem 1.25rem !important;
    transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.45s ease !important;
    opacity: 0 !important;
  }

  :global(.live-update-float-toast.is-visible) {
    transform: translateX(-50%) translateY(0) !important;
    opacity: 1 !important;
  }

  :global(.live-update-float-inner) {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
    justify-content: space-between !important;
  }

  :global(.live-update-icon) {
    font-size: 1.75rem !important;
    flex-shrink: 0 !important;
    animation: icon-bounce 1s infinite alternate !important;
  }

  :global(.live-update-msg) {
    flex: 1 !important;
    min-width: 0 !important;
    color: #78350F !important;
  }

  :global(.live-update-heading) {
    font-size: 0.95rem !important;
    color: #92400E !important;
    line-height: 1.35 !important;
  }

  :global(.live-update-sub) {
    font-size: 0.8rem !important;
    color: #B45309 !important;
    margin-top: 0.25rem !important;
    line-height: 1.4 !important;
  }

  :global(.btn-float-reload) {
    flex-shrink: 0 !important;
    background: linear-gradient(135deg, #EA580C 0%, #D97706 100%) !important;
    color: #FFFFFF !important;
    font-size: 0.85rem !important;
    font-weight: 800 !important;
    padding: 0.6rem 1.1rem !important;
    border-radius: 10px !important;
    border: none !important;
    cursor: pointer !important;
    box-shadow: 0 4px 10px rgba(234, 88, 12, 0.4) !important;
    white-space: nowrap !important;
    animation: btn-attention 1.6s infinite !important;
  }

  @media (max-width: 640px) {
    :global(.live-update-float-inner) {
      flex-direction: column !important;
      align-items: stretch !important;
      gap: 0.75rem !important;
    }
    :global(.btn-float-reload) {
      width: 100% !important;
      text-align: center !important;
    }
  }
'''
    if ':global(.live-update-float-toast)' not in content:
        content = content.replace('</style>', global_css + '\n</style>')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated", filepath)

update_file("app/src/pages/events/coco-pikmin/staging.astro")
update_file("app/src/pages/events/coco-pikmin.astro")
