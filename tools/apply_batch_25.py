import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    store_xiangxinnan = {
        "id": "coco-349",
        "city": "台中市",
        "name": "CoCo都可 南屯向心南店",
        "shortName": "台中南屯向心南",
        "address": "台中市南屯區向心南路966號",
        "phone": "04 2471 0833",
        "lat": 24.13730,
        "lng": 120.64398,
        "coordsText": "24.13730, 120.64398",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.13730,120.64398",
        "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        if not any(s['id'] == store_xiangxinnan['id'] for s in stores):
            stores.append(store_xiangxinnan)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_25 = {
        "batch_id": 25,
        "applied_at": "2026-11-06 07:15:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": store_xiangxinnan["id"],
                "name": store_xiangxinnan["name"],
                "coords": store_xiangxinnan["coordsText"],
                "source": "使用者驗證新增門市（南屯向心南店實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_25)
    if store_xiangxinnan["id"] not in state.setdefault("all_updated_ids", []):
        state["all_updated_ids"].append(store_xiangxinnan["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #25.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 25,
        "version": "25",
        "updated_at": "11/06 07:15",
        "store_count": 347,
        "description": "第 25 波更新 · 新增台中南屯向心南店（核實補全）"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 25, 347 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="24"', 'data-batch-id="25"')
        content = content.replace('11/06 07:10', '11/06 07:15')
        content = content.replace("u.searchParams.set('v', '24');", "u.searchParams.set('v', '25');")
        content = content.replace("346 店最新", "347 店最新")
        content = content.replace("346 店已校對", "347 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 25.")

if __name__ == '__main__':
    main()
