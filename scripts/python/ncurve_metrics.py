#!/usr/bin/env python3
"""N-curve metrics: SVNM, SINM, WTV, WTI.

Input CSV columns: v, i   (i = current into storage node Q while Q is forced by v)

Zero crossings (linear interpolation):
  V0 = 1st (stable '0'), Vtrip = 2nd (trip point), V1 = 3rd (stable '1') or VDD if absent
SVNM = Vtrip - V0 ; SINM = max|I| on [V0, Vtrip]
WTV  = V1 - Vtrip ; WTI  = max|I| on [Vtrip, V1]
Conventions follow Grossar et al. (JSSC 2006); edit here if your report differs.
"""
import argparse
import numpy as np


def zero_crossings(v, i):
    s = np.sign(i)
    idx = np.where(s[:-1] * s[1:] < 0)[0]
    xs = [v[k] - i[k] * (v[k + 1] - v[k]) / (i[k + 1] - i[k]) for k in idx]
    return sorted(xs + [v[k] for k in np.where(i == 0)[0]])


def ncurve_metrics(v, i, vdd=None):
    v, i = np.asarray(v, float), np.asarray(i, float)
    vdd = float(v.max()) if vdd is None else vdd
    z = zero_crossings(v, i)
    if len(z) < 2:
        raise ValueError(f"need >=2 zero crossings, found {len(z)}: cell may be unstable/monostable")
    v0, vt = z[0], z[1]
    v1 = z[2] if len(z) > 2 else vdd
    rd = (v >= v0) & (v <= vt)
    wr = (v >= vt) & (v <= v1)
    return {"V0": v0, "Vtrip": vt, "V1": v1,
            "SVNM": vt - v0, "SINM": float(np.max(np.abs(i[rd]))),
            "WTV": v1 - vt, "WTI": float(np.max(np.abs(i[wr])))}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--vdd", type=float)
    p.add_argument("--plot")
    a = p.parse_args()
    d = np.genfromtxt(a.csv, delimiter=",", names=True)
    v, i = d[d.dtype.names[0]], d[d.dtype.names[1]]
    m = ncurve_metrics(v, i, a.vdd)
    for k, val in m.items():
        cur = k in ("SINM", "WTI")
        print(f"{k:6s} = {val*(1e6 if cur else 1e3):9.3f} {'uA' if cur else 'mV'}")
    if a.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.plot(v, i * 1e6); ax.axhline(0, color="k", lw=.5)
        for k in ("V0", "Vtrip", "V1"):
            ax.axvline(m[k], ls="--", lw=.7)
        ax.set_xlabel("V(Q) (V)"); ax.set_ylabel("I(Q) (uA)"); ax.set_title("N-curve")
        ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(a.plot, dpi=200)


if __name__ == "__main__":
    main()
