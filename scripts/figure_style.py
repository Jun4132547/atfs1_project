"""Shared figure spec for Biology Open (180 x 210 mm max, 300 ppi, Arial/Helvetica).

Import once per figure notebook so nothing silently ends up on a different spec.
The look follows the convention this literature already uses - only left and bottom
axes, ticks pointing outward, frameless legends sitting inside the panel, bold
letters at the top-left corner - so the panels sit alongside published UPRmt figures
without looking like they came from somewhere else.
"""
import matplotlib as mpl
from matplotlib import font_manager

_names = {f.name for f in font_manager.fontManager.ttflist}
FONT = "Arial" if "Arial" in _names else "Helvetica"
if FONT not in _names:
    raise RuntimeError(
        "Neither Arial nor Helvetica is available to matplotlib, and the journal "
        "requires one of them. Found font families containing 'arial'/'helvetica': "
        + str(sorted(n for n in _names if "rial" in n.lower() or "elvet" in n.lower()))
    )

MM = 1 / 25.4
FULL_W = 180 * MM      # journal maximum width
THREEQ_W = 130 * MM
HALF_W = 87 * MM       # single column
MAX_H = 210 * MM       # journal maximum height

# Wong (2011) colour-blind-safe palette. Saturated enough to read at print size and
# to hold up in greyscale, which the red/green pairs common in this literature do
# not. Anything that is not the point of a panel stays grey rather than becoming a
# fourth competing accent.
BLUE = "#0072B2"      # the thing being claimed
ORANGE = "#E69F00"    # the contrast class
GREEN = "#009E73"     # third series, where a panel genuinely needs three
MAGENTA = "#CC79A7"   # fourth series
GREY = "#BDBDBD"      # context: everything that is not the point
INK = "#1A1A1A"       # text and axes

mpl.rcParams.update({
    "font.family": FONT,
    "font.size": 9,
    "axes.labelsize": 9.5,
    "axes.titlesize": 10,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.linewidth": 1.0,
    # Outward ticks with real length: the convention in this literature, and easier
    # to read against a plot area that has no grid.
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 4.0,
    "ytick.major.size": 4.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "lines.linewidth": 1.6,
    "lines.markersize": 5,
    "legend.frameon": False,
    "legend.handletextpad": 0.5,
    "legend.labelspacing": 0.35,
    "legend.borderaxespad": 0.3,
    "pdf.fonttype": 42,     # TrueType: text stays real text in the PDF, not outlines
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "figure.dpi": 150,       # screen preview only
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})


def panel_label(ax, letter, dx=-0.16, dy=1.08):
    """Bold uppercase panel letter at the top-left corner of an axes."""
    ax.text(dx, dy, letter.upper(), transform=ax.transAxes,
            fontsize=13, fontweight="bold", va="top", ha="left", color=INK)


def figure_label(fig, letter, x, y):
    """Panel letter placed in figure coordinates, for panels positioned with
    add_axes() where an axes-relative offset would land inconsistently."""
    fig.text(x, y, letter.upper(), fontsize=13, fontweight="bold",
             va="top", ha="left", color=INK)


def save(fig, name):
    """Write PDF (submission), SVG (editable), and PNG (preview) to figures/."""
    import os
    os.makedirs("figures", exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(f"figures/{name}.{ext}")
    print(f"Saved figures/{name}.{{pdf,svg,png}}")
