import json
import os
import sys
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def update_stores_and_export():
    sys.stdout.reconfigure(encoding='utf-8')

    stores_path = 'app/src/data/coco_stores.json'
    staging_path = 'app/src/data/coco_stores_staging.json'
    state_path = 'app/src/data/coco_sync_state.json'

    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    # Map store_id to update info
    store_update_info = {}
    for b in state.get('batches', []):
        bid = b.get('batch_id')
        for u in b.get('updated_stores', []):
            sid = u.get('id')
            if sid:
                action = u.get('action', '')
                reason = u.get('reason', u.get('source', ''))
                desc = f"第 {bid} 波"
                if action:
                    desc += f" {action}"
                elif '新增' in reason:
                    desc += " 新增門市"
                elif '微調' in reason or '校正' in reason:
                    desc += " 點位微調"
                elif '去重' in reason:
                    desc += " 去重校正"
                else:
                    desc += " 點位校正"
                store_update_info[sid] = {
                    'is_updated': True,
                    'batch_id': bid,
                    'status': f"已更新 ({desc})",
                    'detail': reason or "點位經實勘校正"
                }

    # Inject fields into each store
    for s in stores:
        sid = s['id']
        if sid in store_update_info:
            info = store_update_info[sid]
            s['isUpdated'] = True
            s['updateStatus'] = info['status']
            s['updateDetail'] = info['detail']
            s['updateBatch'] = info['batch_id']
        else:
            s['isUpdated'] = False
            s['updateStatus'] = "未更新 (初始點位)"
            s['updateDetail'] = ""
            s['updateBatch'] = None

    # Save back to json files
    with open(stores_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    with open(staging_path, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"Updated store records in {stores_path} and {staging_path}")

    # Build Excel Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"CoCo全台{len(stores)}店總資料庫"

    # Define styles
    header_fill = PatternFill(start_color="FF6600", end_color="FF6600", fill_type="solid")  # CoCo Orange
    header_font = Font(name="微軟正黑體", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="微軟正黑體", size=10)
    updated_font = Font(name="微軟正黑體", size=10, bold=True, color="1B5E20")  # Dark Green
    updated_fill = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")  # Light Green
    untouched_font = Font(name="微軟正黑體", size=10, color="757575")  # Gray
    link_font = Font(name="微軟正黑體", size=10, color="0000FF", underline="single")
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    headers = [
        "門市編號", "縣市", "門市名稱", "門市簡稱", "地址", 
        "電話", "緯度", "經度", "直飛座標 (複製用)", "是否已更新過", "更新歷程摘要", "Google Maps 連結", "建議路線分區"
    ]

    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    ws.row_dimensions[1].height = 28

    for row_idx, s in enumerate(stores, start=2):
        row_data = [
            s.get("id", ""),
            s.get("city", ""),
            s.get("name", ""),
            s.get("shortName", ""),
            s.get("address", ""),
            s.get("phone", ""),
            s.get("lat", 0.0),
            s.get("lng", 0.0),
            s.get("coordsText", ""),
            s.get("updateStatus", ""),
            s.get("updateDetail", ""),
            s.get("gmapUrl", ""),
            s.get("route", "")
        ]
        ws.append(row_data)
        ws.row_dimensions[row_idx].height = 20

        # Style each cell
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.border = thin_border
            
            if col_idx in [1, 2, 4, 6, 7, 8, 9]:
                cell.alignment = center_align
                cell.font = data_font
            elif col_idx == 10:  # 是否已更新過
                cell.alignment = center_align
                if s.get("isUpdated"):
                    cell.font = updated_font
                    cell.fill = updated_fill
                else:
                    cell.font = untouched_font
            elif col_idx == 11:  # 更新歷程摘要
                cell.alignment = left_align
                cell.font = data_font
            elif col_idx == 12:  # Hyperlink
                cell.alignment = center_align
                cell.font = link_font
                if s.get("gmapUrl"):
                    cell.hyperlink = s.get("gmapUrl")
            else:
                cell.alignment = left_align
                cell.font = data_font

    # Column widths
    column_widths = {
        1: 12,  # 編號
        2: 10,  # 縣市
        3: 26,  # 名稱
        4: 16,  # 簡稱
        5: 38,  # 地址
        6: 15,  # 電話
        7: 12,  # 緯度
        8: 12,  # 經度
        9: 22,  # 直飛座標
        10: 22, # 是否已更新過
        11: 42, # 更新歷程摘要
        12: 18, # 連結
        13: 30  # 分區
    }
    for col_idx, width in column_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(stores) + 1}"
    ws.freeze_panes = "A2"

    # Save to Google_shared
    output_dir = r"D:\Google_shared"
    xlsx_path = os.path.join(output_dir, f"CoCo都可_全台{len(stores)}店門市總資料庫.xlsx")
    wb.save(xlsx_path)
    print(f"Excel saved: {xlsx_path}")

    csv_path = os.path.join(output_dir, f"CoCo都可_全台{len(stores)}店門市總資料庫.csv")
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for s in stores:
            writer.writerow([
                s.get("id", ""),
                s.get("city", ""),
                s.get("name", ""),
                s.get("shortName", ""),
                s.get("address", ""),
                s.get("phone", ""),
                s.get("lat", 0.0),
                s.get("lng", 0.0),
                s.get("coordsText", ""),
                s.get("updateStatus", ""),
                s.get("updateDetail", ""),
                s.get("gmapUrl", ""),
                s.get("route", "")
            ])
    print(f"CSV saved: {csv_path}")

    # Export to public/events for online cloud access & Google Sheets =IMPORTDATA formula
    public_events_dir = 'app/public/events'
    os.makedirs(public_events_dir, exist_ok=True)
    
    pub_json = os.path.join(public_events_dir, 'coco-stores.json')
    with open(pub_json, 'w', encoding='utf-8') as f:
        json.dump(stores, f, ensure_ascii=False, indent=2)
    print(f"Public JSON saved: {pub_json}")

    pub_csv = os.path.join(public_events_dir, 'coco-stores.csv')
    with open(pub_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for s in stores:
            writer.writerow([
                s.get("id", ""),
                s.get("city", ""),
                s.get("name", ""),
                s.get("shortName", ""),
                s.get("address", ""),
                s.get("phone", ""),
                s.get("lat", 0.0),
                s.get("lng", 0.0),
                s.get("coordsText", ""),
                s.get("updateStatus", ""),
                s.get("updateDetail", ""),
                s.get("gmapUrl", ""),
                s.get("route", "")
            ])
    print(f"Public CSV saved: {pub_csv}")

if __name__ == '__main__':
    update_stores_and_export()
