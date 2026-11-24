#!/usr/bin/env python3
"""Render ad.png: the entry presented as its ad page (PIL render).

Reads entry.png, scales it into a 1024x768 ad frame with the masthead and a
referral footer. Deterministic: no clock, no network.
"""
from PIL import Image, ImageDraw, ImageFont

FONTDIR = "/usr/share/fonts/truetype/dejavu/"
NAVY = (18, 40, 75)
GOLD = (250, 205, 21)
PAPER = (247, 241, 222)
INK = (18, 24, 40)


def main():
    entry = Image.open("entry.png").convert("RGB")
    ad = Image.new("RGB", (1024, 768), PAPER)
    d = ImageDraw.Draw(ad)
    serif_b = ImageFont.truetype(FONTDIR + "DejaVuSerif-Bold.ttf", 34)
    sans_b = ImageFont.truetype(FONTDIR + "DejaVuSans-Bold.ttf", 14)
    sans = ImageFont.truetype(FONTDIR + "DejaVuSans.ttf", 13)

    d.rectangle([0, 0, 1024, 64], fill=NAVY)
    d.text((512, 10), "THE WORLD IN ONE PAGE", font=serif_b,
           fill=(245, 242, 234), anchor="ma")
    d.text((512, 44), "TUESDAY, 24 NOVEMBER 2026  ·  43 STORIES",
           font=sans_b, fill=GOLD, anchor="ma")

    small = entry.resize((640, 640), Image.LANCZOS)
    ad.paste(small, (192, 76))

    d.text((512, 724), "43 stories reported on 24 November 2026 — one image.",
           font=sans, fill=INK, anchor="ma")
    d.text((512, 744), "Referral: trfjt22d  ·  make.fun",
           font=sans_b, fill=NAVY, anchor="ma")
    ad.save("ad.png", optimize=True)
    print("saved ad.png")


if __name__ == "__main__":
    main()
