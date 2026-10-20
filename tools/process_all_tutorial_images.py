from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

FONT_BOLD = 'C:/Windows/Fonts/msjhbd.ttc'
FONT_REG = 'C:/Windows/Fonts/msjh.ttc'

def get_font(size, bold=True):
    path = FONT_BOLD if bold else FONT_REG
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def apply_mosaic(im, box, block_size=10):
    x1, y1, x2, y2 = box
    r = im.crop((x1, y1, x2, y2))
    r = r.filter(ImageFilter.GaussianBlur(radius=2))
    s = r.resize((max(1, (x2 - x1) // block_size), max(1, (y2 - y1) // block_size)), Image.Resampling.NEAREST)
    m = s.resize((x2 - x1, y2 - y1), Image.Resampling.NEAREST)
    im.paste(m, (x1, y1))

def draw_top_banner(im, step_num, title_text):
    width, height = im.size
    banner_h = 58
    
    # Overlay with alpha
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    # Dark banner background
    odraw.rectangle([0, 0, width, banner_h], fill=(15, 23, 42, 245))
    odraw.line([(0, banner_h - 1), (width, banner_h - 1)], fill=(99, 102, 241, 230), width=2)
    
    # Step Badge
    badge_w, badge_h = 80, 28
    badge_x, badge_y = 12, 15
    odraw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=14, fill=(99, 102, 241, 255))
    odraw.text((badge_x + 10, badge_y + 4), f"步驟 {step_num}", font=get_font(13, True), fill=(255, 255, 255, 255))
    
    # Title Text
    odraw.text((badge_x + badge_w + 10, badge_y + 4), title_text, font=get_font(14, True), fill=(255, 255, 255, 255))
    
    im_rgba = im.convert('RGBA')
    im_final = Image.alpha_composite(im_rgba, overlay)
    return im_final.convert('RGB')

def draw_pill(im, x, y, text, subtext="", bg_color=(99, 102, 241, 240), border_color=(224, 231, 255, 255)):
    font_main = get_font(13, True)
    font_sub = get_font(11, False)
    
    text_bbox = font_main.getbbox(text)
    tw = text_bbox[2] - text_bbox[0]
    th = text_bbox[3] - text_bbox[1]
    
    if subtext:
        sub_bbox = font_sub.getbbox(subtext)
        sw = sub_bbox[2] - sub_bbox[0]
        total_w = max(tw, sw) + 24
        total_h = th + 26
    else:
        total_w = tw + 22
        total_h = th + 14
        
    overlay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    
    # Subtle drop shadow
    odraw.rounded_rectangle([x + 2, y + 2, x + total_w + 2, y + total_h + 2], radius=8, fill=(0, 0, 0, 90))
    # Pill box
    odraw.rounded_rectangle([x, y, x + total_w, y + total_h], radius=8, fill=bg_color, outline=border_color, width=1)
    odraw.text((x + 11, y + 6), text, font=font_main, fill=(255, 255, 255, 255))
    if subtext:
        odraw.text((x + 11, y + th + 10), subtext, font=font_sub, fill=(224, 231, 255, 255))
        
    im_rgba = im.convert('RGBA')
    return Image.alpha_composite(im_rgba, overlay).convert('RGB')

def draw_highlight(im, box, color=(99, 102, 241, 255), width=3, radius=12):
    overlay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rounded_rectangle(box, radius=radius, outline=color, width=width)
    im_rgba = im.convert('RGBA')
    return Image.alpha_composite(im_rgba, overlay).convert('RGB')

base_dir = 'app/public/images/tips'

# --- IMAGE 1 ---
print("Processing Image 1...")
im1 = Image.open(f"{base_dir}/geosim-circle-step1-center.jpg")
apply_mosaic(im1, (0, 0, 471, 50), 10) # Status bar
apply_mosaic(im1, (115, 140, 360, 190), 10) # 未模擬 • 真實定位
apply_mosaic(im1, (0, 150, 120, 240), 12) # Map river/highway names
apply_mosaic(im1, (15, 800, 230, 880), 12) # Address & coordinate

im1 = draw_top_banner(im1, "1 / 5", "地圖選定中心點，點擊右下「進階」")
im1 = draw_pill(im1, 230, 540, "📍 設為繞圈中心點", bg_color=(30, 41, 59, 235), border_color=(99, 102, 241, 255))
im1 = draw_highlight(im1, (380, 890, 465, 975), color=(99, 102, 241, 255), width=3, radius=10)
im1 = draw_pill(im1, 240, 840, "👉 點擊右下「進階」", bg_color=(99, 102, 241, 245), border_color=(199, 210, 254, 255))
im1.save(f"{base_dir}/geosim-circle-step1-center.jpg", quality=92)

# --- IMAGE 2 ---
print("Processing Image 2...")
im2 = Image.open(f"{base_dir}/geosim-circle-step2-advanced.jpg")
apply_mosaic(im2, (0, 0, 471, 50), 10) # Status bar
im2 = draw_top_banner(im2, "2 / 5", "在進階功能中點選「繞圈移動」")
im2 = draw_highlight(im2, (20, 255, 450, 385), color=(99, 102, 241, 255), width=3, radius=16)
im2 = draw_pill(im2, 130, 280, "👉 點選「繞圈移動」", subtext="以選定點為圓心，自動生成幾何軌跡", bg_color=(99, 102, 241, 245))
im2.save(f"{base_dir}/geosim-circle-step2-advanced.jpg", quality=92)

# --- IMAGE 3 ---
print("Processing Image 3...")
im3 = Image.open(f"{base_dir}/geosim-circle-step3-shape-radius.jpg")
apply_mosaic(im3, (0, 0, 471, 50), 10) # Status bar
apply_mosaic(im3, (150, 650, 420, 690), 10) # Center coordinate
im3 = draw_top_banner(im3, "3 / 5", "形狀選「圓繞圈」，半徑拉至 475m")

im3 = draw_highlight(im3, (38, 390, 130, 455), color=(99, 102, 241, 255), width=3, radius=10)
im3 = draw_pill(im3, 140, 400, "1️⃣ 形狀選「圓繞圈」", bg_color=(99, 102, 241, 245))

im3 = draw_highlight(im3, (20, 715, 450, 845), color=(99, 102, 241, 255), width=3, radius=16)
im3 = draw_pill(im3, 60, 740, "2️⃣ 半徑設定為 475 m", subtext="上方精算一趟 9:55（大於 5 分鐘冷卻，絕不浪費花瓣！）", bg_color=(99, 102, 241, 245))
im3.save(f"{base_dir}/geosim-circle-step3-shape-radius.jpg", quality=92)

# --- IMAGE 4 ---
print("Processing Image 4...")
im4 = Image.open(f"{base_dir}/geosim-circle-step4-speed-loop.jpg")
apply_mosaic(im4, (0, 0, 471, 50), 10) # Status bar
im4 = draw_top_banner(im4, "4 / 5", "速度設 18~19 km/h，模式選「循環」")

im4 = draw_highlight(im4, (170, 320, 305, 385), color=(99, 102, 241, 255), width=3, radius=12)
im4 = draw_pill(im4, 60, 410, "1️⃣ 速度鎖定 18~19 km/h", subtext="臨界避開 20 km/h 系統防乘車超速中斷", bg_color=(99, 102, 241, 245))

im4 = draw_highlight(im4, (170, 795, 300, 865), color=(99, 102, 241, 255), width=3, radius=12)
im4 = draw_pill(im4, 150, 740, "2️⃣ 運行模式選「循環」", bg_color=(99, 102, 241, 245))

im4 = draw_highlight(im4, (20, 900, 450, 965), color=(16, 185, 129, 255), width=3, radius=12)
im4 = draw_pill(im4, 155, 895, "3️⃣ 點擊「▶ 開始繞圈」", bg_color=(16, 185, 129, 245))
im4.save(f"{base_dir}/geosim-circle-step4-speed-loop.jpg", quality=92)

# --- IMAGE 5 ---
print("Processing Image 5...")
im5 = Image.open(f"{base_dir}/geosim-circle-step5-running.jpg")
apply_mosaic(im5, (0, 0, 471, 50), 10) # Status bar
apply_mosaic(im5, (0, 110, 80, 220), 12) # Map river/highway names
im5 = draw_top_banner(im5, "5 / 5", "自動生成 24 航點巡航，切回遊戲開種！")

im5 = draw_pill(im5, 80, 475, "🎯 自動生成 24 航點平滑大圓", subtext="半徑 475m • 圓周 2.98 km • 完美閉環", bg_color=(30, 41, 59, 240), border_color=(99, 102, 241, 255))
im5 = draw_pill(im5, 60, 610, "🚀 依線巡航中！切回遊戲開始種花", subtext="40隻滿編 • 5.75 朵/秒 • 全自動穩定爆花", bg_color=(16, 185, 129, 245), border_color=(209, 250, 229, 255))
im5.save(f"{base_dir}/geosim-circle-step5-running.jpg", quality=92)

print("All 5 images processed and saved successfully!")
