#!/usr/bin/env python3
"""Regenerate README artwork: isometric 3D banner, exploded architecture view, and
ILLUSTRATIVE butterfly / N-curve figures (synthetic curves, not measured data).
Usage: python scripts/make_assets.py
"""
import math, os, sys
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts", "python"))
C30, S30 = math.cos(math.radians(30)), 0.5


def shade(hexcol, f):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))


class Iso:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z):
        return (self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * S30 * self.s - z * self.s)

    def poly(self, pts, fill, extra=""):
        d = " ".join("%.1f,%.1f" % self.p(*q) for q in pts)
        return f'<polygon points="{d}" fill="{fill}" {extra}/>'

    def cube(self, x, y, z, w, d, h, col, cls="", op=1.0, stroke="rgba(255,255,255,0.10)"):
        ex = f'stroke="{stroke}" stroke-width="0.6" opacity="{op}"'
        top = self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], shade(col, 1.15), ex)
        left = self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], shade(col, 0.72), ex)
        right = self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], shade(col, 0.50), ex)
        return f'<g class="{cls}">{left}{right}{top}</g>'


FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def banner(path):
    W, H = 1280, 340
    iso = Iso(1010, 60, 25)
    n, gap = 8, 0.14
    cubes = []
    for gx in range(n):
        for gy in range(n):
            active = gy == 3
            row_hi = gx == 5
            h = 0.28
            col = "#3b5b92"
            cls = ""
            if active:
                h, col, cls = 0.62, "#19c3d6", "wave"
            elif row_hi:
                h, col = 0.45, "#f0a73a"
            cubes.append((gx + gy, gx, gy, h, col, cls))
    cubes.sort()
    body = ""
    for _, gx, gy, h, col, cls in cubes:
        delay = gx * 0.18
        g = iso.cube(gx, gy, 0, 1 - gap, 1 - gap, h, col, cls="")
        if cls:
            g = g.replace('class=""', f'class="wave" style="animation-delay:{delay:.2f}s"')
        body += g
    # base plate
    plate = iso.poly([(-0.4, -0.4, -0.18), (n + 0.1, -0.4, -0.18), (n + 0.1, n + 0.1, -0.18), (-0.4, n + 0.1, -0.18)], "#0f2038",
                     'stroke="rgba(120,170,255,0.35)" stroke-width="1"')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="FlexDCIM SRAM bit-cell analysis banner">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070d1a"/><stop offset="0.6" stop-color="#0c1a33"/><stop offset="1" stop-color="#12305a"/></linearGradient>
<linearGradient id="ttl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#7fe3f0"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="rgba(120,170,255,0.07)" stroke-width="1"/></pattern>
<style>
@keyframes pulse {{ 0%,100% {{ opacity:.55; }} 50% {{ opacity:1; }} }}
.wave {{ animation: pulse 2.2s ease-in-out infinite; }}
@media (prefers-reduced-motion: reduce) {{ .wave {{ animation: none; }} }}
</style>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#grid)"/>
<g font-family="{FONT}">
<text x="64" y="76" font-size="15" letter-spacing="3" fill="#7fe3f0" font-weight="600">IIT ROORKEE  ·  ECE DEPARTMENT  ·  INTERNSHIP 2026</text>
<text x="64" y="140" font-size="46" font-weight="800" fill="url(#ttl)">FlexDCIM SRAM Bit-Cell</text>
<text x="64" y="192" font-size="46" font-weight="800" fill="url(#ttl)">Stability &amp; PVT Analysis</text>
<text x="64" y="236" font-size="19" fill="#b7c7e2">Unsigned 8-bit MAC in the digital domain  ·  TSMC 65 nm  ·  Cadence Virtuoso</text>
<g font-size="14" font-weight="600">
<rect x="64" y="266" width="136" height="30" rx="15" fill="rgba(25,195,214,0.15)" stroke="#19c3d6"/><text x="132" y="286" text-anchor="middle" fill="#7fe3f0">Hold / Read SNM</text>
<rect x="212" y="266" width="86" height="30" rx="15" fill="rgba(25,195,214,0.15)" stroke="#19c3d6"/><text x="255" y="286" text-anchor="middle" fill="#7fe3f0">N-curve</text>
<rect x="310" y="266" width="112" height="30" rx="15" fill="rgba(25,195,214,0.15)" stroke="#19c3d6"/><text x="366" y="286" text-anchor="middle" fill="#7fe3f0">Write margin</text>
<rect x="434" y="266" width="98" height="30" rx="15" fill="rgba(240,167,58,0.15)" stroke="#f0a73a"/><text x="483" y="286" text-anchor="middle" fill="#f6c37a">PVT sweep</text>
</g></g>
{plate}
{body}
</svg>'''
    open(path, "w").write(svg)


def arch(path):
    W, H = 1100, 740
    iso = Iso(200, 430, 24)
    tx, ty = 12, 6
    levels = [  # (z, name, colour, builder)
        (0.0, "acc", "#8e6bd8"),
        (6.0, "add", "#19b8a6"),
        (12.0, "arr", "#3f7be0"),
    ]
    out = ""
    # draw bottom (front/lower) slabs first? In this projection higher z is drawn later (on top)
    for z, kind, col in levels:
        if kind == "arr":
            tiles = [(i, j, 1, 1, 0.34) for i in range(tx) for j in range(ty)]
        elif kind == "add":
            tiles = [(i, 0, 1, ty, 0.2) for i in range(tx)]
        else:
            tiles = [(i, ty / 2 - 1, 1, 2, 0.34) for i in range(tx)]
        plate = iso.poly([(-0.3, -0.3, z - 0.05), (tx + 0.3, -0.3, z - 0.05), (tx + 0.3, ty + 0.3, z - 0.05), (-0.3, ty + 0.3, z - 0.05)],
                         "#0e1b30", 'stroke="rgba(130,170,240,0.45)" stroke-width="1"')
        out += plate
        for (i, j, w, d, h) in sorted(tiles, key=lambda t: (t[0] + t[1], t[1])):
            hi = (kind == "arr" and j == 2)
            c = "#19c3d6" if hi else col
            out += iso.cube(i + 0.06, j + 0.06, z, w - 0.12, d - 0.12, h, c, op=1.0)
    # flow arrows between slabs (at right-front corner)
    def arrow(z1, z2):
        x, y = tx + 0.6, ty * 0.5
        a, b = iso.p(x, y, z1 + 0.5), iso.p(x, y, z2 - 0.1)
        return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#f0a73a" stroke-width="2.2" stroke-dasharray="6 5" marker-end="url(#ah)"/>')
    out += arrow(12.0, 6.5) + arrow(6.0, 0.5)
    # labels with leader lines
    def label(z, x, y, title, sub, ty_):
        px, py = iso.p(x, y, z + 0.3)
        lx = 660
        return (f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{lx-14}" y2="{ty_-6}" stroke="rgba(160,190,240,0.5)" stroke-width="1"/>'
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="#f0a73a"/>'
                f'<text x="{lx}" y="{ty_}" font-size="19" font-weight="700" fill="#e9f0ff">{title}</text>'
                f'<text x="{lx}" y="{ty_+24}" font-size="14.5" fill="#9fb3d6">{sub[0]}</text>'
                f'<text x="{lx}" y="{ty_+44}" font-size="14.5" fill="#9fb3d6">{sub[1]}</text>')
    out += label(12.0, tx, ty / 2, "512 x 128 SRAM array", ("8x1 DPUs: 8T SRAM + shared digital logic", "8.75 T per stored bit, divided bit-line"), 230)
    out += label(6.0, tx, ty / 2, "Binary adder trees (x16)", ("64 products of 1b x 8b per cycle", "14-bit partial sum"), 400)
    out += label(0.0, tx, ty / 2, "Shift-and-add accumulators (x16)", ("Bit-serial input, MSB first", "22-bit result for 64 x 8b x 8b"), 570)
    # input / output tags
    ix, iy = iso.p(2, 0, 13.8)
    out += (f'<text x="{ix-70:.0f}" y="{iy-14:.0f}" font-size="15" font-weight="600" fill="#7fe3f0">1b input (RWL)</text>'
            f'<line x1="{ix:.1f}" y1="{iy-10:.1f}" x2="{ix:.1f}" y2="{iso.p(2,0,12.9)[1]:.1f}" stroke="#7fe3f0" stroke-width="2" marker-end="url(#ah2)"/>')
    ox_, oy_ = iso.p(tx / 2, ty + 0.3, -0.2)
    out += f'<text x="{ox_-40:.0f}" y="{oy_+34:.0f}" font-size="15" font-weight="600" fill="#f6c37a">MAC output</text>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Exploded 3D view of the FlexDCIM macro">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#080f1d"/><stop offset="1" stop-color="#112a4f"/></linearGradient>
<marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#f0a73a"/></marker>
<marker id="ah2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#7fe3f0"/></marker>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<g font-family="{FONT}">
<text x="40" y="52" font-size="22" font-weight="700" fill="#ffffff">FlexDCIM macro - exploded view</text>
<text x="40" y="76" font-size="14" fill="#9fb3d6">Highlighted row: one input activates a row of DPUs; products flow down to the adder trees. Block-level sketch, not to scale.</text>
{out}
</g></svg>'''
    open(path, "w").write(svg)


def figures(outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from snm_butterfly import snm
    from ncurve_metrics import ncurve_metrics
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    v = np.linspace(0, 1, 801)
    f = 1 / (1 + np.exp(22 * (v - 0.5)))
    val, _, _ = snm(v, f, f, "hold")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(v, f, color="#2f6fd6", lw=2, label="VTC 1:  QB = f(Q)")
    ax.plot(f, v, color="#d9822b", lw=2, label="VTC 2 (mirrored):  Q = f(QB)")
    # largest square in lobe (upper-left): brute force for drawing
    best = (0, 0, 0)
    xs = np.linspace(0, 1, 400)
    for x0 in xs:
        y0 = np.interp(x0, f[::-1], v[::-1]) if False else None
    A = lambda x: np.interp(x, v, f)
    B = lambda x: np.interp(x, f[::-1], v[::-1])
    for x0 in xs:
        for s in np.linspace(0, 0.6, 300):
            if x0 + s <= 1 and A(x0 + s) - B(x0) >= s and B(x0) + s <= 1:
                if s > best[0]:
                    best = (s, x0, B(x0))
    s, x0, y0 = best
    ax.add_patch(plt.Rectangle((x0, y0), s, s, fill=True, fc="#19c3d6", alpha=.35, ec="#0a8c9b", lw=1.5))
    ax.add_patch(plt.Rectangle((y0, x0), s, s, fill=True, fc="#19c3d6", alpha=.35, ec="#0a8c9b", lw=1.5))
    ax.annotate("SNM = side of the largest\ninscribed square", xy=(x0 + s / 2, y0 + s / 2), xytext=(0.42, 0.88),
                arrowprops=dict(arrowstyle="->"), fontsize=9)
    ax.set_xlabel("Q (V)"); ax.set_ylabel("QB (V)"); ax.set_aspect("equal"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.grid(alpha=.25); ax.legend(loc="lower left", fontsize=8, frameon=False)
    ax.set_title("Butterfly-curve SNM (illustrative, synthetic VTC)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "butterfly_illustration.png"), dpi=200); plt.close(fig)

    i = 3.0e-4 * v * (v - 0.38) * (v - 1.0) * -1
    i = -i * 4
    m = ncurve_metrics(v, i, 1.0)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_ylim(-100, 60)
    ax.plot(v, i * 1e6, color="#2f6fd6", lw=2); ax.axhline(0, color="k", lw=.6)
    for k, lab in (("V0", "V0"), ("Vtrip", "V_trip"), ("V1", "V1")):
        ax.axvline(m[k], ls="--", lw=.8, color="gray"); ax.text(m[k], ax.get_ylim()[1] * .92, lab, ha="center", fontsize=8, backgroundcolor="white")
    mid = (m["V0"] + m["Vtrip"]) / 2
    ax.annotate("", xy=(m["Vtrip"], 0), xytext=(m["V0"], 0), arrowprops=dict(arrowstyle="<->", color="#d9822b"))
    ax.text(mid, 0.03 * ax.get_ylim()[1], "SVNM", color="#d9822b", ha="center", fontsize=9)
    mid2 = (m["Vtrip"] + m["V1"]) / 2
    ax.annotate("", xy=(m["V1"], 0), xytext=(m["Vtrip"], 0), arrowprops=dict(arrowstyle="<->", color="#19a392"))
    ax.text(mid2, -0.1 * abs(ax.get_ylim()[0]), "WTV", color="#19a392", ha="center", fontsize=9)
    ax.text(mid, i[(v > m["V0"]) & (v < m["Vtrip"])].max() * 1e6 + 4, "SINM", color="#d9822b", ha="center", fontsize=9)
    ax.text(mid2, i[(v > m["Vtrip"]) & (v < m["V1"])].min() * 1e6 - 10, "WTI", color="#19a392", ha="center", fontsize=9)
    ax.set_xlabel("V(Q) (V)"); ax.set_ylabel("I(Q) (a.u.)"); ax.grid(alpha=.25)
    ax.set_title("N-curve metrics (illustrative, synthetic curve)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "ncurve_illustration.png"), dpi=200); plt.close(fig)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    banner(os.path.join(ROOT, "assets", "banner.svg"))
    arch(os.path.join(ROOT, "assets", "arch_3d.svg"))
    figures(os.path.join(ROOT, "docs", "images"))
    print("assets written")
