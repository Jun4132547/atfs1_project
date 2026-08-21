"""Shared renderer for the manuscript's data tables (Table 1, Table S1, Table S2).

Follows the plain three-line convention this literature uses for tables - a rule
above the header, a rule under it, a rule at the foot, no vertical gridlines, no
shading. Pages are sized to the same Biology Open spec as the figures and share
their font, so a table and a figure sitting side by side in the same manuscript
don't look like they came from two different tools.

Text is wrapped by measured rendered width, not by a guessed character count. A
first version wrapped on a fixed characters-per-line estimate, which does not
track how wide text actually renders at a given font size - "PF03073 (TspO_MBR)"
(19 characters) was judged short enough to leave on one line and overflowed into
the neighbouring column, invisible until the rendered page was actually opened.
"""
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D

from figure_style import FONT, INK, GREY, FULL_W, MAX_H

TABLE_FONT = 8
HEADER_FONT = 8
TITLE_FONT = 10
FOOTNOTE_FONT = 7
LINE_H = 0.155       # inches per text line at these font sizes, header or body
ROW_PAD = 0.06        # inches of extra space per row, beyond its text lines
HEADER_PAD = 0.10     # extra space between the last header line and its rule
CELL_PAD = 0.06       # inches kept clear on each side of a cell's wrap width


def _measurer():
    """A throwaway figure used only to measure how wide text actually renders,
    so wrapping is decided from real glyph widths instead of a character count."""
    fig = plt.figure()
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    def width_in(text, fontsize, weight="normal"):
        if not text:
            return 0.0
        t = fig.text(0, 0, text, fontsize=fontsize, fontweight=weight, family=FONT)
        w = t.get_window_extent(renderer=renderer).width / fig.dpi
        t.remove()
        return w

    return width_in, fig


def _wrap_to_width(text, max_width_in, measure, fontsize, weight="normal"):
    words = str(text).split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if measure(trial, fontsize, weight) <= max_width_in:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def render_table(df, columns, title, filename, footnote=None,
                  page_w=FULL_W, page_h=MAX_H, margin=0.45):
    """columns: list of dicts, each
         key      - column in df
         label    - header text (wrapped the same way as body text)
         width    - fraction of the table width (should sum to ~1.0)
         align    - "left" (default), "right", or "center"
         wrap     - True to wrap this column's body text to its column width
         format   - optional callable applied to the cell value before wrapping
    Paginates by measured height so nothing runs off the bottom of a page; the
    header repeats on every page and the footnote (if any) sits under the table
    on the last page only.
    """
    usable_w = page_w - 2 * margin
    col_w = [c["width"] * usable_w for c in columns]
    col_x, x = [], margin
    for w in col_w:
        col_x.append(x)
        x += w

    measure, measure_fig = _measurer()

    header_lines = []
    for c, w in zip(columns, col_w):
        lines = (_wrap_to_width(c["label"], w - 2 * CELL_PAD, measure, HEADER_FONT, "bold")
                 if c.get("wrap") else str(c["label"]).split("\n"))
        header_lines.append(lines)
    header_h = max(len(l) for l in header_lines) * LINE_H + HEADER_PAD

    prepared = []
    for _, row in df.iterrows():
        cells, max_lines = [], 1
        for c, w in zip(columns, col_w):
            val = c.get("format", lambda v: v)(row[c["key"]])
            text = "" if val is None else str(val)
            lines = (_wrap_to_width(text, w - 2 * CELL_PAD, measure, TABLE_FONT)
                     if c.get("wrap") else [text])
            cells.append(lines)
            max_lines = max(max_lines, len(lines))
        prepared.append((cells, max_lines))

    footnote_lines = (_wrap_to_width(footnote, page_w - 2 * margin, measure, FOOTNOTE_FONT)
                      if footnote else [])
    plt.close(measure_fig)

    top_margin, bottom_margin = 0.6, 0.55 + (0.55 if footnote else 0)
    usable_h = page_h - top_margin - bottom_margin

    pages, cur, cur_h = [], [], header_h
    for item in prepared:
        h = item[1] * LINE_H + ROW_PAD
        if cur and cur_h + h > usable_h:
            pages.append(cur)
            cur, cur_h = [], header_h
        cur.append(item)
        cur_h += h
    if cur:
        pages.append(cur)
    n_pages = len(pages)

    os.makedirs("tables", exist_ok=True)
    png_paths = []
    with PdfPages(f"tables/{filename}.pdf") as pdf:
        for pi, page_rows in enumerate(pages):
            fig = plt.figure(figsize=(page_w, page_h))
            fig.patch.set_facecolor("white")

            def hline(y, lw):
                fig.add_artist(Line2D([margin / page_w, (page_w - margin) / page_w],
                                      [y / page_h, y / page_h], color=INK,
                                      linewidth=lw, transform=fig.transFigure))

            y = page_h - top_margin
            page_note = "" if n_pages == 1 else f"  (page {pi + 1} of {n_pages})"
            fig.text(margin / page_w, (y + 0.06) / page_h, title + page_note,
                     fontsize=TITLE_FONT, fontweight="bold", family=FONT,
                     color=INK, va="bottom", ha="left")
            y -= 0.16
            hline(y, 1.2)

            for c, x0, w, lines in zip(columns, col_x, col_w, header_lines):
                ha = c.get("align", "left")
                tx = x0 + CELL_PAD if ha == "left" else (
                    x0 + w - CELL_PAD if ha == "right" else x0 + w / 2)
                for li, line in enumerate(lines):
                    fig.text(tx / page_w, (y - li * LINE_H) / page_h, line,
                             fontsize=HEADER_FONT, fontweight="bold", family=FONT,
                             color=INK, va="top", ha=ha)
            y -= header_h
            hline(y, 0.8)

            for cells, max_lines in page_rows:
                row_h = max_lines * LINE_H + ROW_PAD
                for c, x0, w, lines in zip(columns, col_x, col_w, cells):
                    ha = c.get("align", "left")
                    tx = x0 + CELL_PAD if ha == "left" else (
                        x0 + w - CELL_PAD if ha == "right" else x0 + w / 2)
                    for li, line in enumerate(lines):
                        fig.text(tx / page_w, (y - ROW_PAD / 2 - li * LINE_H) / page_h,
                                 line, fontsize=TABLE_FONT, family=FONT, color=INK,
                                 va="top", ha=ha)
                y -= row_h
            hline(y, 1.2)

            if footnote and pi == n_pages - 1:
                fy = y - 0.22
                for line in footnote_lines:
                    fig.text(margin / page_w, fy / page_h, line, fontsize=FOOTNOTE_FONT,
                             family=FONT, color=GREY, va="top", ha="left")
                    fy -= LINE_H * 0.85

            if n_pages > 1:
                fig.text(0.5, 0.02, f"{pi + 1} / {n_pages}", fontsize=FOOTNOTE_FONT,
                         family=FONT, color=GREY, ha="center", va="bottom")

            pdf.savefig(fig)
            png_path = f"tables/{filename}_page{pi + 1}.png"
            fig.savefig(png_path, dpi=200)
            png_paths.append(png_path)
            plt.close(fig)

    print(f"Wrote tables/{filename}.pdf ({n_pages} page(s)); preview PNG(s): {png_paths}")
    return n_pages
