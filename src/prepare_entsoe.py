"""Turn raw ENTSO-E "Aggregated generation per type" files into a monthly table.

Reads every .csv / .tsv / .zip in data/raw/ and writes
data/processed/monthly_gwh.csv with columns: country, year, month, category, gwh.

Usage:  python src/prepare_entsoe.py [--raw data/raw] [--out data/processed/monthly_gwh.csv]
"""
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

from config import COUNTRIES, PRODUCTION_TYPE_MAP

# ENTSO-E has renamed columns between exports; accept the known variants.
COLUMN_ALIASES = {
    "datetime": ["DateTime(UTC)", "DateTime", "MTU (UTC)"],
    "resolution": ["ResolutionCode"],
    "area_type": ["AreaTypeCode"],
    "map_code": ["MapCode"],
    "production_type": ["ProductionType", "Production Type"],
    "mw": ["ActualGenerationOutput(MW)", "ActualGenerationOutput", "Actual Generation Output (MW)"],
}

HOURS_PER_INTERVAL = {"PT15M": 0.25, "PT30M": 0.5, "PT60M": 1.0}


def read_raw_file(path: Path) -> pd.DataFrame:
    sep = "," if path.suffix == ".csv" and _looks_comma_separated(path) else "\t"
    df = pd.read_csv(path, sep=sep, low_memory=False)
    rename = {}
    for std, variants in COLUMN_ALIASES.items():
        found = next((c for c in variants if c in df.columns), None)
        if found is None and std != "area_type":
            sys.exit(f"{path.name}: no column for '{std}' (looked for {variants}).\n"
                     f"Columns found: {list(df.columns)}")
        if found:
            rename[found] = std
    return df.rename(columns=rename)[list(rename.values())]


def _looks_comma_separated(path: Path) -> bool:
    with open(path, encoding="utf-8-sig") as f:
        header = f.readline()
    return header.count(",") > header.count("\t")


def to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    if "area_type" in df.columns:
        df = df[df["area_type"] == "CTY"]
    df = df[df["map_code"].isin(COUNTRIES)]

    unknown = set(df["production_type"].unique()) - set(PRODUCTION_TYPE_MAP)
    if unknown:
        sys.exit(f"Unmapped production types: {sorted(unknown)} -> add them to config.py")

    df = df.assign(category=df["production_type"].map(PRODUCTION_TYPE_MAP)).dropna(subset=["category"])
    hours = df["resolution"].map(HOURS_PER_INTERVAL)
    if hours.isna().any():
        sys.exit(f"Unknown resolutions: {sorted(df.loc[hours.isna(), 'resolution'].unique())}")

    ts = pd.to_datetime(df["datetime"], utc=True)
    out = pd.DataFrame({
        "country": df["map_code"],
        "year": ts.dt.year,
        "month": ts.dt.month,
        "category": df["category"],
        "gwh": pd.to_numeric(df["mw"], errors="coerce").fillna(0) * hours / 1000,
    })
    return out.groupby(["country", "year", "month", "category"], as_index=False)["gwh"].sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--out", default="data/processed/monthly_gwh.csv")
    args = ap.parse_args()

    files = sorted(p for p in Path(args.raw).iterdir() if re.search(r"\.(csv|tsv|zip)$", p.name))
    if not files:
        sys.exit(f"No raw files in {args.raw}/")

    monthly = pd.concat([to_monthly(read_raw_file(f)) for f in files])
    # The same month can appear in two files (e.g. re-downloads): keep the latest file's value
    monthly = monthly.groupby(["country", "year", "month", "category"], as_index=False).last()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    monthly.round(3).to_csv(args.out, index=False)
    print(f"Wrote {args.out}: {len(monthly)} rows from {len(files)} file(s)")


if __name__ == "__main__":
    main()
