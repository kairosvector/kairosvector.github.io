import json
import sys
import os

def apply_batch42():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'
    manager_path = 'tools/coco_manager.py'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # 1. Add coco-356 (苗栗玉清店)
    if not any(s['id'] == 'coco-356' for s in stores):
        store_356 = {
            "id": "coco-356",
            "city": "苗栗縣",
            "name": "CoCo都可 苗栗玉清店",
            "shortName": "苗栗玉清",
            "address": "苗栗縣苗栗市玉清街9-2號",
            "phone": "03 736 1089",
            "lat": 24.56370,
            "lng": 120.82662,
            "coordsText": "24.56370, 120.82662",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.5637001,120.8266201",
            "route": "新竹市東區＋新竹縣＋苗栗北／中",
            "isUpdated": True,
            "updateStatus": "已更新 (第 42 波 新增門市)",
            "updateDetail": "使用者提報新增苗栗玉清店（玉清街9-2號，全台總數增至 355 店）",
            "updateBatch": 42
        }
        stores.append(store_356)
        print("Added coco-356 (CoCo都可 苗栗玉清店)")

    # 2. Add coco-357 (後龍三民店)
    if not any(s['id'] == 'coco-357' for s in stores):
        store_357 = {
            "id": "coco-357",
            "city": "苗栗縣",
            "name": "CoCo都可 後龍三民店",
            "shortName": "後龍三民",
            "address": "苗栗縣後龍鎮中龍里三民路126號",
            "phone": "03 772 9077",
            "lat": 24.61451,
            "lng": 120.78733,
            "coordsText": "24.61451, 120.78733",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.6145079,120.7873302",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）",
            "isUpdated": True,
            "updateStatus": "已更新 (第 42 波 新增門市)",
            "updateDetail": "使用者提報新增後龍三民店（三民路126號，全台總數增至 356 店）",
            "updateBatch": 42
        }
        stores.append(store_357)
        print("Added coco-357 (CoCo都可 後龍三民店)")

    print(f"Total stores now: {len(stores)}")

    # Write stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update coco_sync_state.json
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    # Check if batch 42 already in batches
    if not any(b.get('batch_id') == 42 for b in state.get('batches', [])):
        batch_42 = {
            "batch_id": 42,
            "applied_at": "2026-11-10 17:30:00 (UTC+8)",
            "target": "Product & Staging",
            "updated_stores_count": 2,
            "updated_stores": [
                {
                    "id": "coco-356",
                    "name": "CoCo都可 苗栗玉清店",
                    "city": "苗栗縣",
                    "action": "新增門市",
                    "coords": "24.56370, 120.82662",
                    "source": "使用者提報新增苗栗玉清店（玉清街9-2號，全台總數增至 355 店）"
                },
                {
                    "id": "coco-357",
                    "name": "CoCo都可 後龍三民店",
                    "city": "苗栗縣",
                    "action": "新增門市",
                    "coords": "24.61451, 120.78733",
                    "source": "使用者提報新增後龍三民店（三民路126號，全台總數增至 356 店）"
                }
            ]
        }
        state['batches'].append(batch_42)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 42,
        "version": "42",
        "updated_at": "11/10 17:30",
        "store_count": len(stores),
        "description": "第 42 波更新 · 新增苗栗玉清店、後龍三民店（苗栗縣增至 20 間，全台總數增至 356 店）"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    # Update RESOLVED_STORES in coco_manager.py
    with open(manager_path, 'r', encoding='utf-8') as f:
        manager_code = f.read()

    new_resolved = (
        '\n    "coco-356",   # 苗栗玉清店 (第42波新增門市)'
        '\n    "CoCo都可 苗栗玉清店",'
        '\n    "CoCo都可(苗栗玉清店)",'
        '\n    "苗栗玉清店",'
        '\n    "苗栗玉清",'
        '\n    "coco-357",   # 後龍三民店 (第42波新增門市)'
        '\n    "CoCo都可 後龍三民店",'
        '\n    "CoCo都可(後龍三民店)",'
        '\n    "後龍三民店",'
        '\n    "後龍三民",'
    )
    if '"coco-356"' not in manager_code:
        manager_code = manager_code.replace('RESOLVED_STORES = {', 'RESOLVED_STORES = {' + new_resolved)

    new_alias = (
        '\n    "CoCo都可 苗栗玉清店": "coco-356",'
        '\n    "CoCo都可(苗栗玉清店)": "coco-356",'
        '\n    "苗栗玉清店": "coco-356",'
        '\n    "苗栗玉清": "coco-356",'
        '\n    "COCO 苗栗玉清": "coco-356",'
        '\n    "CoCo都可 後龍三民店": "coco-357",'
        '\n    "CoCo都可(後龍三民店)": "coco-357",'
        '\n    "後龍三民店": "coco-357",'
        '\n    "後龍三民": "coco-357",'
        '\n    "COCO 後龍三民": "coco-357",'
    )
    if '"苗栗玉清"' not in manager_code:
        manager_code = manager_code.replace('STORE_ALIASES = {', 'STORE_ALIASES = {' + new_alias)

    with open(manager_path, 'w', encoding='utf-8') as f:
        f.write(manager_code)
    print("Updated RESOLVED_STORES and STORE_ALIASES in coco_manager.py.")

    print("Batch #42 applied successfully!")

if __name__ == '__main__':
    apply_batch42()
