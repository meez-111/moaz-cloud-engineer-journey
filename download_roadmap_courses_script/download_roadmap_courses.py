#!/usr/bin/env python3
"""
Enterprise YouTube Course Downloader – Cloud Engineering Roadmap
Features:
- Manual cookies.txt support (--cookies)
- iOS client to bypass bot detection
- Parallel downloads (ThreadPoolExecutor)
- Global registry → never re-download
- Resume partial downloads
- Exponential backoff retry
- Interactive phase selection

Usage:
    python download_roadmap_courses.py [roadmap.md] --cookies cookies.txt [--parallel N] [--output DIR]
"""

import os
import re
import sys
import time
import json
import argparse
import hashlib
import threading
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from urllib.error import URLError
from concurrent.futures import ThreadPoolExecutor, as_completed

import yt_dlp

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
DEFAULT_PARALLEL = 4
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds, doubles each retry
REGISTRY_FILE = "download_registry.json"

registry_lock = threading.Lock()


# ----------------------------------------------------------------------
# Colour helpers (optional, works on most terminals)
# ----------------------------------------------------------------------
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def colored(text: str, color: str) -> str:
    if os.name == "nt":
        return text
    return f"{color}{text}{Colors.ENDC}"


# ----------------------------------------------------------------------
# 1. Markdown Parsing
# ----------------------------------------------------------------------
def extract_phase_title(line: str) -> Optional[str]:
    match = re.match(r"^###\s+Phase\s+\d+:\s*(.+)$", line.strip())
    return match.group(1).strip() if match else None


def extract_youtube_links(content: str) -> List[Tuple[str, str]]:
    pattern = r"\[([^\]]+)\]\((https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^\s\)]+)\)"
    return re.findall(pattern, content)


def parse_roadmap(filepath: str) -> Dict[str, Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    phases = {}
    current_phase = None
    current_content = []

    for line in content.splitlines():
        phase_title = extract_phase_title(line)
        if phase_title:
            if current_phase is not None:
                phases[current_phase] = {
                    "courses": extract_youtube_links("\n".join(current_content)),
                    "folder_name": re.sub(r"[^\w\s-]", "", current_phase)
                    .strip()
                    .replace(" ", "_"),
                }
            current_phase = phase_title
            current_content = []
        else:
            current_content.append(line)

    if current_phase is not None:
        phases[current_phase] = {
            "courses": extract_youtube_links("\n".join(current_content)),
            "folder_name": re.sub(r"[^\w\s-]", "", current_phase)
            .strip()
            .replace(" ", "_"),
        }

    return phases


# ----------------------------------------------------------------------
# 2. Registry Management (Thread‑safe)
# ----------------------------------------------------------------------
def load_registry() -> Dict[str, Any]:
    if Path(REGISTRY_FILE).exists():
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_registry(registry: Dict[str, Any]) -> None:
    with registry_lock:
        temp_file = REGISTRY_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        os.replace(temp_file, REGISTRY_FILE)


def get_course_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def is_course_completed(
    registry: Dict[str, Any], course_id: str, output_dir: Path
) -> bool:
    if course_id not in registry:
        return False
    entry = registry[course_id]
    if entry.get("status") != "completed":
        return False
    if not output_dir.exists():
        return False
    if entry.get("type") == "playlist":
        archive_file = output_dir / f".archive_{entry['playlist_name']}.txt"
        if not archive_file.exists():
            return False
        with open(archive_file, "r") as f:
            downloaded_count = sum(1 for _ in f)
        expected_count = entry.get("total_videos", 0)
        if downloaded_count < expected_count:
            return False
    else:
        safe_title = entry.get("safe_title", "")
        if not safe_title:
            return False
        files = list(output_dir.glob(f"{safe_title}.*"))
        if not files:
            return False
    return True


def mark_course_completed(
    registry: Dict[str, Any], course_id: str, course_info: Dict[str, Any]
) -> None:
    with registry_lock:
        registry[course_id] = {
            **course_info,
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
        }
        save_registry(registry)


def mark_course_failed(
    registry: Dict[str, Any], course_id: str, course_info: Dict[str, Any], error: str
) -> None:
    with registry_lock:
        registry[course_id] = {
            **course_info,
            "status": "failed",
            "error": error,
            "last_attempt": datetime.now().isoformat(),
        }
        save_registry(registry)


# ----------------------------------------------------------------------
# 3. Download Functions (with iOS client workaround)
# ----------------------------------------------------------------------
def download_playlist(
    url: str, output_dir: Path, playlist_name: str, cookie_args: List[str]
) -> Tuple[bool, str, int]:
    """
    Download a playlist. Returns (success, message, total_videos).
    """
    archive_file = (
        output_dir / f".archive_{re.sub(r'[^\w\-_\.]', '_', playlist_name)}.txt"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    def get_playlist_info():
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        }
        for key, val in zip(["cookies", "cookies_from_browser"], cookie_args):
            if val:
                ydl_opts[key] = val
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            entries = info.get("entries", [])
            videos = [
                {"id": e.get("id"), "title": e.get("title", e.get("id"))}
                for e in entries
                if e
            ]
            return videos, info.get("title", playlist_name)

    try:
        videos, real_title = get_playlist_info()
        total_videos = len(videos)
    except Exception as e:
        return False, f"Failed to fetch playlist: {e}", 0

    downloaded_ids = set()
    if archive_file.exists():
        with open(archive_file, "r") as f:
            downloaded_ids = {line.strip().split()[1] for line in f if line.strip()}

    done = len(downloaded_ids)
    pending = total_videos - done
    if pending == 0:
        return (
            True,
            f"Already fully downloaded ({total_videos}/{total_videos} videos)",
            total_videos,
        )

    ydl_opts = {
        "outtmpl": str(output_dir / "%(playlist_index)02d - %(title)s.%(ext)s"),
        "download_archive": str(archive_file),
        "ignoreerrors": True,
        "nooverwrites": True,
        "continuedl": True,
        "quiet": True,
        "no_warnings": True,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "retries": MAX_RETRIES,
        "fragment_retries": MAX_RETRIES,
        "retry_sleep": lambda n: RETRY_DELAY * (2 ** (n - 1)),
        # ---- iOS client workaround ----
        "extractor_args": {
            "youtube": {
                "player_client": ["ios"],
                "skip": ["hls", "dash"],
            }
        },
        "sleep_interval": 5,
        "max_sleep_interval": 15,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    }
    for key, val in zip(["cookies", "cookies_from_browser"], cookie_args):
        if val:
            ydl_opts[key] = val

    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            break
        except (yt_dlp.utils.DownloadError, URLError, ConnectionError) as e:
            attempt += 1
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * (2 ** (attempt - 1))
                time.sleep(wait)
            else:
                return False, f"Failed after {MAX_RETRIES} attempts: {e}", total_videos

    with open(archive_file, "r") as f:
        final_downloaded = {line.strip().split()[1] for line in f if line.strip()}
    missing = [v for v in videos if v["id"] not in final_downloaded]
    if missing:
        return False, f"Missing {len(missing)} videos after download", total_videos
    return True, f"Successfully downloaded all {total_videos} videos", total_videos


def download_single_video(
    url: str, output_dir: Path, video_title: str, cookie_args: List[str]
) -> Tuple[bool, str]:
    """
    Download a single video. Returns (success, message).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_title = re.sub(r"[^\w\s-]", "", video_title).strip().replace(" ", "_")
    outtmpl = str(output_dir / f"{safe_title}.%(ext)s")

    if list(output_dir.glob(f"{safe_title}.*")):
        return True, f"Already downloaded: {safe_title}"

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "retries": MAX_RETRIES,
        "fragment_retries": MAX_RETRIES,
        "retry_sleep": lambda n: RETRY_DELAY * (2 ** (n - 1)),
        "nooverwrites": True,
        "continuedl": True,
        # ---- iOS client workaround ----
        "extractor_args": {
            "youtube": {
                "player_client": ["ios"],
                "skip": ["hls", "dash"],
            }
        },
        "sleep_interval": 5,
        "max_sleep_interval": 15,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    }
    for key, val in zip(["cookies", "cookies_from_browser"], cookie_args):
        if val:
            ydl_opts[key] = val

    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True, f"Downloaded: {safe_title}"
        except Exception as e:
            attempt += 1
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * (2 ** (attempt - 1))
                time.sleep(wait)
            else:
                return False, f"Failed: {e}"
    return False, "Unknown error"


def is_playlist_url(url: str) -> bool:
    return "playlist" in url or "&list=" in url or "?list=" in url


# ----------------------------------------------------------------------
# 4. Task Wrapper for Parallel Execution
# ----------------------------------------------------------------------
def process_course(
    course_info: Dict[str, Any],
    cookie_args: List[str],
    registry: Dict[str, Any],
    force: bool,
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Process a single course (playlist or single video) and update registry.
    Returns (success, message, updated_course_info).
    """
    url = course_info["url"]
    course_id = get_course_id(url)
    course_type = course_info["type"]
    output_dir = (
        Path(course_info["output_subdir"])
        if course_type == "playlist"
        else Path(course_info["output_path"])
    )
    link_text = course_info["link_text"]

    if not force and is_course_completed(registry, course_id, output_dir):
        return True, "Already completed", course_info

    if course_type == "playlist":
        safe_name = (
            re.sub(r"[^\w\s-]", "", link_text).strip().replace(" ", "_") or "playlist"
        )
        success, msg, total_vids = download_playlist(
            url, output_dir, safe_name, cookie_args
        )
        course_info["total_videos"] = total_vids
        if success:
            mark_course_completed(registry, course_id, course_info)
        else:
            mark_course_failed(registry, course_id, course_info, msg)
        return success, msg, course_info
    else:
        success, msg = download_single_video(url, output_dir, link_text, cookie_args)
        if success:
            mark_course_completed(registry, course_id, course_info)
        else:
            mark_course_failed(registry, course_id, course_info, msg)
        return success, msg, course_info


# ----------------------------------------------------------------------
# 5. User Interaction & Main
# ----------------------------------------------------------------------
def get_phases_to_download(all_phases: List[str]) -> List[str]:
    print("\nAvailable phases:")
    for i, phase in enumerate(all_phases, 1):
        print(f"  {i:2d}. {phase}")

    choice = (
        input("\nEnter phase numbers to download (e.g., 1,3,5-8 or 'all'): ")
        .strip()
        .lower()
    )
    if choice == "all":
        return all_phases

    selected = set()
    for part in choice.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            try:
                selected.update(range(int(start), int(end) + 1))
            except ValueError:
                print(f"Invalid range: {part}")
        else:
            try:
                selected.add(int(part))
            except ValueError:
                print(f"Invalid number: {part}")

    return [all_phases[i - 1] for i in sorted(selected) if 1 <= i <= len(all_phases)]


def main():
    parser = argparse.ArgumentParser(description="Pro YouTube Course Downloader")
    parser.add_argument(
        "roadmap_file", nargs="?", default="Cloud Engineering Roadmap 170 days.md"
    )
    parser.add_argument(
        "--output", "-o", default=r"D:\courses", help="Output directory"
    )
    parser.add_argument(
        "--parallel",
        "-p",
        type=int,
        default=DEFAULT_PARALLEL,
        help=f"Parallel downloads (default: {DEFAULT_PARALLEL})",
    )
    parser.add_argument(
        "--cookies", "-c", help="Path to cookies.txt file (strongly recommended)"
    )
    parser.add_argument(
        "--force", action="store_true", help="Ignore registry and force re-download"
    )
    args = parser.parse_args()

    if not os.path.exists(args.roadmap_file):
        print(f"{colored('❌ File not found:', Colors.FAIL)} {args.roadmap_file}")
        sys.exit(1)

    print(f"{colored('📘 Parsing roadmap:', Colors.OKBLUE)} {args.roadmap_file}")
    phases_data = parse_roadmap(args.roadmap_file)

    if not phases_data:
        print("No phases found.")
        sys.exit(1)

    all_titles = list(phases_data.keys())
    selected_titles = get_phases_to_download(all_titles)

    if not selected_titles:
        print("No phases selected. Exiting.")
        return

    base_output = Path(args.output)
    base_output.mkdir(parents=True, exist_ok=True)
    print(
        f"\n{colored('📁 Output directory:', Colors.OKBLUE)} {base_output.absolute()}"
    )
    print(f"{colored('⚡ Parallel downloads:', Colors.OKCYAN)} {args.parallel}")

    # ---- Cookie Handling ----
    if args.cookies:
        if os.path.exists(args.cookies):
            cookie_args = ["--cookies", args.cookies]
            print(
                f"{colored('🍪 Using manual cookies file:', Colors.OKGREEN)} {args.cookies}"
            )
        else:
            print(
                f"{colored('❌ Cookies file not found:', Colors.FAIL)} {args.cookies}"
            )
            sys.exit(1)
    else:
        print(
            "\n🔐 No cookies file provided. Provide one with --cookies to avoid bot errors."
        )
        choice = input("Use browser cookies instead? (y/n) [n]: ").strip().lower()
        if choice == "y":
            browser = (
                input("Browser (chrome/firefox/edge) [firefox]: ").strip() or "firefox"
            )
            cookie_args = ["--cookies-from-browser", browser]
        else:
            print(
                f"{colored('⚠️  Proceeding without cookies. Downloads may fail.', Colors.WARNING)}"
            )
            cookie_args = []

    registry = load_registry() if not args.force else {}
    if args.force:
        print(f"{colored('⚠️  Force mode: registry ignored.', Colors.WARNING)}")

    # Build list of tasks
    tasks = []
    for phase_title in selected_titles:
        phase_info = phases_data[phase_title]
        phase_folder = base_output / phase_info["folder_name"]
        phase_folder.mkdir(exist_ok=True)

        for link_text, url in phase_info["courses"]:
            course_type = "playlist" if is_playlist_url(url) else "single"
            course_info = {
                "url": url,
                "link_text": link_text,
                "type": course_type,
                "phase": phase_title,
                "output_path": str(phase_folder),
            }
            if course_type == "playlist":
                safe_name = (
                    re.sub(r"[^\w\s-]", "", link_text).strip().replace(" ", "_")
                    or "playlist"
                )
                course_info["output_subdir"] = str(phase_folder / safe_name)
                course_info["playlist_name"] = safe_name
            else:
                course_info["safe_title"] = (
                    re.sub(r"[^\w\s-]", "", link_text).strip().replace(" ", "_")
                )
            tasks.append(course_info)

    if not tasks:
        print("No courses found in selected phases.")
        return

    print(f"\n{colored('🚀 Starting parallel downloads...', Colors.OKGREEN)}")
    print(f"   Total courses to process: {len(tasks)}\n")

    completed_count = 0
    failed_count = 0
    skipped_count = 0

    with ThreadPoolExecutor(max_workers=args.parallel) as executor:
        future_to_task = {
            executor.submit(
                process_course, task, cookie_args, registry, args.force
            ): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                success, msg, updated_info = future.result()
                status_icon = (
                    colored("✅", Colors.OKGREEN)
                    if success
                    else colored("❌", Colors.FAIL)
                )
                if "Already completed" in msg:
                    skipped_count += 1
                    status_icon = colored("⏭️", Colors.OKCYAN)
                elif success:
                    completed_count += 1
                else:
                    failed_count += 1

                phase_short = (
                    task["phase"][:30] + "..."
                    if len(task["phase"]) > 30
                    else task["phase"]
                )
                print(f"{status_icon} [{phase_short}] {task['link_text'][:50]} - {msg}")
            except Exception as e:
                failed_count += 1
                print(
                    f"{colored('❌', Colors.FAIL)} {task['link_text'][:50]} - Exception: {e}"
                )

    # Summary
    print("\n" + "=" * 60)
    print(f"{colored('🎉 SUMMARY', Colors.BOLD)}")
    print(f"   Total courses: {len(tasks)}")
    print(f"   {colored('✅ Completed:', Colors.OKGREEN)} {completed_count}")
    print(f"   {colored('⏭️  Skipped (already done):', Colors.OKCYAN)} {skipped_count}")
    if failed_count > 0:
        print(f"   {colored('❌ Failed:', Colors.FAIL)} {failed_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
