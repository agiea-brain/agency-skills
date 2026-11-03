#!/usr/bin/env python3
"""Render a performance-review Markdown file into a clean .docx that converts well to Google Docs.

Google Docs' own tables wrap and crowd because nobody sets column widths, padding or borders.
This sets all three, right-aligns numbers, and draws charts as images, so the doc reads cleanly
and stays commentable once it is uploaded to Drive (Drive converts .docx to a Google Doc).

Input is ordinary Markdown plus three conventions:
  | pipe tables |            first row is the header. A row whose every filled cell is **bold**
                             is a group/total row (bold, rule above). Numeric columns right-align.
  <!-- table: widths=40,12,12,12,12,12 -->   optional, on the line before a table: column % widths
  ```chart  {json}  ```      a chart (see CHART TYPES below); rendered with matplotlib
  > **Takeaway.** text       a shaded callout (use for the one line a reader must not miss)
  ---                        page break

CHART TYPES (json "type"):
  hbar    {"labels":[...], "values":[...], "fmt":"{:.1f}", "highlight":["Video"], "ref": 4.2, "ref_label":"avg"}
  bar     {"labels":[...], "series":{"Emails":[...], ...}}           grouped vertical bars
  line    {"labels":[...], "series":{"Reply %":[...]}, "fmt":"{:.1f}%"}
  funnel  {"labels":[...], "values":[...]}                            stage counts, top to bottom
Every chart takes "title" (the takeaway, not the axis name) and optional "note" (source line).

Usage:
  python3 build_review_doc.py review.md -o review.docx [--pdf]
  --pdf also writes review.pdf via LibreOffice, so you can eyeball it before uploading.
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

try:
    from docx import Document
    from docx.enum.section import WD_ORIENT  # noqa: F401
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    sys.exit("pip install python-docx matplotlib  (a venv is fine)")

# ---- house style: one place to change it ----
FONT = "Inter"            # a Google Font, so it survives conversion; falls back to Arial
INK = RGBColor(0x1F, 0x23, 0x28)
MUTED = RGBColor(0x5F, 0x63, 0x68)
ACCENT_HEX = "#2F5BEA"
GREY_HEX = "#C4C9D0"
RULE = "D9DCE1"           # hairline between rows
HEAD_RULE = "1F2328"      # rule under the header
GROUP_FILL = "F3F4F6"
CALLOUT_FILL = "EEF2FD"
PAGE_W_IN = 6.5           # Letter with 1in margins
BODY_PT, TABLE_PT, HEAD_PT = 10.5, 9.5, 9

NUM_RE = re.compile(r"^[~<>≈$€£+\-−]?\s?[\d,.]+\s?(%|x|k|m|K|M|pts?)?(\s*\(.*\))?$|^[ - --]$|^0$")


def set_cell_borders(cell, top=None, bottom=None):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side, spec in (("top", top), ("bottom", bottom), ("left", None), ("right", None)):
        el = OxmlElement(f"w:{side}")
        if spec:
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(spec[0])); el.set(qn("w:color"), spec[1])
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)
    tcPr.append(borders)


def set_cell_fill(cell, hex_fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_fill)
    cell._tc.get_or_add_tcPr().append(shd)


def set_cell_margins(table, top=70, bottom=70, left=90, right=90):  # twips (20 = 1pt)
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side, v in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        el = OxmlElement(f"w:{side}"); el.set(qn("w:w"), str(v)); el.set(qn("w:type"), "dxa"); mar.append(el)
    tblPr.append(mar)


def fix_grid(table, widths):
    """Fixed layout + explicit grid. Without the grid, LibreOffice and Drive's importer ignore cell widths."""
    tblPr = table._tbl.tblPr
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(PAGE_W_IN * 1440))); tw.set(qn("w:type"), "dxa"); tblPr.append(tw)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for gc, w in zip(table._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(PAGE_W_IN * 1440 * w / 100)))


def add_runs(par, text, size=BODY_PT, color=INK, bold=False):
    """Inline **bold** and *italic*; nothing else."""
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not part:
            continue
        b, i = bold, False
        if part.startswith("**") and part.endswith("**"):
            part, b = part[2:-2], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, i = part[1:-1], True
        r = par.add_run(part)
        r.bold, r.italic = b, i
        r.font.size, r.font.color.rgb, r.font.name = Pt(size), color, FONT


def para(doc, text="", size=BODY_PT, color=INK, space_after=6, bold=False, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.2
    if align:
        p.alignment = align
    add_runs(p, text, size, color, bold)
    return p


def is_num(s):
    s = s.replace("**", "").strip()
    return bool(s) and bool(NUM_RE.match(s))


def auto_widths(rows):
    """Width by the longest token a column must show unbroken, capped, first column widest."""
    n = len(rows[0])
    need = []
    for c in range(n):
        cells = [r[c].replace("**", "") for r in rows if c < len(r)]
        longest_word = max((len(w) for v in cells for w in v.split()), default=4)
        typical = sorted(len(v) for v in cells)[len(cells) // 2] if cells else 4
        need.append(max(longest_word, min(typical, 28 if c == 0 else 14), 5))
    tot = sum(need)
    return [w / tot * 100 for w in need]


def add_table(doc, rows, widths=None):
    header, body = rows[0], rows[1:]
    n = len(header)
    widths = widths or auto_widths(rows)
    numeric = [c > 0 and sum(is_num(r[c]) for r in body if c < len(r)) >= max(1, len(body) * 0.6) for c in range(n)]
    t = doc.add_table(rows=len(rows), cols=n)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    set_cell_margins(t)
    fix_grid(t, widths)
    for ri, row in enumerate(rows):
        is_head = ri == 0
        filled = [c.strip() for c in row if c.strip()]
        is_group = not is_head and bool(filled) and all(c.startswith("**") and c.endswith("**") for c in filled)
        for ci in range(n):
            cell = t.cell(ri, ci)
            cell.width = Inches(PAGE_W_IN * widths[ci] / 100)
            txt = row[ci].strip() if ci < len(row) else ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            if numeric[ci]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if is_head:
                add_runs(p, txt.replace("**", ""), HEAD_PT, MUTED, bold=True)
                set_cell_borders(cell, bottom=(8, HEAD_RULE))
            else:
                add_runs(p, txt, TABLE_PT, INK, bold=is_group)
                set_cell_borders(cell, top=(6, "9AA0A6") if is_group and ri > 1 else None, bottom=(4, RULE))
                if is_group:
                    set_cell_fill(cell, GROUP_FILL)
    # repeat header row across pages, keep rows from splitting
    trPr = t.rows[0]._tr.get_or_add_trPr(); h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)
    for r in t.rows:
        cs = OxmlElement("w:cantSplit"); cs.set(qn("w:val"), "true"); r._tr.get_or_add_trPr().append(cs)
    para(doc, "", space_after=4)


def render_chart(spec, out_png):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker  # noqa: F401
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    fam = next((n for n in (FONT, "Helvetica Neue", "Arial") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": fam, "font.size": 9, "axes.edgecolor": GREY_HEX,
                         "axes.labelcolor": "#5F6368", "xtick.color": "#5F6368", "ytick.color": "#1F2328"})
    kind, labels = spec["type"], spec["labels"]
    fmt = spec.get("fmt", "{:,.0f}")
    hl = set(spec.get("highlight", []))
    h = spec.get("height") or (max(1.6, 0.32 * len(labels) + 0.5) if kind in ("hbar", "funnel") else 2.4)
    fig, ax = plt.subplots(figsize=(PAGE_W_IN, h), dpi=200)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if kind in ("hbar", "funnel"):
        vals = spec["values"]
        colors = [ACCENT_HEX if (not hl or l in hl) else GREY_HEX for l in labels]
        y = range(len(labels))[::-1]
        if kind == "funnel":
            colors = [ACCENT_HEX] * len(labels)
            if spec.get("log", True):
                ax.set_xscale("log")
            ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.barh(list(y), vals, color=colors, height=0.62)
        ax.set_yticks(list(y)); ax.set_yticklabels(labels)
        ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
        ax.set_xticks([]); ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator()); ax.tick_params(axis="y", length=0)
        vmax = max(vals) or 1
        for yi, v in zip(y, vals):
            ax.text(v * (1.04 if kind == "funnel" else 1) + (0 if kind == "funnel" else vmax * 0.015), yi,
                    fmt.format(v), va="center", fontsize=8.5, color="#1F2328",
                    bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"), zorder=5)
        if "ref" in spec:
            ax.axvline(spec["ref"], color="#5F6368", lw=0.8, ls=(0, (3, 3)))
            ax.text(spec["ref"], len(labels) - 0.4, " " + spec.get("ref_label", "avg"), fontsize=8, color="#5F6368")
        ax.set_xlim(right=vmax * (3 if kind == "funnel" else 1.15))
    else:
        series = spec["series"]
        palette = [ACCENT_HEX, "#9AA0A6", "#F29D38", "#34A853"]
        x = range(len(labels))
        if kind == "bar":
            k = len(series); w = 0.8 / k
            for i, (name, vals) in enumerate(series.items()):
                xs = [xi - 0.4 + w * (i + 0.5) for xi in x]
                bars = ax.bar(xs, vals, w * 0.9, label=name, color=palette[i % 4])
                for b, v in zip(bars, vals):
                    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt.format(v), ha="center",
                            va="bottom", fontsize=7.5, color="#1F2328")
        else:
            for i, (name, vals) in enumerate(series.items()):
                ax.plot(list(x), vals, marker="o", ms=3.5, lw=1.8, label=name, color=palette[i % 4])
                ax.text(len(labels) - 1 + 0.08, vals[-1], fmt.format(vals[-1]), va="center", fontsize=8,
                        color=palette[i % 4])
        ax.set_xticks(list(x)); ax.set_xticklabels(labels)
        ax.yaxis.grid(True, color="#EEF0F2", lw=0.8); ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0, labelcolor="#5F6368")
        if len(series) > 1:
            ax.legend(frameon=False, fontsize=8, loc="upper left", ncol=len(series), bbox_to_anchor=(0, 1.12))
    fig.tight_layout()
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    plt.close(fig)


def add_chart(doc, spec, tmpdir, idx):
    if spec.get("title"):
        para(doc, spec["title"], size=10, bold=True, space_after=2)
    png = Path(tmpdir) / f"chart{idx}.png"
    render_chart(spec, png)
    doc.add_picture(str(png), width=Inches(PAGE_W_IN))
    if spec.get("note"):
        para(doc, spec["note"], size=8.5, color=MUTED, space_after=8)


def add_callout(doc, text):
    t = doc.add_table(rows=1, cols=1)
    set_cell_margins(t, 110, 110, 160, 160)
    fix_grid(t, [100])
    c = t.cell(0, 0); c.width = Inches(PAGE_W_IN)
    set_cell_fill(c, CALLOUT_FILL); set_cell_borders(c)
    p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
    add_runs(p, text, BODY_PT)
    para(doc, "", space_after=2)


def build(md_text, out_path):
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Inches(1); sec.top_margin = sec.bottom_margin = Inches(0.9)
    st = doc.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(BODY_PT)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    for lvl, size in ((1, 20), (2, 14), (3, 11.5)):
        hs = doc.styles[f"Heading {lvl}"]
        hs.font.name, hs.font.size, hs.font.bold, hs.font.color.rgb = FONT, Pt(size), True, INK
        hs.paragraph_format.space_before = Pt({1: 0, 2: 18, 3: 12}[lvl])
        hs.paragraph_format.space_after = Pt(6 if lvl > 1 else 4)
        hs.paragraph_format.keep_with_next = True

    lines = md_text.splitlines()
    i, chart_n, pending_widths = 0, 0, None
    tmp = tempfile.mkdtemp()
    while i < len(lines):
        ln = lines[i].rstrip()
        m = re.match(r"<!--\s*table:\s*widths=([\d,\s.]+)-->", ln)
        if m:
            pending_widths = [float(x) for x in m.group(1).split(",")]; i += 1; continue
        if ln.startswith("```chart"):
            j = i + 1; buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            add_chart(doc, json.loads("\n".join(buf)), tmp, chart_n); chart_n += 1
            i = j + 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            add_table(doc, rows, pending_widths); pending_widths = None; continue
        if ln.strip() == "---":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE); i += 1; continue
        if ln.startswith("#"):
            lvl = len(ln) - len(ln.lstrip("#"))
            h = doc.add_heading(level=min(lvl, 3)); add_runs(h, ln.lstrip("# ").strip(), {1: 20, 2: 14, 3: 11.5}[min(lvl, 3)], INK, True)
            i += 1; continue
        if ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ").strip()); i += 1
            add_callout(doc, " ".join(buf)); continue
        if re.match(r"^(\s*)([-*]|\d+\.)\s", ln):
            numbered = bool(re.match(r"^\s*\d+\.", ln))
            p = doc.add_paragraph(style="List Number" if numbered else "List Bullet")
            p.paragraph_format.space_after = Pt(3)
            add_runs(p, re.sub(r"^\s*([-*]|\d+\.)\s", "", ln)); i += 1; continue
        if ln.startswith("_") and ln.endswith("_"):
            para(doc, ln.strip("_"), size=8.5, color=MUTED); i += 1; continue
        if ln.strip():
            p = para(doc, ln.strip())
            nxt = next((l for l in lines[i + 1:] if l.strip()), "")
            if nxt.startswith(("|", "<!-- table", "```chart")):
                p.paragraph_format.keep_with_next = True  # a table's label never strands at a page foot
        i += 1
    doc.save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md"); ap.add_argument("-o", "--out"); ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    out = Path(a.out or Path(a.md).with_suffix(".docx"))
    build(Path(a.md).read_text(), out)
    print(f"wrote {out}")
    if a.pdf:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out.parent), str(out)],
                       check=True, capture_output=True)
        print(f"wrote {out.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
