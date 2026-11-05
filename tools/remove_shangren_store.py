import json
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    target_id = "coco-266"

    # 1. Update coco_stores.json and staging
    for filepath in ['app/src/data/coco_stores.json', 'app/src/data/coco_stores_staging.json']:
        with open(filepath, 'r', encoding='utf-8') as f:
            stores = json.load(f)
        
        orig_len = len(stores)
        stores = [s for s in stores if s['id'] != target_id]
        new_len = len(stores)
        print(f"Updated {filepath}: removed {orig_len - new_len} store, new total {new_len}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)

    # 2. Update coco_sync_state.json
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    state.setdefault('removed_stores', []).append({
        "id": target_id,
        "name": "CoCo都可(新豐尚仁店)",
        "reason": "已歇業/撤店，由使用者指示移除點位",
        "removed_at": "2026-11-05 20:10:00 (UTC+8)"
    })

    batch_14 = {
        "batch_id": 14,
        "applied_at": "2026-11-05 20:10:00 (UTC+8)",
        "target": "Product & Staging",
        "updated_stores_count": 1,
        "updated_stores": [
            {
                "id": target_id,
                "name": "CoCo都可(新豐尚仁店)",
                "action": "移除點位",
                "reason": "已歇業/撤店，由使用者指示移除點位"
            }
        ]
    }
    state["batches"].append(batch_14)

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Updated sync state with Batch #14.")

    # 3. Update coco-version.json
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 14,
        "version": "14",
        "updated_at": "11/05 20:10",
        "store_count": 337,
        "description": "第 14 波更新 · 移除已歇業門市（新豐尚仁店）"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Updated coco-version.json to batch 14, 337 stores.")

    # 4. Update Astro pages
    for astro_path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
        with open(astro_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('data-batch-id="13"', 'data-batch-id="14"')
        content = content.replace('11/05 17:25', '11/05 20:10')
        content = content.replace('u.searchParams.set(\'v\', \'13\');', 'u.searchParams.set(\'v\', \'14\');')
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {astro_path} to batch 14 and timestamp 11/05 20:10.")

if __name__ == '__main__':
    main()
