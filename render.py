#!/usr/bin/env python3
"""Draw the front page of Saturday, 21 November 2026.

One image, 1024x1024, deterministic: only Pillow primitives, fixed fonts,
no randomness, no network, no time dependence.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (10, 22, 40)
NAVY2 = (18, 38, 66)
PAPER = (255, 255, 255)
INK = (13, 27, 46)
GREY = (88, 102, 120)
RED = (198, 28, 44)
RED_DK = (160, 18, 32)
GOLD = (214, 176, 58)
GOLD_DK = (176, 140, 40)
LIGHT = (232, 239, 247)
LIGHT2 = (240, 243, 248)
TEAL = (0, 148, 134)
ORANGE = (228, 120, 30)
PURPLE = (118, 78, 178)
BLUE = (28, 108, 198)
GREEN = (38, 158, 78)
BROWN = (146, 96, 48)


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, xy, text, fnt, fill, max_w, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def card(d, x, y, w, h, accent=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PAPER)
    if accent:
        d.rounded_rectangle([x, y, x + 9, y + h], radius=4, fill=accent)


# ---------------- pictograms (drawn, each with its own character) ----------------

def pic_chart(d, x, y, w, h):
    """Lead: candlesticks plunging, big red down arrow, cracked AI chip."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 246))
    for gy in range(5):
        yy = y + 24 + gy * (h - 48) // 4
        d.line([x + 14, yy, x + w - 14, yy], fill=(205, 218, 232), width=1)
    # descending red candles
    candles = [(0.10, 0.34, 0.52), (0.26, 0.44, 0.60), (0.42, 0.55, 0.72),
               (0.58, 0.66, 0.82), (0.74, 0.76, 0.92)]
    for fx, top, bot in candles:
        cx = x + int(fx * w)
        d.line([cx, y + int(top * h) - 10, cx, y + int(bot * h) + 10],
               fill=RED_DK, width=3)
        d.rectangle([cx - 13, y + int(top * h), cx + 13, y + int(bot * h)],
                    fill=RED)
    # big diagonal down arrow
    ax0, ay0 = x + 26, y + 26
    ax1, ay1 = x + w - 30, y + h - 46
    d.line([ax0, ay0, ax1, ay1], fill=RED_DK, width=7)
    d.polygon([(ax1, ay1), (ax1 - 26, ay1 - 4), (ax1 - 6, ay1 - 26)],
              fill=RED_DK)
    # cracked AI chip, top right
    cx, cy, s = x + w - 92, y + 18, 56
    d.rounded_rectangle([cx, cy, cx + s, cy + s], radius=6, fill=NAVY)
    for k in range(3):
        d.line([cx + 10 + k * 18, cy - 6, cx + 10 + k * 18, cy], fill=NAVY, width=4)
        d.line([cx + 10 + k * 18, cy + s, cx + 10 + k * 18, cy + s + 6],
               fill=NAVY, width=4)
    d.text((cx + 12, cy + 15), "AI", font=font(22, True), fill=(255, 255, 255))
    d.line([cx + 8, cy + 6, cx + 26, cy + 26, cx + 20, cy + 44],
           fill=GOLD, width=3)
    d.text((x + 18, y + h - 38), "NASDAQ -5.3%", font=font(21, True),
           fill=RED_DK)


def pic_missile(d, x, y, w, h):
    """Shield deflecting a missile with a flame trail."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 246))
    # shield
    sx, sy = x + w // 2 - 34, y + 26
    d.polygon([(sx, sy), (sx + 68, sy), (sx + 68, sy + 44),
               (sx + 34, sy + 84), (sx, sy + 44)], fill=BLUE)
    d.polygon([(sx + 8, sy + 6), (sx + 60, sy + 6), (sx + 60, sy + 42),
               (sx + 34, sy + 72), (sx + 8, sy + 42)], fill=(60, 140, 220))
    d.text((sx + 24, sy + 22), "3", font=font(30, True), fill=(255, 255, 255))
    # missile crossing top right with flame
    mx, my = x + w - 96, y + 14
    d.polygon([(mx, my + 10), (mx + 52, my), (mx + 66, my + 10),
               (mx + 52, my + 20), (mx, my + 20)], fill=(90, 100, 112))
    d.polygon([(mx + 52, my), (mx + 66, my + 10), (mx + 52, my + 20)],
              fill=RED)
    for k, c in enumerate([(255, 170, 40), (255, 110, 30), (255, 200, 80)]):
        d.polygon([(mx - 4 - k * 12, my + 2), (mx - 4 - k * 12, my + 18),
                   (mx - 22 - k * 12, my + 10)], fill=c)
    # ground line only; the shield already tells the story
    d.line([x + 16, y + h - 26, x + w - 16, y + h - 26], fill=GREY, width=2)


def pic_cop(d, x, y, w, h):
    """Globe with leaf, rising thermometer, overtime clock."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 232))
    cx, cy, r = x + w // 2 - 6, y + h // 2 - 6, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 160, 210))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.polygon([(cx - 26, cy - 18), (cx - 6, cy - 30), (cx + 8, cy - 12),
               (cx - 12, cy + 2)], fill=GREEN)
    d.polygon([(cx + 4, cy + 12), (cx + 26, cy + 4), (cx + 30, cy + 24),
               (cx + 10, cy + 30)], fill=GREEN)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255),
          width=3)
    # thermometer
    tx, ty = x + w - 34, y + 16
    d.rounded_rectangle([tx, ty, tx + 14, ty + 52], radius=7, fill=PAPER,
                        outline=RED, width=2)
    d.rectangle([tx + 3, ty + 30, tx + 11, ty + 49], fill=RED)
    d.ellipse([tx - 3, ty + 48, tx + 17, ty + 68], fill=RED)
    # small clock showing overtime
    kx, ky, kr = x + 26, y + h - 30, 15
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=PAPER,
              outline=NAVY, width=2)
    d.line([kx, ky, kx, ky - 9], fill=NAVY, width=2)
    d.line([kx, ky, kx + 8, ky + 3], fill=NAVY, width=2)


def pic_quake(d, x, y, w, h):
    """Tilting building over a cracked street, seismic arcs."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 222))
    # seismic arcs
    for k, r in enumerate((14, 26, 38)):
        d.arc([x + w // 2 - r, y + 12 - r // 2, x + w // 2 + r,
               y + 12 + r // 2], 200, 340, fill=ORANGE, width=3)
    # tilting building
    bx, by = x + w // 2 - 22, y + 34
    d.polygon([(bx, by + 52), (bx + 6, by), (bx + 44, by + 8),
               (bx + 40, by + 52)], fill=(150, 120, 88))
    for r in range(3):
        for c in range(2):
            d.rectangle([bx + 8 + c * 16, by + 10 + r * 14,
                         bx + 18 + c * 16, by + 20 + r * 14],
                        fill=(255, 220, 130))
    # cracked ground, crack kept to the right half
    d.line([x + 8, y + h - 26, x + w - 8, y + h - 26], fill=NAVY, width=3)
    d.line([x + w // 2 + 2, y + h - 26, x + w // 2 + 16, y + h - 12,
            x + w // 2 + 4, y + h - 4], fill=RED_DK, width=3)


def pic_fire(d, x, y, w, h):
    """Power-station tower with flame and smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(246, 232, 222))
    # tower
    tx = x + w // 2 - 20
    d.polygon([(tx, y + h - 30), (tx + 8, y + 34), (tx + 32, y + 34),
               (tx + 40, y + h - 30)], fill=(120, 118, 112))
    d.rectangle([tx + 6, y + 30, tx + 34, y + 40], fill=(90, 88, 84))
    for r in range(2):
        d.rectangle([tx + 10, y + 52 + r * 18, tx + 30, y + 62 + r * 18],
                    fill=(255, 220, 130))
    # flame
    fx, fy = x + w // 2, y + 26
    d.polygon([(fx - 16, fy + 16), (fx - 6, fy - 14), (fx + 2, fy + 2),
               (fx + 10, fy - 18), (fx + 18, fy + 16)],
              fill=(255, 140, 20))
    d.polygon([(fx - 8, fy + 16), (fx, fy - 2), (fx + 8, fy + 16)],
              fill=(255, 210, 60))
    # smoke puffs
    for k, (sx, sy, sr) in enumerate([(x + 16, y + 22, 9), (x + 30, y + 12, 11),
                                      (x + w - 24, y + 18, 10)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 150))
    d.line([x + 8, y + h - 30, x + w - 8, y + h - 30], fill=NAVY, width=3)


def pic_robot(d, x, y, w, h):
    """Robot head inside a red prohibition ring."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 232, 246))
    cx, cy = x + w // 2, y + h // 2 + 4
    # antenna
    d.line([cx, cy - 34, cx, cy - 48], fill=NAVY, width=3)
    d.ellipse([cx - 5, cy - 54, cx + 5, cy - 44], fill=RED)
    # head
    d.rounded_rectangle([cx - 30, cy - 34, cx + 30, cy + 26], radius=10,
                        fill=(150, 160, 175), outline=NAVY, width=3)
    d.ellipse([cx - 18, cy - 18, cx - 4, cy - 4], fill=(30, 220, 220))
    d.ellipse([cx + 4, cy - 18, cx + 18, cy - 4], fill=(30, 220, 220))
    for k in range(4):
        d.line([cx - 16 + k * 11, cy + 12, cx - 16 + k * 11, cy + 18],
               fill=NAVY, width=3)
    # prohibition ring + slash
    d.ellipse([cx - 44, cy - 48, cx + 44, cy + 40], outline=RED, width=6)
    d.line([cx - 31, cy + 28, cx + 31, cy - 34], fill=RED, width=6)


def pic_nato(d, x, y, w, h):
    """Four-point NATO-style star on a blue shield, map pin."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 246))
    cx, cy = x + w // 2 - 8, y + h // 2
    d.polygon([(cx, cy - 40), (cx + 44, cy), (cx, cy + 40), (cx - 44, cy)],
              fill=BLUE)
    d.polygon([(cx, cy - 26), (cx + 26, cy), (cx, cy + 26), (cx - 26, cy)],
              fill=(255, 255, 255))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=BLUE)
    # map pin
    px, py = x + w - 26, y + h - 34
    d.ellipse([px - 11, py - 22, px + 11, py], fill=RED)
    d.polygon([(px - 11, py - 6), (px + 11, py - 6), (px, py + 14)], fill=RED)
    d.ellipse([px - 4, py - 15, px + 4, py - 7], fill=(255, 255, 255))


def pic_chip(d, x, y, w, h):
    """Microchip with a lightning bolt and AI label."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 244))
    cx, cy, s = x + w // 2 - 26, y + h // 2 - 26, 52
    d.rounded_rectangle([cx, cy, cx + s, cy + s], radius=8, fill=NAVY)
    for k in range(3):
        d.line([cx + 10 + k * 16, cy - 8, cx + 10 + k * 16, cy], fill=NAVY,
               width=4)
        d.line([cx + 10 + k * 16, cy + s, cx + 10 + k * 16, cy + s + 8],
               fill=NAVY, width=4)
        d.line([cx - 8, cy + 10 + k * 16, cx, cy + 10 + k * 16], fill=NAVY,
               width=4)
        d.line([cx + s, cy + 10 + k * 16, cx + s + 8, cy + 10 + k * 16],
               fill=NAVY, width=4)
    # lightning bolt
    d.polygon([(cx + 30, cy + 6), (cx + 16, cy + 28), (cx + 26, cy + 28),
               (cx + 20, cy + 46), (cx + 36, cy + 22), (cx + 26, cy + 22)],
              fill=GOLD)
    d.text((cx + 4, cy + 34), "AI", font=font(13, True), fill=(255, 255, 255))


def pic_gavel(d, x, y, w, h):
    """Gavel over a law document with a '6' badge."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 226))
    # document
    dx, dy = x + 14, y + 30
    d.rectangle([dx, dy, dx + 44, dy + 52], fill=PAPER, outline=NAVY, width=2)
    for k in range(4):
        d.line([dx + 7, dy + 12 + k * 10, dx + 37, dy + 12 + k * 10],
               fill=GREY, width=2)
    # gavel: horizontal head, vertical handle, clear of the document
    d.rounded_rectangle([x + w - 46, y + 14, x + w - 10, y + 32], radius=6,
                        fill=BROWN)
    d.line([x + w - 28, y + 32, x + w - 28, y + 62], fill=BROWN, width=7)
    # badge "6"
    bx, by = x + w - 30, y + h - 32
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=RED)
    d.text((bx - 6, by - 11), "6", font=font(17, True), fill=(255, 255, 255))


def pic_phone(d, x, y, w, h):
    """Phone with a protest placard."""
    d.rectangle([x, y, x + w, y + h], fill=(236, 232, 246))
    # phone
    px, py = x + 12, y + 18
    d.rounded_rectangle([px, py, px + 34, py + 58], radius=6, fill=NAVY)
    d.rectangle([px + 4, py + 8, px + 30, py + 44], fill=(255, 255, 255))
    d.text((px + 9, py + 18), "f", font=font(22, True), fill=BLUE)
    # placard
    d.line([x + w - 26, y + 30, x + w - 26, y + h - 14], fill=BROWN, width=4)
    d.rectangle([x + w - 52, y + 12, x + w - 2, y + 40], fill=RED)
    d.text((x + w - 46, y + 18), "NO!", font=font(15, True),
           fill=(255, 255, 255))


def pic_hockey(d, x, y, w, h):
    """Crossed hockey sticks, ball, and a 3-0 score bug."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 232))
    cx, cy = x + w // 2, y + h // 2 + 6
    d.line([cx - 30, cy - 30, cx + 26, cy + 26], fill=BROWN, width=6)
    d.line([cx + 30, cy - 30, cx - 26, cy + 26], fill=(60, 90, 60), width=6)
    d.ellipse([cx - 8, cy + 14, cx + 8, cy + 30], fill=NAVY)
    d.rounded_rectangle([x + 6, y + 8, x + 62, y + 30], radius=8, fill=NAVY)
    d.text((x + 12, y + 11), "3-0", font=font(16, True), fill=GOLD)


def pic_fta(d, x, y, w, h):
    """Two flags with a double arrow between them."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 246))
    # left flag
    d.line([x + 14, y + 16, x + 14, y + h - 16], fill=NAVY, width=3)
    d.polygon([(x + 14, y + 16), (x + 46, y + 22), (x + 14, y + 32)],
              fill=RED)
    d.ellipse([x + 20, y + 21, x + 26, y + 27], fill=(255, 255, 255))
    # right flag
    d.line([x + w - 14, y + 16, x + w - 14, y + h - 16], fill=NAVY, width=3)
    d.polygon([(x + w - 14, y + 16), (x + w - 46, y + 22),
               (x + w - 14, y + 32)], fill=(200, 40, 40))
    # double arrow
    ay = y + h // 2 + 8
    d.line([x + 22, ay, x + w - 22, ay], fill=TEAL, width=4)
    d.polygon([(x + w - 22, ay), (x + w - 34, ay - 7), (x + w - 34, ay + 7)],
              fill=TEAL)
    d.polygon([(x + 22, ay), (x + 34, ay - 7), (x + 34, ay + 7)], fill=TEAL)
    d.text((x + w // 2 - 16, ay - 28), "FTA", font=font(17, True), fill=TEAL)


def pic_globe_small(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 160, 210),
              outline=GOLD, width=2)
    d.polygon([(cx - r + 4, cy - 6), (cx - 4, cy - r + 4), (cx + 6, cy - 2),
               (cx - 4, cy + 6)], fill=GREEN)
    d.polygon([(cx + 2, cy + 8), (cx + r - 4, cy + 2), (cx + r - 6, cy + 12),
               (cx + 4, cy + r - 4)], fill=GREEN)


# ---------------- page ----------------

def render(out_path):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- masthead: bold, red top bar, big title, gold date ----
    d.rectangle([0, 0, W, 8], fill=RED)
    pic_globe_small(d, 78, 62, 34)
    pic_globe_small(d, W - 78, 62, 34)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=font(52, True),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 76), "SATURDAY, 21 NOVEMBER 2026", font=font(30, True),
           fill=GOLD, anchor="ma")
    d.rectangle([24, 122, W - 24, 126], fill=GOLD)
    d.rectangle([24, 130, W - 24, 133], fill=RED)

    # ---- lead: bigger, dramatic ----
    lx, ly, lw, lh = 24, 146, 976, 234
    card(d, lx, ly, lw, lh, accent=RED)
    pic_chart(d, lx + 10, ly, 330, lh)
    tx = lx + 362
    d.text((tx, ly + 20), "MARKETS  ·  UNITED STATES", font=font(17, True),
           fill=RED)
    draw_wrapped(d, (tx, ly + 48), "WALL STREET SLIDES INTO CORRECTION",
                 font(34, True), INK, lw - 386, leading=40)
    draw_wrapped(
        d, (tx, ly + 140),
        "S&P 500 -3.7%, Nasdaq -5.3% as the AI trade unwinds. "
        "Nvidia -14% as the SEC probes its accounting; Anthropic -9% on day two.",
        font(19), GREY, lw - 386, leading=25)

    # ---- half-width row ----
    hy, hh = 394, 162
    for i, (pic, title, body, accent) in enumerate([
        (pic_missile, "THREE MISSILES AT RIYADH STOPPED",
         "Saudi-led coalition intercepts Houthi ballistic missiles; "
         "strikes hit Hodeidah and Sanaa. Houthis claim 41 dead.", BLUE),
        (pic_cop, "COP31 RUNS INTO OVERTIME",
         "Antalya talks miss their deadline; the draft drops all mention "
         "of fossil fuels. A third draft is due Saturday.", TEAL),
    ]):
        hx = 24 + i * 500
        card(d, hx, hy, 476, hh, accent=accent)
        pic(d, hx + 10, hy, 148, hh)
        tx = hx + 176
        draw_wrapped(d, (tx, hy + 16), title, font(20, True), INK, 288,
                     leading=24)
        draw_wrapped(d, (tx, hy + 68), body, font(15), GREY, 288, leading=19)

    # ---- grid 3 x 2 ----
    grid = [
        (pic_quake, "6.8 QUAKE SHAKES PERU",
         "Tremor in Junin felt in Lima; residents rush into the streets. "
         "No casualties reported.", ORANGE),
        (pic_fire, "BASRA POWER PLANT FIRE",
         "Blaze at Hartha station kills 4 and injures 30 in southern Iraq.",
         RED),
        (pic_robot, "UN MOVES TO CURB 'KILLER ROBOTS'",
         "States agree talks to regulate autonomous weapons by 2028.",
         PURPLE),
        (pic_nato, "NATO CONDEMNS POLAND INCURSION",
         "Chief Rutte heads to Warsaw; France seeks a UN Security Council "
         "meeting.", BLUE),
        (pic_chip, "SEOUL: SPEED IS VITAL IN AI RACE",
         "President Lee tours a data centre under construction in Ulsan.",
         TEAL),
        (pic_gavel, "VIETNAM SPEEDS LAND SEIZURES",
         "New laws also widen data control and drop the death penalty for "
         "six crimes.", BROWN),
    ]
    for i, (pic, title, body, accent) in enumerate(grid):
        gx = 24 + (i % 3) * 329
        gy = 570 + (i // 3) * 141
        card(d, gx, gy, 317, 129, accent=accent)
        pic(d, gx + 10, gy, 86, 129)
        tx = gx + 108
        y = draw_wrapped(d, (tx, gy + 12), title, font(18, True), INK, 198,
                         leading=21)
        draw_wrapped(d, (tx, y + 4), body, font(14), GREY, 198, leading=18)

    # ---- ALSO TODAY ----
    d.text((24, 856), "ALSO TODAY", font=font(20, True), fill=GOLD)
    d.rectangle([168, 866, W - 24, 869], fill=GOLD)
    also = [
        (pic_phone, "PROTESTS AT META'S INDIA OFFICES",
         "Congress youth wing clashes with police over removed accounts."),
        (pic_hockey, "MALAYSIA 3-0 SOUTH KOREA",
         "Hosts open the Sultan Azlan Shah Cup with a win in Ipoh."),
        (pic_fta, "SINGAPORE-CHINA TRADE TALKS",
         "Negotiations begin to upgrade the two nations' free-trade deal."),
    ]
    for i, (pic, title, body) in enumerate(also):
        ax = 24 + i * 329
        ay = 884
        card(d, ax, ay, 317, 112, accent=GOLD)
        pic(d, ax + 10, ay, 72, 112)
        tx = ax + 94
        y = draw_wrapped(d, (tx, ay + 10), title, font(16, True), INK, 212,
                         leading=19)
        draw_wrapped(d, (tx, y + 3), body, font(13), GREY, 212, leading=16)

    img.save(out_path, format="PNG", optimize=True)
    print("saved", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    render("entry.png")
