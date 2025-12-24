import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _overall_bar(df_overall, metrics, out_dir):
    if df_overall.empty:
        return

    row = df_overall.iloc[0]
    update_vals = [row[f"{m}_update"] for m, _ in metrics]
    pure_vals = [row[f"{m}_pure"] for m, _ in metrics]
    labels = [label for _, label in metrics]

    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    x = np.arange(len(metrics))
    width = 0.35
    ax.bar(x - width / 2, update_vals, width, label="update")
    ax.bar(x + width / 2, pure_vals, width, label="pure")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Score")
    ax.set_title("Overall comparison")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_dir / "overall_bar.png")
    plt.close(fig)


def _scatter_plots(df_seq, metrics, out_dir):
    total = len(df_seq)
    for metric, label in metrics:
        col_update = f"{metric}_update"
        col_pure = f"{metric}_pure"
        update_vals = df_seq[col_update]
        pure_vals = df_seq[col_pure]

        fig, ax = plt.subplots(figsize=(5, 5), dpi=150)
        ax.scatter(pure_vals, update_vals, s=25, alpha=0.7, edgecolors="none")
        minv = min(pure_vals.min(), update_vals.min())
        maxv = max(pure_vals.max(), update_vals.max())
        ax.plot([minv, maxv], [minv, maxv], color="gray", linewidth=1, linestyle="--")
        ax.set_xlabel(f"{label} (pure)")
        ax.set_ylabel(f"{label} (update)")
        ax.set_title(f"{label} per sequence")
        wins = int((update_vals > pure_vals).sum())
        ties = int((update_vals == pure_vals).sum())
        ax.text(
            0.02,
            0.98,
            f"update>pure: {wins}/{total} | ties: {ties}",
            transform=ax.transAxes,
            va="top",
        )
        ax.grid(alpha=0.3)

        fig.tight_layout()
        fig.savefig(out_dir / f"{metric}_scatter.png")
        plt.close(fig)


def _delta_histograms(df_seq, metrics, out_dir):
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), dpi=150)
    axes = axes.ravel()
    for ax, (metric, label) in zip(axes, metrics):
        delta = df_seq[f"{metric}_update"] - df_seq[f"{metric}_pure"]
        ax.hist(delta, bins=30, color="#4c72b0", alpha=0.85)
        ax.axvline(0, color="black", linewidth=1)
        ax.set_title(f"{label} delta (update - pure)")
        ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_dir / "delta_hist.png")
    plt.close(fig)


def main():
    root_dir = Path(__file__).resolve().parents[1]
    default_csv = root_dir / "auc_compare.csv"
    default_out = root_dir / "plots"

    parser = argparse.ArgumentParser(description="Plot CSRT update vs pure metrics.")
    parser.add_argument("--csv", type=Path, default=default_csv)
    parser.add_argument("--out", type=Path, default=default_out)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df_seq = df[df["sequence"] != "OVERALL"].copy()
    df_overall = df[df["sequence"] == "OVERALL"].copy()

    metrics = [
        ("auc", "AUC"),
        ("success50", "Success@0.5"),
        ("precision20", "Precision@20"),
        ("fps", "FPS"),
    ]

    args.out.mkdir(parents=True, exist_ok=True)
    _overall_bar(df_overall, metrics, args.out)
    _scatter_plots(df_seq, metrics, args.out)
    _delta_histograms(df_seq, metrics, args.out)


if __name__ == "__main__":
    main()
