#!/usr/bin/env python3
"""3D PVT visualisation: metric vs (VDD, temperature), one panel per process corner.

CSV columns: corner,temp_c,vdd,metric,value   (value in volts; plotted in mV; blank rows skipped)
Usage: python scripts/python/pvt_3d.py data/pvt_summary.csv --metric read_snm --out results/figures
"""
import argparse, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm

ORDER = ["TT", "FF", "SS", "FS", "SF"]


def plot_3d(df, metric, out_dir):
    d = df[df["metric"] == metric].dropna(subset=["value"])
    if d.empty:
        raise ValueError(f"no data for metric '{metric}'")
    corners = [c for c in ORDER if c in set(d["corner"])] + sorted(set(d["corner"]) - set(ORDER))
    vmax = d["value"].max() * 1e3
    vmin = d["value"].min() * 1e3
    cols = min(3, len(corners))
    rows = int(np.ceil(len(corners) / cols))
    fig = plt.figure(figsize=(5 * cols, 4.4 * rows))
    norm = plt.Normalize(vmin, vmax)
    for k, c in enumerate(corners):
        ax = fig.add_subplot(rows, cols, k + 1, projection="3d")
        g = d[d["corner"] == c].pivot_table(index="temp_c", columns="vdd", values="value") * 1e3
        T, V = g.index.values, g.columns.values
        xx, yy = np.meshgrid(np.arange(len(V)), np.arange(len(T)))
        z = g.values
        ax.bar3d(xx.ravel() - .35, yy.ravel() - .35, np.zeros(z.size), .7, .7, np.nan_to_num(z.ravel()),
                 color=cm.viridis(norm(np.nan_to_num(z.ravel()))), shade=True, edgecolor="none")
        ax.set_xticks(np.arange(len(V))); ax.set_xticklabels([f"{x:g}" for x in V])
        ax.set_yticks(np.arange(len(T))); ax.set_yticklabels([f"{x:g}" for x in T])
        ax.set_xlabel("VDD (V)"); ax.set_ylabel("Temp (C)"); ax.set_zlabel(f"{metric} (mV)")
        ax.set_zlim(0, vmax * 1.1); ax.set_title(c, fontweight="bold"); ax.view_init(28, -55)
    fig.suptitle(f"{metric} across PVT", fontsize=14, fontweight="bold")
    fig.tight_layout()
    os.makedirs(out_dir, exist_ok=True)
    fn = os.path.join(out_dir, f"pvt3d_{metric}.png")
    fig.savefig(fn, dpi=200); plt.close(fig)
    return fn


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv"); p.add_argument("--metric", required=True); p.add_argument("--out", default="results/figures")
    a = p.parse_args()
    print("saved", plot_3d(pd.read_csv(a.csv), a.metric, a.out))


if __name__ == "__main__":
    main()
