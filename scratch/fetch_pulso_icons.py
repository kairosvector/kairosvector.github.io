import urllib.request
import json
import re

names = [
    'map.ts', 'map-2.ts', 'map-pin.ts', 'gamepad-2.ts', 'flower.ts',
    'plane.ts', 'plane-takeoff.ts', 'rocket.ts', 'navigation-2.ts', 'send-2.ts',
    'gps.ts', 'crosshair.ts'
]

url = 'https://api.github.com/repos/CityPulso/PulsoIcon/git/trees/main?recursive=1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
tree = json.loads(urllib.request.urlopen(req).read().decode('utf-8')).get('tree', [])
lookup = {t['path'].split('/')[-1]: t['path'] for t in tree if t['path'].split('/')[-1] in names}

results = {}
for n in names:
    if n in lookup:
        raw_url = f'https://raw.githubusercontent.com/CityPulso/PulsoIcon/main/{lookup[n]}'
        raw_req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
        code = urllib.request.urlopen(raw_req).read().decode('utf-8')
        
        # PulsoIcon nodes format: [ "tag", { ... } ]
        # Let's extract paths/circles/lines
        # e.g.: ["path", { d: "..." }]
        elements = []
        for line in code.splitlines():
            line = line.strip()
            d_match = re.search(r'd:\s*\"([^\"]+)\"', line)
            if d_match:
                elements.append(f'<path d="{d_match.group(1)}" />')
            cx_match = re.search(r'cx:\s*([0-9.]+).*?cy:\s*([0-9.]+).*?r:\s*([0-9.]+)', line)
            if cx_match:
                elements.append(f'<circle cx="{cx_match.group(1)}" cy="{cx_match.group(2)}" r="{cx_match.group(3)}" />')
            x1_match = re.search(r'x1:\s*\"?([0-9.]+)\"?.*?y1:\s*\"?([0-9.]+)\"?.*?x2:\s*\"?([0-9.]+)\"?.*?y2:\s*\"?([0-9.]+)\"?', line)
            if x1_match:
                elements.append(f'<line x1="{x1_match.group(1)}" y1="{x1_match.group(2)}" x2="{x1_match.group(3)}" y2="{x1_match.group(4)}" />')
        
        svg = f'<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n  ' + '\n  '.join(elements) + '\n</svg>'
        results[n] = svg
        print(f'=== {n} ===')
        print(svg)

with open('scratch/pulso_icons.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
