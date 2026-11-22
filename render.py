"""Draw the 22 November 2026 world-news front page as a PNG.

A single 1024x1024 newspaper front page built with Pillow and written to
assets/entry.png. Everything is fixed: no randomness, no clock reads, no
network, fixed fonts and fixed geometry, so repeated runs produce
byte-identical output.
"""

import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "assets" / "entry.png"

W, H = 1024, 1024
M = 30
CW = W - 2 * M

PAPER = "#f6f1e4"
INK = "#191919"
RED = "#a41220"
NAVY = "#1e2c3c"
GOLD = "#b57f24"
GREY = "#6b655a"
FAINT = "#c0b7a3"
SKY = "#dfe5ea"
SAND = "#e9e0cb"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

_cache = {}


def font(size, serif=False, bold=False):
    """Load a cached DejaVu face at the requested size."""
    key = (size, serif, bold)
    if key not in _cache:
        stem = "DejaVuSerif" if serif else "DejaVuSans"
        if bold:
            stem += "-Bold"
        try:
            _cache[key] = ImageFont.truetype(FONT_DIR + stem + ".ttf", size)
        except OSError:
            _cache[key] = ImageFont.load_default()
    return _cache[key]


def wrap(text, fnt, width):
    """Break text into lines that fit inside width pixels."""
    out = []
    for chunk in text.split("\n"):
        cur = ""
        for word in chunk.split():
            trial = (cur + " " + word).strip()
            if cur and fnt.getlength(trial) > width:
                out.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            out.append(cur)
    return out


def para(d, x, y, text, size, width, serif=False, bold=False,
         fill=INK, lead=5):
    """Draw wrapped text starting at (x, y); return y below the last line."""
    fnt = font(size, serif, bold)
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += size + lead
    return y


def rule(d, y, weight=2, colour=RED):
    d.line((M, y, W - M, y), fill=colour, width=weight)


def star(d, cx, cy, outer, inner, points=5, rot=-90, fill=GOLD):
    """A regular star polygon centred at (cx, cy)."""
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def streak(d, x0, y0, x1, y1, colour):
    """A missile trail: thin line with a small white dart head."""
    d.line((x0, y0, x1, y1), fill=colour, width=3)
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1.0
    ux, uy, px, py = dx / ln, dy / ln, -dy / ln, dx / ln
    d.polygon([(x1, y1),
               (x1 - 15 * ux + 6 * px, y1 - 15 * uy + 6 * py),
               (x1 - 15 * ux - 6 * px, y1 - 15 * uy - 6 * py)],
              fill="#f4f1e6")


def icon(d, kind, x, y):
    """Flat pictogram for one grid story, inside a 46x34 box."""
    if kind == "shield":  # NATO / Kryvyi Rih
        d.polygon([(x + 23, y + 34), (x + 2, y + 24), (x + 2, y + 8),
                   (x + 23, y), (x + 44, y + 8), (x + 44, y + 24)],
                  fill=NAVY)
        d.line((x + 14, y + 16, x + 20, y + 23, x + 33, y + 9),
               fill="white", width=3)
    elif kind == "lock":  # FBI breach
        d.rectangle((x + 8, y + 14, x + 38, y + 34), fill=RED)
        d.arc((x + 13, y + 2, x + 33, y + 20), 180, 360, fill=RED, width=4)
        d.rectangle((x + 21, y + 20, x + 25, y + 28), fill="white")
    elif kind == "chip":  # Nvidia
        d.rectangle((x + 10, y + 6, x + 36, y + 30), fill=NAVY)
        for cx in (16, 23, 30):
            d.line((x + cx, y, x + cx, y + 6), fill=NAVY, width=2)
            d.line((x + cx, y + 30, x + cx, y + 36), fill=NAVY, width=2)
        d.rectangle((x + 18, y + 14, x + 28, y + 22), fill=GOLD)
    elif kind == "ball":  # ATP final
        d.ellipse((x + 6, y + 2, x + 40, y + 34), fill=GOLD)
        d.arc((x + 12, y + 2, x + 30, y + 34), 270, 90, fill=INK, width=2)
        d.arc((x + 16, y + 2, x + 34, y + 34), 270, 90, fill=INK, width=2)
    elif kind == "drop":  # Norway oil ruling
        d.polygon([(x + 23, y), (x + 40, y + 22), (x + 23, y + 34),
                   (x + 6, y + 22)], fill=NAVY)
        d.line((x + 8, y + 10, x + 38, y + 30), fill=RED, width=4)
    elif kind == "bank":  # ECB chief
        d.polygon([(x, y + 12), (x + 23, y), (x + 46, y + 12)], fill=NAVY)
        for i in range(3):
            d.rectangle((x + 5 + i * 15, y + 15, x + 10 + i * 15, y + 29),
                        fill=NAVY)
        d.rectangle((x + 2, y + 31, x + 44, y + 35), fill=NAVY)


def build():
    """Draw the whole front page and return the Pillow image."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    para(d, M, 12, "THE WORLD TODAY", 62, CW, serif=True, bold=True, lead=2)
    para(d, M + 2, 90, "SUNDAY, 22 NOVEMBER 2026", 19, CW, bold=True, lead=2)
    para(d, M + 2, 118, "Six stories that shaped the day, in one page.",
         16, CW, fill=GREY, lead=2)
    rule(d, 146, weight=3)
    d.line((M, 152, W - M, 152), fill=INK, width=1)

    # ---- Hero: Iran strikes --------------------------------------------
    hw = 640
    para(d, M, 168, "MIDDLE EAST ON EDGE", 20, hw, bold=True, fill=RED,
         lead=2)
    y = para(d, M, 194, "IRAN STRIKES US DEFENCES AS GULF BRACES",
             40, hw, serif=True, bold=True, lead=6)
    y = para(d, M, y + 8,
             "Revolutionary Guards fire missiles and drones at two US "
             "Patriot radar sites; Bahrain says an industrial facility "
             "was hit.",
             19, hw, lead=6)
    y = para(d, M, y + 4,
             "Tehran calls the US blockade a hostile act; the Strait of "
             "Hormuz could reopen in two days.",
             18, hw, lead=6)

    # Hero picture: night sky over the Gulf, radar dish, incoming fire.
    x0, y0, x1, y1 = 700, 168, 994, 428
    d.rectangle((x0, y0, x1, y1), fill=NAVY)
    for sx, sy in ((724, 190), (770, 214), (836, 186), (912, 208),
                   (958, 190), (742, 240), (880, 238)):
        d.ellipse((sx, sy, sx + 3, sy + 3), fill=SKY)
    # Radar dish and mast, clear of the caption below.
    d.arc((x0 + 70, y0 + 120, x0 + 150, y0 + 200), 180, 360, fill=SKY,
          width=4)
    d.line((x0 + 110, y0 + 160, x0 + 110, y0 + 200), fill=SKY, width=4)
    d.line((x0 + 90, y0 + 200, x0 + 130, y0 + 200), fill=SKY, width=4)
    streak(d, x0 + 30, y0 + 40, x0 + 120, y0 + 96, SKY)
    streak(d, x0 + 70, y0 + 22, x0 + 150, y0 + 72, "#aeb7bc")
    star(d, x0 + 226, y0 + 128, 46, 20, points=8, fill="#e7a34c")
    star(d, x0 + 226, y0 + 128, 24, 10, points=8, fill="#f0b45c")
    d.text((x0 + 16, y1 - 52), "STRAIT OF HORMUZ",
           font=font(17, bold=True), fill="white")
    d.text((x0 + 16, y1 - 28), "US Patriot radar sites targeted",
           font=font(14), fill="#c9d2da")

    rule(d, 448, weight=2)

    # ---- Six-story grid -------------------------------------------------
    stories = [
        ("shield", "RUSSIA HITS KRYVYI RIH",
         "2 killed, 58 injured; NATO vows to defend Poland."),
        ("lock", "FBI PROBES DATABASE BREACH",
         "Bureau probes a suspected breach of its national crime "
         "database."),
        ("chip", "NVIDIA: NO WAY BACK FOR HUANG",
         "Board rules out a return for Huang. Revenue $115.8bn, "
         "up 103%."),
        ("ball", "ALCARAZ v ZVEREV FOR ATP CROWN",
         "Alcaraz meets world No. 1 Zverev in the ATP Finals title "
         "decider."),
        ("drop", "NORWAY COURT VOIDS OIL LICENCES",
         "Supreme court rules climate-disputed oil licences invalid."),
        ("bank", "LAGARDE RESIGNS, ECB HUNT BEGINS",
         "EU launches search for a new central bank chief."),
    ]
    col_w, row_h = 304, 158
    col_x = [M, M + 328, M + 656]
    row_y = [466, 624]
    for i, (kind, head, deck) in enumerate(stories):
        cx, cy = col_x[i % 3], row_y[i // 3]
        icon(d, kind, cx, cy + 2)
        para(d, cx, cy + 44, head, 21, col_w, serif=True, bold=True,
             lead=4)
        para(d, cx, cy + 100, deck, 17, col_w, lead=5)
    for vx in (M + 316, M + 644):
        d.line((vx, 466, vx, 774), fill=FAINT, width=1)
    d.line((M, 616, W - M, 616), fill=FAINT, width=1)

    # ---- Also today ------------------------------------------------------
    rule(d, 790, weight=2)
    para(d, M, 804, "ALSO TODAY", 17, CW, bold=True, fill=RED, lead=2)
    also_left = ("Mexico captures cartel boss El Chapo Isidro in Sinaloa  "
                 "\u2022  Magnitude 6.7 quake in Peru: 152 homes "
                 "uninhabitable  \u2022  Myanmar hit by a 4.1 quake")
    also_right = ("Democrats reclaim Congress in US midterm vote  \u2022  "
                  "EU and Indonesia sign trade deals  \u2022  Al-Shabaab "
                  "claims ambush on Somali troops")
    para(d, M, 830, also_left, 17, 470, lead=6)
    para(d, M + 494, 830, also_right, 17, 470, lead=6)

    # ---- Footer ----------------------------------------------------------
    d.line((M, 964, W - M, 964), fill=FAINT, width=1)
    para(d, M, 976, "Sources: Reuters, AP, ANI, BBC, Al Jazeera  "
         "\u00b7  22 November 2026", 14, CW, fill=GREY, lead=2)

    return img


def main():
    page = build()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    page.save(OUT_PATH, optimize=True)
    data = OUT_PATH.read_bytes()
    print(len(data), hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
