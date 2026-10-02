"""Show that Figure 10b prints a label for its smallest slice, Seed Idea Generation, in both donuts.

Why this exists: the persona review (fix-list F-CL-7) said the slice "has no printed label". The
figure is a raster, so its text layer cannot settle it; this script reads the raster itself.
docs/paper/claims/discussion.md (C-DISC-2) cites its output.

Method: extract the embedded rasters of src/figures/scientisttwo_cost.pdf (pdfimages), take the
2048 x 1174 donut raster, count dark text pixels in a small box above each donut's top (the label
row, clear of the legend text above it), and write a 5x nearest-neighbour crop for a human to read.

Usage: python3 playground/paper/fig10_seed_labels.py   (needs pdfimages, numpy, Pillow, the cache)
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FIGURE = ROOT / ".cache/paper/2609.19644v1/src/figures/scientisttwo_cost.pdf"
BOXES = {"time donut": (470, 148, 520, 166), "cost donut": (1570, 148, 1620, 166)}   # x0, y0, x1, y1


def main() -> int:
    out = Path(tempfile.mkdtemp()) / "fig10_seed_labels.png"
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-j", str(FIGURE), f"{tmp}/img"], check=True)
        donut = next(p for p in sorted(Path(tmp).glob("img-*.jpg")) if Image.open(p).size == (2048, 1174))
        image = Image.open(donut).convert("RGB")
    pixels = np.array(image).astype(int)
    luminance = 0.299 * pixels[..., 0] + 0.587 * pixels[..., 1] + 0.114 * pixels[..., 2]
    tiles = []
    for name, (x0, y0, x1, y1) in BOXES.items():
        ys, xs = np.nonzero(luminance[y0:y1, x0:x1] < 120)
        found = f"x {x0 + xs.min()}-{x0 + xs.max()}, y {y0 + ys.min()}-{y0 + ys.max()}" if len(xs) else "none"
        print(f"{name}: {len(xs)} dark text pixels in the label box ({found})")
        crop = image.crop((x0 - 40, y0 - 10, x1 + 40, y1 + 25))
        tiles.append(crop.resize((crop.size[0] * 5, crop.size[1] * 5), Image.NEAREST))
    sheet = Image.new("RGB", (sum(t.size[0] for t in tiles) + 20, tiles[0].size[1]), "white")
    sheet.paste(tiles[0], (0, 0))
    sheet.paste(tiles[1], (tiles[0].size[0] + 20, 0))
    sheet.save(out)
    print(f"5x crop of both labels, for reading: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
