import json

def bump():
    # 1. Bump coco-version.json to batch 14
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 14,
        "version": "14",
        "updated_at": "11/05 18:28",
        "store_count": 338,
        "description": "第 14 波更新 · 引擎自動換新測試"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Bumped app/public/events/coco-version.json to batch 14")

    # 2. Update staging.astro to batch 14
    staging_path = 'app/src/pages/events/coco-pikmin/staging.astro'
    with open(staging_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('data-batch-id="13"', 'data-batch-id="14"')
    content = content.replace('11/05 17:25', '11/05 18:28')

    # Ensure JS uses dynamic data-batch-id attribute
    old_js_block = """      // On Staging: If URL has no ?v=13, simulate an outdated visitor (batch 12, 334 stores)
      const hasUpdatedParam = window.location.search.includes('v=13');
      const localBatch = hasUpdatedParam ? 13 : 12;
      const localCount = hasUpdatedParam ? 338 : 334;

      // If user just arrived from an auto-reload, show a friendly toast
      if (sessionStorage.getItem('coco_just_auto_reloaded')) {
        sessionStorage.removeItem('coco_just_auto_reloaded');
        setTimeout(function () {
          showToast('已自動為您刷新至最新 338 店門市點位！');
        }, 400);
      }"""

    new_js_block = """      const localBatch = parseInt(card.getAttribute('data-batch-id') || '0', 10);
      const localCount = parseInt(card.getAttribute('data-store-count') || '0', 10);

      // If user just arrived from an auto-reload, show a friendly toast
      if (sessionStorage.getItem('coco_just_auto_reloaded')) {
        sessionStorage.removeItem('coco_just_auto_reloaded');
        setTimeout(function () {
          showToast('已偵測到新版本，自動為您刷新至最新點位！');
        }, 400);
      }"""

    if old_js_block in content:
        content = content.replace(old_js_block, new_js_block)
        print("Replaced JS with dynamic data-batch-id read.")
    elif old_js_block.replace('\n', '\r\n') in content:
        content = content.replace(old_js_block.replace('\n', '\r\n'), new_js_block.replace('\n', '\r\n'))
        print("Replaced JS (CRLF) with dynamic data-batch-id read.")

    with open(staging_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated staging.astro successfully.")

if __name__ == '__main__':
    bump()
