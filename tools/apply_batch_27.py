import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    store_guangfu = {
        "id": "coco-351",
        "city": "新北市",
        "name": "CoCo都可 土城廣福店",
        "shortName": "新北土城廣福",
        "address": "新北市土城區學府路一段146號",
        "phone": "02 2270 4575",
        "lat": 24.98723,
        "lng": 121.45489,
        "coordsText": "24.98723, 121.45489",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.98723,121.45489",
        "route": "新北其餘"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        # Update coco-322 coords
        for s in stores:
            if s['id'] == 'coco-322':
                s['lat'] = 22.99059
                s['lng'] = 120.23268
                s['coordsText'] = "22.99059, 120.23268"
                s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=22.99059,120.23268"

        # Add store_guangfu if not present
        if not any(s['id'] == store_guangfu['id'] for s in stores):
            stores.append(store_guangfu)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_27 = {
        "batch_id": 27,
        "applied_at": "2026-11-06 09:35:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": store_guangfu["id"],
                "name": store_guangfu["name"],
                "coords": store_guangfu["coordsText"],
                "source": "使用者驗證新增門市（土城廣福店實體店核實補全，學府路一段146號）"
            },
            {
                "id": "coco-322",
                "name": "CoCo都可 南紡購物中心店",
                "coords": "22.99059, 120.23268",
                "source": "使用者驗證精確微調（南紡購物中心B1美食街，22.9905907, 120.2326752）"
            }
        ]
    }
    state["batches"].append(batch_27)
    for sid in [store_guangfu["id"], "coco-322"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #27.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 27,
        "version": "27",
        "updated_at": "11/06 09:35",
        "store_count": 349,
        "description": "第 27 波更新 · 新增土城廣福店、南紡購物中心店座標微調"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 27, 349 stores.")

    # 4. Clear buffer
    with open('app/src/data/coco_verified_buffer.json', 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("Cleared coco_verified_buffer.json.")

    # 5. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="26"', 'data-batch-id="27"')
        content = content.replace('11/06 07:20', '11/06 09:35')
        content = content.replace("u.searchParams.set('v', '26');", "u.searchParams.set('v', '27');")
        content = content.replace("348 店最新", "349 店最新")
        content = content.replace("348 店已校對", "349 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 27.")

if __name__ == '__main__':
    main()
