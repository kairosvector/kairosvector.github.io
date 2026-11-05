import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)

        for s in stores:
            if s['id'] == 'coco-34':
                s['lat'] = 25.11618
                s['lng'] = 121.51621
                s['coordsText'] = "25.11618, 121.51621"
                s['gmapUrl'] = "https://www.google.com/maps/search/?api=1&query=25.11618,121.51621"
            elif s['id'] == 'coco-101':
                s['name'] = "CoCo都可 中和永華店"
                s['shortName'] = "新北中和永華"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)
        print(f"Updated {filepath}: total {len(stores)} stores.")

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batch_24 = {
        "batch_id": 24,
        "applied_at": "2026-11-06 07:10:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 2,
        "updated_stores": [
            {
                "id": "coco-34",
                "name": "CoCo都可(石牌商城店)",
                "coords": "25.11618, 121.51621",
                "source": "使用者驗證微調精確座標（25.1161823, 121.5162096）"
            },
            {
                "id": "coco-101",
                "name": "CoCo都可 中和永華店",
                "coords": "24.9971, 121.50421",
                "source": "使用者驗證門市更名（原南華店更名為中和永華店，座標維持不動）"
            }
        ]
    }
    state["batches"].append(batch_24)
    for sid in ["coco-34", "coco-101"]:
        if sid not in state.setdefault("all_updated_ids", []):
            state["all_updated_ids"].append(sid)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #24.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 24,
        "version": "24",
        "updated_at": "11/06 07:10",
        "store_count": 346,
        "description": "第 24 波更新 · 石牌商城店座標微調、南華店更名為中和永華店"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 24, 346 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="23"', 'data-batch-id="24"')
        content = content.replace('11/06 07:05', '11/06 07:10')
        content = content.replace("u.searchParams.set('v', '23');", "u.searchParams.set('v', '24');")
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 24.")

if __name__ == '__main__':
    main()
