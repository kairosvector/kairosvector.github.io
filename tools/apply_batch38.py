import json
import sys
import os

def apply_batch38():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'
    manager_path = 'tools/coco_manager.py'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # Check if coco-354 already exists
    if not any(s['id'] == 'coco-354' for s in stores):
        new_store = {
            "id": "coco-354",
            "city": "台中市",
            "name": "CoCo都可 豐原太平洋店",
            "shortName": "豐原太平洋",
            "address": "台中市豐原區復興路2號 (太平洋百貨B1生活美食街)",
            "phone": "04 2525 0253",
            "lat": 24.25098,
            "lng": 120.72066,
            "coordsText": "24.25098, 120.72066",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.25098,120.72066",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）",
            "isUpdated": True,
            "updateStatus": "已更新 (第 38 波 新增門市)",
            "updateDetail": "使用者提報新增台中豐原太平洋百貨B1門市（復興路2號B1，台中市增至 24 間，全台總店數增至 353 店）",
            "updateBatch": 38
        }
        stores.append(new_store)
        print(f"Added coco-354 (CoCo都可 豐原太平洋店), total stores: {len(stores)}")

    # Write stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update coco_sync_state.json
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_38 = {
        "batch_id": 38,
        "applied_at": "2026-11-08 19:50:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": "coco-354",
                "name": "CoCo都可 豐原太平洋店",
                "city": "台中市",
                "action": "新增門市",
                "coords": "24.25098, 120.72066",
                "source": "使用者提報新增台中豐原太平洋百貨B1門市（復興路2號B1，台中市增至 24 間，全台總店數增至 353 店）"
            }
        ]
    }

    state['batches'].append(batch_38)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 38,
        "version": "38",
        "updated_at": "11/08 19:50",
        "store_count": len(stores),
        "description": "第 38 波更新 · 新增台中豐原太平洋店（全台總店數增至 353 間）"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    # Update RESOLVED_STORES in coco_manager.py
    with open(manager_path, 'r', encoding='utf-8') as f:
        manager_code = f.read()

    new_resolved = '\n    "coco-354",   # 豐原太平洋店 (第38波新增門市)\n    "CoCo都可 豐原太平洋店",'
    if '"coco-354"' not in manager_code:
        manager_code = manager_code.replace('RESOLVED_STORES = {', 'RESOLVED_STORES = {' + new_resolved)
        with open(manager_path, 'w', encoding='utf-8') as f:
            f.write(manager_code)
        print("Updated RESOLVED_STORES in coco_manager.py.")

    print("Batch #38 applied successfully!")

if __name__ == '__main__':
    apply_batch38()
