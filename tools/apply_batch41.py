import json
import sys
import os

def apply_batch41():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'
    manager_path = 'tools/coco_manager.py'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # Check if coco-355 already exists
    if not any(s['id'] == 'coco-355' for s in stores):
        new_store = {
            "id": "coco-355",
            "city": "高雄市",
            "name": "CoCo都可 楠梓後昌店",
            "shortName": "楠梓後昌店",
            "address": "高雄市楠梓區後昌路737號1樓",
            "phone": "07 301 0032",
            "lat": 22.70957,
            "lng": 120.29667,
            "coordsText": "22.70957, 120.29667",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.7095709,120.29667",
            "route": "【中南部】高屏南台南線（含外島）",
            "isUpdated": True,
            "updateStatus": "已更新 (第 41 波 新增門市)",
            "updateDetail": "使用者提報新增高雄楠梓後昌店（後昌路737號1樓，全台總數增至 354 店）",
            "updateBatch": 41
        }
        stores.append(new_store)
        print(f"Added coco-355 (CoCo都可 楠梓後昌店), total stores: {len(stores)}")

    # Write stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update coco_sync_state.json
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_41 = {
        "batch_id": 41,
        "applied_at": "2026-11-09 19:30:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": "coco-355",
                "name": "CoCo都可 楠梓後昌店",
                "city": "高雄市",
                "action": "新增門市",
                "coords": "22.70957, 120.29667",
                "source": "使用者提報新增高雄楠梓後昌店（後昌路737號1樓，全台總數增至 354 店）"
            }
        ]
    }

    state['batches'].append(batch_41)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 41,
        "version": "41",
        "updated_at": "11/09 19:30",
        "store_count": len(stores),
        "description": "第 41 波更新 · 新增高雄楠梓後昌店（全台總數增至 354 店）"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    # Update RESOLVED_STORES in coco_manager.py
    with open(manager_path, 'r', encoding='utf-8') as f:
        manager_code = f.read()

    new_resolved = '\n    "coco-355",   # 楠梓後昌店 (第41波新增門市)\n    "CoCo都可 楠梓後昌店",\n    "CoCo都可 南梓後昌店",'
    if '"coco-355"' not in manager_code:
        manager_code = manager_code.replace('RESOLVED_STORES = {', 'RESOLVED_STORES = {' + new_resolved)

    new_alias = '\n    "CoCo都可 南梓後昌店": "coco-355",\n    "CoCo都可(南梓後昌店)": "coco-355",\n    "南梓後昌店": "coco-355",'
    if '"南梓後昌店"' not in manager_code:
        manager_code = manager_code.replace('STORE_ALIASES = {', 'STORE_ALIASES = {' + new_alias)

    with open(manager_path, 'w', encoding='utf-8') as f:
        f.write(manager_code)
    print("Updated RESOLVED_STORES and STORE_ALIASES in coco_manager.py.")

    print("Batch #41 applied successfully!")

if __name__ == '__main__':
    apply_batch41()
