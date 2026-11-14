"""Recover plotted values from the draft's main-paper figure PDFs.

The draft figures were produced by an analysis pipeline we do not have. Many
per-arm intervals are not printed in the manuscript, so this script reads them
back from the vector geometry (marker centres, interval-line endpoints) using a
linear (or log) calibration from the tick labels. Output: recovered.json.
Every value printed in the paper is cross-checked in check_recovered.py.

Usage: python3 -I scripts/recover/recover_main.py figures/draft_originals scripts/recover/recovered.json
"""
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from vecdump import load, hexc

FIG = sys.argv[1]
OUT = sys.argv[2]


def num(s):
    s = s.replace(",", "").replace("−", "-").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


def calib(texts, xr, yr, axis="x", log=False):
    """Fit value = a*coord + b from numeric tick labels inside a box."""
    pts = []
    for t in texts:
        v = num(t["t"])
        if v is None:
            continue
        if xr[0] <= t["x"] <= xr[1] and yr[0] <= t["y"] <= yr[1]:
            c = t["x"] if axis == "x" else t["y"]
            pts.append((c, math.log10(v) if log else v))
    assert len(pts) >= 2, (xr, yr, pts)
    (c0, v0), (c1, v1) = min(pts), max(pts)
    a = (v1 - v0) / (c1 - c0)
    b = v0 - a * c0
    # residual check on all ticks
    res = max(abs(a * c + b - v) for c, v in pts)
    assert res < 1e-2 * max(1, abs(v1)), ("bad calibration", pts, res)
    f = (lambda c: 10 ** (a * c + b)) if log else (lambda c: a * c + b)
    return f


def markers(draws, xr, yr):
    out = []
    for d in draws:
        if not (xr[0] <= d["cx"] <= xr[1] and yr[0] <= d["cy"] <= yr[1]):
            continue
        if 2.4 <= d["w"] <= 4.6 and 2.4 <= d["h"] <= 4.6 and d["fill"] is not None:
            col = hexc(d["color"]) if hexc(d["fill"]) == "#ffffff" else hexc(d["fill"])
            out.append(dict(x=d["cx"], y=d["cy"], col=col))
    return out


def ci_for(draws, m):
    """Horizontal interval line through marker m (same colour)."""
    best = None
    for d in draws:
        if d["h"] < 0.05 and d["w"] > 0.3 and hexc(d["color"]) == m["col"] and abs(d["cy"] - m["y"]) < 0.4 \
                and d["cx"] - d["w"] / 2 - 0.5 <= m["x"] <= d["cx"] + d["w"] / 2 + 0.5 and (d["lw"] or 0) > 1.0:
            if best is None or d["w"] > best["w"]:
                best = d
    if best is None:
        return None
    return best["cx"] - best["w"] / 2, best["cx"] + best["w"] / 2


def row_label(texts, y, xmax):
    cands = [t for t in texts if t["x"] < xmax and abs(t["y"] - y) < 3.5 and num(t["t"]) is None and t["t"]]
    return min(cands, key=lambda t: abs(t["y"] - y))["t"] if cands else None


def forest(path, panels):
    """panels: list of (name, xr, yr_markers, tick_yr, log)."""
    _, texts, draws = load(path)
    res = {}
    for name, xr, yr, tyr, log in panels:
        f = calib(texts, xr, tyr, log=log)
        rows = []
        for m in sorted(markers(draws, xr, yr), key=lambda m: m["y"]):
            ci = ci_for(draws, m)
            rows.append(dict(label=row_label(texts, m["y"], xr[0] + 2 if xr[0] > 60 else 75), y=round(m["y"], 2), col=m["col"],
                             est=f(m["x"]), lo=f(ci[0]) if ci else None, hi=f(ci[1]) if ci else None))
        res[name] = rows
    return res


def ycalib(texts, draws, tick_xr, yr, log=False):
    """y calibration from horizontal tick marks (w=2.8) paired with labels."""
    ticks = [d for d in draws if abs(d["w"] - 2.8) < 0.05 and d["h"] < 0.05 and yr[0] - 3 <= d["cy"] <= yr[1] + 3
             and tick_xr[0] <= d["cx"] <= tick_xr[1] + 12]
    pts = []
    for t in texts:
        v = num(t["t"])
        if v is None or not (tick_xr[0] <= t["x"] <= tick_xr[1] and yr[0] - 3 <= t["y"] <= yr[1] + 3):
            continue
        tk = min(ticks, key=lambda d: abs(d["cy"] - t["y"]))
        assert abs(tk["cy"] - t["y"]) < 3, (t, tk)
        pts.append((tk["cy"], math.log10(v) if log else v))
    (c0, v0), (c1, v1) = min(pts), max(pts)
    a = (v1 - v0) / (c1 - c0); b = v0 - a * c0
    assert max(abs(a * c + b - v) for c, v in pts) < 1e-3 * max(1, abs(v1)), pts
    return (lambda c: 10 ** (a * c + b)) if log else (lambda c: a * c + b)


def polyline_pts(d):
    pts = []
    for it in d["items"]:
        if it[0] == "l":
            for p in it[1:3]:
                if not pts or abs(pts[-1][0] - p.x) > 1e-3 or abs(pts[-1][1] - p.y) > 1e-3:
                    pts.append((p.x, p.y))
    return pts


def lines(path, panels, xvals):
    """Line plots: vertices of each coloured polyline (one per series)."""
    _, texts, draws = load(path)
    res = {}
    for name, xr, yr, tick_xr, log in panels:
        fy = ycalib(texts, draws, tick_xr, yr, log=log)
        series = {}
        for d in draws:
            if d["fill"] is None and d["color"] is not None and len(d["items"]) >= 2 and d["w"] > 30 \
                    and xr[0] <= d["cx"] <= xr[1] and yr[0] <= d["cy"] <= yr[1] and (d["lw"] or 0) > 1.0:
                pts = polyline_pts(d)
                if len(pts) == len(xvals):
                    series[hexc(d["color"])] = [(x, fy(y)) for x, y in pts]
        res[name] = {}
        for col, pts in series.items():
            pts.sort()
            res[name][col] = [v for _, v in pts]
        res[name]["x"] = xvals
    return res


R = {}
R["overview"] = forest(os.path.join(FIG, "overview.pdf"), [
    ("cifar_kid_x1e3", (75, 236), (10, 40), (45, 52), False),
    ("mnist_class_mass_err_pct", (75, 236), (80, 106), (112, 118), False)])

R["init_b"] = forest(os.path.join(FIG, "initialization_repair.pdf"), [
    ("kid_x1e3", (75, 236), (110, 152), (158, 165), False)])
R["init_a"] = lines(os.path.join(FIG, "initialization_repair.pdf"), [
    ("variance_ratio", (44, 150), (20, 70), (20, 36), False)], [1, 2, 4, 8])

R["numerical"] = forest(os.path.join(FIG, "numerical_repair.pdf"), [
    ("pixel_spread", (48, 108), (25, 66), (73, 80), False),
    ("coverage", (110, 170), (25, 66), (73, 80), False),
    ("kid_x1e3", (172, 236), (25, 66), (73, 80), False)])

R["edm"] = lines(os.path.join(FIG, "edm_solver_audit.pdf"), [
    ("kid_x1e3", (34, 115), (18, 80), (10, 30), True),
    ("coverage", (148, 230), (20, 80), (128, 145), False)], [3, 7, 15, 35])

with open(OUT, "w") as fh:
    json.dump(R, fh, indent=1)
print(json.dumps(R, indent=1)[:6000])

# ---- T2I within-prompt spread ratios (2x2 panels, 5 rows each) -------------
R["t2i"] = forest(os.path.join(FIG, "t2i_representation_reference.pdf"), [
    ("sampling_latent", (50, 140), (15, 66), (72, 79), False),
    ("image_reencoding", (142, 236), (15, 66), (72, 79), False),
    ("dinov2_image", (50, 140), (92, 142), (148, 155), False),
    ("clip_image", (142, 236), (92, 142), (148, 155), False)])


# ---- Support power: vertical CI lines --------------------------------------
def power(path):
    _, texts, draws = load(path)
    fx = calib(texts, (40, 225), (100, 108), log=True)
    fy = ycalib(texts, draws, (25, 40), (20, 98))
    out = {}
    for m in markers(draws, (45, 225), (20, 98)):
        vl = [d for d in draws if d["w"] < 0.05 and hexc(d["color"]) == m["col"] and abs(d["cx"] - m["x"]) < 0.3
              and d["cy"] - d["h"] / 2 - 0.3 <= m["y"] <= d["cy"] + d["h"] / 2 + 0.3 and (d["lw"] or 0) > 1.0]
        lo = hi = fy(m["y"])
        if vl:
            v = max(vl, key=lambda d: d["h"]); hi, lo = fy(v["cy"] - v["h"] / 2), fy(v["cy"] + v["h"] / 2)
        out.setdefault(m["col"], []).append(dict(n=round(fx(m["x"])), est=fy(m["y"]), lo=lo, hi=hi))
    for c in out:
        out[c].sort(key=lambda r: r["n"])
    return out
R["power"] = power(os.path.join(FIG, "support_power_main.pdf"))


# ---- MNIST full balance ----------------------------------------------------
def mnist(path):
    _, texts, draws = load(path)
    fy = ycalib(texts, draws, (20, 35), (40, 96))
    fy2 = ycalib(texts, draws, (20, 35), (140, 176))
    xs = {t["t"]: t["x"] for t in texts if t["y"] > 104 and t["y"] < 109}
    gaps = {}
    for m in markers(draws, (40, 236), (25, 100)):
        if any(abs(m["y"] - t["y"]) < 2 and 0 < t["bbox"][0] - m["x"] < 8 and t["t"] in ("Keep targeting", "Ordinary data") for t in texts):  # legend swatch
            continue
        key = min(xs, key=lambda k: abs(xs[k] - m["x"]))
        gaps.setdefault(m["col"], {})[key] = fy(m["y"])
    tv = []
    for d in draws:
        if d["fill"] is None and hexc(d["color"]) == "#4a5c70" and d["w"] > 100 and d["cy"] > 130:
            pts = polyline_pts(d)
            dash = d.get("dashes")
            tv.append(dict(left=fy2(pts[0][1]), right=fy2(pts[-1][1])))
    return dict(gaps_pp=gaps, tv_pct_by_seed=tv)
R["mnist"] = mnist(os.path.join(FIG, "mnist_full_balance.pdf"))

with open(OUT, "w") as fh:
    json.dump(R, fh, indent=1)
