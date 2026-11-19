#!/usr/bin/env python3
"""Render the GTA VI loading screen meme for gta6-meme-x-01.

Draws everything programmatically with PIL: Vice City sunset, skyline and
palm silhouettes, the make.fun ghost leaning on a 99% loading bar, and all
caption text. No external image assets. Output: meme.png, 1024x1024.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2  # supersample factor
W, H = 1024 * S, 1024 * S
OUT = "meme.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, int(size * S))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def text(draw, cx, y, s, fnt, fill, stroke=0, stroke_fill=(10, 5, 20)):
    """Draw text centred at cx, top at y, with an outline for contrast."""
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill,
              stroke_width=int(stroke * S), stroke_fill=stroke_fill)


def sparkle(draw, cx, cy, r, fill):
    """Four-pointed star (sparkle) centred at cx, cy with radius r."""
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rad = r if i % 2 == 0 else r * 0.28
        pts.append((cx + rad * math.cos(ang), cy - rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def ghost(draw, cx, top, wdt, hgt):
    """The make.fun ghost: white body, thick black outline, sparkle eyes,
    one small round hand holding a magenta coin with a white star."""
    x0, x1 = cx - wdt / 2, cx + wdt / 2
    y0, y1 = top, top + hgt
    # Body outline: dome top, straight sides, wavy hem.
    body = []
    n = 40
    for i in range(n + 1):  # dome arc, left to right
        a = math.pi - i * math.pi / n
        body.append((cx + (wdt / 2) * math.cos(a),
                     y0 + (wdt / 2) * (1 - math.sin(a)) * 0.9))
    hem_y = y1
    waves = 5
    nhem = 120
    for i in range(nhem + 1):  # smooth wavy hem, right to left
        x = x1 - i * (wdt / nhem)
        y = hem_y - (12 * S) * (0.5 + 0.5 * math.sin(i / nhem * waves * 2 * math.pi))
        body.append((x, y))
    body.append((x0, y0 + (wdt / 2) * 0.9))
    draw.polygon(body, fill=(255, 255, 255),
                 outline=(12, 8, 18), width=int(9 * S))
    # Sparkle eyes.
    ey, er = y0 + hgt * 0.34, 30 * S
    sparkle(draw, cx - wdt * 0.17, ey, er, (12, 8, 18))
    sparkle(draw, cx + wdt * 0.17, ey, er, (12, 8, 18))
    # Arm and hand holding the coin, on the ghost's right side.
    hx, hy = x1 + 6 * S, y0 + hgt * 0.62
    draw.line([(x1 - 8 * S, y0 + hgt * 0.58), (hx, hy)],
              fill=(12, 8, 18), width=int(10 * S))
    coin_cx, coin_cy, coin_r = hx + 52 * S, hy - 14 * S, 46 * S
    draw.ellipse([coin_cx - coin_r, coin_cy - coin_r,
                  coin_cx + coin_r, coin_cy + coin_r],
                 fill=(226, 0, 122), outline=(12, 8, 18), width=int(7 * S))
    sparkle(draw, coin_cx, coin_cy, 30 * S, (255, 255, 255))
    draw.ellipse([hx - 17 * S, hy - 17 * S, hx + 17 * S, hy + 17 * S],
                 fill=(255, 255, 255), outline=(12, 8, 18), width=int(6 * S))


def palm(draw, x, y, hgt, lean=1):
    """A simple palm-tree silhouette rooted at (x, y)."""
    trunk_w = 12 * S
    top_x = x + 30 * S * lean
    draw.line([(x, y), (top_x, y - hgt)], fill=(24, 8, 34),
              width=int(trunk_w))
    for k in range(7):
        ang = math.pi * (0.08 + 0.13 * k)
        direction = 1 if k % 2 == 0 else -1
        ex = top_x + direction * math.cos(ang) * 100 * S
        ey = y - hgt - math.sin(ang) * 40 * S + 55 * S
        # Drooping frond as a quadratic bezier from the crown.
        mx = top_x + direction * math.cos(ang) * 55 * S
        my = y - hgt - math.sin(ang) * 70 * S
        pts = []
        for i in range(13):
            t = i / 12
            px = (1 - t) ** 2 * top_x + 2 * (1 - t) * t * mx + t ** 2 * ex
            py = (1 - t) ** 2 * (y - hgt) + 2 * (1 - t) * t * my + t ** 2 * ey
            pts.append((px, py))
        draw.line(pts, fill=(24, 8, 34), width=int(8 * S))


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # Sunset gradient: deep purple top, magenta mid, orange horizon.
    stops = [(0.0, (26, 11, 46)), (0.42, (123, 30, 110)),
             (0.62, (255, 94, 60)), (0.72, (255, 150, 60)),
             (1.0, (24, 8, 34))]
    for yy in range(H):
        t = yy / H
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                tt = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
                d.line([(0, yy), (W, yy)], fill=lerp(stops[i][1],
                                                      stops[i + 1][1], tt))
                break
    # Soft sun glow: one big disc, blurred so no rings show.
    sun_cx, sun_cy, sun_r = 512 * S, 600 * S, 150 * S
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([sun_cx - sun_r * 2.4, sun_cy - sun_r * 2.4,
                sun_cx + sun_r * 2.4, sun_cy + sun_r * 2.4],
               fill=(255, 120, 60, 130))
    glow = glow.filter(ImageFilter.GaussianBlur(110 * S))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r,
               sun_cx + sun_r, sun_cy + sun_r], fill=(255, 214, 110))
    # Skyline silhouettes with a few lit windows.
    import random
    random.seed(6)
    bx = -20 * S
    while bx < W:
        bw = random.randint(70, 150) * S
        bh = random.randint(90, 210) * S
        d.rectangle([bx, 760 * S - bh, bx + bw, 800 * S],
                    fill=(30, 10, 44))
        for _ in range(random.randint(2, 6)):
            wx = bx + random.randint(8, max(9, int(bw / S) - 14)) * S
            wy = 760 * S - bh + random.randint(10, max(11, int(bh / S) - 20)) * S
            d.rectangle([wx, wy, wx + 8 * S, wy + 12 * S],
                        fill=(255, 190, 90))
        bx += bw + random.randint(6, 26) * S
    palm(d, 70 * S, 800 * S, 260 * S, lean=1)
    palm(d, 150 * S, 800 * S, 200 * S, lean=-1)
    palm(d, 950 * S, 800 * S, 230 * S, lean=-1)
    # Ground band.
    d.rectangle([0, 800 * S, W, H], fill=(18, 6, 28))

    # Title, auto-fit so it never touches the edges.
    title_size = 76
    while d.textlength("GRAND THEFT AUTO VI", font=font(title_size)) > 940 * S:
        title_size -= 2
    text(d, 512 * S, 52 * S, "GRAND THEFT AUTO VI", font(title_size),
         (255, 255, 255), stroke=7)
    # Subtitle.
    text(d, 512 * S, 400 * S, "LOADING LEONIDA...", font(58),
         (255, 255, 255), stroke=6)

    # Ghost leaning on the loading bar, right side.
    ghost(d, 780 * S, 470 * S, 240 * S, 250 * S)

    # Loading bar.
    bar_x0, bar_x1 = 90 * S, 934 * S
    bar_y0, bar_y1 = 712 * S, 762 * S
    d.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=25 * S,
                        fill=(20, 8, 30), outline=(255, 255, 255),
                        width=int(5 * S))
    fill_x1 = bar_x0 + (bar_x1 - bar_x0) * 0.99
    d.rounded_rectangle([bar_x0 + 4 * S, bar_y0 + 4 * S,
                         fill_x1, bar_y1 - 4 * S], radius=20 * S,
                        fill=(226, 0, 122))
    text(d, 150 * S, 640 * S, "99%", font(56), (255, 255, 255), stroke=6)

    # Below the bar.
    text(d, 512 * S, 792 * S, "13 YEARS ELAPSED", font(54),
         (255, 255, 255), stroke=6)
    text(d, 512 * S, 872 * S, "TIP: While you waited 4,811 days,", font(34),
         (255, 230, 140), stroke=4)
    text(d, 512 * S, 922 * S, "my AI agent earned real money on make.fun.",
         font(34), (255, 230, 140), stroke=4)

    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
