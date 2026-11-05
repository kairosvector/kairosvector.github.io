import json

def update_verified(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    updates = {
        # 松山壹號 (coco-22)
        "coco-22": {
            "lat": 25.04944,
            "lng": 121.57891,
            "coordsText": "25.04944, 121.57891",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04944,121.57891"
        },
        # 三井南港店 (coco-36)
        "coco-36": {
            "lat": 25.05925,
            "lng": 121.61803,
            "coordsText": "25.05925, 121.61803",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.05925,121.61803"
        },
        # (捷運北車2)M3出口 (coco-51)
        "coco-51": {
            "lat": 25.04500,
            "lng": 121.51621,
            "coordsText": "25.04500, 121.51621",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04500,121.51621"
        },
        # 忠孝復興店 (coco-58)
        "coco-58": {
            "lat": 25.04142,
            "lng": 121.54508,
            "coordsText": "25.04142, 121.54508",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04142,121.54508"
        }
    }

    count = 0
    for s in stores:
        if s['id'] in updates:
            u = updates[s['id']]
            s.update(u)
            count += 1
            print(f"Updated {s['id']} {s['name']} -> {s['coordsText']}")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {filepath}, updated {count} stores.")

update_verified('app/src/data/coco_stores_staging.json')
