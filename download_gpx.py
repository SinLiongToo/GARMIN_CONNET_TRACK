"""Download GPX track files for Marathons and GPS running activities from Garmin Connect."""

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

from garmin_client import GarminClientManager
from garminconnect import Garmin
# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console(legacy_windows=False, force_terminal=True)


def sanitize_filename(name: str) -> str:
    """Sanitize strings for safe Windows/Linux file naming."""
    # Replace illegal filesystem characters: \ / : * ? " < > |
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', name)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized.strip('._')


TRAIL_KEYWORDS = [
    "越野", "trail", "ultra", "山徑", "野跑", "縱走", "柴山", "棲蘭", "陽明山", 
    "谷關", "salomon", "tnf", "utmb", "formosa", "super_race", "跑山", "越野賽"
]

TRAIL_ACTIVITY_TYPES = {"trail_running", "ultra_run", "hiking", "mountaineering", "obstacle_run"}


def is_trail_activity(act_type: str, act_name: str) -> bool:
    """Determine if an activity is a trail run or trail race."""
    act_type_lower = act_type.lower()
    act_name_lower = act_name.lower()

    if any(t in act_type_lower for t in ["trail", "ultra"]):
        return True
    if any(kw in act_name_lower for kw in TRAIL_KEYWORDS):
        return True
    return False


def classify_activity(distance_meters: float, act_type: str, act_name: str, elevation_gain_m: Optional[float] = None) -> str:
    """Classify activity into human-friendly categories."""
    km = distance_meters / 1000.0
    elev_str = f" +{int(elevation_gain_m)}m" if (elevation_gain_m and elevation_gain_m > 50) else ""

    is_trail = is_trail_activity(act_type, act_name)

    if is_trail:
        if km >= 42.0:
            return f"🌲 越野超馬 ({km:.1f}k{elev_str})"
        elif km >= 20.0:
            return f"🌲 越野半馬 ({km:.1f}k{elev_str})"
        else:
            return f"🌲 越野跑 ({km:.1f}k{elev_str})"
    
    # Road / General Running
    if 40.0 <= km <= 46.0:
        return f"🏃 全馬 (~42k{elev_str})"
    elif 20.0 <= km <= 23.0:
        return f"🏃 半馬 (~21k{elev_str})"
    elif km > 46.0:
        return f"🏃 超級馬拉松 ({km:.1f}k{elev_str})"
    return f"🏃 路跑 ({km:.1f}k{elev_str})"


def download_single_activity(client: Garmin, output_dir: Path, activity_id_or_url: str):
    """Download GPX track for a specific Garmin activity URL or ID."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract activity ID if full URL is passed
    match = re.search(r'activity/(\d+)', activity_id_or_url)
    if match:
        act_id = match.group(1)
    else:
        act_id = activity_id_or_url.strip()

    console.print(f"[bold cyan]🔍 Fetching activity details for ID: {act_id}...[/bold cyan]")

    try:
        act_details = client.get_activity(act_id)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not fetch metadata ({e}), attempting direct GPX download...[/yellow]")
        act_details = {}

    start_time = act_details.get("summaryDTO", {}).get("startTimeLocal") or act_details.get("startTimeLocal", "")
    date_part = start_time[:10] if start_time else datetime.now().strftime("%Y-%m-%d")
    act_name = sanitize_filename(act_details.get("activityName", f"activity_{act_id}"))

    filename = f"{date_part}_{act_name}.gpx"
    target_path = output_dir / filename

    console.print(f"[bold green]⬇️  Downloading GPX: {filename}[/bold green]")

    try:
        gpx_data = client.download_activity(act_id, dl_fmt=Garmin.ActivityDownloadFormat.GPX)
        if not gpx_data or len(gpx_data) == 0:
            console.print(f"[bold red]❌ No GPX track found for activity {act_id}. This activity might not have GPS coordinates (e.g. indoor/manual).[/bold red]")
            return
        
        with open(target_path, "wb") as f:
            f.write(gpx_data)
        console.print(f"[bold green]✅ Downloaded successfully to: {target_path.resolve()}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to download GPX for activity {act_id}: {e}[/bold red]")


def download_gpx_activities(
    client: Garmin,
    output_dir: Path,
    filter_type: str = "all_gps_runs",
    min_distance_km: float = 0.0,
    limit: int = 1000,
    include_all_sports: bool = False,
    include_treadmill: bool = False,
):
    """Fetch activity list and download GPX tracks."""
    output_dir.mkdir(parents=True, exist_ok=True)

    limit_desc = f"up to {limit}" if limit > 0 else "ALL"
    console.print(f"[bold cyan]🔍 Fetching {limit_desc} activities from Garmin Connect...[/bold cyan]")

    all_activities = []
    batch_size = 50
    start = 0

    while True:
        if limit > 0 and start >= limit:
            break
        current_batch_limit = min(batch_size, limit - start) if limit > 0 else batch_size
        try:
            batch = client.get_activities(start=start, limit=current_batch_limit)
            if not batch:
                break
            all_activities.extend(batch)
            if len(batch) < current_batch_limit:
                break
            start += len(batch)
        except Exception as e:
            console.print(f"[yellow]Warning: Fetching batch failed at offset {start}: {e}[/yellow]")
            break

    console.print(f"[green]Found total {len(all_activities)} activities on account.[/green]")

    # Filter activities
    matched_activities = []
    for act in all_activities:
        act_type = act.get("activityType", {}).get("typeKey", "").lower()
        act_name = act.get("activityName", "")
        dist_m = act.get("distance") or 0.0
        dist_km = dist_m / 1000.0

        # Skip treadmill and indoor activities without GPS tracks
        is_treadmill = (
            "treadmill" in act_type
            or "indoor" in act_type
            or "跑步機" in act_name
            or act.get("hasPolyline") is False
        )
        if not include_treadmill and is_treadmill:
            continue

        is_trail = is_trail_activity(act_type, act_name)
        is_ultra = "ultra" in act_type or "ultra" in act_name.lower() or "超馬" in act_name or dist_km >= 45.0
        is_run = "run" in act_type or "trail" in act_type or is_trail or is_ultra

        # Check sport type
        if not include_all_sports and not is_run:
            continue

        # Check minimum distance filter
        if dist_km < min_distance_km:
            continue

        # Mode filters
        if filter_type == "trail_only":
            if not is_trail:
                continue
        elif filter_type == "marathons_only" and dist_km < 20.0 and not is_ultra:
            continue
        elif filter_type == "full_marathons_only" and dist_km < 40.0:
            continue

        matched_activities.append(act)

    if not matched_activities:
        console.print("[yellow]No activities matched your search criteria.[/yellow]")
        return

    # Display list table
    table = Table(title=f"🎯 Target Activities to Download ({len(matched_activities)})", show_header=True)
    table.add_column("Date", style="cyan", width=12)
    table.add_column("Activity Name", style="white")
    table.add_column("Type", style="dim", width=14)
    table.add_column("Distance", style="green", width=12)
    table.add_column("Elevation Gain", style="yellow", width=14)
    table.add_column("Category", style="bold magenta", width=24)

    for act in matched_activities:
        start_time_local = act.get("startTimeLocal", "")[:10]
        name = act.get("activityName", "Activity")
        act_type = act.get("activityType", {}).get("typeKey", "run")
        dist_m = act.get("distance", 0)
        elev_gain = act.get("elevationGain") or act.get("totalAscent")
        elev_str = f"+{int(elev_gain)} m" if elev_gain is not None else "-"
        category = classify_activity(dist_m, act_type, name, elev_gain)
        table.add_row(start_time_local, name, act_type, f"{dist_m/1000:.2f} km", elev_str, category)

    console.print(table)

    # Download GPX files
    console.print(f"\n[bold green]⬇️  Downloading GPX files to: {output_dir.resolve()}[/bold green]\n")

    downloaded_count = 0
    skipped_count = 0
    failed_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Downloading...", total=len(matched_activities))

        for act in matched_activities:
            act_id = str(act.get("activityId"))
            start_time_str = act.get("startTimeLocal", "")
            
            # Format date as YYYY-MM-DD
            try:
                date_part = start_time_str[:10]
            except Exception:
                date_part = "unknown_date"

            act_name = sanitize_filename(act.get("activityName", "Activity"))
            dist_km = (act.get("distance") or 0) / 1000.0

            # Target filename: YYYY-MM-DD_ActivityName.gpx or YYYY-MM-DD_ActivityName_ID.gpx
            filename = f"{date_part}_{act_name}.gpx"
            target_path = output_dir / filename

            # If file already exists, check if it's the exact same activity ID or append ID
            if target_path.exists():
                # Avoid re-downloading if already present
                skipped_count += 1
                progress.advance(task)
                continue

            progress.update(task, description=f"Downloading {filename}...")

            try:
                # Download GPX bytes
                gpx_data = client.download_activity(
                    act_id,
                    dl_fmt=Garmin.ActivityDownloadFormat.GPX
                )

                if not gpx_data or len(gpx_data) == 0:
                    # Some indoor activities or manual entries have no GPS track
                    failed_count += 1
                else:
                    with open(target_path, "wb") as f:
                        f.write(gpx_data)
                    downloaded_count += 1
            except Exception as e:
                failed_count += 1
                # If error is because no GPS data exists for this activity
                pass

            # Gentle rate limit delay to avoid triggering Garmin API limits
            time.sleep(0.5)
            progress.advance(task)

    console.print(f"\n[bold green]✅ Download Complete![/bold green]")
    console.print(f"  • [green]Downloaded:[/green] {downloaded_count} GPX files")
    console.print(f"  • [yellow]Skipped (already exists):[/yellow] {skipped_count} files")
    if failed_count > 0:
        console.print(f"  • [dim]Skipped / No GPS track:[/dim] {failed_count} activities")
    console.print(f"  • [cyan]Folder location:[/cyan] [link=file:///{output_dir.resolve()}]{output_dir.resolve()}[/link]\n")


def main():
    parser = argparse.ArgumentParser(description="Download GPX tracks for Marathons and GPS running activities from Garmin Connect.")
    parser.add_argument(
        "--mode",
        choices=["all", "marathon", "full_marathon", "trail"],
        default="all",
        help="Filter mode: 'all' (all GPS runs & trail), 'marathon' (>=20km half & full marathons), 'full_marathon' (>=40km full marathons), 'trail' (Trail races & 越野跑 only). Default: all",
    )
    parser.add_argument(
        "--min-km",
        type=float,
        default=0.0,
        help="Minimum distance in kilometers (e.g. --min-km 21.0 or --min-km 42.0)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./marathon_gpx",
        help="Destination directory for GPX files (default: ./marathon_gpx)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Maximum number of activities to search through (default: 500)",
    )
    parser.add_argument(
        "--all-sports",
        action="store_true",
        help="Include all GPS sports (Cycling, Hiking, Walking), not just Running",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="Directly download a specific activity by Garmin Connect URL (e.g. https://connect.garmin.com/app/activity/22482939704)",
    )
    parser.add_argument(
        "--activity-id",
        type=str,
        default=None,
        help="Directly download a specific activity by its ID (e.g. 22482939704)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch ALL historical activities from account without limit",
    )
    parser.add_argument(
        "--include-treadmill",
        action="store_true",
        help="Include treadmill and indoor activities without GPS tracks (default: False)",
    )
    parser.add_argument(
        "--cn",
        action="store_true",
        help="Use Garmin China (garmin.cn) server",
    )

    args = parser.parse_args()

    if args.cn:
        os.environ["GARMIN_IS_CN"] = "true"

    filter_map = {
        "all": "all_gps_runs",
        "marathon": "marathons_only",
        "full_marathon": "full_marathons_only",
        "trail": "trail_only",
    }
    filter_type = filter_map[args.mode]

    client_mgr = GarminClientManager()
    try:
        client = client_mgr.get_client()
    except Exception as e:
        console.print(f"[bold red]Login Error:[/bold red] {e}")
        sys.exit(1)

    out_path = Path(args.output_dir)

    # 1. Single activity direct download
    target_single = args.url or args.activity_id
    if target_single:
        download_single_activity(client, out_path, target_single)
        return

    # 2. Batch download
    fetch_limit = 0 if args.all else args.limit
    download_gpx_activities(
        client=client,
        output_dir=out_path,
        filter_type=filter_type,
        min_distance_km=args.min_km,
        limit=fetch_limit,
        include_all_sports=args.all_sports,
        include_treadmill=args.include_treadmill,
    )


if __name__ == "__main__":
    main()
