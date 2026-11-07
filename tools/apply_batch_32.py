import json
import sys
import re

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    updates = {
        "coco-1": {
            "name": "CoCo都可（百福門市）",
            "lat": 25.08176,
            "lng": 121.69608,
            "coordsText": "25.08176, 121.69608",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.08176,121.69608",
            "source": "使用者指定微調精準點位（基隆市七堵區百三街60號，微調5.4米至店門口）"
        },
        "coco-9": {
            "name": "CoCo都可 基隆長庚店",
            "lat": 25.12044,
            "lng": 121.72307,
            "coordsText": "25.12044, 121.72307",
            "gmapUrl": "https://www.google.com/maps/search/?api=1&query=25.12044,121.72307",
            "source": "現場玩家回報精準微調（基隆市安樂區安樂路二段229號，微調4.1米至醫院商圈店門）"
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

    batch_32 = {
        "batch_id": 32,
        "applied_at": "2026-11-07 09:05:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": "coco-1",
                "name": "CoCo都可（百福門市）",
                "coords": "25.08176, 121.69608",
                "source": updates["coco-1"]["source"]
            },
            {
                "id": "coco-9",
                "name": "CoCo都可 基隆長庚店",
                "coords": "25.12044, 121.72307",
                "source": updates["coco-9"]["source"]
            }
        ]
    }
    state["batches"].append(batch_32)
    for sid in ["coco-1", "coco-9"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #32.")

    # 3. Clear buffer
    buffer_path = 'app/src/data/coco_verified_buffer.json'
    with open(buffer_path, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("Cleared coco_verified_buffer.json.")

    # 4. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 32,
        "version": "32",
        "updated_at": "11/07 09:05",
        "store_count": 349,
        "description": "第 32 波更新 · 基隆百福門市、基隆長庚店 2 間門市座標精準微調",
        "ticker": "最新第 32 波：基隆百福門市、基隆長庚店 座標已校準！"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to Batch #32.")

    # 5. Update top ticker in coco-pikmin.astro and staging.astro
    for astro_file in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_file, 'r', encoding='utf-8') as f:
            c = f.read()

        c = re.sub(r'data-batch-id="\d+"', 'data-batch-id="32"', c)

        ticker_regex = r'<span class="ticker-badge">最新</span>[^<]*'
        new_ticker = '<span class="ticker-badge">最新</span>基隆百福門市、基隆長庚店 已校準！'
        c = re.sub(ticker_regex, new_ticker, c)

        with open(astro_file, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated ticker in {astro_file}")

    # 6. Add to coco_manager.py RESOLVED_STORES
    with open('tools/coco_manager.py', 'r', encoding='utf-8') as f:
        mgr = f.read()
    if '"coco-1"' not in mgr:
        mgr = mgr.replace('"coco-221",', '"coco-221",\n    "coco-1",     # 基隆百福 (批次#32已微調完成)\n    "coco-9",     # 基隆長庚 (批次#32已微調完成),')
        with open('tools/coco_manager.py', 'w', encoding='utf-8') as f:
            f.write(mgr)
        print("Updated tools/coco_manager.py RESOLVED_STORES")

if __name__ == '__main__':
    main()
