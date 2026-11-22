#!/usr/bin/env python3
"""Render the Sunday Globe: one image summing up Sunday 22 November 2026.

Build-time renderer. Draws everything with Pillow into entry.png
(1024x1024, deterministic). main.py only copies the finished PNG.
All facts were verified against live reporting on 23 Nov 2026.
COP31 ended with NO deal: the EU, UK and Panama rejected a final
text that mentioned no fossil fuels. The 35% electricity goal and
the $120bn adaptation target lived only in the rejected draft.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (18, 18, 18)
PAPER = (250, 246, 238)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
BLUE = (24, 58, 110)
GREY = (96, 96, 96)
LIGHT = (232, 226, 214)
RULE = (60, 60, 60)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped paragraph; returns y after last line."""
    if leading is None:
        leading = fnt.size + 3
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def center(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag_chip(draw, x, y, label, fill):
    """Small certainty chip; returns width used."""
    f = font(SANS_B, 8)
    w = draw.textlength(label, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories
# tag: C = confirmed by officials / several outlets; R = reported, attributed.
LEADS = [
    dict(num=1, region="CLIMATE", tag="C",
         head="COP31 COLLAPSES: NO DEAL IN ANTALYA",
         dek="The EU, Britain and Panama reject a final text that never "
             "mentions fossil fuels. The longest climate summit on record "
             "ends with no pact at all.",
         scene="cop"),
    dict(num=2, region="UKRAINE", tag="C",
         head="186 DRONES OVER KYIV IN ONE NIGHT",
         dek="Ukraine downs 161 of them, but a strike flattens part of a "
             "block of flats in Dymer. Fourteen people are unaccounted for.",
         scene="drones"),
    dict(num=3, region="SPORT", tag="C",
         head="INDIA 720 FOR 9: A RECORD IN NEW ZEALAND",
         dek="Rahul 136, Pant 128 as India declare with a 352-run lead on "
             "day four of the first Test in Wellington.",
         scene="cricket"),
]

SMALL = [
    dict(num=4, region="HONG KONG", tag="C",
         head="Hong Kong picks its kingmakers",
         dek="723 seats filled on the Election Committee; turnout 98.79%, a record.",
         scene="ballot"),
    dict(num=5, region="MOTOR RACING", tag="C",
         head="Verstappen wins the Vegas yo-yo",
         dek="35 lead changes, 352 overtakes. Norris 2nd, Piastri 3rd; his 75th win.",
         scene="f1"),
    dict(num=6, region="BASKETBALL", tag="C",
         head="Wemby 50 — and a piece of history",
         dek="50 points, 19 rebounds, 5 blocks, 4 steals. Spurs beat Pelicans 114-91.",
         scene="hoops"),
    dict(num=7, region="BALTIC SEA", tag="C",
         head="The ship that would not sink",
         dek="Drone-hit Sparta II is towed out of Finnish waters; 16 crew safe, one hurt.",
         scene="ship"),
    dict(num=8, region="INDONESIA", tag="C",
         head="Fire at the candy factory",
         dek="24 body bags recovered in Cikande; dozens still missing after Saturday's blaze.",
         scene="fire"),
    dict(num=9, region="PERU", tag="C",
         head="The earth shakes again in Junin",
         dek="M5.4 and M5.0 aftershocks on Sunday follow Friday's M6.7; one dead, 853 displaced.",
         scene="quake"),
    dict(num=10, region="GULF", tag="R",
         head="Missiles over the Gulf",
         dek="Iran hits targets in Bahrain; tankers struck near Hormuz as the region braces.",
         scene="tanker"),
    dict(num=11, region="GAZA", tag="R",
         head="Gaza plan on the brink",
         dek="Board of Peace warns it may 'throw the keys back to the UN' as talks stall.",
         scene="dove"),
    dict(num=12, region="TRADE", tag="R",
         head="EU and Indonesia sign the big deal",
         dek="After almost 10 years of talks, tariffs scrapped on up to 98.5% of goods.",
         scene="trade"),
    dict(num=13, region="JUSTICE", tag="R",
         head="Myanmar guilty of genocide",
         dek="World Court rules on the Rohingya — the first state ever found responsible.",
         scene="scales"),
    dict(num=14, region="FRANCE", tag="R",
         head="France strikes, week six",
         dek="Nationwide wage strikes enter a sixth week; the government intervenes.",
         scene="march"),
    dict(num=15, region="BANGLADESH", tag="R",
         head="Streets boil in Dhaka",
         dek="Violent pro-Hasina protests shake Bangladesh.",
         scene="crowd"),
]

ALSO = [
    "Kryvyi Rih: a Russian missile kills a boy of 7 and a woman of 20; 60 hurt.",
    "Houthis say they hit a Rabigh oil refinery in Saudi Arabia.",
    "Saudi-led coalition intercepts three Houthi missiles bound for Riyadh.",
    "Blast wrecks an ammunition depot at a military base in Benghazi.",
    "A Russian ship is hit by a drone at a Libya dock, officials say.",
    "Dutch PM pledges NATO security for Poland after drone incursions.",
    "Lithuania denies any part in a drone attack on Kaliningrad.",
    "FBI crime database hit in a new cyberattack, reports say.",
    "South Korea: AI cheating scandal forces the education minister out.",
    "Nepal PM Balen Shah presses border issues on a first visit to India.",
    "Drones hit homes and UN offices in Sudan's capital.",
    "A landmine kills four children in north-west Syria.",
    "Croatians rally over a death at a psychiatric hospital.",
    "Lahore tops the world's pollution ranking; AQI over 500.",
    "US ports face a surge of cyberattack attempts.",
    "Delta flights delayed across the US after Atlanta hub trouble.",
    "Spain heads for a 29 November election amid political uncertainty.",
    "Britain opens its gates to 100,000 young Europeans a year.",
    "Trump works on a wider Ukraine-Russia ceasefire, the US says.",
    "Sudan's Burhan plays down RSF gains in Blue Nile, vows to fight on.",
    "A British swimmer crosses the Strait of Hormuz to highlight the war.",
]

STATS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "drones downed or jammed"),
    ("35%", "draft clean-power goal — never adopted"),
    ("$120bn", "adaptation target dropped from the draft"),
    ("720/9", "India declare in Wellington"),
    ("50", "Wembanyama points in 32 minutes"),
]

REGIONS = [
    ("CLIMATE", (139, 0, 0)), ("UKRAINE", (24, 58, 110)),
    ("ASIA", (176, 112, 0)), ("SPORT", (0, 110, 60)),
    ("MIDDLE EAST", (110, 40, 120)), ("AMERICAS", (0, 110, 130)),
    ("EUROPE", (90, 90, 90)),
]

TIMELINE = ("00:51 UTC  Peru M5.0   •   05:51 UTC  Peru M5.0   •   08:00 Kyiv  "
            "161 drones downed   •   16:35 Lima  Peru M5.4   •   18:00 HK  polls close"
            "   •   22:15 Antalya  COP31 ends, no deal")


# ---------------------------------------------------------------- scenes
# Each scene draws one original coded illustration into box (x, y, w, h).
# Simple flat shapes, distinct palettes, no text inside the picture.

def _sky(d, x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)


def _sun(d, x, y, r, fill=(240, 200, 60)):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def _globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180),
              outline=(20, 60, 110), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(255, 255, 255), width=2)
    d.ellipse([cx - r * 0.45, cy - r * 0.55, cx + r * 0.1, cy - r * 0.05],
              fill=(60, 160, 90))
    d.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.6],
              fill=(60, 160, 90))


def scene_cop(d, x, y, w, h):
    _sky(d, x, y, w, h, (30, 40, 70), (90, 60, 50))
    _sun(d, x + w - 26, y + 26, 15, (230, 120, 40))
    # summit hall: columns + broken roofline
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(40, 40, 48))
    for i in range(5):
        cx = x + 14 + i * (w - 28) // 4
        d.rectangle([cx - 5, y + h - 62, cx + 5, y + h - 34], fill=(210, 205, 190))
    d.polygon([(x + 8, y + h - 62), (x + w // 2, y + h - 84),
               (x + w - 8, y + h - 62)], fill=(150, 40, 40))
    d.polygon([(x + w // 2 - 14, y + h - 84), (x + w // 2 + 14, y + h - 84),
               (x + w // 2 + 30, y + h - 62), (x + w // 2 - 30, y + h - 62)],
              fill=(250, 246, 238))
    _globe(d, x + 30, y + 26, 17)


def scene_drones(d, x, y, w, h):
    _sky(d, x, y, w, h, (12, 16, 40), (60, 50, 90))
    for sx, sy in [(0.2, 0.25), (0.55, 0.18), (0.8, 0.35), (0.35, 0.45)]:
        px, py = x + int(w * sx), y + int(h * sy)
        d.ellipse([px - 8, py - 3, px + 8, py + 3], fill=(220, 220, 220))
        d.line([(px - 12, py - 6), (px + 12, py - 6)], fill=(180, 180, 180), width=2)
        d.line([(px - 12, py + 6), (px + 12, py + 6)], fill=(180, 180, 180), width=2)
    # searchlights + burning block
    d.polygon([(x + 20, y + h), (x + 60, y + 10), (x + 70, y + 10), (x + 45, y + h)],
              fill=(240, 220, 120))
    d.rectangle([x + w - 70, y + h - 42, x + w - 10, y + h], fill=(50, 50, 60))
    for wy in range(3):
        d.rectangle([x + w - 62, y + h - 38 + wy * 12, x + w - 18, y + h - 30 + wy * 12],
                    fill=(240, 150, 30) if wy != 1 else (60, 60, 70))
    d.polygon([(x + w - 60, y + h - 42), (x + w - 45, y + h - 62),
               (x + w - 30, y + h - 42)], fill=(255, 90, 20))


def scene_cricket(d, x, y, w, h):
    _sky(d, x, y, w, h, (120, 180, 110), (220, 230, 190))
    d.ellipse([x + w // 2 - 46, y + h - 46, x + w // 2 + 46, y + h - 8],
              fill=(90, 150, 70))
    # stumps + bat + ball
    bx = x + w // 2
    for sx in (-8, 0, 8):
        d.line([(bx + sx, y + h - 58), (bx + sx, y + h - 30)], fill=(240, 220, 160), width=3)
    d.polygon([(bx + 26, y + 18), (bx + 44, y + 30), (bx + 30, y + h - 40),
               (bx + 14, y + h - 34)], fill=(200, 160, 90))
    d.ellipse([bx - 52, y + 22, bx - 38, y + 36], fill=(200, 40, 40),
              outline=(255, 255, 255), width=2)
    d.arc([bx - 60, y + 8, bx - 20, y + 48], 300, 60, fill=(255, 255, 255), width=2)


def scene_ballot(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 60, 60), (250, 230, 210))
    d.rectangle([x + 12, y + h - 46, x + w - 12, y + h - 8], fill=(140, 30, 30))
    d.rectangle([x + 12, y + h - 52, x + w - 12, y + h - 46], fill=(90, 20, 20))
    d.rectangle([x + w // 2 - 16, y + h - 52, x + w // 2 + 16, y + h - 46],
                fill=(250, 246, 238))
    # ballot paper dropping in + tick
    d.polygon([(x + w // 2 - 22, y + 12), (x + w // 2 + 22, y + 12),
               (x + w // 2 + 16, y + h - 52), (x + w // 2 - 16, y + h - 52)],
              fill=(255, 255, 255), outline=(120, 120, 120))
    d.line([(x + w // 2 - 12, y + 28), (x + w // 2 - 4, y + 38),
            (x + w // 2 + 14, y + 16)], fill=(0, 130, 60), width=4)


def scene_f1(d, x, y, w, h):
    _sky(d, x, y, w, h, (20, 20, 50), (90, 30, 90))
    for i in range(6):  # neon strip lights
        d.rectangle([x + 6 + i * 12, y + 8, x + 12 + i * 12, y + 20],
                    fill=(255, 200, 40) if i % 2 == 0 else (255, 80, 200))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 40, 44))
    d.line([(x, y + h - 22), (x + w, y + h - 22)], fill=(255, 255, 255), width=2)
    # race car silhouette
    cx, cy = x + w // 2, y + h - 34
    d.polygon([(cx - 34, cy + 6), (cx - 20, cy - 4), (cx + 8, cy - 8),
               (cx + 30, cy - 2), (cx + 34, cy + 6)], fill=(200, 20, 20))
    d.polygon([(cx - 6, cy - 8), (cx + 6, cy - 16), (cx + 18, cy - 8)],
              fill=(20, 20, 20))
    for wx in (-22, 22):
        d.ellipse([cx + wx - 8, cy - 2, cx + wx + 8, cy + 12], fill=(15, 15, 15),
                  outline=(200, 200, 200), width=2)
    d.line([(cx - 40, cy + 8), (cx + 40, cy + 8)], fill=(255, 220, 80), width=2)


def scene_hoops(d, x, y, w, h):
    _sky(d, x, y, w, h, (240, 180, 90), (200, 90, 40))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(150, 90, 40))
    # hoop + ball dropping through
    hx, hy = x + w - 26, y + 22
    d.line([(hx, y + 8), (hx, hy)], fill=(200, 200, 200), width=3)
    d.ellipse([hx - 14, hy, hx + 14, hy + 6], outline=(255, 255, 255), width=3)
    d.ellipse([x + 16, y + 12, x + 40, y + 36], fill=(230, 120, 30),
              outline=(120, 60, 0), width=2)
    d.arc([x + 16, y + 12, x + 40, y + 36], 20, 160, fill=(120, 60, 0), width=2)
    d.line([(x + 16, y + 24), (x + 40, y + 24)], fill=(120, 60, 0), width=2)
    d.line([(x + 28, y + 12), (x + 28, y + 36)], fill=(120, 60, 0), width=2)


def scene_ship(d, x, y, w, h):
    _sky(d, x, y, w, h, (150, 190, 210), (220, 230, 235))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 90, 130))
    for i in range(3):
        d.arc([x + 6 + i * 24, y + h - 26, x + 26 + i * 24, y + h - 10],
              180, 360, fill=(255, 255, 255), width=2)
    # hull + containers + smoke
    d.polygon([(x + 8, y + h - 34), (x + w - 8, y + h - 34),
               (x + w - 18, y + h - 22), (x + 18, y + h - 22)], fill=(90, 30, 30))
    for i, col in enumerate([(200, 60, 40), (40, 120, 180), (220, 160, 40)]):
        d.rectangle([x + 14 + i * 20, y + h - 52, x + 30 + i * 20, y + h - 34],
                    fill=col, outline=(255, 255, 255))
    for i, (sx, sy, r) in enumerate([(0.62, 0.3, 9), (0.7, 0.18, 12), (0.78, 0.08, 15)]):
        d.ellipse([x + int(w * sx) - r, y + int(h * sy) - r,
                   x + int(w * sx) + r, y + int(h * sy) + r], fill=(90, 90, 90))
    d.polygon([(x + int(w * 0.55), y + h - 52), (x + int(w * 0.6), y + h - 66),
               (x + int(w * 0.66), y + h - 52)], fill=(255, 120, 20))


def scene_fire(d, x, y, w, h):
    _sky(d, x, y, w, h, (60, 30, 30), (120, 50, 30))
    d.rectangle([x + 8, y + h - 40, x + w - 8, y + h - 8], fill=(70, 70, 78))
    d.rectangle([x + 8, y + h - 46, x + w - 8, y + h - 40], fill=(40, 40, 46))
    for i in range(3):
        fx = x + 18 + i * 20
        d.polygon([(fx, y + h - 40), (fx + 8, y + h - 66), (fx + 16, y + h - 40)],
                  fill=(255, 140, 20) if i % 2 == 0 else (255, 200, 40))
    d.ellipse([x + w - 22, y + 8, x + w - 6, y + 24], fill=(120, 120, 120))
    d.ellipse([x + w - 30, y + 16, x + w - 12, y + 34], fill=(90, 90, 90))


def scene_quake(d, x, y, w, h):
    _sky(d, x, y, w, h, (190, 170, 130), (120, 100, 70))
    # mountains + crack
    d.polygon([(x, y + h), (x + 18, y + 22), (x + 40, y + h)], fill=(110, 90, 60))
    d.polygon([(x + 26, y + h), (x + 52, y + 12), (x + w - 6, y + h)],
              fill=(90, 75, 50))
    d.polygon([(x + 46, y + 22), (x + 52, y + 12), (x + 58, y + 22)],
              fill=(250, 246, 238))
    d.line([(x + 10, y + h - 6), (x + 26, y + h - 22), (x + 20, y + h - 34),
            (x + 44, y + h - 44), (x + 40, y + h - 56), (x + 62, y + h - 62)],
           fill=(40, 30, 20), width=3)
    # seismograph trace
    pts = []
    for i in range(24):
        px = x + 6 + i * 3
        py = y + h - 14 + (6 if i % 4 == 0 else -6 if i % 4 == 2 else 0)
        pts.append((px, py))
    d.line(pts, fill=(178, 34, 34), width=2)


def scene_tanker(d, x, y, w, h):
    _sky(d, x, y, w, h, (240, 170, 80), (200, 110, 50))
    _sun(d, x + w - 20, y + 18, 13, (255, 240, 180))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 70, 110))
    d.polygon([(x + 10, y + h - 40), (x + w - 10, y + h - 40),
               (x + w - 20, y + h - 26), (x + 20, y + h - 26)], fill=(60, 60, 66))
    d.rectangle([x + w // 2 - 6, y + h - 58, x + w // 2 + 6, y + h - 40],
                fill=(200, 200, 200))
    for i in range(3):
        d.ellipse([x + 14 + i * 10, y + 12 + i * 4, x + 24 + i * 10, y + 22 + i * 4],
                  fill=(120, 60, 30))
    d.polygon([(x + 30, y + 30), (x + 36, y + 12), (x + 42, y + 30)],
              fill=(255, 120, 20))


def scene_dove(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 220, 235), (250, 246, 238))
    _globe(d, x + w // 2, y + h - 26, 20)
    # dove: body, wing, head
    d.ellipse([x + 14, y + 16, x + 52, y + 34], fill=(255, 255, 255),
              outline=(150, 150, 150))
    d.ellipse([x + 46, y + 10, x + 60, y + 24], fill=(255, 255, 255),
              outline=(150, 150, 150))
    d.polygon([(x + 58, y + 16), (x + 68, y + 19), (x + 58, y + 21)],
              fill=(240, 180, 40))
    d.ellipse([x + 52, y + 14, x + 55, y + 17], fill=(20, 20, 20))
    d.polygon([(x + 20, y + 20), (x + 34, y + 6), (x + 44, y + 20)],
              fill=(230, 230, 230), outline=(150, 150, 150))
    d.line([(x + 30, y + 34), (x + 44, y + 44)], fill=(60, 130, 60), width=2)
    d.ellipse([x + 42, y + 40, x + 50, y + 46], fill=(60, 130, 60))


def scene_trade(d, x, y, w, h):
    _sky(d, x, y, w, h, (30, 60, 120), (90, 130, 190))
    # two flags + handshake arc
    d.rectangle([x + 10, y + 12, x + 34, y + 28], fill=(0, 40, 130))
    d.rectangle([x + 10, y + 12, x + 34, y + 20], fill=(200, 40, 40))
    d.rectangle([x + w - 34, y + 12, x + w - 10, y + 28], fill=(200, 40, 40))
    d.rectangle([x + w - 34, y + 20, x + w - 10, y + 28], fill=(255, 255, 255))
    d.arc([x + 14, y + 30, x + w - 14, y + h - 6], 200, 340, fill=(255, 220, 80),
          width=5)
    d.ellipse([x + w // 2 - 8, y + h - 26, x + w // 2 + 8, y + h - 10],
              fill=(255, 220, 80))


def scene_scales(d, x, y, w, h):
    _sky(d, x, y, w, h, (60, 60, 90), (150, 150, 170))
    cx, cy = x + w // 2, y + 14
    d.line([(cx, cy), (cx, y + h - 16)], fill=(220, 200, 120), width=3)
    d.line([(cx - 26, cy + 6), (cx + 26, cy + 6)], fill=(220, 200, 120), width=3)
    for sx in (-26, 26):
        d.line([(cx + sx, cy + 6), (cx + sx, cy + 26)], fill=(200, 180, 100), width=2)
        d.polygon([(cx + sx - 12, cy + 26), (cx + sx + 12, cy + 26),
                   (cx + sx, cy + 38)], fill=(200, 160, 60))
    d.ellipse([cx - 5, cy - 6, cx + 5, cy + 4], fill=(220, 200, 120))


def scene_march(d, x, y, w, h):
    _sky(d, x, y, w, h, (200, 200, 210), (120, 120, 140))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(80, 80, 90))
    for i, col in enumerate([(178, 34, 34), (24, 58, 110), (176, 112, 0),
                             (0, 110, 60), (110, 40, 120)]):
        px = x + 8 + i * 13
        d.ellipse([px, y + 22, px + 9, y + 31], fill=(240, 200, 170))
        d.polygon([(px - 2, y + 32), (px + 11, y + 32), (px + 8, y + h - 14),
                   (px + 1, y + h - 14)], fill=col)
        d.line([(px + 4, y + 32), (px + 4, y + 12)], fill=(60, 60, 60), width=2)
        d.rectangle([px + 4, y + 6, px + 16, y + 14], fill=(255, 255, 255),
                    outline=(60, 60, 60))


def scene_crowd(d, x, y, w, h):
    _sky(d, x, y, w, h, (230, 140, 60), (160, 60, 40))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(60, 40, 30))
    for i in range(7):
        px = x + 6 + i * 10
        d.ellipse([px, y + 26 + (i % 2) * 8, px + 9, y + 35 + (i % 2) * 8],
                  fill=(240, 200, 170))
        d.polygon([(px - 2, y + 36 + (i % 2) * 8), (px + 11, y + 36 + (i % 2) * 8),
                   (px + 8, y + h - 12), (px + 1, y + h - 12)],
                  fill=(120 + i * 12, 50, 40))
    d.rectangle([x + w // 2 - 18, y + 6, x + w // 2 + 18, y + 16],
                fill=(255, 255, 255), outline=(120, 30, 30))


SCENES = {
    "cop": scene_cop, "drones": scene_drones, "cricket": scene_cricket,
    "ballot": scene_ballot, "f1": scene_f1, "hoops": scene_hoops,
    "ship": scene_ship, "fire": scene_fire, "quake": scene_quake,
    "tanker": scene_tanker, "dove": scene_dove, "trade": scene_trade,
    "scales": scene_scales, "march": scene_march, "crowd": scene_crowd,
}


# ---------------------------------------------------------------- map
# Rough continent shapes, hand-plotted in a 620x104 equirectangular box.
CONTINENTS = [
    # North America
    [(18, 22), (52, 14), (96, 10), (128, 18), (118, 34), (96, 40), (78, 52),
     (60, 44), (34, 40), (18, 30)],
    # South America
    [(96, 58), (128, 56), (142, 70), (128, 96), (108, 92), (96, 74)],
    # Europe
    [(268, 12), (300, 8), (322, 16), (316, 30), (292, 32), (272, 26)],
    # Africa
    [(272, 44), (310, 40), (330, 52), (322, 80), (300, 92), (282, 70),
     (270, 56)],
    # Asia
    [(330, 10), (420, 6), (500, 12), (540, 26), (520, 44), (470, 52),
     (420, 46), (360, 44), (332, 28)],
    # SE Asia / Indonesia islands
    [(470, 56), (500, 54), (516, 60), (496, 64), (472, 62)],
    # Australia
    [(500, 76), (540, 74), (556, 84), (530, 94), (502, 88)],
]

# (story num, map x, map y) in the 620x104 box
PINS = [(1, 306, 28), (2, 324, 16), (3, 540, 84), (4, 470, 42),
        (5, 52, 40), (6, 62, 44), (7, 292, 14), (8, 486, 58),
        (9, 108, 76), (10, 392, 40), (11, 348, 34), (12, 300, 46),
        (13, 336, 40), (14, 272, 20), (15, 452, 44)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240),
                outline=RULE, width=1)
    sx, sy = w / 600.0, h / 104.0
    for poly in CONTINENTS:
        pts = [(x + px * sx, y + py * sy) for px, py in poly]
        d.polygon(pts, fill=(196, 178, 140), outline=(120, 100, 70))
    for num, px, py in PINS:
        cx, cy = x + px * sx, y + py * sy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9)
        t = str(num)
        d.text((cx - d.textlength(t, font=f) / 2, cy - 5), t, font=f,
               fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    hline(d, 8, W - 8, 6, fill=INK, width=3)
    center(d, W // 2, 12, "THE SUNDAY GLOBE", font(SERIF_B, 52))
    d.text((10, 30), "No. 326", font=font(SANS, 10), fill=GREY)
    d.text((W - 10 - d.textlength("ONE DAY, ONE PAGE", font=font(SANS, 10)),
            30), "ONE DAY, ONE PAGE", font=font(SANS, 10), fill=GREY)
    center(d, W // 2, 72,
           "SUNDAY, 22 NOVEMBER 2026  •  THE WORLD IN ONE DAY  •  ALL TIMES UTC",
           font(SANS_B, 12))
    hline(d, 8, W - 8, 92, fill=INK, width=2)
    center(d, W // 2, 98,
           "The climate talks collapse, Kyiv endures a night of drones, India "
           "piles up 720 — and the world keeps turning.",
           font(SERIF_I, 15), fill=DARKRED)

    # ---- stat strip
    y = 122
    d.rectangle([8, y, W - 8, y + 34], fill=(255, 255, 255), outline=RULE)
    cw = (W - 16) / 6
    for i, (num, label) in enumerate(STATS):
        cx = 8 + i * cw
        if i:
            d.line([(cx, y + 4), (cx, y + 30)], fill=LIGHT, width=1)
        center(d, cx + cw / 2, y + 2, num, font(SERIF_B, 15), fill=RED)
        center(d, cx + cw / 2, y + 20, label, font(SANS, 8), fill=GREY)
    y += 40

    # ---- region bar + timeline
    rx = 8
    for name, col in REGIONS:
        f = font(SANS_B, 8)
        wch = d.textlength(name, font=f) + 12
        d.rectangle([rx, y, rx + wch, y + 13], fill=col)
        d.text((rx + 6, y + 2), name, font=f, fill=(255, 255, 255))
        rx += wch + 4
    d.text((rx + 4, y + 1), "7 REGIONS  •  36 STORIES  •  15 ILLUSTRATED",
           font=font(SANS_B, 9), fill=INK)
    y += 18
    center(d, W // 2, y, TIMELINE, font(SANS, 8), fill=GREY)
    y += 14
    hline(d, 8, W - 8, y, fill=INK, width=2)
    y += 6

    # ---- three leads
    lead_top = y
    colw = 328
    for i, st in enumerate(LEADS):
        x = 8 + i * (colw + 8)
        SCENES[st["scene"]](d, x, lead_top, colw, 104)
        d.rectangle([x, lead_top, x + colw, lead_top + 104], outline=RULE)
        ty = lead_top + 110
        tag_chip(d, x, ty, st["region"], RED if st["tag"] == "C" else (90, 90, 90))
        d.text((x + 62, ty + 1), "● CONFIRMED" if st["tag"] == "C" else "◆ REPORTED",
               font=font(SANS_B, 8), fill=GREY)
        ty += 18
        ty = para(d, x, ty, st["head"], font(SERIF_B, 21), colw,
                  leading=23, max_lines=3)
        ty = para(d, x, ty + 2, st["dek"], font(SERIF, 13), colw,
                  leading=16, max_lines=4)
        d.text((x, lead_top + 232), "No. %d" % st["num"], font=font(SANS_B, 9),
               fill=RED)
    y = lead_top + 240
    hline(d, 8, W - 8, y, fill=RULE, width=1)
    y += 6

    # ---- 12 small illustrated stories: 4 cols x 3 rows
    cellw, cellh = 248, 82
    for i, st in enumerate(SMALL):
        r, c = divmod(i, 4)
        x = 8 + c * (cellw + 8)
        cy = y + r * (cellh + 6)
        SCENES[st["scene"]](d, x, cy, 72, 72)
        d.rectangle([x, cy, x + 72, cy + 72], outline=RULE)
        tx = x + 80
        d.text((tx, cy), "%d. %s" % (st["num"], st["region"]),
               font=font(SANS_B, 8), fill=RED)
        ty = para(d, tx, cy + 12, st["head"], font(SERIF_B, 13), cellw - 80,
                  leading=14, max_lines=2)
        para(d, tx, ty + 1, st["dek"], font(SERIF, 11), cellw - 80,
             leading=13, max_lines=3)
    y += 3 * cellh + 2 * 6 + 4
    hline(d, 8, W - 8, y, fill=INK, width=2)
    y += 6

    # ---- world map + date check / legend
    map_h = 96
    d.text((8, y), "THE DAY ON THE MAP — numbered pins match the stories above",
           font=font(SANS_B, 10), fill=INK)
    y += 16
    draw_map(d, 8, y, 620, map_h)
    bx = 640
    d.text((bx, y), "DATE CHECK — NOT SUNDAY", font=font(SANS_B, 10), fill=RED)
    para(d, bx, y + 16,
         "Shenzhen summit of Trump, Xi and Putin (19–20 Nov). "
         "'El Chapo Isidro' captured (21 Nov). Peru's M6.7 quake (20 Nov). "
         "S&P 500 correction (20 Nov). None of these is today's news.",
         font(SERIF, 11), W - 8 - bx, leading=14, max_lines=5)
    ly = y + 60
    d.text((bx, ly), "HOW TO READ THIS PAGE", font=font(SANS_B, 10), fill=INK)
    para(d, bx, ly + 16,
         "● CONFIRMED — officials or several outlets. "
         "◆ REPORTED — attributed, single source.",
         font(SERIF, 11), W - 8 - bx, leading=12, max_lines=2)
    y += map_h + 6
    hline(d, 8, W - 8, y, fill=INK, width=2)
    y += 6

    # ---- also on Sunday: 21 more stories, 3 columns
    d.text((8, y), "ALSO ON SUNDAY 22 NOVEMBER — 21 MORE STORIES",
           font=font(SANS_B, 11), fill=INK)
    y += 18
    colw = 328
    for i, item in enumerate(ALSO):
        c = i // 7
        r = i % 7
        x = 8 + c * (colw + 8)
        iy = y + r * 18
        d.text((x, iy), "%d." % (16 + i), font=font(SANS_B, 10), fill=RED)
        para(d, x + 20, iy, item, font(SERIF, 11), colw - 20, leading=13,
             max_lines=2)
    y += 7 * 18 + 4
    hline(d, 8, W - 8, y, fill=INK, width=2)

    # ---- footer
    y += 5
    center(d, W // 2, y,
           "Sources: UN News, Reuters, AP, The Times, Ukrainian Air Force, "
           "ESPNcricinfo, Formula 1, NBA, Finnish Border Guard, USGS, HK Govt.",
           font(SANS, 9), fill=GREY)
    y += 14
    center(d, W // 2, y,
           "All 36 stories happened or were first reported on Sunday 22 November "
           "2026. Illustrations drawn in code for this page. — THE SUNDAY GLOBE",
           font(SERIF_I, 10), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])
    return OUT


if __name__ == "__main__":
    build()
