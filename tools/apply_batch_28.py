import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    beiche_updates = {
        "coco-49": {
            "name": "CoCo都可 台北站前店",
            "shortName": "台北站前",
            "lat": 25.04499,
            "lng": 121.51627,
            "coordsText": "25.04499, 121.51627",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04499,121.51627"
        },
        "coco-51": {
            "name": "CoCo都可 捷運北車2店",
            "shortName": "捷運北車2",
            "lat": 25.04640,
            "lng": 121.51764,
            "coordsText": "25.04640, 121.51764",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04640,121.51764"
        },
        "coco-52": {
            "name": "CoCo都可 捷運北車店",
            "shortName": "捷運北車",
            "lat": 25.04817,
            "lng": 121.51845,
            "coordsText": "25.04817, 121.51845",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04817,121.51845"
        },
        "coco-53": {
            "name": "CoCo都可 台北開封",
            "shortName": "台北開封",
            "lat": 25.04610,
            "lng": 121.51351,
            "coordsText": "25.04610, 121.51351",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04610,121.51351"
        }
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        for s in stores:
            if s['id'] in beiche_updates:
                u = beiche_updates[s['id']]
                s['name'] = u['name']
                s['shortName'] = u['shortName']
                s['lat'] = u['lat']
                s['lng'] = u['lng']
                s['coordsText'] = u['coordsText']
                s['gmapUrl'] = u['gmapUrl']

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_28 = {
        "batch_id": 28,
        "applied_at": "2026-11-06 10:25:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 4,
        "updated_stores": [
            {
                "id": "coco-51",
                "name": "CoCo都可 捷運北車2店",
                "coords": "25.04640, 121.51764",
                "source": "使用者以遊戲官方內核實校正（修正原南陽街疊標211米偏差，移至M3出口真實點位）"
            },
            {
                "id": "coco-49",
                "name": "CoCo都可 台北站前店",
                "coords": "25.04499, 121.51627",
                "source": "使用者以遊戲官方內核實校正（名稱去除括號、點位微調至官方點）"
            },
            {
                "id": "coco-52",
                "name": "CoCo都可 捷運北車店",
                "coords": "25.04817, 121.51845",
                "source": "使用者以遊戲官方內核實微調至官方點"
            },
            {
                "id": "coco-53",
                "name": "CoCo都可 台北開封",
                "coords": "25.04610, 121.51351",
                "source": "使用者以遊戲官方內核實微調至官方點"
            }
        ]
    }
    state["batches"].append(batch_28)
    for sid in ["coco-49", "coco-51", "coco-52", "coco-53"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #28.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 28,
        "version": "28",
        "updated_at": "11/06 10:25",
        "store_count": 349,
        "description": "第 28 波更新 · 台北車站商圈 4 間門市全面校準為遊戲官方點位與名稱"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 28, 349 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="27"', 'data-batch-id="28"')
        content = content.replace('11/06 09:35', '11/06 10:25')
        content = content.replace("u.searchParams.set('v', '27');", "u.searchParams.set('v', '28');")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 28.")

if __name__ == '__main__':
    main()
