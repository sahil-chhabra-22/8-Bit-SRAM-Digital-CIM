#!/usr/bin/env python3
"""Plot the hold / read / write SNM PVT summary (worst case over 10-50 C per corner and VDD).

CSV columns: mode,corner,vdd,snm_v,status   (status = simulated | estimated)

  python scripts/python/snm_summary.py data/snm_pvt_summary.csv --out results/figures
  python scripts/python/snm_summary.py data/snm_pvt_summary.csv --convention side   # marker reading / sqrt(2)
"""
import argparse, math, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm

CORNERS = ["TT", "FF", "SS", "FS", "SF"]
MODES = ["hold", "read", "write"]
COLORS = {"TT": "#2f6fd6", "FF": "#19a392", "SS": "#8e6bd8", "FS": "#f0a73a", "SF": "#d64545"}
TITLES = {"hold": "Hold SNM", "read": "Read SNM", "write": "Write-mode SNM"}


def load(path, convention="marker"):
    df = pd.read_csv(path)
    if convention == "side":
        df["snm_v"] = df["snm_v"] / math.sqrt(2)
    return df


def _ylabel(convention):
    return "SNM (V)" if convention == "marker" else "SNM, square side (V)"


def plot_lines(df, out_dir, convention="marker"):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.3), sharey=True)
    for ax, mode in zip(axes, MODES):
        g = df[df["mode"] == mode]
        for c in CORNERS:
            s = g[g["corner"] == c].sort_values("vdd")
            ax.plot(s["vdd"], s["snm_v"], "-o", color=COLORS[c], lw=2, ms=6, label=c)
            e = s[s["status"] == "estimated"]
            if not e.empty:
                ax.plot(e["vdd"], e["snm_v"], "o", mfc="white", mec=COLORS[c], ms=9, mew=2)
                ax.annotate("estimated", (e["vdd"].iloc[0], e["snm_v"].iloc[0]), xytext=(8, -16),
                            textcoords="offset points", fontsize=8, color=COLORS[c])
        ax.set_title(TITLES[mode], fontweight="bold"); ax.set_xlabel("VDD (V)")
        ax.set_xticks([1.1, 1.2, 1.3]); ax.grid(alpha=.3)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel(_ylabel(convention)); axes[0].legend(title="Corner", frameon=False)
    fig.suptitle("SNM vs supply voltage, all process corners (worst case over 10-50 C)", fontsize=12)
    fig.tight_layout()
    fn = os.path.join(out_dir, "snm_vs_vdd.png"); fig.savefig(fn, dpi=200); plt.close(fig)
    return fn


def plot_3d(df, out_dir, convention="marker"):
    fig = plt.figure(figsize=(15, 5))
    norm = plt.Normalize(df["snm_v"].min(), df["snm_v"].max())
    vdds = [1.1, 1.2, 1.3]
    for k, mode in enumerate(MODES):
        ax = fig.add_subplot(1, 3, k + 1, projection="3d")
        g = df[df["mode"] == mode]
        for yi, c in enumerate(CORNERS):
            for xi, v in enumerate(vdds):
                r = g[(g["corner"] == c) & (np.isclose(g["vdd"], v))].iloc[0]
                ax.bar3d(xi - .3, yi - .3, 0, .6, .6, r["snm_v"], color=cm.viridis(norm(r["snm_v"])),
                         alpha=.45 if r["status"] == "estimated" else 1.0, shade=True, edgecolor="none")
        ax.set_xticks(range(3)); ax.set_xticklabels(vdds)
        ax.set_yticks(range(len(CORNERS))); ax.set_yticklabels(CORNERS)
        ax.set_xlabel("VDD (V)"); ax.set_ylabel("Corner"); ax.set_zlabel(_ylabel(convention))
        ax.set_zlim(0, df["snm_v"].max() * 1.1); ax.set_title(TITLES[mode], fontweight="bold"); ax.view_init(27, -58)
    fig.suptitle("SNM across process corners and supply voltage", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fn = os.path.join(out_dir, "snm_3d.png"); fig.savefig(fn, dpi=200); plt.close(fig)
    return fn


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv"); p.add_argument("--out", default="results/figures")
    p.add_argument("--convention", choices=["marker", "side"], default="marker",
                   help="marker = values as read from the SNM marker; side = marker reading / sqrt(2)")
    a = p.parse_args()
    os.makedirs(a.out, exist_ok=True)
    df = load(a.csv, a.convention)
    for m in MODES:
        g = df[df["mode"] == m]
        lo, hi = g.loc[g["snm_v"].idxmin()], g.loc[g["snm_v"].idxmax()]
        print(f"{m:5s} min {lo.snm_v:.3f} V ({lo.corner}, {lo.vdd} V)  max {hi.snm_v:.3f} V ({hi.corner}, {hi.vdd} V)")
    print("saved", plot_lines(df, a.out, a.convention)); print("saved", plot_3d(df, a.out, a.convention))


if __name__ == "__main__":
    main()
