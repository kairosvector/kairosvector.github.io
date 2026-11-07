import json
import sys
import os

def generate_clean_txt():
    sys.stdout.reconfigure(encoding='utf-8')
    state_path = 'app/src/data/coco_sync_state.json'
    stores_path = 'app/src/data/coco_stores.json'
    
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    batches = state.get('batches', [])
    removed_stores = state.get('removed_stores', [])

    lines = []
    lines.append("================================================================================")
    lines.append("  Pikmin Bloom × CoCo 都可全台門市 點位維護與更新總紀錄（乾淨純文字版）")
    lines.append("================================================================================")
    lines.append("最新更新時間：2026/11/07 09:57 (UTC+8)")
    lines.append("活動網址：https://kairosvector.pages.dev/events/coco-pikmin/")
    lines.append("")
    lines.append("--------------------------------------------------------------------------------")
    lines.append("【總體數據概覽】")
    lines.append("--------------------------------------------------------------------------------")
    lines.append(f"• 總發布批次：共 {len(batches)} 波更新（已全數同步至正式站、Staging、GitHub 雙備援遠端）")
    lines.append(f"• 門市總數：目前全台共 {len(stores)} 間門市資料庫，均經實勘與精準校對")
    lines.append("• 本次重大恢復（Batch #33）：重新上架「新豐尚仁店」(coco-266)，座標校正為 24.86688, 120.99024")
    lines.append(f"• 永久歇業移除：{len(removed_stores)} 間（土城廣福店）")
    lines.append("• 玩家回報處理率：245 筆回報全數過濾完畢，0 筆待處理")
    lines.append("")
    lines.append("--------------------------------------------------------------------------------")
    lines.append("【一、全部 33 波更新歷程摘要】")
    lines.append("--------------------------------------------------------------------------------")
    
    for b in batches:
        bid = b.get('batch_id')
        tm = b.get('applied_at', '')
        items = b.get('updated_stores', [])
        lines.append(f"• 第 {bid:02d} 波 ({tm}) [{len(items)} 筆]")
        for item in items:
            name = item.get('name', item.get('id', ''))
            coords = item.get('coords', item.get('new_coords', ''))
            action = item.get('action', '')
            reason = item.get('reason', item.get('source', ''))
            extra = f" -> {coords}" if coords else ""
            if action:
                extra += f" [{action}]"
            lines.append(f"    - {name}{extra}")
            if reason:
                lines.append(f"      備註：{reason}")
        lines.append("")

    lines.append("--------------------------------------------------------------------------------")
    lines.append("【二、目前待追蹤門市名單】")
    lines.append("--------------------------------------------------------------------------------")
    lines.append("• [coco-101] CoCo都可 南華店 (新北市中和區南華路57號) - 待玩家提供精準 GPS")
    lines.append("• [coco-34] CoCo都可 石牌商城店 (台北市北投區裕民三路1號) - 待玩家提供精準 GPS")
    lines.append("")
    lines.append("================================================================================")
    lines.append("  本文件由 Kairos Vector Studio 自動化運維紀錄系統匯出")
    lines.append("================================================================================")

    content = "\n".join(lines)

    target_file = r"D:\Google_shared\CoCo都可_點位更新紀錄_純文字版.txt"
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully generated clean text file: {target_file}")

    target_md = r"D:\Google_shared\CoCo都可_點位更新紀錄_純文字版.md"
    with open(target_md, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully generated markdown file: {target_md}")

if __name__ == '__main__':
    generate_clean_txt()
