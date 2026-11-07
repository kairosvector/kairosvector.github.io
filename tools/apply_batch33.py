import json
import sys
import os

def apply_batch33():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # Check if coco-266 already exists
    if any(s['id'] == 'coco-266' for s in stores):
        print("coco-266 already in stores!")
        return

    new_store = {
        "id": "coco-266",
        "city": "新竹縣",
        "name": "CoCo都可 新豐尚仁店",
        "shortName": "新竹新豐尚仁",
        "address": "304新竹縣新豐鄉松柏村尚仁街2-3號",
        "phone": "03 557 6078",
        "lat": 24.86688,
        "lng": 120.99024,
        "coordsText": "24.86688, 120.99024",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.86688,120.99024",
        "route": "新竹市東區＋新竹縣＋苗栗北／中"
    }

    # Find position of coco-265
    insert_idx = None
    for i, s in enumerate(stores):
        if s['id'] == 'coco-265':
            insert_idx = i + 1
            break

    if insert_idx is not None:
        stores.insert(insert_idx, new_store)
    else:
        stores.append(new_store)

    print(f"Total stores after insert: {len(stores)}")

    # Save stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update sync state
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    # Remove coco-266 from removed_stores
    state['removed_stores'] = [s for s in state.get('removed_stores', []) if s['id'] != 'coco-266']

    batch_33 = {
        "batch_id": 33,
        "applied_at": "2026-11-07 09:57:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": "coco-266",
                "name": "CoCo都可 新豐尚仁店",
                "city": "新竹縣",
                "coords": "24.86688, 120.99024",
                "source": "使用者查得重大線索：實體門市仍在營業（新豐鄉尚仁街2-3號門口，原第14波下架解除，全台總店數由 349 增至 350 店）"
            }
        ]
    }

    state['batches'].append(batch_33)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Update version.json
    version_data = {
        "batch_id": 33,
        "version": "33",
        "updated_at": "11/07 09:57",
        "store_count": len(stores),
        "description": "第 33 波更新 · 重新上架新竹新豐尚仁店（全台總店數恢復為 350 間）"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    print("Batch #33 applied successfully!")

if __name__ == '__main__':
    apply_batch33()
