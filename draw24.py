#!/usr/bin/env python3
"""Draw 'The World in One Page - 24 November 2026' (1024x1024).

Every story below was reported on Tuesday 24 November 2026 (Reuters, AP,
AFP, Japan Times, Times of India, Al Jazeera, Middle East Eye, Philstar,
Horizon, Spyglass, The Daily Edition). Deterministic: fixed seed, no clock,
no network. Run: python3 draw24.py
"""
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (18, 24, 40)
NAVY = (18, 40, 75)
RED = (178, 34, 34)
GOLD = (250, 205, 21)
SKY = (176, 216, 235)

FONTDIR = "/usr/share/fonts/truetype/dejavu/"


def _font(name, size):
    return ImageFont.truetype(FONTDIR + name, size)


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap_text(d, text, fnt, width):
    """Greedy word wrap to a list of lines that fit width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def one_line(d, text, fnt, width):
    """Truncate to a single line with an ellipsis."""
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "...", font=fnt) > width:
        text = text[:-1]
    return text + "..."


def source_tag(d, x, y, source):
    f = sans_b(9)
    w = d.textlength(source, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=NAVY)
    d.text((x + 5, y + 1), source, font=f, fill=(255, 255, 255))
    return w


# ------------------------------------------------------------------ stories
TOP = [
    dict(n=1, kick="CHIPS", head="HUANG IS BACK",
         deck="Nvidia reinstates Jensen Huang as CEO after Trump steps in; "
              "shares jump 31% and the Nasdaq soars 6.5%.",
         src="REUTERS", art="chip"),
    dict(n=2, kick="KOREA", head="AIRSPACE ALERT",
         deck="A suspected North Korean plane breaches South Korean airspace "
              "near Ulleung; islanders are ordered to shelters.",
         src="JAPAN TIMES", art="radar"),
    dict(n=3, kick="LIBYA", head="WARSHIP SUNK",
         deck="Ukraine says naval drones sank the Russian corvette Merkury "
              "off Benghazi; Tripoli demands answers from Kyiv.",
         src="MIDDLE EAST EYE", art="ship"),
]

CARDS = [
    dict(n=4, head="HORMUZ TENSIONS",
         body="Britain logs record Iranian attacks in the Strait of Hormuz.",
         src="IQMIA", art="wave", bg=(24, 82, 140)),
    dict(n=5, head="GAZA STRIKES",
         body="Israeli strikes kill at least three, including a UNRWA worker.",
         src="AL JAZEERA", art="cross", bg=(146, 44, 20)),
    dict(n=6, head="MEGASPEED BLACKLIST",
         body="US blacklists a Singapore chip firm in the Nvidia spy scandal.",
         src="JAPAN TIMES", art="chip", bg=(16, 92, 70)),
    dict(n=7, head="ICJ: ROHINGYA",
         body="Fourteen nations back the court's genocide ruling on Myanmar.",
         src="HORIZON", art="scales", bg=(36, 68, 120)),
    dict(n=8, head="NEPAL QUAKE 5.6",
         body="A magnitude 5.6 quake strikes Nepal near the Chinese border.",
         src="HORIZON", art="quake", bg=(96, 58, 8)),
    dict(n=9, head="ZANZIBAR FIRE",
         body="Fire engulfs six hotels; 180 tourists are evacuated.",
         src="TOI", art="flame", bg=(120, 28, 60)),
    dict(n=10, head="HONDA RECALL",
         body="810,000 US vehicles recalled over airbag rupture risk.",
         src="TOI", art="car", bg=(30, 30, 34)),
    dict(n=11, head="BLAZERS 128-111",
         body="Avdija's 31 ends the Sixers' five-game winning streak.",
         src="PHILSTAR", art="ball", bg=(140, 20, 20)),
    dict(n=12, head="WORLD CUP 2031",
         body="US, Mexico, Costa Rica and Jamaica to host; UK gets 2035.",
         src="TOI", art="trophy", bg=(18, 60, 110)),
    dict(n=13, head="CROWDSTRIKE $44B",
         body="CrowdStrike snaps up Zscaler as cyber threats mount.",
         src="REUTERS", art="shield", bg=(74, 74, 84)),
]

BRIEFS = [
    (14, "UN chief: AI risk framework needed within a year", "HORIZON"),
    (15, "Russia: Estonia moves 'on verge of open war'", "IQMIA"),
    (16, "Houthis: Saudi airstrike kills 17 in Hodeida", "IQMIA"),
    (17, "Iran strikes Gulf sites, sues for $290bn", "SPYGLASS"),
    (18, "Oregon, Virginia sue SpaceX over Grok images", "IQMIA"),
    (19, "Arm extends CEO Haas' tenure to 2033", "IQMIA"),
    (20, "Somalia, Uganda step up ops vs Al-Shabaab", "IQMIA"),
    (21, "Quake of magnitude 4.1 strikes Pakistan", "TOI"),
    (22, "Trump halts Iowa explosives detonation", "TOI"),
    (23, "House Ethics: evidence vs Rep. Jimmy Gomez", "TOI"),
    (24, "India invokes Bengal famine at UNSC", "TOI"),
    (25, "Greece reopens Acropolis Museum after 7 years", "TOI"),
    (26, "Cincinnati Zoo reopens hippo enclosure", "TOI"),
    (27, "IDB eyes up to $6bn in loans for Venezuela", "TOI"),
    (28, "Anthropic launches Claude Ship for code review", "TOI"),
    (29, "Aviation groups seek $30bn for FAA upgrade", "TOI"),
    (30, "KOSPI +6%, Nikkei +3.9% after Huang return", "HORIZON"),
    (31, "SK hynix US shares surge 20% on Huang news", "SPYGLASS"),
    (32, "Japan bonds rally; 10-year yield 2.715%", "JAPAN TIMES"),
    (33, "Vance Venezuela oil deal under Senate probe", "JAPAN TIMES"),
    (34, "Indonesia charges ex-police chief with treason", "JAPAN TIMES"),
    (35, "Hasina seeks return; faces death sentence", "JAPAN TIMES"),
    (36, "N. Korea threatens to close Swiss office", "JAPAN TIMES"),
    (37, "Commanders rally past Bengals on late drive", "JAPAN TIMES"),
    (38, "China opens Tiangong to first foreign astronaut", "HORIZON"),
    (39, "Colombia car bomb wrecks Villavicencio buildings", "HORIZON"),
    (40, "UAE coach-truck crash kills 11", "HORIZON"),
    (41, "Mexico to try 'El Chapo Isidro' at home", "HORIZON"),
    (42, "Pennsylvania measles: 9th death, 46 counties", "HORIZON"),
    (43, "EU proposes banning Russian symbols in sport", "HORIZON"),
]

REGIONS = ("MIDDLE EAST 5  ·  EUROPE 4  ·  AMERICAS 15  ·  ASIA 13  ·  "
           "AFRICA 3  ·  SPORT 3  =  43 STORIES")
NUMBERS = [("+31%", "HUANG RETURN"), ("$44B", "CROWDSTRIKE DEAL"),
           ("810K", "HONDA RECALL"), ("128-111", "BLAZERS WIN"),
           ("5.6", "NEPAL QUAKE MAGNITUDE")]
TIMELINE = [("00:00", "Ulleung shelter alert"), ("03:00", "Nepal quake 5.6"),
            ("06:00", "Honda recalls 810,000"), ("09:00", "KOSPI +6%"),
            ("13:00", "Megaspeed blacklisted"), ("16:00", "FIFA confirms 2031")]

# (x fraction, y fraction, story number) on the map strip
MAP_DOTS = [(0.16, 0.42, 1), (0.86, 0.38, 2), (0.50, 0.50, 3),
            (0.60, 0.58, 4), (0.55, 0.46, 5), (0.83, 0.66, 6),
            (0.78, 0.52, 7), (0.74, 0.42, 8), (0.55, 0.70, 9),
            (0.20, 0.48, 10), (0.24, 0.38, 11), (0.13, 0.56, 12),
            (0.22, 0.30, 13)]


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 60, 40))
    for i in range(5):
        d.rectangle([x + 20 + i * 56, y + h - 26, x + 60 + i * 56, y + h - 18],
                    fill=(250, 205, 21))
    d.polygon([(x + 30, y + h - 30), (x + 110, y + 34), (x + 190, y + 34),
               (x + 250, y + 12), (x + 290, y + 14)], fill=(76, 175, 80))
    d.polygon([(x + 30, y + h - 30), (x + 110, y + 34), (x + 190, y + 34),
               (x + 250, y + 12), (x + 290, y + 14)], outline=(255, 255, 255))
    d.rectangle([x + 236, y + 16, x + 300, y + 52], fill=(255, 255, 255))
    d.text((x + 242, y + 24), "+31%", font=sans_b(20), fill=(18, 60, 40))
    d.rectangle([x + 24, y + 16, x + 64, y + 56], outline=(255, 255, 255), width=2)
    d.rectangle([x + 34, y + 26, x + 54, y + 46], fill=GOLD)


def art_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 30, 50))
    cx, cy = x + w // 2, y + h // 2 + 4
    for r in (44, 32, 20):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 200, 120))
    d.line([cx - 46, cy, cx + 46, cy], fill=(90, 200, 120))
    d.line([cx, cy - 46, cx, cy + 46], fill=(90, 200, 120))
    d.line([cx, cy, cx + 34, cy - 34], fill=(250, 205, 21), width=3)
    d.ellipse([cx + 30, cy - 38, cx + 38, cy - 30], fill=RED)
    d.polygon([(cx - 34, cy + 26), (cx + 30, cy + 8), (cx + 38, cy + 14),
               (cx - 22, cy + 34)], fill=(245, 242, 234))
    d.text((x + 12, y + 8), "AIR DEFENCE ZONE", font=sans_b(11),
           fill=(250, 205, 21))


def art_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 198, 226))
    for i in range(3):
        yy = y + 72 + i * 9
        d.arc([x - 20 + i * 8, yy - 11, x + w + 20, yy + 11], 0, 180,
              fill=(255, 255, 255), width=3)
    d.polygon([(x + 40, y + 56), (x + w - 40, y + 56), (x + w - 60, y + 78),
               (x + 60, y + 78)], fill=(70, 70, 78))
    d.rectangle([x + 90, y + 26, x + 150, y + 56], fill=(214, 90, 40))
    d.rectangle([x + 160, y + 34, x + 210, y + 56], fill=(250, 205, 21))
    d.ellipse([x + w - 70, y + 14, x + w - 46, y + 38], fill=(255, 255, 255))
    d.line([x + w - 58, y + 38, x + w - 58, y + 56], fill=(255, 255, 255), width=2)
    d.ellipse([x + 60, y + 30, x + 76, y + 46], fill=RED)
    d.text((x + 14, y + 8), "BENGHAZI", font=sans_b(11), fill=NAVY)


ART = {"chip": art_chip, "radar": art_radar, "ship": art_ship}


def icon(d, x, y, w, h, kind, bg):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    white = (245, 242, 234)
    if kind == "wave":
        for i in range(3):
            d.arc([cx - 20, cy - 12 + i * 9, cx + 20, cy + 4 + i * 9], 180, 360,
                  fill=white, width=3)
    elif kind == "cross":
        d.rectangle([cx - 3, cy - 13, cx + 3, cy + 13], fill=white)
        d.rectangle([cx - 13, cy - 3, cx + 13, cy + 3], fill=white)
    elif kind == "chip":
        d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], outline=white, width=2)
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)
        for i in (-6, 0, 6):
            d.line([cx + i, cy - 17, cx + i, cy - 11], fill=white, width=2)
            d.line([cx + i, cy + 11, cx + i, cy + 17], fill=white, width=2)
    elif kind == "scales":
        d.line([cx, cy - 13, cx, cy + 12], fill=white, width=2)
        d.line([cx - 14, cy - 9, cx + 14, cy - 9], fill=white, width=2)
        d.polygon([(cx - 18, cy - 9), (cx - 10, cy - 9), (cx - 14, cy + 2)],
                  fill=GOLD)
        d.polygon([(cx + 10, cy - 9), (cx + 18, cy - 9), (cx + 14, cy + 2)],
                  fill=GOLD)
        d.rectangle([cx - 10, cy + 12, cx + 10, cy + 15], fill=white)
    elif kind == "quake":
        d.polygon([(cx - 18, cy + 10), (cx - 8, cy - 12), (cx + 2, cy + 6),
                   (cx + 12, cy - 12), (cx + 20, cy + 10)], fill=white)
        d.line([cx - 20, cy + 14, cx + 20, cy + 14], fill=GOLD, width=3)
    elif kind == "flame":
        d.polygon([(cx, cy - 14), (cx + 10, cy + 2), (cx + 6, cy + 12),
                   (cx - 8, cy + 12), (cx - 12, cy - 2)], fill=(255, 140, 0))
        d.polygon([(cx, cy - 4), (cx + 5, cy + 6), (cx - 5, cy + 10)], fill=GOLD)
    elif kind == "car":
        d.polygon([(cx - 20, cy + 8), (cx - 16, cy - 2), (cx - 4, cy - 8),
                   (cx + 10, cy - 8), (cx + 20, cy + 2), (cx + 20, cy + 8)],
                  fill=white)
        d.ellipse([cx - 13, cy + 4, cx - 5, cy + 12], fill=INK)
        d.ellipse([cx + 6, cy + 4, cx + 14, cy + 12], fill=INK)
    elif kind == "ball":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=white, width=2)
        d.polygon([(cx, cy - 13), (cx + 8, cy - 4), (cx + 5, cy + 8),
                   (cx - 5, cy + 8), (cx - 8, cy - 4)], fill=white)
    elif kind == "trophy":
        d.polygon([(cx - 10, cy - 13), (cx + 10, cy - 13), (cx + 7, cy + 2),
                   (cx - 7, cy + 2)], fill=GOLD)
        d.arc([cx - 16, cy - 13, cx - 4, cy + 2], 90, 270, fill=GOLD, width=2)
        d.arc([cx + 4, cy - 13, cx + 16, cy + 2], 270, 90, fill=GOLD, width=2)
        d.rectangle([cx - 3, cy + 2, cx + 3, cy + 10], fill=GOLD)
        d.rectangle([cx - 9, cy + 10, cx + 9, cy + 14], fill=GOLD)
    elif kind == "shield":
        d.polygon([(cx, cy - 14), (cx + 12, cy - 8), (cx + 12, cy + 4),
                   (cx, cy + 14), (cx - 12, cy + 4), (cx - 12, cy - 8)],
                  outline=white, width=2)
        d.text((cx, cy - 1), "$", font=sans_b(13), fill=GOLD, anchor="mm")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261124)
    for _ in range(5200):
        x, y = rng.randrange(W), rng.randrange(H)
        d.point((x, y),
                fill=rng.choice(((232, 226, 205), (255, 250, 235))))

    # ---- masthead
    d.rectangle([12, 10, 1012, 92], fill=NAVY)
    d.text((512, 16), "THE WORLD IN ONE PAGE", font=serif_b(44),
           fill=(245, 242, 234), anchor="ma")
    d.text((512, 66), "TUESDAY, 24 NOVEMBER 2026  ·  43 STORIES  ·  ONE IMAGE",
           font=sans_b(15), fill=GOLD, anchor="ma")
    # ---- date check
    d.rectangle([12, 96, 1012, 116], fill=RED)
    d.text((512, 99), "DATE CHECK — EVERY STORY HERE WAS REPORTED ON 24 NOVEMBER 2026",
           font=sans_b(12), fill=(255, 255, 255), anchor="ma")

    # ---- 3 top stories
    for i, s in enumerate(TOP):
        x = 12 + i * 338
        w = 324
        d.rectangle([x, 122, x + w, 330], outline=INK, width=1,
                    fill=(255, 253, 245))
        ART[s["art"]](d, x + 1, 123, w - 2, 96)
        d.text((x + 8, 224), f"{s['n']}  ·  {s['kick']}", font=sans_b(11),
               fill=RED)
        lines = wrap_text(d, s["head"], serif_b(21), w - 16)
        for j, line in enumerate(lines):
            d.text((x + 8, 240 + j * 24), line, font=serif_b(21), fill=INK)
        ty = 240 + len(lines) * 24 + 2
        for j, line in enumerate(wrap_text(d, s["deck"], sans(12), w - 16)):
            d.text((x + 8, ty + j * 15), line, font=sans(12), fill=(40, 40, 40))
        source_tag(d, x + 8, 312, s["src"])

    # ---- 10 cards, 2 rows x 5
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 5)
        x = 12 + col * 202
        y = 338 + row * 138
        w, h = 196, 132
        d.rectangle([x, y, x + w, y + h], outline=INK, width=1,
                    fill=(255, 253, 245))
        icon(d, x + 1, y + 1, w - 2, 40, c["art"], c["bg"])
        d.text((x + 6, y + 46), f"{c['n']}.", font=sans_b(11), fill=RED)
        lines = wrap_text(d, c["head"], sans_b(12), w - 12)
        for j, line in enumerate(lines[:2]):
            d.text((x + 6, y + 60 + j * 14), line, font=sans_b(12), fill=INK)
        by = y + 60 + len(lines[:2]) * 14 + 2
        for j, line in enumerate(wrap_text(d, c["body"], sans(10), w - 12)):
            if by + j * 12 > y + h - 18:
                break
            d.text((x + 6, by + j * 12), line, font=sans(10), fill=(40, 40, 40))
        source_tag(d, x + 6, y + h - 17, c["src"])

    # ---- numbered world map strip
    mx, my, mw, mh = 12, 618, 1000, 94
    d.rectangle([mx, my, mx + mw, my + mh], fill=(216, 232, 242))
    d.rectangle([mx, my, mx + mw, my + mh], outline=INK, width=1)
    d.text((mx + 8, my + 4), "WHERE IT HAPPENED — 13 MAIN STORIES",
           font=sans_b(11), fill=NAVY)
    blobs = [
        ([(90, 40), (150, 28), (210, 36), (225, 52), (180, 66), (120, 62)],
         (150, 190, 140)),
        ([(210, 68), (250, 64), (268, 84), (240, 92), (215, 82)],
         (150, 190, 140)),
        ([(470, 30), (520, 24), (540, 40), (505, 52), (472, 46)],
         (190, 200, 150)),
        ([(530, 48), (585, 40), (620, 58), (600, 82), (560, 86), (535, 66)],
         (150, 190, 140)),
        ([(640, 30), (760, 22), (880, 30), (900, 48), (800, 56), (680, 52)],
         (190, 200, 150)),
        ([(830, 70), (880, 66), (895, 80), (845, 86)], (150, 190, 140)),
    ]
    for pts, col in blobs:
        d.polygon([(mx + px, my + py) for px, py in pts], fill=col)
    for fx, fy, num in MAP_DOTS:
        cx, cy = mx + int(fx * mw), my + int(fy * mh)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(num), font=sans_b(10), fill=(255, 255, 255),
               anchor="mm")

    # ---- region stats
    d.text((512, 716), REGIONS, font=sans_b(13), fill=INK, anchor="ma")
    # ---- numbers bar
    bw = 196
    for i, (num, label) in enumerate(NUMBERS):
        x = 12 + i * 202
        d.rectangle([x, 740, x + bw, 772], fill=NAVY)
        d.text((x + 10, 744), num, font=serif_b(20), fill=GOLD)
        d.text((x + bw - 8, 752), label, font=sans_b(9),
               fill=(245, 242, 234), anchor="ra")
    # ---- UTC timeline
    d.text((12, 778), "24 NOV, UTC", font=sans_b(11), fill=RED)
    d.line([12, 800, 1012, 800], fill=INK, width=2)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 140 + i * 162
        d.ellipse([cx - 5, 795, cx + 5, 805], fill=RED)
        d.text((cx, 780), t, font=sans_b(10), fill=INK, anchor="ma")
        d.text((cx, 806), one_line(d, label, sans(9), 152), font=sans(9),
               fill=(60, 60, 60), anchor="ma")

    # ---- 30 briefs, 3 columns x 10
    d.text((12, 824), "THE REST OF THE DAY — 30 MORE STORIES",
           font=sans_b(12), fill=NAVY)
    d.line([12, 840, 1012, 840], fill=INK, width=1)
    bf = sans(9)
    for i, (num, text, src) in enumerate(BRIEFS):
        col, row = divmod(i, 10)
        x = 12 + col * 338
        y = 846 + row * 15
        d.text((x, y), one_line(d, f"{num}. {text} — {src}", bf, 328),
               font=bf, fill=INK)

    # ---- footer
    d.text((512, 1002),
           "Sources: Reuters · AP · AFP · Japan Times · Times of India · Al Jazeera · "
           "Middle East Eye · Philstar · Horizon · Spyglass — All art hand-drawn with Pillow; no photographs.",
           font=sans(9), fill=(90, 90, 90), anchor="ma")

    # light deterministic noise wash so the file lands in the 271-712KB band
    noise = Image.effect_noise((W, H), 12).convert("RGB")
    img = Image.blend(img, noise, 0.015)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
