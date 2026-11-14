"""Shared figure style for the paper (CVPR column = 3.25 in, page = 6.875 in).

Colour roles are the same in every figure:
  CONTROL  gray   baseline / control arm (standard start, DDIM, Euler)
  REPAIR   blue   the repair the paper advocates (covariance start, ordinary data)
  ADVERSE  orange the contrasting intervention (output covariance, keep targeting)
  ALT      aqua   an alternative solver / model (UniPC, DPM++, Heun, LCM)
Blue/orange/aqua is the categorical trio that passes the all-pairs colour-blind
check; marker shape is always a second encoding.
"""
import matplotlib as mpl

COL_W = 3.25
PAGE_W = 6.875

CONTROL = "#6b6a66"
REPAIR = "#2a78d6"
ADVERSE = "#eb6834"
ALT = "#1baf7a"
REF = "#2a78d6"      # reference P in schematics
GEN = "#eb6834"      # generator Q in schematics
SEQ = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]  # ordinal blue ramp (light -> dark)

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e4e3df"
BAND = "#f1f0ec"     # null-region band
HILITE = "#eaf2fc"   # row highlight for the repair arm


def apply():
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "TeX Gyre Termes", "Nimbus Roman", "Liberation Serif", "Times"],
        "mathtext.fontset": "stix",
        "font.size": 7.5,
        "axes.titlesize": 8,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": 7.5,
        "axes.labelcolor": INK,
        "axes.edgecolor": MUTED,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "lines.linewidth": 1.4,
        "lines.markersize": 4.5,
        "errorbar.capsize": 2.2,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.015,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def ci(ax, y, est, lo, hi, color, marker="o", size=4.6, filled=True, lw=1.3, zorder=3):
    """Horizontal estimate with a capped 95% interval."""
    ax.errorbar([est], [y], xerr=[[est - lo], [hi - est]], fmt="none", ecolor=color,
                elinewidth=lw, capsize=2.4, capthick=lw, zorder=zorder)
    ax.plot([est], [y], marker=marker, ms=size, color=color, mfc=color if filled else "white",
            mec=color if not filled else "white", mew=0.9 if not filled else 0.5, ls="none", zorder=zorder + 1)
