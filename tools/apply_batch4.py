import json
import urllib.request

updates_batch4 = {
    "coco-157": {
        "lat": 25.00492,
        "lng": 121.22852,
        "coordsText": "25.00492, 121.22852",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.00492,121.22852"
    },
    "coco-311": {
        "lat": 24.17015,
        "lng": 120.64485,
        "coordsText": "24.17015, 120.64485",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.17015,120.64485"
    }
}

for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    for s in stores:
        if s["id"] in updates_batch4:
            u = updates_batch4[s["id"]]
            s["lat"] = u["lat"]
            s["lng"] = u["lng"]
            s["coordsText"] = u["coordsText"]
            s["gmapUrl"] = u["gmapUrl"]
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

# Update state
GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"
req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    all_rows = json.loads(resp.read().decode("utf-8"))

latest_ts = all_rows[-1][0] if all_rows else "2026-11-05T06:42:13.000Z"

state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["last_processed_timestamp"] = latest_ts
state["last_processed_local_time"] = "2026-11-05 14:45:00 (UTC+8)"
state["last_processed_row_index"] = len(all_rows) - 1
state["total_records_at_last_sync"] = len(all_rows)

batch_4 = {
    "batch_id": 4,
    "applied_at": "2026-11-05 14:52:00 (UTC+8)",
    "cutoff_timestamp": latest_ts,
    "target": "Product & Staging",
    "updated_stores_count": 2,
    "updated_stores": [
        {"id": "coco-157", "name": "中壢大江店", "coords": "25.00492, 121.22852", "source": "表單提供點位"},
        {"id": "coco-311", "name": "CoCo都可 青海萬家福", "coords": "24.17015, 120.64485", "source": "表單提供點位"}
    ]
}

state["batches"].append(batch_4)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #4 (watermark: {latest_ts})")
