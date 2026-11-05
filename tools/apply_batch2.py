import json
import urllib.request
from datetime import datetime

# 5 stores to update
updates_5 = {
    "coco-293": {
        "name_check": "苗栗通霄",
        "lat": 24.48930,
        "lng": 120.67809,
        "coordsText": "24.48930, 120.67809",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.48930,120.67809"
    },
    "coco-296": {
        "name_check": "文心秀泰",
        "lat": 24.12969,
        "lng": 120.64577,
        "coordsText": "24.12969, 120.64577",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.12969,120.64577"
    },
    "coco-304": {
        "name_check": "太平樹孝",
        "lat": 24.15219,
        "lng": 120.71744,
        "coordsText": "24.15219, 120.71744",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.15219,120.71744"
    },
    "coco-73": {
        "name_check": "洲子洋",
        "lat": 25.08961,
        "lng": 121.44604,
        "coordsText": "25.08961, 121.44604",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.08961,121.44604"
    },
    "coco-317": {
        "name_check": "南投服務區",
        "lat": 23.90005,
        "lng": 120.71165,
        "coordsText": "23.90005, 120.71165",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=23.90005,120.71165"
    }
}

# Update both store files
for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    count = 0
    for s in stores:
        if s["id"] in updates_5:
            u = updates_5[s["id"]]
            s["lat"] = u["lat"]
            s["lng"] = u["lng"]
            s["coordsText"] = u["coordsText"]
            s["gmapUrl"] = u["gmapUrl"]
            count += 1
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"Finished {filepath}, total stores: {len(stores)}, updated {count} stores.\n")

# Fetch latest sheet row count & timestamp to update sync state
GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"
req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    all_rows = json.loads(resp.read().decode("utf-8"))

latest_ts = all_rows[-1][0] if all_rows else "2026-11-05T06:07:18.000Z"

# Update state file
state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

state["last_processed_timestamp"] = latest_ts
state["last_processed_local_time"] = "2026-11-05 14:07:18 (UTC+8)"
state["last_processed_row_index"] = len(all_rows) - 1
state["total_records_at_last_sync"] = len(all_rows)

batch_2 = {
    "batch_id": 2,
    "applied_at": "2026-11-05 14:14:00 (UTC+8)",
    "cutoff_timestamp": latest_ts,
    "target": "Product & Staging",
    "updated_stores_count": 5,
    "updated_stores": [
        {"id": "coco-293", "name": "CoCo都可 苗栗通霄店", "coords": "24.48930, 120.67809", "source": "表單提供點位"},
        {"id": "coco-296", "name": "CoCo都可 文心秀泰店", "coords": "24.12969, 120.64577", "source": "表單提供點位"},
        {"id": "coco-304", "name": "CoCo都可 太平樹孝店", "coords": "24.15219, 120.71744", "source": "表單提供點位"},
        {"id": "coco-73", "name": "CoCo都可 洲子洋店", "coords": "25.08961, 121.44604", "source": "表單提供點位"},
        {"id": "coco-317", "name": "CoCo都可 南投服務區店", "coords": "23.90005, 120.71165", "source": "表單提供點位"}
    ]
}

state["batches"].append(batch_2)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #2 (watermark: {latest_ts})")
