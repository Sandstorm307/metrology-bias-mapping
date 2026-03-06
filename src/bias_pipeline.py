from dataclasses import dataclass
from pathlib import Path
import pandas as pd

from .io_ams import read_table, write_csv
from .lot_report import parse_lot_report, enrich_with_lot


@dataclass
class PipelineOutputs:
    bias_csv: Path


def load_extraction_measurement(input_dir: Path, prefix: str) -> pd.DataFrame:
    extraction = read_table(input_dir / f"{prefix}_extraction.csv")
    measurement = read_table(input_dir / f"{prefix}_measurement.csv")

    if "EXTRACTION_ID" not in extraction.columns or "EXTRACTION_ID" not in measurement.columns:
        raise ValueError("extraction and measurement must include EXTRACTION_ID")

    return extraction.merge(measurement, on="EXTRACTION_ID", how="inner")


def compute_bias(input_dir: Path) -> pd.DataFrame:
    df_etch = load_extraction_measurement(input_dir, "etch")
    df_ph = load_extraction_measurement(input_dir, "ph")
    lot = parse_lot_report(input_dir / "lot_report.csv")

    df_etch = enrich_with_lot(df_etch, lot)
    df_ph = enrich_with_lot(df_ph, lot)

    if "MEASUREMENT_VALUE" not in df_etch.columns or "MEASUREMENT_VALUE" not in df_ph.columns:
        raise ValueError("measurement tables must include MEASUREMENT_VALUE")

    keys = ["SITE_ID", "EXTRACTION_ID", "DOSE", "FOCUS", "DIE_ROW", "DIE_COL", "DIE_ID"]
    merged = df_etch.merge(df_ph, on=keys, how="inner", suffixes=("_ETCH", "_PH"))

    merged["BIAS"] = merged["MEASUREMENT_VALUE_ETCH"] - merged["MEASUREMENT_VALUE_PH"]

    keep = keys + ["MEASUREMENT_VALUE_ETCH", "MEASUREMENT_VALUE_PH", "BIAS"]
    return merged[keep].dropna(subset=["BIAS"])


def run_pipeline(input_dir: Path, output_dir: Path) -> PipelineOutputs:
    bias_df = compute_bias(input_dir)
    out_csv = output_dir / "bias_results.csv"
    write_csv(bias_df, out_csv)
    return PipelineOutputs(bias_csv=out_csv)
