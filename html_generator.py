"""Garmin Health Dashboard HTML Generator with Light/Dark Mode, Bulletproof Rendering, and Outlier Trimming."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from insights_engine import InsightsEngine, WindowSummary, RecommendationItem, MonthlyStats, AnnualMarathonStats


def generate_dashboard_html(
    records: List[Dict[str, Any]],
    user_name: str = "Garmin User",
    last_synced: Optional[str] = None,
    output_path: Optional[Path] = None,
) -> Path:
    """Generates a standalone, responsive, interactive HTML dashboard with Light/Dark mode, bulletproof rendering and outlier trimming."""
    output_path = output_path or Path("garmin_health_dashboard.html")

    # 🛡️ Privacy Scrubbing: Ensure no user GUIDs or personal identifiers are published
    if not user_name or len(user_name) > 25 or "-" in user_name or user_name.lower().startswith("garmin user"):
        safe_user_name = "Garmin 運動員 (Athlete)"
    else:
        safe_user_name = user_name

    # 🛡️ Privacy Scrubbing: Strip raw_data and sanitize activity names to strictly generic sports metrics
    sanitized_records = []
    for r in records:
        r_copy = dict(r)
        r_copy.pop("raw_data", None)
        r_copy.pop("user_summary", None)
        r_copy.pop("userProfileId", None)
        r_copy.pop("uuid", None)
        
        # Sanitize activities
        clean_acts = []
        for act in r_copy.get("activities", []):
            act_type = (act.get("type") or "").lower()
            dist = act.get("distance_km") or 0.0
            if "treadmill" in act_type:
                clean_name = "跑步機跑步 (Treadmill Run)"
            elif dist >= 42.0:
                clean_name = "全馬賽事 / 訓練 (Marathon)"
            elif dist >= 21.0:
                clean_name = "半馬賽事 / LSD (Half Marathon)"
            elif dist >= 10.0:
                clean_name = "10K+ 長跑 (Long Run)"
            elif "trail" in act_type:
                clean_name = "越野跑 (Trail Run)"
            elif "track" in act_type:
                clean_name = "田徑場跑步 (Track Run)"
            elif "cycling" in act_type:
                clean_name = "單車騎乘 (Cycling)"
            elif "walking" in act_type or "hiking" in act_type:
                clean_name = "健走 / 徒步 (Walking / Hiking)"
            elif "swim" in act_type:
                clean_name = "游泳 (Swimming)"
            elif "running" in act_type:
                clean_name = "路跑 (Road Running)"
            else:
                clean_name = "體能訓練 (Workout)"

            clean_acts.append({
                "name": clean_name,
                "type": act.get("type", "running"),
                "duration_minutes": act.get("duration_minutes"),
                "distance_km": dist,
                "pace": act.get("pace"),
                "elevation_gain_m": act.get("elevation_gain_m", 0),
                "calories": act.get("calories"),
                "avg_hr": act.get("avg_hr"),
                "max_hr": act.get("max_hr"),
            })
        r_copy["activities"] = clean_acts
        sanitized_records.append(r_copy)

    engine = InsightsEngine(sanitized_records)
    daily_records = engine.filter_days(1)
    monthly_records = engine.filter_days(30)
    quarterly_records = engine.filter_days(90)
    all_records = engine.records

    daily_summary = engine.compute_summary(daily_records, "今日 (Daily)")
    monthly_summary = engine.compute_summary(monthly_records, "近 30 天 (Monthly)")
    quarterly_summary = engine.compute_summary(quarterly_records, "近 90 天 (Quarterly)")
    all_summary = engine.compute_summary(all_records, "全部歷史 (All-Time)")

    monthly_breakdown = engine.compute_monthly_breakdown()
    annual_marathons = engine.compute_annual_marathon_stats()
    recommendations = engine.generate_recommendations()

    payload = {
        "user_name": safe_user_name,
        "last_synced": last_synced or datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_records_count": len(all_records),
        "records": all_records,
        "summaries": {
            "daily": asdict(daily_summary),
            "monthly": asdict(monthly_summary),
            "quarterly": asdict(quarterly_summary),
            "all": asdict(all_summary),
        },
        "monthly_breakdown": [asdict(m) for m in monthly_breakdown],
        "annual_marathons": [asdict(a) for a in annual_marathons],
        "recommendations": [asdict(r) for r in recommendations],
    }

    payload_json = json.dumps(payload, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garmin 健康趨勢、長跑與每日/月度睡眠圖表分析 (支援淺色/深色模式)</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        garmin: {{
                            blue: '#007cc3',
                            dark: '#0f172a',
                            card: '#1e293b',
                            border: '#334155',
                            accent: '#38bdf8',
                            green: '#10b981',
                            amber: '#f59e0b',
                            rose: '#f43f5e',
                            purple: '#a855f7',
                            orange: '#f97316'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            transition: background 0.3s ease, color 0.3s ease;
        }}
        
        /* Dark Mode Theme Styles */
        html.dark body {{
            background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #131b2e 100%);
            color: #f1f5f9;
        }}
        html.dark .glass-card {{
            background: rgba(30, 41, 59, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        }}
        
        /* Light Mode Theme Styles */
        html:not(.dark) body {{
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
            color: #0f172a;
        }}
        html:not(.dark) .glass-card {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(12px);
            border: 1px solid #cbd5e1;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
            color: #0f172a;
        }}
        html:not(.dark) h1, html:not(.dark) h2, html:not(.dark) h3, html:not(.dark) h4 {{
            color: #0f172a !important;
        }}
        html:not(.dark) .text-slate-100, html:not(.dark) .text-slate-200 {{
            color: #0f172a;
        }}
        html:not(.dark) .text-slate-300 {{
            color: #1e293b !important;
        }}
        html:not(.dark) .text-slate-400 {{
            color: #334155 !important;
        }}
        html:not(.dark) .text-slate-500 {{
            color: #475569 !important;
        }}
        html:not(.dark) .text-white:not(button):not(.tab-btn):not([class*="bg-sky"]):not([class*="bg-blue"]):not([class*="bg-emerald"]):not([class*="bg-rose"]):not([class*="bg-amber"]):not([class*="bg-purple"]) {{
            color: #0f172a !important;
        }}

        /* Metric cards and panels in light mode */
        html:not(.dark) .bg-slate-900, html:not(.dark) .bg-slate-950 {{
            background-color: #ffffff;
            border-color: #cbd5e1;
            color: #0f172a;
        }}
        html:not(.dark) [class*="bg-slate-900/"] {{
            background-color: #ffffff;
            border-color: #cbd5e1 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            color: #0f172a;
        }}
        html:not(.dark) [class*="border-slate-800"],
        html:not(.dark) [class*="border-slate-700"],
        html:not(.dark) [class*="border-slate-700/60"] {{
            border-color: #cbd5e1 !important;
        }}
        html:not(.dark) .bg-slate-800 {{
            background-color: #e2e8f0;
            border-color: #cbd5e1;
            color: #1e293b;
        }}

        /* High-contrast palette for colored text in light mode */
        html:not(.dark) .text-sky-400, html:not(.dark) [class*="text-sky-400"] {{
            color: #0284c7 !important;
        }}
        html:not(.dark) .text-sky-300, html:not(.dark) [class*="text-sky-300"] {{
            color: #0369a1 !important;
        }}
        html:not(.dark) .text-purple-400, html:not(.dark) [class*="text-purple-400"] {{
            color: #7e22ce !important;
        }}
        html:not(.dark) .text-purple-300, html:not(.dark) [class*="text-purple-300"] {{
            color: #6b21a8 !important;
        }}
        html:not(.dark) .text-fuchsia-400, html:not(.dark) [class*="text-fuchsia-400"] {{
            color: #a21caf !important;
        }}
        html:not(.dark) .text-emerald-400, html:not(.dark) [class*="text-emerald-400"] {{
            color: #047857 !important;
        }}
        html:not(.dark) .text-emerald-300, html:not(.dark) [class*="text-emerald-300"] {{
            color: #065f46 !important;
        }}
        html:not(.dark) .text-rose-400, html:not(.dark) [class*="text-rose-400"] {{
            color: #be123c !important;
        }}
        html:not(.dark) .text-rose-500, html:not(.dark) [class*="text-rose-500"] {{
            color: #be123c !important;
        }}
        html:not(.dark) .text-amber-400, html:not(.dark) [class*="text-amber-400"] {{
            color: #b45309 !important;
        }}
        html:not(.dark) .text-amber-500, html:not(.dark) [class*="text-amber-500"] {{
            color: #b45309 !important;
        }}
        html:not(.dark) .text-orange-400, html:not(.dark) [class*="text-orange-400"] {{
            color: #c2410c !important;
        }}
        html:not(.dark) .text-indigo-400, html:not(.dark) [class*="text-indigo-400"] {{
            color: #4338ca !important;
        }}
        html:not(.dark) .text-indigo-300, html:not(.dark) [class*="text-indigo-300"] {{
            color: #3730a3 !important;
        }}

        /* Table & Divider Gridlines in Light Mode */
        html:not(.dark) table {{
            border-collapse: collapse;
        }}
        html:not(.dark) thead,
        html:not(.dark) thead.bg-slate-800,
        html:not(.dark) [class*="bg-slate-800"] {{
            background-color: #f1f5f9 !important;
            border-bottom: 2px solid #cbd5e1 !important;
            color: #0f172a !important;
        }}
        html:not(.dark) thead th {{
            color: #0f172a !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #94a3b8 !important;
        }}
        html:not(.dark) tbody td {{
            border-bottom: 1px solid #e2e8f0 !important;
            color: #0f172a !important;
        }}
        html:not(.dark) tbody tr:hover td {{
            background-color: #f1f5f9 !important;
        }}
        html:not(.dark) [class*="divide-slate-800"] > :not([hidden]) ~ :not([hidden]) {{
            border-color: #cbd5e1 !important;
        }}
        html:not(.dark) tr:hover {{
            background-color: rgba(241, 245, 249, 0.8);
        }}
        html:not(.dark) #help-modal .glass-card {{
            background-color: #ffffff;
            border-color: #cbd5e1;
        }}
        html:not(.dark) input {{
            background-color: #ffffff;
            border-color: #cbd5e1;
            color: #0f172a;
        }}

        /* ⭐ ALL Active/Highlighted buttons ALWAYS have crisp pure white text in both modes ⭐ */
        .tab-btn.active,
        html:not(.dark) .tab-btn.active,
        html.dark .tab-btn.active {{
            background: #007cc3 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(0, 124, 195, 0.35) !important;
        }}

        .plot-mode-btn.active,
        html:not(.dark) .plot-mode-btn.active,
        html.dark .plot-mode-btn.active {{
            background: #0284c7 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3) !important;
        }}

        .trim-level-btn.active,
        html:not(.dark) .trim-level-btn.active,
        html.dark .trim-level-btn.active {{
            background: #10b981 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3) !important;
        }}

        /* Recommendation active filters text */
        #rec-filter-all.bg-sky-600,
        #rec-filter-critical.bg-rose-600,
        #rec-filter-warning.bg-amber-600,
        #rec-filter-good.bg-emerald-600 {{
            color: #ffffff !important;
            font-weight: 700 !important;
        }}

        /* Unselected buttons in light mode */
        html:not(.dark) .tab-btn:not(.active) {{
            color: #475569 !important;
        }}
        html:not(.dark) .tab-btn:not(.active):hover {{
            color: #0f172a !important;
            background-color: rgba(226, 232, 240, 0.8) !important;
        }}

        html:not(.dark) .plot-mode-btn:not(.active) {{
            color: #475569 !important;
        }}
        html:not(.dark) .plot-mode-btn:not(.active):hover {{
            color: #0f172a !important;
        }}

        html:not(.dark) .trim-level-btn:not(.active) {{
            color: #64748b !important;
        }}
        html:not(.dark) .trim-level-btn:not(.active):hover {{
            color: #0f172a !important;
        }}

        /* Top Right Theme and Help buttons in light mode */
        html:not(.dark) #theme-toggle-btn,
        html:not(.dark) header button[onclick*="openHelpModal"] {{
            background-color: #ffffff !important;
            border-color: #cbd5e1 !important;
            color: #1e293b !important;
        }}
        html:not(.dark) #theme-toggle-btn:hover,
        html:not(.dark) header button[onclick*="openHelpModal"]:hover {{
            background-color: #f1f5f9 !important;
            border-color: #94a3b8 !important;
        }}

        /* Header Logo */
        .header-logo {{
            color: #ffffff !important;
        }}
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #64748b;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #475569;
        }}
    </style>
</head>
<body class="p-4 md:p-8">

    <div class="max-w-7xl mx-auto space-y-6">
        
        <!-- Top Header -->
        <header class="glass-card rounded-2xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-sky-600 via-indigo-600 to-cyan-400 flex items-center justify-center text-white font-black text-2xl shadow-lg shadow-sky-500/30 flex-shrink-0">
                    G
                </div>
                <div>
                    <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-white flex items-center gap-3">
                        Garmin 健康趨勢 & 每日 / 月度圖表分析
                        <span class="text-xs px-2.5 py-1 rounded-full bg-sky-500/20 text-sky-400 font-normal border border-sky-500/30">
                            Pro Analytics
                        </span>
                        <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-400 font-medium border border-emerald-500/30">
                            🛡️ 隱私保護 (純健康指標)
                        </span>
                    </h1>
                    <p class="text-sm text-slate-400 mt-1">
                        使用者: <span class="text-sky-500 font-semibold" id="header-username">{user_name}</span> 
                        &bull; 資料更新: <span id="header-synced" class="text-slate-400 font-medium">{last_synced or '剛剛'}</span>
                        &bull; 總記錄: <span class="text-amber-500 font-medium">{len(all_records)} 天</span> 
                        (<span class="text-sky-500 font-medium">{len(monthly_breakdown)} 個月份</span>)
                    </p>
                </div>
            </div>

            <!-- Time Window Switcher Tabs, Theme Switcher & Help Button -->
            <div class="flex flex-wrap items-center gap-2 self-stretch md:self-auto">
                <div class="flex flex-wrap bg-slate-900/80 p-1.5 rounded-xl border border-slate-700/60 justify-between gap-1 flex-1 md:flex-initial">
                    <button onclick="switchTab('daily')" id="tab-daily" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all text-slate-400 hover:text-white">
                        今日 (Daily)
                    </button>
                    <button onclick="switchTab('monthly')" id="tab-monthly" class="tab-btn active px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all text-slate-400 hover:text-white">
                        近 30 天 (30D)
                    </button>
                    <button onclick="switchTab('quarterly')" id="tab-quarterly" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all text-slate-400 hover:text-white">
                        近 90 天 (90D)
                    </button>
                    <button onclick="switchTab('all')" id="tab-all" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all text-slate-400 hover:text-white">
                        全部每日歷史 ({len(all_records)}D)
                    </button>
                    <button onclick="switchTab('comparison')" id="tab-comparison" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all text-amber-500 hover:text-white border border-amber-500/30">
                        📅 月度彙總趨勢 ({len(monthly_breakdown)}M)
                    </button>
                </div>

                <!-- 🏃‍♂️ Sport English & Training Principles Link -->
                <a href="sport_english.html" class="px-3.5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-xs sm:text-sm font-bold text-white transition-all flex items-center gap-1.5 shadow-md shadow-emerald-600/30 hover:scale-[1.02]" title="運動英語與訓練十大原則 (Sport English & Training Principles)">
                    <span>🏃‍♂️</span>
                    <span>運動英語與原則</span>
                </a>

                <!-- ☀️/🌙 Theme Toggle Button -->
                <button onclick="toggleTheme()" id="theme-toggle-btn" class="px-3.5 py-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-xs sm:text-sm font-semibold text-amber-400 hover:text-amber-300 border border-slate-700 transition-all flex items-center gap-1.5 shadow-sm" title="切換淺色 / 深色主題">
                    <span id="theme-icon">☀️</span>
                    <span id="theme-text">淺色模式</span>
                </button>

                <!-- ❓ Help Modal Button -->
                <button onclick="openHelpModal()" class="px-3.5 py-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-xs sm:text-sm font-semibold text-sky-400 hover:text-sky-300 border border-sky-500/40 hover:border-sky-400 transition-all flex items-center gap-1.5 shadow-sm">
                    <span>❓</span>
                    <span>指標指南</span>
                </button>
            </div>
        </header>

        <!-- 🎯 OUTLIER FILTER CONTROL & COMPARISON HUB BAR -->
        <div class="glass-card rounded-2xl p-4 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 border border-sky-500/30">
            <div class="flex items-center gap-3">
                <span class="text-2xl">🎯</span>
                <div>
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        異常值過濾與對比引擎 (Outlier Trimming & Live Comparison)
                        <span id="filter-active-badge" class="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                            未啟用 (全量原始數據)
                        </span>
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">
                        去除手錶未配戴（如1~2小時睡眠）、感測器雜訊或劇烈波動，計算更具代表性的強健均值。
                    </p>
                </div>
            </div>

            <!-- Controls: Toggle + Strength Level + Show Overlay Comparison -->
            <div class="flex flex-wrap items-center gap-3 self-stretch lg:self-auto">
                
                <!-- Main Checkbox Toggle -->
                <label class="flex items-center gap-2 cursor-pointer bg-slate-900 px-3 py-1.5 rounded-xl border border-sky-500/40 hover:border-sky-400 transition-all">
                    <input 
                        type="checkbox" 
                        id="trim-outliers-toggle" 
                        onchange="toggleOutliersFilter()" 
                        class="w-4 h-4 rounded text-sky-500 bg-slate-800 border-slate-600 focus:ring-sky-500 cursor-pointer"
                    />
                    <span class="text-xs sm:text-sm font-bold text-sky-400 select-none">
                        開啟去噪 (Trim Outliers)
                    </span>
                </label>

                <!-- Filter Ratio Level Buttons -->
                <div class="flex bg-slate-900 p-1 rounded-xl border border-slate-700" id="trim-level-group">
                    <button onclick="setTrimLevel(0.05)" id="trim-lvl-5" class="trim-level-btn active px-2.5 py-1 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
                        5% 輕度
                    </button>
                    <button onclick="setTrimLevel(0.10)" id="trim-lvl-10" class="trim-level-btn px-2.5 py-1 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
                        10% 標準
                    </button>
                    <button onclick="setTrimLevel(0.15)" id="trim-lvl-15" class="trim-level-btn px-2.5 py-1 rounded-lg text-xs font-medium transition-all text-slate-400 hover:text-white">
                        15% 強力
                    </button>
                </div>

                <!-- Show Comparison Overlay Checkbox -->
                <label class="flex items-center gap-1.5 cursor-pointer bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-700 hover:border-slate-600 text-xs text-amber-500 select-none">
                    <input 
                        type="checkbox" 
                        id="show-overlay-toggle" 
                        checked 
                        onchange="toggleOverlayComparison()" 
                        class="w-3.5 h-3.5 rounded text-amber-500 bg-slate-800 border-slate-600 cursor-pointer"
                    />
                    <span>📊 顯示原始對比線 (Overlay)</span>
                </label>

            </div>
        </div>

        <!-- 🏃‍♂️ SPECIAL ENDURANCE & MARATHON METRICS SECTION -->
        <section class="glass-card rounded-2xl p-6 border-l-4 border-l-orange-500" id="endurance-hub-section">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-2.5">
                    <span class="text-2xl">🏃‍♂️</span>
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            長跑耐力、馬拉松與熱量消耗分析 (Endurance & Mileage Hub)
                        </h2>
                        <p class="text-xs text-slate-400">追蹤 10K+ 長跑週期、全馬/半馬累積次數、總跑量與能量消耗 (卡路里)</p>
                    </div>
                </div>
                <span class="text-xs px-2.5 py-1 rounded bg-orange-500/20 text-orange-400 font-mono border border-orange-500/30 hidden sm:inline-block">
                    Long Run Tracker
                </span>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                
                <!-- 1. 10K+ Cadence Card -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                    <div class="text-xs text-slate-400 flex items-center justify-between">
                        <span>10K+ 長跑頻率 / 間隔</span>
                        <span class="text-orange-500">⏱️</span>
                    </div>
                    <div class="text-2xl font-bold text-orange-500 mt-2" id="kpi-10k-cadence">--</div>
                    <div class="text-xs text-slate-400 mt-1" id="kpi-10k-recency">距上次長跑: --</div>
                </div>

                <!-- 2. Running Mileage Card -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                    <div class="text-xs text-slate-400 flex items-center justify-between">
                        <span>總跑量 / 週均里程</span>
                        <span class="text-sky-500">🗺️</span>
                    </div>
                    <div class="text-2xl font-bold text-sky-500 mt-2" id="kpi-run-mileage">-- <span class="text-xs text-slate-400 font-normal">km</span></div>
                    <div class="text-xs text-slate-400 mt-1" id="kpi-run-weekly">週均: -- km / 共 -- 次</div>
                </div>

                <!-- 3. Marathon & Race Breakdown Card -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                    <div class="text-xs text-slate-400 flex items-center justify-between">
                        <span>馬拉松 / 長距離次數</span>
                        <span class="text-emerald-500">🏅</span>
                    </div>
                    <div class="text-xl font-bold text-emerald-500 mt-2" id="kpi-marathon-counts">--</div>
                    <div class="text-xs text-slate-400 mt-1" id="kpi-longest-run">最長單次: -- km</div>
                </div>

                <!-- 4. Run Calories & Burn Card -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800">
                    <div class="text-xs text-slate-400 flex items-center justify-between">
                        <span>跑步熱量消耗 (卡路里)</span>
                        <span class="text-rose-500">🔥</span>
                    </div>
                    <div class="text-2xl font-bold text-rose-500 mt-2" id="kpi-run-calories">-- <span class="text-xs text-slate-400 font-normal">kcal</span></div>
                    <div class="text-xs text-slate-400 mt-1" id="kpi-cal-per-km">平均約 -- kcal / km</div>
                </div>

            </div>

            <!-- ⏱️ 室外半馬與全馬年度平均耗時專區 (Annual Outdoor Marathon Time Spent - Outside Only) -->
            <div class="mt-6 pt-5 border-t border-slate-700/60 space-y-4" id="annual-marathon-stats-container">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                    <div class="flex items-center gap-2.5">
                        <span class="text-xl">⏱️</span>
                        <div>
                            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                                室外半馬與全馬年度平均耗時分析 (Annual Outdoor Marathon Time Spent)
                            </h3>
                            <p class="text-[11px] text-slate-400">嚴格限定室外路跑與賽事 (Outside Only，排除室內跑步機) &bull; 統計歷年半馬與全馬場次、平均完賽耗時、平均配速與最快成績</p>
                        </div>
                    </div>
                    <!-- Scope Switcher: Standard vs Extended/Ultra -->
                    <div class="flex items-center bg-slate-900/80 p-1 rounded-lg border border-slate-700/60 text-xs self-start md:self-auto">
                        <span class="text-slate-400 px-2 font-medium">賽制範圍:</span>
                        <button onclick="setMarathonScope('standard')" id="btn-mara-std" class="px-2.5 py-1 rounded font-medium transition-all bg-orange-600 text-white shadow-sm" title="標準賽制：半馬 21~25km、全馬 42~45km">
                            🎯 標準賽制 (Standard)
                        </button>
                        <button onclick="setMarathonScope('extended')" id="btn-mara-ext" class="px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="包含超長距離：半馬/LSD 21~42km、全馬/超馬 ≥42km (含50k~97k越野)">
                            ⛰️ 含超馬/LSD (Extended)
                        </button>
                    </div>
                </div>

                <!-- Annual Cards Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs" id="annual-marathon-cards">
                    <!-- Populated dynamically via JS -->
                </div>

                <!-- Detailed Side-by-Side Comparison Table -->
                <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/60">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
                            <tr>
                                <th class="py-2.5 px-3 font-semibold text-white">年度 (Year)</th>
                                <th class="py-2.5 px-3 text-emerald-400 font-semibold">🏃‍♂️ 半馬場次</th>
                                <th class="py-2.5 px-3 text-emerald-300 font-semibold">⏱️ 半馬平均耗時</th>
                                <th class="py-2.5 px-3 text-slate-400">⚡ 半馬均速</th>
                                <th class="py-2.5 px-3 text-emerald-400">⚡ 最快半馬紀錄</th>
                                <th class="py-2.5 px-3 text-rose-400 font-semibold border-l border-slate-700/60">🏅 全馬場次</th>
                                <th class="py-2.5 px-3 text-rose-300 font-semibold">⏱️ 全馬平均耗時</th>
                                <th class="py-2.5 px-3 text-slate-400">⚡ 全馬均速</th>
                                <th class="py-2.5 px-3 text-rose-400">⚡ 最快全馬紀錄</th>
                            </tr>
                        </thead>
                        <tbody id="annual-marathon-table-body" class="divide-y divide-slate-800">
                            <!-- Populated dynamically via JS -->
                        </tbody>
                    </table>
                </div>

                <!-- 🎯 標準全馬每小時配速與時速策略建議 (Standard Marathon Pace per Hour & Hourly Pacing Strategy) -->
                <div class="mt-5 pt-4 border-t border-slate-700/60 space-y-4" id="marathon-pace-suggestion-block">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                        <div class="flex items-center gap-2.5">
                            <span class="text-xl">🎯</span>
                            <div>
                                <h4 class="text-sm font-bold text-white flex items-center gap-2">
                                    標準全馬每小時配速與時速策略建議 (Marathon Pace & Speed per Hour)
                                </h4>
                                <p class="text-[11px] text-slate-400">標準全馬 42.195 km &bull; 依據您 2026 半馬 1h 55m 與全馬 4h 03m PB 精算各目標檔位之每小時推進時速 (km/h)、公里配速與 4 小時分段補給</p>
                            </div>
                        </div>
                        
                        <!-- Target Pace Select Buttons -->
                        <div class="flex flex-wrap items-center bg-slate-900/80 p-1 rounded-lg border border-slate-700/60 text-xs self-start md:self-auto gap-1">
                            <span class="text-slate-400 px-1 font-medium">目標:</span>
                            <button onclick="setMarathonTargetPace('sub4')" id="btn-pace-sub4" class="px-2 py-1 rounded font-medium transition-all bg-sky-600 text-white shadow-sm" title="目標 3:59:59 破4小時 (時速 10.55 km/h)">
                                ⚡ Sub-4 (3h 59m)
                            </button>
                            <button onclick="setMarathonTargetPace('sub415')" id="btn-pace-sub415" class="px-2 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="目標 4:14:59 (時速 9.93 km/h)">
                                🏃 4h 15m
                            </button>
                            <button onclick="setMarathonTargetPace('sub430')" id="btn-pace-sub430" class="px-2 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="目標 4:29:59 (時速 9.38 km/h，貼合2025均速)">
                                🎯 4h 30m
                            </button>
                            <button onclick="setMarathonTargetPace('sub445')" id="btn-pace-sub445" class="px-2 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="目標 4:44:59 (時速 8.88 km/h，貼合2026均速)">
                                🛡️ 4h 45m
                            </button>
                            <button onclick="setMarathonTargetPace('sub500')" id="btn-pace-sub500" class="px-2 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="目標 4:59:59 破5小時 (時速 8.44 km/h)">
                                🚶 Sub-5 (4h 59m)
                            </button>
                        </div>
                    </div>

                    <!-- Dynamic Personalized Form Alignment Notice -->
                    <div class="p-3 rounded-xl bg-sky-950/30 border border-sky-500/30 flex items-start gap-2.5 text-xs">
                        <span class="text-base">💡</span>
                        <div class="space-y-0.5">
                            <span class="font-bold text-sky-400" id="pace-advice-title">體能對標：具備衝刺 Sub-4 (破4小時) 的強大有氧實力！</span>
                            <p class="text-slate-300 text-[11px]" id="pace-advice-desc">您在 2026 年室外半馬跑出 1h 52m 42s (均速 5:20/km)，歷史全馬最佳 4h 03m 12s (5:46/km)。依據運動生理學 VDOT 模型，半馬 1h52m 具備全馬 3h 54m ~ 3h 58m 的實力！建議將每小時時速精準控制在 10.55 km/h，配合定時補給即可成功叩關。</p>
                        </div>
                    </div>

                    <!-- 4 Core Target Stats Cards -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                        <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                            <div class="text-slate-400">⚡ 建議每小時時速</div>
                            <div class="text-lg font-bold text-sky-400 font-mono mt-0.5" id="pace-kpi-speed">10.55 km/h</div>
                            <div class="text-[10px] text-slate-500" id="pace-kpi-dist-hr">每小時推進 10.55 公里</div>
                        </div>
                        <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                            <div class="text-slate-400">⏱️ 每公里平均配速</div>
                            <div class="text-lg font-bold text-emerald-400 font-mono mt-0.5" id="pace-kpi-pace">5:41 / km</div>
                            <div class="text-[10px] text-slate-500">建議區間: 5:38 ~ 5:44</div>
                        </div>
                        <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                            <div class="text-slate-400">🚩 半馬折返點預計</div>
                            <div class="text-lg font-bold text-amber-400 font-mono mt-0.5" id="pace-kpi-half">1h 59m 59s</div>
                            <div class="text-[10px] text-slate-500">21.0975 km 半程檢核</div>
                        </div>
                        <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                            <div class="text-slate-400">📏 每 5 公里分段耗時</div>
                            <div class="text-lg font-bold text-purple-400 font-mono mt-0.5" id="pace-kpi-5k">28m 25s</div>
                            <div class="text-[10px] text-slate-500">10K 耗時約 56m 50s</div>
                        </div>
                    </div>

                    <!-- Hourly Progress & Fueling Strategy Breakdown -->
                    <div class="bg-slate-900/60 rounded-xl border border-slate-800 p-3 space-y-2">
                        <div class="flex items-center justify-between text-xs text-slate-300 font-semibold border-b border-slate-800 pb-2">
                            <span class="flex items-center gap-1.5">
                                <span>📋</span>
                                <span>全馬 4 小時各階段里程推進與補給作戰方針 (Hourly Progression & Strategy)</span>
                            </span>
                            <span class="text-[11px] text-slate-400 font-normal">等速巡航 / 均速推進</span>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-2.5 text-xs pt-1" id="hourly-progression-cards">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>

                    <!-- Complete Marathon Pace Benchmark Table -->
                    <div class="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/40">
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
                                <tr>
                                    <th class="py-2 px-3 text-white font-semibold">全馬目標成績</th>
                                    <th class="py-2 px-3 text-sky-400 font-semibold">⚡ 每小時時速 (Speed)</th>
                                    <th class="py-2 px-3 text-emerald-400 font-semibold">⏱️ 每公里配速 (Pace)</th>
                                    <th class="py-2 px-3 text-slate-300">10 km 耗時</th>
                                    <th class="py-2 px-3 text-amber-300">半馬 21.1k 耗時</th>
                                    <th class="py-2 px-3 text-purple-300">30 km 耗時</th>
                                    <th class="py-2 px-3 text-slate-400">心率與體能建議</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800 font-mono text-[11px]">
                                <tr class="hover:bg-slate-800/50 transition-colors bg-sky-950/20">
                                    <td class="py-2 px-3 font-bold text-sky-400">⚡ Sub-4 (3:59:59)</td>
                                    <td class="py-2 px-3 font-bold text-sky-400">10.55 km/h</td>
                                    <td class="py-2 px-3 font-bold text-emerald-400">5:41 / km</td>
                                    <td class="py-2 px-3 text-slate-300">56m 52s</td>
                                    <td class="py-2 px-3 text-amber-400">1h 59m 59s</td>
                                    <td class="py-2 px-3 text-purple-400">2h 50m 38s</td>
                                    <td class="py-2 px-3 text-slate-400 font-sans">衝刺破4！對標您半馬 1h52m 與全馬 4h03m PB</td>
                                </tr>
                                <tr class="hover:bg-slate-800/50 transition-colors">
                                    <td class="py-2 px-3 font-semibold text-white">🏃 Sub-4:15 (4:14:59)</td>
                                    <td class="py-2 px-3 text-sky-300">9.93 km/h</td>
                                    <td class="py-2 px-3 text-emerald-300">6:02 / km</td>
                                    <td class="py-2 px-3 text-slate-300">1h 00m 26s</td>
                                    <td class="py-2 px-3 text-amber-300">2h 07m 30s</td>
                                    <td class="py-2 px-3 text-purple-300">3h 01m 18s</td>
                                    <td class="py-2 px-3 text-slate-400 font-sans">穩健發揮，後段餘力充足，低撞牆風險</td>
                                </tr>
                                <tr class="hover:bg-slate-800/50 transition-colors">
                                    <td class="py-2 px-3 font-semibold text-white">🎯 Sub-4:30 (4:29:59)</td>
                                    <td class="py-2 px-3 text-sky-300">9.38 km/h</td>
                                    <td class="py-2 px-3 text-emerald-300">6:24 / km</td>
                                    <td class="py-2 px-3 text-slate-300">1h 04m 00s</td>
                                    <td class="py-2 px-3 text-amber-300">2h 15m 00s</td>
                                    <td class="py-2 px-3 text-purple-300">3h 12m 00s</td>
                                    <td class="py-2 px-3 text-slate-400 font-sans">貼合 2025 年全馬均速 (4h 34m)，Zone 2 有氧舒適圈</td>
                                </tr>
                                <tr class="hover:bg-slate-800/50 transition-colors">
                                    <td class="py-2 px-3 font-semibold text-white">🛡️ Sub-4:45 (4:44:59)</td>
                                    <td class="py-2 px-3 text-sky-300">8.88 km/h</td>
                                    <td class="py-2 px-3 text-emerald-300">6:45 / km</td>
                                    <td class="py-2 px-3 text-slate-300">1h 07m 32s</td>
                                    <td class="py-2 px-3 text-amber-300">2h 22m 29s</td>
                                    <td class="py-2 px-3 text-purple-300">3h 22m 41s</td>
                                    <td class="py-2 px-3 text-slate-400 font-sans">貼合 2026 年全馬均速 (4h 44m)，安全巡航完賽</td>
                                </tr>
                                <tr class="hover:bg-slate-800/50 transition-colors">
                                    <td class="py-2 px-3 font-semibold text-white">🚶 Sub-5:00 (4:59:59)</td>
                                    <td class="py-2 px-3 text-sky-300">8.44 km/h</td>
                                    <td class="py-2 px-3 text-emerald-300">7:06 / km</td>
                                    <td class="py-2 px-3 text-slate-300">1h 11m 06s</td>
                                    <td class="py-2 px-3 text-amber-300">2h 30m 00s</td>
                                    <td class="py-2 px-3 text-purple-300">3h 33m 17s</td>
                                    <td class="py-2 px-3 text-slate-400 font-sans">基礎有氧慢跑，高溫或多坡賽道保守配速</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- 📊 SPECIAL RUNNING DISTANCE HISTOGRAM SECTION (次數 vs 公里數, 室內外分組, 年/月/時序篩選) -->
        <section class="glass-card rounded-2xl p-6 border-l-4 border-l-sky-500 space-y-4" id="distance-histogram-section">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-2xl">📊</span>
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            單次跑步里程分佈直方圖 (Distance Distribution Histogram)
                        </h2>
                        <p class="text-xs text-slate-400">次數 (Frequency) vs 公里數 (Distance Bins) &bull; 室內 / 室外分組對比 &bull; 支援年份 (Year)、月份 (Month) 與時序 (Trailing) 鑽取</p>
                    </div>
                </div>
                <!-- Control Badges: Quick Switchers -->
                <div class="flex flex-wrap items-center gap-2 text-xs">
                    <!-- Grouping Mode Switcher -->
                    <div class="flex items-center bg-slate-900/80 p-1 rounded-lg border border-slate-700/60">
                        <span class="text-slate-400 px-2 font-medium">分組:</span>
                        <button onclick="setHistGroupMode('stacked')" id="btn-hist-stacked" class="px-2.5 py-1 rounded font-medium transition-all bg-sky-600 text-white shadow-sm" title="室內與室外堆疊顯示總次數">
                            🔀 堆疊 (Stacked)
                        </button>
                        <button onclick="setHistGroupMode('grouped')" id="btn-hist-grouped" class="px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="室內與室外並排對比">
                            ⏸️ 並排 (Grouped)
                        </button>
                        <button onclick="setHistGroupMode('split_trail')" id="btn-hist-split" class="px-2.5 py-1 rounded font-medium transition-all text-emerald-400 hover:text-white" title="拆分室內、室外路跑與越野山徑 (Trail)">
                            ⛰️ 含越野 (Trail)
                        </button>
                    </div>

                    <!-- Bin Strategy Switcher -->
                    <div class="flex items-center bg-slate-900/80 p-1 rounded-lg border border-slate-700/60">
                        <span class="text-slate-400 px-2 font-medium">級距:</span>
                        <button onclick="setHistBinMode('athletic')" id="btn-bin-athletic" class="px-2.5 py-1 rounded font-medium transition-all bg-sky-600 text-white shadow-sm" title="經典跑馬訓練分級 (<3k, 3-5k, 5-8k, 8-10k, 10-15k, 15-21k, 21-30k, 30-42k, 42k+)">
                            🎯 跑馬分級
                        </button>
                        <button onclick="setHistBinMode('fixed_2k')" id="btn-bin-2k" class="px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="每 2 公里固定級距">
                            📏 每 2 km
                        </button>
                        <button onclick="setHistBinMode('fixed_5k')" id="btn-bin-5k" class="px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white" title="每 5 公里固定級距">
                            📐 每 5 km
                        </button>
                    </div>
                </div>
            </div>

            <!-- Time Filter Toolbar (treil by YEAR or MONTH) -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800 text-xs">
                <div class="flex flex-wrap items-center gap-2">
                    <span class="text-slate-300 font-semibold flex items-center gap-1.5">
                        <span>⏳</span>
                        <span>時序鑽取 (Time Slicing):</span>
                    </span>
                    <button onclick="setHistTimeMode('all')" id="btn-time-all" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-sky-600 text-white shadow-sm">
                        🌐 全歷史 (All-Time)
                    </button>
                    <button onclick="setHistTimeMode('year')" id="btn-time-year" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 text-slate-300 hover:bg-slate-700">
                        📅 依年份 (By Year)
                    </button>
                    <button onclick="setHistTimeMode('month')" id="btn-time-month" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 text-slate-300 hover:bg-slate-700">
                        📆 依月份 (By Month)
                    </button>
                    <button onclick="setHistTimeMode('trailing')" id="btn-time-trailing" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 text-slate-300 hover:bg-slate-700">
                        ⏱️ 滾動時序 (Trailing)
                    </button>
                    <button onclick="setHistTimeMode('yoy_year')" id="btn-time-yoy_year" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 text-purple-400 hover:bg-slate-700" title="年度與年度同比直方圖對比 (例如 2026 vs 2025)">
                        📅 年度 YoY
                    </button>
                    <button onclick="setHistTimeMode('yoy_month')" id="btn-time-yoy_month" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 text-fuchsia-400 hover:bg-slate-700" title="跨年同月份同比直方圖對比 (例如 2026-10 vs 2025-10)">
                        🗓️ 月度 YoY
                    </button>
                    <button onclick="setHistTimeMode('mom')" id="btn-time-mom" class="px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 text-emerald-400 hover:bg-slate-700" title="連續相鄰月份環比直方圖對比 (例如 2026-10 vs 2026-09)">
                        🔄 月度 MoM
                    </button>
                </div>

                <!-- Dynamic Sub-Select dropdowns -->
                <div class="flex items-center gap-2">
                    <!-- Year select -->
                    <div id="hist-year-select-wrap" class="hidden flex items-center gap-1.5">
                        <span class="text-slate-400">選擇年份:</span>
                        <select id="hist-year-select" onchange="onHistYearChange()" class="bg-slate-800 text-sky-400 border border-slate-700 rounded-lg px-2.5 py-1 focus:outline-none focus:border-sky-500 font-mono">
                            <!-- Populated dynamically -->
                        </select>
                    </div>

                    <!-- Month select -->
                    <div id="hist-month-select-wrap" class="hidden flex items-center gap-1.5">
                        <span class="text-slate-400">選擇月份:</span>
                        <select id="hist-month-select" onchange="onHistMonthChange()" class="bg-slate-800 text-sky-400 border border-slate-700 rounded-lg px-2.5 py-1 focus:outline-none focus:border-sky-500 font-mono">
                            <!-- Populated dynamically -->
                        </select>
                    </div>

                    <!-- Trailing period select -->
                    <div id="hist-trailing-select-wrap" class="hidden flex items-center gap-1.5">
                        <span class="text-slate-400">滾動週期:</span>
                        <select id="hist-trailing-select" onchange="onHistTrailingChange()" class="bg-slate-800 text-amber-400 border border-slate-700 rounded-lg px-2.5 py-1 focus:outline-none focus:border-amber-500 font-mono">
                            <option value="30">近 30 天 (30 Days)</option>
                            <option value="90">近 90 天 (90 Days)</option>
                            <option value="180">近 180 天 (半年)</option>
                            <option value="365" selected>近 365 天 (1 年)</option>
                            <option value="730">近 730 天 (2 年)</option>
                        </select>
                    </div>

                    <!-- YoY Year select -->
                    <div id="hist-yoy-year-select-wrap" class="hidden flex items-center gap-1.5">
                        <span class="text-purple-400 font-semibold">年度 YoY:</span>
                        <select id="hist-yoy-year-select" onchange="onHistYoYYearChange()" class="bg-slate-800 text-purple-400 border border-purple-500/50 rounded-lg px-2.5 py-1 focus:outline-none focus:border-purple-400 font-mono">
                            <!-- Populated dynamically -->
                        </select>
                    </div>

                    <!-- YoY Month select -->
                    <div id="hist-yoy-month-select-wrap" class="hidden flex items-center gap-1.5">
                        <span class="text-fuchsia-400 font-semibold">月度 YoY:</span>
                        <select id="hist-yoy-month-select" onchange="onHistYoYMonthChange()" class="bg-slate-800 text-fuchsia-400 border border-fuchsia-500/50 rounded-lg px-2.5 py-1 focus:outline-none focus:border-fuchsia-400 font-mono">
                            <!-- Populated dynamically -->
                        </select>
                    </div>

                    <!-- MoM select -->
                    <div id="hist-mom-select-wrap" class="hidden flex items-center gap-1.5">
                        <span class="text-emerald-400 font-semibold">月度 MoM:</span>
                        <select id="hist-mom-select" onchange="onHistMoMChange()" class="bg-slate-800 text-emerald-400 border border-emerald-500/50 rounded-lg px-2.5 py-1 focus:outline-none focus:border-emerald-400 font-mono">
                            <!-- Populated dynamically -->
                        </select>
                    </div>

                    <span class="text-slate-400 text-[11px]" id="hist-current-filter-desc">顯示: 全部歷史累計</span>
                </div>
            </div>

            <!-- Dynamic Aggregate Metric Badges -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 text-xs">
                <div class="bg-slate-900/70 p-2.5 rounded-xl border border-slate-800">
                    <div class="text-slate-400">🏃 篩選總跑步</div>
                    <div class="text-base font-bold text-white mt-0.5" id="hist-stat-total">-- 次</div>
                    <div class="text-[10px] text-slate-500" id="hist-stat-total-km">共 -- km</div>
                </div>
                <div class="bg-slate-900/70 p-2.5 rounded-xl border border-amber-500/20">
                    <div class="text-amber-400">🏠 室內跑步機</div>
                    <div class="text-base font-bold text-amber-500 mt-0.5" id="hist-stat-indoor">-- 次</div>
                    <div class="text-[10px] text-amber-400/80" id="hist-stat-indoor-detail">-- km (佔 --%)</div>
                </div>
                <div class="bg-slate-900/70 p-2.5 rounded-xl border border-sky-500/20">
                    <div class="text-sky-400">🌲 室外路跑/田徑</div>
                    <div class="text-base font-bold text-sky-400 mt-0.5" id="hist-stat-outdoor">-- 次</div>
                    <div class="text-[10px] text-sky-400/80" id="hist-stat-outdoor-detail">-- km (佔 --%)</div>
                </div>
                <div class="bg-slate-900/70 p-2.5 rounded-xl border border-emerald-500/20">
                    <div class="text-emerald-400">⛰️ 越野 (Trail)/登山</div>
                    <div class="text-base font-bold text-emerald-400 mt-0.5" id="hist-stat-trail">-- 次</div>
                    <div class="text-[10px] text-emerald-400/80" id="hist-stat-trail-detail">-- km</div>
                </div>
                <div class="bg-slate-900/70 p-2.5 rounded-xl border border-slate-800">
                    <div class="text-slate-400">🏆 最常跑區間 (眾數)</div>
                    <div class="text-sm font-bold text-orange-400 mt-0.5 truncate" id="hist-stat-modal">--</div>
                    <div class="text-[10px] text-slate-500" id="hist-stat-modal-count">-- 次</div>
                </div>
                <div class="bg-slate-900/70 p-2.5 rounded-xl border border-slate-800">
                    <div class="text-slate-400">🚀 最長單次跑量</div>
                    <div class="text-base font-bold text-rose-400 mt-0.5" id="hist-stat-max-dist">-- km</div>
                    <div class="text-[10px] text-slate-500" id="hist-stat-avg-dist">單次平均: -- km</div>
                </div>
            </div>

            <!-- Canvas Container -->
            <div class="h-72 sm:h-80 md:h-96 relative w-full">
                <canvas id="chart-distance-histogram"></canvas>
            </div>

            <!-- Collapsible Detailed Breakdown Drawer -->
            <div class="border-t border-slate-800/80 pt-3">
                <button onclick="toggleHistTable()" id="btn-toggle-hist-table" class="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 transition-all">
                    <span id="hist-table-toggle-icon">▶</span>
                    <span>檢視各距離區間明細數據表 (Distance Bins Data Table)</span>
                </button>
                <div id="hist-table-container" class="hidden mt-3 overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
                            <tr>
                                <th class="py-2 px-3">距離區間 (Bucket)</th>
                                <th class="py-2 px-3 text-amber-400">室內次數 (Indoor)</th>
                                <th class="py-2 px-3 text-sky-400">室外次數 (Outdoor)</th>
                                <th class="py-2 px-3 text-emerald-400">越野次數 (Trail)</th>
                                <th class="py-2 px-3 text-white font-bold">合計次數</th>
                                <th class="py-2 px-3 text-slate-400">佔比 (%)</th>
                                <th class="py-2 px-3 text-slate-400">累積里程 (km)</th>
                            </tr>
                        </thead>
                        <tbody id="hist-table-body" class="divide-y divide-slate-800">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- General Health KPI Cards Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4" id="kpi-cards">
            <!-- RHR Card -->
            <div class="glass-card rounded-xl p-4 transition-all hover:scale-[1.02]">
                <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                    <span>靜止心率 (RHR)</span>
                    <span class="text-rose-500">❤️</span>
                </div>
                <div class="text-2xl font-bold text-white mt-2" id="kpi-rhr">-- <span class="text-xs font-normal text-slate-400">bpm</span></div>
                <div class="text-xs mt-1 text-slate-400" id="kpi-rhr-sub">--</div>
            </div>

            <!-- HRV Card -->
            <div class="glass-card rounded-xl p-4 transition-all hover:scale-[1.02]">
                <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                    <span>心率變異度 (HRV)</span>
                    <span class="text-emerald-500">⚡</span>
                </div>
                <div class="text-2xl font-bold text-white mt-2" id="kpi-hrv">-- <span class="text-xs font-normal text-slate-400">ms</span></div>
                <div class="text-xs mt-1 text-slate-400" id="kpi-hrv-sub">--</div>
            </div>

            <!-- Sleep Card -->
            <div class="glass-card rounded-xl p-4 transition-all hover:scale-[1.02]">
                <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                    <span>睡眠分數 / 時長</span>
                    <span class="text-indigo-500">🌙</span>
                </div>
                <div class="text-2xl font-bold text-white mt-2" id="kpi-sleep">--</div>
                <div class="text-xs mt-1 text-slate-400" id="kpi-sleep-sub">--</div>
            </div>

            <!-- Body Battery Card -->
            <div class="glass-card rounded-xl p-4 transition-all hover:scale-[1.02]">
                <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                    <span>電量充電 / 壓力</span>
                    <span class="text-amber-500">🔋</span>
                </div>
                <div class="text-2xl font-bold text-white mt-2" id="kpi-bb">--</div>
                <div class="text-xs mt-1 text-slate-400" id="kpi-bb-sub">--</div>
            </div>

            <!-- Steps Card -->
            <div class="glass-card rounded-xl p-4 transition-all hover:scale-[1.02]">
                <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                    <span>日均步數 / 達標</span>
                    <span class="text-sky-500">👟</span>
                </div>
                <div class="text-2xl font-bold text-white mt-2" id="kpi-steps">--</div>
                <div class="text-xs mt-1 text-slate-400" id="kpi-steps-sub">--</div>
            </div>

            <!-- Fitness Card -->
            <div class="glass-card rounded-xl p-4 transition-all hover:scale-[1.02]">
                <div class="text-xs text-slate-400 font-medium flex items-center justify-between">
                    <span>VO2 Max / 呼吸</span>
                    <span class="text-purple-500">🫁</span>
                </div>
                <div class="text-2xl font-bold text-white mt-2" id="kpi-fitness">--</div>
                <div class="text-xs mt-1 text-slate-400" id="kpi-fitness-sub">--</div>
            </div>
        </div>

        <!-- 🩺 TODAY'S EXECUTIVE HEALTH & READINESS ASSESSMENT SECTION -->
        <section class="glass-card rounded-2xl p-6 border-l-4 border-l-sky-500 shadow-xl" id="today-assessment-section">
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 pb-4 border-b border-slate-700/60">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white text-2xl shadow-md flex-shrink-0">
                        🩺
                    </div>
                    <div>
                        <h2 class="text-lg md:text-xl font-bold text-white flex items-center gap-2">
                            今日即時健康評估與訓練恢復指南
                            <span class="text-xs px-2.5 py-0.5 rounded-full bg-sky-500/20 text-sky-400 font-semibold border border-sky-500/30">
                                今日即時診斷
                            </span>
                        </h2>
                        <p class="text-xs text-slate-400 mt-0.5" id="today-assessment-subtitle">
                            綜合最新訓練完備度 (Readiness)、夜間 HRV 恢復、睡眠結構與近期跑步負荷之個人化實戰解讀。
                        </p>
                    </div>
                </div>
                <div class="flex flex-wrap items-center gap-2 text-xs" id="today-status-badges">
                    <!-- Dynamic badges populated via JS -->
                </div>
            </div>

            <!-- 3 Columns Diagnosis Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 mt-5">
                <!-- Col 1: 🫀 當前疲勞與恢復診斷 -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
                            <span class="flex items-center gap-1.5 text-rose-400">
                                <span>🫀</span> 當前疲勞與恢復診斷
                            </span>
                            <span id="col-recovery-badge">--</span>
                        </div>
                        <h4 class="text-sm font-bold text-white mb-1.5" id="col-recovery-title">--</h4>
                        <p class="text-xs text-slate-300 leading-relaxed" id="col-recovery-desc">--</p>
                    </div>
                    <div class="mt-3 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-400" id="col-recovery-meta">
                        --
                    </div>
                </div>

                <!-- Col 2: 🏃 近期課表負荷關聯 -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
                            <span class="flex items-center gap-1.5 text-orange-400">
                                <span>🏃</span> 近期課表與負荷追蹤
                            </span>
                            <span id="col-workload-badge">--</span>
                        </div>
                        <h4 class="text-sm font-bold text-white mb-1.5" id="col-workload-title">--</h4>
                        <p class="text-xs text-slate-300 leading-relaxed" id="col-workload-desc">--</p>
                    </div>
                    <div class="mt-3 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-400" id="col-workload-meta">
                        --
                    </div>
                </div>

                <!-- Col 3: 🎯 今日專屬訓練與生活建議 -->
                <div class="bg-slate-900/70 p-4 rounded-xl border border-slate-800 flex flex-col justify-between" id="col-action-box">
                    <div>
                        <div class="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
                            <span class="flex items-center gap-1.5 text-emerald-400">
                                <span>🎯</span> 今日具體訓練執行方針
                            </span>
                            <span id="col-action-badge">--</span>
                        </div>
                        <h4 class="text-sm font-bold text-white mb-1.5" id="col-action-title">--</h4>
                        <p class="text-xs text-slate-300 leading-relaxed" id="col-action-desc">--</p>
                    </div>
                    <div class="mt-3 pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-400" id="col-action-meta">
                        --
                    </div>
                </div>
            </div>
        </section>

        <!-- 📊 PLOTS MODE SWITCHER: DAILY PLOTS vs MONTHLY PLOTS -->
        <div class="flex items-center justify-between glass-card p-3 rounded-xl border border-sky-500/30">
            <div class="flex items-center gap-2">
                <span class="text-lg">📈</span>
                <span class="font-bold text-sm text-slate-200">圖表檢視模式 (Plots View Mode):</span>
            </div>
            <div class="flex bg-slate-900 p-1 rounded-lg border border-slate-700">
                <button onclick="setPlotMode('daily')" id="plot-mode-daily" class="plot-mode-btn active px-4 py-1.5 rounded-md text-xs sm:text-sm font-medium transition-all text-slate-300">
                    📈 每日走勢圖 (Daily Plots)
                </button>
                <button onclick="setPlotMode('monthly')" id="plot-mode-monthly" class="plot-mode-btn px-4 py-1.5 rounded-md text-xs sm:text-sm font-medium transition-all text-slate-300">
                    📅 月度統計圖 (Monthly Plots)
                </button>
            </div>
        </div>

        <!-- 📈 1. DAILY PLOTS SECTION (Day-by-Day Curves) -->
        <div id="daily-plots-container" class="space-y-6">
            <div class="flex items-center justify-between px-1">
                <h3 class="text-base font-bold text-sky-500 flex items-center gap-2">
                    <span>📈</span> 每日原始數據走勢圖 (Daily Time Series Plots)
                </h3>
                <span class="text-xs text-slate-400" id="daily-outlier-hint">
                    每一個數據點代表一天的實際測量值
                </span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Daily Chart 1: Resting HR & HRV Status -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
                            每日靜止心率 (RHR) 與 HRV 恢復走勢
                        </h3>
                        <span class="text-xs text-slate-400">每日點 (bpm / ms)</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-rhr-hrv"></canvas>
                    </div>
                </div>

                <!-- Daily Chart 2: Sleep Stages Breakdown -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-indigo-500 inline-block"></span>
                            每日睡眠時長與階段分佈 (深層 / REM / 淺層 / 清醒)
                        </h3>
                        <span class="text-xs text-slate-400">堆疊時長 (小時)</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-sleep"></canvas>
                    </div>
                </div>

                <!-- Daily Chart 3: Body Battery & Stress -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
                            每日身體電量充放 (+Charge / -Drain) 與壓力
                        </h3>
                        <span class="text-xs text-slate-400">電量點數 vs 壓力指數</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-bb-stress"></canvas>
                    </div>
                </div>

                <!-- Daily Chart 4: Steps & Intensity Minutes -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-sky-500 inline-block"></span>
                            每日步數、目標達成與中高強度運動
                        </h3>
                        <span class="text-xs text-slate-400">步數 vs 分鐘數</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-activity"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- 📅 2. MONTHLY PLOTS SECTION (Month-by-Month Aggregates & Stacked Sleep Stages) -->
        <div id="monthly-plots-container" class="space-y-6 hidden">
            <div class="flex items-center justify-between px-1">
                <h3 class="text-base font-bold text-amber-500 flex items-center gap-2">
                    <span>📅</span> 月度彙總趨勢圖 (Monthly Aggregate Plots)
                </h3>
                <span class="text-xs text-slate-400" id="monthly-outlier-indicator">
                    統計方式: 全量平均 (打勾上方可開啟截尾去噪與雙軌對比)
                </span>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                <!-- ⭐ Monthly Chart 1: Monthly Stacked Sleep Stages Breakdown ⭐ -->
                <div class="glass-card rounded-2xl p-5 border-l-4 border-l-indigo-500">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-indigo-500 inline-block"></span>
                            平均每月睡眠時長與階段分佈 (深層 / REM / 淺層 / 清醒)
                        </h3>
                        <span class="text-xs text-indigo-400 font-mono" id="monthly-sleep-legend">堆疊時長 (小時)</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-monthly-sleep-stages"></canvas>
                    </div>
                </div>

                <!-- Monthly Chart 2: Monthly Mileage & 10K+ Counts -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-sky-500 inline-block"></span>
                            每月總跑量 (km) 與 10K+ 長跑次數
                        </h3>
                        <span class="text-xs text-slate-400">月跑量 vs 長跑次數</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-monthly-mileage"></canvas>
                    </div>
                </div>

                <!-- Monthly Chart 3: Monthly RHR & HRV Evolution -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
                            月均靜止心率 (RHR) 與 HRV 自律神經趨勢
                        </h3>
                        <span class="text-xs text-slate-400" id="monthly-vitals-legend">實線: 均值 &bull; 虛線: 對比線</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-monthly-vitals"></canvas>
                    </div>
                </div>

                <!-- Monthly Chart 4: Monthly Calories & Races -->
                <div class="glass-card rounded-2xl p-5">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                            <span class="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
                            月度運動總卡路里 (kcal) 與賽事場次
                        </h3>
                        <span class="text-xs text-slate-400">卡路里 vs 全馬/半馬</span>
                    </div>
                    <div class="h-64 sm:h-72">
                        <canvas id="chart-monthly-calories"></canvas>
                    </div>
                </div>

                <!-- ⭐ Monthly Chart 5: YoY & MoM Growth Dynamics (Full Width) ⭐ -->
                <div class="glass-card rounded-2xl p-5 col-span-1 lg:col-span-2 border-l-4 border-l-purple-500">
                    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-4">
                        <div>
                            <h3 class="font-bold text-slate-200 flex items-center gap-2 text-sm md:text-base">
                                <span class="w-3 h-3 rounded-full bg-purple-500 inline-block"></span>
                                跑量 YoY (年同比) 與 MoM (月環比) 成長走勢圖
                            </h3>
                            <p class="text-xs text-slate-400 mt-0.5">跨年度同期跑量變化 (YoY %) 與連續月度訓練增減 (MoM %) &bull; 雙軸呈現月跑量與增長率</p>
                        </div>
                        <div class="flex flex-wrap items-center gap-3 text-xs">
                            <span class="flex items-center gap-1.5 text-purple-400 font-mono">
                                <span class="inline-block w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                                YoY 年增長率 (%)
                            </span>
                            <span class="flex items-center gap-1.5 text-emerald-400 font-mono">
                                <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                                MoM 月增長率 (%)
                            </span>
                            <span class="flex items-center gap-1.5 text-sky-400 font-mono">
                                <span class="inline-block w-2.5 h-2.5 rounded-full bg-sky-400"></span>
                                當月跑量 (km)
                            </span>
                            <span class="flex items-center gap-1.5 text-slate-400 font-mono">
                                <span class="inline-block w-2.5 h-2.5 rounded-full bg-slate-500"></span>
                                去年同期 (km)
                            </span>
                        </div>
                    </div>
                    <div class="h-64 sm:h-72 md:h-80">
                        <canvas id="chart-monthly-yoy-mom"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- 📋 STANDALONE MONTHLY COMPARISON TABLE SECTION (Never Hidden) -->
        <section class="glass-card rounded-2xl p-6" id="monthly-table-section">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-4 border-b border-slate-700/60 pb-3">
                <div>
                    <h3 class="font-bold text-white text-lg flex items-center gap-2">
                        <span>📋</span> 各月份歷史數據明細對照表 (Monthly Historical Breakdown)
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">跨月份檢視跑量、MoM 環比增長、YoY 同比增長、去年同期跑量、長跑與生理指標</p>
                </div>
                <div class="text-xs text-slate-400 flex items-center gap-2">
                    <span class="inline-block w-2.5 h-2.5 rounded-full bg-sky-400"></span>
                    <span id="table-filter-note">當前顯示: 全量原始平均</span>
                </div>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="text-xs uppercase bg-slate-800 text-slate-400 border-b border-slate-700">
                        <tr>
                            <th class="py-3 px-3">月份</th>
                            <th class="py-3 px-3 text-sky-400">月總跑量</th>
                            <th class="py-3 px-3 text-emerald-400">MoM 月增率</th>
                            <th class="py-3 px-3 text-purple-400">YoY 年增率</th>
                            <th class="py-3 px-3 text-slate-400">去年同期</th>
                            <th class="py-3 px-3 text-orange-400">10K+ 長跑</th>
                            <th class="py-3 px-3 text-emerald-400">全馬 / 半馬</th>
                            <th class="py-3 px-3">單月最長</th>
                            <th class="py-3 px-3 text-rose-400">運動總卡路里</th>
                            <th class="py-3 px-3 text-rose-300">月均 RHR</th>
                            <th class="py-3 px-3 text-emerald-300">月均 HRV</th>
                            <th class="py-3 px-3 text-indigo-300">月均睡眠 (深層/REM)</th>
                            <th class="py-3 px-3">月均步數</th>
                        </tr>
                    </thead>
                    <tbody id="monthly-table-body" class="divide-y divide-slate-800">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Smart Health Improvement Insights Section -->
        <section class="glass-card rounded-2xl p-6" id="insights-section">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-5 border-b border-slate-700/60 pb-4">
                <div>
                    <h2 class="text-xl font-bold text-white flex items-center gap-2">
                        <span>💡</span> 智慧健康診斷與可改善建議
                    </h2>
                    <p class="text-xs text-slate-400 mt-0.5">
                        整合長跑訓練週期、睡眠修復、自律神經 (HRV) 與心血管負荷之個人化實證建議。
                    </p>
                </div>
                <div class="flex flex-wrap gap-2 text-xs">
                    <button onclick="filterRecs('all')" id="rec-filter-all" class="px-3 py-1.5 rounded-lg bg-sky-600 text-white font-medium">全部</button>
                    <button onclick="filterRecs('critical')" id="rec-filter-critical" class="px-3 py-1.5 rounded-lg bg-slate-800 text-rose-400 hover:bg-slate-700">🔴 需改善</button>
                    <button onclick="filterRecs('warning')" id="rec-filter-warning" class="px-3 py-1.5 rounded-lg bg-slate-800 text-amber-400 hover:bg-slate-700">🟡 注意</button>
                    <button onclick="filterRecs('good')" id="rec-filter-good" class="px-3 py-1.5 rounded-lg bg-slate-800 text-emerald-400 hover:bg-slate-700">🟢 良好表現</button>
                </div>
            </div>

            <!-- Recommendations Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="recommendations-container">
                <!-- Dynamically Populated -->
            </div>
        </section>

        <!-- 📋 FULL GRANULAR DAILY RECORDS TABLE SECTION -->
        <section class="glass-card rounded-2xl p-6" id="daily-records-section">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 mb-4">
                <div class="flex items-center gap-2.5">
                    <span class="text-2xl">📋</span>
                    <div>
                        <h3 class="text-lg font-bold text-white flex items-center gap-2">
                            每日完整原始健康與運動明細表 (Daily Granular History)
                        </h3>
                        <p class="text-xs text-slate-400">完整保留每一天的原始步數、心率、睡眠、HRV、身體電量與運動項目</p>
                    </div>
                </div>
                <!-- Search Filter & Count -->
                <div class="flex items-center gap-2">
                    <input 
                        type="text" 
                        id="daily-search-input" 
                        placeholder="搜尋日期 (如 2026-08) 或運動名稱..." 
                        oninput="filterDailyRecords()" 
                        class="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500 w-64"
                    />
                    <span class="text-xs text-slate-400 whitespace-nowrap" id="daily-record-count">共 -- 筆</span>
                </div>
            </div>

            <div class="overflow-x-auto max-h-[500px]">
                <table class="w-full text-left text-xs text-slate-300">
                    <thead class="text-xs uppercase bg-slate-800 text-slate-400 sticky top-0 border-b border-slate-700">
                        <tr>
                            <th class="py-2.5 px-3">日期</th>
                            <th class="py-2.5 px-3 text-sky-400">步數 / 目標</th>
                            <th class="py-2.5 px-3 text-emerald-400">當日運動 / 距離</th>
                            <th class="py-2.5 px-3 text-rose-400">靜止心率</th>
                            <th class="py-2.5 px-3 text-emerald-300">HRV (昨夜)</th>
                            <th class="py-2.5 px-3 text-indigo-300">睡眠 (時長/分)</th>
                            <th class="py-2.5 px-3 text-amber-400">電量充 / 放</th>
                            <th class="py-2.5 px-3">平均壓力</th>
                            <th class="py-2.5 px-3 text-orange-400">活動卡路里</th>
                            <th class="py-2.5 px-3">SpO2 / 呼吸</th>
                            <th class="py-2.5 px-3">VO2 Max</th>
                        </tr>
                    </thead>
                    <tbody id="daily-records-table-body" class="divide-y divide-slate-800">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Footer -->
        <footer class="text-center text-xs text-slate-500 py-6">
            Garmin Connect Health & Endurance Trends &bull; 本地運算與獨立視覺化報表 &bull; 0 Token 消耗 &bull; 雙軌異常去噪與對比
        </footer>

    </div>

    <!-- 📖 HELP & BENCHMARK GUIDE MODAL -->
    <div id="help-modal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 hidden">
        <div class="glass-card bg-slate-900 border border-slate-700 rounded-2xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            
            <!-- Modal Header -->
            <div class="p-5 border-b border-slate-700/80 flex items-center justify-between bg-slate-950/70">
                <div class="flex items-center gap-3">
                    <span class="text-2xl">📖</span>
                    <div>
                        <h3 class="text-lg font-bold text-white">Garmin 健康與運動指標對照指南 (Help & Benchmark Guide)</h3>
                        <p class="text-xs text-slate-400">各項生理數值標準、常態區間與跑者體能評估標準</p>
                    </div>
                </div>
                <button onclick="closeHelpModal()" class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-all text-sm font-bold">
                    ✕ 關閉
                </button>
            </div>

            <!-- Modal Content (Scrollable) -->
            <div class="p-6 overflow-y-auto space-y-6 text-sm text-slate-300">
                
                <!-- 1. VO2 Max Guide -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-purple-500/30 space-y-3">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">🫁</span>
                        <h4 class="font-bold text-white text-base">最大攝氧量 (VO2 Max) 典型標準對照表</h4>
                        <span class="text-xs px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 font-mono">mL/(kg·min)</span>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        VO2 Max 是衡量心血管耐力與長壽潛力的黃金指標。代表身體在高強度運動中每公斤體重每分鐘能攝取並利用的最高氧氣量。
                    </p>

                    <!-- Male Table -->
                    <div class="overflow-x-auto mt-2">
                        <div class="text-xs font-semibold text-sky-400 mb-1">👨 男性標準分級</div>
                        <table class="w-full text-xs text-left border border-slate-700 rounded-lg">
                            <thead class="bg-slate-900 text-slate-400 border-b border-slate-700">
                                <tr>
                                    <th class="py-2 px-3">年齡區間</th>
                                    <th class="py-2 px-3 text-rose-400">較差 (Low)</th>
                                    <th class="py-2 px-3 text-amber-400">典型平均 (Average)</th>
                                    <th class="py-2 px-3 text-emerald-400">良好 (Good)</th>
                                    <th class="py-2 px-3 text-purple-400">優良/頂尖 (Excellent)</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800">
                                <tr><td class="py-1.5 px-3 font-medium">20 ~ 29 歲</td><td class="py-1.5 px-3">&lt; 38</td><td class="py-1.5 px-3 font-semibold text-amber-400">38 ~ 45</td><td class="py-1.5 px-3 text-emerald-400">46 ~ 53</td><td class="py-1.5 px-3 text-purple-400">&gt; 54</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">30 ~ 39 歲</td><td class="py-1.5 px-3">&lt; 35</td><td class="py-1.5 px-3 font-semibold text-amber-400">35 ~ 43</td><td class="py-1.5 px-3 text-emerald-400">44 ~ 50</td><td class="py-1.5 px-3 text-purple-400">&gt; 51</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">40 ~ 49 歲</td><td class="py-1.5 px-3">&lt; 32</td><td class="py-1.5 px-3 font-semibold text-amber-400">33 ~ 40</td><td class="py-1.5 px-3 text-emerald-400">41 ~ 47</td><td class="py-1.5 px-3 text-purple-400">&gt; 48</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">50 ~ 59 歲</td><td class="py-1.5 px-3">&lt; 29</td><td class="py-1.5 px-3 font-semibold text-amber-400">30 ~ 36</td><td class="py-1.5 px-3 text-emerald-400">37 ~ 44</td><td class="py-1.5 px-3 text-purple-400">&gt; 45</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">60 歲以上</td><td class="py-1.5 px-3">&lt; 24</td><td class="py-1.5 px-3 font-semibold text-amber-400">25 ~ 33</td><td class="py-1.5 px-3 text-emerald-400">34 ~ 40</td><td class="py-1.5 px-3 text-purple-400">&gt; 41</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Female Table -->
                    <div class="overflow-x-auto mt-3">
                        <div class="text-xs font-semibold text-pink-400 mb-1">👩 女性標準分級 (肌肉量與血紅素差異約低 10~15%)</div>
                        <table class="w-full text-xs text-left border border-slate-700 rounded-lg">
                            <thead class="bg-slate-900 text-slate-400 border-b border-slate-700">
                                <tr>
                                    <th class="py-2 px-3">年齡區間</th>
                                    <th class="py-2 px-3 text-rose-400">較差 (Low)</th>
                                    <th class="py-2 px-3 text-amber-400">典型平均 (Average)</th>
                                    <th class="py-2 px-3 text-emerald-400">良好 (Good)</th>
                                    <th class="py-2 px-3 text-purple-400">優良/頂尖 (Excellent)</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800">
                                <tr><td class="py-1.5 px-3 font-medium">20 ~ 29 歲</td><td class="py-1.5 px-3">&lt; 32</td><td class="py-1.5 px-3 font-semibold text-amber-400">32 ~ 39</td><td class="py-1.5 px-3 text-emerald-400">40 ~ 46</td><td class="py-1.5 px-3 text-purple-400">&gt; 47</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">30 ~ 39 歲</td><td class="py-1.5 px-3">&lt; 30</td><td class="py-1.5 px-3 font-semibold text-amber-400">30 ~ 37</td><td class="py-1.5 px-3 text-emerald-400">38 ~ 44</td><td class="py-1.5 px-3 text-purple-400">&gt; 45</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">40 ~ 49 歲</td><td class="py-1.5 px-3">&lt; 27</td><td class="py-1.5 px-3 font-semibold text-amber-400">28 ~ 35</td><td class="py-1.5 px-3 text-emerald-400">36 ~ 41</td><td class="py-1.5 px-3 text-purple-400">&gt; 42</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">50 ~ 59 歲</td><td class="py-1.5 px-3">&lt; 24</td><td class="py-1.5 px-3 font-semibold text-amber-400">25 ~ 32</td><td class="py-1.5 px-3 text-emerald-400">33 ~ 38</td><td class="py-1.5 px-3 text-purple-400">&gt; 39</td></tr>
                                <tr><td class="py-1.5 px-3 font-medium">60 歲以上</td><td class="py-1.5 px-3">&lt; 20</td><td class="py-1.5 px-3 font-semibold text-amber-400">21 ~ 28</td><td class="py-1.5 px-3 text-emerald-400">29 ~ 35</td><td class="py-1.5 px-3 text-purple-400">&gt; 36</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Runner Tiers -->
                    <div class="mt-3 p-2.5 rounded-lg bg-slate-900/80 border border-slate-700 text-xs text-slate-300 space-y-1">
                        <div class="font-bold text-amber-400">🏃‍♂️ 跑者與運動員等級對照：</div>
                        <div>&bull; <b>市民休閒跑者 / 全馬完賽</b>：約 <b>48 ~ 54</b></div>
                        <div>&bull; <b>進階業餘跑者 / 波馬資格 (BQ / Sub-3)</b>：約 <b>55 ~ 65</b></div>
                        <div>&bull; <b>頂尖菁英長跑選手 (如 Kipchoge)</b>：約 <b>75 ~ 85+</b></div>
                    </div>
                </div>

                <!-- 2. Sleep Stages Benchmark -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-indigo-500/30 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">🌙</span>
                        <h4 class="font-bold text-white text-base">睡眠各階段黃金佔比標準</h4>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <div class="p-2.5 rounded-lg bg-blue-950/40 border border-blue-500/30">
                            <div class="font-bold text-blue-400">深層睡眠 (Deep Sleep)</div>
                            <div class="text-lg font-black text-blue-400 mt-1">15% ~ 25%</div>
                            <div class="text-slate-400 mt-1">身體修復、肌肉生長與生長激素釋放。</div>
                        </div>
                        <div class="p-2.5 rounded-lg bg-purple-950/40 border border-purple-500/30">
                            <div class="font-bold text-purple-400">快速動眼 (REM Sleep)</div>
                            <div class="text-lg font-black text-purple-400 mt-1">20% ~ 25%</div>
                            <div class="text-slate-400 mt-1">大腦神經重整、記憶固化與情緒調適。</div>
                        </div>
                        <div class="p-2.5 rounded-lg bg-slate-950/60 border border-slate-700">
                            <div class="font-bold text-slate-300">淺層睡眠 (Light Sleep)</div>
                            <div class="text-lg font-black text-slate-400 mt-1">50% ~ 60%</div>
                            <div class="text-slate-400 mt-1">身體放鬆過渡期，維持基本休息。</div>
                        </div>
                    </div>
                </div>

                <!-- 3. HRV & Recovery -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-emerald-500/30 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">⚡</span>
                        <h4 class="font-bold text-white text-base">HRV 自律神經與恢復解讀</h4>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        心率變異度 (HRV) 反映副交感神經（修復）與交感神經（壓力）的平衡。HRV 數值具有高度個體性，最重要的是觀察是否在您個人的「平衡基準線 (Baseline)」之內。連續數天低於基準線常代表訓練疲勞累積、睡眠不足或生病前兆。
                    </p>
                </div>

                <!-- 4. Outlier Trimming Engine -->
                <div class="p-4 rounded-xl bg-slate-800/60 border border-sky-500/30 space-y-2">
                    <div class="flex items-center gap-2">
                        <span class="text-xl">🎯</span>
                        <h4 class="font-bold text-white text-base">異常值過濾與雙軌對比原理</h4>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        當您開啟「去噪 (Trim Outliers)」時，系統會採用統計學上的截尾平均數 (Trimmed Mean)，自動剔除單月中手錶脫落（如僅記錄 1 小時睡眠）或感測器雜訊的極端極值，計算出更具常態代表性的健康平均值，並在圖表上以黃色虛線繪出原始對比線。
                    </p>
                </div>

            </div>
            
            <!-- Modal Footer -->
            <div class="p-4 border-t border-slate-700/80 bg-slate-950/70 text-right">
                <button onclick="closeHelpModal()" class="px-5 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition-all shadow-md">
                    了解並返回
                </button>
            </div>

        </div>
    </div>

    <!-- Embedded Data Payload -->
    <script>
        const APP_DATA = {payload_json};
    </script>

    <!-- Dashboard Logic Script with Light/Dark Mode & Outlier Trimming -->
    <script>
        let currentTab = 'monthly';
        let currentPlotMode = 'daily';
        let currentRecFilter = 'all';
        let isOutlierTrimEnabled = false;
        let currentTrimRatio = 0.05; // 0.05, 0.10, 0.15
        let showOverlayComparison = true;
        let charts = {{}};

        // ☀️/🌙 Theme Switcher Logic
        function getChartThemeColors() {{
            const isDark = document.documentElement.classList.contains('dark');
            return {{
                isDark: isDark,
                gridColor: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(100, 116, 139, 0.25)',
                tickColor: isDark ? '#94a3b8' : '#0f172a',
                legendColor: isDark ? '#e2e8f0' : '#0f172a',
                titleColor: isDark ? '#cbd5e1' : '#0f172a',
                axisBorderColor: isDark ? 'rgba(255, 255, 255, 0.15)' : '#94a3b8'
            }};
        }}

        function applyTheme(theme) {{
            const html = document.documentElement;
            const icon = document.getElementById('theme-icon');
            const text = document.getElementById('theme-text');
            if (theme === 'light') {{
                html.classList.remove('dark');
                if (icon) icon.innerText = '🌙';
                if (text) text.innerText = '深色模式';
                localStorage.setItem('garmin_dashboard_theme', 'light');
            }} else {{
                html.classList.add('dark');
                if (icon) icon.innerText = '☀️';
                if (text) text.innerText = '淺色模式';
                localStorage.setItem('garmin_dashboard_theme', 'dark');
            }}
            renderDailyCharts();
            renderMonthlyCharts();
            renderDistanceHistogram();
        }}

        function toggleTheme() {{
            const isDark = document.documentElement.classList.contains('dark');
            applyTheme(isDark ? 'light' : 'dark');
        }}

        // 🎯 Robust Trimmed Mean
        function computeTrimmedMean(arr, trimRatio = 0.05) {{
            if (!arr || arr.length === 0) return null;
            const valid = arr.filter(v => v !== null && v !== undefined && !isNaN(v)).sort((a, b) => a - b);
            if (valid.length === 0) return null;
            if (valid.length < 4) {{
                return valid.reduce((a, b) => a + b, 0) / valid.length;
            }}
            let trimCount = Math.floor(valid.length * trimRatio);
            if (trimCount === 0 && valid.length >= 6) trimCount = 1;
            const trimmed = valid.slice(trimCount, valid.length - trimCount);
            if (trimmed.length === 0) return valid.reduce((a, b) => a + b, 0) / valid.length;
            return trimmed.reduce((a, b) => a + b, 0) / trimmed.length;
        }}

        function computeRawMean(arr) {{
            if (!arr || arr.length === 0) return null;
            const valid = arr.filter(v => v !== null && v !== undefined && !isNaN(v));
            if (valid.length === 0) return null;
            return valid.reduce((a, b) => a + b, 0) / valid.length;
        }}

        // Dynamic Monthly Breakdown Computation
        function getComputedMonthlyData() {{
            const records = APP_DATA.records || [];
            const monthsMap = {{}};

            records.forEach(r => {{
                const d = r.date || '';
                if (d.length >= 7) {{
                    const mKey = d.slice(0, 7);
                    if (!monthsMap[mKey]) monthsMap[mKey] = [];
                    monthsMap[mKey].push(r);
                }}
            }});

            const sortedMonths = Object.keys(monthsMap).sort();
            const runningTypes = ['running', 'trail_running', 'treadmill_running', 'street_running', 'track_running', 'virtual_run', 'obstacle_run'];
            
            // Pre-calculate month totals to enable YoY lookups
            const monthTotalsMap = {{}};
            sortedMonths.forEach(mKey => {{
                const mRecs = monthsMap[mKey];
                let km = 0;
                let runs = 0;
                mRecs.forEach(r => {{
                    (r.activities || []).forEach(act => {{
                        const actType = (act.type || '').toLowerCase();
                        const actName = (act.name || '').toLowerCase();
                        const dist = act.distance_km || 0.0;
                        const isRun = runningTypes.some(rt => actType.includes(rt)) || ['跑', 'run', 'marathon', '馬拉松', '越野'].some(k => actName.includes(k));
                        if (isRun || dist >= 3.0) {{
                            km += dist;
                            runs++;
                        }}
                    }});
                }});
                monthTotalsMap[mKey] = {{ totRunKm: +km.toFixed(2), totalRuns: runs }};
            }});

            let prevKm = null;

            return sortedMonths.map(mKey => {{
                const mRecs = monthsMap[mKey];
                const parts = mKey.split('-');
                const monthLabel = parts.length === 2 ? `${{parts[0]}}年 ${{parts[1]}}月` : mKey;

                // Running & Endurance Stats (Totals are exact sums)
                const mRuns = [];
                mRecs.forEach(r => {{
                    (r.activities || []).forEach(act => {{
                        const actType = (act.type || '').toLowerCase();
                        const actName = (act.name || '').toLowerCase();
                        const dist = act.distance_km || 0.0;
                        const cals = act.calories || 0;
                        const isRun = runningTypes.some(rt => actType.includes(rt)) || ['跑', 'run', 'marathon', '馬拉松', '越野'].some(k => actName.includes(k));
                        if (isRun || dist >= 3.0) {{
                            mRuns.push({{ dist: dist, cals: cals, name: act.name }});
                        }}
                    }});
                }});

                const totRunKm = +(mRuns.reduce((sum, r) => sum + r.dist, 0)).toFixed(2);
                const runs10k = mRuns.filter(r => r.dist >= 10.0).length;
                const fullMarathons = mRuns.filter(r => r.dist >= 42.0).length;
                const halfMarathons = mRuns.filter(r => r.dist >= 21.0 && r.dist < 42.0).length;
                const longestKm = mRuns.length > 0 ? Math.max(...mRuns.map(r => r.dist)) : 0.0;
                const totCals = mRecs.reduce((sum, r) => sum + (r.active_calories || 0), 0);

                let growthPct = null;
                if (prevKm !== null && prevKm > 0) {{
                    growthPct = +(((totRunKm - prevKm) / prevKm) * 100).toFixed(1);
                }}
                prevKm = totRunKm;

                // YoY Calculation
                const prevYKey = parts.length === 2 ? `${{parseInt(parts[0], 10) - 1}}-${{parts[1]}}` : '';
                let yoyGrowthPct = null;
                let lastYearRunKm = null;
                if (monthTotalsMap[prevYKey]) {{
                    lastYearRunKm = monthTotalsMap[prevYKey].totRunKm;
                    if (lastYearRunKm > 0) {{
                        yoyGrowthPct = +(((totRunKm - lastYearRunKm) / lastYearRunKm) * 100).toFixed(1);
                    }}
                }}

                // Extract Arrays for Statistical Averaging
                const rhrs = mRecs.map(r => r.resting_hr);
                const hrvs = mRecs.map(r => r.hrv_overnight_avg);
                const sleepSecs = mRecs.map(r => r.sleep_duration_seconds);
                const deepSecs = mRecs.map(r => r.deep_sleep_seconds);
                const remSecs = mRecs.map(r => r.rem_sleep_seconds);
                const lightSecs = mRecs.map(r => r.light_sleep_seconds);
                const awakeSecs = mRecs.map(r => r.awake_seconds);
                const sleepScores = mRecs.map(r => r.sleep_score);
                const steps = mRecs.map(r => r.steps);
                const stresses = mRecs.map(r => r.avg_stress);

                // Raw Averages
                const rawRhr = computeRawMean(rhrs);
                const rawHrv = computeRawMean(hrvs);
                const rawSleepH = computeRawMean(sleepSecs) ? +(computeRawMean(sleepSecs) / 3600).toFixed(2) : null;
                const rawDeepH = computeRawMean(deepSecs) ? +(computeRawMean(deepSecs) / 3600).toFixed(2) : 0;
                const rawRemH = computeRawMean(remSecs) ? +(computeRawMean(remSecs) / 3600).toFixed(2) : 0;
                const rawLightH = computeRawMean(lightSecs) ? +(computeRawMean(lightSecs) / 3600).toFixed(2) : 0;
                const rawAwakeH = computeRawMean(awakeSecs) ? +(computeRawMean(awakeSecs) / 3600).toFixed(2) : 0;
                const rawSleepScore = computeRawMean(sleepScores);
                const rawSteps = computeRawMean(steps);
                const rawStress = computeRawMean(stresses);

                // 🎯 Trimmed Means
                const trimRhr = computeTrimmedMean(rhrs, currentTrimRatio);
                const trimHrv = computeTrimmedMean(hrvs, currentTrimRatio);
                const trimSleepH = computeTrimmedMean(sleepSecs, currentTrimRatio) ? +(computeTrimmedMean(sleepSecs, currentTrimRatio) / 3600).toFixed(2) : null;
                const trimDeepH = computeTrimmedMean(deepSecs, currentTrimRatio) ? +(computeTrimmedMean(deepSecs, currentTrimRatio) / 3600).toFixed(2) : 0;
                const trimRemH = computeTrimmedMean(remSecs, currentTrimRatio) ? +(computeTrimmedMean(remSecs, currentTrimRatio) / 3600).toFixed(2) : 0;
                const trimLightH = computeTrimmedMean(lightSecs, currentTrimRatio) ? +(computeTrimmedMean(lightSecs, currentTrimRatio) / 3600).toFixed(2) : 0;
                const trimAwakeH = computeTrimmedMean(awakeSecs, currentTrimRatio) ? +(computeTrimmedMean(awakeSecs, currentTrimRatio) / 3600).toFixed(2) : 0;
                const trimSleepScore = computeTrimmedMean(sleepScores, currentTrimRatio);
                const trimSteps = computeTrimmedMean(steps, currentTrimRatio);
                const trimStress = computeTrimmedMean(stresses, currentTrimRatio);

                // Active Display Values
                const activeRhr = isOutlierTrimEnabled ? (trimRhr ? +trimRhr.toFixed(1) : null) : (rawRhr ? +rawRhr.toFixed(1) : null);
                const activeHrv = isOutlierTrimEnabled ? (trimHrv ? +trimHrv.toFixed(1) : null) : (rawHrv ? +rawRhr.toFixed(1) : null);
                const activeSleepH = isOutlierTrimEnabled ? trimSleepH : rawSleepH;
                const activeDeepH = isOutlierTrimEnabled ? trimDeepH : rawDeepH;
                const activeRemH = isOutlierTrimEnabled ? trimRemH : rawRemH;
                const activeLightH = isOutlierTrimEnabled ? trimLightH : rawLightH;
                const activeAwakeH = isOutlierTrimEnabled ? trimAwakeH : rawAwakeH;
                const activeSleepScore = isOutlierTrimEnabled ? (trimSleepScore ? +trimSleepScore.toFixed(1) : null) : (rawSleepScore ? +rawSleepScore.toFixed(1) : null);
                const activeSteps = isOutlierTrimEnabled ? (trimSteps ? Math.round(trimSteps) : null) : (rawSteps ? Math.round(rawSteps) : null);
                const activeStress = isOutlierTrimEnabled ? (trimStress ? +trimStress.toFixed(1) : null) : (rawStress ? +rawStress.toFixed(1) : null);

                const totStage = (activeDeepH || 0) + (activeRemH || 0) + (activeLightH || 0) + (activeAwakeH || 0);
                const deepPct = totStage > 0 ? +((activeDeepH / totStage) * 100).toFixed(1) : null;
                const remPct = totStage > 0 ? +((activeRemH / totStage) * 100).toFixed(1) : null;

                return {{
                    month: mKey,
                    month_label: monthLabel,
                    days_count: mRecs.length,
                    total_run_km: totRunKm,
                    total_runs: mRuns.length,
                    runs_10k_plus: runs10k,
                    full_marathons: fullMarathons,
                    half_marathons: halfMarathons,
                    longest_run_km: +longestKm.toFixed(2),
                    total_calories: Math.round(totCals),
                    mom_km_growth_pct: growthPct,
                    yoy_km_growth_pct: yoyGrowthPct,
                    last_year_run_km: lastYearRunKm,
                    
                    // Active Values
                    avg_rhr: activeRhr,
                    avg_hrv: activeHrv,
                    avg_sleep_hours: activeSleepH,
                    avg_deep_hours: activeDeepH,
                    avg_rem_hours: activeRemH,
                    avg_light_hours: activeLightH,
                    avg_awake_hours: activeAwakeH,
                    avg_sleep_score: activeSleepScore,
                    avg_steps: activeSteps,
                    avg_stress: activeStress,
                    deep_pct: deepPct,
                    rem_pct: remPct,

                    // Comparison Reference Pairs
                    raw: {{
                        avg_rhr: rawRhr ? +rawRhr.toFixed(1) : null,
                        avg_hrv: rawHrv ? +rawHrv.toFixed(1) : null,
                        avg_sleep_hours: rawSleepH,
                        avg_deep_hours: rawDeepH,
                        avg_rem_hours: rawRemH,
                        avg_light_hours: rawLightH,
                        avg_awake_hours: rawAwakeH,
                        avg_sleep_score: rawSleepScore ? +rawSleepScore.toFixed(1) : null,
                        avg_steps: rawSteps ? Math.round(rawSteps) : null
                    }},
                    trimmed: {{
                        avg_rhr: trimRhr ? +trimRhr.toFixed(1) : null,
                        avg_hrv: trimHrv ? +trimHrv.toFixed(1) : null,
                        avg_sleep_hours: trimSleepH,
                        avg_deep_hours: trimDeepH,
                        avg_rem_hours: trimRemH,
                        avg_light_hours: trimLightH,
                        avg_awake_hours: trimAwakeH,
                        avg_sleep_score: trimSleepScore ? +trimSleepScore.toFixed(1) : null,
                        avg_steps: trimSteps ? Math.round(trimSteps) : null
                    }}
                }};
            }});
        }}

        function setTrimLevel(ratio) {{
            currentTrimRatio = ratio;
            document.querySelectorAll('.trim-level-btn').forEach(btn => btn.classList.remove('active'));
            const pct = Math.round(ratio * 100);
            const activeBtn = document.getElementById(`trim-lvl-${{pct}}`);
            if (activeBtn) activeBtn.classList.add('active');

            if (!isOutlierTrimEnabled) {{
                document.getElementById('trim-outliers-toggle').checked = true;
                isOutlierTrimEnabled = true;
            }}
            updateFilterUI();
            renderKPIs();
            renderMonthlyTable();
            renderMonthlyCharts();
            renderDailyCharts();
        }}

        function toggleOutliersFilter() {{
            const checkbox = document.getElementById('trim-outliers-toggle');
            isOutlierTrimEnabled = checkbox.checked;
            updateFilterUI();
            renderKPIs();
            renderMonthlyTable();
            renderMonthlyCharts();
            renderDailyCharts();
        }}

        function toggleOverlayComparison() {{
            showOverlayComparison = document.getElementById('show-overlay-toggle').checked;
            renderMonthlyCharts();
        }}

        function updateFilterUI() {{
            const badge = document.getElementById('filter-active-badge');
            const indicator = document.getElementById('monthly-outlier-indicator');
            const tableNote = document.getElementById('table-filter-note');
            const dailyHint = document.getElementById('daily-outlier-hint');
            const pct = Math.round(currentTrimRatio * 100);

            if (isOutlierTrimEnabled) {{
                if (badge) {{
                    badge.innerHTML = `🟢 已啟用 (排除上下 ${{pct}}% 極端值)`;
                    badge.className = 'text-xs px-2.5 py-0.5 rounded-full bg-emerald-950/80 text-emerald-300 border border-emerald-500/60 font-semibold shadow-sm';
                }}
                if (indicator) indicator.innerHTML = `<span class="text-emerald-500 font-semibold">🎯 統計方式: 已排除上下 ${{pct}}% 極端值 (中間 ${{100 - pct*2}}% 常態代表性均值)</span>`;
                if (tableNote) tableNote.innerHTML = `<span class="text-emerald-500 font-semibold">去極值均值 (附帶原始全量數據對比標籤)</span>`;
                if (dailyHint) dailyHint.innerHTML = `<span class="text-emerald-500 font-semibold">已啟用去極值運算模式 (${{pct}}%)</span>`;
            }} else {{
                if (badge) {{
                    badge.innerText = '未啟用 (全量原始數據)';
                    badge.className = 'text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700';
                }}
                if (indicator) indicator.innerText = '統計方式: 全量平均 (打勾上方可開啟截尾去噪與雙軌對比)';
                if (tableNote) tableNote.innerText = '當前顯示: 全量原始平均';
                if (dailyHint) dailyHint.innerText = '每一個數據點代表一天的實際測量值';
            }}
        }}

        function setPlotMode(mode) {{
            currentPlotMode = mode;
            document.querySelectorAll('.plot-mode-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById(`plot-mode-${{mode}}`);
            if (activeBtn) activeBtn.classList.add('active');

            const dailyContainer = document.getElementById('daily-plots-container');
            const monthlyContainer = document.getElementById('monthly-plots-container');

            if (mode === 'daily') {{
                if (dailyContainer) dailyContainer.classList.remove('hidden');
                if (monthlyContainer) monthlyContainer.classList.add('hidden');
                renderDailyCharts();
            }} else {{
                if (dailyContainer) dailyContainer.classList.add('hidden');
                if (monthlyContainer) monthlyContainer.classList.remove('hidden');
                renderMonthlyCharts();
            }}
        }}

        function switchTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById(`tab-${{tab}}`);
            if (activeBtn) activeBtn.classList.add('active');

            if (tab === 'comparison') {{
                setPlotMode('monthly');
            }} else {{
                setPlotMode('daily');
            }}

            renderTodayAssessment();
            renderKPIs();
            renderMonthlyTable();
            renderDailyTable();
        }}

        function getActiveRecords() {{
            const all = APP_DATA.records;
            if (!all || all.length === 0) return [];
            if (currentTab === 'daily') return all.slice(-1);
            if (currentTab === 'monthly') return all.slice(-30);
            if (currentTab === 'quarterly') return all.slice(-90);
            return all;
        }}

        function renderKPIs() {{
            const summaryKey = (currentTab === 'comparison' || !APP_DATA.summaries[currentTab]) ? 'all' : currentTab;
            const summary = APP_DATA.summaries[summaryKey] || {{}};
            const run = summary.running || {{}};
            const records = getActiveRecords();

            // 1. Endurance & Marathon Hub KPIs
            const runs10k = run.runs_10k_plus_count || 0;
            const kpi10kCadence = document.getElementById('kpi-10k-cadence');
            if (kpi10kCadence) {{
                if (runs10k > 0) {{
                    const freqStr = run.days_per_10k_run ? `每 ${{run.days_per_10k_run}} 天一次` : '已累積長跑';
                    kpi10kCadence.innerHTML = `${{runs10k}} <span class="text-xs font-normal text-slate-400">次 (${{freqStr}})</span>`;
                }} else {{
                    kpi10kCadence.innerHTML = `0 <span class="text-xs font-normal text-slate-400">次 (區間內)</span>`;
                }}
            }}

            const since10k = run.days_since_last_10k;
            const kpi10kRecency = document.getElementById('kpi-10k-recency');
            if (kpi10kRecency) {{
                if (since10k !== null && since10k !== undefined) {{
                    const statusColor = since10k > 14 ? 'text-rose-500 font-semibold' : 'text-slate-400';
                    kpi10kRecency.innerHTML = `距上次 10K+: <span class="${{statusColor}}">${{since10k}} 天前</span> (${{run.last_10k_km || 0}} km)`;
                }} else {{
                    kpi10kRecency.innerText = '尚無 10K+ 紀錄';
                }}
            }}

            const totalRunKm = run.total_run_km || 0;
            const kpiRunMileage = document.getElementById('kpi-run-mileage');
            if (kpiRunMileage) kpiRunMileage.innerHTML = `${{totalRunKm.toLocaleString()}} <span class="text-xs text-slate-400 font-normal">km</span>`;
            
            const kpiRunWeekly = document.getElementById('kpi-run-weekly');
            if (kpiRunWeekly) kpiRunWeekly.innerText = `週均: ${{run.weekly_run_km || 0}} km / 共 ${{run.total_runs || 0}} 次跑步`;

            const fullCnt = run.full_marathon_count || 0;
            const halfCnt = run.half_marathon_count || 0;
            const midCnt = run.mid_distance_count || 0;
            const kpiMarathon = document.getElementById('kpi-marathon-counts');
            if (kpiMarathon) kpiMarathon.innerHTML = `全馬 ${{fullCnt}} &bull; 半馬 ${{halfCnt}} &bull; 10K ${{midCnt}}`;
            
            const kpiLongest = document.getElementById('kpi-longest-run');
            if (kpiLongest) kpiLongest.innerText = `最長單次: ${{run.longest_run_km || 0}} km (${{run.longest_run_date || '-'}})`;

            const runCals = run.total_run_calories || 0;
            const kpiRunCals = document.getElementById('kpi-run-calories');
            if (kpiRunCals) kpiRunCals.innerHTML = `${{runCals.toLocaleString()}} <span class="text-xs text-slate-400 font-normal">kcal</span>`;
            
            const calPerKm = run.avg_calories_per_km ? `均約 ${{run.avg_calories_per_km}} kcal/km` : '熱量充足';
            const kpiCalPerKm = document.getElementById('kpi-cal-per-km');
            if (kpiCalPerKm) kpiCalPerKm.innerText = `${{calPerKm}} | 單次最高 ${{run.max_workout_calories || 0}} kcal`;

            // 2. Standard Vitals KPIs (Recalculate with dynamic trim)
            let avgRhr = summary.avg_rhr;
            let avgHrv = summary.avg_hrv;
            let avgSleepH = summary.avg_sleep_hours;
            let avgSteps = summary.avg_steps;

            if (isOutlierTrimEnabled && records.length >= 4) {{
                const trRhr = computeTrimmedMean(records.map(r => r.resting_hr), currentTrimRatio);
                if (trRhr) avgRhr = +trRhr.toFixed(1);

                const trHrv = computeTrimmedMean(records.map(r => r.hrv_overnight_avg), currentTrimRatio);
                if (trHrv) avgHrv = +trHrv.toFixed(1);

                const trSleep = computeTrimmedMean(records.map(r => r.sleep_duration_seconds), currentTrimRatio);
                if (trSleep) avgSleepH = +(trSleep / 3600).toFixed(2);

                const trSteps = computeTrimmedMean(records.map(r => r.steps), currentTrimRatio);
                if (trSteps) avgSteps = Math.round(trSteps);
            }}

            const trimPctStr = `${{Math.round(currentTrimRatio * 100)}}%`;
            const kpiRhr = document.getElementById('kpi-rhr');
            const kpiRhrSub = document.getElementById('kpi-rhr-sub');
            if (kpiRhr) {{
                if (avgRhr !== null && avgRhr !== undefined) {{
                    const trimBadge = isOutlierTrimEnabled ? `<span class="text-emerald-500 text-xs font-normal"> (去噪${{trimPctStr}})</span>` : '';
                    kpiRhr.innerHTML = `${{avgRhr}}${{trimBadge}} <span class="text-xs font-normal text-slate-400">bpm</span>`;
                    if (kpiRhrSub) kpiRhrSub.innerText = `區間: ${{summary.min_rhr || '-'}} ~ ${{summary.max_rhr || '-'}} bpm`;
                }} else {{
                    kpiRhr.innerText = 'N/A';
                    if (kpiRhrSub) kpiRhrSub.innerText = '無紀錄';
                }}
            }}

            const kpiHrv = document.getElementById('kpi-hrv');
            const kpiHrvSub = document.getElementById('kpi-hrv-sub');
            if (kpiHrv) {{
                if (avgHrv !== null && avgHrv !== undefined) {{
                    const trimBadge = isOutlierTrimEnabled ? `<span class="text-emerald-500 text-xs font-normal"> (去噪${{trimPctStr}})</span>` : '';
                    kpiHrv.innerHTML = `${{avgHrv}}${{trimBadge}} <span class="text-xs font-normal text-slate-400">ms</span>`;
                    const balPct = summary.hrv_balanced_pct !== null ? `${{summary.hrv_balanced_pct}}% 平衡` : 'HRV 紀錄中';
                    if (kpiHrvSub) kpiHrvSub.innerText = balPct;
                }} else {{
                    kpiHrv.innerText = 'N/A';
                    if (kpiHrvSub) kpiHrvSub.innerText = '無紀錄';
                }}
            }}

            const kpiSleep = document.getElementById('kpi-sleep');
            const kpiSleepSub = document.getElementById('kpi-sleep-sub');
            if (kpiSleep) {{
                if (avgSleepH !== null && avgSleepH !== undefined) {{
                    const trimBadge = isOutlierTrimEnabled ? `<span class="text-emerald-500 text-xs font-normal"> (去噪${{trimPctStr}})</span>` : '';
                    kpiSleep.innerHTML = `${{avgSleepH}}${{trimBadge}} <span class="text-xs font-normal text-slate-400">h</span>`;
                    const scoreText = summary.avg_sleep_score ? `均分: ${{summary.avg_sleep_score}} 分` : '時長穩定';
                    if (kpiSleepSub) kpiSleepSub.innerText = `${{scoreText}} | 深層 ${{summary.deep_sleep_pct || 0}}%`;
                }} else {{
                    kpiSleep.innerText = 'N/A';
                    if (kpiSleepSub) kpiSleepSub.innerText = '無紀錄';
                }}
            }}

            const kpiBb = document.getElementById('kpi-bb');
            const kpiBbSub = document.getElementById('kpi-bb-sub');
            if (kpiBb) {{
                if (summary.avg_bb_charged !== null && summary.avg_bb_charged !== undefined) {{
                    kpiBb.innerHTML = `+${{summary.avg_bb_charged}} <span class="text-xs font-normal text-slate-400">充能</span>`;
                    const stressText = summary.avg_stress ? `均壓: ${{summary.avg_stress}}` : '正常';
                    if (kpiBbSub) kpiBbSub.innerText = `${{stressText}} | 消耗 -${{summary.avg_bb_drained || 0}}`;
                }} else {{
                    kpiBb.innerText = 'N/A';
                    if (kpiBbSub) kpiBbSub.innerText = '無紀錄';
                }}
            }}

            const kpiSteps = document.getElementById('kpi-steps');
            const kpiStepsSub = document.getElementById('kpi-steps-sub');
            if (kpiSteps) {{
                if (avgSteps !== null && avgSteps !== undefined) {{
                    const trimBadge = isOutlierTrimEnabled ? `<span class="text-emerald-500 text-xs font-normal"> (去噪${{trimPctStr}})</span>` : '';
                    kpiSteps.innerHTML = `${{avgSteps.toLocaleString()}}${{trimBadge}} <span class="text-xs font-normal text-slate-400">步</span>`;
                    if (kpiStepsSub) kpiStepsSub.innerText = `達標率: ${{summary.goal_met_pct || 0}}% (${{summary.total_distance_km || 0}} km)`;
                }} else {{
                    kpiSteps.innerText = 'N/A';
                    if (kpiStepsSub) kpiStepsSub.innerText = '無紀錄';
                }}
            }}

            const kpiFitness = document.getElementById('kpi-fitness');
            const kpiFitnessSub = document.getElementById('kpi-fitness-sub');
            if (kpiFitness) {{
                if (summary.latest_vo2_max !== null && summary.latest_vo2_max !== undefined) {{
                    kpiFitness.innerHTML = `${{summary.latest_vo2_max}} <span class="text-xs font-normal text-slate-400">VO2</span>`;
                    const respText = summary.avg_respiration ? `呼吸 ${{summary.avg_respiration}} brpm` : '心肺優良';
                    if (kpiFitnessSub) kpiFitnessSub.innerText = `${{respText}} | SpO2 ${{summary.avg_spo2 || 95}}%`;
                }} else if (summary.avg_respiration !== null && summary.avg_respiration !== undefined) {{
                    kpiFitness.innerHTML = `${{summary.avg_respiration}} <span class="text-xs font-normal text-slate-400">brpm</span>`;
                    if (kpiFitnessSub) kpiFitnessSub.innerText = `SpO2 ${{summary.avg_spo2 || 95}}%`;
                }} else {{
                    kpiFitness.innerText = '良好';
                    if (kpiFitnessSub) kpiFitnessSub.innerText = '心肺健康';
                }}
            }}

            // Render Annual Outdoor Half & Full Marathon Stats
            renderAnnualMarathonStats();
        }}

        let marathonScopeMode = 'standard'; // 'standard' or 'extended'

        function setMarathonScope(mode) {{
            marathonScopeMode = mode;
            const btnStd = document.getElementById('btn-mara-std');
            const btnExt = document.getElementById('btn-mara-ext');
            if (btnStd && btnExt) {{
                if (mode === 'standard') {{
                    btnStd.className = 'px-2.5 py-1 rounded font-medium transition-all bg-orange-600 text-white shadow-sm';
                    btnExt.className = 'px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white';
                }} else {{
                    btnStd.className = 'px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white';
                    btnExt.className = 'px-2.5 py-1 rounded font-medium transition-all bg-orange-600 text-white shadow-sm';
                }}
            }}
            renderAnnualMarathonStats();
        }}

        function renderAnnualMarathonStats() {{
            const list = APP_DATA.annual_marathons || [];
            if (!list || list.length === 0) return;

            const isStd = marathonScopeMode === 'standard';
            const cardsContainer = document.getElementById('annual-marathon-cards');
            const tableBody = document.getElementById('annual-marathon-table-body');

            // 1. Render Cards
            if (cardsContainer) {{
                cardsContainer.innerHTML = list.map(item => {{
                    const isAll = item.year === 'all';
                    const halfCount = isStd ? item.std_half_count : item.ext_half_count;
                    const halfTime = isStd ? item.std_half_avg_time_str : item.ext_half_avg_time_str;
                    const halfPace = isStd ? item.std_half_avg_pace_str : item.ext_half_avg_pace_str;
                    const halfKm = isStd ? item.std_half_avg_km : item.ext_half_avg_km;
                    const halfFastest = isStd ? item.std_half_fastest_time_str : item.ext_half_fastest_time_str;
                    const halfFastDate = isStd ? (item.std_half_fastest_date || '') : (item.ext_half_fastest_date || '');

                    const fullCount = isStd ? item.std_full_count : item.ext_full_count;
                    const fullTime = isStd ? item.std_full_avg_time_str : item.ext_full_avg_time_str;
                    const fullPace = isStd ? item.std_full_avg_pace_str : item.ext_full_avg_pace_str;
                    const fullKm = isStd ? item.std_full_avg_km : item.ext_full_avg_km;
                    const fullFastest = isStd ? item.std_full_fastest_time_str : item.ext_full_fastest_time_str;
                    const fullFastDate = isStd ? (item.std_full_fastest_date || '') : (item.ext_full_fastest_date || '');

                    const borderCol = isAll ? 'border-amber-500/40 bg-gradient-to-b from-slate-900/90 to-amber-950/20' : 'border-slate-800 bg-slate-900/70';
                    const titleBadge = isAll ? '👑 歷史總計 (All-Time)' : `📅 ${{item.year_label}}`;

                    const halfDateBadge = halfFastDate ? halfFastDate.slice(5) : '';
                    const fullDateBadge = fullFastDate ? fullFastDate.slice(5) : '';

                    return `
                        <div class="${{borderCol}} p-3.5 rounded-xl border flex flex-col justify-between space-y-3">
                            <div class="flex items-center justify-between border-b border-slate-700/50 pb-2">
                                <span class="font-bold ${{isAll ? 'text-amber-400 text-sm' : 'text-white font-mono'}}">${{titleBadge}}</span>
                                <span class="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded-full">室外共 ${{halfCount + fullCount}} 場</span>
                            </div>

                            <!-- Half Marathon Sub-Block -->
                            <div class="bg-emerald-950/20 p-2.5 rounded-lg border border-emerald-500/20 space-y-1">
                                <div class="flex items-center justify-between">
                                    <span class="text-emerald-400 font-semibold flex items-center gap-1">
                                        <span>🏃‍♂️</span>
                                        <span>${{isStd ? '標準半馬' : '半馬/LSD'}}</span>
                                    </span>
                                    <span class="font-mono font-bold text-emerald-400">${{halfCount}} 場</span>
                                </div>
                                <div class="flex items-baseline justify-between">
                                    <span class="text-slate-400 text-[11px]">平均耗時:</span>
                                    <span class="font-mono text-white font-bold text-sm">${{halfTime}}</span>
                                </div>
                                <div class="flex items-center justify-between text-[11px] text-slate-400">
                                    <span>均速: <span class="text-emerald-300 font-mono">${{halfPace}}</span></span>
                                    <span>均距: <span class="text-slate-300 font-mono">${{halfKm ? halfKm + 'k' : '-'}}</span></span>
                                </div>
                                ${{halfFastest !== '-' ? `
                                    <div class="pt-1 mt-1 border-t border-emerald-500/10 text-[10px] text-emerald-400/90 flex justify-between">
                                        <span>最快單次:</span>
                                        <span class="font-mono font-bold">${{halfFastest}} (${{halfDateBadge}})</span>
                                    </div>
                                ` : ''}}
                            </div>

                            <!-- Full Marathon Sub-Block -->
                            <div class="bg-rose-950/20 p-2.5 rounded-lg border border-rose-500/20 space-y-1">
                                <div class="flex items-center justify-between">
                                    <span class="text-rose-400 font-semibold flex items-center gap-1">
                                        <span>🏅</span>
                                        <span>${{isStd ? '標準全馬' : '全馬/超馬'}}</span>
                                    </span>
                                    <span class="font-mono font-bold text-rose-400">${{fullCount}} 場</span>
                                </div>
                                <div class="flex items-baseline justify-between">
                                    <span class="text-slate-400 text-[11px]">平均耗時:</span>
                                    <span class="font-mono text-white font-bold text-sm">${{fullTime}}</span>
                                </div>
                                <div class="flex items-center justify-between text-[11px] text-slate-400">
                                    <span>均速: <span class="text-rose-300 font-mono">${{fullPace}}</span></span>
                                    <span>均距: <span class="text-slate-300 font-mono">${{fullKm ? fullKm + 'k' : '-'}}</span></span>
                                </div>
                                ${{fullFastest !== '-' ? `
                                    <div class="pt-1 mt-1 border-t border-rose-500/10 text-[10px] text-rose-400/90 flex justify-between">
                                        <span>最快單次:</span>
                                        <span class="font-mono font-bold">${{fullFastest}} (${{fullDateBadge}})</span>
                                    </div>
                                ` : ''}}
                            </div>
                        </div>
                    `;
                }}).join('');
            }}

            // 2. Render Table
            if (tableBody) {{
                tableBody.innerHTML = list.map(item => {{
                    const isAll = item.year === 'all';
                    const halfCount = isStd ? item.std_half_count : item.ext_half_count;
                    const halfTime = isStd ? item.std_half_avg_time_str : item.ext_half_avg_time_str;
                    const halfPace = isStd ? item.std_half_avg_pace_str : item.ext_half_avg_pace_str;
                    const halfKm = isStd ? item.std_half_avg_km : item.ext_half_avg_km;
                    const halfFastest = isStd ? item.std_half_fastest_time_str : item.ext_half_fastest_time_str;
                    const halfFastDate = isStd ? item.std_half_fastest_date : item.ext_half_fastest_date;

                    const fullCount = isStd ? item.std_full_count : item.ext_full_count;
                    const fullTime = isStd ? item.std_full_avg_time_str : item.ext_full_avg_time_str;
                    const fullPace = isStd ? item.std_full_avg_pace_str : item.ext_full_avg_pace_str;
                    const fullKm = isStd ? item.std_full_avg_km : item.ext_full_avg_km;
                    const fullFastest = isStd ? item.std_full_fastest_time_str : item.ext_full_fastest_time_str;
                    const fullFastDate = isStd ? item.std_full_fastest_date : item.ext_full_fastest_date;

                    const rowBg = isAll ? 'bg-amber-950/20 font-semibold' : 'hover:bg-slate-800/40';
                    const yearLabel = isAll ? '<span class="text-amber-400 font-bold">👑 全部歷史 (All-Time)</span>' : `<span class="font-mono font-bold text-white">${{item.year_label}}</span>`;

                    return `
                        <tr class="${{rowBg}} transition-colors">
                            <td class="py-2.5 px-3 whitespace-nowrap">${{yearLabel}}</td>
                            <td class="py-2.5 px-3 text-emerald-400 font-mono font-bold">${{halfCount}} 場</td>
                            <td class="py-2.5 px-3 text-white font-mono font-bold text-xs">${{halfTime}}</td>
                            <td class="py-2.5 px-3 text-emerald-300 font-mono">${{halfPace}}</td>
                            <td class="py-2.5 px-3 text-slate-300 font-mono text-[11px]">${{halfFastest !== '-' ? `${{halfFastest}} <span class="text-slate-500">(${{halfFastDate}})</span>` : '-'}}</td>
                            <td class="py-2.5 px-3 text-rose-400 font-mono font-bold border-l border-slate-700/60">${{fullCount}} 場</td>
                            <td class="py-2.5 px-3 text-white font-mono font-bold text-xs">${{fullTime}}</td>
                            <td class="py-2.5 px-3 text-rose-300 font-mono">${{fullPace}}</td>
                            <td class="py-2.5 px-3 text-slate-300 font-mono text-[11px]">${{fullFastest !== '-' ? `${{fullFastest}} <span class="text-slate-500">(${{fullFastDate}})</span>` : '-'}}</td>
                        </tr>
                    `;
                }}).join('');
            }}

            // Render Target Marathon Pace Suggestions
            renderMarathonPaceSuggestion();
        }}

        const MARATHON_PACE_TIERS = {{
            sub4: {{
                name: 'Sub-4 (破4小時)',
                time: '3:59:59',
                speed_kmh: 10.55,
                pace: '5:41',
                pace_range: '5:38 ~ 5:44',
                half_time: '1h 59m 59s',
                split_5k: '28m 25s',
                split_10k: '56m 52s',
                advice_title: '體能對標：具備衝刺 Sub-4 (破4小時) 的強大有氧實力！',
                advice_desc: '您在 2026 年室外半馬跑出 1h 52m 42s (均速 5:20/km)，歷史全馬最佳 4h 03m 12s (5:46/km)。依據運動生理學 VDOT 模型，半馬 1h52m 具備全馬 3h 54m ~ 3h 58m 的實力！建議將每小時時速精準控制在 10.55 km/h，配合定時補給即可成功叩關。',
                hours: [
                    {{ h: '第 1 小時 (0~1h)', range: '0 ~ 10.55 km', speed: '10.55 km/h', note: '壓制起跑興奮感，嚴守 Zone 2 心率區，第 45 分鐘吞第一包能量膠。' }},
                    {{ h: '第 2 小時 (1~2h)', range: '10.55 ~ 21.10 km', speed: '10.55 km/h', note: '通過半馬感應毯（約 1:59:59），步頻維持 180+，補充電解質鹽錠與水分。' }},
                    {{ h: '第 3 小時 (2~3h)', range: '21.10 ~ 31.65 km', speed: '10.55 km/h', note: '關鍵 30K 門檻！大腿股四頭肌開始抗疲勞，保持核心收緊，吞第三包咖啡因能量膠。' }},
                    {{ h: '第 4 小時 (3~4h)', range: '31.65 ~ 42.195 km', speed: '10.60 km/h', note: '意志力決勝階段，倒數 5 公里穩住步幅，最後 1.5 公里微幅開出全力衝向終點拱門！' }}
                ]
            }},
            sub415: {{
                name: 'Sub-4:15',
                time: '4:14:59',
                speed_kmh: 9.93,
                pace: '6:02',
                pace_range: '6:00 ~ 6:05',
                half_time: '2h 07m 30s',
                split_5k: '30m 13s',
                split_10k: '1h 00m 26s',
                advice_title: '體能對標：極佳成功率的穩健衝刺目標',
                advice_desc: '以均速 6:02/km (時速 9.93 km/h) 推進，後段保留充分體力抗衰減，適合氣候稍熱或略有起伏的認證賽道。',
                hours: [
                    {{ h: '第 1 小時 (0~1h)', range: '0 ~ 9.93 km', speed: '9.93 km/h', note: '輕鬆起跑，熱身均速 6:05/km，順暢配合呼吸節奏。' }},
                    {{ h: '第 2 小時 (1~2h)', range: '9.93 ~ 19.86 km', speed: '9.93 km/h', note: '接近半馬點，每小時補充 1 包能量膠與水站少量多次補水。' }},
                    {{ h: '第 3 小時 (2~3h)', range: '19.86 ~ 29.79 km', speed: '9.93 km/h', note: '進入 25~30 km 巡航，注意手臂擺動帶動核心，預防小腿緊繃。' }},
                    {{ h: '第 4 小時+ (3h~4h15m)', range: '29.79 ~ 42.195 km', speed: '9.95 km/h', note: '剩餘 12.4 km 耗時約 75 分鐘，咬住 6 分速列車穩步完賽。' }}
                ]
            }},
            sub430: {{
                name: 'Sub-4:30',
                time: '4:29:59',
                speed_kmh: 9.38,
                pace: '6:24',
                pace_range: '6:20 ~ 6:28',
                half_time: '2h 15m 00s',
                split_5k: '32m 00s',
                split_10k: '1h 04m 00s',
                advice_title: '體能對標：貼合您 2025 年全馬平均實力 (4h 34m)',
                advice_desc: '您在 2025 年 7 場全馬平均耗時為 4h 34m 37s (6:29/km)。此檔位幾乎處於您的舒適有氧區，能游刃有餘穩定跑完全程。',
                hours: [
                    {{ h: '第 1 小時 (0~1h)', range: '0 ~ 9.38 km', speed: '9.38 km/h', note: '舒適 Zone 2 有氧配速 6:24/km，呼吸平穩自如。' }},
                    {{ h: '第 2 小時 (1~2h)', range: '9.38 ~ 18.76 km', speed: '9.38 km/h', note: '維持均速，進水站喝水或運動飲料，第 50 分鐘補膠。' }},
                    {{ h: '第 3 小時 (2~3h)', range: '18.76 ~ 28.14 km', speed: '9.38 km/h', note: '通過半馬後持續巡航，檢查心率是否維持在乳酸閥值以下。' }},
                    {{ h: '第 4 小時+ (3h~4h30m)', range: '28.14 ~ 42.195 km', speed: '9.40 km/h', note: '剩餘 14 km 耗時約 90 分鐘，以 6:24 均速直達終點。' }}
                ]
            }},
            sub445: {{
                name: 'Sub-4:45',
                time: '4:44:59',
                speed_kmh: 8.88,
                pace: '6:45',
                pace_range: '6:40 ~ 6:50',
                half_time: '2h 22m 29s',
                split_5k: '33m 46s',
                split_10k: '1h 07m 32s',
                advice_title: '體能對標：貼合您 2026 年全馬平均實力 (4h 44m)',
                advice_desc: '您在 2026 年 3 場全馬平均耗時為 4h 44m 38s (6:42/km)。這是您目前最熟悉且能保證 100% 完賽的巡航節奏。',
                hours: [
                    {{ h: '第 1 小時 (0~1h)', range: '0 ~ 8.88 km', speed: '8.88 km/h', note: '基礎巡航節奏，心率保持在低有氧區，完全不喘。' }},
                    {{ h: '第 2 小時 (1~2h)', range: '8.88 ~ 17.76 km', speed: '8.88 km/h', note: '穩定前進，進站補水兼降溫，攝取第一份固態補給。' }},
                    {{ h: '第 3 小時 (2~3h)', range: '17.76 ~ 26.64 km', speed: '8.88 km/h', note: '過半馬後節奏不變，定時吞鹽錠補充流失鈉離子。' }},
                    {{ h: '第 4 小時+ (3h~4h45m)', range: '26.64 ~ 42.195 km', speed: '8.90 km/h', note: '剩餘 15.5 km 耗時約 105 分鐘，維持穩健步頻收尾。' }}
                ]
            }},
            sub500: {{
                name: 'Sub-5 (破5小時)',
                time: '4:59:59',
                speed_kmh: 8.44,
                pace: '7:06',
                pace_range: '7:00 ~ 7:12',
                half_time: '2h 30m 00s',
                split_5k: '35m 33s',
                split_10k: '1h 11m 06s',
                advice_title: '體能對標：超馬後恢復賽事或極端炎熱天候適用',
                advice_desc: '時速 8.44 km/h，配速 7:06/km。對您的體能而言屬於極輕鬆節奏，適合當作背靠背 (Back-to-Back) 或長距離訓練賽。',
                hours: [
                    {{ h: '第 1 小時 (0~1h)', range: '0 ~ 8.44 km', speed: '8.44 km/h', note: '超輕鬆慢跑節奏，心率 Zone 1~2。' }},
                    {{ h: '第 2 小時 (1~2h)', range: '8.44 ~ 16.88 km', speed: '8.44 km/h', note: '享受賽道氛圍，每小時補水 400ml。' }},
                    {{ h: '第 3 小時 (2~3h)', range: '16.88 ~ 25.32 km', speed: '8.44 km/h', note: '過半馬點，肌肉無明顯疲勞感。' }},
                    {{ h: '第 4 小時+ (3h~5h00m)', range: '25.32 ~ 42.195 km', speed: '8.45 km/h', note: '後段可視體能微幅提速或輕鬆巡航完賽。' }}
                ]
            }}
        }};

        let currentPaceTier = 'sub4';

        function setMarathonTargetPace(tier) {{
            currentPaceTier = tier;
            ['sub4', 'sub415', 'sub430', 'sub445', 'sub500'].forEach(t => {{
                const btn = document.getElementById(`btn-pace-${{t}}`);
                if (btn) {{
                    if (t === tier) {{
                        btn.className = 'px-2 py-1 rounded font-medium transition-all bg-sky-600 text-white shadow-sm';
                    }} else {{
                        btn.className = 'px-2 py-1 rounded font-medium transition-all text-slate-400 hover:text-white';
                    }}
                }}
            }});
            renderMarathonPaceSuggestion();
        }}

        function renderMarathonPaceSuggestion() {{
            const data = MARATHON_PACE_TIERS[currentPaceTier] || MARATHON_PACE_TIERS.sub4;
            
            const elSpeed = document.getElementById('pace-kpi-speed');
            const elDistHr = document.getElementById('pace-kpi-dist-hr');
            const elPace = document.getElementById('pace-kpi-pace');
            const elHalf = document.getElementById('pace-kpi-half');
            const el5k = document.getElementById('pace-kpi-5k');
            const elTitle = document.getElementById('pace-advice-title');
            const elDesc = document.getElementById('pace-advice-desc');
            const elHourly = document.getElementById('hourly-progression-cards');

            if (elSpeed) elSpeed.innerText = `${{data.speed_kmh}} km/h`;
            if (elDistHr) elDistHr.innerText = `每小時推進 ${{data.speed_kmh}} 公里`;
            if (elPace) elPace.innerText = `${{data.pace}} / km`;
            if (elHalf) elHalf.innerText = data.half_time;
            if (el5k) el5k.innerText = data.split_5k;
            if (elTitle) elTitle.innerText = data.advice_title;
            if (elDesc) elDesc.innerText = data.advice_desc;

            if (elHourly) {{
                elHourly.innerHTML = data.hours.map(hr => `
                    <div class="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700/60 space-y-1">
                        <div class="flex items-center justify-between border-b border-slate-700/40 pb-1">
                            <span class="font-bold text-sky-400 font-mono">${{hr.h}}</span>
                            <span class="text-[10px] text-emerald-400 font-mono font-bold">${{hr.speed}}</span>
                        </div>
                        <div class="text-[11px] font-mono text-slate-200">
                            里程: <span class="text-white font-bold">${{hr.range}}</span>
                        </div>
                        <p class="text-[10px] text-slate-400 leading-relaxed pt-0.5">${{hr.note}}</p>
                    </div>
                `).join('');
            }}
        }}

        function filterRecs(level) {{
            currentRecFilter = level;
            document.querySelectorAll('[id^="rec-filter-"]').forEach(btn => {{
                btn.className = "px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 font-medium";
            }});
            const activeBtn = document.getElementById(`rec-filter-${{level}}`);
            if (activeBtn) {{
                if (level === 'all') activeBtn.className = "px-3 py-1.5 rounded-lg bg-sky-600 text-white font-medium";
                if (level === 'critical') activeBtn.className = "px-3 py-1.5 rounded-lg bg-rose-600 text-white font-medium";
                if (level === 'warning') activeBtn.className = "px-3 py-1.5 rounded-lg bg-amber-600 text-white font-medium";
                if (level === 'good') activeBtn.className = "px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-medium";
            }}
            renderRecommendations();
        }}

        function renderRecommendations() {{
            const container = document.getElementById('recommendations-container');
            if (!container) return;
            const recs = APP_DATA.recommendations || [];
            
            const filtered = currentRecFilter === 'all' 
                ? recs 
                : recs.filter(r => r.level === currentRecFilter);

            if (filtered.length === 0) {{
                container.innerHTML = `
                    <div class="col-span-full py-8 text-center text-slate-500">
                        在此分類下無特定警示，各項相關生理與運動指標保持在良好常態範圍內！
                    </div>
                `;
                return;
            }}

            const levelConfig = {{
                'critical': {{ border: 'border-rose-500/40', badge: 'bg-rose-500/20 text-rose-400 border border-rose-500/40', icon: '🔴', tag: '建議改善' }},
                'warning': {{ border: 'border-amber-500/40', badge: 'bg-amber-500/20 text-amber-400 border border-amber-500/40', icon: '🟡', tag: '注意觀察' }},
                'good': {{ border: 'border-emerald-500/40', badge: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40', icon: '🟢', tag: '良好保持' }}
            }};

            container.innerHTML = filtered.map(item => {{
                const cfg = levelConfig[item.level] || levelConfig['warning'];
                return `
                    <div class="p-4 rounded-xl bg-slate-900/60 border ${{cfg.border}} flex flex-col justify-between space-y-3">
                        <div>
                            <div class="flex items-center justify-between gap-2">
                                <span class="text-xs font-semibold px-2 py-0.5 rounded-full ${{cfg.badge}}">
                                    ${{cfg.icon}} ${{cfg.tag}} &bull; ${{item.category}}
                                </span>
                            </div>
                            <h4 class="font-bold text-slate-100 text-base mt-2">${{item.title}}</h4>
                            <p class="text-xs text-slate-300 mt-1 leading-relaxed">${{item.description}}</p>
                        </div>
                        <div class="pt-2 border-t border-slate-800/80 text-xs text-sky-400 flex items-start gap-1.5">
                            <span class="font-semibold text-sky-500">行動建議:</span>
                            <span>${{item.action}}</span>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        // 🩺 TODAY'S EXECUTIVE HEALTH & READINESS ASSESSMENT
        function renderTodayAssessment() {{
            const records = APP_DATA.records || [];
            if (!records || records.length === 0) return;

            const latest = records[records.length - 1];
            const dateStr = latest.date || '今日';
            const readiness = latest.training_readiness;
            const rhr = latest.resting_hr;
            const hrvVal = latest.hrv_overnight_avg;
            const hrvStatus = latest.hrv_status || '未知';
            const sleepScore = latest.sleep_score;
            const sleepSecs = latest.sleep_duration_seconds || 0;
            const sleepHours = sleepSecs > 0 ? (sleepSecs / 3600).toFixed(1) : '-';
            const bbRecent = latest.body_battery_recent !== null && latest.body_battery_recent !== undefined ? latest.body_battery_recent : '-';
            const bbCharged = latest.body_battery_charged !== null && latest.body_battery_charged !== undefined ? latest.body_battery_charged : '-';

            // 1. Analyze Recent Workload in past 5 days
            const recentDays = records.slice(-5);
            let recentWorkouts = [];
            let recentKm = 0;
            let recentElev = 0;

            recentDays.forEach(r => {{
                (r.activities || []).forEach(act => {{
                    const dist = act.distance_km || 0;
                    const elev = act.elevation_gain_m || 0;
                    const type = (act.type || '').toLowerCase();
                    const isRun = dist >= 3.0 || type.includes('running') || type.includes('run');
                    if (isRun) {{
                        recentWorkouts.push({{
                            date: r.date,
                            name: act.name || '跑步',
                            dist: dist,
                            elev: elev,
                            pace: act.pace || ''
                        }});
                        recentKm += dist;
                        recentElev += elev;
                    }}
                }});
            }});

            // 2. Render Top Badges
            const badgesContainer = document.getElementById('today-status-badges');
            if (badgesContainer) {{
                let readinessBadge = '';
                if (readiness !== null && readiness !== undefined) {{
                    const rClass = readiness <= 25 
                        ? 'bg-rose-500/20 text-rose-400 border-rose-500/40' 
                        : (readiness <= 59 ? 'bg-amber-500/20 text-amber-400 border-amber-500/40' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40');
                    readinessBadge = `<span class="px-2.5 py-1 rounded-lg border ${{rClass}} font-semibold font-mono">🎯 完備度: ${{readiness}}/100</span>`;
                }}
                
                const hrvClass = (hrvStatus === 'BALANCED') 
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' 
                    : 'bg-amber-500/20 text-amber-400 border-amber-500/40';
                const hrvBadge = hrvVal ? `<span class="px-2.5 py-1 rounded-lg border ${{hrvClass}} font-semibold">⚡ HRV: ${{hrvVal}} ms (${{hrvStatus}})</span>` : '';
                
                const sleepBadge = sleepScore ? `<span class="px-2.5 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-semibold">🌙 睡眠: ${{sleepHours}}h (${{sleepScore}}分)</span>` : '';
                const bbBadge = bbRecent !== '-' ? `<span class="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/40 font-semibold">🔋 電量: ${{bbRecent}} (+${{bbCharged}})</span>` : '';

                badgesContainer.innerHTML = `
                    <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 border border-slate-700 font-mono">📅 最新: ${{dateStr}}</span>
                    ${{readinessBadge}}
                    ${{hrvBadge}}
                    ${{sleepBadge}}
                    ${{bbBadge}}
                `;
            }}

            // 3. Col 1: Fatigue & Recovery Diagnostics
            const colRecBadge = document.getElementById('col-recovery-badge');
            const colRecTitle = document.getElementById('col-recovery-title');
            const colRecDesc = document.getElementById('col-recovery-desc');
            const colRecMeta = document.getElementById('col-recovery-meta');

            if (colRecBadge && colRecTitle && colRecDesc && colRecMeta) {{
                if (readiness !== null && readiness <= 25) {{
                    colRecBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/40';
                    colRecBadge.innerText = `🔴 深度修復期 (${{readiness}}/100)`;
                    colRecTitle.innerText = '自律神經與肌群處於高負荷修復期';
                    colRecDesc.innerText = `訓練完備度目前降至偏低水準（${{readiness}}/100），反映近期連續大跑量與爬升負荷尚未完全消退。夜間自律神經（HRV ${{hrvVal ? hrvVal + ' ms' : ''}}，${{hrvStatus}}）處於持續平衡校準中，此時心血管與骨骼肌纖維正在進行重要的超補償適應修復。`;
                }} else if (readiness !== null && readiness <= 59) {{
                    colRecBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/40';
                    colRecBadge.innerText = `🟡 適度調節期 (${{readiness}}/100)`;
                    colRecTitle.innerText = '身體負荷逐步回穩，機能溫和恢復中';
                    colRecDesc.innerText = `訓練完備度處於中等水平（${{readiness}}/100）。身體可耐受基礎有氧與常態活動，但神經系統尚未達到極限輸出的最佳峰值狀態，整體生理機能正平穩回升。`;
                }} else if (readiness !== null) {{
                    colRecBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
                    colRecBadge.innerText = `🟢 狀態充沛 (${{readiness}}/100)`;
                    colRecTitle.innerText = '自律神經恢復極佳，機能完全就緒';
                    colRecDesc.innerText = `訓練完備度高達 ${{readiness}}/100，夜間自律神經調節優良，身體已充足消除前期疲勞，肌力與心肺系統已準備好迎接挑戰。`;
                }} else {{
                    colRecBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700';
                    colRecBadge.innerText = '常態觀測中';
                    colRecTitle.innerText = '生理指標維持常態運作';
                    colRecDesc.innerText = `靜止心率為 ${{rhr ? rhr + ' bpm' : '正常'}}，夜間 HRV 為 ${{hrvVal ? hrvVal + ' ms' : '常態'}}，各項指標皆在穩定區間之內。`;
                }}

                const rhrStr = rhr ? `❤️ 靜止心率: ${{rhr}} bpm` : '';
                const hrvStr = hrvVal ? `⚡ HRV: ${{hrvVal}} ms (${{hrvStatus}})` : '';
                const bbStr = bbRecent !== '-' ? `🔋 電量: ${{bbRecent}} (+${{bbCharged}})` : '';
                colRecMeta.innerHTML = [rhrStr, hrvStr, bbStr].filter(Boolean).join(' &bull; ');
            }}

            // 4. Col 2: Recent Workload Tracking
            const colWorkBadge = document.getElementById('col-workload-badge');
            const colWorkTitle = document.getElementById('col-workload-title');
            const colWorkDesc = document.getElementById('col-workload-desc');
            const colWorkMeta = document.getElementById('col-workload-meta');

            if (colWorkBadge && colWorkTitle && colWorkDesc && colWorkMeta) {{
                if (recentWorkouts.length > 0) {{
                    colWorkBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-orange-500/20 text-orange-400 border border-orange-500/40';
                    colWorkBadge.innerText = `🏃 近期累積 ${{recentKm.toFixed(1)}} km`;
                    colWorkTitle.innerText = `近幾天有 ${{recentWorkouts.length}} 次主要訓練課表負荷`;
                    const workoutListStr = recentWorkouts.map(w => `<span class="text-sky-400 font-semibold">${{w.date.slice(5)}} ${{w.name}} (${{w.dist}}k${{w.elev > 50 ? ' +' + w.elev + 'm' : ''}})</span>`).join('、');
                    colWorkDesc.innerHTML = `記錄到近期主要運動：${{workoutListStr}}。累計跑量達 ${{recentKm.toFixed(1)}} km（累積爬升 +${{Math.round(recentElev)}} m），高跑量與坡度刺激是當前肌肉疲勞與完備度回落的主因，代謝修復通常需 48~72 小時。`;
                    colWorkMeta.innerHTML = `🏔️ 爬升負荷: +${{Math.round(recentElev)}} m &bull; ⏱️ 總跑量: ${{recentKm.toFixed(1)}} km`;
                }} else {{
                    colWorkBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-slate-300 border border-slate-700';
                    colWorkBadge.innerText = '🌱 輕量常態活動';
                    colWorkTitle.innerText = '近期未記錄到 10K+ 大跑量負荷';
                    colWorkDesc.innerText = '過去數天運動量維持在低至中等水平，肌群無劇烈急性微損傷累積，身體能量消耗適中。';
                    colWorkMeta.innerHTML = '運動狀態: 基礎日常活動與休跑維護';
                }}
            }}

            // 5. Col 3: Actionable Training Prescription
            const colActBadge = document.getElementById('col-action-badge');
            const colActTitle = document.getElementById('col-action-title');
            const colActDesc = document.getElementById('col-action-desc');
            const colActMeta = document.getElementById('col-action-meta');
            const colActionBox = document.getElementById('col-action-box');

            if (colActBadge && colActTitle && colActDesc && colActMeta) {{
                if (readiness !== null && readiness <= 25) {{
                    colActBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/40';
                    colActBadge.innerText = '🛑 建議主動修復 / 輕量散步';
                    colActTitle.innerText = '今日課表方針：積極恢復日 (Active Recovery)';
                    colActDesc.innerText = `強烈建議今天不要進行任何高心率（>Zone 3）或高衝擊的長跑訓練。建議安排 20~30 分鐘輕鬆散步、下肢滾筒筋膜放鬆或瑜珈伸展。昨夜睡眠（${{sleepHours}}h）已順利充電 +${{bbCharged}}，今天多補充水分、電解質與優質蛋白質以加速微損傷修復！`;
                    colActMeta.innerHTML = '💡 建議上限: Zone 1 (<125 bpm) &bull; 滾筒伸展 &bull; 充足水分與蛋白質';
                    if (colActionBox) colActionBox.className = 'bg-slate-900/70 p-4 rounded-xl border border-rose-500/40 flex flex-col justify-between';
                }} else if (readiness !== null && readiness <= 59) {{
                    colActBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-sky-500/20 text-sky-400 border border-sky-500/40';
                    colActBadge.innerText = '🏃 建議 Zone 2 輕鬆跑';
                    colActTitle.innerText = '今日課表方針：有氧基礎維持跑 (Easy Run)';
                    colActDesc.innerText = '適合安排 30~50 分鐘的 Zone 2 輕鬆慢跑（心率保持在可輕鬆對話的節奏），或進行低衝擊室內自行車/快走，促進全身微血管循環並加速代謝廢物排除。';
                    colActMeta.innerHTML = '💡 建議強度: Zone 2 有氧區間 &bull; 避免間歇衝刺 &bull; 跑後伸展';
                    if (colActionBox) colActionBox.className = 'bg-slate-900/70 p-4 rounded-xl border border-sky-500/40 flex flex-col justify-between';
                }} else {{
                    colActBadge.className = 'px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
                    colActBadge.innerText = '🚀 適合質量訓練 / 挑戰課表';
                    colActTitle.innerText = '今日課表方針：質量訓練日 (Quality Workout)';
                    colActDesc.innerText = '身心各項機能處於高檔窗口，可按照個人課表安排間歇衝刺、節奏跑（Tempo）或長距離耐力課表。跑前務必進行 10~15 分鐘動態熱身。';
                    colActMeta.innerHTML = '💡 課表類型: 節奏跑 / 間歇衝刺 / 週末長距離 LSD';
                    if (colActionBox) colActionBox.className = 'bg-slate-900/70 p-4 rounded-xl border border-emerald-500/40 flex flex-col justify-between';
                }}
            }}
        }}

        function destroyChart(name) {{
            if (charts[name]) {{
                charts[name].destroy();
            }}
        }}

        // 📈 RENDER DAILY PLOTS (Day-by-Day Points)
        function renderDailyCharts() {{
            const dailyContainer = document.getElementById('daily-plots-container');
            if (dailyContainer && dailyContainer.classList.contains('hidden')) return;

            const records = getActiveRecords();
            const labels = records.map(r => r.date ? r.date.slice(5) : '');
            const theme = getChartThemeColors();

            // 1. RHR & HRV Chart
            destroyChart('rhrHrv');
            const rhrCanvas = document.getElementById('chart-rhr-hrv');
            if (rhrCanvas) {{
                const rhrData = records.map(r => r.resting_hr);
                const hrvData = records.map(r => r.hrv_overnight_avg);
                const ctxRhr = rhrCanvas.getContext('2d');
                charts['rhrHrv'] = new Chart(ctxRhr, {{
                    type: 'line',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                label: '每日靜止心率 (RHR, bpm)',
                                data: rhrData,
                                borderColor: '#f43f5e',
                                backgroundColor: 'rgba(244, 63, 94, 0.1)',
                                yAxisID: 'yRhr',
                                tension: 0.25,
                                fill: false,
                                pointRadius: records.length > 60 ? (records.length > 180 ? 0 : 1.5) : 3.5
                            }},
                            {{
                                label: '每日 HRV 昨夜平均 (ms)',
                                data: hrvData,
                                borderColor: '#10b981',
                                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                yAxisID: 'yHrv',
                                tension: 0.25,
                                fill: false,
                                pointRadius: records.length > 60 ? (records.length > 180 ? 0 : 1.5) : 3.5
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            yRhr: {{
                                type: 'linear',
                                position: 'left',
                                title: {{ display: true, text: 'RHR (bpm)', color: '#f43f5e' }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: '#f43f5e' }}
                            }},
                            yHrv: {{
                                type: 'linear',
                                position: 'right',
                                title: {{ display: true, text: 'HRV (ms)', color: '#10b981' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#10b981' }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 2. Sleep Stages Chart
            destroyChart('sleep');
            const sleepCanvas = document.getElementById('chart-sleep');
            if (sleepCanvas) {{
                const deepData = records.map(r => r.deep_sleep_seconds ? +(r.deep_sleep_seconds / 3600).toFixed(2) : 0);
                const remData = records.map(r => r.rem_sleep_seconds ? +(r.rem_sleep_seconds / 3600).toFixed(2) : 0);
                const lightData = records.map(r => r.light_sleep_seconds ? +(r.light_sleep_seconds / 3600).toFixed(2) : 0);
                const awakeData = records.map(r => r.awake_seconds ? +(r.awake_seconds / 3600).toFixed(2) : 0);
                const ctxSleep = sleepCanvas.getContext('2d');
                charts['sleep'] = new Chart(ctxSleep, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{ label: '深層 (Deep)', data: deepData, backgroundColor: '#3b82f6', stack: 'sleep' }},
                            {{ label: 'REM (快速動眼)', data: remData, backgroundColor: '#a855f7', stack: 'sleep' }},
                            {{ label: '淺層 (Light)', data: lightData, backgroundColor: '#64748b', stack: 'sleep' }},
                            {{ label: '清醒 (Awake)', data: awakeData, backgroundColor: '#f59e0b', stack: 'sleep' }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            y: {{
                                stacked: true,
                                title: {{ display: true, text: '時長 (小時)', color: theme.titleColor }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: theme.tickColor }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 3. Body Battery & Stress Chart
            destroyChart('bbStress');
            const bbCanvas = document.getElementById('chart-bb-stress');
            if (bbCanvas) {{
                const bbCharge = records.map(r => r.body_battery_charged || 0);
                const bbDrain = records.map(r => r.body_battery_drained ? -r.body_battery_drained : 0);
                const stressData = records.map(r => r.avg_stress);
                const ctxBB = bbCanvas.getContext('2d');
                charts['bbStress'] = new Chart(ctxBB, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{ label: '充能 (+Charge)', data: bbCharge, backgroundColor: '#10b981' }},
                            {{ label: '消耗 (-Drain)', data: bbDrain, backgroundColor: '#f43f5e' }},
                            {{
                                type: 'line',
                                label: '平均壓力指數 (Stress)',
                                data: stressData,
                                borderColor: '#f59e0b',
                                backgroundColor: '#f59e0b',
                                yAxisID: 'yStress',
                                tension: 0.3,
                                pointRadius: records.length > 60 ? (records.length > 180 ? 0 : 1.5) : 3.5
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            y: {{
                                title: {{ display: true, text: '電量點數', color: theme.titleColor }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: theme.tickColor }}
                            }},
                            yStress: {{
                                position: 'right',
                                min: 0,
                                max: 100,
                                title: {{ display: true, text: '壓力 (0-100)', color: '#f59e0b' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#f59e0b' }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 4. Activity & Steps Chart
            destroyChart('activity');
            const actCanvas = document.getElementById('chart-activity');
            if (actCanvas) {{
                const stepsData = records.map(r => r.steps || 0);
                const goalData = records.map(r => r.step_goal || 10000);
                const intData = records.map(r => (r.moderate_intensity_minutes || 0) + (r.vigorous_intensity_minutes || 0) * 2);
                const ctxAct = actCanvas.getContext('2d');
                charts['activity'] = new Chart(ctxAct, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                type: 'bar',
                                label: '每日步數',
                                data: stepsData,
                                backgroundColor: '#0ea5e9',
                                yAxisID: 'ySteps'
                            }},
                            {{
                                type: 'line',
                                label: '步數目標',
                                data: goalData,
                                borderColor: '#94a3b8',
                                borderDash: [5, 5],
                                pointRadius: 0,
                                fill: false,
                                yAxisID: 'ySteps'
                            }},
                            {{
                                type: 'line',
                                label: '強度分鐘數',
                                data: intData,
                                borderColor: '#e11d48',
                                backgroundColor: 'rgba(225, 29, 72, 0.2)',
                                fill: true,
                                yAxisID: 'yInt',
                                tension: 0.3,
                                pointRadius: records.length > 60 ? (records.length > 180 ? 0 : 1.5) : 3.5
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            ySteps: {{
                                type: 'linear',
                                position: 'left',
                                title: {{ display: true, text: '步數 (Steps)', color: '#0ea5e9' }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: '#0ea5e9' }}
                            }},
                            yInt: {{
                                type: 'linear',
                                position: 'right',
                                title: {{ display: true, text: '強度 (分鐘)', color: '#e11d48' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#e11d48' }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}
        }}

        // 📅 RENDER MONTHLY PLOTS (With Live Dual-Track Overlay Comparison)
        function renderMonthlyCharts() {{
            const monthlyContainer = document.getElementById('monthly-plots-container');
            if (monthlyContainer && monthlyContainer.classList.contains('hidden')) return;

            const monthlyData = getComputedMonthlyData();
            if (monthlyData.length === 0) return;

            const labels = monthlyData.map(m => m.month);
            const pctStr = `${{Math.round(currentTrimRatio * 100)}}%`;
            const theme = getChartThemeColors();

            // ⭐ 1. Monthly Stacked Sleep Stages Chart + Raw Total Overlay Line ⭐
            destroyChart('monthlySleepStages');
            const monthlySleepCanvas = document.getElementById('chart-monthly-sleep-stages');
            if (monthlySleepCanvas) {{
                const deepMonthlyData = monthlyData.map(m => m.avg_deep_hours || 0);
                const remMonthlyData = monthlyData.map(m => m.avg_rem_hours || 0);
                const lightMonthlyData = monthlyData.map(m => m.avg_light_hours || 0);
                const awakeMonthlyData = monthlyData.map(m => m.avg_awake_hours || 0);
                const rawSleepTotals = monthlyData.map(m => m.raw.avg_sleep_hours || 0);

                const sleepDatasets = [
                    {{ label: isOutlierTrimEnabled ? `深層 (Deep, 去噪${{pctStr}})` : '深層 (Deep)', data: deepMonthlyData, backgroundColor: '#3b82f6', stack: 'monthlySleep' }},
                    {{ label: isOutlierTrimEnabled ? `REM (快速動眼, 去噪${{pctStr}})` : 'REM (快速動眼)', data: remMonthlyData, backgroundColor: '#a855f7', stack: 'monthlySleep' }},
                    {{ label: isOutlierTrimEnabled ? `淺層 (Light, 去噪${{pctStr}})` : '淺層 (Light)', data: lightMonthlyData, backgroundColor: '#64748b', stack: 'monthlySleep' }},
                    {{ label: isOutlierTrimEnabled ? `清醒 (Awake, 去噪${{pctStr}})` : '清醒 (Awake)', data: awakeMonthlyData, backgroundColor: '#f59e0b', stack: 'monthlySleep' }}
                ];

                if (isOutlierTrimEnabled && showOverlayComparison) {{
                    sleepDatasets.push({{
                        type: 'line',
                        label: '🔍 原始全量睡眠總時長 (Raw Unfiltered)',
                        data: rawSleepTotals,
                        borderColor: '#eab308',
                        borderDash: [4, 4],
                        backgroundColor: 'rgba(234, 179, 8, 0.1)',
                        pointRadius: 4.5,
                        borderWidth: 2,
                        fill: false,
                        tension: 0.2
                    }});
                }}

                const ctxMonthlySleep = monthlySleepCanvas.getContext('2d');
                charts['monthlySleepStages'] = new Chart(ctxMonthlySleep, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: sleepDatasets
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            y: {{
                                stacked: true,
                                title: {{ display: true, text: isOutlierTrimEnabled ? `月均時長 (小時, 去噪${{pctStr}})` : '月均時長 (小時)', color: theme.titleColor }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: theme.tickColor }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 2. Monthly Mileage & 10K+ Count
            destroyChart('monthlyMileage');
            const monthlyMileageCanvas = document.getElementById('chart-monthly-mileage');
            if (monthlyMileageCanvas) {{
                const kmData = monthlyData.map(m => m.total_run_km);
                const count10kData = monthlyData.map(m => m.runs_10k_plus);

                const ctxMileage = monthlyMileageCanvas.getContext('2d');
                charts['monthlyMileage'] = new Chart(ctxMileage, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                type: 'bar',
                                label: '月總跑量 (km)',
                                data: kmData,
                                backgroundColor: '#38bdf8',
                                yAxisID: 'yKm'
                            }},
                            {{
                                type: 'line',
                                label: '10K+ 長跑次數',
                                data: count10kData,
                                borderColor: '#f97316',
                                backgroundColor: '#f97316',
                                yAxisID: 'yCount',
                                tension: 0.2,
                                pointRadius: 4.5
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            yKm: {{
                                type: 'linear',
                                position: 'left',
                                title: {{ display: true, text: '月跑量 (km)', color: '#38bdf8' }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: '#38bdf8' }}
                            }},
                            yCount: {{
                                type: 'linear',
                                position: 'right',
                                title: {{ display: true, text: '次數', color: '#f97316' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#f97316', stepSize: 1 }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 3. Monthly RHR & HRV with Dual-Track Overlay Lines
            destroyChart('monthlyVitals');
            const monthlyVitalsCanvas = document.getElementById('chart-monthly-vitals');
            if (monthlyVitalsCanvas) {{
                const rhrData = monthlyData.map(m => m.avg_rhr);
                const hrvData = monthlyData.map(m => m.avg_hrv);
                const rawRhrData = monthlyData.map(m => m.raw.avg_rhr);
                const rawHrvData = monthlyData.map(m => m.raw.avg_hrv);

                const vitalsDatasets = [
                    {{
                        label: isOutlierTrimEnabled ? `月均 RHR (bpm, 去噪${{pctStr}})` : '月均 RHR (bpm)',
                        data: rhrData,
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        yAxisID: 'yRhr',
                        tension: 0.3,
                        borderWidth: 2.5,
                        pointRadius: 4.5
                    }},
                    {{
                        label: isOutlierTrimEnabled ? `月均 HRV (ms, 去噪${{pctStr}})` : '月均 HRV (ms)',
                        data: hrvData,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        yAxisID: 'yHrv',
                        tension: 0.3,
                        borderWidth: 2.5,
                        pointRadius: 4.5
                    }}
                ];

                if (isOutlierTrimEnabled && showOverlayComparison) {{
                    vitalsDatasets.push({{
                        label: '🔍 原始全量 RHR (Raw)',
                        data: rawRhrData,
                        borderColor: '#fda4af',
                        borderDash: [4, 4],
                        borderWidth: 1.5,
                        pointRadius: 3.5,
                        yAxisID: 'yRhr',
                        fill: false
                    }});
                    vitalsDatasets.push({{
                        label: '🔍 原始全量 HRV (Raw)',
                        data: rawHrvData,
                        borderColor: '#6ee7b7',
                        borderDash: [4, 4],
                        borderWidth: 1.5,
                        pointRadius: 3.5,
                        yAxisID: 'yHrv',
                        fill: false
                    }});
                }}

                const ctxVitals = monthlyVitalsCanvas.getContext('2d');
                charts['monthlyVitals'] = new Chart(ctxVitals, {{
                    type: 'line',
                    data: {{
                        labels: labels,
                        datasets: vitalsDatasets
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            yRhr: {{
                                type: 'linear',
                                position: 'left',
                                title: {{ display: true, text: 'RHR (bpm)', color: '#f43f5e' }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: '#f43f5e' }}
                            }},
                            yHrv: {{
                                type: 'linear',
                                position: 'right',
                                title: {{ display: true, text: 'HRV (ms)', color: '#10b981' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#10b981' }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 4. Monthly Calories & Races
            destroyChart('monthlyCalories');
            const monthlyCaloriesCanvas = document.getElementById('chart-monthly-calories');
            if (monthlyCaloriesCanvas) {{
                const calData = monthlyData.map(m => m.total_calories);
                const fullMarathonData = monthlyData.map(m => m.full_marathons);
                const halfMarathonData = monthlyData.map(m => m.half_marathons);

                const ctxCal = monthlyCaloriesCanvas.getContext('2d');
                charts['monthlyCalories'] = new Chart(ctxCal, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                type: 'bar',
                                label: '運動總卡路里 (kcal)',
                                data: calData,
                                backgroundColor: '#f43f5e',
                                yAxisID: 'yCal'
                            }},
                            {{
                                type: 'line',
                                label: '全馬場次',
                                data: fullMarathonData,
                                borderColor: '#e11d48',
                                backgroundColor: '#e11d48',
                                yAxisID: 'yRace',
                                pointRadius: 4
                            }},
                            {{
                                type: 'line',
                                label: '半馬場次',
                                data: halfMarathonData,
                                borderColor: '#f59e0b',
                                backgroundColor: '#f59e0b',
                                yAxisID: 'yRace',
                                borderDash: [3, 3],
                                pointRadius: 4
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            yCal: {{
                                type: 'linear',
                                position: 'left',
                                title: {{ display: true, text: '卡路里 (kcal)', color: '#f43f5e' }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{ color: '#f43f5e' }}
                            }},
                            yRace: {{
                                type: 'linear',
                                position: 'right',
                                title: {{ display: true, text: '場次', color: '#f59e0b' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#f59e0b', stepSize: 1 }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }}
                        }}
                    }}
                }});
            }}

            // 5. Monthly YoY & MoM Growth Dynamics
            destroyChart('monthlyYoYMoM');
            const monthlyYoYMoMCanvas = document.getElementById('chart-monthly-yoy-mom');
            if (monthlyYoYMoMCanvas) {{
                const kmData = monthlyData.map(m => m.total_run_km);
                const prevYearKmData = monthlyData.map(m => m.last_year_run_km);
                const yoyData = monthlyData.map(m => m.yoy_km_growth_pct);
                const momData = monthlyData.map(m => m.mom_km_growth_pct);

                const ctxYoY = monthlyYoYMoMCanvas.getContext('2d');
                charts['monthlyYoYMoM'] = new Chart(ctxYoY, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                type: 'line',
                                label: 'YoY 年增長率 (%)',
                                data: yoyData,
                                borderColor: '#a855f7',
                                backgroundColor: 'rgba(168, 85, 247, 0.1)',
                                borderWidth: 2.5,
                                tension: 0.25,
                                pointRadius: 4,
                                pointHoverRadius: 6,
                                yAxisID: 'yPct'
                            }},
                            {{
                                type: 'line',
                                label: 'MoM 月增長率 (%)',
                                data: momData,
                                borderColor: '#10b981',
                                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                borderWidth: 2,
                                borderDash: [4, 4],
                                tension: 0.2,
                                pointRadius: 3.5,
                                yAxisID: 'yPct'
                            }},
                            {{
                                type: 'bar',
                                label: '當月跑量 (km)',
                                data: kmData,
                                backgroundColor: 'rgba(56, 189, 248, 0.75)',
                                borderColor: '#0284c7',
                                borderWidth: 1,
                                yAxisID: 'yKm'
                            }},
                            {{
                                type: 'bar',
                                label: '去年同期跑量 (km)',
                                data: prevYearKmData,
                                backgroundColor: 'rgba(148, 163, 184, 0.35)',
                                borderColor: '#94a3b8',
                                borderWidth: 1,
                                yAxisID: 'yKm'
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{ grid: {{ color: theme.gridColor }}, ticks: {{ color: theme.tickColor }} }},
                            yPct: {{
                                type: 'linear',
                                position: 'left',
                                title: {{ display: true, text: '增長率 (%)', color: '#a855f7' }},
                                grid: {{ color: theme.gridColor }},
                                ticks: {{
                                    color: '#a855f7',
                                    callback: function(v) {{ return (v > 0 ? '+' : '') + v + '%'; }}
                                }}
                            }},
                            yKm: {{
                                type: 'linear',
                                position: 'right',
                                title: {{ display: true, text: '月跑量 (km)', color: '#38bdf8' }},
                                grid: {{ drawOnChartArea: false }},
                                ticks: {{ color: '#38bdf8' }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ labels: {{ color: theme.legendColor }} }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        let label = context.dataset.label || '';
                                        if (context.parsed.y !== null && context.parsed.y !== undefined) {{
                                            if (label.includes('%')) {{
                                                const val = context.parsed.y;
                                                return `${{label}}: ${{val > 0 ? '+' : ''}}${{val}}%`;
                                            }} else {{
                                                return `${{label}}: ${{context.parsed.y}} km`;
                                            }}
                                        }}
                                        return `${{label}}: -`;
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
            }}
        }}

        // 📊 Distance Histogram State & Interactive Logic (次數 vs 公里數, 室內外分組, 年/月/時序篩選, 年度YoY / 月度YoY / 月度MoM 對比)
        let histTimeMode = 'all'; // 'all', 'year', 'month', 'trailing', 'yoy_year', 'yoy_month', 'mom'
        let histSelectedYear = 'all';
        let histSelectedMonth = 'all';
        let histSelectedTrailing = 365;
        let histSelectedYoYYear = '';
        let histSelectedYoYMonth = '';
        let histSelectedMoM = '';
        let histGroupMode = 'stacked'; // 'stacked', 'grouped', 'split_trail'
        let histBinMode = 'athletic'; // 'athletic', 'fixed_2k', 'fixed_5k'
        let isHistTableOpen = false;

        function setHistGroupMode(mode) {{
            histGroupMode = mode;
            ['stacked', 'grouped', 'split'].forEach(m => {{
                const btn = document.getElementById(`btn-hist-${{m}}`);
                if (btn) {{
                    const activeKey = m === 'split' ? 'split_trail' : m;
                    if (activeKey === mode) {{
                        btn.className = 'px-2.5 py-1 rounded font-medium transition-all bg-sky-600 text-white shadow-sm';
                    }} else {{
                        btn.className = 'px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white';
                    }}
                }}
            }});
            renderDistanceHistogram();
        }}

        function setHistBinMode(mode) {{
            histBinMode = mode;
            const modes = [
                {{ id: 'athletic', key: 'athletic' }},
                {{ id: '2k', key: 'fixed_2k' }},
                {{ id: '5k', key: 'fixed_5k' }}
            ];
            modes.forEach(m => {{
                const btn = document.getElementById(`btn-bin-${{m.id}}`);
                if (btn) {{
                    if (m.key === mode) {{
                        btn.className = 'px-2.5 py-1 rounded font-medium transition-all bg-sky-600 text-white shadow-sm';
                    }} else {{
                        btn.className = 'px-2.5 py-1 rounded font-medium transition-all text-slate-400 hover:text-white';
                    }}
                }}
            }});
            renderDistanceHistogram();
        }}

        function setHistTimeMode(mode) {{
            histTimeMode = mode;
            ['all', 'year', 'month', 'trailing', 'yoy_year', 'yoy_month', 'mom'].forEach(m => {{
                const btn = document.getElementById(`btn-time-${{m}}`);
                if (btn) {{
                    if (m === mode) {{
                        let activeBg = 'bg-sky-600';
                        if (m === 'yoy_year') activeBg = 'bg-purple-600';
                        else if (m === 'yoy_month') activeBg = 'bg-fuchsia-600';
                        else if (m === 'mom') activeBg = 'bg-emerald-600';
                        btn.className = `px-2.5 py-1 rounded-lg font-medium transition-all ${{activeBg}} text-white shadow-sm`;
                    }} else {{
                        let textColor = 'text-slate-300';
                        if (m === 'yoy_year') textColor = 'text-purple-400';
                        else if (m === 'yoy_month') textColor = 'text-fuchsia-400';
                        else if (m === 'mom') textColor = 'text-emerald-400';
                        btn.className = `px-2.5 py-1 rounded-lg font-medium transition-all bg-slate-800 ${{textColor}} hover:bg-slate-700`;
                    }}
                }}
            }});

            const yearWrap = document.getElementById('hist-year-select-wrap');
            const monthWrap = document.getElementById('hist-month-select-wrap');
            const trailWrap = document.getElementById('hist-trailing-select-wrap');
            const yoyYearWrap = document.getElementById('hist-yoy-year-select-wrap');
            const yoyMonthWrap = document.getElementById('hist-yoy-month-select-wrap');
            const momWrap = document.getElementById('hist-mom-select-wrap');

            if (yearWrap) yearWrap.classList.toggle('hidden', mode !== 'year');
            if (monthWrap) monthWrap.classList.toggle('hidden', mode !== 'month');
            if (trailWrap) trailWrap.classList.toggle('hidden', mode !== 'trailing');
            if (yoyYearWrap) yoyYearWrap.classList.toggle('hidden', mode !== 'yoy_year');
            if (yoyMonthWrap) yoyMonthWrap.classList.toggle('hidden', mode !== 'yoy_month');
            if (momWrap) momWrap.classList.toggle('hidden', mode !== 'mom');

            renderDistanceHistogram();
        }}

        function onHistYearChange() {{
            const select = document.getElementById('hist-year-select');
            if (select) {{
                histSelectedYear = select.value;
                renderDistanceHistogram();
            }}
        }}

        function onHistMonthChange() {{
            const select = document.getElementById('hist-month-select');
            if (select) {{
                histSelectedMonth = select.value;
                renderDistanceHistogram();
            }}
        }}

        function onHistTrailingChange() {{
            const select = document.getElementById('hist-trailing-select');
            if (select) {{
                histSelectedTrailing = parseInt(select.value, 10) || 365;
                renderDistanceHistogram();
            }}
        }}

        function onHistYoYYearChange() {{
            const select = document.getElementById('hist-yoy-year-select');
            if (select) {{
                histSelectedYoYYear = select.value;
                renderDistanceHistogram();
            }}
        }}

        function onHistYoYMonthChange() {{
            const select = document.getElementById('hist-yoy-month-select');
            if (select) {{
                histSelectedYoYMonth = select.value;
                renderDistanceHistogram();
            }}
        }}

        function onHistMoMChange() {{
            const select = document.getElementById('hist-mom-select');
            if (select) {{
                histSelectedMoM = select.value;
                renderDistanceHistogram();
            }}
        }}

        function toggleHistTable() {{
            isHistTableOpen = !isHistTableOpen;
            const container = document.getElementById('hist-table-container');
            const icon = document.getElementById('hist-table-toggle-icon');
            if (container) container.classList.toggle('hidden', !isHistTableOpen);
            if (icon) icon.innerText = isHistTableOpen ? '▼' : '▶';
        }}

        function getAllActivities() {{
            const list = [];
            const records = APP_DATA.records || [];
            records.forEach(r => {{
                const d = r.date || '';
                (r.activities || []).forEach(act => {{
                    const km = act.distance_km || 0;
                    if (km > 0) {{
                        const actType = (act.type || '').toLowerCase();
                        const isIndoor = actType.includes('treadmill') || actType.includes('indoor');
                        const isTrail = actType.includes('trail') || actType.includes('mountain') || actType.includes('hiking');
                        list.push({{
                            date: d,
                            year: d.slice(0, 4),
                            month: d.slice(0, 7),
                            distance_km: km,
                            type: actType,
                            name: act.name || '',
                            isIndoor: isIndoor,
                            isTrail: isTrail,
                            duration_minutes: act.duration_minutes || 0,
                            calories: act.calories || 0
                        }});
                    }}
                }});
            }});
            return list;
        }}

        function initDistanceHistogramControls() {{
            const allActs = getAllActivities();
            const years = [...new Set(allActs.map(a => a.year).filter(Boolean))].sort().reverse();
            const months = [...new Set(allActs.map(a => a.month).filter(Boolean))].sort().reverse();

            const yearSelect = document.getElementById('hist-year-select');
            if (yearSelect && yearSelect.options.length === 0) {{
                yearSelect.innerHTML = years.map(y => `<option value="${{y}}">${{y}} 年</option>`).join('');
                if (years.length > 0 && histSelectedYear === 'all') {{
                    histSelectedYear = years[0];
                }}
            }}

            const monthSelect = document.getElementById('hist-month-select');
            if (monthSelect && monthSelect.options.length === 0) {{
                monthSelect.innerHTML = months.map(m => `<option value="${{m}}">${{m}}</option>`).join('');
                if (months.length > 0 && histSelectedMonth === 'all') {{
                    histSelectedMonth = months[0];
                }}
            }}

            // 年度 YoY Options (Full year vs full year)
            const yoyYearSelect = document.getElementById('hist-yoy-year-select');
            if (yoyYearSelect && yoyYearSelect.options.length === 0) {{
                const yoyYearOpts = [];
                for (let i = 0; i < years.length - 1; i++) {{
                    yoyYearOpts.push({{
                        value: `${{years[i]}}:${{years[i+1]}}`,
                        text: `📅 ${{years[i]}} vs ${{years[i+1]}} (年度同比)`
                    }});
                }}
                yoyYearSelect.innerHTML = yoyYearOpts.map(o => `<option value="${{o.value}}">${{o.text}}</option>`).join('');
                if (yoyYearOpts.length > 0 && !histSelectedYoYYear) {{
                    histSelectedYoYYear = yoyYearOpts[0].value;
                }}
            }}

            // 月度 YoY Options (Same month across consecutive years)
            const yoyMonthSelect = document.getElementById('hist-yoy-month-select');
            if (yoyMonthSelect && yoyMonthSelect.options.length === 0) {{
                const yoyMonthOpts = [];
                months.forEach(m => {{
                    const parts = m.split('-');
                    if (parts.length === 2) {{
                        const prevYM = `${{parseInt(parts[0], 10) - 1}}-${{parts[1]}}`;
                        if (months.includes(prevYM)) {{
                            yoyMonthOpts.push({{
                                value: `${{m}}:${{prevYM}}`,
                                text: `🗓️ ${{m}} vs ${{prevYM}} (月度同比)`
                            }});
                        }}
                    }}
                }});
                yoyMonthSelect.innerHTML = yoyMonthOpts.map(o => `<option value="${{o.value}}">${{o.text}}</option>`).join('');
                if (yoyMonthOpts.length > 0 && !histSelectedYoYMonth) {{
                    histSelectedYoYMonth = yoyMonthOpts[0].value;
                }}
            }}

            // 月度 MoM Options (Adjacent months)
            const momSelect = document.getElementById('hist-mom-select');
            if (momSelect && momSelect.options.length === 0) {{
                const momOpts = [];
                for (let i = 0; i < months.length - 1; i++) {{
                    momOpts.push({{
                        value: `${{months[i]}}:${{months[i+1]}}`,
                        text: `🔄 ${{months[i]}} vs ${{months[i+1]}} (月度環比)`
                    }});
                }}
                momSelect.innerHTML = momOpts.map(o => `<option value="${{o.value}}">${{o.text}}</option>`).join('');
                if (momOpts.length > 0 && !histSelectedMoM) {{
                    histSelectedMoM = momOpts[0].value;
                }}
            }}
        }}

        function getFilteredActivities() {{
            const allActs = getAllActivities();
            if (histTimeMode === 'all') {{
                const desc = document.getElementById('hist-current-filter-desc');
                if (desc) desc.innerText = `顯示: 全歷史累計 (共 ${{allActs.length}} 場次)`;
                return allActs;
            }}
            if (histTimeMode === 'year') {{
                const filtered = allActs.filter(a => a.year === histSelectedYear);
                const desc = document.getElementById('hist-current-filter-desc');
                if (desc) desc.innerText = `顯示: ${{histSelectedYear}} 年 (共 ${{filtered.length}} 場次)`;
                return filtered;
            }}
            if (histTimeMode === 'month') {{
                const filtered = allActs.filter(a => a.month === histSelectedMonth);
                const desc = document.getElementById('hist-current-filter-desc');
                if (desc) desc.innerText = `顯示: ${{histSelectedMonth}} 月 (共 ${{filtered.length}} 場次)`;
                return filtered;
            }}
            if (histTimeMode === 'trailing') {{
                if (allActs.length === 0) return [];
                const sortedDates = allActs.map(a => a.date).sort();
                const latestDateStr = sortedDates[sortedDates.length - 1];
                const latestDate = new Date(latestDateStr);
                const cutoff = new Date(latestDate.getTime() - histSelectedTrailing * 24 * 60 * 60 * 1000);
                const cutoffStr = cutoff.toISOString().slice(0, 10);
                const filtered = allActs.filter(a => a.date >= cutoffStr);
                const desc = document.getElementById('hist-current-filter-desc');
                if (desc) desc.innerText = `顯示: 近 ${{histSelectedTrailing}} 天 (~${{latestDateStr}}, 共 ${{filtered.length}} 場次)`;
                return filtered;
            }}
            return allActs;
        }}

        function getHistogramBinsDef() {{
            if (histBinMode === 'athletic') {{
                return [
                    {{ id: 'b0', min: 0, max: 3, label: '< 3 km', sublabel: '短程/熱身' }},
                    {{ id: 'b1', min: 3, max: 5, label: '3 - 5 km', sublabel: '日常恢復' }},
                    {{ id: 'b2', min: 5, max: 8, label: '5 - 8 km', sublabel: '基礎節奏' }},
                    {{ id: 'b3', min: 8, max: 10, label: '8 - 10 km', sublabel: '中程維持' }},
                    {{ id: 'b4', min: 10, max: 15, label: '10 - 15 km', sublabel: '突破10K' }},
                    {{ id: 'b5', min: 15, max: 21.1, label: '15 - 21 km', sublabel: '半馬/LSD' }},
                    {{ id: 'b6', min: 21.1, max: 30, label: '21 - 30 km', sublabel: '超半馬特訓' }},
                    {{ id: 'b7', min: 30, max: 42.2, label: '30 - 42 km', sublabel: '全馬挑戰' }},
                    {{ id: 'b8', min: 42.2, max: 9999, label: '≥ 42.2 km', sublabel: '全馬/超馬' }}
                ];
            }} else if (histBinMode === 'fixed_2k') {{
                return [
                    {{ id: '2k_0', min: 0, max: 2, label: '0-2 km', sublabel: '' }},
                    {{ id: '2k_1', min: 2, max: 4, label: '2-4 km', sublabel: '' }},
                    {{ id: '2k_2', min: 4, max: 6, label: '4-6 km', sublabel: '' }},
                    {{ id: '2k_3', min: 6, max: 8, label: '6-8 km', sublabel: '' }},
                    {{ id: '2k_4', min: 8, max: 10, label: '8-10 km', sublabel: '' }},
                    {{ id: '2k_5', min: 10, max: 12, label: '10-12 km', sublabel: '' }},
                    {{ id: '2k_6', min: 12, max: 14, label: '12-14 km', sublabel: '' }},
                    {{ id: '2k_7', min: 14, max: 16, label: '14-16 km', sublabel: '' }},
                    {{ id: '2k_8', min: 16, max: 18, label: '16-18 km', sublabel: '' }},
                    {{ id: '2k_9', min: 18, max: 20, label: '18-20 km', sublabel: '' }},
                    {{ id: '2k_10', min: 20, max: 25, label: '20-25 km', sublabel: '' }},
                    {{ id: '2k_11', min: 25, max: 30, label: '25-30 km', sublabel: '' }},
                    {{ id: '2k_12', min: 30, max: 42.2, label: '30-42 km', sublabel: '' }},
                    {{ id: '2k_13', min: 42.2, max: 9999, label: '≥ 42 km', sublabel: '' }}
                ];
            }} else {{
                return [
                    {{ id: '5k_0', min: 0, max: 5, label: '0-5 km', sublabel: '' }},
                    {{ id: '5k_1', min: 5, max: 10, label: '5-10 km', sublabel: '' }},
                    {{ id: '5k_2', min: 10, max: 15, label: '10-15 km', sublabel: '' }},
                    {{ id: '5k_3', min: 15, max: 20, label: '15-20 km', sublabel: '' }},
                    {{ id: '5k_4', min: 20, max: 25, label: '20-25 km', sublabel: '' }},
                    {{ id: '5k_5', min: 25, max: 30, label: '25-30 km', sublabel: '' }},
                    {{ id: '5k_6', min: 30, max: 35, label: '30-35 km', sublabel: '' }},
                    {{ id: '5k_7', min: 35, max: 40, label: '35-40 km', sublabel: '' }},
                    {{ id: '5k_8', min: 40, max: 45, label: '40-45 km', sublabel: '' }},
                    {{ id: '5k_9', min: 45, max: 9999, label: '≥ 45 km', sublabel: '' }}
                ];
            }}
        }}

        // Inline Chart.js Plugin: Bar Data Labels for Distance Histogram
        function getHistogramDataLabelsPlugin(isStacked, theme) {{
            return {{
                id: 'histogramDataLabelsPlugin',
                afterDatasetsDraw(chart) {{
                    const ctx = chart.ctx;
                    const datasets = chart.data.datasets;
                    if (!datasets || datasets.length === 0) return;

                    const isDark = theme ? theme.isDark : document.documentElement.classList.contains('dark');
                    const topTextColor = isDark ? '#f1f5f9' : '#1e293b';

                    if (isStacked) {{
                        const numBins = chart.data.labels.length;
                        for (let j = 0; j < numBins; j++) {{
                            let stackTotal = 0;
                            let nonZeroSegments = [];

                            for (let i = 0; i < datasets.length; i++) {{
                                const meta = chart.getDatasetMeta(i);
                                if (meta.hidden) continue;
                                const val = datasets[i].data[j];
                                if (val && val > 0) {{
                                    stackTotal += val;
                                    const el = meta.data[j];
                                    if (el) {{
                                        nonZeroSegments.push({{
                                            val: val,
                                            el: el,
                                            datasetIndex: i
                                        }});
                                    }}
                                }}
                            }}

                            if (stackTotal <= 0 || nonZeroSegments.length === 0) continue;

                            // 1. Draw segment counts inside segments when there are multiple non-zero segments
                            if (nonZeroSegments.length > 1) {{
                                nonZeroSegments.forEach(seg => {{
                                    const segHeight = Math.abs(seg.el.base - seg.el.y);
                                    if (segHeight >= 14 && (seg.el.width === undefined || seg.el.width >= 12)) {{
                                        ctx.save();
                                        ctx.font = 'bold 10px Inter, system-ui, -apple-system, sans-serif';
                                        ctx.textAlign = 'center';
                                        ctx.textBaseline = 'middle';
                                        ctx.fillStyle = '#ffffff';
                                        ctx.shadowColor = 'rgba(0, 0, 0, 0.75)';
                                        ctx.shadowBlur = 3;
                                        ctx.shadowOffsetX = 0;
                                        ctx.shadowOffsetY = 1;
                                        const midY = (seg.el.y + seg.el.base) / 2;
                                        ctx.fillText(seg.val, seg.el.x, midY);
                                        ctx.restore();
                                    }}
                                }});
                            }}

                            // 2. Draw stack total on top of the stack
                            let topElement = nonZeroSegments[0].el;
                            for (let k = 1; k < nonZeroSegments.length; k++) {{
                                if (nonZeroSegments[k].el.y < topElement.y) {{
                                    topElement = nonZeroSegments[k].el;
                                }}
                            }}

                            ctx.save();
                            ctx.font = 'bold 11px Inter, system-ui, -apple-system, sans-serif';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'bottom';
                            ctx.fillStyle = topTextColor;
                            ctx.shadowColor = isDark ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.8)';
                            ctx.shadowBlur = 3;
                            let posY = topElement.y - 4;
                            if (posY < chart.chartArea.top + 8) {{
                                posY = topElement.y + 13;
                                ctx.textBaseline = 'top';
                                ctx.fillStyle = '#ffffff';
                                ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
                            }}
                            ctx.fillText(stackTotal, topElement.x, posY);
                            ctx.restore();
                        }}
                    }} else {{
                        // Grouped mode (side-by-side bars)
                        for (let i = 0; i < datasets.length; i++) {{
                            const meta = chart.getDatasetMeta(i);
                            if (meta.hidden) continue;
                            for (let j = 0; j < datasets[i].data.length; j++) {{
                                const val = datasets[i].data[j];
                                if (val && val > 0) {{
                                    const el = meta.data[j];
                                    if (!el) continue;
                                    ctx.save();
                                    ctx.font = 'bold 10px Inter, system-ui, -apple-system, sans-serif';
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'bottom';
                                    ctx.fillStyle = topTextColor;
                                    ctx.shadowColor = isDark ? 'rgba(0, 0, 0, 0.8)' : 'rgba(255, 255, 255, 0.8)';
                                    ctx.shadowBlur = 3;
                                    let posY = el.y - 4;
                                    if (posY < chart.chartArea.top + 8) {{
                                        posY = el.y + 13;
                                        ctx.textBaseline = 'top';
                                        ctx.fillStyle = '#ffffff';
                                        ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
                                    }}
                                    ctx.fillText(val, el.x, posY);
                                    ctx.restore();
                                }}
                            }}
                        }}
                    }}
                }}
            }};
        }}

        function renderDistanceHistogram() {{
            const canvas = document.getElementById('chart-distance-histogram');
            if (!canvas) return;

            initDistanceHistogramControls();
            const theme = getChartThemeColors();
            const binsDef = getHistogramBinsDef();
            const isComparison = histTimeMode === 'yoy_year' || histTimeMode === 'yoy_month' || histTimeMode === 'mom';

            if (isComparison) {{
                // 📅 年度 YoY, 🗓️ 月度 YoY, or 🔄 月度 MoM Comparative Distribution Mode
                const allActs = getAllActivities();
                let curActs = [];
                let cmpActs = [];
                let curTitle = '';
                let cmpTitle = '';
                let compTag = '';
                let cmpColor = 'rgba(168, 85, 247, 0.85)';
                let cmpBorderColor = '#9333ea';
                let cmpTextClass = 'text-purple-400';
                let cmpTextLightClass = 'text-purple-300';

                if (histTimeMode === 'yoy_year') {{
                    compTag = '年度 YoY (年同比)';
                    const parts = (histSelectedYoYYear || '').split(':');
                    const p1 = parts[0] || '';
                    const p2 = parts[1] || '';
                    curActs = allActs.filter(a => a.year === p1);
                    cmpActs = allActs.filter(a => a.year === p2);
                    curTitle = `${{p1}} 年 (當期)`;
                    cmpTitle = `${{p2}} 年 (去年)`;
                    cmpColor = theme.isDark ? 'rgba(168, 85, 247, 0.85)' : 'rgba(126, 34, 206, 0.9)';
                    cmpBorderColor = theme.isDark ? '#9333ea' : '#6b21a8';
                    cmpTextClass = 'text-purple-400';
                    cmpTextLightClass = 'text-purple-300';
                }} else if (histTimeMode === 'yoy_month') {{
                    compTag = '月度 YoY (同月同比)';
                    const parts = (histSelectedYoYMonth || '').split(':');
                    const p1 = parts[0] || '';
                    const p2 = parts[1] || '';
                    curActs = allActs.filter(a => a.month === p1);
                    cmpActs = allActs.filter(a => a.month === p2);
                    curTitle = `${{p1}} (當期月)`;
                    cmpTitle = `${{p2}} (去年同月)`;
                    cmpColor = theme.isDark ? 'rgba(217, 70, 239, 0.85)' : 'rgba(162, 28, 175, 0.9)';
                    cmpBorderColor = theme.isDark ? '#c026d3' : '#86198f';
                    cmpTextClass = 'text-fuchsia-400';
                    cmpTextLightClass = 'text-fuchsia-300';
                }} else {{
                    compTag = '月度 MoM (月環比)';
                    const parts = (histSelectedMoM || '').split(':');
                    const curM = parts[0] || '';
                    const prevM = parts[1] || '';
                    curActs = allActs.filter(a => a.month === curM);
                    cmpActs = allActs.filter(a => a.month === prevM);
                    curTitle = `${{curM}} (當月)`;
                    cmpTitle = `${{prevM}} (上月)`;
                    cmpColor = theme.isDark ? 'rgba(245, 158, 11, 0.85)' : 'rgba(217, 119, 6, 0.9)';
                    cmpBorderColor = theme.isDark ? '#d97706' : '#b45309';
                    cmpTextClass = 'text-amber-400';
                    cmpTextLightClass = 'text-amber-300';
                }}

                const desc = document.getElementById('hist-current-filter-desc');
                if (desc) desc.innerText = `對比: ${{curTitle}} vs ${{cmpTitle}} (${{compTag}})`;

                // Bins calculation
                const compBins = binsDef.map(b => {{
                    const cList = curActs.filter(a => a.distance_km >= b.min && a.distance_km < b.max);
                    const pList = cmpActs.filter(a => a.distance_km >= b.min && a.distance_km < b.max);
                    const cKm = cList.reduce((s, a) => s + a.distance_km, 0);
                    const pKm = pList.reduce((s, a) => s + a.distance_km, 0);
                    return {{
                        ...b,
                        curCount: cList.length,
                        cmpCount: pList.length,
                        curKm: cKm,
                        cmpKm: pKm,
                        diffCount: cList.length - pList.length,
                        diffKm: +(cKm - pKm).toFixed(1)
                    }};
                }});

                // Summary Statistics
                const curTotalRuns = curActs.length;
                const cmpTotalRuns = cmpActs.length;
                const curTotalKm = curActs.reduce((s, a) => s + a.distance_km, 0);
                const cmpTotalKm = cmpActs.reduce((s, a) => s + a.distance_km, 0);

                const curIndoorRuns = curActs.filter(a => a.isIndoor).length;
                const cmpIndoorRuns = cmpActs.filter(a => a.isIndoor).length;
                const curIndoorKm = curActs.filter(a => a.isIndoor).reduce((s, a) => s + a.distance_km, 0);
                const cmpIndoorKm = cmpActs.filter(a => a.isIndoor).reduce((s, a) => s + a.distance_km, 0);

                const curOutdoorRuns = curActs.filter(a => !a.isIndoor).length;
                const cmpOutdoorRuns = cmpActs.filter(a => !a.isIndoor).length;
                const curOutdoorKm = curActs.filter(a => !a.isIndoor).reduce((s, a) => s + a.distance_km, 0);
                const cmpOutdoorKm = cmpActs.filter(a => !a.isIndoor).reduce((s, a) => s + a.distance_km, 0);

                const curTrailRuns = curActs.filter(a => a.isTrail).length;
                const cmpTrailRuns = cmpActs.filter(a => a.isTrail).length;
                const curTrailKm = curActs.filter(a => a.isTrail).reduce((s, a) => s + a.distance_km, 0);
                const cmpTrailKm = cmpActs.filter(a => a.isTrail).reduce((s, a) => s + a.distance_km, 0);

                const runsDiff = curTotalRuns - cmpTotalRuns;
                const runsPct = cmpTotalRuns > 0 ? (((curTotalRuns - cmpTotalRuns) / cmpTotalRuns) * 100).toFixed(1) : null;
                const kmDiff = +(curTotalKm - cmpTotalKm).toFixed(1);
                const kmPct = cmpTotalKm > 0 ? (((curTotalKm - cmpTotalKm) / cmpTotalKm) * 100).toFixed(1) : null;

                const curMaxDist = curActs.length > 0 ? Math.max(...curActs.map(a => a.distance_km)) : 0;
                const cmpMaxDist = cmpActs.length > 0 ? Math.max(...cmpActs.map(a => a.distance_km)) : 0;

                let curModalBin = null, curMaxCount = -1;
                let cmpModalBin = null, cmpMaxCount = -1;
                compBins.forEach(b => {{
                    if (b.curCount > curMaxCount) {{ curMaxCount = b.curCount; curModalBin = b; }}
                    if (b.cmpCount > cmpMaxCount) {{ cmpMaxCount = b.cmpCount; cmpModalBin = b; }}
                }});

                // Update Badges
                const elTotal = document.getElementById('hist-stat-total');
                const elTotalKm = document.getElementById('hist-stat-total-km');
                const elIndoor = document.getElementById('hist-stat-indoor');
                const elIndoorDet = document.getElementById('hist-stat-indoor-detail');
                const elOutdoor = document.getElementById('hist-stat-outdoor');
                const elOutdoorDet = document.getElementById('hist-stat-outdoor-detail');
                const elTrail = document.getElementById('hist-stat-trail');
                const elTrailDet = document.getElementById('hist-stat-trail-detail');
                const elModal = document.getElementById('hist-stat-modal');
                const elModalCount = document.getElementById('hist-stat-modal-count');
                const elMaxDist = document.getElementById('hist-stat-max-dist');
                const elAvgDist = document.getElementById('hist-stat-avg-dist');

                if (elTotal) elTotal.innerHTML = `${{curTotalRuns}} <span class="text-xs font-normal text-slate-400">vs ${{cmpTotalRuns}} 次</span>`;
                if (elTotalKm) elTotalKm.innerHTML = `<span class="${{runsDiff >= 0 ? 'text-emerald-400' : 'text-rose-400'}} font-bold font-mono">${{runsDiff >= 0 ? '+' : ''}}${{runsDiff}} 次 (${{runsPct !== null ? (runsPct >= 0 ? '+' : '') + runsPct + '%' : '-'}})</span>`;
                if (elIndoor) elIndoor.innerHTML = `<span class="text-sky-400 font-bold">${{curTotalKm.toFixed(1)}}k</span> <span class="text-xs font-normal text-slate-400">vs ${{cmpTotalKm.toFixed(1)}}k</span>`;
                if (elIndoorDet) elIndoorDet.innerHTML = `<span class="${{kmDiff >= 0 ? 'text-emerald-400' : 'text-rose-400'}} font-mono">${{kmDiff >= 0 ? '+' : ''}}${{kmDiff}} km (${{kmPct !== null ? (kmPct >= 0 ? '+' : '') + kmPct + '%' : '-'}})</span>`;
                if (elOutdoor) elOutdoor.innerHTML = `室內: ${{curIndoorRuns}} vs ${{cmpIndoorRuns}} | 室外: ${{curOutdoorRuns}} vs ${{cmpOutdoorRuns}}`;
                if (elOutdoorDet) elOutdoorDet.innerHTML = `室內跑量: ${{curIndoorKm.toFixed(0)}}k vs ${{cmpIndoorKm.toFixed(0)}}k`;
                if (elTrail) elTrail.innerHTML = `越野: ${{curTrailRuns}} vs ${{cmpTrailRuns}} 次`;
                if (elTrailDet) elTrailDet.innerHTML = `越野跑量: ${{curTrailKm.toFixed(1)}} vs ${{cmpTrailKm.toFixed(1)}} km`;
                if (elModal) elModal.innerText = `${{curModalBin ? curModalBin.label : '-'}} vs ${{cmpModalBin ? cmpModalBin.label : '-'}}`;
                if (elModalCount) elModalCount.innerText = `眾數場次: ${{curMaxCount > 0 ? curMaxCount : 0}} vs ${{cmpMaxCount > 0 ? cmpMaxCount : 0}} 次`;
                if (elMaxDist) elMaxDist.innerText = `${{curMaxDist.toFixed(1)}}k vs ${{cmpMaxDist.toFixed(1)}}k`;
                if (elAvgDist) elAvgDist.innerText = `均量: ${{(curTotalKm / (curTotalRuns || 1)).toFixed(1)}}k vs ${{(cmpTotalKm / (cmpTotalRuns || 1)).toFixed(1)}}k`;

                // Update Table in Comparative Mode
                const tableContainer = document.getElementById('hist-table-container');
                if (tableContainer) {{
                    tableContainer.innerHTML = `
                        <table class="w-full text-left text-xs text-slate-300">
                            <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
                                <tr>
                                    <th class="py-2 px-3">距離區間 (Bucket)</th>
                                    <th class="py-2 px-3 text-sky-400">當期次數 (${{curTitle}})</th>
                                    <th class="py-2 px-3 ${{cmpTextClass}}">對比期次數 (${{cmpTitle}})</th>
                                    <th class="py-2 px-3 text-white font-bold">次數差額 (Delta)</th>
                                    <th class="py-2 px-3 text-sky-300">當期里程 (km)</th>
                                    <th class="py-2 px-3 ${{cmpTextLightClass}}">對比期里程 (km)</th>
                                    <th class="py-2 px-3 text-slate-400">里程差額 (km)</th>
                                </tr>
                            </thead>
                            <tbody id="hist-table-body" class="divide-y divide-slate-800">
                                ${{compBins.map(b => {{
                                    const diffCountColor = b.diffCount > 0 ? 'text-emerald-400 font-bold' : (b.diffCount < 0 ? 'text-rose-400 font-bold' : 'text-slate-400');
                                    const diffKmColor = b.diffKm > 0 ? 'text-emerald-400 font-bold' : (b.diffKm < 0 ? 'text-rose-400 font-bold' : 'text-slate-400');
                                    return `
                                        <tr class="hover:bg-slate-800/50 transition-colors">
                                            <td class="py-2 px-3 font-medium">${{b.label}} ${{b.sublabel ? `<span class="text-[11px] text-slate-400">(${{b.sublabel}})</span>` : ''}}</td>
                                            <td class="py-2 px-3 text-sky-400 font-mono font-bold">${{b.curCount}} 次</td>
                                            <td class="py-2 px-3 ${{cmpTextClass}} font-mono">${{b.cmpCount}} 次</td>
                                            <td class="py-2 px-3 font-mono ${{diffCountColor}}">${{b.diffCount > 0 ? '+' : ''}}${{b.diffCount}} 次</td>
                                            <td class="py-2 px-3 text-sky-300 font-mono">${{b.curKm.toFixed(1)}} km</td>
                                            <td class="py-2 px-3 ${{cmpTextLightClass}} font-mono">${{b.cmpKm.toFixed(1)}} km</td>
                                            <td class="py-2 px-3 font-mono ${{diffKmColor}}">${{b.diffKm > 0 ? '+' : ''}}${{b.diffKm}} km</td>
                                        </tr>
                                    `;
                                }}).join('')}}
                            </tbody>
                        </table>
                    `;
                }}

                // Render Comparative Chart
                destroyChart('distanceHistogram');
                const labels = compBins.map(b => b.sublabel ? `${{b.label}} (${{b.sublabel}})` : b.label);
                const isStacked = histGroupMode === 'stacked';

                const ctx = canvas.getContext('2d');
                charts['distanceHistogram'] = new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [
                            {{
                                label: curTitle,
                                data: compBins.map(b => b.curCount),
                                backgroundColor: theme.isDark ? 'rgba(56, 189, 248, 0.85)' : 'rgba(2, 132, 199, 0.9)',
                                borderColor: theme.isDark ? '#0284c7' : '#0369a1',
                                borderWidth: 1,
                                borderRadius: isStacked ? 0 : 4,
                                stack: isStacked ? 'combined' : undefined
                            }},
                            {{
                                label: cmpTitle,
                                data: compBins.map(b => b.cmpCount),
                                backgroundColor: cmpColor,
                                borderColor: cmpBorderColor,
                                borderWidth: 1,
                                borderRadius: 4,
                                stack: isStacked ? 'combined' : undefined
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        scales: {{
                            x: {{
                                stacked: isStacked,
                                grid: {{ color: theme.gridColor }},
                                border: {{ color: theme.axisBorderColor }},
                                ticks: {{
                                    color: theme.tickColor,
                                    maxRotation: 45,
                                    minRotation: 0,
                                    font: {{ size: 11, weight: theme.isDark ? 'normal' : 'bold' }}
                                }},
                                title: {{
                                    display: true,
                                    text: '單次跑步里程區間 (Distance Buckets, km)',
                                    color: theme.titleColor,
                                    font: {{ size: 12, weight: 'bold' }}
                                }}
                            }},
                            y: {{
                                stacked: isStacked,
                                beginAtZero: true,
                                grace: '8%',
                                grid: {{ color: theme.gridColor }},
                                border: {{ color: theme.axisBorderColor }},
                                ticks: {{
                                    color: theme.tickColor,
                                    stepSize: 1,
                                    font: {{ size: 11, weight: theme.isDark ? 'normal' : 'bold' }}
                                }},
                                title: {{
                                    display: true,
                                    text: '累積次數 (Sessions / Frequency)',
                                    color: theme.titleColor,
                                    font: {{ size: 12, weight: 'bold' }}
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                position: 'top',
                                labels: {{
                                    color: theme.legendColor,
                                    boxWidth: 14,
                                    font: {{ size: 12, weight: 'bold' }}
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    afterTitle: function(context) {{
                                        const idx = context[0].dataIndex;
                                        const b = compBins[idx];
                                        return `當期: ${{b.curKm.toFixed(1)}} km | 對比期: ${{b.cmpKm.toFixed(1)}} km (差額: ${{b.diffKm > 0 ? '+' : ''}}${{b.diffKm}} km)`;
                                    }},
                                    footer: function(tooltipItems) {{
                                        const idx = tooltipItems[0].dataIndex;
                                        const b = compBins[idx];
                                        const deltaStr = b.diffCount >= 0 ? `+${{b.diffCount}}` : `${{b.diffCount}}`;
                                        return `增減變化: ${{deltaStr}} 次 (${{b.curCount}} vs ${{b.cmpCount}})`;
                                    }}
                                }}
                            }}
                        }}
                    }},
                    plugins: [getHistogramDataLabelsPlugin(isStacked, theme)]
                }});
                return;
            }}

            // Standard Mode (All / Year / Month / Trailing)
            const activities = getFilteredActivities();

            // Structure per bin
            const binStats = binsDef.map(b => ({{
                ...b,
                indoorCount: 0,
                outdoorCount: 0,
                trailCount: 0,
                indoorKm: 0,
                outdoorKm: 0,
                trailKm: 0,
                totalCount: 0,
                totalKm: 0
            }}));

            let totalRuns = 0;
            let totalKm = 0;
            let indoorRuns = 0;
            let indoorKm = 0;
            let outdoorRuns = 0;
            let outdoorKm = 0;
            let trailRuns = 0;
            let trailKm = 0;
            let maxDist = 0;

            activities.forEach(act => {{
                const km = act.distance_km;
                totalRuns++;
                totalKm += km;
                if (km > maxDist) maxDist = km;

                if (act.isIndoor) {{
                    indoorRuns++;
                    indoorKm += km;
                }} else {{
                    outdoorRuns++;
                    outdoorKm += km;
                    if (act.isTrail) {{
                        trailRuns++;
                        trailKm += km;
                    }}
                }}

                // Locate bin
                for (let i = 0; i < binStats.length; i++) {{
                    const b = binStats[i];
                    if (km >= b.min && km < b.max) {{
                        b.totalCount++;
                        b.totalKm += km;
                        if (act.isIndoor) {{
                            b.indoorCount++;
                            b.indoorKm += km;
                        }} else {{
                            b.outdoorCount++;
                            b.outdoorKm += km;
                            if (act.isTrail) {{
                                b.trailCount++;
                                b.trailKm += km;
                            }}
                        }}
                        break;
                    }}
                }}
            }});

            // Modal bin calculation (most frequent bucket)
            let modalBin = null;
            let maxBinCount = -1;
            binStats.forEach(b => {{
                if (b.totalCount > maxBinCount) {{
                    maxBinCount = b.totalCount;
                    modalBin = b;
                }}
            }});

            // Update Badges
            const elTotal = document.getElementById('hist-stat-total');
            const elTotalKm = document.getElementById('hist-stat-total-km');
            const elIndoor = document.getElementById('hist-stat-indoor');
            const elIndoorDet = document.getElementById('hist-stat-indoor-detail');
            const elOutdoor = document.getElementById('hist-stat-outdoor');
            const elOutdoorDet = document.getElementById('hist-stat-outdoor-detail');
            const elTrail = document.getElementById('hist-stat-trail');
            const elTrailDet = document.getElementById('hist-stat-trail-detail');
            const elModal = document.getElementById('hist-stat-modal');
            const elModalCount = document.getElementById('hist-stat-modal-count');
            const elMaxDist = document.getElementById('hist-stat-max-dist');
            const elAvgDist = document.getElementById('hist-stat-avg-dist');

            const indoorPct = totalRuns > 0 ? ((indoorRuns / totalRuns) * 100).toFixed(1) : '0.0';
            const outdoorPct = totalRuns > 0 ? ((outdoorRuns / totalRuns) * 100).toFixed(1) : '0.0';
            const avgDist = totalRuns > 0 ? (totalKm / totalRuns).toFixed(2) : '0.00';

            if (elTotal) elTotal.innerText = `${{totalRuns}} 次`;
            if (elTotalKm) elTotalKm.innerText = `共 ${{totalKm.toFixed(1)}} km`;
            if (elIndoor) elIndoor.innerText = `${{indoorRuns}} 次`;
            if (elIndoorDet) elIndoorDet.innerText = `${{indoorKm.toFixed(1)}} km (${{indoorPct}}%)`;
            if (elOutdoor) elOutdoor.innerText = `${{outdoorRuns}} 次`;
            if (elOutdoorDet) elOutdoorDet.innerText = `${{outdoorKm.toFixed(1)}} km (${{outdoorPct}}%)`;
            if (elTrail) elTrail.innerText = `${{trailRuns}} 次`;
            if (elTrailDet) elTrailDet.innerText = `${{trailKm.toFixed(1)}} km`;
            if (elModal) elModal.innerText = modalBin && maxBinCount > 0 ? modalBin.label : '無資料';
            if (elModalCount) elModalCount.innerText = maxBinCount > 0 ? `${{maxBinCount}} 次 (${{((maxBinCount / totalRuns) * 100).toFixed(1)}}%)` : '--';
            if (elMaxDist) elMaxDist.innerText = `${{maxDist.toFixed(2)}} km`;
            if (elAvgDist) elAvgDist.innerText = `單次均量: ${{avgDist}} km`;

            // Restore Standard Table Structure
            const tableContainer = document.getElementById('hist-table-container');
            if (tableContainer) {{
                tableContainer.innerHTML = `
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="text-xs uppercase bg-slate-800/90 text-slate-400 border-b border-slate-700">
                            <tr>
                                <th class="py-2 px-3">距離區間 (Bucket)</th>
                                <th class="py-2 px-3 text-amber-400">室內次數 (Indoor)</th>
                                <th class="py-2 px-3 text-sky-400">室外次數 (Outdoor)</th>
                                <th class="py-2 px-3 text-emerald-400">越野次數 (Trail)</th>
                                <th class="py-2 px-3 text-white font-bold">合計次數</th>
                                <th class="py-2 px-3 text-slate-400">佔比 (%)</th>
                                <th class="py-2 px-3 text-slate-400">累積里程 (km)</th>
                            </tr>
                        </thead>
                        <tbody id="hist-table-body" class="divide-y divide-slate-800">
                            ${{binStats.map(b => {{
                                const pct = totalRuns > 0 ? ((b.totalCount / totalRuns) * 100).toFixed(1) : '0.0';
                                const highlightClass = b === modalBin && b.totalCount > 0 ? 'bg-sky-500/10 font-bold text-sky-300' : '';
                                return `
                                    <tr class="${{highlightClass}} hover:bg-slate-800/50 transition-colors">
                                        <td class="py-2 px-3 font-medium">${{b.label}} ${{b.sublabel ? `<span class="text-[11px] text-slate-400">(${{b.sublabel}})</span>` : ''}}</td>
                                        <td class="py-2 px-3 text-amber-400 font-mono">${{b.indoorCount}} 次 <span class="text-[10px] text-slate-400">(${{b.indoorKm.toFixed(1)}} km)</span></td>
                                        <td class="py-2 px-3 text-sky-400 font-mono">${{b.outdoorCount}} 次 <span class="text-[10px] text-slate-400">(${{b.outdoorKm.toFixed(1)}} km)</span></td>
                                        <td class="py-2 px-3 text-emerald-400 font-mono">${{b.trailCount}} 次 <span class="text-[10px] text-slate-400">(${{b.trailKm.toFixed(1)}} km)</span></td>
                                        <td class="py-2 px-3 text-white font-bold font-mono">${{b.totalCount}} 次</td>
                                        <td class="py-2 px-3 text-slate-300 font-mono">${{pct}}%</td>
                                        <td class="py-2 px-3 text-slate-400 font-mono">${{b.totalKm.toFixed(1)}} km</td>
                                    </tr>
                                `;
                            }}).join('')}}
                        </tbody>
                    </table>
                `;
            }}

            // Chart Configuration
            destroyChart('distanceHistogram');
            const labels = binStats.map(b => b.sublabel ? `${{b.label}} (${{b.sublabel}})` : b.label);

            let datasets = [];
            const isStacked = histGroupMode === 'stacked' || histGroupMode === 'split_trail';

            if (histGroupMode === 'split_trail') {{
                // 3-way split: Indoor, Outdoor Road/Track, Trail
                datasets = [
                    {{
                        label: '室內跑步機 (Indoor)',
                        data: binStats.map(b => b.indoorCount),
                        backgroundColor: theme.isDark ? 'rgba(245, 158, 11, 0.85)' : 'rgba(217, 119, 6, 0.9)',
                        borderColor: theme.isDark ? '#d97706' : '#b45309',
                        borderWidth: 1,
                        borderRadius: isStacked ? 0 : 4,
                        stack: 'combined'
                    }},
                    {{
                        label: '室外路跑/操場 (Road/Track)',
                        data: binStats.map(b => Math.max(0, b.outdoorCount - b.trailCount)),
                        backgroundColor: theme.isDark ? 'rgba(14, 165, 233, 0.85)' : 'rgba(2, 132, 199, 0.9)',
                        borderColor: theme.isDark ? '#0284c7' : '#0369a1',
                        borderWidth: 1,
                        borderRadius: isStacked ? 0 : 4,
                        stack: 'combined'
                    }},
                    {{
                        label: '越野山徑/登山 (Trail)',
                        data: binStats.map(b => b.trailCount),
                        backgroundColor: theme.isDark ? 'rgba(16, 185, 129, 0.85)' : 'rgba(5, 150, 105, 0.9)',
                        borderColor: theme.isDark ? '#059669' : '#047857',
                        borderWidth: 1,
                        borderRadius: isStacked ? 4 : 4,
                        stack: 'combined'
                    }}
                ];
            }} else {{
                // 2-way: Indoor vs Outdoor
                datasets = [
                    {{
                        label: '室內運動 (Indoor)',
                        data: binStats.map(b => b.indoorCount),
                        backgroundColor: theme.isDark ? 'rgba(245, 158, 11, 0.85)' : 'rgba(217, 119, 6, 0.9)',
                        borderColor: theme.isDark ? '#d97706' : '#b45309',
                        borderWidth: 1,
                        borderRadius: isStacked ? 0 : 4,
                        stack: isStacked ? 'combined' : undefined
                    }},
                    {{
                        label: '室外運動 (Outdoor)',
                        data: binStats.map(b => b.outdoorCount),
                        backgroundColor: theme.isDark ? 'rgba(14, 165, 233, 0.85)' : 'rgba(2, 132, 199, 0.9)',
                        borderColor: theme.isDark ? '#0284c7' : '#0369a1',
                        borderWidth: 1,
                        borderRadius: 4,
                        stack: isStacked ? 'combined' : undefined
                    }}
                ];
            }}

            const ctx = canvas.getContext('2d');
            charts['distanceHistogram'] = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: datasets
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ mode: 'index', intersect: false }},
                    scales: {{
                        x: {{
                            stacked: isStacked,
                            grid: {{ color: theme.gridColor }},
                            border: {{ color: theme.axisBorderColor }},
                            ticks: {{
                                color: theme.tickColor,
                                maxRotation: 45,
                                minRotation: 0,
                                font: {{ size: 11, weight: theme.isDark ? 'normal' : 'bold' }}
                            }},
                            title: {{
                                display: true,
                                text: '單次跑步里程區間 (Distance Buckets, km)',
                                color: theme.titleColor,
                                font: {{ size: 12, weight: 'bold' }}
                            }}
                        }},
                        y: {{
                            stacked: isStacked,
                            beginAtZero: true,
                            grace: '8%',
                            grid: {{ color: theme.gridColor }},
                            border: {{ color: theme.axisBorderColor }},
                            ticks: {{
                                color: theme.tickColor,
                                stepSize: 1,
                                font: {{ size: 11, weight: theme.isDark ? 'normal' : 'bold' }}
                            }},
                            title: {{
                                display: true,
                                text: '累積次數 (Sessions / Frequency)',
                                color: theme.titleColor,
                                font: {{ size: 12, weight: 'bold' }}
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                color: theme.legendColor,
                                boxWidth: 14,
                                font: {{ size: 12, weight: 'bold' }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                afterTitle: function(context) {{
                                    const idx = context[0].dataIndex;
                                    const b = binStats[idx];
                                    return `區間里程累計: ${{b.totalKm.toFixed(1)}} km`;
                                }},
                                footer: function(tooltipItems) {{
                                    let sum = 0;
                                    tooltipItems.forEach(ti => {{
                                        sum += ti.parsed.y || 0;
                                    }});
                                    const pct = totalRuns > 0 ? ((sum / totalRuns) * 100).toFixed(1) : 0;
                                    return `合計場次: ${{sum}} 次 (佔總量 ${{pct}}%)`;
                                }}
                            }}
                        }}
                    }}
                }},
                plugins: [getHistogramDataLabelsPlugin(isStacked, theme)]
            }});
        }}

        // Monthly Comparison Table (Always Rendered cleanly)
        function renderMonthlyTable() {{
            const tableBody = document.getElementById('monthly-table-body');
            if (!tableBody) return;

            const monthlyData = getComputedMonthlyData();
            const reversedMonthly = [...monthlyData].reverse();

            tableBody.innerHTML = reversedMonthly.map(m => {{
                const momStr = m.mom_km_growth_pct !== null 
                    ? (m.mom_km_growth_pct >= 0 ? `<span class="text-emerald-500 font-mono font-semibold">+${{m.mom_km_growth_pct}}%</span>` : `<span class="text-rose-500 font-mono font-semibold">${{m.mom_km_growth_pct}}%</span>`)
                    : '<span class="text-slate-500 font-mono">-</span>';

                const yoyStr = m.yoy_km_growth_pct !== null 
                    ? (m.yoy_km_growth_pct >= 0 ? `<span class="text-purple-400 font-mono font-semibold">+${{m.yoy_km_growth_pct}}%</span>` : `<span class="text-amber-500 font-mono font-semibold">${{m.yoy_km_growth_pct}}%</span>`)
                    : '<span class="text-slate-500 font-mono">-</span>';

                const lastYearKmStr = m.last_year_run_km !== null
                    ? `<span class="font-mono text-slate-300">${{m.last_year_run_km}} km</span>`
                    : '<span class="text-slate-500 font-mono">-</span>';

                // Sleep cell rendering with comparison
                let sleepCell = '-';
                if (m.avg_sleep_hours) {{
                    const sleepPctStr = (m.deep_pct && m.rem_pct) ? `<span class="text-xs text-slate-400"> (深層${{m.deep_pct}}% / REM${{m.rem_pct}}%)</span>` : '';
                    if (isOutlierTrimEnabled && m.raw.avg_sleep_hours && m.raw.avg_sleep_hours !== m.avg_sleep_hours) {{
                        const diff = +(m.avg_sleep_hours - m.raw.avg_sleep_hours).toFixed(2);
                        const diffColor = diff > 0 ? 'text-emerald-500 bg-emerald-500/10 border-emerald-500/40' : 'text-rose-500 bg-rose-500/10 border-rose-500/40';
                        const diffStr = diff > 0 ? `+${{diff}}h` : `${{diff}}h`;
                        sleepCell = `
                            <div>
                                <span class="font-bold text-indigo-400">${{m.avg_sleep_hours}}h</span>
                                <span class="text-[10px] px-1.5 py-0.5 rounded border ${{diffColor}} font-mono ml-1 font-semibold" title="原始全量: ${{m.raw.avg_sleep_hours}}h">${{diffStr}}</span>
                                ${{sleepPctStr}}
                            </div>
                        `;
                    }} else {{
                        sleepCell = `<span class="text-indigo-400 font-medium">${{m.avg_sleep_hours}}h</span> ${{sleepPctStr}}`;
                    }}
                }}

                // RHR cell rendering with comparison
                let rhrCell = '-';
                if (m.avg_rhr) {{
                    if (isOutlierTrimEnabled && m.raw.avg_rhr && m.raw.avg_rhr !== m.avg_rhr) {{
                        const rhrDiff = +(m.avg_rhr - m.raw.avg_rhr).toFixed(1);
                        const diffColor = rhrDiff < 0 ? 'text-emerald-500 bg-emerald-500/10 border-emerald-500/40' : 'text-rose-500 bg-rose-500/10 border-rose-500/40';
                        const diffStr = rhrDiff > 0 ? `+${{rhrDiff}}` : `${{rhrDiff}}`;
                        rhrCell = `
                            <span class="font-bold text-rose-400">${{m.avg_rhr}} bpm</span> 
                            <span class="text-[10px] px-1.5 py-0.5 rounded border ${{diffColor}} font-mono ml-1 font-semibold" title="原始全量: ${{m.raw.avg_rhr}} bpm">${{diffStr}}</span>
                        `;
                    }} else {{
                        rhrCell = `<span class="text-rose-400">${{m.avg_rhr}} bpm</span>`;
                    }}
                }}

                // HRV cell rendering with comparison
                let hrvCell = '-';
                if (m.avg_hrv) {{
                    if (isOutlierTrimEnabled && m.raw.avg_hrv && m.raw.avg_hrv !== m.avg_hrv) {{
                        const hrvDiff = +(m.avg_hrv - m.raw.avg_hrv).toFixed(1);
                        const diffColor = hrvDiff > 0 ? 'text-emerald-500 bg-emerald-500/10 border-emerald-500/40' : 'text-rose-500 bg-rose-500/10 border-rose-500/40';
                        const diffStr = hrvDiff > 0 ? `+${{hrvDiff}}` : `${{hrvDiff}}`;
                        hrvCell = `
                            <span class="font-bold text-emerald-400">${{m.avg_hrv}} ms</span> 
                            <span class="text-[10px] px-1.5 py-0.5 rounded border ${{diffColor}} font-mono ml-1 font-semibold" title="原始全量: ${{m.raw.avg_hrv}} ms">${{diffStr}}</span>
                        `;
                    }} else {{
                        hrvCell = `<span class="text-emerald-400">${{m.avg_hrv}} ms</span>`;
                    }}
                }}

                return `
                    <tr class="hover:bg-slate-800/60 transition-colors">
                        <td class="py-3 px-3 font-bold">${{m.month_label}}</td>
                        <td class="py-3 px-3 font-bold text-sky-500">${{m.total_run_km}} km</td>
                        <td class="py-3 px-3">${{momStr}}</td>
                        <td class="py-3 px-3">${{yoyStr}}</td>
                        <td class="py-3 px-3">${{lastYearKmStr}}</td>
                        <td class="py-3 px-3 font-semibold text-orange-500">${{m.runs_10k_plus}} 次</td>
                        <td class="py-3 px-3 text-emerald-500 font-medium">全馬 ${{m.full_marathons}} &bull; 半馬 ${{m.half_marathons}}</td>
                        <td class="py-3 px-3 text-slate-400 font-mono">${{m.longest_run_km > 0 ? m.longest_run_km + ' km' : '-'}}</td>
                        <td class="py-3 px-3 text-rose-500 font-semibold">${{m.total_calories.toLocaleString()}} kcal</td>
                        <td class="py-3 px-3">${{rhrCell}}</td>
                        <td class="py-3 px-3">${{hrvCell}}</td>
                        <td class="py-3 px-3">${{sleepCell}}</td>
                        <td class="py-3 px-3 text-slate-400">${{m.avg_steps ? m.avg_steps.toLocaleString() : '-'}}</td>
                    </tr>
                `;
            }}).join('');
        }}

        function renderDailyTable(filterKeyword = "") {{
            const records = getActiveRecords();
            const tableBody = document.getElementById('daily-records-table-body');
            const countElem = document.getElementById('daily-record-count');
            if (!tableBody) return;

            let filtered = records;
            if (filterKeyword) {{
                const kw = filterKeyword.toLowerCase().trim();
                filtered = records.filter(r => {{
                    const dateMatch = r.date && r.date.toLowerCase().includes(kw);
                    const actMatch = r.activities && r.activities.some(a => (a.name && a.name.toLowerCase().includes(kw)) || (a.type && a.type.toLowerCase().includes(kw)));
                    return dateMatch || actMatch;
                }});
            }}

            if (countElem) countElem.innerText = `顯示 ${{filtered.length}} / ${{records.length}} 筆`;

            if (filtered.length === 0) {{
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="11" class="py-6 text-center text-slate-500">
                            未找到符合「${{filterKeyword}}」條件的每日原始資料。
                        </td>
                    </tr>
                `;
                return;
            }}

            const reversed = [...filtered].reverse();

            tableBody.innerHTML = reversed.map(r => {{
                let actText = '-';
                if (r.activities && r.activities.length > 0) {{
                    actText = r.activities.map(a => {{
                        const distStr = a.distance_km > 0 ? `${{a.distance_km}}km` : '';
                        const paceStr = a.pace ? `(${{a.pace}})` : '';
                        return `${{a.name}} ${{distStr}} ${{paceStr}}`.trim();
                    }}).join(' | ');
                }}

                let sleepText = '-';
                if (r.sleep_duration_seconds) {{
                    const hrs = (r.sleep_duration_seconds / 3600).toFixed(1);
                    const score = r.sleep_score ? `${{r.sleep_score}}分` : '';
                    sleepText = `${{hrs}}h ${{score}}`.trim();
                }}

                const stepsVal = r.steps ? r.steps.toLocaleString() : '-';
                const goalVal = r.step_goal ? ` / ${{r.step_goal.toLocaleString()}}` : '';
                const stepColor = (r.steps && r.step_goal && r.steps >= r.step_goal) ? 'text-emerald-500 font-semibold' : 'text-slate-400';

                let bbText = '-';
                if (r.body_battery_charged !== null || r.body_battery_drained !== null) {{
                    bbText = `+${{r.body_battery_charged || 0}} / -${{r.body_battery_drained || 0}}`;
                }}

                const rhrVal = r.resting_hr ? `${{r.resting_hr}} bpm` : '-';
                const hrvVal = r.hrv_overnight_avg ? `${{r.hrv_overnight_avg}} ms` : '-';
                const stressVal = r.avg_stress !== null ? `${{r.avg_stress}}` : '-';
                const calsVal = r.active_calories ? `${{Math.round(r.active_calories)}} kcal` : '-';
                const spo2Resp = (r.spo2_avg || r.respiration_avg) ? `${{r.spo2_avg ? r.spo2_avg + '%' : '-'}} / ${{r.respiration_avg ? r.respiration_avg + 'brpm' : '-'}}` : '-';
                const vo2Val = r.vo2_max ? `${{r.vo2_max}}` : '-';

                return `
                    <tr class="hover:bg-slate-800/60 transition-colors">
                        <td class="py-2.5 px-3 font-mono text-sky-500 font-bold whitespace-nowrap">${{r.date}}</td>
                        <td class="py-2.5 px-3 ${{stepColor}} whitespace-nowrap">${{stepsVal}}${{goalVal}}</td>
                        <td class="py-2.5 px-3 text-emerald-500 font-medium max-w-xs truncate" title="${{actText}}">${{actText}}</td>
                        <td class="py-2.5 px-3 text-rose-500 whitespace-nowrap">${{rhrVal}}</td>
                        <td class="py-2.5 px-3 text-emerald-500 whitespace-nowrap">${{hrvVal}}</td>
                        <td class="py-2.5 px-3 text-indigo-400 whitespace-nowrap">${{sleepText}}</td>
                        <td class="py-2.5 px-3 text-amber-500 whitespace-nowrap">${{bbText}}</td>
                        <td class="py-2.5 px-3 text-slate-400 whitespace-nowrap">${{stressVal}}</td>
                        <td class="py-2.5 px-3 text-orange-500 whitespace-nowrap">${{calsVal}}</td>
                        <td class="py-2.5 px-3 text-slate-400 whitespace-nowrap">${{spo2Resp}}</td>
                        <td class="py-2.5 px-3 text-purple-500 font-semibold whitespace-nowrap">${{vo2Val}}</td>
                    </tr>
                `;
            }}).join('');
        }}

        function filterDailyRecords() {{
            const kw = document.getElementById('daily-search-input').value;
            renderDailyTable(kw);
        }}

        function openHelpModal() {{
            const modal = document.getElementById('help-modal');
            if (modal) modal.classList.remove('hidden');
        }}

        function closeHelpModal() {{
            const modal = document.getElementById('help-modal');
            if (modal) modal.classList.add('hidden');
        }}

        // Close help modal on backdrop click or ESC key
        window.addEventListener('click', (e) => {{
            const modal = document.getElementById('help-modal');
            if (modal && e.target === modal) {{
                modal.classList.add('hidden');
            }}
        }});

        window.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                closeHelpModal();
            }}
        }});

        // Initial Boot with theme support
        window.addEventListener('DOMContentLoaded', () => {{
            const savedTheme = localStorage.getItem('garmin_dashboard_theme') || 'dark';
            applyTheme(savedTheme);
            renderTodayAssessment();
            renderRecommendations();
            renderMonthlyTable();
            switchTab('monthly');
        }});
    </script>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
