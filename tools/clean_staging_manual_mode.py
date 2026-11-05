import json

def clean():
    # 1. Reset coco-version.json to batch 13
    ver_path = 'app/public/events/coco-version.json'
    ver_data = {
        "batch_id": 13,
        "version": "13",
        "updated_at": "11/05 17:25",
        "store_count": 338,
        "description": "第 13 波更新 · 高雄 4 間門市補全校正"
    }
    with open(ver_path, 'w', encoding='utf-8') as f:
        json.dump(ver_data, f, ensure_ascii=False, indent=2)
    print("Reset app/public/events/coco-version.json to batch 13")

    # 2. Sync staging.astro script with production coco-pikmin.astro script
    with open('app/src/pages/events/coco-pikmin.astro', 'r', encoding='utf-8') as f:
        prod = f.read()
    with open('app/src/pages/events/coco-pikmin/staging.astro', 'r', encoding='utf-8') as f:
        stag = f.read()

    # Extract the checkRemoteVersion block from prod
    js_marker_start = '// Force refresh button logic & Remote Version Auto-Check'
    js_marker_end = 'const PLAY_STORE_URL ='

    prod_js = prod[prod.find(js_marker_start):prod.find(js_marker_end)]
    
    stag_start = stag.find(js_marker_start)
    stag_end = stag.find(js_marker_end)

    if stag_start != -1 and stag_end != -1:
        stag = stag[:stag_start] + prod_js + stag[stag_end:]
        print("Synced checkRemoteVersion JS in staging.astro")

    stag = stag.replace('data-batch-id="14"', 'data-batch-id="13"')
    stag = stag.replace('11/05 18:28', '11/05 17:25')

    with open('app/src/pages/events/coco-pikmin/staging.astro', 'w', encoding='utf-8') as f:
        f.write(stag)
    print("staging.astro successfully updated to match manual mode!")

if __name__ == '__main__':
    clean()
