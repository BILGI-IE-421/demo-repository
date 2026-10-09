"""Download the raw dataset into data/raw/.

Run from the repository root:
    python scripts/download_data.py

Raw files are not committed (see .gitignore); this script recreates them.
"""
from pathlib import Path

import requests

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / "taxis.csv"
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    target.write_bytes(response.content)
    print(f"saved {target.relative_to(ROOT)} ({len(response.content) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
