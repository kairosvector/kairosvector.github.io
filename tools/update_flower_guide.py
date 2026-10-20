import json

TIPS_FILE = 'app/src/data/tips.json'

with open(TIPS_FILE, 'r', encoding='utf-8') as f:
    tips = json.load(f)

new_content = [
    {
        "type": "heading",
        "text": "顛覆直覺的核心機制：花瓣消耗看時間，跟速度無關！"
    },
    {
        "type": "paragraph",
        "text": "許多《Pikmin Bloom》玩家在種花時常有一個直覺迷思：「是不是走慢一點比較省花瓣？」然而經過嚴謹的控制變數實測（相同 40 隻皮克敏滿員隊伍、相同路線、相同花種、固定實測 5 分鐘 / 300 秒），結果徹底顛覆了大家的認知——<strong>花瓣消耗完全只取決於「時間」，與你的移動速度毫無關係！</strong>"
    },
    {
        "type": "callout",
        "title": "💡 核心實測結論：想省花瓣，就必須提高移動速度！",
        "text": "• 300 秒（5 分鐘）無論時速 6 km/h 還是 19 km/h，花瓣消耗全部固定為 31 片（約每 9.68 秒扣除 1 片）！\n• 原地停留或散步慢走，花瓣依然在持續流失；但如果把時速拉高到 18~19 km/h，單位時間掃過的新地圖網格翻倍，每片珍貴花瓣換得的花朵數足足暴增 2.7 倍！"
    },
    {
        "type": "heading",
        "text": "實測數據大公開：6 km/h vs 19 km/h 的 2.7 倍差距"
    },
    {
        "type": "paragraph",
        "text": "以下為在 40 隻皮克敏滿編條件下，分別以悠閒散步（6 km/h）、一般快走（10 km/h）與極限巡航（19 km/h）進行 5 分鐘實測的完整數據比對："
    },
    {
        "type": "table",
        "headers": [
            "測試時速",
            "花朵總數",
            "花瓣消耗",
            "每片花瓣可種花數",
            "每秒種花速率",
            "每公里種花密度"
        ],
        "highlightCol": 3,
        "rows": [
            [
                "6 km/h（悠閒散步）",
                "636 朵",
                "31 片",
                "20.52 朵/片",
                "2.12 朵/秒",
                "1,272 朵/km"
            ],
            [
                "10 km/h（一般快走）",
                "1,151 朵",
                "31 片",
                "37.13 朵/片",
                "3.84 朵/秒",
                "1,381 朵/km"
            ],
            [
                "19 km/h（極限巡航）",
                "1,725 朵",
                "31 片",
                "55.65 朵/片 (最高 ★)",
                "5.75 朵/秒 (最快 ★)",
                "1,089 朵/km"
            ]
        ]
    },
    {
        "type": "paragraph",
        "text": "從數據中可以清楚發現：在同樣消耗 31 片花瓣的情況下，19 km/h 比 6 km/h 多種出了將近 1,100 朵花（1,725 朵 vs 636 朵），播種速率從每秒 2.12 朵衝上 5.75 朵！特別是在面對活動限定、取得不易的稀有花瓣（如櫻花、山茶花、彼岸花）時，拉高速度才能把花瓣價值發揮到極致。"
    },
    {
        "type": "image",
        "src": "/images/tips/pikmin-planting-speed-test.jpg",
        "caption": "▲ 皮克敏種花效率實測圖：速度越快，花開越多！19 km/h 每花瓣產出高達 55.65 朵，差距達 2.7 倍",
        "size": "full"
    },
    {
        "type": "heading",
        "text": "解任務花瓣需求速查表：19 km/h 幫你省下 75% 珍貴花瓣"
    },
    {
        "type": "paragraph",
        "text": "許多玩家常苦惱活動挑戰或社群日到底需要準備多少花瓣才夠？透過實測速率換算，鎖定 18~19 km/h 不僅完成速度快了將近 4 倍，所需花瓣更是直接打 2.5 折："
    },
    {
        "type": "table",
        "headers": [
            "目標花朵數",
            "19 km/h 巡航耗時",
            "所需花瓣量（40隻滿編）",
            "一般散步 (5 km/h) 耗時對比"
        ],
        "highlightCol": 2,
        "rows": [
            [
                "1,000 朵",
                "約 3 分鐘",
                "約 18 片 (省花瓣 ★)",
                "約 12 分鐘（需 ~75 片）"
            ],
            [
                "2,500 朵（活動常見）",
                "約 7.2 分鐘",
                "約 45 片 (省花瓣 ★)",
                "約 30 分鐘（需 ~188 片）"
            ],
            [
                "5,000 朵",
                "約 14.5 分鐘",
                "約 90 片 (省花瓣 ★)",
                "約 60 分鐘（需 ~375 片）"
            ],
            [
                "10,000 朵（社群日）",
                "約 29 分鐘",
                "約 180 片 (省花瓣 ★)",
                "將近 2 小時（需 ~750 片）"
            ]
        ]
    },
    {
        "type": "heading",
        "text": "為什麼不能折返跑？破解「5 分鐘網格冷卻」陷阱"
    },
    {
        "type": "paragraph",
        "text": "《Pikmin Bloom》地圖在底層是以 S2 網格劃分。同一個網格被種過之後，會進入 <strong>5 分鐘（300 秒）冷卻時間</strong>。在冷卻期間，即使你人物再次經過該處，系統也不會產生任何新花朵！<br/><br/><strong>⚠️ 致命雷區：</strong>若你走直線「折返跑」，折返後的 5 分鐘內全部是在做白工，但珍貴花瓣依然每 9.68 秒被扣除一片！<br/><br/><strong>💡 完美解法：</strong>規劃「直徑夠大的環形閉環（周長 > 1.6 公里）」。當你繞完一圈回到起點時，耗時剛好超過 5 分鐘，冷卻早已解除，達成 100% 無縫、零浪費的無限循環開花！"
    },
    {
        "type": "heading",
        "text": "【實戰教學】GeoSim「繞圈巡航」5 步標準 SOP（自動閉環爆花）"
    },
    {
        "type": "paragraph",
        "text": "以往手動在地圖上一個個打點非常耗時。GeoSim 內建了強大的「進階幾何巡航生成器」，只要 5 步即可全自動生成完美大圓閉環，徹底解放雙手："
    },
    {
        "type": "image",
        "src": "/images/tips/geosim-circle-step1-center.jpg",
        "caption": "【步驟 1】在 GeoSim 地圖上挑選合適的開闊區域點選為中心點，點擊右下角「進階」功能選單",
        "size": "normal"
    },
    {
        "type": "image",
        "src": "/images/tips/geosim-circle-step2-advanced.jpg",
        "caption": "【步驟 2】在進階功能清單中，點選「繞圈移動」（以選定點為圓心自動生成幾何巡航軌跡）",
        "size": "normal"
    },
    {
        "type": "image",
        "src": "/images/tips/geosim-circle-step3-shape-radius.jpg",
        "caption": "【步驟 3】移動形狀選「圓繞圈」，將半徑設定為 475 m（上方精算圓周 2.98 km、預估一趟 9:55，遠大於 5 分鐘冷卻，絕不浪費任何花瓣！）",
        "size": "normal"
    },
    {
        "type": "image",
        "src": "/images/tips/geosim-circle-step4-speed-loop.jpg",
        "caption": "【步驟 4】速度切換為「騎」，拉至 18~19 km/h（避開 20 km/h 防超速判定），運行模式選「循環」，點擊「開始繞圈」",
        "size": "normal"
    },
    {
        "type": "image",
        "src": "/images/tips/geosim-circle-step5-running.jpg",
        "caption": "【步驟 5】系統自動在圓周均勻生成 24 個平滑航點並開始依線巡航！切回《Pikmin Bloom》點擊開始種花，放著就能全自動狂開花",
        "size": "normal"
    },
    {
        "type": "heading",
        "text": "極速種花 4 大防踩坑 Checklist"
    },
    {
        "type": "steps",
        "items": [
            "維持 40 隻皮克敏滿編出動：種花的單次播種半徑與隊伍隻數直接連動。未滿 40 隻時播種圓圈狹小；只有在 40 隻滿編時才能展開最大圓形覆蓋面，徹底發揮 19 km/h 的地圖掃描效益。",
            "時速嚴格壓在 18~19 km/h：Pikmin Bloom 的時速上限判定點在 20 km/h。一旦瞬時速度突破 20 km/h，系統會判定為乘車並立刻強制中斷種花。定速在 18~19 km/h 是數學上的最大效益安全點。",
            "半徑抓在 400~500 公尺（單趟 > 5 分鐘）：太小的圓圈一趟跑完不到 5 分鐘，繞第二圈時會撞上網格冷卻；設定 475m 半徑一趟約 9 分 55 秒，冷卻完美解除，可無限循環。",
            "原地停等或切換時務必先「暫停種花」：切記「停下來依然每 9.68 秒扣 1 片花瓣」，在停等、進入室內或整理背包前，養成先暫停種花的習慣，避免花瓣在原地憑空蒸發。"
        ]
    }
]

for t in tips:
    if t.get('slug') == 'efficient-flower-planting-guide':
        t['title'] = "如何種花最高效率：實測 18~19 km/h 黃金時速與「繞圈巡航」SOP，花瓣效益翻倍秘訣"
        t['updatedAt'] = "2026-10-20"
        t['summary'] = "花瓣消耗只看「時間」不看速度！透過 5 分鐘控制變數實測，揭秘 6 km/h 與 19 km/h 的 2.7 倍巨大差距。搭配 GeoSim「進階繞圈巡航」5 步標準 SOP，教你如何設定半徑 475m 完美破解 5 分鐘冷卻，全自動穩定爆花！"
        t['content'] = new_content
        break

with open(TIPS_FILE, 'w', encoding='utf-8') as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)

print("Successfully updated tips.json with new flower planting SOP guide!")
