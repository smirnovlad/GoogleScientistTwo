"""Count the task slots of Figure 1b (the teaser's ring of bars) and bin the bars by legend colour.

Why this exists: the paper says ScientistTwo improves 86 of 107 tasks [Fig. 1 caption] with a mean
relative gain of 25.2% and a median of 7.7% [Tab. 4]. Figure 1b is the only per-task view of those
gains that the paper prints, and its values are not in the TeX. docs/paper/claims.md cites this output.

Method: render src/figures/sc2_new_fig2.pdf at 600 dpi (pdftoppm); fit the "Human SOTA" ring (RGB
76,95,204) by least squares; walk a circle 30 px outside the ring in 0.01-degree steps; count runs of
bar-coloured pixels at least 1 degree wide; measure the angular gaps between consecutive bars in units
of the median bar-to-bar spacing (one task slot). Each bar goes to the legend bin whose colour is
nearest (L1) to the bar's median colour; the six legend colours are read from the legend itself.

Caveat: the bars are drawn with a continuous colour scale, so a bar near a bin edge can land in the
neighbouring bin. The bar and slot counts do not depend on colour; the per-bin counts are approximate.
Bar lengths are printed per bin as a cross-check (they should rise from bin to bin).

Usage: python3 playground/paper/fig1b_bars.py   (needs pdftoppm, numpy, Pillow and the paper cache)
"""

import math
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FIGURE = ROOT / ".cache/paper/2609.19644v1/src/figures/sc2_new_fig2.pdf"
BINS = ["0-10%", "10-25%", "25-50%", "50-75%", "75-100%", ">100%"]   # legend order, light to dark
RING = np.array((76, 95, 204))


def render() -> np.ndarray:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "600", "-png", str(FIGURE), f"{tmp}/fig"], check=True,
                       stderr=subprocess.DEVNULL)
        png = next(Path(tmp).glob("fig*.png"))
        return np.array(Image.open(png).convert("RGB")).astype(int)


def legend_colours(im: np.ndarray) -> dict:
    """The six most frequent greens in the legend strip, ordered from light to dark."""
    h, w, _ = im.shape
    strip = im[: int(h * 0.16), w // 2:].reshape(-1, 3)
    green = strip[(strip[:, 1] > strip[:, 0] + 20) & (strip[:, 1] > strip[:, 2] + 10) & (strip.max(1) < 250)]
    top = [np.array(c) for c, _ in Counter(map(tuple, green)).most_common(6)]
    top.sort(key=lambda c: -(0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]))
    return dict(zip(BINS, top))


def fit_ring(im: np.ndarray):
    h, w, _ = im.shape
    mask = np.abs(im - RING).sum(axis=2) < 25
    mask[:, : w // 2] = False
    mask[: int(h * 0.16), :] = False            # the legend's own blue line
    ys, xs = np.nonzero(mask)
    a = np.c_[2 * xs, 2 * ys, np.ones(len(xs))]
    cx, cy, c = np.linalg.lstsq(a, xs ** 2 + ys ** 2, rcond=None)[0]
    return cx, cy, math.sqrt(c + cx ** 2 + cy ** 2)


def main() -> int:
    im = render()
    h, w, _ = im.shape
    legend = legend_colours(im)
    cx, cy, radius = fit_ring(im)

    def px(angle, r):
        x, y = int(round(cx + r * math.cos(angle))), int(round(cy - r * math.sin(angle)))
        return im[y, x] if (0 <= x < w and 0 <= y < h) else np.array((255, 255, 255))

    def is_bar(c):
        return c[1] > c[0] + 15 and c[1] > c[2] + 10 and c.min() < 235

    step, r0 = 0.01, radius + 30
    ring = "".join("B" if is_bar(px(math.radians(i * step), r0)) else "." for i in range(36000))
    shift = ring.find(".")
    ring = ring[shift:] + ring[:shift]
    bars, i = [], 0
    while i < len(ring):
        j = i
        while j < len(ring) and ring[j] == ring[i]:
            j += 1
        if ring[i] == "B" and j - i >= 100:          # at least 1 degree wide
            bars.append((i, j))
        i = j
    centres = [(a + b) / 2 for a, b in bars]
    gaps = [(centres[(k + 1) % len(centres)] - centres[k]) % 36000 for k in range(len(centres))]
    slot = float(np.median(gaps))
    empty = sum(round(g / slot) - 1 for g in gaps if round(g / slot) > 1)

    counts, lengths = Counter(), {b: [] for b in BINS}
    for a, b in bars:
        mid = math.radians(((a + b) / 2 + shift) * step)
        cols, r = [], r0
        while is_bar(px(mid, r)):
            cols.append(px(mid, r))
            r += 1
        cols = np.array(cols)
        median = np.median(cols[len(cols) // 4: max(len(cols) // 4 + 1, 3 * len(cols) // 4)], axis=0)
        best = min(BINS, key=lambda k: np.abs(median - legend[k]).sum())
        counts[best] += 1
        lengths[best].append(int(r - radius))

    print(f"ring centre ({cx:.0f}, {cy:.0f}) px, radius {radius:.0f} px at 600 dpi")
    print(f"bars: {len(bars)}; slot width {slot * step:.2f} deg -> {36000 / slot:.1f} slots; empty slots: {empty}")
    print(f"bars + empty slots = {len(bars) + empty}")
    lower = {"0-10%": 0, "10-25%": 10, "25-50%": 25, "50-75%": 50, "75-100%": 75, ">100%": 100}
    for b in BINS:
        span = f"{min(lengths[b])}-{max(lengths[b])}" if lengths[b] else "-"
        print(f"  {b:8s} {counts[b]:3d} bars   bar length beyond the ring: {span} px")
    floor = sum(counts[b] * lower[b] for b in BINS) / max(1, len(bars))
    print(f"mean gain implied by the bins' lower edges: >= {floor:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
