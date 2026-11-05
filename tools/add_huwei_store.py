import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    new_store = {
        "id": "coco-340",
        "city": "雲林縣",
        "name": "CoCo都可 虎尾中正店",
        "shortName": "雲林虎尾中正",
        "address": "雲林縣虎尾鎮中正路125號",
        "phone": "05 632 6083",
        "lat": 23.70814,
        "lng": 120.43351,
        "coordsText": "23.70814, 120.43351",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=23.70814,120.43351",
        "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)
        
        # Check if already present
        if not any(s['id'] == new_store['id'] for s in stores):
            stores.append(new_store)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_15 = {
        "batch_id": 15,
        "applied_at": "2026-11-05 20:25:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": new_store["id"],
                "name": new_store["name"],
                "coords": new_store["coordsText"],
                "source": "使用者提供新增門市（雲林實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_15)
    state.setdefault("all_updated_ids", []).append(new_store["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #15.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 15,
        "version": "15",
        "updated_at": "11/05 20:25",
        "store_count": 338,
        "description": "第 15 波更新 · 新增雲林虎尾中正店"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 15, 338 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="14"', 'data-batch-id="15"')
        content = content.replace('11/05 20:10', '11/05 20:25')
        content = content.replace("u.searchParams.set('v', '14');", "u.searchParams.set('v', '15');")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 15.")

if __name__ == '__main__':
    main()
