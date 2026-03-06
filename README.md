# Metrology Bias Mapping (3D)

Pipeline Python (données synthétiques) :
- fusion extraction/measurement + lot report
- calcul du biais BIAS = ETCH - PH
- cartographie 3D par interpolation (griddata)
- export CSV + visualisations Plotly (HTML)

## Installation
pip install -r requirements.txt

## Générer des données d'exemple
python scripts/make_sample_data.py

## Lancer le pipeline
python -m src.cli run --input-dir data/sample --output-dir outputs --plot
