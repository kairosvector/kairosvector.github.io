import os
from PIL import Image, ImageFilter
import numpy as np

def make_phone_transparent(input_path, output_path, brightness_thresh=225):
    img = Image.open(input_path).convert('RGBA')
    arr = np.array(img)
    
    # Extract RGB channels
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # Calculate luminance / brightness
    # Formula: 0.299 R + 0.587 G + 0.114 B
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    
    # Create mask of background candidate (bright pixels)
    # The phone body has dark metal edges (< 180 brightness)
    bg_candidate = (brightness > brightness_thresh)
    
    # Floodfill from borders to only select background connected to image boundary
    from scipy.ndimage import binary_fill_holes, label
    
    # Label connected components of background
    labeled, num_features = label(bg_candidate)
    
    # Find which labels touch the outer boundary
    boundary_labels = set()
    boundary_labels.update(np.unique(labeled[0, :]))
    boundary_labels.update(np.unique(labeled[-1, :]))
    boundary_labels.update(np.unique(labeled[:, 0]))
    boundary_labels.update(np.unique(labeled[:, -1]))
    if 0 in boundary_labels:
        boundary_labels.remove(0)
        
    is_outer_bg = np.isin(labeled, list(boundary_labels))
    
    # Soft alpha feathering on the edges for smooth anti-aliased cutout
    alpha_mask = np.where(is_outer_bg, 0, 255).astype(np.uint8)
    
    # Create feathered alpha
    mask_img = Image.fromarray(alpha_mask, mode='L')
    # Slight smooth blur
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=0.8))
    
    # Combine back
    img.putalpha(mask_img)
    
    # Crop unnecessary bounding box if any
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(output_path, 'PNG', optimize=True)
    print(f"Saved clean transparent PNG to {output_path} with size {img.size}")

if __name__ == '__main__':
    os.makedirs('app/public/images', exist_ok=True)
    make_phone_transparent('rc/ChatGPT Image 2026年8月25日 14_30_21.png', 'app/public/images/geosim-mockup.png', brightness_thresh=220)
    make_phone_transparent('rc/ChatGPT Image 2026年8月25日 14_42_29.png', 'app/public/images/pikiewalker-mockup.png', brightness_thresh=220)
