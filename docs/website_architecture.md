# Kairos Vector Studio — Website Architecture

## 1. Overview & Technology Stack

- **Framework:** [Astro](https://astro.build/) (Static Site Generation / SSG)
- **Styling:** Vanilla CSS Custom Properties (Design Token System with Cyber Dark & Electric Prism)
- **Fonts:** Space Grotesk + Noto Sans TC via Google Fonts
- **Deployment:** Cloudflare Pages (https://kairosvector.pages.dev/); docs historically mentioned GitHub Pages / Actions

---

## 2. Directory Structure

```
kairosVector_web/
├── app/
│   ├── public/
│   │   └── favicon.svg                  # Studio SVG favicon
│   ├── src/
│   │   ├── data/
│   │   │   ├── products.json            # Data-driven product definitions
│   │   │   ├── tips.json                # Blog tutorial guide articles repository
│   │   │   └── locations.json           # Weekly Featured & Spot Map database
│   │   ├── layouts/
│   │   │   └── BaseLayout.astro         # Global layout (Nav, Footer, SEO, Theme Switcher)
│   │   ├── pages/
│   │   │   ├── index.astro              # Studio homepage
│   │   │   ├── pikiewalker.astro        # PikieWalker product page + Blog hub
│   │   │   ├── geosim.astro             # GeoSim product page + Blog hub + Location hub
│   │   │   ├── geosim/
│   │   │   │   ├── story.astro          # 📖 《GeoSim 的一天》開發者深度實戰手記專頁
│   │   │   │   ├── weekly-featured/
│   │   │   │   │   ├── index.astro      # 🌟 每周精選專欄總覽
│   │   │   │   │   └── [issue].astro    # 單期詳情（含特別企劃）
│   │   │   │   └── spot-map.astro       # 🗺️ GeoSim 純點地圖庫專頁
│   │   │   └── tips/
│   │   │       └── [slug].astro         # Dynamic full-length blog article template (11 guides: 3 新手入門 + 8 進階技巧)
│   │   └── styles/
│   │       └── global.css               # Cyber Dark & Electric Prism design system
│   ├── dist/                            # Production build artifacts
│   ├── astro.config.mjs
│   ├── package.json
│   └── tsconfig.json
├── .github/
│   └── workflows/
│       └── deploy.yml                   # Automated GitHub Pages workflow
└── docs/
    ├── design_system.md                 # Visual specification & tokens
    └── website_architecture.md          # Architectural documentation
```

---

## 3. GeoSim 專屬頁面架構

### 1. 《GeoSim 的一天》實戰手記 (`/geosim/story`)
- **定位：** 專為 Android 開發者打造的情境敘事與深度技術白皮書。
- **特點：**
  - 時間軸小說體裁（09:00 至 23:00 共 8 幕場景）。
  - 動態純 SVG 五點折線雷達波動畫與即時狀態丸（模擬中 / 凍結偵測）。
  - 完整盤點 GPS / NETWORK / Fused 三來源注入、Haversine 調速、兩層書籤、GPX 抽稀、懸浮搖桿、Health Connect 步數換算等 30+ 項殺手級功能與合規邊界聲明。
  - 完美相容 Cyber Dark 與 Electric Prism 雙主題。

### 2. 每周精選專頁 (`/geosim/weekly-featured`)
- **定位：** 定期策劃的主題式探索路線；另含不定期「特別企劃」（例如吉卜力龍貓與貓巴士）。
- **路由：** `/geosim/weekly-featured` 總覽；`/geosim/weekly-featured/<id>` 單期（例：`issue-05`、`special-totoro`）。
- **資料：** `app/src/data/locations.json` → `weeklyFeatured`（陣列第 0 筆為最新主打）。
- **特點：** 景點微故事、推薦巡航速率、精確經緯度、一鍵複製座標、社群轉發文案、往期回顧。

### 3. 純點地圖庫專頁 (`/geosim/spot-map`)
- **定位：** 全球熱門經緯度座標總庫。
- **特點：** 支援分類標籤切換（都市地標、文化/景點、大型綠地、交通樞紐）、即時座標一鍵複製、Google 地圖預覽連結，以及「如何將座標匯入 GeoSim」步驟指引。

---

## 4. 如何新增更多地點或每周期刊
- **每周精選：** 於 `app/src/data/locations.json` 中的 `weeklyFeatured` 陣列新增一期期刊物件（一般期用 `issue-NN`；特別企劃用 `special-*`，例如 `special-totoro`）。陣列順序：最新在前。
- **純點地圖：** 於 `app/src/data/locations.json` 中的 `spots` 陣列新增地點資料。
- 系統建置時會自動靜態編譯並更新相關頁面！
