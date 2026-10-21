from PIL import Image, ImageFilter

def apply_mosaic(im, box, block_size=10):
    x1, y1, x2, y2 = box
    r = im.crop((x1, y1, x2, y2))
    r = r.filter(ImageFilter.GaussianBlur(radius=2))
    s = r.resize((max(1, (x2 - x1) // block_size), max(1, (y2 - y1) // block_size)), Image.Resampling.NEAREST)
    m = s.resize((x2 - x1, y2 - y1), Image.Resampling.NEAREST)
    im.paste(m, (x1, y1))

raw_dir = "C:/Users/kevy_win11/.gemini/antigravity/brain/54b49599-cd6a-4bdf-a92c-1c9393255b72/.user_uploaded"
out_dir = "app/public/images/tips"

# Step 1: Ready state (media_1792571532093_7167d2c1.jpg)
im1 = Image.open(f"{raw_dir}/media_1792571532093_7167d2c1.jpg")
apply_mosaic(im1, (0, 0, 471, 50), 10) # Status bar
im1.save(f"{out_dir}/geosim-area-roam-step1-ready.jpg", quality=95)

# Step 2: Free walk settings (media_1792571536355_f3b48b21.jpg)
im2 = Image.open(f"{raw_dir}/media_1792571536355_f3b48b21.jpg")
apply_mosaic(im2, (0, 0, 471, 50), 10) # Status bar
im2.save(f"{out_dir}/geosim-area-roam-step2-free-walk.jpg", quality=95)

# Step 3: Full coverage settings (media_1792571540464_7ed20b41.jpg)
im3 = Image.open(f"{raw_dir}/media_1792571540464_7ed20b41.jpg")
apply_mosaic(im3, (0, 0, 471, 50), 10) # Status bar
im3.save(f"{out_dir}/geosim-area-roam-step3-full-coverage.jpg", quality=95)

# Step 4: Running state (media_1792571527494_87d8aace.jpg)
im4 = Image.open(f"{raw_dir}/media_1792571527494_87d8aace.jpg")
apply_mosaic(im4, (0, 0, 471, 50), 10) # Status bar
im4.save(f"{out_dir}/geosim-area-roam-step4-running.jpg", quality=95)

print("Saved all 4 clean area roam screenshots with status bar mosaic!")
