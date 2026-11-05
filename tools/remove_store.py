import json

TARGET_ID = "coco-114"

# 1. Remove from store datasets
for filepath in ["app/src/data/coco_stores.json", "app/src/data/coco_stores_staging.json"]:
    with open(filepath, "r", encoding="utf-8") as f:
        stores = json.load(f)

    orig_len = len(stores)
    stores = [s for s in stores if s["id"] != TARGET_ID]
    new_len = len(stores)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    print(f"[{filepath}] Removed {TARGET_ID}. Count changed from {orig_len} to {new_len}")

# 2. Update state file to track removal
state_path = "app/src/data/coco_sync_state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

if "removed_stores" not in state:
    state["removed_stores"] = []
if TARGET_ID not in state["removed_stores"]:
    state["removed_stores"].append({
        "id": TARGET_ID,
        "name": "CoCo都可 土城廣福店",
        "reason": "已歇業/撤店，由使用者指示移除點位",
        "removed_at": "2026-11-05 15:05:30 (UTC+8)"
    })

if "confirmed_correct_stores" not in state:
    state["confirmed_correct_stores"] = []
if TARGET_ID not in state["confirmed_correct_stores"]:
    state["confirmed_correct_stores"].append(TARGET_ID)

with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"Updated {state_path} with removal of {TARGET_ID}.")
