import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    new_stores = [
        {
            "id": "coco-336",
            "city": "高雄市",
            "name": "CoCo都可 岡山樂購廣場店",
            "shortName": "岡山樂購廣場",
            "address": "高雄市岡山區捷安路1巷2號3樓",
            "phone": "07 625 7808",
            "lat": 22.77993,
            "lng": 120.30010,
            "coordsText": "22.77993, 120.30010",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.77993,120.30010",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
        },
        {
            "id": "coco-337",
            "city": "高雄市",
            "name": "CoCo都可 SKM Park店",
            "shortName": "高雄SKM Park",
            "address": "高雄市前鎮區中安路1之1號3樓",
            "phone": "07 791 5808",
            "lat": 22.58334,
            "lng": 120.33010,
            "coordsText": "22.58334, 120.33010",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.58334,120.33010",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
        },
        {
            "id": "coco-338",
            "city": "高雄市",
            "name": "CoCo都可 鳳山青年店",
            "shortName": "高雄鳳山青年",
            "address": "高雄市鳳山區青年路二段296號",
            "phone": "07 777 6288",
            "lat": 22.63975,
            "lng": 120.35117,
            "coordsText": "22.63975, 120.35117",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.63975,120.35117",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
        },
        {
            "id": "coco-339",
            "city": "高雄市",
            "name": "CoCo都可 左營新光店",
            "shortName": "高雄左營新光",
            "address": "高雄市左營區高鐵路123號B2",
            "phone": "07 345 6608",
            "lat": 22.68780,
            "lng": 120.30921,
            "coordsText": "22.68780, 120.30921",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.68780,120.30921",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
        }
    ]

    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)
        
        # Check if already present
        existing_ids = {s['id'] for s in stores}
        added = 0
        for ns in new_stores:
            if ns['id'] not in existing_ids:
                stores.append(ns)
                added += 1
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: added {added} stores, total {len(stores)}")

    # Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_13 = {
        "batch_id": 13,
        "applied_at": "2026-11-05 17:25:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 4,
        "updated_stores": [
            {
                "id": ns["id"],
                "name": ns["name"],
                "coords": ns["coordsText"],
                "source": "使用者回報新增門市（高雄實體店核實補全）"
            }
            for ns in new_stores
        ]
    }
    state["batches"].append(batch_13)
    if "all_updated_ids" in state:
        for ns in new_stores:
            if ns["id"] not in state["all_updated_ids"]:
                state["all_updated_ids"].append(ns["id"])

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"Updated sync state with Batch #13!")

if __name__ == '__main__':
    main()
