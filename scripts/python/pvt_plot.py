#!/usr/bin/env python3
"""Plot PVT summaries. CSV columns: corner,temp_c,vdd,metric,value (blank values skipped; value in volts)."""
import argparse, os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ORDER = ["SS", "SF", "TT", "FS", "FF"]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv")
    p.add_argument("--out", default="results/figures")
    a = p.parse_args()
    os.makedirs(a.out, exist_ok=True)
    df = pd.read_csv(a.csv).dropna(subset=["value"])
    if df.empty:
        raise SystemExit("no values to plot - fill the 'value' column first")
    for metric, g in df.groupby("metric"):
        for vdd, gv in g.groupby("vdd"):
            pt = gv.pivot_table(index="corner", columns="temp_c", values="value")
            pt = pt.reindex([c for c in ORDER if c in pt.index])
            ax = (pt * 1e3).plot(kind="bar", figsize=(6, 3.8), rot=0)
            ax.set_ylabel(f"{metric} (mV)"); ax.set_xlabel("Process corner")
            ax.set_title(f"{metric} @ VDD={vdd} V"); ax.legend(title="Temp (C)")
            ax.grid(axis="y", alpha=.3)
            fn = os.path.join(a.out, f"pvt_{metric}_{vdd}V.png")
            ax.figure.tight_layout(); ax.figure.savefig(fn, dpi=200); plt.close(ax.figure)
            print("saved", fn)


if __name__ == "__main__":
    main()
