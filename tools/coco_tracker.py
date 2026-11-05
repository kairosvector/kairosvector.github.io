import urllib.request
import json
import os
import sys

# Ensure UTF-8 output even in Windows cmd/PowerShell
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

STATE_FILE = "app/src/data/coco_sync_state.json"

GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_processed_timestamp": "1970-01-01T00:00:00.000Z",
        "last_processed_row_index": -1,
        "batches": []
    }

def fetch_sheet_rows():
    req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def check_new_reports():
    state = load_state()
    watermark = state.get("last_processed_timestamp", "")
    last_idx = state.get("last_processed_row_index", -1)
    
    rows = fetch_sheet_rows()
    total_rows = len(rows)
    
    new_rows = []
    for idx, r in enumerate(rows):
        ts = r[0]
        if ts > watermark and idx > last_idx:
            new_rows.append((idx, r))

    return state, rows, new_rows

if __name__ == "__main__":
    state, all_rows, new_rows = check_new_reports()
    print("=" * 60)
    print("【CoCo 點位回報處理狀態水線】")
    print(f"目前處理進度時間點：{state['last_processed_local_time']}")
    print(f"UTC 基準時間戳記  ：{state['last_processed_timestamp']}")
    print(f"上次已處理累計列數：第 {state['last_processed_row_index'] + 1} 筆 (Row index {state['last_processed_row_index']})")
    print(f"目前表單最新總列數：{len(all_rows)} 筆")
    print(f"待處理新進回報數量：{len(new_rows)} 筆")
    print("=" * 60)
    
    if new_rows:
        print("\n=== 新進未處理的回報清單 ===")
        for idx, r in new_rows:
            ts, name, city, orig_coords, rtype, new_coords, note = r
            print(f"[{idx:02d}] {ts} | {name} ({city}) | 類型: {rtype} | 新座標: {new_coords} | 備註: {note}")
    else:
        print("\n目前無新進回報，所有回報皆已處理至最新。")
