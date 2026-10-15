# 【教學】透過 Google 地圖秒抓香菇 GPS 點位，一鍵分享至 GeoSim 精準打菇！

## 🎯 教學目標與核心情境
- **適用對象**：Pikmin Bloom 新手玩家、跨國/遠距打菇玩家。
- **痛點解決**：遠處香菇看得到打不到、外國地標拼不出來、手動輸座標太慢。
- **神技流程**：利用遊戲內建「前往這裡」喚起 Google 地圖，透過 Android 原生系統「分享」一鍵丟給 GeoSim，經緯度秒代入、直達香菇正下方！

---

## 📸 圖文步驟對照（圖片均已放在本資料夾）

### 第一步：點開香菇，按右下角「前往這裡」
- **說明**：在遊戲地圖中點開你想打的那顆遠處香菇，查看畫面右下角，點擊「📍 前往這裡」按鈕。
- **對應圖片**：step1_前往這裡.jpg

---

### 第二步：點選「在地圖應用程式開啟」
- **說明**：點擊後底部彈出選單，直接選擇「在地圖應用程式開啟」，手機系統會自動啟動 Google 地圖。
- **對應圖片**：step2_在地圖應用程式開啟.jpg

---

### 第三步：在 Google 地圖中點擊「分享」
- **說明**：Google 地圖開啟後，已經精準釘選出該香菇在現實世界的官方真實 GPS 座標點位。點擊地標資訊卡上的「分享」按鈕。
- **對應圖片**：step3_Google地圖點分享.jpg

---

### 第四步：分享清單直接點「GeoSim」秒飛！
- **說明**：在彈出的 Android 系統分享清單中，直接點選「GeoSim」。系統會自動跳轉喚醒 GeoSim，且香菇的經緯度座標已自動帶入、地圖已鎖定目標！只要點擊「換點」（或移動過去），再切回遊戲，你的人就已經完美站在香菇正下方了！
- **對應圖片**：step4_分享選GeoSim秒飛.jpg

---

## 🛡️ 新手安全指南（冷卻時間 CD 法則）
- **同城短距移動（數百公尺至數公里）**：建議換點後稍候 1~3 分鐘再開打。
- **跨國長途飛行（例如台灣飛往德國）**：請務必遵守 2 小時冷卻時間（CD）法則。抵達後不要立刻進行採集或打菇，靜候 CD 結束再送出皮克敏，確保帳號安全！

---

## 💻 網站資料庫與靜態路徑配置現況（供 Agent 參考）

1. **資料來源**：
   - pp/src/data/tips.json 頂部已新增此篇設定，slug 為 geosim-google-maps-mushroom-guide。
2. **Web 圖片存放路徑**：
   - pp/public/images/tips/mushroom-detail-nav.jpg
   - pp/public/images/tips/mushroom-open-maps-menu.jpg
   - pp/public/images/tips/google-maps-location-view.jpg
   - pp/public/images/tips/share-to-geosim-sheet.jpg
3. **本地打包結果**：
   - pp/dist/tips/geosim-google-maps-mushroom-guide/index.html 已成功產出。
4. **Git 狀態**：
   - 已經 commit 並 push 到 origin main (kevycheng/kairosVector_web) 與 ackup main (kairosvector/kairosvector.github.io)。
