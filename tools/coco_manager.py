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
PENDING_FILE = "app/src/data/coco_pending_verification.json"

STORE_ALIASES = {
    "CoCo都可(巨城民生店)": "coco-245",
    "CoCo都可 台中后里店": "coco-298",
    "廣福店": "coco-151",
    "CoCo都可 苓雅忠孝店": "coco-352",
    "CoCo都可 高雄小港機場店": "coco-353",
    "小港機場店": "coco-353",
    "CoCo都可 南華店": "coco-101",
    "CoCo都可 中和永華店": "coco-101",
    "CoCo都可 台中遠雄店": "coco-305",
    "CoCo都可 台中遠雄": "coco-305",
    "CoCo都可 新竹巨城店": "coco-244",
    "CoCo都可(石牌商城店)": "coco-34",
    "CoCo都可 石牌商城店": "coco-34",
    "CoCo都可 新竹金山2店": "coco-250",
    "CoCo都可龍江2店": "coco-20",
}

BUFFER_FILE = "app/src/data/coco_verified_buffer.json"

# Stores that have been reviewed and verified by user/operator as resolved
RESOLVED_STORES = {
    "coco-55",    # 金山店 (第39波已校正)
    "coco-203",   # 內壢忠孝店 (第39波已校正)
    "coco-214",   # 大溪崎頂店 (第39波已校正)
    "coco-149",   # 桃園介壽店 (使用者確認Pass)
    "coco-42",    # 台北華齡店 (使用者確認Pass)
    "coco-19",    # 台北林森北店 (使用者確認Pass)
    "coco-354",   # 豐原太平洋店 (第38波新增門市)
    "CoCo都可 豐原太平洋店",
    "coco-15",    # 羅東門市 (第37波已校正)
    "coco-29",    # 內湖金龍店 (第37波已校正)
    "coco-46",    # 台北南京店 (第37波已校正)
    "coco-20",    # 龍江2店 (舊回報4.2km異常，已審核不採納)
    "coco-244",   # 新竹巨城店 (中央路207號正確，巨城館內另立coco-348)
    "coco-250",   # 新竹金山2店 (已立新竹園區2店coco-347處理完畢)
    "coco-266",   # 新豐尚仁店 (第33波已重新上架並校正為 24.86688, 120.99024)
    "coco-45",    # 台北民生店 (第34波已微調至 25.05739, 121.51761)
    "coco-328",   # 楠梓德賢店 (第34波已微調至 22.72646, 120.30658)
    "coco-151",   # 八德廣福店 (第35波已微調至 24.95942, 121.29649)
    "coco-352",   # 苓雅忠孝店 (第35波已新增至 22.62000, 120.30774)
    "coco-353",   # 高雄小港機場店 (第36波已新增至 22.57120, 120.34020)
    "coco-245",   # 巨城民生店 (使用者確認現有點位沒問題 pass)
    "coco-298",   # 台中后里店 (使用者確認現有點位沒問題 pass)
    "CoCo都可(新豐尚仁店)",
    "coco-305",   # 台中遠雄 (已去重並校正)
    "coco-101",   # 南華店 (已更名為中和永華店)
    "coco-34",    # 石牌商城 (已微調完成)
    "coco-346",   # 西屯水湳
    "coco-347",   # 園區2
    "coco-348",   # 遠東巨城
    "coco-349",   # 南屯向心南
    "coco-350",   # 基隆七堵
    "coco-58",    # 忠孝復興 (批次#30已微調完成)
    "coco-314",   # 台中東海 (批次#30已微調完成)
    "coco-45",    # 台北民生店 (網友誤填南京店座標，南京店原本已精準，不採納)
    "coco-50",
    "coco-332",   # 台北南機場 (批次#31已微調完成)
    "coco-186",   # 龜山民生北 (批次#31已微調完成)
    "coco-221",
    "coco-1",     # 基隆百福 (批次#32已微調完成)
    "coco-9",     # 基隆長庚 (批次#32已微調完成),   # 平鎮龍南 (批次#31已微調完成),    # 台北南昌店 (網友無座標純報錯，OSM圖資核對現有座標已在店址門口，暫維持)
    "CoCo都可 土城廣福店",  # 已納入批次#27
}

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
    if reported_name in STORE_ALIASES:
        target_id = STORE_ALIASES[reported_name]
        for s in stores:
            if s["id"] == target_id:
                return s

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

    # Build set of resolved IDs
    all_resolved_ids = set(RESOLVED_STORES)
    for b in state.get("batches", []):
        for s in b.get("updated_stores", []):
            all_resolved_ids.add(s["id"])
    all_resolved_ids.update(set(state.get("all_updated_ids", [])))
    all_resolved_ids.update(set(state.get("confirmed_correct_stores", [])))

    pending_list = []
    filtered_already_resolved = []
    filtered_exact_match = []

    for idx, r in enumerate(sheet_rows):
        ts, name, city, orig_coords, rtype, new_coords, note = r
        if "測試" in name:
            continue

        store = match_store(name, city, stores)
        sid = store["id"] if store else None

        # Check if already resolved
        if (sid and sid in all_resolved_ids) or (name in all_resolved_ids):
            filtered_already_resolved.append((sid or name, name, r))
            continue

        # If reported with new coordinates
        if new_coords.strip() and rtype != "單純回報有誤":
            try:
                clean_c = new_coords.strip().strip("()（）")
                # Handle space or comma separated
                if "," in clean_c:
                    parts = [float(x.strip()) for x in clean_c.split(",") if x.strip()][:2]
                else:
                    parts = [float(x.strip()) for x in clean_c.split() if x.strip()][:2]
                lat, lng = parts[0], parts[1]
                diff = haversine(store["lat"], store["lng"], lat, lng) if store else 999999
                
                # If store already has these exact coordinates (within 15m), it's already updated
                if diff < 15:
                    filtered_exact_match.append((sid, name, diff))
                    continue

                if diff <= 2000:
                    geo_status = f"合理（偏移 {diff:.0f} 公尺）"
                elif diff <= 5000:
                    geo_status = f"需注意（偏移 {diff/1000:.1f} 公里）"
                else:
                    geo_status = f"可疑/跨區（偏移 {diff/1000:.1f} 公里）"
            except Exception as e:
                lat, lng, diff = None, None, 0
                geo_status = f"座標格式解析失敗: {e}"

            item = {
                "row_index": idx,
                "timestamp": ts,
                "store_id": sid,
                "store_name": store["name"] if store else name,
                "city": city,
                "current_address": store["address"] if store else "無登記地址",
                "current_coords": f"{store['lat']}, {store['lng']}" if store else orig_coords,
                "reported_coords": f"{lat:.5f}, {lng:.5f}" if lat and lng else new_coords,
                "diff_meters": diff,
                "geo_status": geo_status,
                "user_note": note,
                "report_type": rtype
            }
            pending_list.append(item)
        elif rtype == "單純回報有誤":
            # Reported error without coords
            item = {
                "row_index": idx,
                "timestamp": ts,
                "store_id": sid,
                "store_name": store["name"] if store else name,
                "city": city,
                "current_address": store["address"] if store else "無登記地址",
                "current_coords": f"{store['lat']}, {store['lng']}" if store else orig_coords,
                "reported_coords": "無（僅單純回報有誤）",
                "diff_meters": 0,
                "geo_status": "待補座標",
                "user_note": note,
                "report_type": rtype
            }
            pending_list.append(item)

    # De-duplicate pending_list by store_id or name (keep latest)
    deduped_pending = {}
    for p in pending_list:
        key = p["store_id"] if p["store_id"] else p["store_name"]
        deduped_pending[key] = p
    final_pending = list(deduped_pending.values())

    # Save to pending verification json file
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(final_pending, f, ensure_ascii=False, indent=2)

    return final_pending, len(sheet_rows), len(filtered_already_resolved), len(filtered_exact_match)

if __name__ == "__main__":
    pending, total_rows, resolved_count, exact_count = analyze()
    print("=" * 65)
    print(f"【CoCo 門市回報智能過濾與待驗證清單】")
    print(f"表單總回報數：{total_rows} 筆")
    print(f"自動過濾已處理/已解決：{resolved_count} 筆")
    print(f"自動過濾吻合無須更新：{exact_count} 筆")
    print(f"待使用者驗證項目：{len(pending)} 筆")
    print("=" * 65)

    if not pending:
        print("\n✅ 目前無任何待驗證項目，所有回報皆已處理或已過濾完畢！")
    else:
        print(f"\n📋 以下為待驗證清單：")
        for idx, item in enumerate(pending, 1):
            print(f"\n{idx}. [{item['store_id'] or '新門市'}] {item['store_name']} ({item['city']})")
            print(f"   - 目前地址: {item['current_address']}")
            print(f"   - 目前座標: {item['current_coords']}")
            print(f"   - 網友回報座標: {item['reported_coords']}")
            print(f"   - 檢查判斷: {item['geo_status']}")
            if item['user_note']:
                print(f"   - 網友備註: {item['user_note']}")
