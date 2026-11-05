import urllib.request
import json
import math
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"
STATE_FILE = "app/src/data/coco_sync_state.json"
PROD_FILE = "app/src/data/coco_stores.json"
STAGING_FILE = "app/src/data/coco_stores_staging.json"

def load_data():
    req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        sheet_rows = json.loads(resp.read().decode("utf-8"))

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)

    with open(PROD_FILE, "r", encoding="utf-8") as f:
        stores = json.load(f)

    return sheet_rows, state, stores

def match_store(reported_name, city, stores):
    for s in stores:
        if s["name"] == reported_name:
            return s
    for s in stores:
        if s["shortName"] in reported_name or reported_name in s["name"]:
            return s
    for s in stores:
        if s["city"] == city and any(part in s["name"] for part in reported_name.replace("CoCo都可", "").split()):
            return s
    return None

def analyze():
    sheet_rows, state, stores = load_data()
    last_idx = state.get("last_processed_row_index", -1)

    # All stores updated across all batches
    all_updated_ids = set()
    for b in state.get("batches", []):
        for s in b.get("updated_stores", []):
            all_updated_ids.add(s["id"])
    all_updated_ids.update({"coco-332", "coco-333"})

    # 1. Track stores reported wrong but WITHOUT coords
    stores_without_coords = {}
    stores_with_new_coords_all = {}

    for idx, r in enumerate(sheet_rows):
        ts, name, city, orig_coords, rtype, new_coords, note = r
        if "測試" in name:
            continue
        store = match_store(name, city, stores)
        sid = store["id"] if store else name

        if new_coords.strip() and rtype != "單純回報有誤":
            stores_with_new_coords_all[sid] = (idx, r, store)
            if sid in stores_without_coords:
                del stores_without_coords[sid]
        else:
            if sid not in stores_with_new_coords_all:
                stores_without_coords[sid] = (idx, r, store)

    pending_no_coords = {k: v for k, v in stores_without_coords.items() if k not in all_updated_ids}

    # 2. Track ALL un-updated reports with new coords across the entire sheet
    new_unprocessed_dict = {}
    for idx, r in enumerate(sheet_rows):
        ts, name, city, orig_coords, rtype, new_coords, note = r
        if "測試" in name:
            continue
        store = match_store(name, city, stores)
        sid = store["id"] if store else None

        if not sid or sid in all_updated_ids:
            continue

        if new_coords.strip() and rtype != "單純回報有誤":
            try:
                parts = [float(x.strip()) for x in new_coords.split(",") if x.strip()]
                lat, lng = parts[0], parts[1]
                diff = haversine(store["lat"], store["lng"], lat, lng) if store else 0
                
                # If store already has these exact coordinates (within 10m), it's already updated
                if diff < 10:
                    continue

                # Geographic plausibility check
                if diff <= 2000:
                    geo_status = f"合理（偏移 {diff:.0f} 公尺）"
                elif diff <= 5000:
                    geo_status = f"需注意（偏移 {diff/1000:.1f} 公里）"
                else:
                    geo_status = f"可疑/跨區（偏移 {diff/1000:.1f} 公里）"
            except Exception:
                lat, lng, diff = None, None, 0
                geo_status = "座標格式解析失敗"

            new_unprocessed_dict[sid] = {
                "row_index": idx,
                "timestamp": ts,
                "name": name,
                "city": city,
                "store": store,
                "new_lat": lat,
                "new_lng": lng,
                "diff_meters": diff,
                "geo_status": geo_status,
                "note": note
            }


    return state, pending_no_coords, list(new_unprocessed_dict.values()), len(sheet_rows)

if __name__ == "__main__":
    state, pending_no_coords, new_unprocessed, total_sheet_rows = analyze()
    print("=" * 65)
    print(f"【CoCo 點位回報追蹤總表】(目前最新總回報數：{total_sheet_rows} 筆)")
    print(f"上次水線切齊時間：{state['last_processed_local_time']}")
    print("=" * 65)

    print(f"\n1. 錯誤但尚未提供 GPS 座標的待補清單（共 {len(pending_no_coords)} 間）：")
    for sid, (idx, r, store) in pending_no_coords.items():
        addr = store["address"] if store else "無地址"
        sname = store["name"] if store else r[1]
        print(f"   - [{sid}] {sname} ({r[2]}) | 地址: {addr} | 原座標: {r[3]}")

    print(f"\n2. 使用者回報且有提供點位、待更新清單（共 {len(new_unprocessed)} 間）：")
    if not new_unprocessed:
        print("   (目前無待更新項目)")
    for item in new_unprocessed:
        s = item["store"]
        sid = s["id"] if s else "未知"
        print(f"   - [{sid}] {item['name']} ({item['city']})")
        print(f"     原座標: {s['lat']}, {s['lng']}")
        print(f"     新座標: {item['new_lat']:.5f}, {item['new_lng']:.5f}")
        print(f"     地理合理性粗略檢查: {item['geo_status']}")
        if item["note"]:
            print(f"     備註: {item['note']}")
