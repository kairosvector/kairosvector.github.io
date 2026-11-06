import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    updates = {
        "coco-5": {
            "lat": 25.13602,
            "lng": 121.78700,
            "coordsText": "25.13602, 121.78700",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.13602,121.78700"
        },
        "coco-68": {
            "lat": 25.06732,
            "lng": 121.49258,
            "coordsText": "25.06732, 121.49258",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.06732,121.49258"
        },
        "coco-325": {
            "lat": 22.60508,
            "lng": 120.30445,
            "coordsText": "22.60508, 120.30445",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.60508,120.30445"
        }
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        for s in stores:
            if s['id'] in updates:
                u = updates[s['id']]
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

    batch_29 = {
        "batch_id": 29,
        "applied_at": "2026-11-06 14:05:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 3,
        "updated_stores": [
            {
                "id": "coco-5",
                "name": "CoCo都可 基隆海豐店",
                "coords": "25.13602, 121.78700",
                "source": "使用者微調精準點位（新豐街306號）"
            },
            {
                "id": "coco-68",
                "name": "CoCo都可 三重自強店",
                "coords": "25.06732, 121.49258",
                "source": "使用者微調精準點位（自強路一段250號）"
            },
            {
                "id": "coco-325",
                "name": "CoCo都可 萬家福店",
                "coords": "22.60508, 120.30445",
                "source": "網友回報經使用者查核確認微調（高雄家樂福成功店/萬家福商場）"
            }
        ]
    }
    state["batches"].append(batch_29)
    for sid in ["coco-5", "coco-68", "coco-325"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #29.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 29,
        "version": "29",
        "updated_at": "11/06 14:05",
        "store_count": 349,
        "description": "第 29 波更新 · 基隆海豐、三重自強、高雄萬家福 3 間門市座標精準微調"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 29, 349 stores.")

    # 4. Clear buffer
    with open('app/src/data/coco_verified_buffer.json', 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("Cleared coco_verified_buffer.json.")

    # 5. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="28"', 'data-batch-id="29"')
        content = content.replace('11/06 10:25', '11/06 14:05')
        content = content.replace("u.searchParams.set('v', '28');", "u.searchParams.set('v', '29');")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 29.")

if __name__ == '__main__':
    main()
