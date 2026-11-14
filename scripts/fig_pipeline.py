"""Fig. 1 (pipeline overview), full page width. Run: python3 scripts/fig_pipeline.py

Fully vector, Times lettering. Panel B point clouds are simulated with a fixed
seed and the actual rules from Sec. 3 (K-means regions fit on the reference only;
trace-ratio spread; support threshold = calibrated reference quantile), so the
picture is illustrative but internally consistent. If BioRender art becomes
available it can replace the thumbnail tiles and network glyph (see make_tiles).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Rectangle, Ellipse
import style as S

S.apply()
matplotlib.rcParams.update({
    "mathtext.fontset": "custom",
    "mathtext.rm": "TeX Gyre Termes",
    "mathtext.it": "TeX Gyre Termes:italic",
    "mathtext.bf": "TeX Gyre Termes:bold",
    "mathtext.fallback": "stix",
    "axes.grid": False,
})
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")

W, H = S.PAGE_W, 3.70
PANEL_A, PANEL_B, PANEL_C, OUTC = "#eef4fc", "#fdf1ea", "#edf7f2", "#f3f2ef"
EDGE = "#c9c7c1"
FS, FSS, FST = 7.0, 6.3, 8.0  # body, small, panel title


def box(ax, x, y, w, h, fc="white", ec=EDGE, lw=0.7, r=0.06, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, p0, p1, color=S.INK2, lw=0.9, style="-|>", ms=6, conn="arc3", z=4, ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw,
                                 connectionstyle=conn, zorder=z, shrinkA=0, shrinkB=0, linestyle=ls))


def elbow(ax, p0, p1, xm=None, color=S.INK2, lw=0.9, ls="-"):
    """Horizontal-vertical-horizontal connector with an arrow head at p1."""
    xm = (p0[0] + p1[0]) / 2 if xm is None else xm
    ax.plot([p0[0], xm, xm, p1[0] - 0.02], [p0[1], p0[1], p1[1], p1[1]], color=color, lw=lw, ls=ls, zorder=4,
            solid_joinstyle="miter")
    arrow(ax, (p1[0] - 0.06, p1[1]), p1, color=color, lw=lw)


def text(ax, x, y, s, size=FS, ha="center", va="center", weight="normal", color=S.INK, style="normal", z=6, **kw):
    ax.text(x, y, s, fontsize=size, ha=ha, va=va, fontweight=weight, color=color, fontstyle=style, zorder=z, **kw)


def panel(ax, x, y, w, h, fc, letter, title):
    box(ax, x, y, w, h, fc=fc, ec="none", r=0.10, z=0)
    text(ax, x + 0.10, y + h - 0.13, f"({letter})", size=FST, ha="left", va="center", weight="bold")
    text(ax, x + 0.30, y + h - 0.13, title, size=FST, ha="left", va="center", weight="bold")


# --------------------------------------------------------------------------- thumbnails
def tile(ax, x, y, s, rng, frame):
    """A stylised image thumbnail: sky/ground gradient + one object blob."""
    hue_sets = [("#cfe0ef", "#a9c48f"), ("#f1e1c6", "#c9a06a"), ("#dfe7ee", "#8c9aa6"), ("#e8d9e6", "#b39b7c"),
                ("#d6e9f2", "#6f97b8"), ("#f3ead8", "#9fb17a")]
    sky, gnd = hue_sets[rng.integers(len(hue_sets))]
    ax.add_patch(Rectangle((x, y), s, s, fc=sky, ec="none", zorder=3))
    hz = y + s * rng.uniform(0.3, 0.5)
    ax.add_patch(Rectangle((x, y), s, hz - y, fc=gnd, ec="none", zorder=3))
    cx, cy = x + s * rng.uniform(0.3, 0.7), hz + s * rng.uniform(-0.02, 0.12)
    obj = ["#6b4f3a", "#3d4a5c", "#a33b2f", "#d8d2c4", "#2f2f2f", "#7a6a4f"][rng.integers(6)]
    if rng.random() < 0.5:
        ax.add_patch(Ellipse((cx, cy), s * rng.uniform(0.3, 0.5), s * rng.uniform(0.2, 0.35), fc=obj, ec="none", zorder=3))
    else:
        ax.add_patch(Polygon([(cx - s * 0.22, cy - s * 0.08), (cx + s * 0.22, cy - s * 0.08), (cx + s * 0.1, cy + s * 0.12),
                              (cx - s * 0.12, cy + s * 0.12)], fc=obj, ec="none", zorder=3))
    ax.add_patch(Rectangle((x, y), s, s, fc="none", ec=frame, lw=0.6, zorder=4))


def tile_grid(ax, x, y, n, s, gap, seed, frame):
    rng = np.random.default_rng(seed)
    for i in range(n):
        for j in range(n):
            tile(ax, x + j * (s + gap), y + (n - 1 - i) * (s + gap), s, rng, frame)
    tot = n * s + (n - 1) * gap
    ax.add_patch(FancyBboxPatch((x - 0.035, y - 0.035), tot + 0.07, tot + 0.07, boxstyle="round,pad=0,rounding_size=0.03",
                                fc="none", ec=frame, lw=1.1, zorder=5))
    return tot


def network(ax, cx, cy, w, h, color=S.INK2):
    """Small encoder glyph: 4 layers of nodes narrowing to the feature vector."""
    layers = [4, 3, 3, 2]
    xs = np.linspace(cx - w / 2, cx + w / 2, len(layers))
    pts = []
    for x, n in zip(xs, layers):
        ys = np.linspace(cy - h / 2 * n / 4, cy + h / 2 * n / 4, n)
        pts.append([(x, y) for y in ys])
    for a, b in zip(pts[:-1], pts[1:]):
        for p in a:
            for q in b:
                ax.plot([p[0], q[0]], [p[1], q[1]], color=S.MUTED, lw=0.35, zorder=5)
    for layer in pts:
        for p in layer:
            ax.add_patch(Circle(p, 0.028, fc="white", ec=color, lw=0.6, zorder=6))


# --------------------------------------------------------------------------- panel B data
def kmeans(x, k, seed=0, iters=50):
    rng = np.random.default_rng(seed)
    c = x[rng.choice(len(x), k, replace=False)]
    for _ in range(iters):
        lab = ((x[:, None] - c[None]) ** 2).sum(-1).argmin(1)
        c = np.array([x[lab == j].mean(0) for j in range(k)])
    return c


def voronoi_img(ax, centres, extent, cols, alpha=0.5):
    gx, gy = np.meshgrid(np.linspace(extent[0], extent[1], 300), np.linspace(extent[2], extent[3], 300))
    g = np.stack([gx, gy], -1).reshape(-1, 2)
    lab = ((g[:, None] - centres[None]) ** 2).sum(-1).argmin(1).reshape(gx.shape)
    rgb = np.array([matplotlib.colors.to_rgb(cols[j]) for j in range(len(centres))])[lab]
    ax.imshow(rgb, extent=extent, origin="lower", alpha=alpha, zorder=0, interpolation="nearest")
    ax.contour(gx, gy, lab, levels=np.arange(len(centres)) + 0.5, colors=[S.MUTED], linewidths=0.6, zorder=1)
    return lab


def mini_axes(fig, x, y, w, h):
    a = fig.add_axes([x / W, y / H, w / W, h / H])
    a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values():
        sp.set_visible(True); sp.set_color(EDGE); sp.set_linewidth(0.6)
    a.set_facecolor("white")
    return a


def panel_b(fig, x0, y0):
    rng = np.random.default_rng(7)
    ms = 3.2
    cent = np.array([[-1.25, 0.9], [1.25, 0.9], [0.0, -1.1]])
    ext = (-2.6, 2.6, -2.6, 2.6)
    regcol = ["#ffffff", "#f6f5f2", "#ffffff"]
    regcol = ["#fbfbfa", "#f1f0ec", "#fbfbfa"]

    # (1) regional mass: region 1 (top-right) depleted under Q
    a = mini_axes(fig, x0, y0, 0.98, 0.98)
    ref = np.concatenate([c + rng.normal(0, 0.42, (26, 2)) for c in cent])
    gen = np.concatenate([cent[0] + rng.normal(0, 0.42, (36, 2)), cent[2] + rng.normal(0, 0.42, (36, 2)),
                          cent[1] + rng.normal(0, 0.42, (2, 2))])
    voronoi_img(a, kmeans(ref, 3, seed=1), ext, regcol, alpha=1)
    a.scatter(*ref.T, s=ms, c=S.REF, lw=0, zorder=3)
    a.scatter(*gen.T, s=ms, c=S.GEN, lw=0, zorder=3)
    a.text(1.3, 2.15, r"$A_j$", fontsize=FS, ha="center", va="center", zorder=5)
    a.set_xlim(ext[:2]); a.set_ylim(ext[2:])

    # (2) conditional spread: Q contracted inside one region
    a = mini_axes(fig, x0 + 1.12, y0, 0.98, 0.98)
    cov = np.array([[0.30, 0.18], [0.18, 0.30]])
    ref2 = rng.multivariate_normal([0, 0], cov * 2.6, 80)
    gen2 = rng.multivariate_normal([0.05, 0.0], cov * 0.55, 80)
    a.add_patch(Ellipse((0, 0), 2 * 2.0 * np.sqrt(0.48 * 2.6), 2 * 2.0 * np.sqrt(0.12 * 2.6), angle=45,
                        fc="none", ec=S.REF, lw=0.7, ls="--", zorder=2))
    a.add_patch(Ellipse((0.05, 0), 2 * 2.0 * np.sqrt(0.48 * 0.55), 2 * 2.0 * np.sqrt(0.12 * 0.55), angle=45,
                        fc="none", ec=S.GEN, lw=0.7, ls="--", zorder=2))
    a.scatter(*ref2.T, s=ms, c=S.REF, lw=0, zorder=3)
    a.scatter(*gen2.T, s=ms, c=S.GEN, lw=0, zorder=3)
    a.set_xlim(ext[:2]); a.set_ylim(ext[2:])
    a.text(-2.35, 2.2, r"inside $A_j$", fontsize=FSS, ha="left", va="center", color=S.INK2)

    # (3) support: calibrated threshold tau as a dashed contour
    a = mini_axes(fig, x0 + 2.24, y0, 0.98, 0.98)
    ref3 = rng.normal(0, 0.62, (90, 2))
    gen3 = np.concatenate([rng.normal(0, 0.55, (60, 2)),
                           np.array([[2.05, 0.4], [-1.95, 1.3], [1.6, -1.75], [-1.0, -2.1], [0.4, 2.15], [-2.15, -0.6]])])
    a.add_patch(Circle((0, 0), 1.55, fc="#f1f0ec", ec=S.INK2, lw=0.7, ls="--", zorder=1))
    a.scatter(*ref3.T, s=ms, c=S.REF, lw=0, zorder=3)
    a.scatter(*gen3.T, s=ms, c=S.GEN, lw=0, zorder=3)
    a.text(1.05, 1.55, r"$S(x)=τ$", fontsize=FSS, ha="left", va="bottom", color=S.INK2, zorder=5)
    a.set_xlim(ext[:2]); a.set_ylim(ext[2:])


# --------------------------------------------------------------------------- figure
def main():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    top_y, top_h = 1.78, 1.90
    # ---------------- (A)
    ax_w = 3.42
    panel(ax, 0.02, top_y, ax_w, top_h, PANEL_A, "A", "Reference-calibrated comparison")
    s, gap = 0.105, 0.02
    gx = 0.16
    tot = tile_grid(ax, gx, top_y + 1.00, 3, s, gap, 3, S.REF)
    text(ax, gx + tot + 0.10, top_y + 1.30, r"Reference $P$", ha="left", weight="bold", color=S.INK)
    text(ax, gx + tot + 0.10, top_y + 1.16, "teacher or data", ha="left", size=FSS, color=S.INK2)
    tile_grid(ax, gx, top_y + 0.13, 3, s, gap, 11, S.GEN)
    text(ax, gx + tot + 0.10, top_y + 0.43, r"Candidate $Q_a$", ha="left", weight="bold", color=S.INK)
    text(ax, gx + tot + 0.10, top_y + 0.29, "configuration $a$", ha="left", size=FSS, color=S.INK2)

    fx, fy, fw, fh = 1.42, top_y + 0.52, 0.80, 0.86
    box(ax, fx, fy, fw, fh)
    text(ax, fx + fw / 2, fy + fh - 0.13, r"Feature map $φ$", weight="bold")
    network(ax, fx + fw / 2, fy + 0.44, 0.44, 0.30)
    text(ax, fx + fw / 2, fy + 0.13, "pixels, latents,\nDINOv2, CLIP", size=FSS, color=S.INK2, linespacing=1.0)
    elbow(ax, (gx + tot + 0.04, top_y + 1.03), (fx, fy + 0.62), color=S.REF, xm=1.28)
    elbow(ax, (gx + tot + 0.04, top_y + 0.16), (fx, fy + 0.24), color=S.GEN, xm=1.28)

    bx, bw = 2.40, 0.96
    b1y, bh = top_y + 1.10, 0.48
    box(ax, bx, b1y, bw, bh)
    text(ax, bx + bw / 2, b1y + bh - 0.12, r"Fit on $R_{\rm fit}$", weight="bold")
    text(ax, bx + bw / 2, b1y + 0.17, "PCA ($k$ ≤ 32),\n$K$-means ($K$ = 10)", size=FSS, color=S.INK2, linespacing=1.0)
    b2y = top_y + 0.57
    box(ax, bx, b2y, bw, 0.41)
    text(ax, bx + bw / 2, b2y + 0.29, r"Calibrate on $R_{\rm cal}$", weight="bold")
    text(ax, bx + bw / 2, b2y + 0.11, r"support threshold $τ$", size=FSS, color=S.INK2)
    b3y = top_y + 0.06
    box(ax, bx, b3y, bw, 0.34, fc="#ffffff", ec=S.INK2)
    text(ax, bx + bw / 2, b3y + 0.23, "Apply frozen", weight="bold")
    text(ax, bx + bw / 2, b3y + 0.09, r"to $R_{\rm eval}$ and $Q_a$", size=FSS, color=S.INK2)
    elbow(ax, (fx + fw, fy + 0.66), (bx, b1y + 0.12), xm=2.31)
    text(ax, bx + bw / 2, b1y + bh + 0.08, "reference images only", size=FSS, color=S.REF, style="italic", ha="center")
    arrow(ax, (bx + bw / 2, b1y), (bx + bw / 2, b2y + 0.41))
    arrow(ax, (bx + bw / 2, b2y), (bx + bw / 2, b3y + 0.34))
    # freeze glyph (padlock)
    lx, ly = bx + bw / 2 + 0.13, (b2y + b3y + 0.34) / 2 + 0.005
    ax.add_patch(FancyBboxPatch((lx - 0.045, ly - 0.05), 0.09, 0.07, boxstyle="round,pad=0,rounding_size=0.01",
                                fc=S.INK2, ec="none", zorder=6))
    ax.add_patch(matplotlib.patches.Arc((lx, ly + 0.02), 0.06, 0.08, theta1=0, theta2=180, ec=S.INK2, lw=0.9, zorder=6))
    text(ax, lx + 0.07, ly - 0.01, "freeze", size=FSS, color=S.INK2, ha="left", style="italic")
    elbow(ax, (fx + fw, fy + 0.30), (bx, b3y + 0.17), xm=2.31, ls=(0, (2, 1.5)))

    # ---------------- (B)
    bx0 = ax_w + 0.10
    bw0 = W - bx0 - 0.02
    panel(ax, bx0, top_y, bw0, top_h, PANEL_B, "B", "Three fixed-reference diagnostics")
    cols_x = [bx0 + 0.13, bx0 + 0.13 + 1.12, bx0 + 0.13 + 2.24]
    panel_b(fig, cols_x[0], top_y + 0.42)
    heads = ["Regional mass", "Within-region spread", "Reference support"]
    rules = [r"$q_j^{+}/p_j^{-}<ρ=0.5$", r"$r_{aj}$ interval below 0.9", r"$Q_a(S>τ)-P(S>τ)$"]
    verdict = ["depletion", "contraction", "support departure"]
    for cx, hd, rl, vd in zip(cols_x, heads, rules, verdict):
        text(ax, cx + 0.49, top_y + 1.52, hd, weight="bold")
        text(ax, cx + 0.49, top_y + 0.29, rl, size=FSS)
        text(ax, cx + 0.49, top_y + 0.13, vd, size=FSS, color=S.INK2, style="italic")
    # legend
    lx0 = bx0 + bw0 - 0.55
    ax.add_patch(Circle((lx0, top_y + top_h - 0.13), 0.025, fc=S.REF, ec="none", zorder=6))
    text(ax, lx0 + 0.05, top_y + top_h - 0.13, "$P$", ha="left", size=FSS)
    ax.add_patch(Circle((lx0 + 0.26, top_y + top_h - 0.13), 0.025, fc=S.GEN, ec="none", zorder=6))
    text(ax, lx0 + 0.31, top_y + top_h - 0.13, "$Q_a$", ha="left", size=FSS)

    # ---------------- (C)
    cy0, ch = 0.04, 1.68
    cw = 5.38
    panel(ax, 0.02, cy0, cw, ch, PANEL_C, "C", "Diagnosis-guided intervention")
    # findings
    fx0, fwid, fh2 = 0.14, 1.06, 0.27
    finds = ["Regional loss or excess", "Within-region contraction", "Support departure"]
    ys = [cy0 + 0.92, cy0 + 0.55, cy0 + 0.18]
    for yy, f in zip(ys, finds):
        box(ax, fx0, yy, fwid, fh2)
        text(ax, fx0 + fwid / 2, yy + fh2 / 2, f, size=FSS)
    text(ax, fx0 + fwid / 2, cy0 + 1.30, "Diagnostic finding", size=FSS, weight="bold", color=S.INK2)
    # locate
    lx1, lw1 = 1.40, 1.12
    box(ax, lx1, cy0 + 0.18, lw1, 1.01)
    text(ax, lx1 + lw1 / 2, cy0 + 1.04, "Which reference?", weight="bold")
    text(ax, lx1 + lw1 / 2, cy0 + 0.80, r"$\dfrac{q_{aj}}{p_{D,j}}=\dfrac{q_{aj}}{p_{T,j}}\,\dfrac{p_{T,j}}{p_{D,j}}$", size=FS)
    text(ax, lx1 + lw1 / 2, cy0 + 0.52, "sampler vs. teacher", size=FSS, color=S.INK2)
    text(ax, lx1 + lw1 / 2, cy0 + 0.40, "teacher vs. data", size=FSS, color=S.INK2)
    text(ax, lx1 + lw1 / 2, cy0 + 0.25, "persists across samplers?", size=FSS, color=S.INK2, style="italic")
    text(ax, lx1 + lw1 / 2, cy0 + 1.30, "Locate the cause", size=FSS, weight="bold", color=S.INK2)
    for yy in ys:
        arrow(ax, (fx0 + fwid, yy + fh2 / 2), (lx1, cy0 + 0.68), conn="arc3,rad=0")
    # interventions
    ix, iw = 2.72, 1.14
    ints = [("Starting noise", "fixed denoiser, grid, calls"), ("Grid or solver", "same conditioning"),
            ("Training continuation", "same parent, equal updates")]
    for yy, (a, b) in zip(ys, ints):
        box(ax, ix, yy - 0.02, iw, fh2 + 0.04)
        text(ax, ix + iw / 2, yy + fh2 / 2 + 0.06, a, size=FSS, weight="bold")
        text(ax, ix + iw / 2, yy + fh2 / 2 - 0.07, b, size=FSS - 0.4, color=S.INK2)
        arrow(ax, (lx1 + lw1, cy0 + 0.68), (ix, yy + fh2 / 2), conn="arc3,rad=0")
    text(ax, ix + iw / 2, cy0 + 1.30, "One specified change", size=FSS, weight="bold", color=S.INK2)
    # controlled comparison glyph
    gx0, gw = 4.06, 1.22
    box(ax, gx0, cy0 + 0.18, gw, 1.01)
    text(ax, gx0 + gw / 2, cy0 + 1.04, "Frozen comparison", weight="bold")
    text(ax, gx0 + gw / 2, cy0 + 1.30, "Test on fresh samples", size=FSS, weight="bold", color=S.INK2)
    for yy in ys:
        arrow(ax, (ix + iw, yy + fh2 / 2), (gx0, cy0 + 0.68), conn="arc3,rad=0")
    # mini forest: control vs. targeted with intervals
    axs = gx0 + 0.18
    ax.plot([axs, axs + 0.86], [cy0 + 0.40, cy0 + 0.40], color=S.MUTED, lw=0.6, zorder=5)
    for yy, c, xm, half, lab in [(cy0 + 0.80, S.CONTROL, axs + 0.66, 0.08, "control"),
                                  (cy0 + 0.58, S.REPAIR, axs + 0.26, 0.09, "targeted")]:
        ax.plot([xm - half, xm + half], [yy, yy], color=c, lw=1.1, zorder=6)
        for e in (xm - half, xm + half):
            ax.plot([e, e], [yy - 0.03, yy + 0.03], color=c, lw=1.1, zorder=6)
        ax.add_patch(Circle((xm, yy), 0.032, fc=c, ec="white", lw=0.4, zorder=7))
        text(ax, axs - 0.02 if c == S.CONTROL else axs + 0.86, yy, lab, size=FSS - 0.4, color=S.INK2,
             ha="left" if c == S.CONTROL else "right")
    text(ax, gx0 + gw / 2, cy0 + 0.28, "same budget, paired seeds", size=FSS - 0.4, color=S.INK2)

    # outcome panel
    ox = cw + 0.10
    ow = W - ox - 0.02
    box(ax, ox, cy0, ow, ch, fc=OUTC, ec="none", r=0.10, z=0)
    text(ax, ox + ow / 2, cy0 + ch - 0.18, "Independent", weight="bold", size=FST)
    text(ax, ox + ow / 2, cy0 + ch - 0.33, "outcome pool", weight="bold", size=FST)
    arrow(ax, (gx0 + gw, cy0 + 0.68), (ox + 0.06, cy0 + 0.68), conn="arc3,rad=0")
    items = ["targeted outcome", "fidelity and support", "cost (calls, updates)"]
    for k, it in enumerate(items):
        yy = cy0 + 0.88 - k * 0.24
        ax.add_patch(FancyBboxPatch((ox + 0.13, yy - 0.045), 0.09, 0.09, boxstyle="round,pad=0,rounding_size=0.015",
                                    fc="white", ec=S.INK2, lw=0.6, zorder=6))
        ax.plot([ox + 0.145, ox + 0.17, ox + 0.21], [yy, yy - 0.025, yy + 0.03], color=S.REPAIR, lw=0.9, zorder=7)
        text(ax, ox + 0.27, yy, it, size=FSS, ha="left")
    text(ax, ox + ow / 2, cy0 + 0.13, "images unseen in\nfit, calibration, diagnosis", size=FSS - 0.4,
         color=S.INK2, style="italic", linespacing=1.0)

    fig.savefig(os.path.join(OUT, "pipeline_overview.pdf"), bbox_inches=None, pad_inches=0)
    fig.savefig(os.path.join(OUT, "png", "pipeline_overview.png"), dpi=250, bbox_inches=None, pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    main()
