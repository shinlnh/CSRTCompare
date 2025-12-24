# CompareCSRT plots

This folder contains a simple script to compare CSRT "update" vs "pure"
metrics from `auc_compare.csv` and generate charts.

## Requirements

- Python 3
- pandas
- matplotlib
- numpy

## Usage

From the project root:

```bash
python scripts/plot_auc_compare.py
```

Optional arguments:

```bash
python scripts/plot_auc_compare.py --csv path\to\auc_compare.csv --out path\to\plots
```

## Outputs

The script writes PNGs to `plots/`:

- `overall_bar.png` (overall metrics for update vs pure)
- `auc_scatter.png`
- `success50_scatter.png`
- `precision20_scatter.png`
- `fps_scatter.png`
- `delta_hist.png` (distribution of update - pure deltas)
