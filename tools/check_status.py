import json

with open("app/src/data/coco_stores.json", "r", encoding="utf-8") as f:
    prod = json.load(f)

with open("app/src/data/coco_stores_staging.json", "r", encoding="utf-8") as f:
    staging = json.load(f)

print(f"Prod count: {len(prod)}")
print(f"Staging count: {len(staging)}")

for name, dataset in [("Prod", prod), ("Staging", staging)]:
    c332 = [s for s in dataset if s.get("id") == "coco-332"]
    c333 = [s for s in dataset if s.get("id") == "coco-333"]
    print(f"--- {name} ---")
    print("coco-332:", c332[0] if c332 else "Not found")
    print("coco-333:", c333[0] if c333 else "Not found")
