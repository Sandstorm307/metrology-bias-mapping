import argparse
from pathlib import Path

from .bias_pipeline import run_pipeline
from .plots import plot_bias_maps


def main():
    parser = argparse.ArgumentParser(description="Metrology bias mapping (sample-safe).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run bias pipeline")
    run.add_argument("--input-dir", required=True, help="Input directory (e.g., data/sample)")
    run.add_argument("--output-dir", required=True, help="Output directory (e.g., outputs)")
    run.add_argument("--plot", action="store_true", help="Generate Plotly HTML plots")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    out = run_pipeline(input_dir, output_dir)
    if args.plot:
        plot_bias_maps(out.bias_csv, output_dir)


if __name__ == "__main__":
    main()
