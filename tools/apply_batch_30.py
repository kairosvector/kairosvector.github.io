import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    updates = {
        "coco-58": {
            "lat": 25.04150,
            "lng": 121.54508,
            "coordsText": "25.04150, 121.54508",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04150,121.54508"
        },
        "coco-314": {
            "lat": 24.18209,
            "lng": 120.59270,
            "coordsText": "24.18209, 120.59270",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.18209,120.59270"
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

    batch_30 = {
        "batch_id": 30,
        "applied_at": "2026-11-06 17:05:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": "coco-58",
                "name": "CoCo都可 忠孝復興店",
                "coords": "25.04150, 121.54508",
                "source": "使用者微調精準點位（忠孝東路三段302號B1捷運出口）"
            },
            {
                "id": "coco-314",
                "name": "CoCo都可 台中東海店",
                "coords": "24.18209, 120.59270",
                "source": "使用者微調精準點位（台灣大道五段3巷32號）"
            }
        ]
    }
    state["batches"].append(batch_30)
    for sid in ["coco-58", "coco-314"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #30.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 30,
        "version": "30",
        "updated_at": "11/06 17:05",
        "store_count": 349,
        "description": "第 30 波更新 · 忠孝復興店、台中東海店 2 間門市座標精準微調",
        "ticker": "最新第 30 波：忠孝復興店、台中東海店 座標已校準！"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 30, 349 stores.")

    # 4. Clear buffer
    with open('app/src/data/coco_verified_buffer.json', 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("Cleared coco_verified_buffer.json.")

    # 5. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="29"', 'data-batch-id="30"')
        content = content.replace('11/06 14:05', '11/06 17:05')
        content = content.replace("u.searchParams.set('v', '29');", "u.searchParams.set('v', '30');")
        content = content.replace("基隆海豐、三重自強、高雄萬家福 已校準！", "忠孝復興店、台中東海店 已校準！")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 30.")

if __name__ == '__main__':
    main()
