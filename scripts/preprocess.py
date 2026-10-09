"""Clean the raw taxi data and write data/taxis_clean.csv.

Run from the repository root after download_data.py:
    python scripts/preprocess.py

Every cleaning decision here is documented in data/README.md.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "taxis.csv"
OUT = ROOT / "data" / "taxis_clean.csv"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # one format, one place: no dayfirst ambiguity


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in ("pickup", "dropoff"):
        df[col] = pd.to_datetime(df[col], format=DATE_FORMAT, errors="coerce")
    return df


def main() -> None:
    df = pd.read_csv(RAW)
    n_in = len(df)

    df = parse_dates(df)
    df = df.dropna(subset=["pickup", "dropoff", "pickup_borough", "dropoff_borough"])
    df = df.drop_duplicates()
    df = df[(df["distance"] > 0) & (df["fare"] > 0)]

    df["duration_min"] = (df["dropoff"] - df["pickup"]).dt.total_seconds() / 60
    df = df[(df["duration_min"] > 0) & (df["duration_min"] < 180)]

    df["tip_pct"] = 100 * df["tip"] / df["fare"]
    df["hour"] = df["pickup"].dt.hour
    df["date"] = df["pickup"].dt.date
    df["weekday"] = df["pickup"].dt.day_name()

    df.to_csv(OUT, index=False)
    print(f"{n_in} rows in, {len(df)} rows out -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
