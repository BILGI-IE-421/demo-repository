# IE 421 - Data Science for Engineers Term Project (Please keep this main title in Readme as it is)

## Your Project Title Goes Here
Project abstract. Should be around 180-200 words. No visuals here.

## Student Names
Please fill this area with your names and student IDs.

## Files (Explain each of them with a sentence)
- `data/README.md`: the data card, one section per dataset (source, license, range, columns, issues, cleaning decisions).
- `data/taxis_clean.csv`: the cleaned dataset produced by `scripts/preprocess.py`. Raw downloads live in `data/raw/` and are not committed.
- `scripts/download_data.py`: downloads the raw data into `data/raw/`.
- `scripts/preprocess.py`: parses dates, removes bad rows, adds derived columns, writes `data/taxis_clean.csv`.
- `scripts/figures.py`: produces every figure in `visuals/`.
- `visuals/`: `fig1`–`fig5` static PNG figures and `interactive_hourly.html` (plotly).
- `index.html` and `css/style.css`: the GitHub Pages site with the data story.
- `requirements.html`: the project guidelines (themes, milestones, rubric).
- `PROPOSAL.md`, `AI_USAGE.md`: templates to fill in (milestone 1 and the AI usage statement).
- `requirements.txt`: Python libraries; `.github/workflows/structure-check.yml`: the automatic repository check.

## How to run (from the repository root)
```
pip install -r requirements.txt
python scripts/download_data.py
python scripts/preprocess.py
python scripts/figures.py
```

## Key findings
1. Half of all trips cost $10 or less; a long tail of airport and long-distance rides runs past $100.
2. The fare is a straight line in distance; cash riders cluster below three miles.
3. Only 4% of Manhattan card trips record no tip, against 51% in Brooklyn and 93% in the Bronx; riders who tip give 22–27% everywhere.

## Hosting
The project is hosted using GitHub Pages (https://bilgi-ie-421.github.io/demo-repository).
Your page should be available as (https://bilgi-ie-421.github.io/ie421-2026-2027-1-termproject-yourteamname)
