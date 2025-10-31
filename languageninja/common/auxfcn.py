import subprocess
from pathlib import Path

def aiff_to_mp3(aiff_path: Path, mp3_path: Path, bitrate_kbps=64):
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    # -ac 1 mono, -ar 22050 Hz, -b:a 64k CBR MP3
    cmd = [
        "ffmpeg", "-y",
        "-i", str(aiff_path),
        "-ac", "1",
        "-ar", "22050",
        "-c:a", "libmp3lame",
        "-b:a", f"{bitrate_kbps}k",
        str(mp3_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Batch convert all .aiff files in input folder recursively to .mp3
def batch_convert_aiff_to_mp3(input_folder: Path):
    for aiff in input_folder.rglob("*.aiff"):
        print(f"Converting {aiff} ...")
        mp3 = aiff.with_suffix(".mp3")
        if not mp3.exists():
            aiff_to_mp3(aiff, mp3, bitrate_kbps=64)

# Execute as main
if __name__ == "__main__":
    input_dir = Path("data/audio")
    batch_convert_aiff_to_mp3(input_dir)