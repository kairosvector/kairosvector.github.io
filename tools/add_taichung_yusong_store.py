import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    new_store = {
        "id": "coco-346",
        "city": "台中市",
        "name": "CoCo都可 台中遠雄店",
        "shortName": "台中遠雄",
        "address": "台中市東區復興路四段186號B1 (iFG遠雄廣場/新時代B1)",
        "phone": "04 2225 0225",
        "lat": 24.13600,
        "lng": 120.68766,
        "coordsText": "24.13600, 120.68766",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.13600,120.68766",
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

    batch_21 = {
        "batch_id": 21,
        "applied_at": "2026-11-05 23:50:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": new_store["id"],
                "name": new_store["name"],
                "coords": new_store["coordsText"],
                "source": "使用者提供新增門市（台中東區iFG遠雄廣場實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_21)
    state.setdefault("all_updated_ids", []).append(new_store["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #21.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 21,
        "version": "21",
        "updated_at": "11/05 23:50",
        "store_count": 344,
        "description": "第 21 波更新 · 新增台中遠雄店"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 21, 344 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="20"', 'data-batch-id="21"')
        content = content.replace('11/05 23:45', '11/05 23:50')
        content = content.replace("u.searchParams.set('v', '20');", "u.searchParams.set('v', '21');")
        content = content.replace("343 店最新", "344 店最新")
        content = content.replace("343 店已校對", "344 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 21.")

if __name__ == '__main__':
    main()
