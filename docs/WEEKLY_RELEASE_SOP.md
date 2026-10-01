# GeoSim 每周精選發布與維運 SOP (Production Guide)

本文件定義 GeoSim 官方專欄的 **GitHub 雙重備份機制**、**每週更新自動化流程** 與 **發布後確認清單**。

---

## 1. 系統備份架構 (GitHub Backup Architecture)

為了確保服務高可用性與資料 100% 不丟失，本專案建置了雙重託管與冷熱備援機制：

```
                              ┌───────────────────────────────────────────────┐
                              │            本地開發與更新來源                 │
                              │  (locations.json / postcards / weekly_pipeline)│
                              └──────────────────────┬────────────────────────┘
                                                     │
                          ┌──────────────────────────┴──────────────────────────┐
                          ▼                                                     ▼
              【主發布線路 (Primary)】                               【雙重備援線路 (Backup)】
                 Cloudflare Pages                                          GitHub
         (kairosvector.pages.dev)                             (github.com/kevycheng/kairosVector_web)
                          │                                                     │
                          ▼                                                     ▼
                 全球高速 Edge CDN                                       1. 程式碼與圖資全量備份
                 玩家/用戶直接存取                                       2. Release Git Tag 歷史版本保護
                                                                        3. GitHub Actions 自動建置
                                                                        4. GitHub Pages 備援站點
```

### 備份與版本控制要點：
1. **GitHub 遠端儲存庫**：`https://github.com/kevycheng/kairosVector_web.git`
2. **基線 Tag 備份**：當前穩定驗證定版已標記為 `v1.0.0-weekly-featured`。日後若有任何緊急狀況，可一鍵 rollback 至此標籤。
3. **歷史明信片與圖資儲存**：所有期別的 20 張高解析無水印明信片（`app/public/images/postcards/`）均已全量納入 Git 版本控管。
4. **GitHub Actions 自動備援（Cold Standby）**：
   - 每次推送到 `main` 分支，`.github/workflows/deploy.yml` 會自動執行 Astro 建置，並發布至 GitHub Pages。
   - 若 Cloudflare 發生全球性故障，Android App 可立即透過 `meta.json` 切換至 GitHub Pages 備援網址。

---

## 2. 每週更新流程 (Weekly Update Pipeline)

更新週期建議固定於**每週六**（配合玩家週末出遊與社群熱潮）。
更新作業已高度整合於自動化腳本：`tools/weekly_pipeline.py`。

### 推薦執行方式（三選一）：

#### 模式 A：【最推薦】先模擬驗證，再一鍵發布（安全穩健，約 3 分鐘）
```bash
# 步驟 1：Dry-Run 模擬測試（檢查選題、景點篩選、翻譯與文案，不寫入檔案）
python tools/weekly_pipeline.py --auto --dry-run

# 步驟 2：確認預覽滿意後，正式執行更新並部署
python tools/weekly_pipeline.py --auto --deploy
```

#### 模式 B：【全自動化】一鍵全自動更新（極速）
```bash
python tools/weekly_pipeline.py --auto --deploy
```
*系統將自動：輪替選題 ➔ 抓取 20 景點 ➔ OpenCode 翻譯 ➔ 下載圖片 ➔ 更新 locations.json ➔ 部署 Cloudflare ➔ Git Push 備份 ➔ 寄送 Threads 文案信。*

#### 模式 C：【節慶或自訂主題】指定特定關鍵字
```bash
python tools/weekly_pipeline.py --theme "賞櫻特輯" --keywords "sakura,cherry,櫻花,賞櫻" --deploy
```

---

## 3. 每週管線自動完成的工作項目清單

每次執行 `weekly_pipeline.py` 時，背後會精確依序執行以下 10 道工序：

| 步驟 | 動作名稱 | 說明 |
|:---:|:---|:---|
| **1** | **選題輪替** | 自動讀取 `theme_rotation.json`，取得下一個未使用的熱門主題。 |
| **2** | **精準篩選** | 從資料庫中精選 **10 蘑菇戰鬥點 + 10 巨型大花點**，按愛心數排序並排除重複。 |
| **3** | **AI 翻譯與創作** | 調用 OpenCode LLM 免費模型，將非中文地名翻譯為優雅繁體中文，並創作專屬微故事。 |
| **4** | **下載高畫質圖資** | 透過 Pikoohiong API 自動下載 20 張明信片至 `app/public/images/postcards/<slug>/`。 |
| **5** | **更新專欄資料** | 自動將新期別寫入 `locations.json`，最新一期置頂並同步對應 `/latest` 與 `meta.json`。 |
| **6** | **同步 App 書籤庫** | 自動將上週書籤晉升為正式版，並將本週新主題寫入 `geosim-data` 官方書籤庫並 Push。 |
| **7** | **Astro 靜態編譯** | 本地執行 `astro build`，確保 HTML/CSS 語法無錯誤。 |
| **8** | **Cloudflare Pages 上線** | 自動透過 Wrangler 將 `dist/` 上傳至 Cloudflare Edge，秒級全域生效。 |
| **9** | **GitHub 雙重備份** | 自動 `git add`、`git commit` 並 `git push origin main`，同時觸發 GitHub Pages 備援建置。 |
| **10** | **發送行銷郵件** | 自動寄送 Gmail 通知給管理者，信中包含即時可用的 **Threads 行銷貼文草稿與打卡座標**。 |

---

## 4. 發布後檢核清單 (Post-Release Checklist)

執行完管線後，只需花 **1~2 分鐘** 進行三點確認：

- [ ] **1. 線上專欄巡檢**：
  打開瀏覽器造訪 [最新一期專欄](https://kairosvector.pages.dev/geosim/weekly-featured/latest)，快速滑動檢查瀑布流排版、隨機點擊 2~3 張卡片確認彈窗正常置中展開且文字清晰。
- [ ] **2. Android App 實機確認**：
  在手機 GeoSim 點擊「每週精選」按鈕，確認是否順利讀取最新一期主題與景點。
- [ ] **3. 社群推廣發文（Threads）**：
  檢查信箱收到標題為 `【GeoSim 每周精選已發布】...` 的郵件，複製信中的文案，搭配本週明信片精選圖片發布至 Threads。

---

## 5. 常見緊急應變措施 (Troubleshooting)

* **情境 1：手機 App 出現舊快取**
  * 解法：網址後加上版號測試，如 `.../weekly-featured/latest?v=2`，或在 App 內下拉清除快取。
* **情境 2：欲緊急回退到先前版本**
  * 執行：`git checkout v1.0.0-weekly-featured` 並重新執行 `npm run build && npx wrangler pages deploy dist --project-name kairosvector`。

