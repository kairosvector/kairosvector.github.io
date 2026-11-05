import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    new_store = {
        "id": "coco-345",
        "city": "台中市",
        "name": "CoCo都可 台中火車站店",
        "shortName": "台中火車站",
        "address": "台中市中區台灣大道一段1號1樓 (台中火車站/鐵鹿大街)",
        "phone": "04 2220 0272",
        "lat": 24.13701,
        "lng": 120.68713,
        "coordsText": "24.13701, 120.68713",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.13701,120.68713",
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

    batch_20 = {
        "batch_id": 20,
        "applied_at": "2026-11-05 23:45:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": new_store["id"],
                "name": new_store["name"],
                "coords": new_store["coordsText"],
                "source": "使用者提供新增門市（台中火車站鐵鹿大街實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_20)
    state.setdefault("all_updated_ids", []).append(new_store["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #20.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 20,
        "version": "20",
        "updated_at": "11/05 23:45",
        "store_count": 343,
        "description": "第 20 波更新 · 新增台中火車站店"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 20, 343 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="19"', 'data-batch-id="20"')
        content = content.replace('11/05 23:30', '11/05 23:45')
        content = content.replace("u.searchParams.set('v', '19');", "u.searchParams.set('v', '20');")
        content = content.replace("342 店最新", "343 店最新")
        content = content.replace("342 店已校對", "343 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 20.")

if __name__ == '__main__':
    main()
