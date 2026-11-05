import json
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

new_stores = [
    {
        "id": "coco-334",
        "city": "台南市",
        "name": "CoCo都可 安平郡平店",
        "shortName": "台南安平郡平",
        "address": "台南市安平區郡平路160號",
        "phone": "",
        "lat": 22.98922,
        "lng": 120.16823,
        "coordsText": "22.98922, 120.16823",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.98922,120.16823",
        "route": "台南市區"
    },
    {
        "id": "coco-335",
        "city": "台南市",
        "name": "CoCo都可 永康大灣店",
        "shortName": "台南永康大灣",
        "address": "台南市永康區大灣路976號",
        "phone": "",
        "lat": 22.99937,
        "lng": 120.25413,
        "coordsText": "22.99937, 120.25413",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.99937,120.25413",
        "route": "台南市區"
    }
]

for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    # Check if already added
    existing_ids = {s["id"] for s in stores}
    to_add = [ns for ns in new_stores if ns["id"] not in existing_ids]

    if to_add:
        # Insert after last Tainan store
        last_tainan_idx = -1
        for i, s in enumerate(stores):
            if s.get("city") == "台南市":
                last_tainan_idx = i

        if last_tainan_idx != -1:
            for offset, ns in enumerate(to_add):
                stores.insert(last_tainan_idx + 1 + offset, ns)
        else:
            stores.extend(to_add)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    print(f"[{filepath}] Total stores now: {len(stores)}")

# Update state
state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

batch_9 = {
    "batch_id": 9,
    "applied_at": "2026-11-05 15:25:00 (UTC+8)",
    "target": "Product & Staging",
    "updated_stores_count": 2,
    "updated_stores": [
        {"id": "coco-334", "name": "CoCo都可 安平郡平店", "coords": "22.98922, 120.16823", "source": "使用者驗證新增"},
        {"id": "coco-335", "name": "CoCo都可 永康大灣店", "coords": "22.99937, 120.25413", "source": "使用者驗證新增"}
    ]
}

state["batches"].append(batch_9)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with Batch #9.")
