import json
import urllib.request
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

updates_batch5 = {
    # 1. 合宜店
    "coco-85": {
        "lat": 24.99777,
        "lng": 121.44738,
        "coordsText": "24.99777, 121.44738",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.99777,121.44738"
    },
    # 2. 菓林店
    "coco-159": {
        "lat": 25.07462,
        "lng": 121.25931,
        "coordsText": "25.07462, 121.25931",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.07462,121.25931"
    },
    # 3. 台中東海店
    "coco-314": {
        "lat": 24.18201,
        "lng": 120.59263,
        "coordsText": "24.18201, 120.59263",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.18201,120.59263"
    },
    # 4. 頭份文化店
    "coco-281": {
        "lat": 24.69915,
        "lng": 120.89938,
        "coordsText": "24.69915, 120.89938",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.69915,120.89938"
    },
    # 5. 三芝店 (使用者直接指定)
    "coco-100": {
        "lat": 25.25880,
        "lng": 121.50222,
        "coordsText": "25.25880, 121.50222",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.25880,121.50222"
    }
}

# 1. Apply to both store files
for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    count = 0
    for s in stores:
        if s["id"] in updates_batch5:
            u = updates_batch5[s["id"]]
            s["lat"] = u["lat"]
            s["lng"] = u["lng"]
            s["coordsText"] = u["coordsText"]
            s["gmapUrl"] = u["gmapUrl"]
            count += 1
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

# 2. Update state file
state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

# Record confirmed correct stores (no longer tracked)
if "confirmed_correct_stores" not in state:
    state["confirmed_correct_stores"] = []
if "coco-1" not in state["confirmed_correct_stores"]:
    state["confirmed_correct_stores"].append("coco-1")

batch_5 = {
    "batch_id": 5,
    "applied_at": "2026-11-05 15:03:00 (UTC+8)",
    "target": "Product & Staging",
    "updated_stores_count": 5,
    "updated_stores": [
        {"id": "coco-85", "name": "CoCo都可 合宜店", "coords": "24.99777, 121.44738", "source": "表單提供點位"},
        {"id": "coco-159", "name": "菓林店", "coords": "25.07462, 121.25931", "source": "表單提供點位"},
        {"id": "coco-314", "name": "CoCo都可 台中東海店", "coords": "24.18201, 120.59263", "source": "表單提供點位"},
        {"id": "coco-281", "name": "CoCo都可 頭份文化店", "coords": "24.69915, 120.89938", "source": "表單提供點位"},
        {"id": "coco-100", "name": "CoCo都可 三芝店", "coords": "25.25880, 121.50222", "source": "使用者驗證"}
    ]
}

state["batches"].append(batch_5)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #5 and marked coco-1 as confirmed correct.")
