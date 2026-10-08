# Electricity mix

Rebuilds the "electricity generation mix" deck (doughnut charts per country, 2021 vs 2026)
from ENTSO-E Transparency Platform data, without manual work in Excel/PowerPoint.

```
data/raw/*.csv            ENTSO-E "Aggregated generation per type" (16.1.B&C) exports
   │  src/prepare_entsoe.py
   ▼
data/processed/monthly_gwh.csv   country, year, month, category, gwh
   │  src/build_deck.py
   ▼
output/electricity_mix.pptx      editable native PowerPoint charts
output/data_checks.md            warnings (missing months, suspicious values…)
```

## Automatic updates

Push a new ENTSO-E file into `data/raw/` (also via the GitHub web UI: *Add file → Upload files*).
The workflow in `.github/workflows/build-deck.yml` rebuilds the deck and commits it to `output/`.
The deck can also be downloaded from the run page (*Actions* tab → artifact `electricity-mix-deck`).

ENTSO-E monthly files are large: compress them as `.zip` before uploading (GitHub rejects files over 100 MB).

## Running locally

```bash
pip install -r requirements.txt
python src/prepare_entsoe.py
python src/build_deck.py --end-months 8 9    # one section for Jan–Aug, one for Jan–Sep
```

Try it without raw data using the sample:

```bash
python src/build_deck.py --data data/sample/monthly_gwh_sample.csv --end-months 8 9
```

`data/sample/monthly_gwh_sample.csv` was reconstructed from the totals in the original deck
(Jan–Aug split evenly over 8 months, September = Jan–Sep minus Jan–Aug): it reproduces the
deck's numbers but the monthly profile is not real.

## Changing things

Everything editable is in `src/config.py`: countries, compared years, colours, the mapping from
ENTSO-E production types to deck categories (e.g. where *Waste* goes), the 5% label threshold.
