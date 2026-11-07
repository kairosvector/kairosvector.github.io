import json
import sys
import os

def apply_batch35():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'
    version_path = 'app/public/events/coco-version.json'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    # 1. Update coco-151 (八德廣福店)
    found_151 = False
    for s in stores:
        if s['id'] == 'coco-151':
            s['lat'] = 24.95942
            s['lng'] = 121.29649
            s['coordsText'] = "24.95942, 121.29649"
            s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=24.95942,121.29649"
            s['isUpdated'] = True
            s['updateStatus'] = "已更新 (第 35 波 點位微調)"
            s['updateDetail'] = "玩家回報經緯度顛倒還原核實微調 4.6m 至店門口"
            s['updateBatch'] = 35
            found_151 = True
            print("Updated coco-151 (八德廣福店)")
            break

    # 2. Add coco-352 (高雄 苓雅忠孝店)
    if not any(s['id'] == 'coco-352' for s in stores):
        new_store = {
            "id": "coco-352",
            "city": "高雄市",
            "name": "CoCo都可 苓雅忠孝店",
            "shortName": "高雄苓雅忠孝",
            "address": "高雄市苓雅區苓雅一路293號",
            "phone": "07 333 0618",
            "lat": 22.62000,
            "lng": 120.30774,
            "coordsText": "22.62000, 120.30774",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=22.62000,120.30774",
            "route": "苗栗南＋台中→高雄中南線（＋金門另飛）",
            "isUpdated": True,
            "updateStatus": "已更新 (第 35 波 新增門市)",
            "updateDetail": "使用者與朋友實勘提報新增（高雄市苓雅區苓雅一路293號，全台總店數增至 351 店）",
            "updateBatch": 35
        }
        stores.append(new_store)
        print(f"Added coco-352 (高雄 苓雅忠孝店), total stores: {len(stores)}")

    # Save stores and staging
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # 3. Update coco_sync_state.json
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_35 = {
        "batch_id": 35,
        "applied_at": "2026-11-07 15:48:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": "coco-352",
                "name": "CoCo都可 苓雅忠孝店",
                "city": "高雄市",
                "action": "新增門市",
                "coords": "22.62000, 120.30774",
                "source": "使用者與朋友實勘提報新增（高雄市苓雅區苓雅一路293號，高雄市增至 11 間，全台總店數增至 351 店）"
            },
            {
                "id": "coco-151",
                "name": "CoCo都可 八德廣福店",
                "city": "桃園市",
                "action": "點位微調",
                "coords": "24.95942, 121.29649",
                "source": "玩家回報經緯度顛倒還原核實微調 4.6m 至店門口（桃園市八德區廣福路126號）"
            }
        ]
    }

    state['batches'].append(batch_35)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # 4. Update coco-version.json
    version_data = {
        "batch_id": 35,
        "version": "35",
        "updated_at": "11/07 15:48",
        "store_count": len(stores),
        "description": "第 35 波更新 · 新增高雄苓雅忠孝店（全台總店數增至 351 間）、微調八德廣福店"
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, ensure_ascii=False, indent=2)

    print("Batch #35 applied successfully!")

if __name__ == '__main__':
    apply_batch35()
