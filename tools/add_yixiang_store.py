import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    new_store = {
        "id": "coco-343",
        "city": "高雄市",
        "name": "CoCo都可 義享店",
        "shortName": "高雄義享",
        "address": "高雄市鼓山區大順一路115號B2 (義享時尚廣場B2)",
        "phone": "07 556 1058",
        "lat": 22.65613,
        "lng": 120.30649,
        "coordsText": "22.65613, 120.30649",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.65613,120.30649",
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

    batch_18 = {
        "batch_id": 18,
        "applied_at": "2026-11-05 21:25:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": new_store["id"],
                "name": new_store["name"],
                "coords": new_store["coordsText"],
                "source": "使用者提供新增門市（高雄義享時尚廣場實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_18)
    state.setdefault("all_updated_ids", []).append(new_store["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #18.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 18,
        "version": "18",
        "updated_at": "11/05 21:25",
        "store_count": 341,
        "description": "第 18 波更新 · 新增高雄義享店"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 18, 341 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="17"', 'data-batch-id="18"')
        content = content.replace('11/05 20:35', '11/05 21:25')
        content = content.replace("u.searchParams.set('v', '17');", "u.searchParams.set('v', '18');")
        content = content.replace("340 店最新", "341 店最新")
        content = content.replace("340 店已校對", "341 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 18.")

if __name__ == '__main__':
    main()
