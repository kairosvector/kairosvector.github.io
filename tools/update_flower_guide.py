import json

TIPS_FILE = 'app/src/data/tips.json'

with open(TIPS_FILE, 'r', encoding='utf-8') as f:
    tips = json.load(f)

new_content = [
    {
        "type": "image",
        "src": "/images/tips/pikmin-planting-speed-test.jpg",
        "caption": "▲ 皮克敏種花效率實測：花瓣消耗只看「時間」不看速度，鎖定 18~19 km/h 效益暴增 2.7 倍，43 分鐘即可拿滿每日 15,000 朵（60 金幣）！",
        "size": "full"
    },
    {
        "type": "paragraph",
        "text": "<strong>一句話核心結論：</strong>《Pikmin Bloom》的花瓣消耗完全只取決於「時間」（固定約每 9.68 秒扣除 1 片），與移動速度無關！因此只要將速度拉高至極限 <strong>18~19 km/h</strong>，單位時間掃過的地圖網格翻倍，花瓣產出直接暴增 2.7 倍，種滿每日 15,000 朵（60 金幣）只需約 43 分鐘。"
    },
    {
        "type": "heading",
        "text": "【實戰教學】GeoSim「繞圈巡航」5 步標準 SOP（自動閉環爆花）"
    },
    {
        "type": "paragraph",
        "text": "以往手動在地圖上一個個打點非常耗時，且走直線折返容易撞上「5 分鐘（300 秒）網格冷卻」白白浪費花瓣。GeoSim 內建了強大的「進階幾何巡航生成器」，只要 5 步即可全自動生成完美大圓閉環，一趟剛好約 9 分 55 秒，冷卻完美解除，徹底解放雙手全自動爆花："
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
            "維持 40 隻皮克敏滿編出動：種花的單次播種半徑與隊伍隻數直接連動。未滿 40 隻時播種圓圈狹小；只有在 40 隻滿編時才能展開最大圓形覆蓋面，徹底發揮 18~19 km/h 的地圖掃描效益。",
            "時速嚴格壓在 18~19 km/h：Pikmin Bloom 的時速上限判定點在 20 km/h。一旦瞬時速度突破 20 km/h，系統會判定為乘車並立刻強制中斷種花。定速在 18~19 km/h 是數學上的最大效益安全點。",
            "半徑抓在 400~500 公尺（單趟 > 5 分鐘）：太小的圓圈一趟跑完不到 5 分鐘，繞第二圈時會撞上網格冷卻；設定 475m 半徑一趟約 9 分 55 秒，冷卻完美解除，可無限循環。",
            "原地停等或切換時務必先「暫停種花」：切記「停下來依然每 9.68 秒扣 1 片花瓣」，在停等、進入室內或整理背包前，養成先暫停種花的習慣，避免花瓣在原地憑空蒸發。"
        ]
    }
]

for t in tips:
    if t.get('slug') == 'efficient-flower-planting-guide':
        t['title'] = "如何種花最高效率：GeoSim「繞圈巡航」5 步標準 SOP（自動閉環爆花）"
        t['updatedAt'] = "2026-10-20"
        t['readTime'] = "3 分鐘閱讀"
        t['summary'] = "實測證明花瓣消耗只看「時間」不看速度！透過 GeoSim 內建「進階繞圈巡航」5 步標準 SOP，設定半徑 475m 配合 18~19 km/h，完美破解 5 分鐘冷卻，全自動穩定爆花！"
        t['content'] = new_content
        break

with open(TIPS_FILE, 'w', encoding='utf-8') as f:
    json.dump(tips, f, ensure_ascii=False, indent=2)

print("Successfully updated tips.json with streamlined SOP-focused guide!")
