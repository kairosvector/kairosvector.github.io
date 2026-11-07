import json
import sys
import re

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    updates = {
        "coco-332": {
            "name": "CoCo都可 台北南機場店",
            "lat": 25.02825,
            "lng": 121.50629,
            "coordsText": "25.02825, 121.50629",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.02825,121.50629",
            "source": "網友回報經核實精準微調（台北市中正區中華路二段307巷18號，微調7米至店門口）"
        },
        "coco-186": {
            "name": "CoCo都可 龜山民生北店",
            "lat": 25.03526,
            "lng": 121.30232,
            "coordsText": "25.03526, 121.30232",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.03526,121.30232",
            "source": "現場玩家回報精準微調（桃園市龜山區民生北路一段168號，微調5米至店門口紅磚道）"
        },
        "coco-221": {
            "name": "CoCo都可 平鎮龍南店",
            "lat": 24.92189,
            "lng": 121.25120,
            "coordsText": "24.92189, 121.25120",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=24.92189,121.25120",
            "source": "現場玩家回報精準微調（桃園市平鎮區龍南路336號，微調4米修正騎樓遮蔽角）"
        }
    }

    # 1. Update coco_stores.json and coco_stores_staging.json
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        for s in stores:
            if s['id'] in updates:
                u = updates[s['id']]
                s['lat'] = u['lat']
                s['lng'] = u['lng']
                s['coordsText'] = u['coordsText']
                s['gmapUrl'] = u['gmapUrl']

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_31 = {
        "batch_id": 31,
        "applied_at": "2026-11-07 09:00:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 3,
        "updated_stores": [
            {
                "id": "coco-332",
                "name": "CoCo都可 台北南機場店",
                "coords": "25.02825, 121.50629",
                "source": updates["coco-332"]["source"]
            },
            {
                "id": "coco-186",
                "name": "CoCo都可 龜山民生北店",
                "coords": "25.03526, 121.30232",
                "source": updates["coco-186"]["source"]
            },
            {
                "id": "coco-221",
                "name": "CoCo都可 平鎮龍南店",
                "coords": "24.92189, 121.25120",
                "source": updates["coco-221"]["source"]
            }
        ]
    }
    state["batches"].append(batch_31)
    for sid in ["coco-332", "coco-186", "coco-221"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #31.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 31,
        "version": "31",
        "updated_at": "11/07 09:00",
        "store_count": 349,
        "description": "第 31 波更新 · 南機場店、龜山民生北店、平鎮龍南店 3 間門市座標精準微調",
        "ticker": "最新第 31 波：南機場店、龜山民生北店、平鎮龍南店 座標已校準！"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to Batch #31.")

    # 4. Update top ticker in coco-pikmin.astro and staging.astro
    for astro_file in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_file, 'r', encoding='utf-8') as f:
            c = f.read()

        # Update data-batch-id
        c = re.sub(r'data-batch-id="\d+"', 'data-batch-id="31"', c)

        # Update ticker text
        ticker_regex = r'<span class="ticker-badge">最新</span>[^<]*'
        new_ticker = '<span class="ticker-badge">最新</span>南機場店、龜山民生北店、平鎮龍南店 已校準！'
        c = re.sub(ticker_regex, new_ticker, c)

        with open(astro_file, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated ticker in {astro_file}")

    # 5. Add to coco_manager.py RESOLVED_STORES
    with open('tools/coco_manager.py', 'r', encoding='utf-8') as f:
        mgr = f.read()
    if '"coco-332"' not in mgr:
        mgr = mgr.replace('"coco-50",', '"coco-50",\n    "coco-332",   # 台北南機場 (批次#31已微調完成)\n    "coco-186",   # 龜山民生北 (批次#31已微調完成)\n    "coco-221",   # 平鎮龍南 (批次#31已微調完成),')
        with open('tools/coco_manager.py', 'w', encoding='utf-8') as f:
            f.write(mgr)
        print("Updated tools/coco_manager.py RESOLVED_STORES")

if __name__ == '__main__':
    main()
