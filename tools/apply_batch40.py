import json
import sys
import os

def apply_batch40():
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
        "coco-78": {
            "lat": 25.02450,
            "lng": 121.42470,
            "coordsText": "25.02450, 121.42470",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.02450,121.42470",
            "source": "使用者實勘微調（新北新莊富國店富國路131號，偏移約 21.2m 至實體店門口）"
        },
        "coco-291": {
            "lat": 24.41110,
            "lng": 120.76849,
            "coordsText": "24.41110, 120.76849",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.41110,120.76849",
            "source": "使用者實勘微調（苗栗三義店中正路168號，偏移約 9.8m 至實體店門口）"
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
            s['updateStatus'] = "已更新 (第 40 波 座標校正)"
            s['updateDetail'] = u['source']
            s['updateBatch'] = 40
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

    batch_40 = {
        "batch_id": 40,
        "applied_at": "2026-11-09 14:18:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": "coco-78",
                "name": "CoCo都可 新莊富國店",
                "city": "新北市",
                "coords": "25.02450, 121.42470",
                "source": "使用者實勘微調（新北新莊富國店富國路131號，偏移約 21.2m 至實體店門口）"
            },
            {
                "id": "coco-291",
                "name": "CoCo都可(苗栗三義店)",
                "city": "苗栗縣",
                "coords": "24.41110, 120.76849",
                "source": "使用者實勘微調（苗栗三義店中正路168號，偏移約 9.8m 至實體店門口）"
            }
        ]
    }

    state['batches'].append(batch_40)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 40,
        "version": "40",
        "updated_at": "11/09 14:18",
        "store_count": len(stores),
        "description": "第 40 波更新 · 精準微調新北新莊富國店、苗栗三義店"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    # Clear pending verification file
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

    new_resolved = '\n    "coco-78",    # 新莊富國店 (第40波已校正)\n    "coco-291",   # 苗栗三義店 (第40波已校正)'
    if '"coco-78"' not in manager_code:
        manager_code = manager_code.replace('RESOLVED_STORES = {', 'RESOLVED_STORES = {' + new_resolved)
        with open(manager_path, 'w', encoding='utf-8') as f:
            f.write(manager_code)
        print("Updated RESOLVED_STORES in coco_manager.py.")

    print("Batch #40 applied successfully!")

if __name__ == '__main__':
    apply_batch40()
