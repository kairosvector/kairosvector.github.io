import json

updates_all = {
    # 4 stores verified by user
    "coco-22": {
        "lat": 25.04944,
        "lng": 121.57891,
        "coordsText": "25.04944, 121.57891",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04944,121.57891"
    },
    "coco-36": {
        "lat": 25.05925,
        "lng": 121.61803,
        "coordsText": "25.05925, 121.61803",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.05925,121.61803"
    },
    "coco-51": {
        "lat": 25.04500,
        "lng": 121.51621,
        "coordsText": "25.04500, 121.51621",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04500,121.51621"
    },
    "coco-58": {
        "lat": 25.04142,
        "lng": 121.54508,
        "coordsText": "25.04142, 121.54508",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04142,121.54508"
    },
    # 4 stores from Category A
    "coco-52": {
        "lat": 25.04811,
        "lng": 121.51839,
        "coordsText": "25.04811, 121.51839",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.04811,121.51839"
    },
    "coco-329": {
        "lat": 22.61292,
        "lng": 120.30435,
        "coordsText": "22.61292, 120.30435",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.61292,120.30435"
    },
    "coco-326": {
        "lat": 22.59486,
        "lng": 120.30697,
        "coordsText": "22.59486, 120.30697",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.59486,120.30697"
    },
    "coco-319": {
        "lat": 23.78876,
        "lng": 120.47742,
        "coordsText": "23.78876, 120.47742",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=23.78876,120.47742"
    }
}

for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
    with open(filepath, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    count = 0
    for s in stores:
        if s['id'] in updates_all:
            s.update(updates_all[s['id']])
            count += 1
            print(f"[{filepath}] Updated {s['id']} {s['name']} -> {s['coordsText']}")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"Finished {filepath}, total stores: {len(stores)}, updated {count} stores.\n")
