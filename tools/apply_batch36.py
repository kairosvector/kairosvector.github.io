import json
import sys
import os

def apply_batch36():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # Add coco-353 (高雄小港機場店)
    if not any(s['id'] == 'coco-353' for s in stores):
        new_store = {
            "id": "coco-353",
            "city": "高雄市",
            "name": "CoCo都可 高雄小港機場店",
            "shortName": "高雄小港機場",
            "address": "高雄市小港區中山四路2號 (國際線航廈1F到達大廳)",
            "phone": "07 801 0565",
            "lat": 22.57120,
            "lng": 120.34020,
            "coordsText": "22.57120, 120.34020",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.57120,120.34020",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）",
            "isUpdated": True,
            "updateStatus": "已更新 (第 36 波 新增門市)",
            "updateDetail": "使用者提報新增高雄國際航空站航廈門市（中山四路2號國際線1F到達大廳，高雄市增至 12 間，全台總店數增至 352 店）",
            "updateBatch": 36
        }
        stores.append(new_store)
        print(f"Added coco-353 (高雄小港機場店), total stores: {len(stores)}")

    # Save stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update coco_sync_state.json
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_36 = {
        "batch_id": 36,
        "applied_at": "2026-11-07 15:52:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": "coco-353",
                "name": "CoCo都可 高雄小港機場店",
                "city": "高雄市",
                "action": "新增門市",
                "coords": "22.57120, 120.34020",
                "source": "使用者提報新增高雄國際航空站航廈門市（中山四路2號國際線1F到達大廳，高雄市增至 12 間，全台總店數增至 352 店）"
            }
        ]
    }

    state['batches'].append(batch_36)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update coco-version.json
    version_data = {
        "batch_id": 36,
        "version": "36",
        "updated_at": "11/07 15:52",
        "store_count": len(stores),
        "description": "第 36 波更新 · 新增高雄小港機場店（全台總店數增至 352 間）"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    print("Batch #36 applied successfully!")

if __name__ == '__main__':
    apply_batch36()
