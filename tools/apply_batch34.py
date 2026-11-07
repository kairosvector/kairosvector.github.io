import json
import sys
import os

def apply_batch34():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'
    buffer_path = 'app/src/data/coco_verified_buffer.json'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    updates = {
        "coco-45": {
            "lat": 25.05739,
            "lng": 121.51761,
            "coordsText": "25.05739, 121.51761",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.05739,121.51761"
        },
        "coco-328": {
            "lat": 22.72646,
            "lng": 120.30658,
            "coordsText": "22.72646, 120.30658",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.72646,120.30658"
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
            modified_count += 1
            print(f"Updated {s['id']} {s['name']} -> {s['coordsText']}")

    print(f"Total stores updated: {modified_count}")

    # Write stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Update sync state
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_34 = {
        "batch_id": 34,
        "applied_at": "2026-11-07 10:09:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": "coco-45",
                "name": "CoCo都可 台北民生店",
                "coords": "25.05739, 121.51761",
                "source": "使用者實勘微調（民生西路159號，向東微調20.0m至大門口）"
            },
            {
                "id": "coco-328",
                "name": "CoCo都可 楠梓德賢店",
                "coords": "22.72646, 120.30658",
                "source": "使用者實勘微調（德賢路167號，微調10.3m至正門前方）"
            }
        ]
    }

    state['batches'].append(batch_34)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Clear buffer
    with open(buffer_path, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

    # Update version.json
    version_data = {
        "batch_id": 34,
        "version": "34",
        "updated_at": "11/07 10:09",
        "store_count": len(stores),
        "description": "第 34 波更新 · 精準微調台北民生店、高雄楠梓德賢店"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    print("Batch #34 applied successfully!")

if __name__ == '__main__':
    apply_batch34()
