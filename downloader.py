#!/usr/bin/env python3
"""
downloader.py — A command-line YouTube video/audio downloader built on yt-dlp.

IMPORTANT: Only download content you own, have explicit permission to
download, or that is licensed for downloading (e.g. Creative Commons,
your own channel's uploads). Downloading copyrighted content without
permission may violate YouTube's Terms of Service and copyright law.

Usage:
    python downloader.py <url>
    python downloader.py <url> --audio-only
    python downloader.py <url> --quality 720p
    python downloader.py <url> --output ~/Downloads
    python downloader.py <playlist_url> --playlist
"""

import argparse
import sys
import os

try:
    import yt_dlp
except ImportError:
    print(
        "Error: yt-dlp is not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


QUALITY_MAP = {
    "best": "bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
}


class DownloadError(Exception):
    """Raised for any user-facing download error."""


def build_ydl_options(args) -> dict:
    output_dir = os.path.expanduser(args.output)
    os.makedirs(output_dir, exist_ok=True)

    outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    opts = {
        "outtmpl": outtmpl,
        "noplaylist": not args.playlist,
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [progress_hook],
    }

    if args.audio_only:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": args.audio_format,
                "preferredquality": "192",
            }
        ]
    else:
        opts["format"] = QUALITY_MAP.get(args.quality, QUALITY_MAP["best"])
        opts["merge_output_format"] = "mp4"

    return opts


def progress_hook(d):
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        sys.stdout.write(f"\r  {pct} downloaded  |  {speed}  |  ETA {eta}   ")
        sys.stdout.flush()
    elif d["status"] == "finished":
        print(f"\n  Finished downloading, now post-processing: {d.get('filename', '')}")


def download(url: str, args) -> None:
    ydl_opts = build_ydl_options(args)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        raise DownloadError(str(e))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="downloader",
        description="Download YouTube videos or audio from the command line (built on yt-dlp). "
                     "Only use for content you have the right to download.",
    )
    parser.add_argument("url", help="YouTube video or playlist URL")
    parser.add_argument(
        "--audio-only", action="store_true", help="Extract audio only (e.g. for music)"
    )
    parser.add_argument(
        "--audio-format",
        default="mp3",
        choices=["mp3", "m4a", "wav", "flac"],
        help="Audio format when using --audio-only (default: mp3)",
    )
    parser.add_argument(
        "--quality",
        default="best",
        choices=list(QUALITY_MAP.keys()),
        help="Max video quality (default: best)",
    )
    parser.add_argument(
        "--output", default="./downloads", help="Output directory (default: ./downloads)"
    )
    parser.add_argument(
        "--playlist", action="store_true", help="Download the entire playlist, not just one video"
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        download(args.url, args)
        print("\nDone.")
        return 0
    except DownloadError as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
