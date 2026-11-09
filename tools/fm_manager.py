# -*- coding: utf-8 -*-
"""
FamilyMart Pikmin Event Report Manager
Synchronizes and verifies user crowdsourced reports from Google Sheets.
Matches store names against tools/data/fm_dictionary.json (965 stores).
"""
import urllib.request
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

GAS_URL = "https://script.google.com/macros/s/AKfycbzgtI_7aWF-x5-y3ETnkDLHrb7wXCGeCw8zfZ-2TAMdty-UI6fox2-NR1EKhJhbdNGZLA/exec"
DICT_FILE = "tools/data/fm_dictionary.json"
STATE_FILE = "tools/data/fm_sync_state.json"

def normalize_name(name):
    if not name:
        return ""
    n = name.strip()
    for prefix in ["全家便利商店", "全家", "FamilyMart", "familymart"]:
        n = n.replace(prefix, "")
    for c_prefix in ["台北", "臺北", "苗栗", "嘉義", "台東", "臺東"]:
        if n.startswith(c_prefix):
            n = n[len(c_prefix):]
    n = n.replace(" ", "").replace("　", "").replace("門市", "").replace("店", "")
    return n

def load_dictionary():
    if not os.path.exists(DICT_FILE):
        return []
    with open(DICT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def match_in_dictionary(reported_name, city=None, address=None, dictionary=None):
    if not dictionary:
        dictionary = load_dictionary()
    
    norm_rep = normalize_name(reported_name)
    if not norm_rep:
        return None

    # 1. Exact match on rawName, shortName or name
    for s in dictionary:
        if s.get("rawName") == reported_name or s.get("shortName") == reported_name or s.get("name") == reported_name:
            return s

    # 2. Match on normalized name
    candidates = []
    for s in dictionary:
        norm_dict = normalize_name(s.get("rawName"))
        if norm_rep == norm_dict:
            candidates.append(s)
        elif norm_rep in norm_dict or norm_dict in norm_rep:
            if len(norm_rep) >= 2 and len(norm_dict) >= 2:
                candidates.append(s)

    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) > 1:
        if city:
            for c in candidates:
                if city in c.get("city", "") or city in c.get("address", "") or city in c.get("district", ""):
                    return c
        return candidates[0]

    # 3. Match on address if provided
    if address and len(address.strip()) >= 5:
        clean_addr = address.replace(" ", "").replace("　", "")
        for s in dictionary:
            dict_addr = s.get("address", "").replace(" ", "").replace("　", "")
            if clean_addr in dict_addr or dict_addr in clean_addr:
                return s

    return None

def fetch_gas_rows():
    req = urllib.request.Request(GAS_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching GAS rows: {e}")
        return []

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_synced_row": 0}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def main():
    rows = fetch_gas_rows()
    state = load_state()
    dictionary = load_dictionary()

    print(f"=== 全家便利商店 Pikmin 活動回報審核系統 ===")
    print(f"資料庫權威字典門市數: {len(dictionary)} 間")
    print(f"雲端總回報列數: {len(rows)} 列 (上次處理至第 {state.get('last_synced_row', 0)} 列)\n")

    fm_rows = []
    for idx, r in enumerate(rows, 1):
        if not isinstance(r, list):
            continue
        # Ensure 7 columns
        while len(r) < 7:
            r.append("")
        ts, name, city, orig_coords, rtype, new_coords, note = r[:7]

        # Check if row belongs to FamilyMart
        is_fm = (
            "全家" in name or
            "全家" in rtype or
            "familymart" in rtype.lower() or
            "familymart" in name.lower() or
            "特別地點" in rtype or
            "特別地點" in note
        )
        if is_fm:
            fm_rows.append((idx, ts, name, city, orig_coords, rtype, new_coords, note))

    print(f"全家相關回報筆數: {len(fm_rows)} 筆")
    if not fm_rows:
        print("目前尚無全家活動相關新回報。系統準備就緒，待玩家提交即可自動核對！")
        return

    card_verifications = []
    new_store_reports = []

    for item in fm_rows:
        idx, ts, name, city, orig_coords, rtype, new_coords, note = item
        if "實測" in rtype or "特別地點" in rtype:
            card_verifications.append(item)
        else:
            new_store_reports.append(item)

    print(f"  - 門市實測回報: {len(card_verifications)} 筆")
    print(f"  - 新增門市回報: {len(new_store_reports)} 筆\n")

    for idx, ts, name, city, orig_coords, rtype, new_coords, note in fm_rows:
        match = match_in_dictionary(name, city=city, dictionary=dictionary)
        if match:
            matched_str = f"✅ 字典比對成功: {match['city']}{match['district']}【{match['name']}】({match['coordsText']})"
        else:
            matched_str = f"⚠️ 未比對到現有字典 (待人工確認或新增縣市)"
        print(f"#{idx} [{ts[:10] if ts else 'N/A'}] 門市: {name} | 城市: {city} | 狀態: {rtype}")
        print(f"     座標: {new_coords or orig_coords or '留空'} | 備註: {note}")
        print(f"     -> {matched_str}")

if __name__ == '__main__':
    main()
