"""Main-paper data figures. Run: python3 scripts/fig_results.py  (writes figures/*.pdf)

File names are unchanged so the manuscript text and \\includegraphics lines are untouched.
All numbers come from scripts/data.py.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator, FuncFormatter

import style as S
import data as D

S.apply()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"))
    fig.savefig(os.path.join(OUT, "png", name + ".png"), dpi=220)
    plt.close(fig)


def rows_axis(ax, labels):
    n = len(labels)
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels)
    ax.set_ylim(n - 0.45, -0.55)
    ax.tick_params(axis="y", length=0, pad=3)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)


def hilite(ax, y):
    ax.axhspan(y - 0.42, y + 0.42, color=S.HILITE, zorder=0, lw=0)


# --------------------------------------------------------------------------- Fig. 2
def fig_overview():
    fig, axes = plt.subplots(2, 1, figsize=(S.COL_W, 1.86), gridspec_kw=dict(hspace=1.35))
    specs = [
        (axes[0], D.FIG2_CIFAR_KID, [S.CONTROL, S.REPAIR], ["o", "D"], "(a) CIFAR-10 at two denoiser calls",
         "KID \N{MULTIPLICATION SIGN}10\N{SUPERSCRIPT THREE} (lower is better)", "\N{MINUS SIGN}32.0%", (115, 196), [125, 145, 165, 185], "{:.1f}"),
        (axes[1], D.FIG2_MNIST_ERR, [S.ADVERSE, S.REPAIR], ["s", "D"], "(b) MNIST after 8,000 updates",
         "Mean class-mass error (%, lower is better)", "\N{MINUS SIGN}58.7%", (0, 3.2), [0, 1, 2, 3], "{:.2f}"),
    ]
    for ax, rows, cols, mks, title, xl, eff, xlim, ticks, fmt in specs:
        labels = [r[0] for r in rows]
        rows_axis(ax, labels)
        hilite(ax, 1)
        for i, (lab, est, lo, hi) in enumerate(rows):
            S.ci(ax, i, est, lo, hi, cols[i], marker=mks[i])
            ax.annotate(fmt.format(est), (hi, i), xytext=(4, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=6.8, color=S.INK2)
        ax.set_xlim(*xlim)
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.set_xlabel(xl, labelpad=1.5)
        ax.set_title(title, pad=4)
        ax.annotate(eff, (1.0, 1.0), xycoords="axes fraction", xytext=(0, 4), textcoords="offset points",
                    ha="right", va="baseline", fontsize=8, fontweight="bold", color=S.INK)
    save(fig, "overview")


# --------------------------------------------------------------------------- Fig. 3
def fig_power():
    fig, ax = plt.subplots(figsize=(S.COL_W, 1.75))
    marks = {"0.5%": "v", "1%": "o", "2%": "s", "5%": "D"}
    lab_pos = {"5%": (500, 50), "2%": (1000, 50), "1%": (2000, 50), "0.5%": (5000, 50)}
    for (mass, pts), col in zip(D.FIG3.items(), S.SEQ):
        n = np.array(D.FIG3_N, float)
        est = np.array([p[0] for p in pts]); lo = np.array([p[1] for p in pts]); hi = np.array([p[2] for p in pts])
        ax.plot(n, est, color=col, marker=marks[mass], ms=3.8, mec="white", mew=0.5, label=mass, zorder=3)
        ax.errorbar(n, est, yerr=[est - lo, hi - est], fmt="none", ecolor=col, elinewidth=1.0, capsize=2.0, zorder=2)
    # direct labels on the rising part of each curve
    for mass, pts in D.FIG3.items():  # label each curve where it crosses 60%
        est = [p[0] for p in pts]
        k = next(i for i in range(1, len(est)) if est[i] >= 60)
        t = (60 - est[k - 1]) / (est[k] - est[k - 1])
        xc = np.exp(np.log(D.FIG3_N[k - 1]) + t * (np.log(D.FIG3_N[k]) - np.log(D.FIG3_N[k - 1])))
        ax.annotate(mass, (xc, 60), xytext=(-4, 0), textcoords="offset points", ha="right", va="center",
                    fontsize=7, color=S.INK, fontweight="bold")
    ax.set_xscale("log")
    ax.set_xlim(85, 11800)
    ax.xaxis.set_major_locator(FixedLocator([100, 250, 500, 1000, 2000, 5000, 10000]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_ylim(-4, 104)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Samples per evaluation set (log scale)")
    ax.set_ylabel("Detection rate (%)")
    leg = ax.legend(title="Removed region's reference mass", ncol=4, loc="lower center",
                    bbox_to_anchor=(0.5, 1.0), columnspacing=1.0, handletextpad=0.4, borderaxespad=0.2)
    leg.get_title().set_fontsize(7)
    leg.get_title().set_fontweight("bold")
    save(fig, "support_power_main")


# --------------------------------------------------------------------------- Fig. 4
def fig_init():
    fig = plt.figure(figsize=(S.COL_W, 2.52))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.05], hspace=0.78)
    ax = fig.add_subplot(gs[0])
    st = {"Matched Gaussian": dict(color=S.REPAIR, ls="--", marker="s"),
          "Normal Gaussian": dict(color=S.CONTROL, ls=":", marker="o"),
          "Learned DDIM": dict(color=S.INK2, ls="-", marker="^")}
    for k, v in D.FIG4A.items():
        ax.plot(D.FIG4A_CALLS, v, label=k, ms=3.8, mec="white", mew=0.5, **st[k])
    ax.axhline(1.0, color=S.MUTED, lw=0.6, ls=(0, (1, 1.5)), zorder=1)
    ax.set_xscale("log", base=2)
    ax.xaxis.set_major_locator(FixedLocator(D.FIG4A_CALLS))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
    ax.set_ylim(-0.03, 1.08)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("Denoiser calls (log scale)", labelpad=1.5)
    ax.set_ylabel("Variance ratio")
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), handlelength=2.2)
    ax.set_title("(a) Gaussian predictions and learned DDIM", pad=4)
    box = ax.get_position()

    ax = fig.add_subplot(gs[1])
    rows = D.FIG4B_KID
    rows_axis(ax, [r[0] for r in rows])
    style_b = {"Leading DDIM": (S.CONTROL, "o", True), "Trailing DDIM": (S.CONTROL, "o", False),
               "DPM++ / UniPC": (S.ALT, "s", True), "Full moments": (S.REPAIR, "D", False),
               "Covariance only": (S.REPAIR, "D", True)}
    hilite(ax, len(rows) - 1)
    for i, (lab, est, lo, hi) in enumerate(rows):
        c, m, f = style_b[lab]
        S.ci(ax, i, est, lo, hi, c, marker=m, filled=f)
        ax.annotate(f"{est:.1f}", (hi, i), xytext=(4, 0), textcoords="offset points", va="center",
                    fontsize=6.8, color=S.INK2)
    ax.set_xlim(115, 238)
    ax.xaxis.set_major_locator(FixedLocator([125, 150, 175, 200, 225]))
    ax.set_xlabel("KID \N{MULTIPLICATION SIGN}10\N{SUPERSCRIPT THREE} (lower is better)", labelpad=1.5)
    ax.set_title("(b) Fresh two-call CIFAR-10 results", pad=4)
    save(fig, "initialization_repair")


# --------------------------------------------------------------------------- Fig. 5
def fig_numerical():
    fig, axes = plt.subplots(1, 3, figsize=(S.COL_W, 1.08), sharey=True, gridspec_kw=dict(wspace=0.12))
    cols = {"DDIM": (S.CONTROL, "o"), "Output cov.": (S.ADVERSE, "s"), "UniPC": (S.ALT, "^")}
    specs = [(D.FIG5_PIXEL_SPREAD, "Pixel spread", (0.3, 1.05), [0.4, 0.7, 1.0], "{:.1f}"),
             (D.FIG5_COVERAGE, "Coverage \N{UPWARDS ARROW}", (0.29, 0.6), [0.35, 0.45, 0.55], "{:.2f}"),
             (D.FIG5_KID, "KID \N{MULTIPLICATION SIGN}10\N{SUPERSCRIPT THREE} \N{DOWNWARDS ARROW}", (60, 110), [70, 90], "{:.0f}")]
    for j, (ax, (rows, title, xlim, ticks, fmt)) in enumerate(zip(axes, specs)):
        if j == 0:
            rows_axis(ax, [r[0] for r in rows])
        else:
            ax.tick_params(axis="y", length=0)
            ax.spines["left"].set_visible(False)
            ax.grid(axis="y", visible=False)
        for i, (lab, est, lo, hi) in enumerate(rows):
            c, m = cols[lab]
            S.ci(ax, i, est, lo, hi, c, marker=m)
        if j == 0:
            ax.axvline(1.0, color=S.INK2, lw=0.7, ls="--", zorder=1)
        ax.set_xlim(*xlim)
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _, f=fmt: f.format(v)))
        ax.set_title(title, loc="center", pad=3, fontsize=7.5)
    save(fig, "numerical_repair")


# --------------------------------------------------------------------------- Fig. 6
def fig_edm():
    fig, axes = plt.subplots(1, 2, figsize=(S.COL_W, 1.42), gridspec_kw=dict(wspace=0.42))
    st = {"Euler": dict(color=S.CONTROL, marker="o", ls="-"), "Heun": dict(color=S.ALT, marker="s", ls="--")}
    for ax, dat, title in [(axes[0], D.FIG6_KID, "(a) KID \N{MULTIPLICATION SIGN}10\N{SUPERSCRIPT THREE} \N{DOWNWARDS ARROW}"),
                           (axes[1], D.FIG6_COV, "(b) Data coverage \N{UPWARDS ARROW}")]:
        for k, v in dat.items():
            ax.plot(D.FIG6_CALLS, v, label=k, ms=3.8, mec="white", mew=0.5, **st[k])
        ax.set_xscale("log")
        ax.xaxis.set_major_locator(FixedLocator(D.FIG6_CALLS))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v)}"))
        ax.set_xlim(2.6, 41)
        ax.set_xlabel("Denoiser calls (log scale)", labelpad=1.5)
        ax.set_title(title, pad=4, fontsize=7.5)
    axes[0].set_yscale("log")
    axes[0].set_ylim(0.25, 1500)
    axes[0].yaxis.set_major_locator(FixedLocator([1, 10, 100, 1000]))
    axes[0].yaxis.set_minor_locator(NullLocator())
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    axes[1].set_ylim(-0.03, 0.56)
    axes[1].set_yticks([0, 0.25, 0.5])
    axes[1].legend(loc="lower right", handlelength=2.0)
    save(fig, "edm_solver_audit")


# --------------------------------------------------------------------------- Fig. 7
def fig_mnist():
    fig = plt.figure(figsize=(S.COL_W, 3.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.35, 1.0], hspace=0.62)
    ax = fig.add_subplot(gs[0])
    x = np.arange(len(D.FIG7_KEYS)).astype(float)
    x[-1] += 0.6  # separate the reject event
    keep, ordi = np.array(D.FIG7_GAP["Keep targeting"]), np.array(D.FIG7_GAP["Ordinary data"])
    for xi, a, b in zip(x, keep, ordi):
        ax.plot([xi, xi], [a, b], color=S.GRID, lw=1.6, zorder=1, solid_capstyle="round")
    ax.plot(x, keep, "s", color=S.ADVERSE, mec="white", mew=0.5, ms=4.6, label="Keep targeting", zorder=3)
    ax.plot(x, ordi, "D", color=S.REPAIR, mec="white", mew=0.5, ms=4.2, label="Ordinary data", zorder=3)
    ax.axhline(0, color=S.INK2, lw=0.7, zorder=2)
    ax.axvline((x[-2] + x[-1]) / 2, color=S.MUTED, lw=0.6, ls=":", zorder=1)
    ax.set_xticks(x)
    ax.set_xticklabels(D.FIG7_KEYS[:-1] + ["Reject"])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    ax.set_xlim(x[0] - 0.6, x[-1] + 0.7)
    ax.set_ylim(-3.6, 9.2)
    ax.set_yticks([-2.5, 0, 2.5, 5, 7.5])
    ax.set_xlabel("Classifier outcome (digit or reject)", labelpad=1.5)
    ax.set_ylabel("Gap to real data (pp)")
    ax.legend(loc="upper left", ncol=2, handletextpad=0.3, columnspacing=1.2, borderaxespad=0.1)
    ax.set_title("(a) Signed mass gaps from real data", pad=4)

    ax = fig.add_subplot(gs[1])
    mk, ls = ["o", "s", "^"], ["-", "--", ":"]
    for i, (a, b) in enumerate(D.FIG7_TV):
        ax.plot([0, 1], [a, b], color=S.INK2, ls=ls[i], marker=mk[i], ms=4.0, mec="white", mew=0.5,
                lw=1.1, label=f"Seed {i + 1}", zorder=3)
    for xx, c in [(0, S.ADVERSE), (1, S.REPAIR)]:
        ax.axvspan(xx - 0.06, xx + 0.06, color=c, alpha=0.12, lw=0, zorder=0)
    ma = np.mean([a for a, b in D.FIG7_TV]); mb = np.mean([b for a, b in D.FIG7_TV])
    ax.text(-0.1, ma + 1.2, f"mean {ma:.1f}", ha="right", va="center", fontsize=6.8, color=S.INK2)
    ax.text(1.1, mb, f"mean {mb:.1f}", ha="left", va="center", fontsize=6.8, color=S.INK2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Keep targeting", "Ordinary data"])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(5.5, 17.5)
    ax.set_yticks([6, 9, 12, 15])
    ax.set_ylabel("Total variation (%)")
    ax.legend(loc="lower left", ncol=1, handlelength=2.2, borderaxespad=0.1, labelspacing=0.25)
    ax.set_title("(b) Full outcome distribution by training seed", pad=4)
    save(fig, "mnist_full_balance")


# --------------------------------------------------------------------------- Fig. 8
def fig_t2i():
    fig, axes = plt.subplots(2, 2, figsize=(S.COL_W, 2.55), sharex=True,
                             gridspec_kw=dict(wspace=0.08, hspace=0.42))
    titles = {"sampling_latent": "Sampling latent", "image_reencoding": "Image re-encoding",
              "dinov2_image": "DINOv2 image", "clip_image": "CLIP image"}
    fam = {"DDIM4": (S.CONTROL, "o"), "LCM4": (S.ALT, "s"), "DMD2": (S.ADVERSE, "D")}
    open_rows = {"LCM4 / 1", "DMD2 / 1.75"}  # alternate teacher (see caption)
    for ax, (key, rows) in zip(axes.flat, D.FIG8.items()):
        labels = [r[0] for r in rows]
        rows_axis(ax, labels)
        if ax in axes[:, 1]:
            ax.set_yticklabels([])
        ax.axvspan(0.9, 1.1, color=S.BAND, zorder=0, lw=0)
        ax.axvline(1.0, color=S.INK2, lw=0.7, ls="--", zorder=1)
        for i, (lab, est, lo, hi) in enumerate(rows):
            c, m = fam[lab.split(" /")[0]]
            S.ci(ax, i, est, lo, hi, c, marker=m, filled=lab not in open_rows, size=4.2)
        ax.set_xlim(0.3, 1.75)
        ax.xaxis.set_major_locator(FixedLocator([0.5, 1.0, 1.5]))
        ax.set_title(titles[key], loc="center", pad=3, fontsize=7.5)
    fig.supxlabel("Within-prompt spread relative to reference", fontsize=7.5, y=-0.01)
    save(fig, "t2i_representation_reference")


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "png"), exist_ok=True)
    for f in [fig_overview, fig_power, fig_init, fig_numerical, fig_edm, fig_mnist, fig_t2i]:
        f()
    print("done")
