"""Garmin Health Status Analyzer, Metrics Extractor & Historical Data Store."""

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
from garminconnect import Garmin

logger = logging.getLogger(__name__)


@dataclass
class HeartRateMetrics:
    resting_hr: Optional[int] = None
    min_hr: Optional[int] = None
    max_hr: Optional[int] = None
    avg_hr: Optional[int] = None


@dataclass
class SleepMetrics:
    sleep_score: Optional[int] = None
    qualifier_key: Optional[str] = None
    total_seconds: Optional[int] = None
    deep_seconds: Optional[int] = None
    light_seconds: Optional[int] = None
    rem_seconds: Optional[int] = None
    awake_seconds: Optional[int] = None
    sleep_start: Optional[str] = None
    sleep_end: Optional[str] = None

    @property
    def total_hours_formatted(self) -> str:
        if not self.total_seconds:
            return "N/A"
        hours = self.total_seconds // 3600
        mins = (self.total_seconds % 3600) // 60
        return f"{hours}h {mins}m"


@dataclass
class StressBodyBatteryMetrics:
    avg_stress_level: Optional[int] = None
    max_stress_level: Optional[int] = None
    stress_qualifier: Optional[str] = None
    rest_stress_seconds: Optional[int] = None
    low_stress_seconds: Optional[int] = None
    medium_stress_seconds: Optional[int] = None
    high_stress_seconds: Optional[int] = None
    body_battery_charged: Optional[int] = None
    body_battery_drained: Optional[int] = None
    body_battery_most_recent: Optional[int] = None
    body_battery_highest: Optional[int] = None
    body_battery_lowest: Optional[int] = None


@dataclass
class HRVMetrics:
    last_night_avg: Optional[int] = None
    last_night_5min_high: Optional[int] = None
    weekly_avg: Optional[int] = None
    baseline_low: Optional[int] = None
    baseline_high: Optional[int] = None
    status: Optional[str] = None
    feedback: Optional[str] = None


@dataclass
class ActivityMetrics:
    total_steps: Optional[int] = None
    step_goal: Optional[int] = None
    total_distance_meters: Optional[float] = None
    active_calories: Optional[int] = None
    total_calories: Optional[int] = None
    moderate_intensity_minutes: Optional[int] = None
    vigorous_intensity_minutes: Optional[int] = None
    floors_climbed: Optional[int] = None
    activities_list: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class WellnessSnapshot:
    target_date: str
    heart_rate: HeartRateMetrics = field(default_factory=HeartRateMetrics)
    sleep: SleepMetrics = field(default_factory=SleepMetrics)
    stress_bb: StressBodyBatteryMetrics = field(default_factory=StressBodyBatteryMetrics)
    hrv: HRVMetrics = field(default_factory=HRVMetrics)
    activity: ActivityMetrics = field(default_factory=ActivityMetrics)
    spo2_avg: Optional[float] = None
    respiration_avg: Optional[float] = None
    vo2_max: Optional[float] = None
    training_readiness_score: Optional[int] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def to_record_dict(self) -> Dict[str, Any]:
        """Convert snapshot into a clean flat record for storage and analytics."""
        return {
            "date": self.target_date,
            "resting_hr": self.heart_rate.resting_hr,
            "min_hr": self.heart_rate.min_hr,
            "max_hr": self.heart_rate.max_hr,
            "avg_hr": self.heart_rate.avg_hr,
            "sleep_score": self.sleep.sleep_score,
            "sleep_qualifier": self.sleep.qualifier_key,
            "sleep_duration_seconds": self.sleep.total_seconds,
            "deep_sleep_seconds": self.sleep.deep_seconds,
            "light_sleep_seconds": self.sleep.light_seconds,
            "rem_sleep_seconds": self.sleep.rem_seconds,
            "awake_seconds": self.sleep.awake_seconds,
            "sleep_start": self.sleep.sleep_start,
            "sleep_end": self.sleep.sleep_end,
            "hrv_status": self.hrv.status,
            "hrv_overnight_avg": self.hrv.last_night_avg,
            "hrv_weekly_avg": self.hrv.weekly_avg,
            "hrv_baseline_low": self.hrv.baseline_low,
            "hrv_baseline_high": self.hrv.baseline_high,
            "hrv_feedback": self.hrv.feedback,
            "body_battery_charged": self.stress_bb.body_battery_charged,
            "body_battery_drained": self.stress_bb.body_battery_drained,
            "body_battery_highest": self.stress_bb.body_battery_highest,
            "body_battery_lowest": self.stress_bb.body_battery_lowest,
            "body_battery_recent": self.stress_bb.body_battery_most_recent,
            "avg_stress": self.stress_bb.avg_stress_level,
            "max_stress": self.stress_bb.max_stress_level,
            "stress_qualifier": self.stress_bb.stress_qualifier,
            "rest_stress_seconds": self.stress_bb.rest_stress_seconds,
            "low_stress_seconds": self.stress_bb.low_stress_seconds,
            "medium_stress_seconds": self.stress_bb.medium_stress_seconds,
            "high_stress_seconds": self.stress_bb.high_stress_seconds,
            "steps": self.activity.total_steps,
            "step_goal": self.activity.step_goal,
            "distance_meters": self.activity.total_distance_meters,
            "active_calories": self.activity.active_calories,
            "total_calories": self.activity.total_calories,
            "moderate_intensity_minutes": self.activity.moderate_intensity_minutes,
            "vigorous_intensity_minutes": self.activity.vigorous_intensity_minutes,
            "floors_climbed": self.activity.floors_climbed,
            "spo2_avg": self.spo2_avg,
            "respiration_avg": self.respiration_avg,
            "vo2_max": self.vo2_max,
            "training_readiness": self.training_readiness_score,
            "activities": self.activity.activities_list,
        }

    @classmethod
    def from_record_dict(cls, data: Dict[str, Any]) -> "WellnessSnapshot":
        """Reconstruct a WellnessSnapshot from a cached record dictionary."""
        snapshot = cls(target_date=data.get("date", ""))
        snapshot.heart_rate = HeartRateMetrics(
            resting_hr=data.get("resting_hr"),
            min_hr=data.get("min_hr"),
            max_hr=data.get("max_hr"),
            avg_hr=data.get("avg_hr"),
        )
        snapshot.sleep = SleepMetrics(
            sleep_score=data.get("sleep_score"),
            qualifier_key=data.get("sleep_qualifier"),
            total_seconds=data.get("sleep_duration_seconds"),
            deep_seconds=data.get("deep_sleep_seconds"),
            light_seconds=data.get("light_sleep_seconds"),
            rem_seconds=data.get("rem_sleep_seconds"),
            awake_seconds=data.get("awake_seconds"),
            sleep_start=data.get("sleep_start"),
            sleep_end=data.get("sleep_end"),
        )
        snapshot.stress_bb = StressBodyBatteryMetrics(
            avg_stress_level=data.get("avg_stress"),
            max_stress_level=data.get("max_stress"),
            stress_qualifier=data.get("stress_qualifier"),
            rest_stress_seconds=data.get("rest_stress_seconds"),
            low_stress_seconds=data.get("low_stress_seconds"),
            medium_stress_seconds=data.get("medium_stress_seconds"),
            high_stress_seconds=data.get("high_stress_seconds"),
            body_battery_charged=data.get("body_battery_charged"),
            body_battery_drained=data.get("body_battery_drained"),
            body_battery_most_recent=data.get("body_battery_recent"),
            body_battery_highest=data.get("body_battery_highest"),
            body_battery_lowest=data.get("body_battery_lowest"),
        )
        snapshot.hrv = HRVMetrics(
            last_night_avg=data.get("hrv_overnight_avg"),
            weekly_avg=data.get("hrv_weekly_avg"),
            baseline_low=data.get("hrv_baseline_low"),
            baseline_high=data.get("hrv_baseline_high"),
            status=data.get("hrv_status"),
            feedback=data.get("hrv_feedback"),
        )
        snapshot.activity = ActivityMetrics(
            total_steps=data.get("steps"),
            step_goal=data.get("step_goal"),
            total_distance_meters=data.get("distance_meters"),
            active_calories=data.get("active_calories"),
            total_calories=data.get("total_calories"),
            moderate_intensity_minutes=data.get("moderate_intensity_minutes"),
            vigorous_intensity_minutes=data.get("vigorous_intensity_minutes"),
            floors_climbed=data.get("floors_climbed"),
            activities_list=data.get("activities", []),
        )
        snapshot.spo2_avg = data.get("spo2_avg")
        snapshot.respiration_avg = data.get("respiration_avg")
        snapshot.vo2_max = data.get("vo2_max")
        snapshot.training_readiness_score = data.get("training_readiness")
        return snapshot


class HealthDataStore:
    """Manages persistent incremental caching for Garmin health metrics."""

    def __init__(self, filepath: Optional[Path] = None):
        self.filepath = filepath or Path("garmin_health_history.json")
        self.data: Dict[str, Any] = {
            "user_name": "Garmin User",
            "last_synced_at": None,
            "records": {},
        }
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache from {self.filepath}: {e}")

    def save(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_record(self, record: Dict[str, Any], user_name: Optional[str] = None):
        date_key = record["date"]
        self.data["records"][date_key] = record
        if user_name:
            self.data["user_name"] = user_name
        self.data["last_synced_at"] = datetime.now().isoformat()

    def get_record(self, date_str: str) -> Optional[Dict[str, Any]]:
        return self.data.get("records", {}).get(date_str)

    def get_all_records(self) -> List[Dict[str, Any]]:
        """Return all stored records sorted chronologically."""
        records = list(self.data.get("records", {}).values())
        records.sort(key=lambda r: r["date"])
        return records

    def get_latest_date(self) -> Optional[str]:
        records = self.get_all_records()
        return records[-1]["date"] if records else None

    def get_oldest_date(self) -> Optional[str]:
        records = self.get_all_records()
        return records[0]["date"] if records else None


class HealthAnalyzer:
    """Fetches and processes daily health indicators from Garmin Connect."""

    def __init__(self, client: Garmin, store: Optional[HealthDataStore] = None):
        self.client = client
        self.store = store or HealthDataStore()

    def fetch_daily_snapshot(self, target_date: Optional[str] = None, force_refresh: bool = False) -> WellnessSnapshot:
        """Fetch all available health metrics for a specific date (YYYY-MM-DD)."""
        if not target_date:
            target_date = date.today().isoformat()

        # If already cached and not force refresh, load from store
        if not force_refresh:
            cached = self.store.get_record(target_date)
            # Only use cache if it's not today (today can change during the day)
            if cached and target_date != date.today().isoformat():
                return WellnessSnapshot.from_record_dict(cached)

        snapshot = WellnessSnapshot(target_date=target_date)
        user_name = None

        # 1. User Daily Summary (Steps, Calories, RHR, Distance)
        try:
            summary = self.client.get_user_summary(target_date)
            if summary:
                snapshot.raw_data["user_summary"] = summary
                user_name = summary.get("displayName")
                snapshot.heart_rate.resting_hr = summary.get("restingHeartRate")
                snapshot.heart_rate.min_hr = summary.get("minHeartRate")
                snapshot.heart_rate.max_hr = summary.get("maxHeartRate")
                snapshot.heart_rate.avg_hr = summary.get("averageHeartRate")

                snapshot.activity.total_steps = summary.get("totalSteps")
                snapshot.activity.step_goal = summary.get("dailyStepGoal")
                snapshot.activity.total_distance_meters = summary.get("totalDistanceMeters")
                snapshot.activity.active_calories = summary.get("activeKilocalories")
                snapshot.activity.total_calories = summary.get("totalKilocalories")
                snapshot.activity.moderate_intensity_minutes = summary.get("moderateIntensityMinutes")
                snapshot.activity.vigorous_intensity_minutes = summary.get("vigorousIntensityMinutes")
                snapshot.activity.floors_climbed = summary.get("floorsAscended")
                snapshot.spo2_avg = summary.get("averageSpo2")
                snapshot.respiration_avg = summary.get("avgWakingRespirationValue")
        except Exception as e:
            logger.debug(f"User summary fetch failed for {target_date}: {e}")

        # 2. Sleep Data
        try:
            sleep_data = self.client.get_sleep_data(target_date)
            if sleep_data:
                snapshot.raw_data["sleep"] = sleep_data
                daily_sleep = sleep_data.get("dailySleepDTO", {})
                snapshot.sleep.sleep_score = (
                    daily_sleep.get("sleepScores", {}).get("overall", {}).get("value")
                    or daily_sleep.get("sleepScores", {}).get("score")
                )
                snapshot.sleep.qualifier_key = (
                    daily_sleep.get("sleepScores", {}).get("overall", {}).get("qualifierKey")
                )
                snapshot.sleep.total_seconds = daily_sleep.get("sleepTimeSeconds")
                snapshot.sleep.deep_seconds = daily_sleep.get("deepSleepSeconds")
                snapshot.sleep.light_seconds = daily_sleep.get("lightSleepSeconds")
                snapshot.sleep.rem_seconds = daily_sleep.get("remSleepSeconds")
                snapshot.sleep.awake_seconds = daily_sleep.get("awakeSleepSeconds")
                if daily_sleep.get("sleepStartTimestampLocal"):
                    snapshot.sleep.sleep_start = daily_sleep.get("sleepStartTimestampLocal")
                if daily_sleep.get("sleepEndTimestampLocal"):
                    snapshot.sleep.sleep_end = daily_sleep.get("sleepEndTimestampLocal")
        except Exception as e:
            logger.debug(f"Sleep data fetch failed for {target_date}: {e}")

        # 3. Body Battery & Stress
        try:
            bb_data = self.client.get_body_battery(target_date)
            if bb_data and isinstance(bb_data, list) and len(bb_data) > 0:
                snapshot.raw_data["body_battery"] = bb_data
                day_bb = bb_data[0] if isinstance(bb_data[0], dict) else {}
                snapshot.stress_bb.body_battery_charged = day_bb.get("charged")
                snapshot.stress_bb.body_battery_drained = day_bb.get("drained")
                snapshot.stress_bb.body_battery_highest = day_bb.get("highest")
                snapshot.stress_bb.body_battery_lowest = day_bb.get("lowest")
                bb_values = day_bb.get("bodyBatteryValuesArray", [])
                if bb_values:
                    snapshot.stress_bb.body_battery_most_recent = bb_values[-1][1]
        except Exception as e:
            logger.debug(f"Body battery fetch failed for {target_date}: {e}")

        try:
            stress_data = self.client.get_stress_data(target_date)
            if stress_data:
                snapshot.raw_data["stress"] = stress_data
                snapshot.stress_bb.avg_stress_level = stress_data.get("avgStressLevel")
                snapshot.stress_bb.max_stress_level = stress_data.get("maxStressLevel")
                snapshot.stress_bb.stress_qualifier = stress_data.get("stressQualifier")
                snapshot.stress_bb.rest_stress_seconds = stress_data.get("restStressDuration")
                snapshot.stress_bb.low_stress_seconds = stress_data.get("lowStressDuration")
                snapshot.stress_bb.medium_stress_seconds = stress_data.get("mediumStressDuration")
                snapshot.stress_bb.high_stress_seconds = stress_data.get("highStressDuration")
        except Exception as e:
            logger.debug(f"Stress data fetch failed for {target_date}: {e}")

        # 4. HRV Status
        try:
            hrv_data = self.client.get_hrv_data(target_date)
            if hrv_data and "hrvSummary" in hrv_data:
                snapshot.raw_data["hrv"] = hrv_data
                summary = hrv_data["hrvSummary"]
                snapshot.hrv.last_night_avg = summary.get("lastNightAvg")
                snapshot.hrv.last_night_5min_high = summary.get("lastNight5MinHigh")
                snapshot.hrv.weekly_avg = summary.get("weeklyAvg")
                snapshot.hrv.status = summary.get("status")
                snapshot.hrv.feedback = summary.get("feedbackPhrase")
                baseline = summary.get("baseline", {})
                snapshot.hrv.baseline_low = baseline.get("lowBalanced")
                snapshot.hrv.baseline_high = baseline.get("highBalanced")
        except Exception as e:
            logger.debug(f"HRV data fetch failed for {target_date}: {e}")

        # 5. Training Readiness & VO2 Max
        try:
            tr_data = self.client.get_training_readiness(target_date)
            if tr_data and isinstance(tr_data, list) and len(tr_data) > 0:
                snapshot.raw_data["training_readiness"] = tr_data
                snapshot.training_readiness_score = tr_data[0].get("score")
            elif isinstance(tr_data, dict):
                snapshot.training_readiness_score = tr_data.get("score")
        except Exception as e:
            logger.debug(f"Training readiness fetch failed for {target_date}: {e}")

        try:
            max_metrics = self.client.get_max_metrics(target_date)
            if max_metrics and isinstance(max_metrics, list) and len(max_metrics) > 0:
                snapshot.raw_data["max_metrics"] = max_metrics
                for item in max_metrics:
                    if "generic" in item and "vo2MaxValue" in item["generic"]:
                        snapshot.vo2_max = item["generic"]["vo2MaxValue"]
                        break
        except Exception as e:
            logger.debug(f"VO2 Max fetch failed for {target_date}: {e}")

        # 6. Activities of the day (Detailed with pace, elevation, calories)
        try:
            activities = self.client.get_activities_by_date(target_date, target_date)
            if activities:
                snapshot.raw_data["activities"] = activities
                for act in activities:
                    dist_km = round(act.get("distance", 0) / 1000, 2)
                    dur_sec = act.get("duration", 0)
                    pace_str = None
                    if dist_km > 0 and dur_sec > 0:
                        pace_seconds_per_km = dur_sec / dist_km
                        mins = int(pace_seconds_per_km // 60)
                        secs = int(pace_seconds_per_km % 60)
                        pace_str = f"{mins}'{secs:02d}\""

                    act_type_key = act.get("activityType", {}).get("typeKey", "unknown")
                    raw_name = act.get("activityName", "")
                    # Fallback mapping for common activity types if raw_name is empty or corrupted with replacement char
                    type_name_map = {
                        "treadmill_running": "跑步機跑步",
                        "running": "跑步",
                        "trail_running": "越野跑",
                        "track_running": "田徑場跑步",
                        "street_running": "路跑",
                        "cycling": "騎乘",
                        "indoor_cycling": "室內騎乘",
                        "swimming": "游泳",
                        "walking": "健走/步行",
                        "hiking": "徒步/登山",
                    }
                    if not raw_name or "\ufffd" in raw_name or raw_name.strip() == "":
                        resolved_name = type_name_map.get(act_type_key, "跑步" if "running" in act_type_key else "運動")
                    else:
                        resolved_name = raw_name

                    snapshot.activity.activities_list.append({
                        "name": resolved_name,
                        "type": act_type_key,
                        "duration_minutes": round(dur_sec / 60, 1),
                        "distance_km": dist_km,
                        "pace": pace_str,
                        "elevation_gain_m": round(act.get("elevationGain") or act.get("elevationGainInMeters") or 0),
                        "calories": act.get("calories"),
                        "avg_hr": act.get("averageHR"),
                        "max_hr": act.get("maxHR"),
                    })
        except Exception as e:
            logger.debug(f"Activities fetch failed for {target_date}: {e}")

        # Save to store
        record = snapshot.to_record_dict()
        self.store.add_record(record, user_name=user_name)
        self.store.save()

        return snapshot

    def sync_range(
        self,
        start_date: str,
        end_date: str,
        progress_callback: Optional[Any] = None,
        delay_seconds: float = 0.2,
    ) -> List[Dict[str, Any]]:
        """Sync a date range, utilizing cache for past dates and fetching missing dates."""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

        current_dt = start_dt
        total_days = (end_dt - start_dt).days + 1
        processed = 0

        synced_records = []
        while current_dt <= end_dt:
            date_str = current_dt.isoformat()
            processed += 1

            cached = self.store.get_record(date_str)
            # Fetch if not in cache or if it is today (today changes)
            if cached is None or date_str == date.today().isoformat():
                if progress_callback:
                    progress_callback(processed, total_days, date_str, "fetching")
                snapshot = self.fetch_daily_snapshot(date_str, force_refresh=True)
                synced_records.append(snapshot.to_record_dict())
                time.sleep(delay_seconds)
            else:
                if progress_callback:
                    progress_callback(processed, total_days, date_str, "cached")
                synced_records.append(cached)

            current_dt += timedelta(days=1)

        return synced_records
