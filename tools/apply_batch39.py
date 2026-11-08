import json
import sys
import os

def apply_batch39():
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
        "coco-55": {
            "lat": 25.03440,
            "lng": 121.52719,
            "coordsText": "25.03440, 121.52719",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.03440,121.52719",
            "source": "使用者實勘微調（台北金山店信義路二段91-4號，偏移約 23.5m 至金山南路口騎樓門市）"
        },
        "coco-203": {
            "lat": 24.97405,
            "lng": 121.25575,
            "coordsText": "24.97405, 121.25575",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.97405,121.25575",
            "source": "使用者實勘微調（桃園內壢忠孝店中壢區忠孝路69號，偏移約 23.1m 至店面正門）"
        },
        "coco-214": {
            "lat": 24.90101,
            "lng": 121.28363,
            "coordsText": "24.90101, 121.28363",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.90101,121.28363",
            "source": "使用者實勘微調（桃園大溪崎頂店介壽路844-5號，偏移約 17.9m 至店面門牌）"
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
            s['updateStatus'] = "已更新 (第 39 波 座標校正)"
            s['updateDetail'] = u['source']
            s['updateBatch'] = 39
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

    batch_39 = {
        "batch_id": 39,
        "applied_at": "2026-11-09 07:15:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 3,
        "updated_stores": [
            {
                "id": "coco-55",
                "name": "CoCo都可 金山店",
                "city": "台北市",
                "coords": "25.03440, 121.52719",
                "source": "使用者實勘微調（台北金山店信義路二段91-4號，偏移約 23.5m 至金山南路口騎樓門市）"
            },
            {
                "id": "coco-203",
                "name": "CoCo都可 內壢忠孝店",
                "city": "桃園市",
                "coords": "24.97405, 121.25575",
                "source": "使用者實勘微調（桃園內壢忠孝店中壢區忠孝路69號，偏移約 23.1m 至店面正門）"
            },
            {
                "id": "coco-214",
                "name": "CoCo都可 大溪崎頂店",
                "city": "桃園市",
                "coords": "24.90101, 121.28363",
                "source": "使用者實勘微調（桃園大溪崎頂店介壽路844-5號，偏移約 17.9m 至店面門牌）"
            }
        ]
    }

    state['batches'].append(batch_39)

    # Also record the passed stores in confirmed_correct_stores
    passed_stores = ["coco-149", "coco-42", "coco-19"]
    confirmed = state.get("confirmed_correct_stores", [])
    for p in passed_stores:
        if p not in confirmed:
            confirmed.append(p)
    state["confirmed_correct_stores"] = confirmed

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 39,
        "version": "39",
        "updated_at": "11/09 07:15",
        "store_count": len(stores),
        "description": "第 39 波更新 · 精準校正台北金山店、桃園內壢忠孝店、桃園大溪崎頂店"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    # Clear pending verification file completely as all items are now resolved or passed
    with open(pending_path, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("Cleared pending verification list.")

    # Update RESOLVED_STORES in coco_manager.py
    with open(manager_path, 'r', encoding='utf-8') as f:
        manager_code = f.read()

    new_resolved = '\n    "coco-55",    # 金山店 (第39波已校正)\n    "coco-203",   # 內壢忠孝店 (第39波已校正)\n    "coco-214",   # 大溪崎頂店 (第39波已校正)\n    "coco-149",   # 桃園介壽店 (使用者確認Pass)\n    "coco-42",    # 台北華齡店 (使用者確認Pass)\n    "coco-19",    # 台北林森北店 (使用者確認Pass)'
    if '"coco-203"' not in manager_code:
        manager_code = manager_code.replace('RESOLVED_STORES = {', 'RESOLVED_STORES = {' + new_resolved)
        with open(manager_path, 'w', encoding='utf-8') as f:
            f.write(manager_code)
        print("Updated RESOLVED_STORES in coco_manager.py.")

    print("Batch #39 applied successfully!")

if __name__ == '__main__':
    apply_batch39()
