# coding: utf-8
import urllib.request
import json
import math
import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlam = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2.0)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"
FM_STATE_FILE = "app/src/data/fm_patrol_state.json"
FM_STORES_FILE = "app/src/data/fm_taipei_stores.json"
FM_DICT_FILE = "app/src/data/fm_dictionary.json"
FM_PROD_ROUTES_FILE = "app/src/data/fm_hot_routes.json"
FM_STAGING_ROUTES_FILE = "app/src/data/fm_hot_routes_staging.json"

def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_sheet_rows():
    req = urllib.request.Request(GAS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

def parse_coords(text):
    if not text:
        return None, None
    clean = text.strip().strip("()（）")
    sep = "," if "," in clean else " "
    parts = [x.strip() for x in clean.split(sep) if x.strip()]
    if len(parts) >= 2:
        try:
            return float(parts[0]), float(parts[1])
        except Exception:
            return None, None
    return None, None

def parse_multi_coords(text):
    if not text:
        return []
    lines = text.strip().split('\n')
    valid = []
    for line in lines:
        lat, lng = parse_coords(line)
        if lat is not None and lng is not None:
            valid.append((lat, lng))
    return valid

def is_in_taiwan(lat, lng):
    return 21.8 <= lat <= 26.5 and 119.5 <= lng <= 122.5

def match_fm_store(name, city, stores):
    clean_name = name.replace("全家便利商店", "").replace("全家", "").strip()
    for s in stores:
        if s["id"] == name or s["name"] == name:
            return s
        if clean_name and (clean_name == s.get("shortName") or clean_name in s.get("name", "")):
            return s
    return None

def run_patrol(dry_run=False):
    rows = fetch_sheet_rows()
    state = load_json(FM_STATE_FILE, {
        "processed_timestamps": [],
        "auto_calibrated_count": 0,
        "auto_routes_count": 0
    })
    processed_set = set(state.get("processed_timestamps", []))

    fm_stores = load_json(FM_STORES_FILE, [])
    fm_dict = load_json(FM_DICT_FILE, {})
    prod_routes = load_json(FM_PROD_ROUTES_FILE, [])
    staging_routes = load_json(FM_STAGING_ROUTES_FILE, [])

    auto_updated_stores = []
    auto_added_routes = []
    flagged_anomalies = []
    has_changes = False

    for idx, r in enumerate(rows):
        ts = r[0] if len(r) > 0 else ""
        name = r[1] if len(r) > 1 else ""
        city = r[2] if len(r) > 2 else ""
        orig_coords = r[3] if len(r) > 3 else ""
        rtype = r[4] if len(r) > 4 else ""
        new_coords = r[5] if len(r) > 5 else ""
        note = r[6] if len(r) > 6 else ""

        # Only process FamilyMart rows
        is_fm = ("全家" in name or "全家" in rtype or "familymart" in name.lower() or 
                 "familymart" in rtype.lower() or name.startswith("[路線投稿]"))
        if not is_fm:
            continue

        if ts in processed_set:
            continue

        # 1. Route Submission
        if rtype == "全家路線投稿" or name.startswith("[路線投稿]"):
            coords_list = parse_multi_coords(new_coords)
            author = "熱心飛友"
            if "貢獻者: @" in note:
                author = note.split("貢獻者: @")[1].split(" |")[0].strip()

            title = name.replace("[路線投稿]", "").strip() or "社群私房路線"

            # Check point count
            if len(coords_list) < 3:
                flagged_anomalies.append({
                    "type": "路線點位過少",
                    "title": title,
                    "author": author,
                    "points": len(coords_list),
                    "ts": ts
                })
                processed_set.add(ts)
                continue

            # Check bounding box (Taiwan)
            all_taiwan = all(is_in_taiwan(lat, lng) for lat, lng in coords_list)
            if not all_taiwan:
                flagged_anomalies.append({
                    "type": "非台灣坐標/測試路線",
                    "title": title,
                    "author": author,
                    "note": note,
                    "sample": f"{coords_list[0][0]:.4f}, {coords_list[0][1]:.4f}",
                    "ts": ts
                })
                processed_set.add(ts)
                continue

            # Check current community routes count in prod
            current_comm_routes = [route for route in prod_routes if route.get("isOfficial") is False]
            if len(current_comm_routes) < 10:
                # Auto-approve & Publish!
                total_dist = 0
                for i in range(len(coords_list) - 1):
                    total_dist += haversine(coords_list[i][0], coords_list[i][1], coords_list[i+1][0], coords_list[i+1][1])
                avg_gap = int(total_dist / (len(coords_list) - 1)) if len(coords_list) > 1 else 150
                km = round(total_dist / 1000, 2)
                walk_min = max(10, int(km / 4.0 * 60))

                route_obj = {
                    "id": f"route-comm-{len(current_comm_routes) + 1}",
                    "title": title,
                    "subtitle": f"社群玩家推薦 · {len(coords_list)} 點",
                    "desc": note.split("| 心得: ")[1].split(" |")[0].strip() if "| 心得: " in note else "由熱心飛友實測推薦之私房巡航路線。",
                    "tag": "玩家推薦",
                    "tagColor": "#8B5CF6",
                    "author": author,
                    "isOfficial": False,
                    "storeCount": len(coords_list),
                    "totalKm": km,
                    "avgGapMeters": avg_gap,
                    "estWalkTimeMin": walk_min,
                    "routeText": "\n".join([f"{lat:.6f},{lng:.6f}" for lat, lng in coords_list]),
                    "firstStore": {
                        "name": f"{title} (起點)",
                        "shortName": title[:6],
                        "lat": coords_list[0][0],
                        "lng": coords_list[0][1],
                        "coordsText": f"{coords_list[0][0]:.5f}, {coords_list[0][1]:.5f}"
                    },
                    "sampleStores": [f"點位 {i+1}" for i in range(min(4, len(coords_list)))],
                    "allStoreIds": []
                }
                prod_routes.append(route_obj)
                staging_routes.append(route_obj)
                auto_added_routes.append(route_obj)
                has_changes = True
                processed_set.add(ts)
            else:
                flagged_anomalies.append({
                    "type": "投稿超過10筆待審核",
                    "title": title,
                    "author": author,
                    "points": len(coords_list),
                    "ts": ts
                })
                processed_set.add(ts)
            continue

        # 2. Store Coordinate Calibration
        if "坐標更正" in rtype or "座標更正" in rtype or (new_coords.strip() and "歇業" not in rtype):
            lat, lng = parse_coords(new_coords)
            if lat is None or lng is None:
                processed_set.add(ts)
                continue

            store = match_fm_store(name, city, fm_stores)
            if not store:
                flagged_anomalies.append({
                    "type": "找不到對應門市",
                    "name": name,
                    "city": city,
                    "reported_coords": f"{lat:.5f}, {lng:.5f}",
                    "ts": ts
                })
                processed_set.add(ts)
                continue

            diff = haversine(store["lat"], store["lng"], lat, lng)
            if diff <= 15:
                # Already matched or within 15m
                processed_set.add(ts)
                continue

            if diff <= 500:
                # Safe auto-calibration (under 500m)!
                old_c_str = f"{store['lat']:.5f}, {store['lng']:.5f}"
                new_c_str = f"{lat:.5f}, {lng:.5f}"
                store["lat"] = lat
                store["lng"] = lng
                store["coordsText"] = new_c_str
                store["gmapUrl"] = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"

                # Update in dictionary if exists
                if store["id"] in fm_dict:
                    fm_dict[store["id"]]["lat"] = lat
                    fm_dict[store["id"]]["lng"] = lng
                    fm_dict[store["id"]]["coordsText"] = new_c_str

                auto_updated_stores.append({
                    "id": store["id"],
                    "name": store["name"],
                    "shortName": store["shortName"],
                    "oldCoords": old_c_str,
                    "newCoords": new_c_str,
                    "diffMeters": round(diff, 1),
                    "ts": ts
                })
                has_changes = True
                processed_set.add(ts)
            else:
                # Distance > 500m (suspicious / anomaly)
                flagged_anomalies.append({
                    "type": f"偏移過大 ({diff:.0f}m > 500m)",
                    "id": store["id"],
                    "name": store["name"],
                    "oldCoords": f"{store['lat']}, {store['lng']}",
                    "reportedCoords": f"{lat:.5f}, {lng:.5f}",
                    "ts": ts
                })
                processed_set.add(ts)
            continue

        # 3. Store Closed Report
        if "歇業" in rtype:
            flagged_anomalies.append({
                "type": "門市已歇業回報",
                "name": name,
                "note": note,
                "ts": ts
            })
            processed_set.add(ts)
            continue

        processed_set.add(ts)

    # If changes made, save and trigger rebuild & deployment
    if has_changes and not dry_run:
        save_json(FM_STORES_FILE, fm_stores)
        save_json(FM_DICT_FILE, fm_dict)
        save_json(FM_PROD_ROUTES_FILE, prod_routes)
        save_json(FM_STAGING_ROUTES_FILE, staging_routes)

        state["auto_calibrated_count"] = state.get("auto_calibrated_count", 0) + len(auto_updated_stores)
        state["auto_routes_count"] = state.get("auto_routes_count", 0) + len(auto_added_routes)

        # Re-generate both pages
        subprocess.run(["python", "tools/generate_fm_page.py", "--prod"], check=True)
        # Build Astro
        subprocess.run(["npm", "--prefix", "app", "run", "build"], shell=True, check=True)
        # Deploy to Cloudflare Pages
        subprocess.run(["npx", "wrangler", "pages", "deploy", "dist", "--project-name", "kairosvector"], cwd="app", shell=True, check=True)

    # Always persist processed reports so we don't repeatedly flag anomalies every cron
    if not dry_run:
        state["processed_timestamps"] = list(processed_set)
        save_json(FM_STATE_FILE, state)

    # Output concise mobile report if updates or anomalies occurred
    if auto_updated_stores or auto_added_routes or flagged_anomalies:
        import datetime
        now_str = datetime.datetime.now().strftime("%H:%M")
        print(f"📱 **全家地圖自動巡檢速報** ({now_str})")
        if auto_updated_stores:
            print(f"✅ **坐標自動校正 ({len(auto_updated_stores)} 間)**：")
            for s in auto_updated_stores:
                print(f"  • {s['shortName']}：微調 {s['diffMeters']}m ➔ 已發布")
        if auto_added_routes:
            print(f"🏆 **新路線自動上架 ({len(auto_added_routes)} 條)**：")
            for r in auto_added_routes:
                print(f"  • {r['title']} (@{r['author']}) · {r['storeCount']} 店 ➔ 已發布")
        if flagged_anomalies:
            print(f"⚠️ **待確認項目 ({len(flagged_anomalies)} 筆)**：")
            for a in flagged_anomalies:
                print(f"  • [{a['type']}] {a.get('name') or a.get('title')}")
        if has_changes:
            print("🚀 *已自動編譯並推播至 Production 正式版*")
    else:
        # Completely silent when no updates
        pass

if __name__ == '__main__':
    run_patrol(dry_run=False)
