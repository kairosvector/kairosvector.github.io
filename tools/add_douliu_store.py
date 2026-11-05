import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    new_store = {
        "id": "coco-341",
        "city": "雲林縣",
        "name": "CoCo都可 斗六萬家福",
        "shortName": "雲林斗六萬家福",
        "address": "雲林縣斗六市雲林路二段297號",
        "phone": "05 537 5500",
        "lat": 23.70152,
        "lng": 120.53048,
        "coordsText": "23.70152, 120.53048",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=23.70152,120.53048",
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

    batch_16 = {
        "batch_id": 16,
        "applied_at": "2026-11-05 20:30:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": new_store["id"],
                "name": new_store["name"],
                "coords": new_store["coordsText"],
                "source": "使用者提供新增門市（雲林斗六萬家福實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_16)
    state.setdefault("all_updated_ids", []).append(new_store["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #16.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 16,
        "version": "16",
        "updated_at": "11/05 20:30",
        "store_count": 339,
        "description": "第 16 波更新 · 新增雲林斗六萬家福"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 16, 339 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="15"', 'data-batch-id="16"')
        content = content.replace('11/05 20:25', '11/05 20:30')
        content = content.replace("u.searchParams.set('v', '15');", "u.searchParams.set('v', '16');")
        content = content.replace("338 店最新", "339 店最新")
        content = content.replace("338 店已校對", "339 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 16.")

if __name__ == '__main__':
    main()
