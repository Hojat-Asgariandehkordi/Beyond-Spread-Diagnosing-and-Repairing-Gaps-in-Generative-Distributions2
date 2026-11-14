"""Cut BioRender art into the pieces used by Fig. 1. Run: python3 -I scripts/br_assets.py

Source: figures/biorender/br_overview_v1.png (BioRender figure b1c851eaaafec41f3d44c9e5,
2752x1536). Only pictorial art is reused (photo thumbnails, network icon); BioRender's
lettering and its panel B/C diagrams are not used (panel B mislabelled the depleted region,
panel C truncated the reference decomposition). All labels are typeset in Times by
fig_pipeline.py.
"""
import os
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "figures", "biorender", "br_overview_v1.png")
OUT = os.path.join(HERE, "..", "figures", "biorender", "assets")

# Photo boxes (x, y, w, h) found by connected components on the card interior.
REF = [(72, 220), (164, 220), (255, 220), (347, 220), (72, 310), (164, 311), (255, 310), (347, 311)]
CAND = [(72, 567), (164, 567), (256, 567), (347, 567), (72, 658), (164, 657), (256, 658), (347, 658)]
SIDE = 84          # common square crop inside each photo (drops the 1-2 px anti-aliased rim)
INSET = 1
REF_PICK = [0, 1, 2, 3, 4, 6]   # both seascapes kept: none appears among the candidates
CAND_PICK = [0, 1, 2, 3, 5, 6]
NET_BOX = (630, 400, 175, 135)  # network icon inside the "Feature map" card


def main():
    os.makedirs(OUT, exist_ok=True)
    im = cv2.imread(SRC, cv2.IMREAD_COLOR)
    assert im is not None and im.shape[:2] == (1536, 2752), "unexpected BioRender export size"
    for name, boxes, pick in (("ref", REF, REF_PICK), ("cand", CAND, CAND_PICK)):
        for k, i in enumerate(pick):
            x, y = boxes[i]
            crop = im[y + INSET:y + INSET + SIDE, x + INSET:x + INSET + SIDE]
            cv2.imwrite(os.path.join(OUT, f"{name}_{k}.png"), crop)
    # network icon: card background -> transparent, keep dark strokes
    x, y, w, h = NET_BOX
    crop = im[y:y + h, x:x + w].astype(np.float32)
    bg = np.median(np.concatenate([crop[:4].reshape(-1, 3), crop[-4:].reshape(-1, 3)]), 0)
    dist = np.abs(crop - bg).sum(2)
    alpha = np.clip((dist - 20) / 120, 0, 1)
    ink = np.full_like(crop, (60, 60, 60))  # recolour strokes to the figure's ink gray (BGR)
    rgba = np.dstack([ink, alpha * 255]).astype(np.uint8)
    ys, xs = np.where(alpha > 0.05)
    rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(os.path.join(OUT, "network.png"), rgba)
    print("assets written to", os.path.relpath(OUT))


if __name__ == "__main__":
    main()
