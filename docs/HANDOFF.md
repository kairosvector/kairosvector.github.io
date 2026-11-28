# Kairos Vector 專案 AI 營運維運與交接白皮書 (HANDOFF.md)

> **致接管本專案的 AI Agent**：  
> 本文件是本專案的最高維運規範與交接手冊。當您接管此專案時，請先通讀本手冊，嚴格遵守既定閥值、流程規範與溝通風格。

---

## 1. 專案核心使命與架構 (Mission & Architecture)

- **專案定位**：Kairos Vector Studio 官方網站，提供 **GeoSim 虛擬漫遊工具** 與 **皮克敏台灣官方活動地圖（全家便利商店、CoCo都可門市）** 等 Web 服務。
- **技術棧架構**：
  - 前端靜態生成：**Astro** (`app/src/pages/`, `app/src/layouts/`)
  - 資料庫 / 靜態資料：JSON / CSV 格式存放在 `app/src/data/` 與 `app/public/events/`
  - 自動化巡檢工具：Python 3 (`tools/patrol_manager.py`)
  - 雲端託管：**Cloudflare Pages** (`kairosvector`)
  - 原始碼版本控制：**GitHub 雙遠端主分支** (`kevycheng` + `kairosvector.github.io`)

---

## 2. 核心維運系統：全家 / CoCo 門市自動巡檢 (Patrol Engine)

專案配備自動巡檢腳本 `tools/patrol_manager.py`，串接 Google 表單（GAS API）收集玩家群眾回報並自動決策：

### 🎯 核心演算法與安全閥值（不可妥協的紅線）：
1. **坐標微調判定**：
   - 距離 $\le 500\text{ m}$：視為現場 GPS 精度微調，**自動更新坐標並自動編譯發布**。
   - 距離 $> 500\text{ m}$：安全攔截為「異常待確認項目」，絕不自動發布，需呈報負責人手動核准。
2. **歇業門市批次下架門檻**：
   - 累積滿 **5 筆**，或最舊歇業回報等待超過 **1 小時（3600 秒）**，自動觸發下架、遞增批次號碼、編譯發布。
3. **現場問題語意辨識**：
   - 表單回報「現場問題」中，若備註含有 `無全家`、`沒有`、`找不到`、`撤櫃`、`已關`、`拆除`、`空屋`、`不存在` 等關鍵字，自動導流至歇業緩衝佇列處理。
4. **定時巡檢排程**：
   - 目前排程為 **每日一次**（UTC 00:00 = 台灣時間 08:00 自動執行 `python tools/patrol_manager.py`）。
   - 若伺服器重啟導致排程中斷，請使用 `schedule` 工具以 Cron `0 0 * * *` 重啟。

---

## 3. GeoSim 每周精選專欄架構 (Weekly Featured Engine)

- **資料庫**：`app/src/data/locations.json`（保留全部 15 期，第 1～14 期 + 龍貓特別企劃，近 300 處精美明信片景點）。
- **當前版本**：
  - 正式版 (Product / Latest)：`issue-13`（瑪利歐特輯）
  - 預覽版 (Staging)：`issue-14`（咖啡店特輯）
- **歷期巡檢切換器 (Issue Navigator)**：
  - 頂部導航列包含：上一期/下一期按鈕、15 期完整下拉選單、歷期專欄庫快捷鈕。
  - 底部包含往期導覽卡片與總覽入口。
- **App 內嵌模式適配 (`?embed=true`)**：
  - Android App WebView 透過 `?embed=true` 載入，去除頂部網頁 Nav 與頁尾，呈現純原生質感。
  - 所有期數切換連結會自動維持 `?embed=true`，確保玩家不跳出 App 視圖。
  - 一鍵直傳座標支援 `window.AndroidGeoSim.setCoordinate(lat, lng, name)`。

---

## 4. 常用維運指令手冊 (Runbook)

```bash
# 1. 執行即時門市巡檢（自動檢查、套用、生成頁面並發布）
python tools/patrol_manager.py

# 2. 手動編譯 Astro 靜態網站
npm --prefix app run build

# 3. 手動部署至 Cloudflare Pages 正式環境
npx wrangler pages deploy app/dist --project-name kairosvector --commit-dirty=true

# 4. 同步推送至 GitHub 雙遠端主分支 (kevycheng + kairosvector.github.io)
git add app/public/events/ app/src/data/ app/src/pages/ tools/data/
git commit -m "feat/fix: <簡短說明>"
git push origin main
```

---

## 5. 當前系統狀態與待辦清單 (Current State & Queue)

- **全家台北市門市總數**：**663 店**（最新 Batch #29）
- **CoCo 都可門市總數**：**356 店**（最新 Batch #42）
- **保留待確認項目（目前安全攔截中，等待負責人指示）**：
  1. `台北松指部店`（松山區民權東路四段121號）：回報深入營區福利社坐標 `25.06314, 121.56083`，偏移 515m。
  2. `台北台大楓林店`（大安區羅斯福路四段1號）：回報女九餐廳實際坐標 `25.01968, 121.53922`，偏移 633m（原坐標為校園正門）。
- **待辦目標**：
  - 等候負責人確認上述 2 間園區型門市是否手動核准更新。
  - 每日早上 08:00 巡檢若有新回報，維持極簡手機版速報回報。

---

## 6. 溝通與回報風格守則 (Communication Style)

1. **極精簡手機版速報**：使用者主要在手機端閱讀，一律使用繁體中文、條列式重點、清晰標註門市與微調距離。
2. **無異動時靜默**：定時巡檢如果沒有新回報或已全數自動過濾，僅回報一句一行狀態即可，不打擾使用者。
3. **安全第一**：未經確認前絕不擅自手動修改門市資料或突破 500m 安全線。
