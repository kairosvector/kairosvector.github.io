import csv
import json
import os
import sys

def build_fm_data():
    sys.stdout.reconfigure(encoding='utf-8')

    input_csv = r'D:\Google_shared\fm-taipei-all.csv'
    output_json = 'app/src/data/fm_taipei_stores.json'
    output_public_json = 'app/public/events/fm-taipei-stores.json'
    output_public_csv = 'app/public/events/fm-taipei-stores.csv'
    output_shared_csv = r'D:\Google_shared\fm-taipei-all-completed.csv'

    # Known exact GPS for the 8 stores missing coordinates in CSV
    coords_patch = {
        '台北玉泉店': (25.05193, 121.51023),
        '台北京盛店': (25.05139, 121.55390),
        '台北仁慈店': (25.03720, 121.54699),
        '台北台師店': (25.02646, 121.52757),
        '台北臺師店': (25.02646, 121.52757),
        '台北和西店': (25.03511, 121.49454),
        '台北園寶店': (25.02640, 121.49149),
        '台北寶興店': (25.02609, 121.49419),
        '台北美崙店': (25.09718, 121.52318),
    }

    stores = []
    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, r in enumerate(reader, 1):
            name = r.get('店名', '').strip()
            orig_name = r.get('原店名', '').strip()
            city = r.get('縣市', '臺北市').strip()
            district = r.get('行政區', '').strip()
            address = r.get('地址', '').strip()
            phone = r.get('電話', '').strip()
            note = r.get('備註', '').strip()

            lat_str = r.get('緯度', '').strip()
            lng_str = r.get('經度', '').strip()

            if lat_str and lng_str:
                lat = round(float(lat_str), 5)
                lng = round(float(lng_str), 5)
            elif name in coords_patch:
                lat, lng = coords_patch[name]
                print(f"Patched coords for {name} ({district}): {lat}, {lng}")
            else:
                print(f"Warning: Missing coords for {name}")
                lat, lng = 25.03300, 121.56540 # Fallback default

            store_id = f"fm-tpe-{idx:03d}"
            short_name = name.replace('台北', '').replace('臺北', '')

            stores.append({
                "id": store_id,
                "city": city,
                "district": district,
                "name": f"全家便利商店 {name}",
                "shortName": short_name,
                "rawName": name,
                "origName": orig_name,
                "address": address,
                "phone": phone,
                "lat": lat,
                "lng": lng,
                "coordsText": f"{lat:.5f}, {lng:.5f}",
                "gmapUrl": f"https://www.google.com/maps/search/?api=1&query={lat:.5f},{lng:.5f}",
                "note": note
            })

    print(f"Processed {len(stores)} FamilyMart stores in Taipei City.")

    # Save to app/src/data
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Save to public
    os.makedirs(os.path.dirname(output_public_json), exist_ok=True)
    with open(output_public_json, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)

    # Save complete CSV
    headers = ['編號', '縣市', '行政區', '店名', '地址', '電話', '緯度', '經度', '座標文字', 'Google地圖連結']
    for p in [output_public_csv, output_shared_csv]:
        with open(p, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerow(headers)
            for s in stores:
                w.writerow([
                    s['id'], s['city'], s['district'], s['name'],
                    s['address'], s['phone'], s['lat'], s['lng'],
                    s['coordsText'], s['gmapUrl']
                ])

    print("All datasets generated successfully!")

if __name__ == '__main__':
    build_fm_data()
