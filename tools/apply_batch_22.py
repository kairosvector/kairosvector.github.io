import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    store_shuinan = {
        "id": "coco-346",
        "city": "台中市",
        "name": "CoCo都可 西屯水湳店",
        "shortName": "台中西屯水湳",
        "address": "台中市西屯區大鵬路25號",
        "phone": "04 2291 0178",
        "lat": 24.17809,
        "lng": 120.66778,
        "coordsText": "24.17809, 120.66778",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.17809,120.66778",
        "route": "苗栗南＋台中→高雄中南線（＋金門另飛）"
    }

    store_yuanqu2 = {
        "id": "coco-347",
        "city": "新竹市",
        "name": "CoCo都可 園區2店",
        "shortName": "新竹園區2",
        "address": "新竹市東區光復路一段125號1樓",
        "phone": "03 668 6523",
        "lat": 24.78133,
        "lng": 121.02319,
        "coordsText": "24.78133, 121.02319",
        "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.78133,121.02319",
        "route": "新竹市東區＋新竹縣＋苗栗北／中"
    }

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        # Update coco-305 台中遠雄 coords
        for s in stores:
            if s['id'] == 'coco-305':
                s['lat'] = 24.13600
                s['lng'] = 120.68766
                s['coordsText'] = "24.13600, 120.68766"
                s['address'] = "台中市東區復興路四段186號B1 (iFG遠雄廣場/新時代B1)"
                s['phone'] = "04 2225 0225"
                s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=24.13600,120.68766"

        # Remove duplicate coco-346 (old 台中遠雄店)
        stores = [s for s in stores if not (s['id'] == 'coco-346' and '遠雄' in s['name'])]

        # Add store_shuinan (id coco-346) if not present
        if not any(s['id'] == store_shuinan['id'] for s in stores):
            stores.append(store_shuinan)

        # Add store_yuanqu2 (id coco-347) if not present
        if not any(s['id'] == store_yuanqu2['id'] for s in stores):
            stores.append(store_yuanqu2)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: new total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_22 = {
        "batch_id": 22,
        "applied_at": "2026-11-06 06:50:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 3,
        "updated_stores": [
            {
                "id": "coco-305",
                "name": "CoCo都可 台中遠雄",
                "coords": "24.13600, 120.68766",
                "source": "使用者驗證去重並校正（移除重複之coco-346，保留coco-305精準點位）"
            },
            {
                "id": store_shuinan["id"],
                "name": store_shuinan["name"],
                "coords": store_shuinan["coordsText"],
                "source": "使用者驗證新增門市（西屯水湳店實體店核實補全）"
            },
            {
                "id": store_yuanqu2["id"],
                "name": store_yuanqu2["name"],
                "coords": store_yuanqu2["coordsText"],
                "source": "使用者驗證新增門市（新竹園區2店實體店核實補全）"
            }
        ]
    }
    state["batches"].append(batch_22)
    for sid in ["coco-305", store_shuinan["id"], store_yuanqu2["id"]]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #22.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 22,
        "version": "22",
        "updated_at": "11/06 06:50",
        "store_count": 345,
        "description": "第 22 波更新 · 台中遠雄去重校正、新增西屯水湳店、新竹園區2店"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 22, 345 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="21"', 'data-batch-id="22"')
        content = content.replace('11/05 23:50', '11/06 06:50')
        content = content.replace("u.searchParams.set('v', '21');", "u.searchParams.set('v', '22');")
        content = content.replace("344 店最新", "345 店最新")
        content = content.replace("344 店已校對", "345 店已校對")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 22.")

if __name__ == '__main__':
    main()
