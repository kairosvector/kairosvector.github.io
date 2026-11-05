import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

update_item = {
    "id": "coco-185",
    "lat": 25.04039,
    "lng": 121.38804,
    "coordsText": "25.04039, 121.38804",
    "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04039,121.38804"
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

batch_8 = {
    "batch_id": 8,
    "applied_at": "2026-11-05 15:10:30 (UTC+8)",
    "target": "Product & Staging",
    "updated_stores_count": 1,
    "updated_stores": [
        {"id": "coco-185", "name": "林口文青店", "coords": "25.04039, 121.38804", "source": "使用者驗證"}
    ]
}

state["batches"].append(batch_8)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #8.")
