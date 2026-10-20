# Garmin Connect Health Tracker, Trends Dashboard & Sport English 🏃‍♂️📊🌐

A powerful, secure, and **privacy-first** toolkit to connect with your Garmin Connect account, track health & recovery metrics, analyze **1000 Days of Historical Trends**, explore **Monthly Stacked Sleep Stages (深層/REM/淺層/清醒)**, **Endurance & Marathon Hub**, and deploy directly to **GitHub Pages** with an integrated **Bilingual Sport English & Athletic Training Principles (運動英語與運動科學核心原則)** knowledge hub.

---

## 🌐 GitHub Pages & Live Demo

This repository is ready for instant deployment to **GitHub Pages**:
- 📊 **Main Health Dashboard**: `index.html` (or `garmin_health_dashboard.html`)
- 🏃‍♂️ **Sport English & Principles Project**: `sport_english.html`
- 🤖 **Automated CI/CD**: `.github/workflows/deploy.yml` (Deploys automatically upon git push)

### 🚀 How to Enable GitHub Pages
1. Push your repository to GitHub.
2. Go to **Settings** $\rightarrow$ **Pages**.
3. Under **Build and deployment** $\rightarrow$ **Source**, choose **GitHub Actions** (or deploy directly from branch `main` root `/`).
4. Your personal health tracker and Sport English hub will be live at: `https://<your-username>.github.io/<repo-name>/`

---

## 🛡️ Absolute Privacy Protection Guarantee (純健康指標原則)

To protect personal privacy when publishing to GitHub Pages:
- 🚫 **Zero Personal Identifiers**: All user account GUIDs, user profile IDs, emails, display names, and device serial numbers are permanently stripped.
- 🚫 **No Location / GPS Leakage**: Activity names with specific cities, districts, parks, or streets are automatically sanitized into generic athletic classifications (e.g., `路跑 (Road Running)`, `10K+ 長跑 (Long Run)`, `全馬 (Marathon)`, `跑步機 (Treadmill)`).
- ✅ **Just Health & Athletic Numbers**: Only objective physiological and performance metrics are published:
  - 靜止心率 (RHR) & 心率變異度 (HRV)
  - 睡眠分期堆疊時長 (深層、REM、淺層、清醒) 與睡眠分數
  - 身體電量充放 (+Charge / -Drain) 與壓力指數
  - 步數、運動卡路里、VO2 Max、訓練完備度
  - 跑步里程、配速、爬升高度與運動時長

---

## 🌟 Key Features

### 1. 🏃‍♂️ 運動英語與十大訓練原則專區 (Sport English & The Principles Project)
專為耐力跑者、馬拉松運動員與體育愛好者打造的英漢雙語運動科學指南 (`sport_english.html`)：
- **📜 運動訓練十大黃金原則 (The 10 Golden Athletic Training Principles)**：
  - 以 Principles Project 格式深入解析：超負荷原則 (Progressive Overload)、特異性原則 (Specificity)、恢復與超補償 (Recovery & Supercompensation)、可逆性原則 (Reversibility)、個別差異 (Individual Differences)、週期化原則 (Periodization)、80/20兩極化訓練 (Polarized Training)、邊際效益遞減 (Diminishing Returns)、能量補給 (Fueling)、持之以恆 (Consistency)。
  - 每項原則皆包含：核心箴言 (Maxim)、運動生理學原理解析、跑者實戰與 Garmin 穿戴數據對應、常見誤區防護。
- **📚 80+ 專業運動英語分類辭典 (Categorized Sport English Glossary)**：
  - 涵蓋 6 大領域：跑步與賽事、運動生理與穿戴指標、肌力與體能、營養與恢復、週期化訓練、跑鞋與科技裝備。
  - 每個詞彙皆附音標、詞性、繁中釋義、詳細運動科學解說、英漢雙語實戰情境例句。
  - 🔊 **支援瀏覽器原生 Web Speech API 英文真人口音語音發音**。
- **🎴 互動式單字卡測驗模式 (Interactive Flashcard Mode)**：
  - 支援「全部顯示」、「隱藏中文（測驗英翻中）」、「隱藏英文（測驗中翻英）」，點擊卡片即可翻開複習。
- **🧭 跑者常用英美賽事縮寫速查表 (Runner's Acronyms Cheat Sheet)**：
  - PR, PB, BQ, DNF, DNS, LSD, MP, HMP, RPE, HRV, RHR, VO2 Max, LT, DOMS, TSS 等速查。
- **🗣️ 賽道與跑團實戰常用英文口語 (Race Day Idioms & Running Phrases)**。

### 2. 📅 跨月份歷史對比與「平均每月睡眠時長/階段分佈堆疊圖」
- **平均每月睡眠時長與階段分佈堆疊圖 (Monthly Stacked Sleep Stages Chart)**：
  - 🌙 清楚呈現每個月的**深層睡眠 (Deep, 藍色)**、**REM 快速動眼 (紫色)**、**淺層睡眠 (Light, 灰色)** 與 **清醒時長 (Awake, 橘色)** 堆疊時長（小時）。
  - 快速看出各月份睡眠總時長波動與深層/REM修復佔比變化。
- **逐月跑量與成長率 (Monthly Mileage & MoM %)**：統計每個月總跑量 (km) 與相較上個月的跑量增減幅度。
- **每月 10K+ 長跑與賽事場次統計**：每月份 10K+ 長跑次數、全馬與半馬場次、單月最長單次跑步距離。
- **生理指標逐月演進**：月均靜止心率 (RHR)、月均 HRV、月均睡眠品質、運動總卡路里。
- **月度歷史對照表**：完整羅列所有歷史月份數據。

### 3. 🎯 異常值過濾與雙軌視覺對比 (Outlier Trimming & Overlay Comparison)
- 一鍵開啟 **`[✓] 開啟去噪 (Trim Outliers)`**，支援 **5% / 10% / 15%** 多段截尾去噪。
- 圖表支援**雙軌對比線（實線：去噪後；黃色虛線：原始全量）**，各月表格即時標註彩色修正差距（如 `🟢 +0.5h`）。

### 4. 🛡️ 完整追蹤至 1000 天歷史 (1000 Days Historical Trace)
- 增量快取支援追蹤至 **1000 天（約 2.7+ 年）** 完整歷史資料，已快取的天數不再重複下載，秒級更新。

### 5. 🏃‍♂️ 長跑耐力、馬拉松與熱量消耗分析專區 (Endurance & Marathon Hub)
- **10K+ 長跑週期與間隔追蹤 (Long Run Cadence)**：10K+ 累積次數、平均間隔天數、距離上次長跑天數即時警示。
- **馬拉松與長距離賽事分級統計**：全馬/超馬（$\ge 42\text{ km}$）、半馬/LSD（$21\sim 42\text{ km}$）、10K 中長跑（$10\sim 21\text{ km}$）、歷史最長單次跑量。
- **跑量與卡路里燃燒統計**：總跑量、週均跑量、跑步總消耗卡路里、每公里平均燃燒熱量（kcal/km）。

### 6. 📊 每日走勢圖 vs 月度統計圖 雙模式
- **📈 每日走勢圖 (Daily Plots)**：逐日點圖（RHR、HRV、每日睡眠分期、身體電量充放、步數與強度）。
- **📅 月度統計圖 (Monthly Plots)**：逐月柱狀/折線圖（月睡眠分期堆疊、月跑量、月均心率/HRV、月卡路里）。
- **📋 每日原始明細表**：支援日期與運動名稱即時搜尋。

---

## 💻 快速使用指南

### 🌟 方式 1：Windows 一鍵更新（追蹤至 1000 天）
直接在資料夾中雙擊：
👉 **`一鍵更新健康儀表板.bat`**

### 🖥️ 方式 2：指令操作
```bash
# 增量同步 1000 天歷史並自動生成 GitHub Pages index.html 與本地儀表板
python main.py --sync --days 1000 --open

# 離線產出並開啟儀表板（不連網，使用現有快取）
python main.py --report --open
```
