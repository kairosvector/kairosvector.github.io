import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    new_store = {
        "id": "coco-344",
        "city": "台北市",
        "name": "CoCo都可 微風南山店",
        "shortName": "台北微風南山",
        "address": "台北市信義區松智路17號B2 (微風南山B2)",
        "phone": "02 6638 9999",
        "lat": 25.03459,
        "lng": 121.56601,
        "coordsText": "25.03459, 121.56601",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.03459,121.56601",
        "route": "東北線：基隆＋宜蘭＋台北東北區"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        # Update coco-116 新店裕隆城
        for s in stores:
            if s['id'] == 'coco-116':
                s['lat'] = 24.97807
                s['lng'] = 121.54653
                s['coordsText'] = "24.97807, 121.54653"
                s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=24.97807,121.54653"

        # Update coco-332 台北南機場
        for s in stores:
            if s['id'] == 'coco-332':
                s['address'] = '台北市中正區中華路二段307巷18號'
                s['phone'] = '02 2301 0042'
                s['lat'] = 25.02820
                s['lng'] = 121.50624
                s['coordsText'] = "25.02820, 121.50624"
                s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=25.02820,121.50624"

        # Check and add coco-344
        if not any(s['id'] == new_store['id'] for s in stores):
            stores.append(new_store)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_19 = {
        "batch_id": 19,
        "applied_at": "2026-11-05 23:30:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": new_store["id"],
                "name": new_store["name"],
                "coords": new_store["coordsText"],
                "source": "使用者提供新增門市（微風南山B2實體店核實補全）"
            },
            {
                "id": "coco-116",
                "name": "CoCo都可 新店裕隆城店",
                "coords": "24.97807, 121.54653",
                "source": "表單玩家提供微調（自建築中心微調31米至B1美食街櫃位）"
            }
        ]
    }
    state["batches"].append(batch_19)
    if new_store["id"] not in state.setdefault("all_updated_ids", []):
        state["all_updated_ids"].append(new_store["id"])
    if "coco-116" not in state["all_updated_ids"]:
        state["all_updated_ids"].append("coco-116")

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #19.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 19,
        "version": "19",
        "updated_at": "11/05 23:30",
        "store_count": 342,
        "description": "第 19 波更新 · 新增微風南山店、新店裕隆城精準微調"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 19, 342 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="18"', 'data-batch-id="19"')
        content = content.replace('11/05 21:25', '11/05 23:30')
        content = content.replace("u.searchParams.set('v', '18');", "u.searchParams.set('v', '19');")
        content = content.replace("341 店最新", "342 店最新")
        content = content.replace("341 店已校對", "342 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 19.")

if __name__ == '__main__':
    main()
