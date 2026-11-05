import urllib.request
import json
import math
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
req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    all_rows = json.loads(resp.read().decode("utf-8"))

with open("app/src/data/coco_stores.json", "r", encoding="utf-8") as f:
    stores = json.load(f)

print(f"Total rows fetched from Google Sheet: {len(all_rows)}")

# Known already-updated stores in product:
# coco-22 (松山壹號), coco-36 (三井南港), coco-51 (捷運北車2-M3), coco-52 (捷運北車),
# coco-58 (忠孝復興), coco-319 (西螺服務區), coco-326 (夢時代), coco-329 (高雄大遠百),
# coco-332 (台北南機場), coco-333 (竹北中正2)
ALREADY_UPDATED_IDS = {
    "coco-22", "coco-36", "coco-51", "coco-52", "coco-58",
    "coco-319", "coco-326", "coco-329", "coco-332", "coco-333"
}

# Also map stores by name / shortName
def match_store(reported_name, city):
    for s in stores:
        if s['name'] == reported_name:
            return s
    for s in stores:
        if s['shortName'] in reported_name or reported_name in s['name']:
            return s
    for s in stores:
        if s['city'] == city and any(part in s['name'] for part in reported_name.replace("CoCo都可", "").split()):
            return s
    return None

no_coords_reports = []
with_coords_not_updated = []
already_updated_reports = []

for idx, r in enumerate(all_rows):
    ts, name, city, orig_coords, rtype, new_coords, note = r
    if "測試" in name:
        continue

    matched = match_store(name, city)
    store_id = matched['id'] if matched else None

    # Check if already updated
    # Note: 台北南機場 was updated in coco-332 to 25.02820, 121.50624
    if store_id in ALREADY_UPDATED_IDS:
        already_updated_reports.append((idx, r, matched))
        continue

    new_coords_clean = new_coords.strip()
    if not new_coords_clean or rtype == "單純回報有誤":
        no_coords_reports.append((idx, r, matched))
    else:
        # has new coords and NOT updated yet
        try:
            parts = [float(x.strip()) for x in new_coords_clean.split(',') if x.strip()]
            lat, lng = parts[0], parts[1]
            diff = haversine(matched['lat'], matched['lng'], lat, lng) if matched else 0
        except Exception:
            lat, lng, diff = None, None, 0
        with_coords_not_updated.append((idx, r, matched, lat, lng, diff))

# Output JSON for precise inspection
res = {
    "total_rows": len(all_rows),
    "no_coords_count": len(no_coords_reports),
    "with_coords_not_updated_count": len(with_coords_not_updated),
    "already_updated_count": len(already_updated_reports),
    "no_coords": [
        {
            "row": idx,
            "time": r[0],
            "name": r[1],
            "city": r[2],
            "orig_coords": r[3],
            "note": r[6],
            "store_id": m['id'] if m else None,
            "address": m['address'] if m else None
        } for idx, r, m in no_coords_reports
    ],
    "with_coords_not_updated": [
        {
            "row": idx,
            "time": r[0],
            "name": r[1],
            "city": r[2],
            "orig_coords": r[3],
            "new_coords": r[5],
            "note": r[6],
            "store_id": m['id'] if m else None,
            "store_name": m['name'] if m else None,
            "address": m['address'] if m else None,
            "parsed_lat": lat,
            "parsed_lng": lng,
            "diff_meters": diff
        } for idx, r, m, lat, lng, diff in with_coords_not_updated
    ]
}

with open("scratch/classified_reports.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("Classification complete. Written to scratch/classified_reports.json")
