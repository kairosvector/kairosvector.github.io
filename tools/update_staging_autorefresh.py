def update_staging_autorefresh():
    path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the checkRemoteVersion function
    old_fn = """    // Auto-detect if user's local cache has older data than Cloudflare server
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
              title.innerHTML = '<strong>最新 ' + remote.store_count + ' 店已釋出</strong>';
            }
            if (btn) {
              btn.classList.add('has-update');
              const label = btn.querySelector('.refresh-label');
              if (label) label.textContent = '更新至 ' + remote.store_count + ' 店';
            }
          }
        })
        .catch(function () {});
    })();"""

    new_fn = """    // Auto-detect & Force Auto-Reload if user's local cache is older than Cloudflare server
    (function checkRemoteVersion() {
      const card = document.getElementById('coco-version-card');
      if (!card) return;

      // On Staging: If URL has no ?v=13, simulate an outdated visitor (batch 12, 334 stores)
      const hasUpdatedParam = window.location.search.includes('v=13');
      const localBatch = hasUpdatedParam ? 13 : 12;
      const localCount = hasUpdatedParam ? 338 : 334;

      // If user just arrived from an auto-reload, show a friendly toast
      if (sessionStorage.getItem('coco_just_auto_reloaded')) {
        sessionStorage.removeItem('coco_just_auto_reloaded');
        setTimeout(function () {
          showToast('已自動為您刷新至最新 338 店門市點位！');
        }, 400);
      }

      fetch('/events/coco-version.json?_t=' + Date.now(), { cache: 'no-store' })
        .then(function (res) { return res.json(); })
        .then(function (remote) {
          if (!remote || !remote.batch_id) return;
          
          // If remote version has newer batch or more stores
          if (remote.batch_id > localBatch || remote.store_count > localCount) {
            const guardKey = 'coco_auto_reloaded_' + remote.batch_id;
            
            // Trigger automatic force reload (once per version update)
            if (!sessionStorage.getItem(guardKey)) {
              sessionStorage.setItem(guardKey, '1');
              sessionStorage.setItem('coco_just_auto_reloaded', '1');
              
              const label = card.querySelector('.refresh-label');
              if (label) label.textContent = '偵測到新點位，自動更新中...';
              
              const u = new URL(window.location.href);
              u.searchParams.set('v', remote.batch_id.toString());
              u.searchParams.set('t', Date.now().toString());
              window.location.replace(u.toString());
              return;
            }

            // Fallback UI if auto-reload was already executed in this session
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
              title.innerHTML = '<strong>最新 ' + remote.store_count + ' 店已釋出</strong>';
            }
            if (btn) {
              btn.classList.add('has-update');
              const label = btn.querySelector('.refresh-label');
              if (label) label.textContent = '更新至 ' + remote.store_count + ' 店';
            }
          }
        })
        .catch(function () {});
    })();"""

    if old_fn in content:
        content = content.replace(old_fn, new_fn, 1)
        print("Updated staging with auto-refresh logic.")
    elif old_fn.replace('\n', '\r\n') in content:
        content = content.replace(old_fn.replace('\n', '\r\n'), new_fn.replace('\n', '\r\n'), 1)
        print("Updated staging (CRLF) with auto-refresh logic.")
    else:
        print("Could not find old_fn in staging.astro!")
        return

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done!")

if __name__ == '__main__':
    update_staging_autorefresh()
