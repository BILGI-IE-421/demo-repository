# Data card

This demo uses one dataset. Your project needs one section like this for **every** dataset you use. Raw files larger than 50 MB are never committed; `scripts/download_data.py` recreates `data/raw/`.

## Dataset 1: NYC taxi trips, March 2019 sample (`taxis.csv`)
- **Source and URL:** seaborn-data repository, https://github.com/mwaskom/seaborn-data (file `taxis.csv`), a sample of the NYC Taxi & Limousine Commission trip records, https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **License:** TLC trip records are public data released by the City of New York; the seaborn-data sample is distributed for teaching.
- **Date accessed:** 9 October 2026
- **Time range and granularity:** 1–31 March 2019, one row per trip
- **Size:** 6,433 rows x 14 columns (raw); see `scripts/preprocess.py` output for the cleaned row count
- **Columns used:** `pickup`, `dropoff` (timestamps), `passengers`, `distance` (miles), `fare`, `tip`, `tolls`, `total` (US dollars), `color` (yellow/green cab), `payment` (credit card/cash), `pickup_zone`, `dropoff_zone`, `pickup_borough`, `dropoff_borough`
- **Known issues:** a few trips have missing zones or boroughs; some rows have zero distance or zero fare; cash tips are not recorded, so `tip` is only meaningful for card payments; the file is a sample, not the full month.
- **Cleaning decisions and why:** timestamps parsed with one explicit format (no day/month ambiguity); rows with missing pickup/drop-off time or borough dropped (cannot be placed in time or space); exact duplicates dropped; zero-distance or zero-fare trips dropped (data-entry artefacts); trips longer than 180 minutes dropped (implausible for a taxi); derived columns `duration_min`, `tip_pct`, `hour`, `date`, `weekday` added for the figures.
- **How to regenerate:** `python scripts/download_data.py && python scripts/preprocess.py`
