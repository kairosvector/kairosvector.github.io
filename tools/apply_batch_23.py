import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    store_yuandong_jucheng = {
        "id": "coco-348",
        "city": "新竹市",
        "name": "CoCo都可 遠東巨城店",
        "shortName": "新竹遠東巨城",
        "address": "新竹市東區中央路229號",
        "phone": "03 532 8120",
        "lat": 24.80954,
        "lng": 120.97500,
        "coordsText": "24.80954, 120.97500",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.80954,120.97500",
        "route": "新竹市東區＋新竹縣＋苗栗北／中"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        # Add store_yuandong_jucheng if not present
        if not any(s['id'] == store_yuandong_jucheng['id'] for s in stores):
            stores.append(store_yuandong_jucheng)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_23 = {
        "batch_id": 23,
        "applied_at": "2026-11-06 07:05:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": store_yuandong_jucheng["id"],
                "name": store_yuandong_jucheng["name"],
                "coords": store_yuandong_jucheng["coordsText"],
                "source": "使用者驗證新增門市（巨城雙門市核實：保留中央路207號新竹巨城店，新增中央路229號遠東巨城店）"
            }
        ]
    }
    state["batches"].append(batch_23)
    if store_yuandong_jucheng["id"] not in state.setdefault("all_updated_ids", []):
        state["all_updated_ids"].append(store_yuandong_jucheng["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #23.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 23,
        "version": "23",
        "updated_at": "11/06 07:05",
        "store_count": 346,
        "description": "第 23 波更新 · 新增新竹遠東巨城店（Big City館內獨立門市）"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 23, 346 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="22"', 'data-batch-id="23"')
        content = content.replace('11/06 06:50', '11/06 07:05')
        content = content.replace("u.searchParams.set('v', '22');", "u.searchParams.set('v', '23');")
        content = content.replace("345 店最新", "346 店最新")
        content = content.replace("345 店已校對", "346 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 23.")

if __name__ == '__main__':
    main()
