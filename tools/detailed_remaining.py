import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with open('scratch/sheet_responses.json', 'r', encoding='utf-8') as f:
    responses = json.load(f)

with open('app/src/data/coco_stores.json', 'r', encoding='utf-8') as f:
    stores = json.load(f)

store_map = {s['id']: s for s in stores}

# 1. First, apply the 4 updates to a helper structure to verify
verified_updates = {
    "coco-22": {"lat": 25.04944, "lng": 121.57891, "text": "25.04944, 121.57891", "raw": "25.0494443, 121.5789132"},
    "coco-36": {"lat": 25.05925, "lng": 121.61803, "text": "25.05925, 121.61803", "raw": "25.0592549, 121.6180288"},
    "coco-51": {"lat": 25.04500, "lng": 121.51621, "text": "25.04500, 121.51621", "raw": "25.045004, 121.516210"},
    "coco-58": {"lat": 25.04142, "lng": 121.54508, "text": "25.04142, 121.54508", "raw": "25.041424, 121.545076"}
}

# Find other reports
other_reports_with_coords = []
other_reports_without_coords = []

covered_store_names = ["松山壹號", "三井南港", "捷運北車2", "忠孝復興"]

for idx, r in enumerate(responses):
    ts, name, city, orig_coords, rtype, new_coords, note = r
    if '測試' in name:
        continue
    # If it's about the 4 covered stores (or duplicate like idx 3 where 龍江2 had 松山壹號 coords)
    if any(k in name for k in covered_store_names) or '25.0494443' in new_coords:
        continue

    # Find matching store in coco_stores.json
    matched = [s for s in stores if s['name'] == name or s['shortName'] in name or (s['city'] == city and (name in s['name'] or s['name'] in name))]
    target_store = matched[0] if matched else None

    item = {
        "sheet_idx": idx,
        "time": ts,
        "reported_name": name,
        "city": city,
        "orig_coords": orig_coords,
        "rtype": rtype,
        "new_coords": new_coords.strip(),
        "note": note.strip(),
        "store": target_store
    }

    if new_coords.strip():
        # parse coords
        try:
            parts = [float(x.strip()) for x in new_coords.split(',') if x.strip()]
            item["parsed_lat"] = parts[0]
            item["parsed_lng"] = parts[1]
            if target_store:
                item["distance_diff_meters"] = haversine(target_store["lat"], target_store["lng"], parts[0], parts[1])
            else:
                item["distance_diff_meters"] = 0
        except Exception as e:
            item["parse_error"] = str(e)
        other_reports_with_coords.append(item)
    else:
        other_reports_without_coords.append(item)

report_data = {
    "with_coords": other_reports_with_coords,
    "without_coords": other_reports_without_coords
}

with open('scratch/detailed_remaining.json', 'w', encoding='utf-8') as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print(f"Other reports with coords: {len(other_reports_with_coords)}")
print(f"Other reports without coords: {len(other_reports_without_coords)}")
