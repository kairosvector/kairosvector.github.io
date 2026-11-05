import json

def update_stores(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # 1. Update 台北南機場
    updated_nanji = False
    for s in stores:
        if s.get('id') == 'coco-332' or s.get('shortName') == '台北南機場':
            s['lat'] = 25.02820
            s['lng'] = 121.50624
            s['coordsText'] = "25.02820, 121.50624"
            s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=25.02820,121.50624"
            updated_nanji = True
            print(f"Updated 台北南機場 coords in {file_path}")
            break

    # 2. Add 竹北中正2 / 台北中正2
    exists = any(s.get('id') == 'coco-333' for s in stores)
    if not exists:
        new_store = {
            "id": "coco-333",
            "city": "新竹縣",
            "name": "CoCo都可-竹北中正2店（台北中正2）",
            "shortName": "竹北中正2",
            "address": "新竹縣竹北市中正西路382號附近",
            "phone": "",
            "lat": 24.84311,
            "lng": 120.99509,
            "coordsText": "24.84311, 120.99509",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.84311,120.99509",
            "route": "新竹縣竹北市中正西路"
        }
        
        # Insert near Hsinchu County stores
        last_hsinchu_idx = -1
        for i, s in enumerate(stores):
            if s.get('city') == '新竹縣':
                last_hsinchu_idx = i

        if last_hsinchu_idx != -1:
            stores.insert(last_hsinchu_idx + 1, new_store)
            print(f"Inserted coco-333 into 新竹縣 in {file_path}")
        else:
            stores.append(new_store)
            print(f"Appended coco-333 in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"Finished {file_path}, total stores: {len(stores)}")

update_stores('app/src/data/coco_stores.json')
update_stores('app/src/data/coco_stores_staging.json')
