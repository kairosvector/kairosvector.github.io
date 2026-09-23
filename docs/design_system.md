# Kairos Vector Studio — Design System

**Visual Direction:** Direction C — Tech Canvas (Cyber Dark & Electric Prism)
**Keywords:** Technology, Modern, Playful, Useful, Developer-created

---

## 1. Theme Configuration (雙主題設計)

網站內建 2 款精選主題（預設為 **🌙 暗夜極客**，支援即時切換）：

### 方案 1：🌙 暗夜極客 (Cyber Dark) — 預設
- **深色基底：** 黑曜石底色 `#0A0C14` / 微光表面 `#141828` / 邊框 `#232A42`
- **文字階層：** 主白 `#F8FAFC` / 次要 `#94A3B8` / 靜音 `#64748B`
- **霓虹色盤：** 極光紫 `#8B5CF6` + 數碼青 `#06B6D4` + 翡翠綠 `#34D399` + 亮琥珀 `#F59E0B`
- **氛圍：** 極致沉浸、開發生態工具感、強烈的夜間極光與卡片微光邊框效果。

### 方案 2：⚡ 活力電氣 (Electric Prism)
- **亮色基底：** 純白 `#FFFFFF` / 微灰底 `#FAFAFC` / 邊框 `#E5E7EB`
- **文字階層：** 主黑 `#111827` / 次要 `#4B5563` / 靜音 `#9CA3AF`
- **電氣色盤：** 電氣紫 `#7C3AED` + 科技青 `#06B6D4` + 暖琥珀 `#F59E0B`
- **氛圍：** 高能量極光動態、明亮吸睛、科技感強烈。

---

## 2. High-Contrast Semantic Badges (高對比度丸型標籤)

為解決同色系背景與文字對比度不足的問題，全站統一採用語義化高對比度標籤：

| 標籤類別 | 暗夜極客 (Dark Mode) | 活力電氣 (Light Mode) | 對比度表現 |
|---|---|---|---|
| **PikieWalker (`.badge--pikiewalker`)** | 背景 `rgba(52, 211, 153, 0.14)`<br/>邊框 `rgba(52, 211, 153, 0.35)`<br/>文字 `#6EE7B7` (薄荷霓虹) | 背景 `#ECFDF5`<br/>邊框 `#A7F3D0`<br/>文字 `#065F46` (深翡翠綠) | WCAG AAA (對比度 > 7:1) |
| **GeoSim (`.badge--geosim`)** | 背景 `rgba(56, 189, 248, 0.14)`<br/>邊框 `rgba(56, 189, 248, 0.35)`<br/>文字 `#7DD3FC` (天藍霓虹) | 背景 `#F0F9FF`<br/>邊框 `#BAE6FD`<br/>文字 `#0369A1` (深湛藍) | WCAG AAA (對比度 > 7:1) |
| **Brand (`.badge--brand`)** | 背景 `rgba(139, 92, 246, 0.20)`<br/>邊框 `rgba(139, 92, 246, 0.4)`<br/>文字 `#DDD6FE` (紫丁香白) | 背景 `#F5F3FF`<br/>邊框 `#DDD6FE`<br/>文字 `#5B21B6` (深紫) | WCAG AAA (對比度 > 7:1) |

---

## 3. Product Hero Visual Asset Protocol (產品視覺資源規範)

- **PikieWalker (`#pikiewalker-asset-container`)**：目前以高擬真純 CSS Mockup 呈現，預留為使用者後續提供的官方視覺圖槽位。
- **GeoSim (`#geosim-asset-container`)**：目前以高擬真純 CSS Mockup 呈現，預留為使用者後續提供的官方視覺圖槽位。

---

## 4. Expandable Interactive Accordion (實用技巧手風琴展開元件)

- **元件類別：** `.accordion-list` / `.accordion-item` / `.accordion-header` / `.accordion-body`
- **互動特性：** 支援單獨展開/收合、動態箭頭旋轉動畫、點擊提示（微光邊框反饋），並預留每篇技巧的詳細指南（`.accordion-body__extra`）擴充空間。
