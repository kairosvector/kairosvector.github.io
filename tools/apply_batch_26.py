import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    store_qidu = {
        "id": "coco-350",
        "city": "基隆市",
        "name": "CoCo都可 基隆七堵店",
        "shortName": "基隆七堵",
        "address": "基隆市七堵區明德一路196號",
        "phone": "02 2455 8339",
        "lat": 25.09744,
        "lng": 121.71289,
        "coordsText": "25.09744, 121.71289",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.09744,121.71289",
        "route": "東北線：基隆＋宜蘭＋台北東北區"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        if not any(s['id'] == store_qidu['id'] for s in stores):
            stores.append(store_qidu)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_26 = {
        "batch_id": 26,
        "applied_at": "2026-11-06 07:20:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": store_qidu["id"],
                "name": store_qidu["name"],
                "coords": store_qidu["coordsText"],
                "source": "使用者驗證新增門市（基隆七堵店實體店核實補全，25.0974408, 121.7128851）"
            }
        ]
    }
    state["batches"].append(batch_26)
    if store_qidu["id"] not in state.setdefault("all_updated_ids", []):
        state["all_updated_ids"].append(store_qidu["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #26.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 26,
        "version": "26",
        "updated_at": "11/06 07:20",
        "store_count": 348,
        "description": "第 26 波更新 · 新增基隆七堵店（核實補全）"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 26, 348 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="25"', 'data-batch-id="26"')
        content = content.replace('11/06 07:15', '11/06 07:20')
        content = content.replace("u.searchParams.set('v', '25');", "u.searchParams.set('v', '26');")
        content = content.replace("347 店最新", "348 店最新")
        content = content.replace("347 店已校對", "348 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 26.")

if __name__ == '__main__':
    main()
