#!/usr/bin/env python3
"""Generate a Draw.io diagram from the Soundwave timeline layout."""
from pathlib import Path
import html as H

PAGE_W, PAGE_H = 2400, 1100
CONTAINER_X, CONTAINER_Y = 80, 260
CONTAINER_W, CONTAINER_H = 2200, 480
LABEL_W = 170
LANE_X = CONTAINER_X + 24 + LABEL_W
LANE_W = CONTAINER_W - 48 - LABEL_W
QUARTERS = 32
Q = LANE_W / QUARTERS
HEADER_Y = CONTAINER_Y + 70
TRACK_YS = [CONTAINER_Y + 160, CONTAINER_Y + 250, CONTAINER_Y + 340]

YEARS = list(range(1983, 1991))
QUARTER_LABELS = ["Jan", "Apr", "July", "Oct"]

BG = "#1a0b2e"
PURPLE = "#a855f7"
PURPLE_FILL = "#581c87"
PURPLE_DARK = "#0f0518"
BLUE = "#6b9aff"
BLUE_FILL = "#2d55b4"
RED = "#dc5555"
RED_FILL = "#8c1e1e"
TITLE_C = "#c084fc"
YEAR_C = "#d8b4fe"
DESC = "#c084fc"

cells = []
cid = 2


def esc(s: str) -> str:
    return H.escape(s, quote=True)


def style_box(fill, stroke, font="#e9d5ff"):
    return (
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
        f"fontColor={font};align=left;verticalAlign=top;spacing=10;"
        f"fontFamily=Helvetica;fontSize=12;strokeWidth=2;arcSize=8;"
    )


def style_bar(fill, stroke):
    return (
        f"rounded=1;fillColor={fill};strokeColor={stroke};strokeWidth=1;"
        f"arcSize=50;html=1;"
    )


def style_text(color, size=14, bold=0, align="center"):
    return (
        f"text;html=1;strokeColor=none;fillColor=none;align={align};"
        f"verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor={color};"
        f"fontSize={size};fontStyle={bold};fontFamily=Helvetica;"
    )


def vertex(value, x, y, w, h, style, parent="1", *, escape=True):
    global cid
    i = str(cid)
    cid += 1
    val = esc(value) if escape else value
    cells.append(
        f'<mxCell id="{i}" value="{val}" style="{style}" vertex="1" parent="{parent}">'
        f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/>'
        f"</mxCell>"
    )
    return i


def edge(source, target, stroke, exit_x=0.5, exit_y=1, entry_x=0, entry_y=0.5, straight=False):
    global cid
    i = str(cid)
    cid += 1
    edge_style = "none" if straight else "orthogonalEdgeStyle"
    style = (
        f"endArrow=oval;startArrow=none;html=1;strokeColor={stroke};strokeWidth=2;"
        f"exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;"
        f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;"
        f"edgeStyle={edge_style};rounded=0;endFill=0;endSize=8;"
    )
    cells.append(
        f'<mxCell id="{i}" style="{style}" edge="1" parent="1" source="{source}" target="{target}">'
        f'<mxGeometry relative="1" as="geometry"/>'
        f"</mxCell>"
    )
    return i


def q_x(start_q):
    return LANE_X + start_q * Q


def q_w(flex):
    return flex * Q


vertex("", 0, 0, PAGE_W, PAGE_H, f"fillColor={BG};strokeColor=none;")

vertex(
    "G1 SOUNDWAVE RELEASES AND MOLD EVOLUTION",
    80,
    40,
    2200,
    50,
    style_text(TITLE_C, 28, 1),
)

vertex(
    "",
    CONTAINER_X,
    CONTAINER_Y,
    CONTAINER_W,
    CONTAINER_H,
    f"rounded=1;fillColor={PURPLE_DARK};strokeColor=#6b21a8;strokeWidth=2;arcSize=6;",
)

for i, year in enumerate(YEARS):
    x = q_x(i * 4)
    w = q_w(4)
    vertex(str(year), x, HEADER_Y, w, 28, style_text(YEAR_C, 18, 1))
    for j, ql in enumerate(QUARTER_LABELS):
        vertex(ql, x + j * Q, HEADER_Y + 28, Q, 18, style_text(PURPLE, 10, 1))

tracks = [
    ("Takara&#xa;Microchange", BLUE, TRACK_YS[0]),
    ("Hasbro/Takara&#xa;Transformers", PURPLE, TRACK_YS[1]),
    ("Takara Japanese&#xa;Exclusives", RED, TRACK_YS[2]),
]
for label, color, ty in tracks:
    vertex(label, CONTAINER_X + 16, ty, LABEL_W - 10, 50, style_text(color, 14, 1, "left"), escape=False)

events = [
    (
        0,
        1.0,
        BLUE_FILL,
        BLUE,
        0,
        "<b>Peach Prototype</b><br><font style=\"font-size:11px\">Hardcopy cast in early 1983. Lacking interior deck details.</font>",
        "top",
        240,
        False,
    ),
    (
        2.7,
        1.3,
        BLUE_FILL,
        BLUE,
        0,
        "<b>MC-10 Cassetteman</b><br><font style=\"font-size:11px\">Debuts Sept 1983. First release lacks cassette deck details.</font>",
        "top",
        200,
        False,
    ),
    (
        6,
        1.0,
        PURPLE_FILL,
        PURPLE,
        1,
        "<b>TF 1.A</b><br><font style=\"font-size:11px\">• Internal Takara stamp<br>• Solid fists</font>",
        "bottom",
        150,
        True,
    ),
    (
        9,
        6.0,
        PURPLE_FILL,
        PURPLE,
        1,
        "<b>Post-Rub Standard</b><br><font style=\"font-size:11px\">Thermal rubsign added. Expanded global distribution.</font>",
        "bottom",
        250,
        False,
    ),
    (
        11,
        1.0,
        RED_FILL,
        RED,
        2,
        "<b>VSY Giftset</b><br><font style=\"font-size:11px\">Oct 1985 release in Japan. Soundwave packed with Grimlock & Frenzy.</font>",
        "bottom",
        250,
        False,
    ),
    (
        18,
        2.0,
        RED_FILL,
        RED,
        2,
        "<b>Soundblaster (Headmasters)</b><br><font style=\"font-size:11px\">Retooled chest to hold two cassettes. Black color scheme.</font>",
        "bottom",
        250,
        False,
    ),
]

top_slots = []
bottom_slots = []

for start_q, flex, fill, stroke, ti, html_val, side, cw, diagonal in events:
    bar_x = q_x(start_q)
    bar_w = max(q_w(flex), 14)
    bar_y = TRACK_YS[ti] + 20
    vertex("", bar_x, bar_y, bar_w, 12, style_bar(fill, stroke))
    dot_id = vertex(
        "",
        bar_x + 4,
        bar_y - 2,
        16,
        16,
        f"ellipse;fillColor={BG};strokeColor={stroke};strokeWidth=2;",
    )

    ch = 78 if "•" in html_val else 70
    if side == "top":
        cy = CONTAINER_Y - 30 - ch
        cx = bar_x + bar_w / 2 - cw / 2
        for other in top_slots:
            if abs(cx - other[0]) < (cw + other[2]) / 2 + 20:
                cy = other[1] - ch - 16
        top_slots.append((cx, cy, cw))
        box_id = vertex(html_val, cx, cy, cw, ch, style_box(fill, stroke))
        edge(box_id, dot_id, stroke, exit_x=0.5, exit_y=1, entry_x=0.5, entry_y=0, straight=False)
    else:
        cy = CONTAINER_Y + CONTAINER_H + 30
        cx = bar_x - cw - 20 if diagonal else bar_x + bar_w / 2 - cw / 2
        for other in bottom_slots:
            if abs(cx - other[0]) < (cw + other[2]) / 2 + 20 and abs(cy - other[1]) < ch + 10:
                cy = other[1] + other[3] + 16
        bottom_slots.append((cx, cy, cw, ch))
        box_id = vertex(html_val, max(20, cx), cy, cw, ch, style_box(fill, stroke))
        if diagonal:
            edge(box_id, dot_id, stroke, exit_x=0.5, exit_y=0, entry_x=0.5, entry_y=0.5, straight=True)
        else:
            edge(box_id, dot_id, stroke, exit_x=0.5, exit_y=0, entry_x=0.5, entry_y=0, straight=False)

vertex(
    "Blue = Takara Microchange      Purple = Hasbro/Takara      Red = Japan Exclusives",
    80,
    PAGE_H - 40,
    2200,
    24,
    style_text(DESC, 12, 0, "left"),
)

out = f"""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-09-22T00:00:00.000Z" agent="Cursor" version="22.1.0" type="device">
  <diagram id="soundwave-timeline" name="G1 Soundwave Timeline">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0" background="{BG}">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {''.join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

path = Path(__file__).resolve().parent / "g1_soundwave_timeline.drawio"
path.write_text(out, encoding="utf-8")
print(f"Wrote {path} ({path.stat().st_size} bytes, {cid - 2} cells)")
