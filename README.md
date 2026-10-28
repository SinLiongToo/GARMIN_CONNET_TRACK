# Garmin Connect Health Tracker, Trends Dashboard & Sport English 🏃‍♂️📊🌐

A powerful, secure, and **privacy-first** toolkit to connect with your Garmin Connect account, track health & recovery metrics, analyze **1000 Days of Historical Trends**, explore **Monthly Stacked Sleep Stages (深層/REM/淺層/清醒)**, **Endurance & Marathon Hub**, and deploy directly to **GitHub Pages** with an integrated **Bilingual Sport English & Athletic Training Principles (運動英語與運動科學核心原則)** knowledge hub.

---

## 🌐 GitHub Pages & Live Demo

This repository is ready for instant deployment to **GitHub Pages**:
- 📊 **Main Health Dashboard**: `index.html` (or `garmin_health_dashboard.html`)
- 🏃‍♂️ **Sport English & Principles Project**: `sport_english.html`
- 🤖 **Automated CI/CD**: `.github/workflows/deploy.yml` (Deploys automatically upon git push)

### 🚀 Live Website
- 👉 **GitHub Pages**: [https://sinliongtoo.github.io/GARMIN_CONNET_TRACK/](https://sinliongtoo.github.io/GARMIN_CONNET_TRACK/)

---

## 📁 專案檔案架構與功能對照表 (Project Manifest)

```text
GARMIN_CONNET_TRACK/
├── 🌐 GitHub Pages 靜態網站發布檔案 (Web Frontend)
│   ├── index.html                   # 預設首頁：純數值個人健康與耐力分析儀表板
│   ├── garmin_health_dashboard.html # 完整健康儀表板（獨立離線版）
│   ├── sport_english.html           # 運動英語辭典、十大黃金訓練原則、熱身音訊與傷病防護指南
│   └── quotes_data.js               # 600 句傳奇運動家經典金句庫與運動心智哲學資料集
│
├── ⚙️ Python 資料同步與分析後端 (Data Pipeline)
│   ├── main.py                      # 主程式：負責抓取、增量快取、統計分析與 HTML 產生
│   ├── garmin_client.py             # Garmin Connect API 連線與 Token/MFA 認證管理
│   ├── health_analyzer.py           # 健康指標分析器（月度聚合、睡眠分期、去噪演算法）
│   ├── html_generator.py            # 動態渲染生成 Chart.js 互動式儀表板 HTML
│   ├── insights_engine.py           # 智慧洞察引擎（生成運動與生理恢復建議）
│   ├── generate_pages.py            # 隱私去識別化產出 GitHub Pages index.html
│   └── download_gpx.py              # 批量下載 Garmin GPS 運動軌跡（自動跳過跑步機等室內運動）
│
├── 🚀 部署與自動化批次檔 (Automation & Deployment)
│   ├── deploy.py                    # 核心自動化發布腳本（安全挑選前端檔案、建立 commit 並推送）
│   ├── deploy.bat                   # 一鍵執行 deploy.py 的 Windows 快速入口
│   ├── 一鍵推送至GitHub.bat          # 繁體中文 Windows 快速部署入口（呼叫 deploy.bat）
│   └── 一鍵更新健康儀表板.bat        # 本地一鍵增量同步 Garmin 數據 + 下載軌跡並更新儀表板
│
├── 🔒 隱私與配置設定 (Configuration & Security)
│   ├── .gitignore                   # 嚴格排除個人憑證、Token、JSON 原始檔與 GPX 軌跡
│   ├── .env.example                 # 環境變數設定範例（Garmin 帳號密碼，選填）
│   ├── requirements.txt             # 專案 Python 依賴清單
│   └── .github/workflows/deploy.yml # GitHub Actions 自動化部署工作流程
│
└── 🗂️ 本地快取與未追蹤資料（自動排除於 Git 之外）
    ├── marathon_gpx/                # 本地儲存的 GPX 軌跡檔案（⚠️ 隱私保護，不納入版本控制）
    ├── garmin_health_history.json   # 1000 天完整生理快取資料（⚠️ 隱私保護，不納入版本控制）
    └── session_cache/ & tokens.json # Garmin 授權憑證（⚠️ 隱私保護，不納入版本控制）
```

---

## 🛡️ Absolute Privacy Protection Guarantee (純健康指標原則)

To protect personal privacy when publishing to GitHub Pages:
- 🚫 **Zero Personal Identifiers**: All user account GUIDs, user profile IDs, emails, display names, and device serial numbers are permanently stripped.
- 🚫 **No Location / GPS Leakage**: Activity names with specific cities, districts, parks, or streets are automatically sanitized into generic athletic classifications (e.g., `路跑 (Road Running)`, `10K+ 長跑 (Long Run)`, `全馬 (Marathon)`, `跑步機 (Treadmill)`).
- 🚫 **GPX 軌跡永久排除**: 所有 GPX 運動軌跡與 `marathon_gpx/` 目錄均已寫入 `.gitignore`，確保包含真實經緯度與訓練路線的 GPS 檔案絕不被 Commit 上傳至公開網路。
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
  - 🔊 **支援瀏覽器原生 Web Speech API 英文真人口音語音發音與自動循環播放**。
- **🎴 互動式單字卡測驗模式 (Interactive Flashcard Mode)**：
  - 支援「全部顯示」、「隱藏中文（測驗英翻中）」、「隱藏英文（測驗中翻英）」，點擊卡片即可翻開複習。
- **🧭 跑者常用英美賽事縮寫速查表 (Runner's Acronyms Cheat Sheet)**：
  - PR, PB, BQ, DNF, DNS, LSD, MP, HMP, RPE, HRV, RHR, VO2 Max, LT, DOMS, TSS 等速查。
- **🩹 跑者常見運動傷害預防與 RAMP 動態熱身示範**：
  - 整合足底筋膜炎、ITBS 髂脛束症候群、髕骨肌腱炎等防護要點與精選示範影片。
- **🏋️‍♂️ 耐力跑者肌力與體能訓練科學 (Strength & Conditioning & Kinetic Chain)**：
  - 深入解析 16 大肌力體能核心模組：收縮力學與漸進超負荷、離心下坡減速、快慢肌纖維轉化、後側動力鏈（臀大肌/膕旁肌）、比目魚肌 8 倍體重承載防護、單腳防骨盆傾斜、抗旋轉核心剛性、牽張縮短循環 (SSC)、跟腱剛性與縮短觸地時間 (GCT)、下落跳與反應力量指數 (RSI)、力量發展率 (RFD)、共存訓練干擾效應破解 (Concurrent Training)、最大肌力神經適應 (85-90% 1RM)、保留次數 (RIR) 自主調節與 DOMS 積極修復。
  - 搭配 16 篇實戰情境雙語運動科學例句與瀏覽器原生真人連續自動語音朗讀引擎。

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
- **馬拉松與長距離賽事分級統計**：全馬/超馬（≥ 42 km）、半馬/LSD（21 ~ 42 km）、10K 中長跑（10 ~ 21 km）、歷史最長單次跑量。
- **跑量與卡路里燃燒統計**：總跑量、週均跑量、跑步總消耗卡路里、每公里平均燃燒熱量（kcal/km）。

---

## 💻 快速使用指南 (Quick Start)

### 🌟 方式 1：Windows 桌面雙擊更新（推薦）

1. **同步 Garmin 資料並產生新儀表板**：
   雙擊 👉 **`一鍵更新健康儀表板.bat`**
   （自動同步 1000 天歷史健康數據，下載最新 GPX 軌跡，並在預設瀏覽器開啟儀表板）

2. **發布最新儀表板到 GitHub Pages**：
   雙擊 👉 **`一鍵推送至GitHub.bat`** 或 **`deploy.bat`**
   （安全加入網頁發布檔案，自動 Commit 並推送至 GitHub main 分支觸發 GitHub Actions）

---

### 🖥️ 方式 2：Command Line 命令列操作

```bash
# 1. 安裝所需依賴套件
pip install -r requirements.txt

# 2. 增量同步 1000 天歷史並自動生成 GitHub Pages index.html 與本地儀表板
python main.py --sync --days 1000 --open

# 3. 批量下載 Garmin 運動 GPX 軌跡（自動跳過跑步機，存放於 marathon_gpx/）
python download_gpx.py --mode all --limit 50

# 4. 離線產出並開啟儀表板（不連網，使用現有快取資料）
python main.py --report --open

# 5. 安全發布至 GitHub Pages
python deploy.py
```

---

## 🔧 常見問答與疑難排解 (FAQ)

### Q1: 為什麼第一次執行會要求輸入代碼？
**答**：Garmin Connect 啟用了雙重認證（2FA/MFA）。初次登入時終端機提示輸入由 Email 或手機簡訊收到的驗證碼，驗證成功後會將安全 Token 儲存在使用者目錄（`~/.garminconnect`），後續執行即可直接免密碼靜默登入。

### Q2: 為什麼 GitHub 上看不到我的 GPX 檔案或 JSON 檔案？
**答**：這是專案的**隱私保護設計**。GPX 檔案含有真實的 GPS 跑步路線與私人地址資訊，JSON 檔案含有個人帳號識別碼；專案透過 [.gitignore](file:///c:/Users/tu-hs/OneDrive/文件/2022_0308_MASA/2022-0708/Projects_antigravity/GARMIN_CONNET_TRACK/.gitignore) 與 [deploy.py](file:///c:/Users/tu-hs/OneDrive/文件/2022_0308_MASA/2022-0708/Projects_antigravity/GARMIN_CONNET_TRACK/deploy.py) 嚴格過濾，只會將去識別化後「純生理數據」的靜態 HTML 與 JS 部署上線。

---

## 📜 授權協議 (License)

本專案採 MIT 授權條款釋出。歡迎耐力運動愛好者、馬拉松跑者與運動科學研究者自由使用與客製化。
