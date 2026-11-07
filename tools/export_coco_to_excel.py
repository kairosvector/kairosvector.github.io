import json
import os
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def export_coco_excel():
    sys.stdout.reconfigure(encoding='utf-8')
    stores_path = 'app/src/data/coco_stores.json'
    with open(stores_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CoCo全台350店資料庫"

    # Define styles
    header_fill = PatternFill(start_color="FF6600", end_color="FF6600", fill_type="solid")  # CoCo Orange
    header_font = Font(name="微軟正黑體", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="微軟正黑體", size=10)
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
        "電話", "緯度", "經度", "直飛座標 (複製用)", "Google Maps 連結", "建議路線分區"
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
            elif col_idx == 10:  # Hyperlink
                cell.alignment = center_align
                cell.font = link_font
                if s.get("gmapUrl"):
                    cell.hyperlink = s.get("gmapUrl")
            else:
                cell.alignment = left_align
                cell.font = data_font

    # Auto-adjust column widths
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
        10: 18, # 連結
        11: 30  # 分區
    }
    for col_idx, width in column_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    # Enable autofilter
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(stores) + 1}"

    # Freeze top row
    ws.freeze_panes = "A2"

    # Save to Google_shared
    output_dir = r"D:\Google_shared"
    output_file = os.path.join(output_dir, "CoCo都可_全台350店門市總資料庫.xlsx")
    wb.save(output_file)
    print(f"Excel saved successfully: {output_file}")

    # Also save a CSV version for direct sheets import
    csv_file = os.path.join(output_dir, "CoCo都可_全台350店門市總資料庫.csv")
    import csv
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
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
                s.get("gmapUrl", ""),
                s.get("route", "")
            ])
    print(f"CSV saved successfully: {csv_file}")

if __name__ == '__main__':
    export_coco_excel()
