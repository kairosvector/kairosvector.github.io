import json
import sys
import os

def apply_batch37():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'
    pending_path = 'app/src/data/coco_pending_verification.json'
    manager_path = 'tools/coco_manager.py'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    updates = {
        "coco-15": {
            "lat": 24.67776,
            "lng": 121.76716,
            "coordsText": "24.67776, 121.76716",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.67776,121.76716",
            "source": "使用者實勘微調（宜蘭羅東門市民生路120號，偏移約 15.6m 至實體店門口）"
        },
        "coco-29": {
            "lat": 25.08483,
            "lng": 121.59323,
            "coordsText": "25.08483, 121.59323",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.08483,121.59323",
            "source": "使用者實勘微調（台北內湖金龍店金龍路56號一樓，偏移約 13.5m 至正門）"
        },
        "coco-46": {
            "lat": 25.05209,
            "lng": 121.54562,
            "coordsText": "25.05209, 121.54562",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.05209,121.54562",
            "source": "使用者實勘微調（台北南京店南京東路三段285號，近南京復興站，偏移約 23.5m）"
        }
    }

    modified_count = 0
    for s in stores:
        if s['id'] in updates:
            u = updates[s['id']]
            s['lat'] = u['lat']
            s['lng'] = u['lng']
            s['coordsText'] = u['coordsText']
            s['gmapUrl'] = u['gmapUrl']
            s['isUpdated'] = True
            s['updateStatus'] = "已更新 (第 37 波 座標校正)"
            s['updateDetail'] = u['source']
            s['updateBatch'] = 37
            modified_count += 1
            print(f"Updated {s['id']} {s['name']} -> {s['coordsText']}")

    print(f"Total stores updated: {modified_count}")

    # Write stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update coco_sync_state.json
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_37 = {
        "batch_id": 37,
        "applied_at": "2026-11-08 19:48:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 3,
        "updated_stores": [
            {
                "id": "coco-15",
                "name": "CoCo都可（羅東門市）",
                "city": "宜蘭縣",
                "coords": "24.67776, 121.76716",
                "source": "使用者實勘微調（宜蘭羅東門市民生路120號，偏移約 15.6m 至實體店門口）"
            },
            {
                "id": "coco-29",
                "name": "CoCo都可 內湖金龍店",
                "city": "台北市",
                "coords": "25.08483, 121.59323",
                "source": "使用者實勘微調（台北內湖金龍店金龍路56號一樓，偏移約 13.5m 至正門）"
            },
            {
                "id": "coco-46",
                "name": "CoCo都可(台北南京店)",
                "city": "台北市",
                "coords": "25.05209, 121.54562",
                "source": "使用者實勘微調（台北南京店南京東路三段285號，近南京復興站，偏移約 23.5m）"
            }
        ]
    }

    state['batches'].append(batch_37)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 37,
        "version": "37",
        "updated_at": "11/08 19:48",
        "store_count": len(stores),
        "description": "第 37 波更新 · 精準校正宜蘭羅東門市、台北內湖金龍店、台北南京店"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    # Remove calibrated stores from pending verification
    if os.path.exists(pending_path):
        with open(pending_path, 'r', encoding='utf-8') as f:
            pending = json.load(f)
        pending = [p for p in pending if p.get('store_id') not in updates]
        with open(pending_path, 'w', encoding='utf-8') as f:
            json.dump(pending, f, ensure_ascii=False, indent=2)
        print("Updated pending verification list.")

    # Update RESOLVED_STORES in coco_manager.py
    with open(manager_path, 'r', encoding='utf-8') as f:
        manager_code = f.read()

    new_resolved = '\n    "coco-15",    # 羅東門市 (第37波已校正)\n    "coco-29",    # 內湖金龍店 (第37波已校正)\n    "coco-46",    # 台北南京店 (第37波已校正)'
    if '"coco-15"' not in manager_code:
        manager_code = manager_code.replace('RESOLVED_STORES = {', 'RESOLVED_STORES = {' + new_resolved)
        with open(manager_path, 'w', encoding='utf-8') as f:
            f.write(manager_code)
        print("Updated RESOLVED_STORES in coco_manager.py.")

    print("Batch #37 applied successfully!")

if __name__ == '__main__':
    apply_batch37()
