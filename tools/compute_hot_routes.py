# -*- coding: utf-8 -*-
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

def solve_tsp_nn(stores_list):
    """Greedy Nearest Neighbor to order stores cleanly with minimal walking distance"""
    if not stores_list:
        return [], 0
    unvisited = list(stores_list)
    # Pick western-most or northern-most as start
    unvisited.sort(key=lambda s: (s['lat'], s['lng']))
    current = unvisited.pop(0)
    route = [current]
    total_dist = 0

    while unvisited:
        nearest_idx = 0
        min_d = haversine(current['lat'], current['lng'], unvisited[0]['lat'], unvisited[0]['lng'])
        for i in range(1, len(unvisited)):
            d = haversine(current['lat'], current['lng'], unvisited[i]['lat'], unvisited[i]['lng'])
            if d < min_d:
                min_d = d
                nearest_idx = i
        current = unvisited.pop(nearest_idx)
        total_dist += min_d
        route.append(current)

    return route, total_dist

def main():
    with open('app/src/data/fm_taipei_stores.json', 'r', encoding='utf-8') as f:
        stores = json.load(f)

    centers = [
        {
            'id': 'route-station-ximen',
            'title': '台北車站 ✕ 西門町雙商圈',
            'subtitle': '全台補給站密度之冠 · 密集度最高',
            'desc': '串聯站前館前路、重慶南路與西門町徒步區，巷弄間門市極為密集。',
            'center_lat': 25.0450,
            'center_lng': 121.5130,
            'radius': 800,
            'tag': '密度冠軍',
            'tagColor': '#EF4444'
        },
        {
            'id': 'route-zhongshan-nanxi',
            'title': '中山南西 ✕ 雙連文青散步圈',
            'subtitle': '綠意林蔭道 · 好走不繞路',
            'desc': '由中山站沿心中山線形公園至雙連站，左右兩側巷弄密集收割。',
            'center_lat': 25.0555,
            'center_lng': 121.5215,
            'radius': 750,
            'tag': '散步首選',
            'tagColor': '#10B981'
        },
        {
            'id': 'route-east-district',
            'title': '東區商圈 ✕ 忠孝復興至敦化',
            'subtitle': '筆直平坦大道 · 巷弄高密連刷',
            'desc': '忠孝東路兩側美食街巷，門市相距不到百米，適合定速巡航。',
            'center_lat': 25.0420,
            'center_lng': 121.5480,
            'radius': 750,
            'tag': '筆直連刷',
            'tagColor': '#3B82F6'
        },
        {
            'id': 'route-xinyi-gov',
            'title': '信義計畫區 ✕ 市政府商辦圈',
            'subtitle': '百貨空橋連通道 · 避暑速刷線',
            'desc': '市府轉運站周邊延伸至世貿中心，冷氣商辦與百貨周邊高效率連線。',
            'center_lat': 25.0380,
            'center_lng': 121.5650,
            'radius': 750,
            'tag': '商辦精華',
            'tagColor': '#8B5CF6'
        },
        {
            'id': 'route-gongguan-taida',
            'title': '公館商圈 ✕ 台大師大生活圈',
            'subtitle': '學生商圈點位 · 連線極順暢',
            'desc': '公館捷運站往台大側門延伸，吃美食兼刷金色花苗最佳路線。',
            'center_lat': 25.0160,
            'center_lng': 121.5335,
            'radius': 750,
            'tag': '學區熱線',
            'tagColor': '#F59E0B'
        },
        {
            'id': 'route-neihu-tech',
            'title': '內科園區 ✕ 港墘西湖高密線',
            'subtitle': '科技園區商辦 · 50米一間極限密度',
            'desc': '瑞光路、港墘路科技商辦林立，高密度全家一次刷齊。',
            'center_lat': 25.0780,
            'center_lng': 121.5720,
            'radius': 750,
            'tag': '超高密集',
            'tagColor': '#EC4899'
        }
    ]

    hot_routes = []
    for c in centers:
        matched = [s for s in stores if haversine(c['center_lat'], c['center_lng'], s['lat'], s['lng']) <= c['radius']]
        ordered_route, total_dist_m = solve_tsp_nn(matched)
        
        # Calculate stats
        store_count = len(ordered_route)
        total_km = round(total_dist_m / 1000, 2)
        avg_gap_m = round(total_dist_m / (store_count - 1)) if store_count > 1 else 0
        walk_time_min = round(total_km / 4.0 * 60) # 4 km/h walking speed
        
        route_coords = [f"{s['lat']:.5f},{s['lng']:.5f}" for s in ordered_route]
        route_text = "\n".join(route_coords)
        first_store = ordered_route[0]

        hot_routes.append({
            'id': c['id'],
            'title': c['title'],
            'subtitle': c['subtitle'],
            'desc': c['desc'],
            'tag': c['tag'],
            'tagColor': c['tagColor'],
            'storeCount': store_count,
            'totalKm': total_km,
            'avgGapMeters': avg_gap_m,
            'estWalkTimeMin': walk_time_min,
            'routeText': route_text,
            'firstStore': {
                'name': first_store['name'],
                'shortName': first_store['shortName'],
                'lat': first_store['lat'],
                'lng': first_store['lng'],
                'coordsText': first_store['coordsText']
            },
            'sampleStores': [s['shortName'] for s in ordered_route[:6]],
            'allStoreIds': [s['id'] for s in ordered_route]
        })
        print(f"{c['title']}: {store_count} stores, {total_km} km, avg gap {avg_gap_m}m, est {walk_time_min} mins")

    with open('app/src/data/fm_hot_routes.json', 'w', encoding='utf-8') as f:
        json.dump(hot_routes, f, ensure_ascii=False, indent=2)
    print("Saved app/src/data/fm_hot_routes.json successfully!")

if __name__ == '__main__':
    main()
