import json
import urllib.request

update_store = {
    "id": "coco-253",
    "lat": 24.82599,
    "lng": 121.00899,
    "coordsText": "24.82599, 121.00899",
    "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.82599,121.00899"
}

# 1. Update stores in prod & staging
for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    for s in stores:
        if s["id"] == update_store["id"]:
            s["lat"] = update_store["lat"]
            s["lng"] = update_store["lng"]
            s["coordsText"] = update_store["coordsText"]
            s["gmapUrl"] = update_store["gmapUrl"]
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")
            break

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

# 2. Fetch latest timestamp to update state
GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"
req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    all_rows = json.loads(resp.read().decode("utf-8"))

latest_ts = all_rows[-1][0] if all_rows else "2026-11-05T06:27:34.000Z"

state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["last_processed_timestamp"] = latest_ts
state["last_processed_local_time"] = "2026-11-05 14:31:00 (UTC+8)"
state["last_processed_row_index"] = len(all_rows) - 1
state["total_records_at_last_sync"] = len(all_rows)

batch_3 = {
    "batch_id": 3,
    "applied_at": "2026-11-05 14:31:30 (UTC+8)",
    "cutoff_timestamp": latest_ts,
    "target": "Product & Staging",
    "updated_stores_count": 1,
    "updated_stores": [
        {"id": "coco-253", "name": "CoCo都可 竹北光明店", "coords": "24.82599, 121.00899", "source": "表單提供點位"}
    ]
}

state["batches"].append(batch_3)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #3 (watermark: {latest_ts})")
