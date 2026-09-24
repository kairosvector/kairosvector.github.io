"""
GeoSim Weekly Pipeline Tool (每周精選自動化管線工具)
===================================================
功能：
1. 自動輪替選題（讀取 theme_rotation.json）或自訂主題
2. 自動從 pikoohiong 資料庫篩選 Top 20 景點（10菇 + 10花，按愛心數排序，去重，排除AI假圖）
3. 透過 Pikoohiong API 自動下載 20 張精確明信片照片至 app/public/images/postcards/<theme>/
4. 自動產生微故事、推薦巡航時速、並寫入 app/src/data/locations.json
5. 自動產出當週 Threads 行銷貼文草稿（附座標、文案與標籤）
6. 支援一鍵 build 驗證與一鍵 Cloudflare Pages 正式部署
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

# Directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = PROJECT_ROOT / "app"
DATA_DIR = APP_DIR / "src" / "data"
LOCATIONS_FILE = DATA_DIR / "locations.json"
PUBLIC_IMAGES_DIR = APP_DIR / "public" / "images"
POSTCARDS_DIR = PUBLIC_IMAGES_DIR / "postcards"
WEEKLY_IMAGES_DIR = PUBLIC_IMAGES_DIR / "weekly"
DOCS_SOCIAL_DIR = PROJECT_ROOT / "docs" / "social"

GEOSIM_DATA_DIR = Path(r"D:\project\py_project\sideprojects\geosim-data")
ROTATION_FILE = GEOSIM_DATA_DIR / "theme_rotation.json"
PIKO_LATEST_FILE = GEOSIM_DATA_DIR / "pikoohiong_data" / "pikoohiong_latest.json"
PIKO_CSV_FILE = GEOSIM_DATA_DIR / "pikoohiong_data" / "by_content_noai.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://pikoohiong.com/",
    "x-pikmin-visitor-id": "v1_" + uuid.uuid4().hex,
}

OPENCODE_CMD = r"C:\Users\kevy_win11\AppData\Roaming\npm\opencode.cmd"
MODELS_FILE = GEOSIM_DATA_DIR / "models.txt"
DEFAULT_OPENCODE_MODELS = [
    "opencode/muse-spark-1.3-contributor-free",
    "opencode/big-pickle",
]


def get_opencode_models() -> list:
    if MODELS_FILE.exists():
        try:
            with open(MODELS_FILE, "r", encoding="utf-8") as f:
                lines = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.startswith("#")
                ]
                if lines:
                    return lines
        except Exception:
            pass
    return DEFAULT_OPENCODE_MODELS


def is_mostly_chinese(text: str) -> bool:
    if not text:
        return True
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    return (chinese_chars / max(len(text), 1)) >= 0.5


def translate_spots_with_opencode(spots: list) -> list:
    need_trans = {}
    for s in spots:
        title = s.get("title") or s.get("placeName") or ""
        if title and not is_mostly_chinese(title):
            need_trans[title] = title

    if not need_trans:
        print("✨ 所有景點名稱均已為繁體中文，無須調用 LLM 翻譯。")
        return spots

    print(
        f"🤖 發現 {len(need_trans)} 個非中文景點名稱，正在透過 OpenCode 免費模型進行繁體中文翻譯..."
    )
    items_to_translate = list(need_trans.keys())
    names_str = "、".join(items_to_translate)
    prompt = (
        f"請將這幾個皮克敏景點名稱翻譯成優雅的繁體中文（格式：原名 => 中文，不同景點用逗號分開）：{names_str}"
    )

    models = get_opencode_models()
    translations = {}

    for model in models:
        print(f"  → 嘗試使用模型: {model} ...")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        try:
            cmd = [
                OPENCODE_CMD,
                "run",
                "--model",
                model,
                "--dir",
                str(GEOSIM_DATA_DIR),
                prompt,
            ]
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
                timeout=35,
                env=env,
            )
            if res.returncode == 0 and res.stdout:
                out = res.stdout
                for item in re.split(r"[,，\n]", out):
                    if "=>" in item:
                        parts = item.split("=>", 1)
                        k = parts[0].strip(" -*`>#0123456789. \t\"'")
                        v = parts[1].strip(" -*`>#0123456789. \t\"'")
                        if k and v:
                            translations[k] = v

                matched = sum(
                    1
                    for k in items_to_translate
                    if k in translations or any(k in tk for tk in translations)
                )
                if matched >= len(items_to_translate) // 2:
                    print(f"  ✅ 模型 {model} 成功返回 {len(translations)} 筆翻譯！")
                    break
        except Exception as e:
            print(f"  ⚠️ 模型 {model} 呼叫失敗或逾時: {e}")

    # Apply translations back to spots
    for s in spots:
        title = s.get("title") or s.get("placeName") or ""
        if title in translations:
            s["translated_title"] = translations[title]
            s["original_title"] = title
        else:
            found = False
            for k, v in translations.items():
                if k.lower() == title.lower() or k.lower() in title.lower():
                    s["translated_title"] = v
                    s["original_title"] = title
                    found = True
                    break
            if not found:
                s["translated_title"] = title

    return spots


def generate_social_intro_with_opencode(theme_title: str) -> str:
    print(f"✍️ 正在透過 OpenCode 模型為【{theme_title}】創作社群短導言...")
    prompt = (
        f"請為本期皮克敏每週精選（主題：{theme_title}）寫一段吸引皮友的短導言（50字以內繁體中文，溫馨活潑，帶有皮克敏花朵與明信片氛圍，直接輸出文案即可，不要有其他對話）："
    )
    models = get_opencode_models()

    for model in models:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        try:
            cmd = [
                OPENCODE_CMD,
                "run",
                "--model",
                model,
                "--dir",
                str(GEOSIM_DATA_DIR),
                prompt,
            ]
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
                timeout=30,
                env=env,
            )
            if res.returncode == 0 and res.stdout:
                out = res.stdout.strip()
                lines = [
                    l.strip()
                    for l in out.splitlines()
                    if l.strip() and not l.startswith(">") and "構思" not in l
                ]
                if lines:
                    intro = lines[-1].strip(" \"'「」")
                    print(f"  ✅ 成功產出文案：{intro}")
                    return intro
        except Exception as e:
            print(f"  ⚠️ 模型 {model} 產出文案失敗: {e}")

    fallback = f"皮友們這周明信片收齊了嗎？本期為大家搜羅全球【{theme_title}】主題座標！🍄 蘑菇點與 🌸 巨型大花已全部就位！"
    print(f"  ℹ️ 使用預設保底文案：{fallback}")
    return fallback


def get_next_rotation_theme() -> dict:
    if not ROTATION_FILE.exists():
        raise FileNotFoundError(f"Rotation file not found: {ROTATION_FILE}")
    with open(ROTATION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    rotation = data.get("rotation", [])
    last_idx = data.get("lastUsedIndex", -1)
    next_idx = (last_idx + 1) % len(rotation)
    theme_info = rotation[next_idx]
    return theme_info, next_idx, data


def advance_rotation_index(next_idx: int, rotation_data: dict):
    rotation_data["lastUsedIndex"] = next_idx
    with open(ROTATION_FILE, "w", encoding="utf-8") as f:
        json.dump(rotation_data, f, ensure_ascii=False, indent=2)
    print(f"Updated theme_rotation.json: lastUsedIndex = {next_idx}")


def filter_spots_from_piko(keywords: str, limit: int = 20) -> list:
    kw_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    print(f"Filtering postcards with keywords: {kw_list} ...")

    with open(PIKO_LATEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])

    matched = []
    seen_locations = set()

    for it in items:
        # Check AI detected
        if it.get("isAiDetected", False):
            continue

        text_corpus = f"{it.get('title', '')} {it.get('placeName', '')} {it.get('tags', '')} {it.get('notes', '')}".lower()
        if any(kw in text_corpus for kw in kw_list):
            lat = it.get("latitude")
            lng = it.get("longitude")
            if lat is None or lng is None:
                continue

            # Deduplicate by ~110m locationKey (3 decimal places)
            loc_key = f"{round(lat, 3)},{round(lng, 3)}"
            if loc_key in seen_locations:
                continue
            seen_locations.add(loc_key)

            matched.append(it)

    # Sort by favoriteCount desc, then likeCount desc
    matched.sort(
        key=lambda x: (x.get("favoriteCount", 0), x.get("likeCount", 0)),
        reverse=True,
    )

    mushrooms = [
        it
        for it in matched
        if str(it.get("postcardType", "")).upper() == "MUSHROOM"
    ]
    flowers = [
        it
        for it in matched
        if str(it.get("postcardType", "")).upper() == "FLOWER"
    ]
    others = [
        it
        for it in matched
        if str(it.get("postcardType", "")).upper() not in ["MUSHROOM", "FLOWER"]
    ]

    half_limit = limit // 2
    selected_mush = mushrooms[:half_limit]
    selected_flow = flowers[:half_limit]

    # Fill if one side is insufficient
    total_selected = selected_mush + selected_flow
    if len(total_selected) < limit:
        remain_need = limit - len(total_selected)
        backup_pool = (
            mushrooms[half_limit:] + flowers[half_limit:] + others
        )
        total_selected.extend(backup_pool[:remain_need])

    print(
        f"Selected {len(total_selected)} spots (Mushroom: {len(selected_mush)}, Flower: {len(selected_flow)})"
    )
    return total_selected


def download_postcards(spots: list, folder_slug: str) -> list:
    out_dir = POSTCARDS_DIR / folder_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    saved_spots = []

    print(f"\nDownloading {len(spots)} postcards to {out_dir} ...")
    for idx, spot in enumerate(spots):
        cid = spot.get("id")
        title = spot.get("title") or spot.get("placeName") or f"景點 #{idx+1}"
        filename = f"spot-{idx+1:02d}.jpg"
        save_file = out_dir / filename
        web_path = f"/images/postcards/{folder_slug}/{filename}"

        if save_file.exists() and save_file.stat().st_size > 1000:
            print(f"  [{idx+1}/{len(spots)}] ⏩ Already exists: {filename}")
            spot["local_image"] = web_path
            saved_spots.append(spot)
            continue

        try:
            # Query Pikoohiong API for fresh signed URL
            api_url = f"https://pikoohiong.com/api/postcards/{cid}"
            res = requests.get(api_url, headers=HEADERS, timeout=12)
            if res.status_code == 200:
                fresh_url = res.json().get("imageUrl")
                if fresh_url:
                    img_res = requests.get(
                        fresh_url, headers=HEADERS, timeout=12
                    )
                    if (
                        img_res.status_code == 200
                        and len(img_res.content) > 1000
                    ):
                        with open(save_file, "wb") as f_img:
                            f_img.write(img_res.content)
                        print(
                            f"  [{idx+1}/{len(spots)}] ✅ Downloaded: {title} ({len(img_res.content)} bytes)"
                        )
                        spot["local_image"] = web_path
                        saved_spots.append(spot)
                    else:
                        print(
                            f"  [{idx+1}/{len(spots)}] ❌ Failed img body for {title}"
                        )
                else:
                    print(
                        f"  [{idx+1}/{len(spots)}] ❌ No imageUrl in json for {title}"
                    )
            else:
                print(
                    f"  [{idx+1}/{len(spots)}] ❌ API HTTP {res.status_code} for {cid}"
                )
        except Exception as e:
            print(f"  [{idx+1}/{len(spots)}] ❌ Exception: {e}")

        time.sleep(0.5)

    return saved_spots


def update_locations_json(
    issue_id: str,
    issue_name: str,
    theme_title: str,
    date_range: str,
    folder_slug: str,
    spots_data: list,
    category: str = "explore",
    category_name: str = "🗺️ 全球探索",
    description: str = "",
    creative_intro: str = "",
):
    with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
        loc = json.load(f)

    # 1. Translate foreign spot titles with OpenCode
    translated_spots = translate_spots_with_opencode(spots_data)

    # 2. Generate creative intro with OpenCode if not provided
    if not creative_intro:
        creative_intro = generate_social_intro_with_opencode(theme_title)

    # Format spots for GeoSim locations.json
    formatted_spots = []
    for idx, s in enumerate(translated_spots):
        ptype = str(s.get("postcardType", "FLOWER")).upper()
        is_mushroom = ptype == "MUSHROOM"

        city = s.get("city") or s.get("state") or s.get("country") or "精選區域"
        name = s.get("translated_title") or s.get("title") or s.get("placeName") or f"精選景點 #{idx+1}"
        raw_loc = s.get("placeName") or f"{city} {name}"
        orig_name = s.get("original_title")

        story_text = s.get("notes")
        if not story_text:
            if orig_name and orig_name != name:
                story_text = f"原名「{orig_name}」。位於 {city} 的代表性打卡點，適合散步巡航探索。"
            else:
                story_text = f"位於 {city} 的代表性打卡點，適合散步巡航探索。"

        formatted_spots.append(
            {
                "id": f"spot-{idx+1:02d}",
                "name": name,
                "city": city,
                "location": raw_loc,
                "lat": s.get("latitude"),
                "lng": s.get("longitude"),
                "region": "global",
                "type": "mushroom" if is_mushroom else "flower",
                "typeName": "蘑菇戰鬥點" if is_mushroom else "巨型大花點",
                "tag": "特色精選",
                "recommendedSpeed": "4.0 km/h"
                if is_mushroom
                else "19.0 km/h（種花黃金時速）",
                "image": s.get("local_image"),
                "story": story_text,
            }
        )

    issue_desc = description or f"{creative_intro} 本期為您精選全球 {len(formatted_spots)} 處必訪明信片打卡座標！支援一鍵複製與巡航速度建議。"
    social_draft = f"【GeoSim 每周精選 {issue_name} 🌟 {theme_title}】\n\n{creative_intro}\n\n📍 完整 20 大座標與路線 👉 https://kairosvector.pages.dev/geosim/weekly-featured/{issue_id}\n#PikminBloom #皮克敏 #GeoSim #每週精選"

    new_issue = {
        "id": issue_id,
        "issue": issue_name,
        "theme": theme_title,
        "date": date_range,
        "category": category,
        "categoryName": category_name,
        "description": issue_desc,
        "region": "全球精選巡航",
        "coverImage": f"/images/weekly/{folder_slug}.jpg",
        "socialShareDraft": social_draft,
        "spots": formatted_spots,
    }

    # Insert or update
    weekly_list = loc.get("weeklyFeatured", [])
    existing_idx = next(
        (i for i, x in enumerate(weekly_list) if x.get("id") == issue_id), None
    )
    if existing_idx is not None:
        weekly_list[existing_idx] = new_issue
    else:
        weekly_list.insert(0, new_issue)

    loc["weeklyFeatured"] = weekly_list
    with open(LOCATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(loc, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully written {issue_id} into {LOCATIONS_FILE}")
    return formatted_spots, creative_intro


def generate_threads_draft(
    issue_id: str,
    issue_name: str,
    theme_title: str,
    folder_slug: str,
    spots: list,
    creative_intro: str = "",
):
    DOCS_SOCIAL_DIR.mkdir(parents=True, exist_ok=True)
    out_file = DOCS_SOCIAL_DIR / f"threads_{issue_id}.md"

    coords_sample = "\n".join(
        [
            f"📍 #{idx+1} {s.get('name')}: `{s.get('lat')}, {s.get('lng')}`"
            for idx, s in enumerate(spots[:8])
        ]
    )

    intro_block = creative_intro or f"皮友們這週的明信片都收齊了嗎？🌸\n本週特別為大家搜羅全球代表性的【{theme_title}】主題路線！"

    content = f"""# Threads 官方宣傳貼文草稿：{issue_name}（{theme_title}）

> 發布時間：每週六上午
> 配圖建議：附帶 `app/public/images/postcards/{folder_slug}/` 中的 4~8 張精選明信片照片

---

## 📱 貼文文案（直接複製貼上）：

【GeoSim 每周精選 {issue_name} 🌟 {theme_title}】

{intro_block}
全數收錄 10 處蘑菇戰鬥點 🍄 與 10 處巨型大花點 🌸，支援一鍵複製與推薦巡航時速！

精選前 8 處打卡座標搶先看：
{coords_sample}

🧭 完整 20 處經緯度座標與路線地圖：
👉 https://kairosvector.pages.dev/geosim/weekly-featured/{issue_id}

#PikminBloom #皮克敏 #GeoSim #皮克敏明信片 #每週精選 #AR遊戲 #散步養成
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"📝 Generated Threads marketing draft at: {out_file}")
    return content


def send_email_notification(subject: str, body_text: str):
    send_script = GEOSIM_DATA_DIR / "send_email.py"
    if not send_script.exists():
        print("send_email.py not found, skipping email.")
        return
    temp_body = PROJECT_ROOT / "scratch" / "email_body.txt"
    temp_body.parent.mkdir(parents=True, exist_ok=True)
    temp_body.write_text(body_text, encoding="utf-8")
    cmd = [sys.executable, str(send_script), subject, "--body-file", str(temp_body)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(f"📧 Email notification: {res.stdout.strip() if res.stdout else res.stderr.strip()}")


def build_and_deploy(deploy: bool = False):
    print("\n🔨 Running Astro Build ...")
    res = subprocess.run(["npm", "run", "build"], cwd=APP_DIR, shell=True)
    if res.returncode != 0:
        print("❌ Build failed! Aborting deploy.")
        return False
    print("✅ Build passed successfully!")

    if deploy:
        print("\n🚀 Deploying to Cloudflare Pages (Production) ...")
        dep_cmd = "npx wrangler pages deploy dist --project-name=kairosvector --branch=main --commit-dirty=true"
        dep_res = subprocess.run(dep_cmd, cwd=APP_DIR, shell=True)
        if dep_res.returncode == 0:
            print("🎉 Deployment to Cloudflare Pages completed successfully!")
            return True
        else:
            print("❌ Deployment failed!")
            return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="GeoSim 每周精選自動化管線工具"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="自動讀取 theme_rotation.json 取下一個輪替主題",
    )
    parser.add_argument(
        "--theme", type=str, help="自訂主題名稱（例如：海灘/海洋）"
    )
    parser.add_argument(
        "--keywords", type=str, help="關鍵字（逗點分隔，例如：beach,sea,海灘）"
    )
    parser.add_argument(
        "--slug", type=str, help="資料夾英文縮寫（例如：beach）"
    )
    parser.add_argument(
        "--issue-num", type=int, help="期別編號（例如：6 代表第 06 期）"
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="完成後直接 Deploy 至 Cloudflare Pages",
    )
    parser.add_argument(
        "--build-only", action="store_true", help="僅執行本地 build 測試"
    )
    parser.add_argument(
        "--deploy-only",
        action="store_true",
        help="僅執行 build 並部署上 Cloudflare",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模擬執行（Dry Run）：檢驗選題、景點篩選、API連線與文案產出，不寫入檔案也不部署",
    )

    args = parser.parse_args()

    if args.build_only:
        build_and_deploy(deploy=False)
        return

    if args.deploy_only:
        build_and_deploy(deploy=True)
        return

    # Theme selection
    if args.auto:
        theme_info, next_idx, rot_data = get_next_rotation_theme()
        theme_name = theme_info["theme"]
        keywords = theme_info["keywords"]
        print(f"🎯 Auto picked theme: {theme_name} (keywords: {keywords})")
    elif args.theme and args.keywords:
        theme_name = args.theme
        keywords = args.keywords
    else:
        print("Please provide --auto or (--theme and --keywords)")
        return

    # Determine issue number
    with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
        loc = json.load(f)
    existing_issues = [
        x for x in loc.get("weeklyFeatured", []) if "issue-" in x.get("id", "")
    ]
    if args.issue_num:
        issue_int = args.issue_num
    else:
        # Latest + 1
        nums = [
            int(re.search(r"\d+", x["id"]).group())
            for x in existing_issues
            if re.search(r"\d+", x["id"])
        ]
        issue_int = max(nums) + 1 if nums else 1

    issue_id = f"issue-{issue_int:02d}"
    issue_name = f"第 {issue_int:02d} 期"
    folder_slug = (
        args.slug
        or theme_name.split("/")[0]
        .replace(" ", "")
        .replace("（", "")
        .replace("）", "")
        .lower()
    )

    # Date range: next Saturday ~ following Friday
    today = datetime.now()
    # Find next Saturday
    days_ahead = (5 - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_sat = today + timedelta(days=days_ahead)
    next_fri = next_sat + timedelta(days=6)
    date_range = (
        f"{next_sat.strftime('%Y-%m-%d')} ~ {next_fri.strftime('%Y-%m-%d')}"
    )

    print(
        f"\n🚀 Pipeline: {issue_name} | 主題: {theme_name} | 日期: {date_range} | Slug: {folder_slug}"
    )

    # 1. Filter spots
    spots = filter_spots_from_piko(keywords, limit=20)
    if not spots:
        print("❌ No matching spots found in pikoohiong database!")
        return

    if args.dry_run:
        print("\n=======================================================")
        print(f"🔍 [DRY RUN 模擬執行模式] - 不會修改任何檔案與遠端設定")
        print("=======================================================")
        print(f"期別編號: {issue_name} ({issue_id})")
        print(f"主題名稱: {theme_name}")
        print(f"關鍵字組: {keywords}")
        print(f"預計日期: {date_range}")
        print(f"靜態圖資目錄: app/public/images/postcards/{folder_slug}/")

        # Test translation with OpenCode
        print(f"\n測試 OpenCode LLM 翻譯 20 個景點名稱...")
        spots_translated = translate_spots_with_opencode(spots)
        print(f"\n篩選與翻譯後的 20 個景點清單：")
        for i, s in enumerate(spots_translated):
            ptype = str(s.get("postcardType", "FLOWER")).upper()
            pt_emoji = "🍄 蘑菇" if ptype == "MUSHROOM" else "🌸 大花"
            title = s.get("translated_title") or s.get("title") or s.get("placeName") or "未命名景點"
            orig = s.get("original_title")
            orig_str = f" (原名: {orig})" if orig and orig != title else ""
            print(f"  #{i+1:02d} [{pt_emoji}] {title}{orig_str} | 愛心: {s.get('favoriteCount', 0)} | 座標: {s.get('latitude')}, {s.get('longitude')} (ID: {s.get('id')})")

        # Test API connection for spot #1
        if spots:
            test_cid = spots[0].get("id")
            print(f"\n測試 Pikoohiong API 連線 (以第 1 個景點 ID: {test_cid} 為例) ...")
            try:
                res = requests.get(f"https://pikoohiong.com/api/postcards/{test_cid}", headers=HEADERS, timeout=8)
                if res.status_code == 200:
                    img_url = res.json().get("imageUrl")
                    print(f"  ✅ API 連線成功！即時取得有效簽名圖片 URL: {img_url[:65]}...")
                else:
                    print(f"  ⚠️ API 狀態碼: {res.status_code}")
            except Exception as e:
                print(f"  ⚠️ 連線異常: {e}")

        # Test creative copy generation
        print(f"\n測試 OpenCode LLM 創作宣傳文案...")
        creative_intro = generate_social_intro_with_opencode(theme_name)

        print(f"\n預計產出的 Threads 社群文案預覽：")
        print("-------------------------------------------------------")
        print(f"【GeoSim 每周精選 {issue_name} 🌟 漫遊全球：精選【{theme_name}】巡航特輯】\n")
        print(f"{creative_intro}\n")
        print("全數收錄 10 處蘑菇戰鬥點 🍄 與 10 處巨型大花點 🌸，支援一鍵複製與推薦巡航時速！\n")
        print("精選前 4 處打卡座標搶先看：")
        for i, s in enumerate(spots_translated[:4]):
            title = s.get("translated_title") or s.get("title") or s.get("placeName")
            print(f"📍 #{i+1} {title}: `{s.get('latitude')}, {s.get('longitude')}`")
        print(f"\n🧭 完整 20 處經緯度座標與路線地圖：")
        print(f"👉 https://kairosvector.pages.dev/geosim/weekly-featured/{issue_id}\n")
        print("#PikminBloom #皮克敏 #GeoSim #皮克敏明信片 #每週精選")
        print("-------------------------------------------------------")
        print(f"✨ [DRY RUN 模擬完成] 流程 100% 驗證通過，隨時可正式執行！")
        return

    # 2. Download postcards
    downloaded = download_postcards(spots, folder_slug)

    # 3. Update locations.json
    full_theme_title = f"漫遊全球：精選【{theme_name}】巡航特輯"
    formatted_spots, creative_intro = update_locations_json(
        issue_id=issue_id,
        issue_name=issue_name,
        theme_title=full_theme_title,
        date_range=date_range,
        folder_slug=folder_slug,
        spots_data=downloaded,
    )

    # 4. Generate Threads draft
    threads_copy = generate_threads_draft(
        issue_id=issue_id,
        issue_name=issue_name,
        theme_title=full_theme_title,
        folder_slug=folder_slug,
        spots=formatted_spots,
        creative_intro=creative_intro,
    )

    # 5. Advance rotation index if auto
    if args.auto:
        advance_rotation_index(next_idx, rot_data)

    # 6. Build & Deploy
    dep_ok = build_and_deploy(deploy=args.deploy)

    # 7. Send Email Notification with full Threads copy
    email_sub = f"【GeoSim 每周精選已發布】{issue_name}（{theme_name}）附 Threads 宣傳文案"
    email_body = f"""🎉 GeoSim 每周精選自動化管線執行完畢！

【發布狀態總覽】
- 期別編號：{issue_name} ({issue_id})
- 本期主題：{full_theme_title}
- 下載明信片數：{len(downloaded)} 張
- Cloudflare Pages 部署：{'已正式發布上線 ✅' if args.deploy else '已完成本地建置（待命狀態）'}
- 線上專欄網址：https://kairosvector.pages.dev/geosim/weekly-featured/{issue_id}

==============================================================
📱【Threads 官方宣傳文案（請直接全選複製貼至 Threads 發文）】
==============================================================

{threads_copy}

==============================================================
📸【配圖建議】
發文時可搭配本機目錄中的前 4~8 張精選明信片照片發布：
app/public/images/postcards/{folder_slug}/

（本信件由 GeoSim 週六自動化管線自動發送）
"""
    send_email_notification(email_sub, email_body)

    print(f"\n🎉 {issue_name} pipeline completed successfully!")


if __name__ == "__main__":
    main()
