import json
import sys
import os

def generate_report():
    sys.stdout.reconfigure(encoding='utf-8')
    state_path = 'app/src/data/coco_sync_state.json'
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    batches = state.get('batches', [])
    removed_stores = state.get('removed_stores', [])
    confirmed_stores = state.get('confirmed_correct_stores', [])

    lines = []
    lines.append("# Pikmin Bloom × CoCo 都可活動門市 點位維護與更新總紀錄")
    lines.append("")
    lines.append(f"**產出時間**：2026/11/05 20:32 (UTC+8)")
    lines.append(f"**維護區間**：2026/11/05 14:00 ～ 20:30")
    lines.append(f"**線上系統網址**：https://kairosvector.pages.dev/events/coco-pikmin/")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 一、總體異動概覽數據")
    lines.append("")
    lines.append("| 項目 | 統計數值 | 說明 |")
    lines.append("| :--- | :---: | :--- |")
    lines.append("| **總發布批次** | **16 批** | Batch #1 ～ Batch #16，全數同步至正式站、Staging、GitHub 備用站 |")
    lines.append("| **門市總數變化** | **333店 → 339店** | 初始 333 間，中途移除 2 間已歇業店、補齊 8 間實體營運店 |")
    lines.append("| **座標精準校正** | **28 筆** | 修正嚴重偏移、中庭落點、商場定位偏差門市 |")
    lines.append("| **補全新增門市** | **8 筆** | 補齊原名單漏列之台南（2間）、高雄（4間）、雲林（2間）營業門市 |")
    lines.append("| **永久歇業移除** | **2 筆** | 土城廣福店、新豐尚仁店（已撤點歇業） |")
    lines.append("| **查核確認維持** | **4 筆** | 百福門市、楠梓德賢店、捷運北車2 (M3出口) 等確認原座標無誤 |")
    lines.append("| **累計處理項目** | **38 筆** | 解決 140 筆玩家回報案件中的所有實質問題 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 二、新增實體營運門市名細（共 8 間）")
    lines.append("")
    lines.append("| 門市 ID | 縣市 | 門市名稱 | 正確 GPS 座標 | 門市地址 | 電話 | 納入批次 |")
    lines.append("| :---: | :---: | :--- | :---: | :--- | :--- | :---: |")
    lines.append("| `coco-334` | 台南市 | CoCo都可 安平郡平店 | `22.98922, 120.16823` | 台南市安平區郡平路160號 | (06) 298-0588 | Batch #9 |")
    lines.append("| `coco-335` | 台南市 | CoCo都可 永康大灣店 | `22.99937, 120.25413` | 台南市永康區大灣路976號 | (06) 271-8818 | Batch #9 |")
    lines.append("| `coco-336` | 高雄市 | CoCo都可 岡山樂購廣場店 | `22.77993, 120.30010` | 高雄市岡山區捷安路1巷2號3樓 (秀泰3F) | (07) 625-7808 | Batch #13 |")
    lines.append("| `coco-337` | 高雄市 | CoCo都可 SKM Park店 | `22.58334, 120.33010` | 高雄市前鎮區中安路1之1號3樓 (大道東3F) | (07) 791-5808 | Batch #13 |")
    lines.append("| `coco-338` | 高雄市 | CoCo都可 鳳山青年店 | `22.63975, 120.35117` | 高雄市鳳山區青年路二段296號 | (07) 777-6288 | Batch #13 |")
    lines.append("| `coco-339` | 高雄市 | CoCo都可 左營新光店 | `22.68780, 120.30921` | 高雄市左營區高鐵路123號B2 (彩虹市集B2) | (07) 345-6608 | Batch #13 |")
    lines.append("| `coco-340` | 雲林縣 | CoCo都可 虎尾中正店 | `23.70814, 120.43351` | 雲林縣虎尾鎮中正路125號 | (05) 632-6083 | Batch #15 |")
    lines.append("| `coco-341` | 雲林縣 | CoCo都可 斗六萬家福 | `23.70152, 120.53048` | 雲林縣斗六市雲林路二段297號 | (05) 537-5500 | Batch #16 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 三、永久歇業門市移除名細（共 2 間）")
    lines.append("")
    lines.append("| 門市 ID | 縣市 | 門市名稱 | 原資料庫地址 | 移除原因 | 執行時間 |")
    lines.append("| :---: | :---: | :--- | :--- | :--- | :--- |")
    lines.append("| `coco-114` | 新北市 | CoCo都可 土城廣福店 | 新北市土城區廣福街48號 | 已歇業撤點，實勘確認無營業 | 2026-11-05 15:05 (Batch #5) |")
    lines.append("| `coco-266` | 新竹縣 | CoCo都可(新豐尚仁店) | 新竹縣新豐鄉松柏村尚仁街2-3號 | 已歇業撤點，實勘確認無營業 | 2026-11-05 20:10 (Batch #14) |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 四、28 筆座標校正明細表（按發布時間排序）")
    lines.append("")
    lines.append("| 序號 | 批次 | 門市 ID | 門市名稱 | 修正後精準座標 | 校正背景說明 |")
    lines.append("| :---: | :---: | :---: | :--- | :---: | :--- |")

    idx = 1
    for b in batches:
        bid = b['batch_id']
        for s in b.get('updated_stores', []):
            if '新增' in s.get('source', '') or '移除' in s.get('action', '') or '移除' in s.get('reason', ''):
                continue
            lines.append(f"| {idx:2d} | #{bid:2d} | `{s['id']}` | {s['name']} | `{s.get('coords', '')}` | {s.get('source', '表單提供點位')} |")
            idx += 1

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 五、各發布批次（Batch #1 ～ #16）執行歷程")
    lines.append("")

    for b in batches:
        lines.append(f"### 第 {b['batch_id']} 波更新 ({b['applied_at']})")
        lines.append(f"- **發布目標**：{b.get('target', 'Product & Staging')}")
        lines.append(f"- **異動筆數**：{len(b.get('updated_stores', []))} 筆")
        lines.append("- **清單**：")
        for s in b.get('updated_stores', []):
            desc = s.get('coords', '')
            if 'action' in s:
                desc = f"[{s['action']}] {s.get('reason', '')}"
            elif 'source' in s:
                desc = f"{desc} ({s['source']})"
            lines.append(f"  * `[{s['id']}]` {s['name']} —— {desc}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 六、目前唯一待追蹤事項")
    lines.append("")
    lines.append("- **`[coco-101]` CoCo都可 南華店**（新北市中和區南華路57號）：")
    lines.append("  * 原座標：`24.9971, 121.50421`")
    lines.append("  * 狀態：使用者回報原座標有微幅誤差，但尚未提供正確 GPS，待後續玩家提供精準座標時再行校正。")
    lines.append("")

    content = "\n".join(lines)

    target_file = "D:\\Google_shared\\CoCo都可_皮克敏點位更新總紀錄_20261105.md"
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully generated shared report at: {target_file}")

if __name__ == '__main__':
    generate_report()
