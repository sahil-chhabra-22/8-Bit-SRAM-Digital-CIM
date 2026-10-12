#!/usr/bin/env python3
"""Static noise margin from butterfly-curve data.

Input CSV columns: v, qb_of_q, q_of_qb
  v        sweep voltage (0..VDD)
  qb_of_q  QB measured while Q is swept   (VTC of inverter 1)
  q_of_qb  Q  measured while QB is swept  (VTC of inverter 2)

SNM = side of the largest axis-parallel square inscribed in a lobe of the butterfly.
  hold / read / write : SNM = min(lobe1, lobe2). 'write' is the write-mode (half-selected cell, WL high,
                        bit-lines at retention levels) disturb SNM used in this project.
  writeability        : full write with a bit-line at 0 V; one lobe collapses and the margin is the
                        remaining (larger) lobe -> max(lobe1, lobe2)
"""
import argparse
import numpy as np


def _curve(x_vals, y_vals):
    order = np.argsort(x_vals)
    xs, ys = np.asarray(x_vals)[order], np.asarray(y_vals)[order]
    return lambda x: np.interp(x, xs, ys)


def _lobe(upper, lower, vdd, n=500):
    """Largest s with lower(x0) <= y0 and upper(x0+s) >= y0+s (both curves decreasing in x)."""
    x0 = np.linspace(0, vdd, n)[:, None]
    s = np.linspace(0, vdd, n)[None, :]
    xe = np.clip(x0 + s, 0, vdd)
    fits = (x0 + s <= vdd) & (upper(xe) - lower(x0) >= s)
    return float(np.max(np.where(fits, s, 0.0)))


def snm(v, qb_of_q, q_of_qb, mode="hold"):
    v = np.asarray(v, float)
    vdd = float(v.max())
    A = _curve(v, qb_of_q)        # y = QB(x = Q)
    B = _curve(q_of_qb, v)        # mirrored: points (x = Q(QB=y), y)
    lobe1, lobe2 = _lobe(A, B, vdd), _lobe(B, A, vdd)
    value = max(lobe1, lobe2) if mode == "writeability" else min(lobe1, lobe2)
    return value, lobe1, lobe2


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--mode", choices=["hold", "read", "write", "writeability"], default="hold")
    p.add_argument("--plot", help="save butterfly plot to this path")
    a = p.parse_args()

    d = np.genfromtxt(a.csv, delimiter=",", names=True)
    n = d.dtype.names
    v, f1, f2 = d[n[0]], d[n[1]], d[n[2]]
    value, l1, l2 = snm(v, f1, f2, a.mode)
    print(f"mode={a.mode}  lobe1={l1*1e3:.1f} mV  lobe2={l2*1e3:.1f} mV  SNM={value*1e3:.1f} mV")

    if a.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.plot(v, f1, label="QB vs Q")
        ax.plot(f2, v, label="Q vs QB (mirrored)")
        ax.set_xlabel("Q (V)"); ax.set_ylabel("QB (V)")
        ax.set_title(f"{a.mode.capitalize()} butterfly, SNM = {value*1e3:.1f} mV")
        ax.set_aspect("equal"); ax.grid(alpha=.3); ax.legend()
        fig.tight_layout(); fig.savefig(a.plot, dpi=200)


if __name__ == "__main__":
    main()
