from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import plotly.graph_objs as go
import plotly.offline as pyo


def plot_bias_maps(
    bias_csv: Path,
    output_dir: Path,
    grid_n: int = 90,
    min_points: int = 6,
) -> None:
    df = pd.read_csv(bias_csv)
    req = {"SITE_ID", "FOCUS", "MEASUREMENT_VALUE_PH", "BIAS"}
    missing = req - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in bias_results.csv: {sorted(missing)}")

    out3d = output_dir / "plots_3d"
    out2d = output_dir / "plots_2d"
    out3d.mkdir(parents=True, exist_ok=True)
    out2d.mkdir(parents=True, exist_ok=True)

    for site_id, g in df.groupby("SITE_ID"):
        if len(g) < min_points:
            continue

        x = g["FOCUS"].to_numpy()
        y = g["MEASUREMENT_VALUE_PH"].to_numpy()
        z = g["BIAS"].to_numpy()

        xi = np.linspace(x.min(), x.max(), grid_n)
        yi = np.linspace(y.min(), y.max(), grid_n)
        XI, YI = np.meshgrid(xi, yi)

        ZI = griddata((x, y), z, (XI, YI), method="linear")

        fig3d = go.Figure(data=[go.Surface(z=ZI, x=XI, y=YI)])
        fig3d.update_layout(
            title=f"BIAS surface - SITE_ID {site_id}",
            scene=dict(xaxis_title="FOCUS", yaxis_title="MEASUREMENT_VALUE_PH", zaxis_title="BIAS"),
        )
        pyo.plot(fig3d, filename=str(out3d / f"bias_surface_site_{site_id}.html"), auto_open=False)

        y_levels = [y.min(), float(np.mean(y)), y.max()]
        fig2d = go.Figure()
        for yl in y_levels:
            idx = int(np.argmin(np.abs(yi - yl)))
            fig2d.add_trace(go.Scatter(x=xi, y=ZI[idx, :], mode="lines", name=f"MEAS_PH≈{yi[idx]:.2f}"))

        fig2d.update_layout(
            title=f"BIAS slices - SITE_ID {site_id}",
            xaxis_title="FOCUS",
            yaxis_title="BIAS",
        )
        pyo.plot(fig2d, filename=str(out2d / f"bias_slices_site_{site_id}.html"), auto_open=False)
