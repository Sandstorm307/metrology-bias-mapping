from pathlib import Path
import numpy as np
import pandas as pd


def make_sample(dir_path: Path, n: int = 250, seed: int = 7) -> None:
    rng = np.random.default_rng(seed)
    dir_path.mkdir(parents=True, exist_ok=True)

    extraction_id = np.arange(1, n + 1)
    die_row = rng.integers(0, 20, size=n)
    die_col = rng.integers(0, 20, size=n)
    die_id = (die_col * 100 + die_row).astype(int)
    site_id = rng.integers(1, 10, size=n)

    focus = rng.normal(0, 60, size=n)
    dose = rng.normal(0, 1.0, size=n)

    extraction = pd.DataFrame({
        "EXTRACTION_ID": extraction_id,
        "DIE_ROW": die_row,
        "DIE_COL": die_col,
    })

    meas_ph = 100 + 0.25 * focus + 1.2 * dose + rng.normal(0, 2.0, size=n)
    meas_etch = meas_ph + rng.normal(0.6, 1.0, size=n)

    measurement_ph = pd.DataFrame({"EXTRACTION_ID": extraction_id, "MEASUREMENT_VALUE": meas_ph})
    measurement_etch = pd.DataFrame({"EXTRACTION_ID": extraction_id, "MEASUREMENT_VALUE": meas_etch})

    lot_report = pd.DataFrame({
        "EXTRACTION_ID": extraction_id,
        "SITE_ID": site_id,
        "DOSE": dose,
        "FOCUS": focus,
        "DIE_ROW": die_row,
        "DIE_COL": die_col,
        "DIE_ID": die_id,
    })

    # create a data/sample folder inside project
    extraction.to_csv(dir_path / "ph_extraction.csv", index=False)
    measurement_ph.to_csv(dir_path / "ph_measurement.csv", index=False)
    extraction.to_csv(dir_path / "etch_extraction.csv", index=False)
    measurement_etch.to_csv(dir_path / "etch_measurement.csv", index=False)
    lot_report.to_csv(dir_path / "lot_report.csv", index=False)


if __name__ == "__main__":
    make_sample(Path("data/sample"))
    print("✅ Sample data created in data/sample/")
