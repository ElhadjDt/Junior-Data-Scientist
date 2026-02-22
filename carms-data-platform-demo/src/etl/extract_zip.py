from pathlib import Path
import zipfile

# Paths relative to the project root (carms-data-platform-demo/)
RAW_DIR = Path("../data/raw")
EXTRACTED_DIR = Path("../data/extracted")

def extract_raw_zip():
    """
    Extract all ZIP files from ../data/raw into ../data/extracted.
    Assumes directories already exist.
    """
    zip_files = list(RAW_DIR.glob("*.zip"))

    if not zip_files:
        print("No ZIP files found in ../data/raw.")
        return

    for zip_path in zip_files:
        print(f"Processing ZIP: {zip_path.name}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACTED_DIR)
        print(f"Extracted into: {EXTRACTED_DIR}")

    print("All ZIP files extracted.")


if __name__ == "__main__":
    extract_raw_zip()