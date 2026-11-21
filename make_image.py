#!/usr/bin/env python3
"""Draw entry.png: one picture summing up the world news of Saturday 21 November 2026.

All artwork is drawn from scratch with PIL primitives and text: no photos,
no copyrighted assets, no outlet logos. Run: python3 make_image.py
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BACKDROP = (16, 24, 44)
CARD = (25, 38, 66)
CARD_EDGE = (52, 84, 138)
AMBER = (255, 190, 90)
WHITE = (244, 247, 252)
MIST = (188, 202, 226)
SKY = (112, 204, 255)
LEAF = (128, 232, 168)
CORAL = (255, 116, 116)
ROSE = (255, 150, 205)
SAND = (255, 214, 120)

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def face(size, bold=True):
    return ImageFont.truetype(SANS_BOLD if bold else SANS, size)


def wrapped(draw, text, fnt, max_width):
    """Greedy word wrap against a pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def card(draw, box, heading, heading_color, body_lines, heading_size=36, body_size=27):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=16, fill=CARD, outline=CARD_EDGE, width=3)
    draw.text((x0 + 22, y0 + 16), heading, font=face(heading_size), fill=heading_color)
    y = y0 + 18 + heading_size + 12
    for line in body_lines:
        for piece in wrapped(draw, line, face(body_size, bold=False), x1 - x0 - 44):
            draw.text((x0 + 22, y), piece, font=face(body_size, bold=False), fill=WHITE)
            y += body_size + 7
    return y


def poland_flag(draw, x, y, w=92, h=58):
    draw.rectangle([x, y, x + w, y + h // 2], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.rectangle([x, y + h // 2, x + w, y + h], fill=(210, 35, 55), outline=(0, 0, 0))


def nato_star(draw, cx, cy, r=30):
    """Four-point compass star in a circle, evoking the NATO emblem."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=SKY, width=4)
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i - math.pi / 2
        rad = r - 6 if i % 2 == 0 else (r - 6) * 0.32
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=SKY)


def burst(draw, cx, cy, r=26, color=CORAL):
    for i in range(8):
        ang = math.pi / 4 * i
        draw.line([cx + 8 * math.cos(ang), cy + 8 * math.sin(ang),
                   cx + r * math.cos(ang), cy + r * math.sin(ang)], fill=color, width=6)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=AMBER)


def missile_trail(draw, start, end, sag=60):
    """Dashed arc from start to end, like a missile trajectory."""
    steps = 26
    for i in range(steps):
        t0, t1 = i / steps, (i + 0.55) / steps
        def point(t):
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t - sag * math.sin(math.pi * t)
            return x, y
        draw.line([point(t0), point(t1)], fill=CORAL, width=5)


def falling_chart(draw, box):
    x0, y0, x1, y1 = box
    # axes
    draw.line([x0, y0, x0, y1], fill=MIST, width=4)
    draw.line([x0, y1, x1, y1], fill=MIST, width=4)
    pts = [(x0 + 14, y0 + 26), (x0 + 110, y0 + 60), (x0 + 190, y0 + 48),
           (x0 + 280, y0 + 130), (x0 + 360, y0 + 118), (x0 + 452, y0 + 198)]
    draw.line(pts, fill=CORAL, width=8)
    for px, py in pts:
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=WHITE)
    # arrow head at the end
    ex, ey = pts[-1]
    draw.polygon([(ex + 22, ey + 16), (ex - 4, ey + 20), (ex + 2, ey - 6)], fill=CORAL)


def flame(draw, cx, cy, scale=1.0):
    s = scale
    outer = [(cx, cy - 46 * s), (cx + 26 * s, cy - 4 * s), (cx + 30 * s, cy + 26 * s),
             (cx + 14 * s, cy + 44 * s), (cx - 14 * s, cy + 44 * s), (cx - 30 * s, cy + 26 * s),
             (cx - 26 * s, cy - 4 * s)]
    draw.polygon(outer, fill=(255, 130, 60))
    inner = [(cx, cy - 8 * s), (cx + 15 * s, cy + 20 * s), (cx + 7 * s, cy + 40 * s),
             (cx - 7 * s, cy + 40 * s), (cx - 15 * s, cy + 20 * s)]
    draw.polygon(inner, fill=AMBER)


def capsule(draw, cx, cy, w=96, h=44):
    draw.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
                           radius=h // 2, outline=WHITE, width=5)
    draw.rectangle([cx - w // 2 + 4, cy - h // 2 + 4, cx, cy + h // 2 - 4], fill=ROSE)


def globe_leaf(draw, cx, cy, r=40):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LEAF, width=5)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], start=90, end=270, fill=LEAF, width=3)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], start=270, end=90, fill=LEAF, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=LEAF, width=3)
    # small leaf sprout on top
    draw.polygon([(cx, cy - r - 4), (cx + 22, cy - r - 26), (cx + 2, cy - r - 30)], fill=LEAF)


def handshake_rings(draw, cx, cy):
    draw.ellipse([cx - 44, cy - 30, cx + 6, cy + 30], outline=SKY, width=6)
    draw.ellipse([cx - 6, cy - 30, cx + 44, cy + 30], outline=WHITE, width=6)


def shield(draw, cx, cy, w=76, h=92):
    pts = [(cx - w // 2, cy - h // 2), (cx + w // 2, cy - h // 2), (cx + w // 2, cy + 6),
           (cx, cy + h // 2), (cx - w // 2, cy + 6)]
    draw.polygon(pts, outline=SAND, width=6)
    draw.line([cx - 16, cy - 2, cx - 3, cy + 14], fill=SAND, width=7)
    draw.line([cx - 3, cy + 14, cx + 20, cy - 16], fill=SAND, width=7)


def build():
    img = Image.new("RGB", (SIZE, SIZE), BACKDROP)
    d = ImageDraw.Draw(img)

    # Header: name the day, big.
    d.text((24, 20), "SATURDAY 21 NOVEMBER 2026", font=face(58), fill=WHITE)
    d.text((26, 94), "The day in one picture — world news", font=face(30, bold=False), fill=AMBER)
    d.rectangle([24, 138, 1000, 144], fill=AMBER)

    # Main story: Russian missiles land in Poland.
    box = (24, 160, 560, 604)
    d.rounded_rectangle(box, radius=16, fill=CARD, outline=CARD_EDGE, width=3)
    d.text((46, 176), "MISSILES HIT POLAND", font=face(38), fill=AMBER)
    poland_flag(d, 60, 248)
    d.text((60, 316), "POLAND", font=face(22), fill=MIST)
    nato_star(d, 486, 278, r=34)
    # border line and incoming trails from the east (right side)
    d.line([330, 236, 330, 452], fill=MIST, width=4)
    d.text((288, 216), "border", font=face(20, bold=False), fill=MIST)
    missile_trail(d, (520, 250), (356, 330), sag=70)
    missile_trail(d, (520, 330), (352, 410), sag=56)
    burst(d, 350, 332, r=30)
    burst(d, 348, 412, r=24)
    # ground
    d.rectangle([46, 452, 538, 460], fill=(90, 70, 46))
    lines = [
        "2 missiles + drone crash in Poland",
        "NATO: \"grave violation\"",
        "NATO chief flies to Warsaw",
        "Tusk: \"deliberate provocation\"",
    ]
    y = 472
    for ln in lines:
        for piece in wrapped(d, ln, face(26, bold=False), 492):
            d.text((46, y), piece, font=face(26, bold=False), fill=WHITE)
            y += 34

    # Bottom-left: Wall Street correction.
    box = (24, 620, 560, 1000)
    d.rounded_rectangle(box, radius=16, fill=CARD, outline=CARD_EDGE, width=3)
    d.text((46, 636), "WALL STREET SLUMPS", font=face(38), fill=AMBER)
    falling_chart(d, (64, 700, 524, 920))
    d.text((46, 930), "S&P 500 enters correction", font=face(28, bold=False), fill=WHITE)
    d.text((46, 964), "AI stocks plunge ~3.7% · Nasdaq −5%+", font=face(25, bold=False), fill=MIST)

    # Right column: five smaller stories.
    rx0, rx1 = 576, 1000
    stories = [
        ("UK–EU DEALS", SKY, ["Britain & EU sign food, carbon and youth-mobility deals"], "rings"),
        ("COP31 CLIMATE TALKS", LEAF, ["Crunch time in Antalya — no deal yet"], "globe"),
        ("PALISADES FIRE VERDICT", CORAL, ["Man convicted of starting LA's Palisades Fire"], "flame"),
        ("CANCER PILL HOPE", ROSE, ["Pancreatic cancer pill + chemo: tumors vanish in trial"], "pill"),
        ("RIYADH MISSILES", SAND, ["Houthi missiles intercepted over Riyadh"], "shield"),
    ]
    y = 160
    for title, color, lines, icon in stories:
        box = (rx0, y, rx1, y + 156)
        d.rounded_rectangle(box, radius=16, fill=CARD, outline=CARD_EDGE, width=3)
        d.rectangle([rx0, y, rx0 + 10, y + 156], fill=color)
        d.text((rx0 + 26, y + 12), title, font=face(29), fill=color)
        ty = y + 52
        for ln in lines:
            for piece in wrapped(d, ln, face(24, bold=False), 262):
                d.text((rx0 + 26, ty), piece, font=face(24, bold=False), fill=WHITE)
                ty += 30
        cx, cy = rx1 - 58, y + 98
        if icon == "rings":
            handshake_rings(d, cx, cy)
        elif icon == "globe":
            globe_leaf(d, cx, cy, r=38)
        elif icon == "flame":
            flame(d, cx, cy)
        elif icon == "pill":
            capsule(d, cx, cy)
        else:
            shield(d, cx, cy)
        y += 166

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
