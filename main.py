"""Garmin Connect Health Status Dashboard, Historical Sync & HTML Generator."""

import argparse
import json
import os
import sys
import webbrowser
from datetime import date, datetime, timedelta
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from garmin_client import GarminClientManager
from health_analyzer import HealthAnalyzer, HealthDataStore, WellnessSnapshot
from insights_engine import InsightsEngine
from html_generator import generate_dashboard_html

console = Console(legacy_windows=False, force_terminal=True)


def format_score(score: int, good_threshold: int = 80, fair_threshold: int = 60) -> Text:
    if score is None:
        return Text("N/A", style="dim")
    if score >= good_threshold:
        return Text(f"{score} (Excellent/Good)", style="bold green")
    elif score >= fair_threshold:
        return Text(f"{score} (Fair)", style="bold yellow")
    else:
        return Text(f"{score} (Poor/Low)", style="bold red")


def display_snapshot(snapshot: WellnessSnapshot):
    """Render a single wellness snapshot nicely in the terminal."""
    target_dt = snapshot.target_date

    user_name = "Garmin User"
    try:
        if snapshot.raw_data.get("user_summary"):
            user_name = snapshot.raw_data["user_summary"].get("displayName", "Garmin User")
    except Exception:
        pass

    header = Panel(
        Text(f"Garmin Health & Wellness Summary - {target_dt}", justify="center", style="bold cyan"),
        subtitle=f"Account: {user_name}",
    )
    console.print(header)

    # 1. Key Vital Signs Table
    vital_table = Table(title="🫀 Key Vitals & Recovery", show_header=True, header_style="bold magenta")
    vital_table.add_column("Metric", style="cyan", width=22)
    vital_table.add_column("Value", style="bold white", width=20)
    vital_table.add_column("Status / Assessment", style="white")

    rhr = snapshot.heart_rate.resting_hr
    rhr_text = f"{rhr} bpm" if rhr else "N/A"
    rhr_status = Text("Normal", style="green") if (rhr and 40 <= rhr <= 80) else (Text("Elevated", style="yellow") if rhr else Text("N/A", style="dim"))
    vital_table.add_row("Resting Heart Rate", rhr_text, rhr_status)

    min_hr, max_hr = snapshot.heart_rate.min_hr, snapshot.heart_rate.max_hr
    hr_range = f"{min_hr or '-'} - {max_hr or '-'} bpm" if (min_hr or max_hr) else "N/A"
    vital_table.add_row("All-Day HR Range", hr_range, Text("Daily variation", style="dim"))

    hrv_stat = snapshot.hrv.status or "N/A"
    hrv_val = f"{snapshot.hrv.last_night_avg} ms" if snapshot.hrv.last_night_avg else "N/A"
    if snapshot.hrv.status == "BALANCED":
        hrv_color = "bold green"
    elif snapshot.hrv.status in ("UNBALANCED", "LOW"):
        hrv_color = "bold yellow"
    elif snapshot.hrv.status == "POOR":
        hrv_color = "bold red"
    else:
        hrv_color = "dim"
    
    baseline_str = f"(Baseline: {snapshot.hrv.baseline_low}-{snapshot.hrv.baseline_high} ms)" if snapshot.hrv.baseline_low else ""
    hrv_comment = f"{hrv_stat} {baseline_str}".strip()
    vital_table.add_row("HRV (Overnight Avg)", hrv_val, Text(hrv_comment, style=hrv_color))

    spo2 = snapshot.spo2_avg
    spo2_str = f"{spo2:.1f}%" if spo2 else "N/A"
    spo2_style = "green" if (spo2 and spo2 >= 95) else ("yellow" if (spo2 and spo2 >= 90) else "dim")
    vital_table.add_row("Average SpO2 (Pulse Ox)", spo2_str, Text("Optimal (>95%)" if (spo2 and spo2 >= 95) else (spo2_str if spo2 else "N/A"), style=spo2_style))

    resp = snapshot.respiration_avg
    resp_str = f"{resp:.1f} brpm" if resp else "N/A"
    vital_table.add_row("Respiration Rate", resp_str, Text("Resting rate" if resp else "N/A", style="dim"))

    if snapshot.training_readiness_score is not None:
        vital_table.add_row("Training Readiness", f"{snapshot.training_readiness_score}/100", format_score(snapshot.training_readiness_score))
    if snapshot.vo2_max is not None:
        vital_table.add_row("VO2 Max", f"{snapshot.vo2_max:.1f} ml/kg/min", Text("Aerobic fitness", style="green"))

    console.print(vital_table)

    # 2. Sleep & Body Battery
    sleep_table = Table(title="😴 Sleep Performance", show_header=True, header_style="bold blue")
    sleep_table.add_column("Metric", style="cyan", width=18)
    sleep_table.add_column("Details", style="white")

    if snapshot.sleep.sleep_score is not None:
        sleep_table.add_row("Sleep Score", format_score(snapshot.sleep.sleep_score))
    sleep_table.add_row("Total Duration", snapshot.sleep.total_hours_formatted)
    
    deep_m = (snapshot.sleep.deep_seconds or 0) // 60
    light_m = (snapshot.sleep.light_seconds or 0) // 60
    rem_m = (snapshot.sleep.rem_seconds or 0) // 60
    awake_m = (snapshot.sleep.awake_seconds or 0) // 60
    
    stages_str = f"Deep: {deep_m}m | Light: {light_m}m | REM: {rem_m}m | Awake: {awake_m}m"
    sleep_table.add_row("Sleep Stages", stages_str if (snapshot.sleep.total_seconds) else "N/A")

    bb_table = Table(title="⚡ Stress & Body Battery", show_header=True, header_style="bold yellow")
    bb_table.add_column("Metric", style="cyan", width=18)
    bb_table.add_column("Value / Details", style="white")

    bb_current = snapshot.stress_bb.body_battery_most_recent
    bb_charged = snapshot.stress_bb.body_battery_charged
    bb_drained = snapshot.stress_bb.body_battery_drained
    bb_high = snapshot.stress_bb.body_battery_highest
    bb_low = snapshot.stress_bb.body_battery_lowest

    bb_summary = f"Current: {bb_current or '-'} (High: {bb_high or '-'}, Low: {bb_low or '-'})"
    bb_charge_drain = f"+{bb_charged or 0} charged / -{bb_drained or 0} drained"
    bb_table.add_row("Body Battery Level", bb_summary)
    bb_table.add_row("Daily Charge/Drain", bb_charge_drain)

    avg_stress = snapshot.stress_bb.avg_stress_level
    if avg_stress is not None:
        stress_text = f"{avg_stress}/100"
        stress_style = "green" if avg_stress <= 25 else ("yellow" if avg_stress <= 50 else "bold red")
        bb_table.add_row("Average Stress", Text(f"{stress_text} ({snapshot.stress_bb.stress_qualifier or 'Normal'})", style=stress_style))
    else:
        bb_table.add_row("Average Stress", "N/A")

    console.print(Columns([sleep_table, bb_table], expand=True))

    # 3. Activity & Movement
    act_table = Table(title="🏃 Daily Activity & Steps", show_header=True, header_style="bold green")
    act_table.add_column("Metric", style="cyan", width=22)
    act_table.add_column("Value", style="bold white", width=18)
    act_table.add_column("Progress / Details", style="white")

    steps = snapshot.activity.total_steps
    goal = snapshot.activity.step_goal
    if steps is not None:
        pct = (steps / goal * 100) if goal else 0
        pct_text = Text(f"{pct:.1f}% of goal ({goal:,} steps)", style="green" if pct >= 100 else "yellow")
        act_table.add_row("Steps", f"{steps:,}", pct_text)
    else:
        act_table.add_row("Steps", "N/A", Text("No step data", style="dim"))

    dist = snapshot.activity.total_distance_meters
    if dist is not None:
        act_table.add_row("Distance", f"{dist / 1000:.2f} km", Text("All-day distance", style="dim"))

    active_cal = snapshot.activity.active_calories
    tot_cal = snapshot.activity.total_calories
    if active_cal is not None or tot_cal is not None:
        cal_str = f"{active_cal or 0} active / {tot_cal or 0} total"
        act_table.add_row("Calories Burned", cal_str, Text("kcal", style="dim"))

    mod_int = snapshot.activity.moderate_intensity_minutes or 0
    vig_int = snapshot.activity.vigorous_intensity_minutes or 0
    act_table.add_row("Intensity Minutes", f"{mod_int + vig_int * 2} mins", Text(f"{mod_int} mod + {vig_int} vig (2x)", style="dim"))

    console.print(act_table)


def main():
    parser = argparse.ArgumentParser(description="Garmin Connect Health Tracker, Trends & HTML Dashboard")
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Incrementally sync recent Garmin health data and update cache",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=1000,
        help="Number of days to sync back from today (default: 1000 days)",
    )
    parser.add_argument(
        "--sync-all",
        action="store_true",
        help="Sync full 1000 days history or specify with --days",
    )
    parser.add_argument(
        "--html",
        "--report",
        dest="generate_html",
        action="store_true",
        help="Generate standalone interactive HTML dashboard",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Automatically open the generated HTML dashboard in the default web browser",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=date.today().isoformat(),
        help="Target date for single day terminal inspection (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--cn",
        action="store_true",
        help="Use Garmin China (garmin.cn) endpoints instead of global",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not automatically open the dashboard in browser after sync",
    )
    args = parser.parse_args()

    if args.cn:
        os.environ["GARMIN_IS_CN"] = "true"

    store = HealthDataStore()

    # Import existing single JSON if available to bootstrap cache
    legacy_json = Path("garmin_health_2026-08-23.json")
    if legacy_json.exists() and not store.get_record("2026-08-23"):
        try:
            with open(legacy_json, "r", encoding="utf-8") as f:
                d = json.load(f)
                store.add_record(d, user_name="Garmin User")
                store.save()
        except Exception:
            pass

    # Determine execution flow
    do_sync = args.sync or args.sync_all or (not args.generate_html and len(sys.argv) == 1)
    
    if do_sync:
        console.print("[bold cyan]Connecting to Garmin Connect...[/bold cyan]")
        client_mgr = GarminClientManager()
        try:
            client = client_mgr.get_client()
        except Exception as e:
            console.print(f"[bold red]Login Error:[/bold red] {e}")
            sys.exit(1)

        analyzer = HealthAnalyzer(client, store=store)

        days_to_fetch = args.days
        if args.sync_all and args.days == 30:
            days_to_fetch = 1000  # Default 1000 days history range

        end_date = date.today().isoformat()
        start_date = (date.today() - timedelta(days=days_to_fetch - 1)).isoformat()

        console.print(f"[bold green]Syncing Garmin health data from {start_date} to {end_date} ({days_to_fetch} days)...[/bold green]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Syncing records...", total=days_to_fetch)

            def progress_cb(current, total, date_str, status):
                progress.update(task, completed=current, description=f"[cyan]Syncing {date_str} ({status})...")

            analyzer.sync_range(start_date, end_date, progress_callback=progress_cb)

        console.print(f"[bold green][OK] Successfully synced {days_to_fetch} days into local cache![/bold green]")
    
    # Generate HTML report if requested or in default 1-click mode
    all_records = store.get_all_records()
    if not all_records:
        console.print("[yellow]No cached health records found. Please run with --sync first.[/yellow]")
        return

    # Always generate dashboard when sync or --report/--open is invoked
    user_name = store.data.get("user_name", "Garmin User")
    
    # 1. Generate GitHub Pages root index.html (Privacy-scrubbed)
    index_file = generate_dashboard_html(
        records=all_records,
        user_name=user_name,
        last_synced=store.data.get("last_synced_at"),
        output_path=Path("index.html"),
    )
    # 2. Also keep garmin_health_dashboard.html in sync
    html_file = generate_dashboard_html(
        records=all_records,
        user_name=user_name,
        last_synced=store.data.get("last_synced_at"),
        output_path=Path("garmin_health_dashboard.html"),
    )
    console.print(f"[bold green][OK] GitHub Pages generated:[/bold green] [underline cyan]{index_file.resolve()}[/underline cyan]")
    console.print(f"[bold green][OK] Local Dashboard updated:[/bold green] [underline cyan]{html_file.resolve()}[/underline cyan]")

    # Terminal output of latest day
    latest_snapshot = WellnessSnapshot.from_record_dict(all_records[-1])
    display_snapshot(latest_snapshot)

    # If --open or running one-click default, open browser
    if (args.open or do_sync) and not args.no_open:
        console.print("[cyan]Opening dashboard in default web browser...[/cyan]")
        webbrowser.open(f"file://{html_file.resolve()}")


if __name__ == "__main__":
    main()
