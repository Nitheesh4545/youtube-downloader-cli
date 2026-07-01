import sys
import os
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from downloader import build_parser, build_ydl_options, QUALITY_MAP, DownloadError

TEST_DIR = "/tmp/yt_downloader_test_output"

print("=== TEST: parser defaults ===")
parser = build_parser()
args = parser.parse_args(["https://youtube.com/watch?v=abc123"])
assert args.url == "https://youtube.com/watch?v=abc123"
assert args.audio_only is False
assert args.quality == "best"
assert args.output == "./downloads"
assert args.playlist is False
print("OK -", args)

print("=== TEST: audio-only flags ===")
args = parser.parse_args(["URL", "--audio-only", "--audio-format", "flac"])
assert args.audio_only is True
assert args.audio_format == "flac"
print("OK")

print("=== TEST: quality choices ===")
for q in QUALITY_MAP:
    args = parser.parse_args(["URL", "--quality", q])
    assert args.quality == q
print("OK - all quality options accepted:", list(QUALITY_MAP.keys()))

print("=== TEST: invalid quality rejected ===")
try:
    parser.parse_args(["URL", "--quality", "8k"])
    assert False, "should have raised SystemExit"
except SystemExit:
    print("OK - argparse rejects invalid quality")

print("=== TEST: build_ydl_options for video download ===")
args = parser.parse_args(["URL", "--output", TEST_DIR, "--quality", "720p"])
opts = build_ydl_options(args)
assert opts["format"] == QUALITY_MAP["720p"]
assert opts["noplaylist"] is True
assert os.path.isdir(TEST_DIR)
print("OK -", {k: v for k, v in opts.items() if k != "progress_hooks"})

print("=== TEST: build_ydl_options for audio-only download ===")
args = parser.parse_args(["URL", "--audio-only", "--audio-format", "mp3", "--output", TEST_DIR])
opts = build_ydl_options(args)
assert opts["format"] == "bestaudio/best"
assert opts["postprocessors"][0]["preferredcodec"] == "mp3"
print("OK -", {k: v for k, v in opts.items() if k != "progress_hooks"})

print("=== TEST: playlist flag toggles noplaylist ===")
args = parser.parse_args(["URL", "--playlist", "--output", TEST_DIR])
opts = build_ydl_options(args)
assert opts["noplaylist"] is False
print("OK - noplaylist =", opts["noplaylist"])

print("=== TEST: output directory auto-created ===")
fresh_dir = "/tmp/yt_downloader_fresh_dir"
if os.path.exists(fresh_dir):
    shutil.rmtree(fresh_dir)
args = parser.parse_args(["URL", "--output", fresh_dir])
build_ydl_options(args)
assert os.path.isdir(fresh_dir)
print("OK - directory created at", fresh_dir)

# cleanup
shutil.rmtree(TEST_DIR, ignore_errors=True)
shutil.rmtree(fresh_dir, ignore_errors=True)

print("\nAll tests passed.")
