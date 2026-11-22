"""Render 'THE WORLD TODAY' — 22 November 2026 newspaper front page.

Deterministic Pillow drawing: no clock, no randomness, no network.
Fixed geometry only. Writes assets/entry.png (1024x1024).
"""
import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 228)
INK = (25, 25, 25)
RED = (164, 18, 32)
NAVY = (30, 44, 60)
GOLD = (181, 127, 36)
GREY = (107, 101, 90)
DIVIDER = (192, 183, 163)
PALE = (223, 229, 234)
ORANGE = (232, 122, 32)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_width):
    """Wrap text to fit max_width; return list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, spacing=4):
    lines = wrap(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def star_points(cx, cy, outer, inner, points=8, rot=-90):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_shield(draw, x, y):
    # Navy shield with a white check, inside a 46x34 box.
    pts = [(x + 23, y + 2), (x + 44, y + 6), (x + 44, y + 18),
           (x + 23, y + 32), (x + 2, y + 18), (x + 2, y + 6)]
    draw.polygon(pts, fill=NAVY)
    draw.line([(x + 12, y + 17), (x + 20, y + 25), (x + 34, y + 9)],
              fill=WHITE, width=3)


def draw_padlock(draw, x, y):
    # Red padlock, inside a 46x34 box.
    draw.arc([x + 14, y + 2, x + 32, y + 20], 180, 360, fill=RED, width=4)
    draw.rounded_rectangle([x + 8, y + 14, x + 38, y + 32], radius=3, fill=RED)
    draw.ellipse([x + 20, y + 19, x + 26, y + 25], fill=WHITE)


def draw_chip(draw, x, y):
    # Navy chip with a gold centre, inside a 46x34 box.
    draw.rounded_rectangle([x + 8, y + 4, x + 38, y + 30], radius=4, fill=NAVY)
    for px in (x + 12, x + 20, x + 28):
        draw.line([(px, y + 1), (px, y + 4)], fill=NAVY, width=2)
        draw.line([(px, y + 30), (px, y + 33)], fill=NAVY, width=2)
    draw.rectangle([x + 17, y + 12, x + 29, y + 22], fill=GOLD)


def draw_tennis(draw, x, y):
    # Gold tennis ball, inside a 46x34 box.
    draw.ellipse([x + 8, y + 2, x + 38, y + 32], fill=GOLD)
    draw.arc([x + 8, y + 2, x + 38, y + 32], 300, 60, fill=WHITE, width=2)
    draw.arc([x + 8, y + 2, x + 38, y + 32], 120, 240, fill=WHITE, width=2)


def draw_oil_drop(draw, x, y):
    # Navy oil drop with a red diagonal slash, inside a 46x34 box.
    pts = [(x + 23, y + 2), (x + 36, y + 18), (x + 36, y + 24),
           (x + 23, y + 32), (x + 10, y + 24), (x + 10, y + 18)]
    draw.polygon(pts, fill=NAVY)
    draw.line([(x + 8, y + 28), (x + 38, y + 4)], fill=RED, width=4)


def draw_bank(draw, x, y):
    # Navy bank building: triangle roof, 3 columns, base.
    draw.polygon([(x + 4, y + 12), (x + 42, y + 12), (x + 23, y + 2)], fill=NAVY)
    for cx in (x + 10, x + 21, x + 32):
        draw.rectangle([cx, y + 15, cx + 4, y + 27], fill=NAVY)
    draw.rectangle([x + 4, y + 29, x + 42, y + 32], fill=NAVY)


ICONS = [draw_shield, draw_padlock, draw_chip,
         draw_tennis, draw_oil_drop, draw_bank]

STORIES = [
    ("RUSSIA HITS KRYVYI RIH",
     "2 killed, 58 injured; NATO vows to defend Poland."),
    ("FBI PROBES DATABASE BREACH",
     "Bureau probes a suspected breach of its national crime database."),
    ("NVIDIA: NO WAY BACK FOR HUANG",
     "Board rules out a return for Huang. Revenue $115.8bn, up 103%."),
    ("ALCARAZ v ZVEREV FOR ATP CROWN",
     "Alcaraz meets world No. 1 Zverev in the ATP Finals title decider."),
    ("NORWAY COURT VOIDS OIL LICENCES",
     "Supreme court rules climate-disputed oil licences invalid."),
    ("LAGARDE RESIGNS, ECB HUNT BEGINS",
     "EU launches search for a new central bank chief."),
]
def draw_hero_illustration(draw):
    # Navy box (700,168)-(994,428) with stars, missile trails, radar dish.
    draw.rectangle([700, 168, 994, 428], fill=NAVY)
    # Pale stars in the upper half.
    for sx, sy, r in [(716, 186, 2), (752, 204, 2), (800, 182, 2),
                      (852, 200, 2), (896, 184, 2), (948, 206, 2),
                      (972, 182, 2), (828, 224, 2), (920, 228, 2),
                      (764, 240, 2), (700 + 180, 190, 2)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=PALE)
    # Two thin pale missile trails running down-right, each with a dart head.
    for (x0, y0, x1, y1) in [(828, 196, 912, 268), (806, 238, 888, 306)]:
        draw.line([(x0, y0), (x1, y1)], fill=PALE, width=2)
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy)
        ux, uy = dx / ln, dy / ln
        px, py = -uy, ux
        tip = (x1 + 10 * ux, y1 + 10 * uy)
        draw.polygon([tip, (x1 + 3 * px, y1 + 3 * py),
                      (x1 - 3 * px, y1 - 3 * py)], fill=WHITE)
    # Radar dish: pale dome arc (upper half of an 80x80 ellipse),
    # short vertical mast below it, small horizontal base line.
    # Dish sits left-centre; its base ends at y=368, 8px above the caption.
    draw.arc([730, 248, 810, 328], 180, 360, fill=PALE, width=4)
    draw.line([(770, 288), (770, 360)], fill=PALE, width=4)
    draw.line([(748, 360), (792, 360)], fill=PALE, width=4)
    # 8-pointed orange starburst: two layered stars at about (926, 296).
    draw.polygon(star_points(926, 296, 46, 20), fill=ORANGE)
    draw.polygon(star_points(926, 296, 24, 10), fill=GOLD)
    draw.text((716, 376), "STRAIT OF HORMUZ",
              font=font(SANS_B, 17), fill=WHITE)
    draw.text((716, 400), "US Patriot radar sites targeted",
              font=font(SANS, 14), fill=PALE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.text((30, 12), "THE WORLD TODAY", font=font(SERIF_B, 62), fill=INK)
    draw.text((32, 90), "SUNDAY, 22 NOVEMBER 2026",
              font=font(SANS_B, 19), fill=INK)
    draw.text((32, 118), "Six stories that shaped the day, in one page.",
              font=font(SANS, 16), fill=GREY)
    draw.rectangle([30, 146, 994, 148], fill=RED)
    draw.rectangle([30, 152, 994, 152], fill=INK)

    # Hero: left text column (width 640), illustration box right.
    draw.text((30, 168), "MIDDLE EAST ON EDGE",
              font=font(SANS_B, 20), fill=RED)
    draw_wrapped(draw, 30, 194, "IRAN STRIKES US DEFENCES AS GULF BRACES",
                 font(SERIF_B, 40), 640, INK, spacing=2)
    draw_wrapped(draw, 30, 322,
                 "Revolutionary Guards fire missiles and drones at two "
                 "US Patriot radar sites; Bahrain says an industrial "
                 "facility was hit.",
                 font(SANS, 19), 640, INK, spacing=3)
    draw_wrapped(draw, 30, 384,
                 "Tehran calls the US blockade a hostile act; the Strait "
                 "of Hormuz could reopen in two days.",
                 font(SANS, 18), 640, INK, spacing=3)
    draw_hero_illustration(draw)
    draw.rectangle([30, 448, 994, 449], fill=RED)

    # Six-story grid: 3 columns x 2 rows.
    col_x = [30, 358, 686]
    row_y = [466, 624]
    for i, (headline, deck) in enumerate(STORIES):
        cx = col_x[i % 3]
        ry = row_y[i // 3]
        ICONS[i](draw, cx, ry + 2)
        draw_wrapped(draw, cx, ry + 44, headline,
                     font(SERIF_B, 21), 304, INK, spacing=2)
        draw_wrapped(draw, cx, ry + 100, deck,
                     font(SANS, 17), 304, INK, spacing=3)
    draw.line([(346, 466), (346, 774)], fill=DIVIDER, width=1)
    draw.line([(674, 466), (674, 774)], fill=DIVIDER, width=1)
    draw.line([(30, 616), (994, 616)], fill=DIVIDER, width=1)

    # Also today.
    draw.rectangle([30, 790, 994, 791], fill=RED)
    draw.text((30, 804), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    draw_wrapped(draw, 30, 830,
                 "Mexico captures cartel boss El Chapo Isidro in Sinaloa "
                 "\u2022 Magnitude 6.7 quake in Peru: 152 homes "
                 "uninhabitable \u2022 Myanmar hit by a 4.1 quake",
                 font(SANS, 17), 470, INK, spacing=3)
    draw_wrapped(draw, 524, 830,
                 "Democrats reclaim Congress in US midterm vote \u2022 EU "
                 "and Indonesia sign trade deals \u2022 Al-Shabaab claims "
                 "ambush on Somali troops",
                 font(SANS, 17), 470, INK, spacing=3)

    # Footer.
    draw.line([(30, 964), (994, 964)], fill=DIVIDER, width=1)
    draw.text((30, 976),
              "Sources: Reuters, AP, ANI, BBC, Al Jazeera \u00b7 "
              "22 November 2026",
              font=font(SANS, 14), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "assets", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print(f"{out} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
