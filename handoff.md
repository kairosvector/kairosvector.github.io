# Handoff：geosim-data (Pikmin Bloom 書籤管理) 專案維運手冊

> **工作區路徑**：`D:\project\py_project\sideprojects\geosim-data`  
> **版本控管**：工作區本身**非** Git repo；Git 只位於 `remote\` 子目錄 (`https://github.com/kevycheng/geosim-data.git`，branch: `main`)。

---

## 1. 三份核心書籤檔與架構原則

| 檔案路徑 | 角色與定位 | 操作權限與注意事項 |
| :--- | :--- | :--- |
| `bookmark_staging.json` | **工作區 staging** | 日常/手動操作的主要修改對象 |
| `remote\official_bookmarks.staging.json` | **GitHub staging** | 用戶在網站上驗證、預覽的即時來源（改完必須 push） |
| `remote\official_bookmarks.json` | **線上 production** | App 實機正式讀取的清單 |

> [!CAUTION]
> **鐵律**：**絕不手動 promote production！**  
> `remote\official_bookmarks.json`（線上 production）**只由每週六 02:00 排程 (`geosim-weekly`) 自動從 staging 晉升**。

---

## 2. 每週精選標準更新流程 (SOP)
*(排程自動跑；若需手動介入時，必須完整遵照相同步驟)*

1. **先拉取最新遠端**：  
   切換至 `remote\` 目錄執行：
   ```bash
   git pull --rebase origin main
   ```
   *(重要：用戶會併行推 VIP 等 commit，務必先 pull 再做後續操作，避免衝突或覆蓋)*

2. **主題輪替與進度紀錄**：  
   讀取 `theme_rotation.json`，取得 `lastUsedIndex` 的下一格主題（若到底則 wrap 回第一個），更新 `lastUsedIndex` 後存回。

3. **雙向同步與晉升**：  
   - 先將舊的 `remote\official_bookmarks.staging.json` 複製覆蓋到 `remote\official_bookmarks.json`（舊 staging 晉升為 production）。
   - 再將最新的 staging 同步回工作區 `bookmark_staging.json`，確保後續操作基於最新基準。

4. **執行書籤生成工具**：  
   在 `D:\project\py_project\sideprojects\geosim-data` 執行：
   ```bash
   python fill_bookmark.py --folder folder_weekly_featured --name "0.[每周精選] 主題:<主題名稱>" --keywords "<該主題關鍵字>" --limit 20 --weekly
   ```
   *配額：菇 10 / 花 10（平分為 20 筆上限）。*

5. **地名全中文化翻譯**：  
   逐筆檢查 `folder_weekly_featured` 下的所有點位名稱，**非中文名稱一律翻成中文**（保留品牌/專有名詞如 IKEA、Xpark 等）。

6. **同步與推送驗證**：  
   - 將工作區的 `bookmark_staging.json` 複製覆蓋至 `remote\official_bookmarks.staging.json`。
   - 在 `remote\` 目錄內執行：
     ```bash
     git add official_bookmarks.staging.json theme_rotation.json
     git commit -m "Update weekly featured (<主題名稱>)"
     git pull --rebase origin main
     git push origin main
     ```
   *(修改 staging 一定要 push，用戶才能在網站與 App 上驗證！)*

7. **發送彙總通知**：  
   寄出 Email 摘要報告。  
   *(每日 12:30 另有獨立的 `geosim-model-check` 任務，執行記錄存於 `scheduled_logs\`)*。

---

## 3. 重要踩坑與避雷守則 (Crucial Rules)

### ① 手動改精選時，必須同步更新 `lastUsedIndex`
* **踩坑歷史**：曾發生過手動加了「城堡」主題，但忘記同步 `lastUsedIndex`，導致週六排程重選同主題並以 `fill_bookmark.py` 覆蓋掉手工調整的點位。
* **守則**：手動改動主題時，**必須同步將 `theme_rotation.json` 內的 `lastUsedIndex` 改為該主題的索引值**。

### ② 模型備援機制與 BAT 呼叫語法
* **模型順序 (`models.txt`)**：  
  `muse-spark-1.3` ➔ `big-pickle` ➔ `mimo-v2.5`（順序即優先序）。
* **排程腳本邏輯**：
  - `schedule_weekly.bat`：依序嘗試，**首個成功即停止**。
  - `check_model.bat`：三個模型**全部測試**，最後寄出一封彙總信。
* **Windows Batch 語法地雷**：
  - 呼叫 `opencode` 務必加上 `call`（因為它是 `.cmd` 包裝，若沒加 `call` 控制權將一去不復返）。
  - 迴圈內部判斷 `%errorlevel%` 時，必須啟用延遲變數擴展：`setlocal enabledelayedexpansion` 並使用 `!errorlevel!`。

### ③ 純點資料夾前綴歸類與批次新增
* **前綴歸類規則**：純點 folder 靠名稱前綴（第一個底線 `_` 之前）歸類，**前綴必須存在於 `reorg_pure.py` 的 `PURE_TYPE_MAP`**，否則下次執行 reorg 時會被判定為無效並移走。
* **新增純點**：使用 `add_pure_batch.py`，座標會以**小數點後 3 位（約 110m 距離）自動進行去重**。

### ④ Windows Console 與檔案編碼防爆
* **UTF-8 BOM**：`pure_data\*.json` 檔案帶有 UTF-8 BOM，Python 讀取時必須指定 `encoding="utf-8-sig"`。
* **Windows Console (cp950)**：含有中文或特殊字符的 Python 腳本，**一律寫成暫存 `.py` 檔案後執行**，嚴禁使用 `python -c "..."` 內聯傳遞中文字串，否則必遭編碼截斷或跳錯。

### ⑤ 資料校驗與 Commit 紀律
* **數量核對**：每步操作完成後，必須核對 bookmarks 與 folders 的總筆數是否符合預期。
* **Commit 紀律**：**測試時絕不隨意 git commit**（除非用戶明確指示）；但實測的測試 Email 則可以正常發送。
