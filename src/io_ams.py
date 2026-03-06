from pathlib import Path
import pandas as pd


from pathlib import Path
import pandas as pd


def read_table(path: Path) -> pd.DataFrame:
    """
    Robust reader:
    - If .csv -> comma-separated by default
    - If .ams -> semicolon + '#' comments by default
    - Fallbacks included
    """
    suffix = path.suffix.lower()

    if suffix == ".csv":
        # sample data is comma-separated
        return pd.read_csv(path, sep=",", header=0)

    # default for .ams-like
    try:
        return pd.read_csv(path, sep=";", comment="#", header=0)
    except Exception:
        return pd.read_csv(path, sep=",", header=0)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
