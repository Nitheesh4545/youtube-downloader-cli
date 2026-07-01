# YouTube Downloader (CLI)

A command-line tool for downloading YouTube videos or extracting audio,
built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## ⚠️ Before you use this

Only download content you **own**, have **explicit permission** to download,
or that is **licensed for downloading** (e.g. Creative Commons, your own
channel's uploads, videos with a "download" option enabled by the creator).
Downloading copyrighted content without permission can violate YouTube's
Terms of Service and copyright law, depending on your jurisdiction and use
case. This tool is provided for legitimate personal use (backups, offline
access to your own content, archiving permitted material) — you're
responsible for how you use it.

## Setup

```bash
pip install -r requirements.txt
```

Audio extraction (`--audio-only`) requires **ffmpeg** to be installed and on
your PATH:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# https://ffmpeg.org/download.html
```

## Usage

```bash
# Download a video at the best available quality
python downloader.py "https://youtube.com/watch?v=VIDEO_ID"

# Cap the quality (useful for saving space/bandwidth)
python downloader.py "URL" --quality 720p

# Extract audio only (e.g. for music)
python downloader.py "URL" --audio-only
python downloader.py "URL" --audio-only --audio-format flac

# Download an entire playlist
python downloader.py "PLAYLIST_URL" --playlist

# Choose an output folder
python downloader.py "URL" --output ~/Videos
```

### Options

| Flag | Description |
|---|---|
| `url` | YouTube video or playlist URL (required) |
| `--audio-only` | Extract audio instead of downloading video |
| `--audio-format` | `mp3` (default), `m4a`, `wav`, or `flac` |
| `--quality` | `best` (default), `1080p`, `720p`, `480p`, `360p` |
| `--output` | Output directory (default: `./downloads`) |
| `--playlist` | Download the full playlist instead of a single video |

## Tests

```bash
python test_downloader.py
```

Covers CLI argument parsing, quality-map validation, download-option
building for both video and audio-only modes, playlist toggling, and
output-directory auto-creation. (Actual network downloads aren't part of
the automated tests since they depend on live YouTube access — the tests
verify all the logic that decides *what* yt-dlp will be told to do.)

## Possible extensions

- Subtitle download support (`--subs`)
- Resume interrupted downloads
- A simple progress bar UI instead of plain percentage text
- Batch mode: read a list of URLs from a file

THX-JUN2626-298
