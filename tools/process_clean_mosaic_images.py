from PIL import Image, ImageFilter
import os

def apply_mosaic(im, box, block_size=10):
    x1, y1, x2, y2 = box
    r = im.crop((x1, y1, x2, y2))
    r = r.filter(ImageFilter.GaussianBlur(radius=2))
    s = r.resize((max(1, (x2 - x1) // block_size), max(1, (y2 - y1) // block_size)), Image.Resampling.NEAREST)
    m = s.resize((x2 - x1, y2 - y1), Image.Resampling.NEAREST)
    im.paste(m, (x1, y1))

raw_dir = "C:/Users/kevy_win11/.gemini/antigravity/brain/54b49599-cd6a-4bdf-a92c-1c9393255b72/.user_uploaded"
out_dir = "app/public/images/tips"

# Image 1
print("Processing Image 1 (clean with mosaic only)...")
im1 = Image.open(f"{raw_dir}/media_1792506935733_914c2e80.jpg")
apply_mosaic(im1, (0, 0, 471, 50), 10) # Status bar
apply_mosaic(im1, (115, 140, 360, 190), 10) # 未模擬 • 真實定位
apply_mosaic(im1, (0, 150, 120, 240), 12) # Map river/highway names
apply_mosaic(im1, (15, 800, 230, 880), 12) # Address & coordinate
im1.save(f"{out_dir}/geosim-circle-step1-center.jpg", quality=95)

# Image 2
print("Processing Image 2 (clean with mosaic only)...")
im2 = Image.open(f"{raw_dir}/media_1792506942119_bdae7fbd.jpg")
apply_mosaic(im2, (0, 0, 471, 50), 10) # Status bar
im2.save(f"{out_dir}/geosim-circle-step2-advanced.jpg", quality=95)

# Image 3
print("Processing Image 3 (clean with mosaic only)...")
im3 = Image.open(f"{raw_dir}/media_1792506948574_f7b8512b.jpg")
apply_mosaic(im3, (0, 0, 471, 50), 10) # Status bar
apply_mosaic(im3, (150, 650, 420, 690), 10) # Center coordinate
im3.save(f"{out_dir}/geosim-circle-step3-shape-radius.jpg", quality=95)

# Image 4
print("Processing Image 4 (clean with mosaic only)...")
im4 = Image.open(f"{raw_dir}/media_1792506955531_3fe345c2.jpg")
apply_mosaic(im4, (0, 0, 471, 50), 10) # Status bar
im4.save(f"{out_dir}/geosim-circle-step4-speed-loop.jpg", quality=95)

# Image 5
print("Processing Image 5 (clean with mosaic only)...")
im5 = Image.open(f"{raw_dir}/media_1792506962489_56cefc70.jpg")
apply_mosaic(im5, (0, 0, 471, 50), 10) # Status bar
apply_mosaic(im5, (0, 110, 80, 220), 12) # Map river/highway names
im5.save(f"{out_dir}/geosim-circle-step5-running.jpg", quality=95)

print("All 5 images saved cleanly with mosaic only!")
