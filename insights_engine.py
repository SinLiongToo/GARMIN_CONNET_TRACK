"""Garmin Health & Running Endurance Trends Analytics Engine."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import statistics


@dataclass
class RecommendationItem:
    category: str  # "睡眠與恢復", "自律神經與壓力", "心肺與活力", "活動與運動", "長跑與馬拉松"
    level: str     # "critical" (🔴 需改善), "warning" (🟡 注意), "good" (🟢 良好)
    title: str
    description: str
    action: str


@dataclass
class RunningEnduranceStats:
    total_runs: int = 0
    total_run_km: float = 0.0
    weekly_run_km: float = 0.0
    longest_run_km: float = 0.0
    longest_run_date: Optional[str] = None
    longest_run_name: Optional[str] = None
    
    # 10K+ Long Run metrics
    runs_10k_plus_count: int = 0
    days_per_10k_run: Optional[float] = None
    days_since_last_10k: Optional[int] = None
    last_10k_date: Optional[str] = None
    last_10k_km: Optional[float] = None
    last_10k_name: Optional[str] = None

    # Distance Breakdown
    full_marathon_count: int = 0  # >= 42 km
    half_marathon_count: int = 0  # 21 km ~ 41.99 km
    mid_distance_count: int = 0   # 10 km ~ 20.99 km
    short_run_count: int = 0      # < 10 km

    # Calories
    total_run_calories: int = 0
    avg_calories_per_km: Optional[float] = None
    max_workout_calories: int = 0


@dataclass
class MonthlyStats:
    month: str  # "2026-08"
    month_label: str  # "2026年 08月"
    days_count: int = 0
    total_run_km: float = 0.0
    total_runs: int = 0
    runs_10k_plus: int = 0
    full_marathons: int = 0
    half_marathons: int = 0
    total_calories: int = 0
    avg_rhr: Optional[float] = None
    avg_hrv: Optional[float] = None
    
    # Monthly Sleep Breakdown (Stacked Stages)
    avg_sleep_hours: Optional[float] = None
    avg_deep_hours: Optional[float] = None
    avg_rem_hours: Optional[float] = None
    avg_light_hours: Optional[float] = None
    avg_awake_hours: Optional[float] = None
    deep_pct: Optional[float] = None
    rem_pct: Optional[float] = None
    avg_sleep_score: Optional[float] = None
    
    avg_steps: Optional[int] = None
    avg_stress: Optional[float] = None
    longest_run_km: float = 0.0
    mom_km_growth_pct: Optional[float] = None
    yoy_km_growth_pct: Optional[float] = None
    last_year_run_km: Optional[float] = None
    mom_runs_growth_pct: Optional[float] = None
    yoy_runs_growth_pct: Optional[float] = None


def format_duration(minutes: float) -> str:
    """Format minutes to Hh MMm SSs."""
    h = int(minutes // 60)
    mins = int(minutes % 60)
    s = int(round((minutes * 60) % 60))
    if s == 60:
        mins += 1
        s = 0
    if mins == 60:
        h += 1
        mins = 0
    return f"{h}h {mins:02d}m {s:02d}s"


def format_pace(minutes: float, km: float) -> str:
    """Format pace to min:sec/km."""
    if not km or km <= 0:
        return "-"
    pace = minutes / km
    pm = int(pace)
    ps = int(round((pace - pm) * 60))
    if ps == 60:
        pm += 1
        ps = 0
    return f"{pm}:{ps:02d}/km"


@dataclass
class AnnualMarathonStats:
    year: str  # "2024", "2025", "2026", "all"
    year_label: str  # "2024 年", "全部歷史累計 (All-Time)"
    
    # Standard Half Marathon (室外 21.0 <= km < 25.0)
    std_half_count: int = 0
    std_half_avg_minutes: Optional[float] = None
    std_half_avg_time_str: str = "-"
    std_half_avg_pace_str: str = "-"
    std_half_avg_km: Optional[float] = None
    std_half_fastest_time_str: str = "-"
    std_half_fastest_date: Optional[str] = None
    std_half_fastest_pace_str: str = "-"
    std_half_fastest_km: Optional[float] = None
    
    # Extended Half Marathon / LSD (室外 21.0 <= km < 42.0)
    ext_half_count: int = 0
    ext_half_avg_minutes: Optional[float] = None
    ext_half_avg_time_str: str = "-"
    ext_half_avg_pace_str: str = "-"
    ext_half_avg_km: Optional[float] = None
    ext_half_fastest_time_str: str = "-"
    ext_half_fastest_date: Optional[str] = None
    ext_half_fastest_pace_str: str = "-"
    ext_half_fastest_km: Optional[float] = None
    
    # Standard Full Marathon (室外 42.0 <= km < 45.0)
    std_full_count: int = 0
    std_full_avg_minutes: Optional[float] = None
    std_full_avg_time_str: str = "-"
    std_full_avg_pace_str: str = "-"
    std_full_avg_km: Optional[float] = None
    std_full_fastest_time_str: str = "-"
    std_full_fastest_date: Optional[str] = None
    std_full_fastest_pace_str: str = "-"
    std_full_fastest_km: Optional[float] = None

    # Extended Full Marathon / Ultra (室外 km >= 42.0)
    ext_full_count: int = 0
    ext_full_avg_minutes: Optional[float] = None
    ext_full_avg_time_str: str = "-"
    ext_full_avg_pace_str: str = "-"
    ext_full_avg_km: Optional[float] = None
    ext_full_fastest_time_str: str = "-"
    ext_full_fastest_date: Optional[str] = None
    ext_full_fastest_pace_str: str = "-"
    ext_full_fastest_km: Optional[float] = None


@dataclass
class WindowSummary:
    window_name: str
    days_count: int
    start_date: str
    end_date: str
    
    # Heart Rate & HRV
    avg_rhr: Optional[float] = None
    min_rhr: Optional[int] = None
    max_rhr: Optional[int] = None
    avg_hrv: Optional[float] = None
    hrv_balanced_pct: Optional[float] = None
    
    # Sleep
    avg_sleep_score: Optional[float] = None
    avg_sleep_hours: Optional[float] = None
    avg_deep_minutes: Optional[float] = None
    avg_rem_minutes: Optional[float] = None
    avg_light_minutes: Optional[float] = None
    avg_awake_minutes: Optional[float] = None
    deep_sleep_pct: Optional[float] = None
    rem_sleep_pct: Optional[float] = None
    
    # Stress & Body Battery
    avg_stress: Optional[float] = None
    avg_bb_charged: Optional[float] = None
    avg_bb_drained: Optional[float] = None
    avg_bb_highest: Optional[float] = None
    
    # Activity & Daily Movement
    avg_steps: Optional[float] = None
    total_steps: Optional[int] = None
    goal_met_days: Optional[int] = None
    goal_met_pct: Optional[float] = None
    total_distance_km: Optional[float] = None
    avg_active_calories: Optional[float] = None
    total_intensity_minutes: Optional[int] = None
    
    # Running & Endurance Specific
    running: RunningEnduranceStats = field(default_factory=RunningEnduranceStats)

    # VO2 Max & Vitals
    latest_vo2_max: Optional[float] = None
    avg_spo2: Optional[float] = None
    avg_respiration: Optional[float] = None


class InsightsEngine:
    """Analyzes health time series and produces statistical summaries, monthly trends, and actionable recommendations."""

    def __init__(self, records: List[Dict[str, Any]]):
        self.records = sorted(records, key=lambda r: r.get("date", ""))

    def filter_days(self, days: Optional[int] = None) -> List[Dict[str, Any]]:
        """Filter records by latest N days. If days is None, returns all records."""
        if not self.records:
            return []
        if days is None:
            return self.records
        return self.records[-days:]

    def compute_monthly_breakdown(self) -> List[MonthlyStats]:
        """Aggregate all records by calendar month (YYYY-MM) for long-term historical comparisons."""
        if not self.records:
            return []

        months_dict: Dict[str, List[Dict[str, Any]]] = {}
        for r in self.records:
            date_str = r.get("date", "")
            if len(date_str) >= 7:
                month_key = date_str[:7]
                if month_key not in months_dict:
                    months_dict[month_key] = []
                months_dict[month_key].append(r)

        sorted_months = sorted(months_dict.keys())
        monthly_list: List[MonthlyStats] = []

        prev_km: Optional[float] = None
        prev_runs: Optional[int] = None
        month_totals_map: Dict[str, Dict[str, Any]] = {}

        running_types = {
            "running", "trail_running", "treadmill_running", "street_running",
            "track_running", "virtual_run", "obstacle_run"
        }

        for m_key in sorted_months:
            m_records = months_dict[m_key]
            
            parts = m_key.split("-")
            month_label = f"{parts[0]}年 {parts[1]}月" if len(parts) == 2 else m_key

            m_runs = []
            for r in m_records:
                for act in r.get("activities", []):
                    act_type = str(act.get("type", "")).lower()
                    act_name = str(act.get("name", "")).lower()
                    dist = act.get("distance_km") or 0.0
                    cals = act.get("calories") or 0
                    is_run = any(rt in act_type for rt in running_types) or any(k in act_name for k in ["跑", "run", "marathon", "馬拉松", "越野"])
                    if is_run or dist >= 3.0:
                        m_runs.append({
                            "distance_km": dist,
                            "calories": cals,
                            "name": act.get("name", "跑步")
                        })

            tot_run_km = round(sum(run["distance_km"] for run in m_runs), 2)
            tot_runs_cnt = len(m_runs)
            runs_10k = sum(1 for run in m_runs if run["distance_km"] >= 10.0)
            full_marathons = sum(1 for run in m_runs if run["distance_km"] >= 42.0)
            half_marathons = sum(1 for run in m_runs if 21.0 <= run["distance_km"] < 42.0)
            longest_km = max([run["distance_km"] for run in m_runs], default=0.0)

            tot_cals = sum(r.get("active_calories") or 0 for r in m_records)

            rhrs = [r["resting_hr"] for r in m_records if r.get("resting_hr") is not None]
            hrvs = [r["hrv_overnight_avg"] for r in m_records if r.get("hrv_overnight_avg") is not None]
            
            # Sleep stages aggregation
            sleep_secs = [r["sleep_duration_seconds"] for r in m_records if r.get("sleep_duration_seconds") is not None]
            deep_secs = [r["deep_sleep_seconds"] for r in m_records if r.get("deep_sleep_seconds") is not None]
            rem_secs = [r["rem_sleep_seconds"] for r in m_records if r.get("rem_sleep_seconds") is not None]
            light_secs = [r["light_sleep_seconds"] for r in m_records if r.get("light_sleep_seconds") is not None]
            awake_secs = [r["awake_seconds"] for r in m_records if r.get("awake_seconds") is not None]
            sleep_scores = [r["sleep_score"] for r in m_records if r.get("sleep_score") is not None]

            avg_sleep_h = round(statistics.mean(sleep_secs) / 3600, 2) if sleep_secs else None
            avg_deep_h = round(statistics.mean(deep_secs) / 3600, 2) if deep_secs else 0.0
            avg_rem_h = round(statistics.mean(rem_secs) / 3600, 2) if rem_secs else 0.0
            avg_light_h = round(statistics.mean(light_secs) / 3600, 2) if light_secs else 0.0
            avg_awake_h = round(statistics.mean(awake_secs) / 3600, 2) if awake_secs else 0.0

            tot_stage_h = avg_deep_h + avg_rem_h + avg_light_h + avg_awake_h
            deep_pct = round(avg_deep_h / tot_stage_h * 100, 1) if tot_stage_h > 0 else None
            rem_pct = round(avg_rem_h / tot_stage_h * 100, 1) if tot_stage_h > 0 else None

            steps = [r["steps"] for r in m_records if r.get("steps") is not None]
            stresses = [r["avg_stress"] for r in m_records if r.get("avg_stress") is not None]

            growth_pct = None
            if prev_km is not None and prev_km > 0:
                growth_pct = round(((tot_run_km - prev_km) / prev_km) * 100, 1)
            prev_km = tot_run_km

            mom_runs_pct = None
            if prev_runs is not None and prev_runs > 0:
                mom_runs_pct = round(((tot_runs_cnt - prev_runs) / prev_runs) * 100, 1)
            prev_runs = tot_runs_cnt

            month_totals_map[m_key] = {
                "tot_run_km": tot_run_km,
                "tot_runs": tot_runs_cnt
            }

            parts = m_key.split("-")
            prev_y_key = f"{int(parts[0]) - 1}-{parts[1]}" if len(parts) == 2 else ""
            yoy_km_pct = None
            last_year_km = None
            yoy_runs_pct = None
            if prev_y_key in month_totals_map:
                last_year_km = month_totals_map[prev_y_key]["tot_run_km"]
                if last_year_km > 0:
                    yoy_km_pct = round(((tot_run_km - last_year_km) / last_year_km) * 100, 1)
                last_year_runs = month_totals_map[prev_y_key]["tot_runs"]
                if last_year_runs > 0:
                    yoy_runs_pct = round(((tot_runs_cnt - last_year_runs) / last_year_runs) * 100, 1)

            m_stat = MonthlyStats(
                month=m_key,
                month_label=month_label,
                days_count=len(m_records),
                total_run_km=tot_run_km,
                total_runs=tot_runs_cnt,
                runs_10k_plus=runs_10k,
                full_marathons=full_marathons,
                half_marathons=half_marathons,
                total_calories=int(tot_cals),
                avg_rhr=round(statistics.mean(rhrs), 1) if rhrs else None,
                avg_hrv=round(statistics.mean(hrvs), 1) if hrvs else None,
                avg_sleep_hours=avg_sleep_h,
                avg_deep_hours=avg_deep_h,
                avg_rem_hours=avg_rem_h,
                avg_light_hours=avg_light_h,
                avg_awake_hours=avg_awake_h,
                deep_pct=deep_pct,
                rem_pct=rem_pct,
                avg_sleep_score=round(statistics.mean(sleep_scores), 1) if sleep_scores else None,
                avg_steps=int(statistics.mean(steps)) if steps else None,
                avg_stress=round(statistics.mean(stresses), 1) if stresses else None,
                longest_run_km=round(longest_km, 2),
                mom_km_growth_pct=growth_pct,
                yoy_km_growth_pct=yoy_km_pct,
                last_year_run_km=last_year_km,
                mom_runs_growth_pct=mom_runs_pct,
                yoy_runs_growth_pct=yoy_runs_pct,
            )
            monthly_list.append(m_stat)

        return monthly_list

    def _extract_running_stats(self, subset: List[Dict[str, Any]]) -> RunningEnduranceStats:
        """Analyze all activities in the subset to extract running and endurance stats."""
        stats = RunningEnduranceStats()
        if not subset:
            return stats

        running_types = {
            "running", "trail_running", "treadmill_running", "street_running",
            "track_running", "virtual_run", "obstacle_run"
        }

        all_runs = []
        all_activities = []
        
        for r in subset:
            rec_date = r.get("date", "")
            for act in r.get("activities", []):
                act_type = str(act.get("type", "")).lower()
                act_name = str(act.get("name", "")).lower()
                dist = act.get("distance_km") or 0.0
                cals = act.get("calories") or 0

                all_activities.append({
                    "date": rec_date,
                    "distance_km": dist,
                    "calories": cals,
                    "name": act.get("name", "Activity"),
                    "type": act.get("type", "unknown")
                })

                is_run = any(rt in act_type for rt in running_types) or any(k in act_name for k in ["跑", "run", "marathon", "馬拉松", "越野"])
                if is_run or dist >= 3.0:
                    all_runs.append({
                        "date": rec_date,
                        "distance_km": dist,
                        "calories": cals,
                        "name": act.get("name", "跑步"),
                        "pace": act.get("pace"),
                        "avg_hr": act.get("avg_hr"),
                    })

        stats.total_runs = len(all_runs)
        stats.total_run_km = round(sum(r["distance_km"] for r in all_runs), 2)
        stats.total_run_calories = sum(r["calories"] for r in all_runs if r["calories"])

        days_count = len(subset)
        if days_count >= 1:
            stats.weekly_run_km = round((stats.total_run_km / days_count) * 7, 1)

        if stats.total_run_km > 0 and stats.total_run_calories > 0:
            stats.avg_calories_per_km = round(stats.total_run_calories / stats.total_run_km, 1)

        if all_activities:
            stats.max_workout_calories = max(a["calories"] for a in all_activities if a["calories"])

        ten_k_runs = []
        for run in all_runs:
            d = run["distance_km"]
            if d >= 42.0:
                stats.full_marathon_count += 1
            elif d >= 21.0:
                stats.half_marathon_count += 1
            elif d >= 10.0:
                stats.mid_distance_count += 1
            else:
                stats.short_run_count += 1

            if d >= 10.0:
                ten_k_runs.append(run)

        stats.runs_10k_plus_count = len(ten_k_runs)

        if all_runs:
            longest = max(all_runs, key=lambda x: x["distance_km"])
            stats.longest_run_km = longest["distance_km"]
            stats.longest_run_date = longest["date"]
            stats.longest_run_name = longest["name"]

        if stats.runs_10k_plus_count > 0:
            stats.days_per_10k_run = round(days_count / stats.runs_10k_plus_count, 1)

        latest_date_str = subset[-1]["date"]
        latest_dt = datetime.strptime(latest_date_str, "%Y-%m-%d").date()

        all_ten_k_in_history = []
        for r in self.records:
            r_date = r.get("date", "")
            for act in r.get("activities", []):
                dist = act.get("distance_km") or 0.0
                if dist >= 10.0:
                    all_ten_k_in_history.append({
                        "date": r_date,
                        "distance_km": dist,
                        "name": act.get("name", "長跑")
                    })

        if all_ten_k_in_history:
            last_10k = all_ten_k_in_history[-1]
            last_10k_dt = datetime.strptime(last_10k["date"], "%Y-%m-%d").date()
            diff_days = (latest_dt - last_10k_dt).days
            stats.days_since_last_10k = max(0, diff_days)
            stats.last_10k_date = last_10k["date"]
            stats.last_10k_km = last_10k["distance_km"]
            stats.last_10k_name = last_10k["name"]

        return stats

    def compute_summary(self, subset: List[Dict[str, Any]], window_name: str) -> WindowSummary:
        """Compute comprehensive statistical aggregations for a subset of records."""
        if not subset:
            return WindowSummary(
                window_name=window_name,
                days_count=0,
                start_date="-",
                end_date="-",
            )

        rhrs = [r["resting_hr"] for r in subset if r.get("resting_hr") is not None]
        hrvs = [r["hrv_overnight_avg"] for r in subset if r.get("hrv_overnight_avg") is not None]
        hrv_statuses = [r["hrv_status"] for r in subset if r.get("hrv_status")]
        
        sleep_scores = [r["sleep_score"] for r in subset if r.get("sleep_score") is not None]
        sleep_secs = [r["sleep_duration_seconds"] for r in subset if r.get("sleep_duration_seconds") is not None]
        deep_secs = [r["deep_sleep_seconds"] for r in subset if r.get("deep_sleep_seconds") is not None]
        rem_secs = [r["rem_sleep_seconds"] for r in subset if r.get("rem_sleep_seconds") is not None]
        light_secs = [r["light_sleep_seconds"] for r in subset if r.get("light_sleep_seconds") is not None]
        awake_secs = [r["awake_seconds"] for r in subset if r.get("awake_seconds") is not None]

        stresses = [r["avg_stress"] for r in subset if r.get("avg_stress") is not None]
        bb_chargeds = [r["body_battery_charged"] for r in subset if r.get("body_battery_charged") is not None]
        bb_draineds = [r["body_battery_drained"] for r in subset if r.get("body_battery_drained") is not None]
        bb_highests = [r["body_battery_highest"] for r in subset if r.get("body_battery_highest") is not None]

        steps = [r["steps"] for r in subset if r.get("steps") is not None]
        goals = [r for r in subset if r.get("steps") is not None and r.get("step_goal") is not None and r["step_goal"] > 0]
        distances = [r["distance_meters"] for r in subset if r.get("distance_meters") is not None]
        active_cals = [r["active_calories"] for r in subset if r.get("active_calories") is not None]
        
        mod_ints = [r.get("moderate_intensity_minutes") or 0 for r in subset]
        vig_ints = [r.get("vigorous_intensity_minutes") or 0 for r in subset]
        tot_intensity = sum(mod + vig * 2 for mod, vig in zip(mod_ints, vig_ints))

        vo2_maxs = [r["vo2_max"] for r in subset if r.get("vo2_max") is not None]
        spo2s = [r["spo2_avg"] for r in subset if r.get("spo2_avg") is not None]
        resps = [r["respiration_avg"] for r in subset if r.get("respiration_avg") is not None]

        tot_sleep_time = sum(sleep_secs) if sleep_secs else 0
        tot_deep_time = sum(deep_secs) if deep_secs else 0
        tot_rem_time = sum(rem_secs) if rem_secs else 0
        
        deep_pct = (tot_deep_time / tot_sleep_time * 100) if tot_sleep_time > 0 else 0
        rem_pct = (tot_rem_time / tot_sleep_time * 100) if tot_sleep_time > 0 else 0

        goal_met_cnt = sum(1 for r in goals if r["steps"] >= r["step_goal"])
        goal_met_rate = (goal_met_cnt / len(goals) * 100) if goals else 0

        balanced_hrv_cnt = sum(1 for s in hrv_statuses if s.upper() == "BALANCED")
        hrv_balanced_rate = (balanced_hrv_cnt / len(hrv_statuses) * 100) if hrv_statuses else 0

        running_stats = self._extract_running_stats(subset)

        summary = WindowSummary(
            window_name=window_name,
            days_count=len(subset),
            start_date=subset[0]["date"],
            end_date=subset[-1]["date"],
            avg_rhr=round(statistics.mean(rhrs), 1) if rhrs else None,
            min_rhr=min(rhrs) if rhrs else None,
            max_rhr=max(rhrs) if rhrs else None,
            avg_hrv=round(statistics.mean(hrvs), 1) if hrvs else None,
            hrv_balanced_pct=round(hrv_balanced_rate, 1) if hrv_statuses else None,
            avg_sleep_score=round(statistics.mean(sleep_scores), 1) if sleep_scores else None,
            avg_sleep_hours=round(statistics.mean(sleep_secs) / 3600, 2) if sleep_secs else None,
            avg_deep_minutes=round(statistics.mean(deep_secs) / 60, 1) if deep_secs else None,
            avg_rem_minutes=round(statistics.mean(rem_secs) / 60, 1) if rem_secs else None,
            avg_light_minutes=round(statistics.mean(light_secs) / 60, 1) if light_secs else None,
            avg_awake_minutes=round(statistics.mean(awake_secs) / 60, 1) if awake_secs else None,
            deep_sleep_pct=round(deep_pct, 1),
            rem_sleep_pct=round(rem_pct, 1),
            avg_stress=round(statistics.mean(stresses), 1) if stresses else None,
            avg_bb_charged=round(statistics.mean(bb_chargeds), 1) if bb_chargeds else None,
            avg_bb_drained=round(statistics.mean(bb_draineds), 1) if bb_draineds else None,
            avg_bb_highest=round(statistics.mean(bb_highests), 1) if bb_highests else None,
            avg_steps=round(statistics.mean(steps), 0) if steps else None,
            total_steps=sum(steps) if steps else 0,
            goal_met_days=goal_met_cnt,
            goal_met_pct=round(goal_met_rate, 1),
            total_distance_km=round(sum(distances) / 1000, 1) if distances else 0,
            avg_active_calories=round(statistics.mean(active_cals), 0) if active_cals else None,
            total_intensity_minutes=tot_intensity,
            running=running_stats,
            latest_vo2_max=vo2_maxs[-1] if vo2_maxs else None,
            avg_spo2=round(statistics.mean(spo2s), 1) if spo2s else None,
            avg_respiration=round(statistics.mean(resps), 1) if resps else None,
        )
        return summary

    def compute_annual_marathon_stats(self) -> List[AnnualMarathonStats]:
        """Compute annual outdoor-only average time spent, pace, and counts for half & full marathons."""
        outdoor_runs = []
        for r in self.records:
            d_str = r.get("date", "")
            y_str = d_str[:4]
            for act in r.get("activities", []):
                act_type = (act.get("type") or "").lower()
                is_indoor = "treadmill" in act_type or "indoor" in act_type
                dist = act.get("distance_km") or 0.0
                dur = act.get("duration_minutes") or 0.0
                if not is_indoor and dist >= 21.0 and dur > 0:
                    outdoor_runs.append({
                        "date": d_str,
                        "year": y_str,
                        "distance_km": dist,
                        "duration_minutes": dur,
                        "name": act.get("name", ""),
                    })

        years = sorted(list(set(r["year"] for r in outdoor_runs if r["year"])))
        results: List[AnnualMarathonStats] = []

        def calc_cohort(runs: List[Dict[str, Any]], year_code: str, year_label: str) -> AnnualMarathonStats:
            stat = AnnualMarathonStats(year=year_code, year_label=year_label)
            
            # Standard Half Marathon (室外 21.0 <= km < 25.0)
            sh = [r for r in runs if 21.0 <= r["distance_km"] < 25.0]
            if sh:
                stat.std_half_count = len(sh)
                tot_dur = sum(r["duration_minutes"] for r in sh)
                tot_km = sum(r["distance_km"] for r in sh)
                avg_dur = tot_dur / len(sh)
                avg_km = tot_km / len(sh)
                stat.std_half_avg_minutes = round(avg_dur, 1)
                stat.std_half_avg_time_str = format_duration(avg_dur)
                stat.std_half_avg_pace_str = format_pace(avg_dur, avg_km)
                stat.std_half_avg_km = round(avg_km, 2)
                fastest = min(sh, key=lambda x: x["duration_minutes"])
                stat.std_half_fastest_time_str = format_duration(fastest["duration_minutes"])
                stat.std_half_fastest_date = fastest["date"]
                stat.std_half_fastest_pace_str = format_pace(fastest["duration_minutes"], fastest["distance_km"])
                stat.std_half_fastest_km = round(fastest["distance_km"], 2)

            # Extended Half Marathon / LSD (室外 21.0 <= km < 42.0)
            eh = [r for r in runs if 21.0 <= r["distance_km"] < 42.0]
            if eh:
                stat.ext_half_count = len(eh)
                tot_dur = sum(r["duration_minutes"] for r in eh)
                tot_km = sum(r["distance_km"] for r in eh)
                avg_dur = tot_dur / len(eh)
                avg_km = tot_km / len(eh)
                stat.ext_half_avg_minutes = round(avg_dur, 1)
                stat.ext_half_avg_time_str = format_duration(avg_dur)
                stat.ext_half_avg_pace_str = format_pace(avg_dur, avg_km)
                stat.ext_half_avg_km = round(avg_km, 2)
                fastest = min(eh, key=lambda x: x["duration_minutes"])
                stat.ext_half_fastest_time_str = format_duration(fastest["duration_minutes"])
                stat.ext_half_fastest_date = fastest["date"]
                stat.ext_half_fastest_pace_str = format_pace(fastest["duration_minutes"], fastest["distance_km"])
                stat.ext_half_fastest_km = round(fastest["distance_km"], 2)

            # Standard Full Marathon (室外 42.0 <= km < 45.0)
            sf = [r for r in runs if 42.0 <= r["distance_km"] < 45.0]
            if sf:
                stat.std_full_count = len(sf)
                tot_dur = sum(r["duration_minutes"] for r in sf)
                tot_km = sum(r["distance_km"] for r in sf)
                avg_dur = tot_dur / len(sf)
                avg_km = tot_km / len(sf)
                stat.std_full_avg_minutes = round(avg_dur, 1)
                stat.std_full_avg_time_str = format_duration(avg_dur)
                stat.std_full_avg_pace_str = format_pace(avg_dur, avg_km)
                stat.std_full_avg_km = round(avg_km, 2)
                fastest = min(sf, key=lambda x: x["duration_minutes"])
                stat.std_full_fastest_time_str = format_duration(fastest["duration_minutes"])
                stat.std_full_fastest_date = fastest["date"]
                stat.std_full_fastest_pace_str = format_pace(fastest["duration_minutes"], fastest["distance_km"])
                stat.std_full_fastest_km = round(fastest["distance_km"], 2)

            # Extended Full Marathon / Ultra (室外 km >= 42.0)
            ef = [r for r in runs if r["distance_km"] >= 42.0]
            if ef:
                stat.ext_full_count = len(ef)
                tot_dur = sum(r["duration_minutes"] for r in ef)
                tot_km = sum(r["distance_km"] for r in ef)
                avg_dur = tot_dur / len(ef)
                avg_km = tot_km / len(ef)
                stat.ext_full_avg_minutes = round(avg_dur, 1)
                stat.ext_full_avg_time_str = format_duration(avg_dur)
                stat.ext_full_avg_pace_str = format_pace(avg_dur, avg_km)
                stat.ext_full_avg_km = round(avg_km, 2)
                fastest = min(ef, key=lambda x: x["duration_minutes"])
                stat.ext_full_fastest_time_str = format_duration(fastest["duration_minutes"])
                stat.ext_full_fastest_date = fastest["date"]
                stat.ext_full_fastest_pace_str = format_pace(fastest["duration_minutes"], fastest["distance_km"])
                stat.ext_full_fastest_km = round(fastest["distance_km"], 2)

            return stat

        # Per Year
        for y in years:
            y_runs = [r for r in outdoor_runs if r["year"] == y]
            results.append(calc_cohort(y_runs, y, f"{y} 年"))

        # All-Time
        results.append(calc_cohort(outdoor_runs, "all", "全部歷史累計 (All-Time)"))
        return results

    def generate_recommendations(self) -> List[RecommendationItem]:
        """Generate smart, evidence-based health and running recommendations based on multi-window trends."""
        recs: List[RecommendationItem] = []
        if not self.records:
            return recs

        recent_7 = self.filter_days(7)
        recent_30 = self.filter_days(30)
        s7 = self.compute_summary(recent_7, "7D")
        s30 = self.compute_summary(recent_30, "30D")
        latest = self.records[-1]

        # 1. 長跑與馬拉松訓練專屬分析
        run_stats_30 = s30.running
        
        if run_stats_30.days_since_last_10k is not None:
            if run_stats_30.days_since_last_10k >= 14:
                recs.append(RecommendationItem(
                    category="長跑與馬拉松",
                    level="warning",
                    title=f"已超過 {run_stats_30.days_since_last_10k} 天未進行 10K+ 長跑",
                    description=f"距離上次長跑（{run_stats_30.last_10k_date}，{run_stats_30.last_10k_km} km）已有 {run_stats_30.days_since_last_10k} 天。有氧耐力與粒線體密度需要每 7~10 天維持一次長距離刺激。",
                    action="建議在本週末安排一次輕鬆節奏的 Zone 2 長距離慢跑（LSD 10~15 km），重啟有氧基礎。",
                ))
            elif run_stats_30.days_since_last_10k <= 6:
                recs.append(RecommendationItem(
                    category="長跑與馬拉松",
                    level="good",
                    title="長跑週期維持良好",
                    description=f"最近一次 10K+ 長跑在 {run_stats_30.days_since_last_10k} 天前完成（{run_stats_30.last_10k_km} km），近 30 天共累積 {run_stats_30.runs_10k_plus_count} 次長距離訓練。",
                    action="持續保持規律的長距離節奏，注意跑後碳水化合物與電解質補給。",
                ))

        if run_stats_30.full_marathon_count > 0 or run_stats_30.half_marathon_count >= 2:
            recs.append(RecommendationItem(
                category="長跑與馬拉松",
                level="good",
                title="具備充沛的長距離賽事耐力底子",
                description=f"近 30 天包含 {run_stats_30.full_marathon_count} 場全馬/超馬與 {run_stats_30.half_marathon_count} 場半馬/LSD，單次最長達 {run_stats_30.longest_run_km} km，心肺與肌肉耐受度極佳。",
                action="高跑量期間請特別關注晨間靜止心率與 HRV，適時穿插滾筒按摩與下肢伸展。",
            ))

        if run_stats_30.total_run_calories > 0 and run_stats_30.avg_calories_per_km:
            recs.append(RecommendationItem(
                category="長跑與馬拉松",
                level="good",
                title=f"長跑每公里約消耗 {run_stats_30.avg_calories_per_km:.0f} 大卡",
                description=f"近 30 天跑步運動總計燃燒 {run_stats_30.total_run_calories:,} kcal。每進行一次 10K 長跑約消耗 {run_stats_30.avg_calories_per_km * 10:.0f} 大卡能量。",
                action="長跑超過 75 分鐘時，建議每 45 分鐘補充 25~30g 能量膠或運動飲料以防撞牆。",
            ))

        # 🎯 標準全馬每小時配速與時速策略建議 (Standard Marathon Pace per Hour Recommendation)
        recs.append(RecommendationItem(
            category="長跑與馬拉松",
            level="good",
            title="標準全馬每小時配速與時速策略建議 (Marathon Pace / Hourly Speed)",
            description="依據您 2026 室外半馬最佳 1h 52m 42s (配速 5:20/km) 與全馬歷史最佳 4h 03m 12s (配速 5:46/km)：\n"
                        "• 🎯 衝刺破四 (Sub-4): 時速 10.55 km/h，每小時前進 10.55 km，均配 5:41/km (心率 Zone 2~3)\n"
                        "• 🏃 穩健精進 (4h 15m): 時速 9.93 km/h，每小時前進 9.93 km，均配 6:02/km\n"
                        "• 🛡️ 巡航完賽 (4h 30m): 時速 9.38 km/h，每小時前進 9.38 km，均配 6:24/km (貼合 2025 均速)\n"
                        "建議採等速或負分段配速（Negative Split），第 1 小時壓制興奮感維持 10.3~10.5 km/h，第 2~3 小時巡航，第 4 小時衝刺剩餘 10.7 km。",
            action="全馬全程每小時推進約 9.5~10.5 公里；每 45~50 分鐘務必補充 1 包能量膠 (25~30g 碳水) 與 400ml 水/電解質，確保血糖平穩以防撞牆。",
        ))

        # 2. 睡眠與恢復
        if s30.avg_sleep_hours is not None:
            if s30.avg_sleep_hours < 6.8:
                recs.append(RecommendationItem(
                    category="睡眠與恢復",
                    level="critical",
                    title="長期睡眠時長偏低",
                    description=f"近 30 天平均睡眠為 {s30.avg_sleep_hours:.1f} 小時，低於運動員與常人建議的 7~8.5 小時，可能影響長跑後的肌肉修復與疲勞消除。",
                    action="建議將睡前就寢時間提前 30~45 分鐘，確保肌肉在睡眠中有充裕時間進行超補償。",
                ))
            elif s30.avg_sleep_hours >= 7.2:
                recs.append(RecommendationItem(
                    category="睡眠與恢復",
                    level="good",
                    title="睡眠時長充裕穩定",
                    description=f"近 30 天平均睡眠達到 {s30.avg_sleep_hours:.1f} 小時，為訓練後的肌肉與自律神經提供充足修復基石。",
                    action="請繼續維持目前的作息節律與就寢習慣。",
                ))

        if s30.deep_sleep_pct is not None and s30.deep_sleep_pct < 13.0:
            recs.append(RecommendationItem(
                category="睡眠與恢復",
                level="warning",
                title="深層睡眠 (Deep Sleep) 比例偏低",
                description=f"近 30 天深層睡眠佔比為 {s30.deep_sleep_pct:.1f}%（理想為 15%~25%）。深層睡眠為生長激素釋放、肌肉修復與關節修復的核心期。",
                action="建議睡前 2 小時避免藍光螢幕與高脂宵夜，維持臥室陰涼通風（建議 20~22°C）。",
            ))

        # 3. HRV 自律神經與恢復
        latest_hrv_stat = latest.get("hrv_status")
        if latest_hrv_stat in ("UNBALANCED", "LOW", "POOR"):
            recs.append(RecommendationItem(
                category="自律神經與壓力",
                level="critical",
                title="HRV 狀態偏低 / 失衡 (Unbalanced/Low)",
                description=f"近期夜間 HRV 處於 {latest_hrv_stat} 狀態，代表交感神經活性偏高，副交感神經（修復力）受抑制，身體正處於高疲勞或壓力累積期。",
                action="若今日有安排跑步訓練，建議改為極低強度恢復跑（Zone 1）或完全休息，多補充電解質。",
            ))
        elif s30.hrv_balanced_pct and s30.hrv_balanced_pct >= 80:
            recs.append(RecommendationItem(
                category="自律神經與壓力",
                level="good",
                title="自律神經調節能力優良",
                description=f"近 30 天有 {s30.hrv_balanced_pct:.0f}% 的天數 HRV 處於平衡區間（Balanced），神經系統對訓練負荷具備良好適應力。",
                action="目前的訓練與恢復調配得宜，可維持當前課表。",
            ))

        # 4. 靜止心率異常趨勢
        if s7.avg_rhr is not None and s30.avg_rhr is not None:
            rhr_diff = s7.avg_rhr - s30.avg_rhr
            if rhr_diff >= 3.5:
                recs.append(RecommendationItem(
                    category="心肺與活力",
                    level="critical",
                    title="近 7 天靜止心率微幅上升 (+{:.1f} bpm)".format(rhr_diff),
                    description=f"近 7 天靜止心率平均 ({s7.avg_rhr:.1f} bpm) 明顯高於 30 天平均 ({s30.avg_rhr:.1f} bpm)，可能為訓練過度、脫水或潛在感冒前兆。",
                    action="建議多喝水、確保充分睡眠，並適度減輕本週訓練強度與跑量。",
                ))
            elif rhr_diff <= -2.0:
                recs.append(RecommendationItem(
                    category="心肺與活力",
                    level="good",
                    title="靜止心率呈現穩定下降趨勢",
                    description=f"近 7 天靜止心率比 30 天平均下降 {abs(rhr_diff):.1f} bpm，顯示長跑有氧耐力與心臟每搏輸出量正在顯著提升。",
                    action="有氧基礎（Zone 2）訓練成效卓著，恭喜！",
                ))

        return recs
