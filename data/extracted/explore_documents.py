import pandas as pd
from pathlib import Path

DATA_DIR = Path(".")

def explore():
    json_files = list(DATA_DIR.glob("*program_descriptions*.json"))
    csv_files = list(DATA_DIR.glob("*program_descriptions*.csv"))

    print("\n=== JSON FILES FOUND ===")
    for f in json_files:
        print(" -", f.name)

    print("\n=== CSV FILES FOUND ===")
    for f in csv_files:
        print(" -", f.name)

    # Explore JSON
    for f in json_files:
        print(f"\n\n===== Exploring JSON: {f.name} =====")
        df = pd.read_json(f)
        print(df.head())
        print("\nColumns:", df.columns.tolist())

    # Explore CSV
    for f in csv_files:
        print(f"\n\n===== Exploring CSV: {f.name} =====")
        df = pd.read_csv(f)
        print(df.head())
        print("\nColumns:", df.columns.tolist())


if __name__ == "__main__":
    explore()