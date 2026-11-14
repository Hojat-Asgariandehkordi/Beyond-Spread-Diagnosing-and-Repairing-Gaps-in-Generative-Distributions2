"""Dump text spans and vector primitives of a one-page figure PDF.

Used once to recover plotted numbers from the draft figures when they were
not printed in the manuscript. Coordinates are PDF points, y downwards.
"""
import sys, pymupdf as fitz

def load(path):
    page = fitz.open(path)[0]
    texts = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                x0, y0, x1, y1 = s["bbox"]
                texts.append(dict(t=s["text"].strip(), x=(x0+x1)/2, y=(y0+y1)/2, bbox=s["bbox"], size=s["size"]))
    draws = []
    for d in page.get_drawings():
        r = d["rect"]
        draws.append(dict(cx=(r.x0+r.x1)/2, cy=(r.y0+r.y1)/2, w=r.width, h=r.height,
                          fill=d.get("fill"), color=d.get("color"), items=d["items"], lw=d.get("width")))
    return page, texts, draws

def hexc(c):
    return None if c is None else "#%02x%02x%02x" % tuple(int(round(v*255)) for v in c[:3])

if __name__ == "__main__":
    page, texts, draws = load(sys.argv[1])
    print("page", page.rect)
    for t in texts:
        if t["t"]: print("T %7.2f %7.2f %s" % (t["x"], t["y"], t["t"]))
    for d in draws:
        kinds = "".join(i[0] for i in d["items"])
        print("D %7.2f %7.2f w%6.2f h%6.2f fill=%s col=%s lw=%s %s" % (d["cx"], d["cy"], d["w"], d["h"], hexc(d["fill"]), hexc(d["color"]), d["lw"], kinds[:12]))
