"""
Script to build GitHub Pages:
1. index.html - Privacy-scrubbed Garmin Health & Endurance Dashboard (Just health numbers).
2. sport_english.html - Bilingual Sport English & 10 Golden Athletic Training Principles (Principles Project style).
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from insights_engine import InsightsEngine
from html_generator import generate_dashboard_html

def sanitize_and_build():
    history_file = Path("garmin_health_history.json")
    if not history_file.exists():
        print("[!] garmin_health_history.json not found!")
        return

    with open(history_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # 1. Privacy Protection: Anonymize user_name
    safe_user_name = "Garmin 運動員 (Athlete)"

    # 2. Privacy Protection: Scrub all records to strictly "Just health numbers"
    records_dict = raw_data.get("records", {})
    clean_records = []

    # Sort by date
    sorted_dates = sorted(records_dict.keys())
    for d_str in sorted_dates:
        r = records_dict[d_str]
        
        # Clean activities: strictly athletic metrics, no location/city names
        clean_activities = []
        for act in r.get("activities", []):
            act_type = (act.get("type") or "").lower()
            dist = act.get("distance_km") or 0.0
            
            # Map to generic sports category without any city / street / location leak
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

            clean_activities.append({
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

        # Retain ONLY pure health numbers
        clean_record = {
            "date": r.get("date", d_str),
            "resting_hr": r.get("resting_hr"),
            "min_hr": r.get("min_hr"),
            "max_hr": r.get("max_hr"),
            "avg_hr": r.get("avg_hr"),
            "sleep_score": r.get("sleep_score"),
            "sleep_qualifier": r.get("sleep_qualifier"),
            "sleep_duration_seconds": r.get("sleep_duration_seconds"),
            "deep_sleep_seconds": r.get("deep_sleep_seconds"),
            "light_sleep_seconds": r.get("light_sleep_seconds"),
            "rem_sleep_seconds": r.get("rem_sleep_seconds"),
            "awake_seconds": r.get("awake_seconds"),
            "sleep_start": r.get("sleep_start"),
            "sleep_end": r.get("sleep_end"),
            "hrv_status": r.get("hrv_status"),
            "hrv_overnight_avg": r.get("hrv_overnight_avg"),
            "hrv_weekly_avg": r.get("hrv_weekly_avg"),
            "hrv_baseline_low": r.get("hrv_baseline_low"),
            "hrv_baseline_high": r.get("hrv_baseline_high"),
            "hrv_feedback": r.get("hrv_feedback"),
            "body_battery_charged": r.get("body_battery_charged"),
            "body_battery_drained": r.get("body_battery_drained"),
            "body_battery_highest": r.get("body_battery_highest"),
            "body_battery_lowest": r.get("body_battery_lowest"),
            "body_battery_recent": r.get("body_battery_recent"),
            "avg_stress": r.get("avg_stress"),
            "max_stress": r.get("max_stress"),
            "stress_qualifier": r.get("stress_qualifier"),
            "steps": r.get("steps"),
            "step_goal": r.get("step_goal"),
            "distance_meters": r.get("distance_meters"),
            "active_calories": r.get("active_calories"),
            "total_calories": r.get("total_calories"),
            "moderate_intensity_minutes": r.get("moderate_intensity_minutes"),
            "vigorous_intensity_minutes": r.get("vigorous_intensity_minutes"),
            "floors_climbed": r.get("floors_climbed"),
            "spo2_avg": r.get("spo2_avg"),
            "respiration_avg": r.get("respiration_avg"),
            "vo2_max": r.get("vo2_max"),
            "training_readiness": r.get("training_readiness"),
            "activities": clean_activities,
        }
        clean_records.append(clean_record)

    print(f"[OK] Processed {len(clean_records)} clean, privacy-scrubbed records.")

    # 3. Generate index.html for GitHub Pages root
    index_path = Path("index.html")
    generate_dashboard_html(
        records=clean_records,
        user_name=safe_user_name,
        last_synced=raw_data.get("last_synced_at"),
        output_path=index_path,
    )
    print(f"[OK] index.html generated: {index_path.resolve()}")

    # Also update garmin_health_dashboard.html so both are synced and sanitized
    dashboard_path = Path("garmin_health_dashboard.html")
    generate_dashboard_html(
        records=clean_records,
        user_name=safe_user_name,
        last_synced=raw_data.get("last_synced_at"),
        output_path=dashboard_path,
    )
    print(f"[OK] garmin_health_dashboard.html generated: {dashboard_path.resolve()}")

if __name__ == "__main__":
    sanitize_and_build()
