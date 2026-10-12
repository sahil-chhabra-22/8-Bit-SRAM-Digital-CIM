import os, sys, random
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "python"))
from snm_butterfly import snm
from ncurve_metrics import ncurve_metrics, zero_crossings
from mac8_golden import dcim_mac, reference, required_bits, decode_ws


def vtc(v, vdd=1.0, k=25.0, shift=0.0):
    return vdd / (1 + np.exp(k * (v - vdd / 2 - shift)))


def test_mac_matches_reference():
    random.seed(1)
    for _ in range(200):
        n = random.choice([1, 8, 64])
        x = [random.randrange(256) for _ in range(n)]
        w = [random.randrange(256) for _ in range(n)]
        assert dcim_mac(x, w) == reference(x, w)


def test_mac_reduced_precision():
    x, w = [3, 1, 2, 0], [7, 5, 6, 1]
    assert dcim_mac(x, w, in_bits=2, w_bits=3) == reference(x, w)


def test_widths_match_paper():
    assert required_bits(64, 1, 8) == 14
    assert required_bits(64, 8, 8) == 22


def test_ws_decode():
    assert decode_ws(0) == 0b1 and decode_ws(7) == 0b11111111


def test_snm_symmetric_cell():
    v = np.linspace(0, 1, 401)
    f = vtc(v)
    s, l1, l2 = snm(v, f, f, "hold")
    assert 0.2 < s < 0.5
    assert abs(l1 - l2) < 0.01


def test_snm_degrades_with_weaker_gain():
    v = np.linspace(0, 1, 401)
    strong, _, _ = snm(v, vtc(v, k=30), vtc(v, k=30))
    weak, _, _ = snm(v, vtc(v, k=8), vtc(v, k=8))
    assert weak < strong


def test_snm_writeability_uses_larger_lobe():
    v = np.linspace(0, 1, 401)
    a, b = vtc(v, shift=0.25), vtc(v, shift=-0.25)
    hold, _, _ = snm(v, a, b, "hold")
    wr, _, _ = snm(v, a, b, "writeability")
    assert wr >= hold


def test_ncurve_metrics_cubic():
    v = np.linspace(0, 1, 1001)
    i = 2e-3 * v * (v - 0.4) * (v - 1.0)     # zeros at 0, 0.4, 1.0
    z = zero_crossings(v, i)
    assert len(z) >= 2 and abs(z[1] - 0.4) < 1e-2
    m = ncurve_metrics(v, i, 1.0)
    assert abs(m["SVNM"] - 0.4) < 2e-2 and abs(m["WTV"] - 0.6) < 2e-2


def test_pvt_3d_runs(tmp_path):
    import pandas as pd
    from pvt_3d import plot_3d
    rows = [(c, t, v, "read_snm", 0.2 + 0.01 * i) for i, (c, t, v) in enumerate(
        (c, t, v) for c in ("TT", "FF", "SS") for t in (-40, 27, 125) for v in (0.9, 1.0, 1.1))]
    df = pd.DataFrame(rows, columns=["corner", "temp_c", "vdd", "metric", "value"])
    assert os.path.exists(plot_3d(df, "read_snm", str(tmp_path)))


def test_reported_summary_dataset():
    import pandas as pd
    from snm_summary import load, plot_lines, plot_3d
    path = os.path.join(os.path.dirname(__file__), "..", "data", "snm_pvt_summary.csv")
    df = load(path)
    assert len(df) == 45 and (df["status"] == "estimated").sum() == 1
    for mode, lo, hi in (("hold", .452, .788), ("read", .479, .810), ("write", .469, .801)):
        g = df[df["mode"] == mode]
        assert abs(g["snm_v"].min() - lo) < 1e-9 and abs(g["snm_v"].max() - hi) < 1e-9
        assert g.loc[g["snm_v"].idxmin(), "corner"] == "SF" and g.loc[g["snm_v"].idxmax(), "corner"] == "FS"
