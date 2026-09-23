# Kairos Vector Studio — Official Website

Kairos Vector Studio 官方網站，介紹旗下實用 Android 應用程式（PikieWalker、GeoSim）與全球純點地圖庫。

---

## 🌟 核心特色

- **官方幾何品牌識別 (Official KV Monogram)**：整合立體純白「K」與發光青藍向量「V」標誌，搭配雙主題（🌙 暗夜極客預設 / ⚡ 活力電氣）。
- **Google Play 合規與法律保障**：包含獨立隱私權政策 (`/privacy`)、服務條款與免責聲明 (`/terms`)，完整符合 Health Connect 與 GPS 模擬之審查規範。
- **純點地圖庫與每周精選**：
  - `40+` 種純點分類多選標籤、國家 / 縣市 / 行政區三級聯動篩選、即時座標一鍵複製。
  - 每周精選主題路線 (`/geosim/weekly-featured`) 與推薦巡航時速建議。
- **實用技巧專欄部落格 (`/tips/[slug]`)**：收錄 8 篇深度教學文章，附帶麵包屑、重點提示盒與 Google Play 下載推薦。
- **超高速 SEO 引擎 (Astro SSG)**：
  - 自動生成 `sitemap.xml` 與 `robots.txt`。
  - 內建 Schema.org JSON-LD 結構化資料。
  - 16 個靜態頁面編譯僅需 ~1 秒。
- **一鍵自動化部署 (GitHub Pages)**：已配置 `.github/workflows/deploy.yml`。

---

## 🚀 本地開發

```bash
# 進入前端目錄
cd app

# 安裝相依套件
npm install

# 啟動開發伺服器
npm run dev

# 建置靜態檔案
npm run build
```

---

## 📦 部署至 GitHub Pages

專案已內建 GitHub Actions 自動化部署工作流程。只要將程式碼推送到 GitHub：

```bash
git add .
git commit -m "feat: complete production launch readiness with privacy, terms, and sitemap"
git push origin main
```

GitHub Actions 會自動執行 Astro 編譯並部署至 GitHub Pages。
