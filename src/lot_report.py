from pathlib import Path
import pandas as pd


REQUIRED_LOT_COLS = {
    "EXTRACTION_ID",
    "SITE_ID",
    "DOSE",
    "FOCUS",
    "DIE_ROW",
    "DIE_COL",
    "DIE_ID",
}


def parse_lot_report(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_LOT_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Lot report missing columns: {sorted(missing)}")
    return df


def enrich_with_lot(df: pd.DataFrame, lot: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich df with lot metadata on EXTRACTION_ID.
    Avoid duplicate columns (DIE_ROW, DIE_COL, etc.) causing _x/_y suffixes.
    """
    if "EXTRACTION_ID" not in df.columns:
        raise ValueError("Input must contain EXTRACTION_ID")

    # Keep only columns that are not already in df (except EXTRACTION_ID)
    cols_to_add = ["EXTRACTION_ID"] + [c for c in lot.columns if c not in df.columns and c != "EXTRACTION_ID"]
    lot_clean = lot[cols_to_add].copy()

    return df.merge(lot_clean, on="EXTRACTION_ID", how="left")
