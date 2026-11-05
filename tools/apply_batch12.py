import json
import urllib.request
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

updates_batch12 = {
    "coco-232": {
        "lat": 24.96488,
        "lng": 121.15103,
        "coordsText": "24.96488, 121.15103",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.96488,121.15103"
    },
    "coco-271": {
        "lat": 24.76736,
        "lng": 121.05588,
        "coordsText": "24.76736, 121.05588",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.76736,121.05588"
    }
}

# 1. Update store files
for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    for s in stores:
        if s["id"] in updates_batch12:
            u = updates_batch12[s["id"]]
            s["lat"] = u["lat"]
            s["lng"] = u["lng"]
            s["coordsText"] = u["coordsText"]
            s["gmapUrl"] = u["gmapUrl"]
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

# 2. Update state file
state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

batch_12 = {
    "batch_id": 12,
    "applied_at": "2026-11-05 16:29:00 (UTC+8)",
    "target": "Product & Staging",
    "updated_stores_count": 2,
    "updated_stores": [
        {"id": "coco-232", "name": "富源店", "coords": "24.96488, 121.15103", "source": "表單提供點位（重大偏差校正）"},
        {"id": "coco-271", "name": "CoCo都可(竹東二重)", "coords": "24.76736, 121.05588", "source": "表單提供點位"}
    ]
}

state["batches"].append(batch_12)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #12.")
