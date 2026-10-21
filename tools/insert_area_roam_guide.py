import json

TIPS_FILE = 'app/src/data/tips.json'

with open(TIPS_FILE, 'r', encoding='utf-8') as f:
    tips = json.load(f)

new_tip = {
    "id": "geosim-area-roaming-guide",
    "productId": "geosim",
    "productName": "GeoSim",
    "title": "【GeoSim 全新功能】「區內漫步」完整教學：把點當圍籬！自由漫步 vs 走遍全區設定全解析",
    "slug": "geosim-area-roaming-guide",
    "category": "實戰技巧",
    "readTime": "4 分鐘閱讀",
    "updatedAt": "2026-10-21",
    "summary": "點的意義完全不同！依線與跳點把點當「依序經過的站」，區內漫步則把點當「圍籬」。搭配實機介面解析「自由漫步」與「走遍全區」兩種走法，讓角色在指定區域內自然探索、自動累積步數與催花開！",
    "content": [
        {
            "type": "heading",
            "text": "三種模式的差別，一句話講透"
        },
        {
            "type": "callout",
            "title": "💡 核心差異哲學：點的意義完全不同！",
            "text": "依線和跳點把點當「依序經過的站」，區內漫步把點當「圍籬」。其餘所有功能差異，都是從這關鍵的一點長出來的！"
        },
        {
            "type": "paragraph",
            "text": "在傳統的「依線移動」或「跳點傳送」中，你在地圖上打下的每個點，都是角色必須依序前往打卡的「車站」。但在 GeoSim 全新推出的<strong>「區內漫步」</strong>中，點下的點不再是目的地，而是用來框出一個專屬的<strong>活動範圍（電子圍籬）</strong>。角色只會在圍籬內部隨機探索，絕不會跑出界外！"
        },
        {
            "type": "heading",
            "text": "依線 vs 跳點 vs 區內漫步：功能對照表"
        },
        {
            "type": "table",
            "headers": [
                "比較項目",
                "依線移動",
                "跳點移動",
                "🌿 區內漫步 (新功能)"
            ],
            "highlightCol": 3,
            "rows": [
                [
                    "最少點數",
                    "2 個點（起點與終點）",
                    "2 個點",
                    "至少 3 個點（圈出面）"
                ],
                [
                    "怎麼動",
                    "平滑前進",
                    "瞬間傳送",
                    "區域內隨機遊走 / 全區覆蓋"
                ],
                [
                    "地圖顯示",
                    "實線路線",
                    "虛線軌跡",
                    "半透明填色區域（圍籬）"
                ],
                [
                    "路徑可預測",
                    "是（沿著固定線段）",
                    "是（固定跳點）",
                    "否（每次隨機，擬真自然）"
                ],
                [
                    "控制面板",
                    "有進度條、方向、停留",
                    "有跳點按鈕、停留倒數",
                    "全部沒有（全自動在區內晃悠）"
                ]
            ]
        },
        {
            "type": "heading",
            "text": "「區內漫步」兩種走法：自由漫步 vs 走遍全區"
        },
        {
            "type": "paragraph",
            "text": "點進「移動設定」後，區內漫步提供了兩種截然不同的遊走策略，滿足不同情境的需求："
        },
        {
            "type": "heading",
            "text": "1. 🔀 自由漫步（漫無目的地走）"
        },
        {
            "type": "paragraph",
            "text": "• <strong>特點：</strong>沒有固定終點、不保證走遍每個角落。模擬真人在公園隨興晃晃、商圈逛街的自然探索軌跡。<br/>• <strong>漫步風格調節：</strong>提供滑桿調整「走得挺直」到「很隨興」（想要筆直穿梭還是隨性轉彎任你選）。<br/>• <strong>結束方式：</strong>靠<strong>時限收尾</strong>（例如設定漫步 30 分鐘，時間到自動停止），也可以設為不會自己停。<br/>• <strong>最佳場景：</strong>邊掛機邊孵蛋、自然累積步數、摸摸商圈周邊散落的蘑菇、模擬真人防檢測。"
        },
        {
            "type": "image",
            "src": "/images/tips/geosim-area-roam-step2-free-walk.jpg",
            "caption": "▲ 自由漫步設定畫面：可自由微調「漫步風格（走得挺直 ~ 很隨興）」與漫步時間限制",
            "size": "normal"
        },
        {
            "type": "heading",
            "text": "2. ▦ 走遍全區（地毯式清掃）"
        },
        {
            "type": "paragraph",
            "text": "• <strong>特點：</strong>系統會智慧切分網格，<strong>隨機逛完範圍內區域，確保每個角落都會踩到</strong>！<br/>• <strong>預估耗時精算：</strong>上方會清楚顯示<strong>「一趟約 XX 分鐘」</strong>，時間掌握度極高。<br/>• <strong>結束後行為：</strong>可選擇「一次（逛完最後一格就停）」或「循環（逛完自動換一條新路線再逛一次，一直重複）」。<br/>• <strong>最佳場景：</strong>在特定公園進行「地毯式開花」、活動挑戰徹底掃街、絕不漏掉區域內的任何大花與果實。"
        },
        {
            "type": "image",
            "src": "/images/tips/geosim-area-roam-step3-full-coverage.jpg",
            "caption": "▲ 走遍全區設定畫面：即時精算預估一趟時間，可選擇逛完即停或循環重複",
            "size": "normal"
        },
        {
            "type": "heading",
            "text": "【實戰教學】區內漫步 3 步上手 SOP"
        },
        {
            "type": "heading",
            "text": "步驟 1：在地圖上打點，圍出你的「漫步圍籬」"
        },
        {
            "type": "paragraph",
            "text": "• 在地圖上點擊至少 3 個以上的頂點（例如在公園周邊點出 5~6 個點）。<br/>• 地圖會自動將頂點連線並以<strong>半透明藍色填色</strong>，形成一個閉合的多邊形圍籬。<br/>• 底部會顯示<strong>「範圍已就緒 • X 個頂點」</strong>，點擊「調整」可進入移動設定。"
        },
        {
            "type": "image",
            "src": "/images/tips/geosim-area-roam-step1-ready.jpg",
            "caption": "▲ 步驟 1：在地圖上標記至少 3 個頂點，系統自動生成半透明填色圍籬區域",
            "size": "normal"
        },
        {
            "type": "heading",
            "text": "步驟 2：選擇走法與速度設定"
        },
        {
            "type": "paragraph",
            "text": "• 在移動設定面板中，確認移動模式切換為<strong>「區內漫步」</strong>。<br/>• 選擇適合的走法（想隨性逛街選「自由漫步」；想地毯式開花選「走遍全區」）。<br/>• 速度推薦設為 18~19 km/h（快速催花開）或 5~10 km/h（模擬散步快走），點擊「✓ 套用設定」。"
        },
        {
            "type": "heading",
            "text": "步驟 3：點擊「開始區內漫步」，全自動在圍籬內探索！"
        },
        {
            "type": "paragraph",
            "text": "• 返回主畫面，點擊藍色大按鈕<strong>「● 開始區內漫步」</strong>。<br/>• 角色就會立即在填色圍籬內部平滑隨機遊走，底欄顯示「持續隨機漫步 • 走完一段自動換路徑，不會停」。<br/>• 隨時可點擊「暫停」或「停止」，不用手動操控搖桿，手機放著就能在指定安全區域內安心掛機！"
        },
        {
            "type": "image",
            "src": "/images/tips/geosim-area-roam-step4-running.jpg",
            "caption": "▲ 步驟 3：點擊開始，角色即可在圍籬範圍內自動隨機遊走，絕不出界",
            "size": "normal"
        },
        {
            "type": "heading",
            "text": "常見問題與使用小訣竅 (FAQ)"
        },
        {
            "type": "steps",
            "items": [
                "圍籬範圍建議設多大？：建議抓半徑 300~600 公尺左右（如一個街區或一座大型公園）。範圍太小容易很快折返，範圍適中可確保兼顧活動密度與 5 分鐘網格冷卻。",
                "想調整圍籬形狀怎麼辦？：在「範圍已就緒」畫面點擊「✏️ 調整頂點」，即可直接拖曳各頂點改變圍籬形狀，或點擊「垃圾桶」圖示重新繪製。",
                "會不會走一走跑出圍籬外？：絕對不會。系統底層算法已嚴格限制所有隨機遊走軌跡與航點轉換，100% 只在多邊形內部生成。"
            ]
        }
    ]
}

# Check if already exists, update or append
existing_idx = next((i for i, t in enumerate(tips) if t.get('slug') == 'geosim-area-roaming-guide'), None)
if existing_idx is not None:
    tips[existing_idx] = new_tip
else:
    tips.insert(0, new_tip)

with open(TIPS_FILE, 'w', encoding='utf-8') as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)

print("Successfully inserted geosim-area-roaming-guide into tips.json!")
