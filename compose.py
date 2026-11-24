#!/usr/bin/env python3
"""Compose the front page for make.fun news-image-20261123.

Reads the six text-free illustration panels in panels/ and draws every word
of the newspaper front page programmatically with Pillow. The output is a
deterministic 1024x1024 JPEG (kept under the name entry.png, as the rules
allow either PNG or JPEG bytes in that file).

Run:  python3 compose.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)      # warm newsprint cream
INK = (26, 26, 26)           # near-black headline ink
RED = (163, 18, 18)          # kicker / rule accent
GREY = (84, 78, 70)          # deck and body grey
RULE = (120, 110, 96)        # hairline rule colour

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# JPEG quality ladder: first entry that fits under the 1 MiB cap wins.
# Pillow's JPEG encoder is deterministic, so the output is reproducible.
QUALITY_LADDER = (92, 88, 84, 80, 76, 72, 68, 64)
SIZE_LIMIT = 1048576


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, y, text, fnt, fill, x0=0, x1=W):
    """Draw one line centred between x0 and x1; returns its height."""
    tw = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)
    return fnt.size


def draw_block(draw, x, y, width, lines, fnt, fill, leading):
    """Draw wrapped lines left-aligned; returns the y after the block."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover_crop(img, target_w, target_h, v_bias=0.35):
    """Centre-crop an image to the target aspect, then resize to it.

    v_bias (0..1) places the crop band vertically: 0 keeps the top,
    1 the bottom. The default favours the upper half.
    """
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        # source is wider: trim the sides
        new_w = int(src_h * tgt_ratio)
        left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        # source is taller: trim top and bottom per v_bias
        new_h = int(src_w / tgt_ratio)
        top = int((src_h - new_h) * v_bias)
        box = (0, top, src_w, top + new_h)
    return img.crop(box).resize((target_w, target_h), Image.LANCZOS)


def hairline(draw, y, x0=24, x1=W - 24, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def story_column(page, draw, x, y, width, panel, kicker, headline, body,
                 img_h, head_size=25, head_lines=2, body_lines=2):
    """One small story: picture, red kicker, headline, short body text."""
    img = cover_crop(Image.open(os.path.join(PANELS, panel)), width, img_h)
    page.paste(img, (x, y))
    y += img_h + 8
    draw.text((x, y), kicker, font=font(SANS_BOLD, 15), fill=RED)
    y += 22
    head_fnt = font(SERIF_BOLD, head_size)
    head = wrap(draw, headline, head_fnt, width)[:head_lines]
    y = draw_block(draw, x, y, width, head, head_fnt, INK, head_size + 4)
    y += 4
    body_fnt = font(SANS, 16)
    lines = wrap(draw, body, body_fnt, width)[:body_lines]
    y = draw_block(draw, x, y, width, lines, body_fnt, GREY, 20)
    return y


def build():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    draw_centered(draw, 14, "THE WORLD IN ONE DAY",
                  font(SERIF_BOLD, 60), INK)
    draw_centered(draw, 82, "MONDAY, 23 NOVEMBER 2026",
                  font(SANS_BOLD, 27), RED)
    hairline(draw, 116, width=2)

    # ---- Lead story: Huang returns to Nvidia ---------------------------
    # v_bias 0.55 keeps the CEO figure in frame; the default upper-half
    # crop caught only the top of his head.
    hero = cover_crop(Image.open(os.path.join(PANELS, "hero.png")),
                      976, 232, v_bias=0.55)
    page.paste(hero, (24, 126))
    draw.text((24, 366), "HUANG RETURNS AS NVIDIA CHIEF",
              font=font(SERIF_BOLD, 40), fill=INK)
    deck = wrap(draw,
                "Nvidia's board reinstates Jensen Huang after President "
                "Trump intervenes; shares jump 31.5%, adding nearly "
                "$1 trillion. The US blacklists Megaspeed the same day.",
                font(SERIF, 19), 976)
    draw_block(draw, 24, 414, 976, deck[:2], font(SERIF, 19), GREY, 24)
    hairline(draw, 470)

    # ---- Second row: three stories --------------------------------------
    col_w, gap = 312, 20
    y2 = 482
    story_column(page, draw, 24, y2, col_w, "nato.png",
                 "POLAND",
                 "NATO on alert after missiles hit Poland",
                 "Russian missiles hit Poland on Friday; NATO sends "
                 "radar jets.",
                 img_h=120)
    story_column(page, draw, 24 + col_w + gap, y2, col_w, "mexico.png",
                 "MEXICO",
                 "US drone helped catch 'El Chapo Isidro'",
                 "A US drone tracked the fugitive; eight more arrested "
                 "after the raid.",
                 img_h=120)
    story_column(page, draw, 24 + 2 * (col_w + gap), y2, col_w, "factory.png",
                 "INDONESIA",
                 "Factory fire toll confirmed at 24",
                 "Toll confirmed at 24; dozens still missing after "
                 "Saturday's blaze.",
                 img_h=120)
    hairline(draw, 744)

    # ---- Third row: two stories -----------------------------------------
    col2_w = 478
    y3 = 756
    story_column(page, draw, 24, y3, col2_w, "nepal.png",
                 "NEPAL",
                 "India pledges $1.62bn to Nepal",
                 "Package worth 240bn rupees for flood-hit Nepal; New "
                 "Delhi calls it a reset of ties.",
                 img_h=130, head_size=25, head_lines=1, body_lines=2)
    story_column(page, draw, 24 + col2_w + gap, y3, col2_w, "dymer.png",
                 "UKRAINE",
                 "Dymer strike toll rises to 11",
                 "Drone strike wrecked an apartment block near Kyiv; 14 "
                 "were missing. Zelenskyy presses for air defences.",
                 img_h=130, head_size=25, head_lines=1, body_lines=2)

    # ---- Footer ----------------------------------------------------------
    hairline(draw, 994)
    draw_centered(draw, 1000,
                  "Sources: Associated Press  ·  Reuters  ·  BBC  ·  Al Jazeera"
                  "   —   All events of Monday, 23 November 2026",
                  font(SANS, 13), GREY)
    return page


def main():
    page = build()
    for quality in QUALITY_LADDER:
        page.save(OUT, format="JPEG", quality=quality, optimize=True,
                  progressive=False)
        size = os.path.getsize(OUT)
        if size <= SIZE_LIMIT:
            print(f"entry.png: {page.size[0]}x{page.size[1]} "
                  f"JPEG quality {quality}, {size} bytes")
            return
    raise SystemExit(f"entry.png still over {SIZE_LIMIT} bytes at "
                     f"quality {QUALITY_LADDER[-1]}")


if __name__ == "__main__":
    main()
