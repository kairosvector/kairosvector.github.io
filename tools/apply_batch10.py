import json
import urllib.request
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

update_item = {
    "id": "coco-291",
    "lat": 24.41105,
    "lng": 120.76841,
    "coordsText": "24.41105, 120.76841",
    "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.41105,120.76841"
}

# 1. Update store files
for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    for s in stores:
        if s["id"] == update_item["id"]:
            s["lat"] = update_item["lat"]
            s["lng"] = update_item["lng"]
            s["coordsText"] = update_item["coordsText"]
            s["gmapUrl"] = update_item["gmapUrl"]
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")
            break

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

# 2. Update state file
state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

batch_10 = {
    "batch_id": 10,
    "applied_at": "2026-11-05 15:41:30 (UTC+8)",
    "target": "Product & Staging",
    "updated_stores_count": 1,
    "updated_stores": [
        {"id": "coco-291", "name": "CoCo都可(苗栗三義店)", "coords": "24.41105, 120.76841", "source": "表單提供點位"}
    ]
}

state["batches"].append(batch_10)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #10.")
