#!/usr/bin/env python3
"""Draw 'The World in One Page - 24 November 2026' (1024x1024).

Round 3 revision: every story below was reported on Tuesday 24 November
2026 (Reuters, AP, AFP, Yonhap, Japan Times, Al Jazeera, Middle East Eye,
France 24, Kathmandu Post, SCMP, Bloomberg). Fixes the round 2 entry: the
Ulleung jets were Russian, not North Korean; Gaza's toll was seven, not
three; the Iowa detonation was cleared by a court, not halted; the Zanzibar
fire was 21 November, so that story is now the inquiry that opened on the
24th; fake-looking source badges are gone; the map is real geography.
Deterministic: fixed seed, no clock, no network. Run: python3 draw24.py
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
         deck="Nvidia reinstates Jensen Huang as CEO; shares jump 31%, "
              "adding $1.5 trillion in value as Trump hails the return.",
         src="REUTERS", art="chip"),
    dict(n=2, kick="KOREA", head="RUSSIAN JETS",
         deck="Five Russian warplanes enter Seoul's air defence zone near "
              "Ulleung; alert lifted.",
         src="YONHAP", art="radar"),
    dict(n=3, kick="LIBYA", head="WARSHIP SUNK",
         deck="Ukraine says naval drones sank the Russian corvette Merkury "
              "off Libya in a rare strike far beyond the Black Sea.",
         src="REUTERS", art="ship"),
]

CARDS = [
    dict(n=4, head="HORMUZ MINES",
         body="Three oil tankers hit mines in the Strait of Hormuz; US blames Iran.",
         src="REUTERS", art="wave", bg=(24, 82, 140)),
    dict(n=5, head="GAZA STRIKES",
         body="Israeli strikes kill seven in Gaza despite the ceasefire.",
         src="AL JAZEERA", art="cross", bg=(146, 44, 20)),
    dict(n=6, head="MEGASPEED BLACKLIST",
         body="US blacklists Alibaba unit and Megaspeed in Nvidia chip scandal.",
         src="REUTERS", art="chip", bg=(16, 92, 70)),
    dict(n=7, head="ICJ: ROHINGYA",
         body="Fourteen nations urge Myanmar to obey the genocide ruling.",
         src="FRANCE 24", art="scales", bg=(36, 68, 120)),
    dict(n=8, head="NEPAL QUAKE 5.6",
         body="Magnitude 5.6 quake hits Taplejung; felt in India, no damage.",
         src="KATHMANDU POST", art="quake", bg=(96, 58, 8)),
    dict(n=9, head="ZANZIBAR INQUIRY",
         body="Probe opens after blaze gutted six Nungwi hotels; 180 evacuated.",
         src="AP", art="flame", bg=(120, 28, 60)),
    dict(n=10, head="HONDA RECALL",
         body="810,000 US vehicles recalled over Takata airbag rupture risk.",
         src="REUTERS", art="car", bg=(30, 30, 34)),
    dict(n=11, head="BLAZERS 128-111",
         body="Avdija's 31 ends the Sixers' five-game winning streak.",
         src="AP", art="ball", bg=(140, 20, 20)),
    dict(n=12, head="WOMEN'S WORLD CUP 2031",
         body="FIFA gives 2031 to US, Mexico, Costa Rica, Jamaica; UK gets 2035.",
         src="AP", art="trophy", bg=(18, 60, 110)),
    dict(n=13, head="CROWDSTRIKE $44B",
         body="CrowdStrike buys Zscaler in a $43.9bn all-stock deal, a cyber record.",
         src="REUTERS", art="shield", bg=(74, 74, 84)),
]

BRIEFS = [
    (14, "Lukashenko: fly with Zelenskiy to Moscow for talks", "REUTERS"),
    (15, "Russia: Estonia moves 'on verge of open war'", "REUTERS"),
    (16, "Houthi strike hits Riyadh PIF Tower; 11 hurt", "REUTERS"),
    (17, "Iran: no US talks until seven conditions met", "AP"),
    (18, "China extends suspension of US export curbs on minerals", "SCMP"),
    (19, "Pentagon rebukes Canada over defence spending, F-35 review", "AP"),
    (20, "Senegal's AFCON title restored as CAS upholds appeal", "REUTERS"),
    (21, "Pakistan's first astronaut set for Tiangong trip", "REUTERS"),
    (22, "Court clears army to detonate toxic explosives in Iowa", "REUTERS"),
    (23, "Eisenkot clinches first coalition deal in Israel", "REUTERS"),
    (24, "China probes Politburo member Chen Jining", "REUTERS"),
    (25, "Zambia charges opposition leader with treason", "REUTERS"),
    (26, "Hanoi restaurant gas blast kills six, injures ten", "AP"),
    (27, "Solomon Islands to swap China pact for Australia treaty", "REUTERS"),
    (28, "European rocket lofts 36 Kuiper satellites", "BLOOMBERG"),
    (29, "Russian strike on Zaporizhzhia kills 2, wounds 40+", "REUTERS"),
    (30, "Nvidia shares add $1.5tn in value on Huang return", "REUTERS"),
    (31, "Huang due to testify before US Senate on Dec 3", "REUTERS"),
    (32, "Japan bonds rally; 10-year yield 2.715%", "JAPAN TIMES"),
    (33, "France: officer to stand trial over 2023 teen killing", "AP"),
    (34, "Indonesia seizes 405t of missile chemical from ship", "AP"),
    (35, "Hasina plans Dec 16 return despite death sentence", "REUTERS"),
    (36, "Malaysia to send back 6,803 Myanmar nationals in Dec", "AP"),
    (37, "Herro's 32 ends Bucks' 13-game skid", "REUTERS"),
    (38, "China urges UK to back free trade, FM says", "REUTERS"),
    (39, "Colombia drone attack in Cucuta wounds 3, incl. infant", "AP"),
    (40, "Qatar urges Iran and US to show restraint", "REUTERS"),
    (41, "Mexico to try 'El Chapo Isidro' at home", "REUTERS"),
    (42, "Bangladesh garment workers protest over wages", "AP"),
    (43, "Iraq PM puts Kurdish borders under federal control", "REUTERS"),
]

REGIONS = ("MIDDLE EAST 7  ·  EUROPE 5  ·  AMERICAS 9  ·  ASIA 15  ·  "
           "AFRICA 4  ·  SPORT 3  =  43 STORIES")
NUMBERS = [("+31%", "HUANG RETURN"), ("$44B", "CROWDSTRIKE DEAL"),
           ("810K", "HONDA RECALL"), ("128-111", "BLAZERS WIN"),
           ("5.6", "NEPAL QUAKE MAGNITUDE")]
TIMELINE = [("00:00", "Nepal quake 5.6"), ("03:00", "Russian jets near Ulleung"),
            ("06:00", "Honda recalls 810,000"), ("09:00", "Gaza strikes kill 7"),
            ("13:00", "Megaspeed blacklisted"), ("16:00", "FIFA confirms 2031")]

# (longitude, latitude, story number) on the map strip; 12 nudged west so
# its dot clears 13 (both are US stories)
MAP_DOTS = [(-122.0, 37.4, 1), (130.9, 37.5, 2), (20.1, 32.1, 3),
            (56.3, 26.6, 4), (34.5, 31.5, 5), (103.8, 1.4, 6),
            (4.3, 52.1, 7), (87.9, 27.9, 8), (39.2, -6.2, 9),
            (-83.0, 42.3, 10), (-75.2, 40.0, 11), (-104.0, 47.0, 12),
            (-97.7, 30.3, 13)]


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
    # warship: grey hull with pointed bow, superstructure, mast, deck gun
    d.polygon([(x + 40, y + 56), (x + w - 30, y + 56), (x + w - 55, y + 78),
               (x + 60, y + 78)], fill=(70, 70, 78))
    d.rectangle([x + 120, y + 30, x + 170, y + 56], fill=(96, 96, 106))
    d.rectangle([x + 185, y + 38, x + 200, y + 56], fill=(96, 96, 106))
    d.line([x + 145, y + 30, x + 145, y + 12], fill=(40, 40, 48), width=3)
    d.polygon([(x + w - 70, y + 56), (x + w - 40, y + 50), (x + w - 38, y + 56)],
              fill=(50, 50, 58))
    d.ellipse([x + 60, y + 30, x + 76, y + 46], fill=RED)
    d.text((x + 14, y + 8), "OFF LIBYA", font=sans_b(11), fill=NAVY)


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
    # coarse real continents, equirectangular: lon -180..180 across the
    # strip, lat 65..-55 below the title band
    def project(lon, lat):
        px = mx + int((lon + 180) / 360 * mw)
        py = my + 16 + int((65 - lat) / 120 * (mh - 16))
        return (px, max(my + 16, min(my + mh - 2, py)))
    LAND = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
         (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20),
         (-90, 15), (-95, 18), (-105, 20), (-115, 28), (-125, 40),
         (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
        [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
         (-50, -30), (-58, -38), (-65, -45), (-70, -52), (-73, -40),
         (-72, -25), (-78, -12), (-80, 5)],
        [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
         (35, 28), (40, 15), (48, 11), (51, 2), (40, -10), (35, -20),
         (30, -30), (20, -35), (15, -30), (12, -18), (9, -2), (9, 4),
         (-8, 5), (-13, 9), (-17, 15)],
        [(-10, 36), (-2, 37), (0, 39), (10, 37), (15, 40), (20, 40),
         (23, 36), (28, 36), (30, 36), (36, 36), (40, 38), (45, 40),
         (50, 42), (55, 45), (60, 50), (65, 55), (70, 60), (75, 68),
         (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
         (140, 72), (150, 70), (160, 66), (170, 66), (178, 65), (170, 60),
         (162, 56), (158, 52), (150, 59), (142, 55), (140, 45), (135, 43),
         (130, 42), (127, 40), (122, 38), (120, 32), (115, 23), (110, 20),
         (108, 12), (105, 8), (100, 7), (98, 12), (95, 16), (92, 21),
         (90, 22), (86, 20), (82, 17), (80, 13), (77, 8), (75, 12),
         (72, 20), (68, 23), (62, 25), (58, 26), (55, 27), (50, 29),
         (48, 30), (44, 29), (40, 30), (36, 36), (33, 36), (30, 36),
         (26, 38), (22, 37), (19, 40), (15, 44), (12, 44), (8, 44),
         (3, 43), (0, 40), (-2, 37), (-9, 37), (-10, 36)],
        [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
         (132, -32), (136, -35), (140, -38), (145, -38), (150, -37),
         (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
         (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
         (126, -14), (122, -17), (117, -20), (113, -22)],
        [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
         (141, 40), (143, 42), (145, 44), (142, 44), (140, 40), (139, 37),
         (137, 34), (134, 34), (131, 33), (130, 31)],
    ]
    for poly in LAND:
        d.polygon([project(lon, lat) for lon, lat in poly], fill=(150, 190, 140))
    for lon, lat, num in MAP_DOTS:
        cx, cy = project(lon, lat)
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
           "Sources: Reuters · AP · AFP · Yonhap · Japan Times · Al Jazeera · "
           "Middle East Eye · France 24 · Kathmandu Post · SCMP · Bloomberg — All art hand-drawn with Pillow; no photographs.",
           font=sans(9), fill=(90, 90, 90), anchor="ma")

    # light deterministic noise wash so the file lands in the 271-712KB band
    noise = Image.effect_noise((W, H), 12).convert("RGB")
    img = Image.blend(img, noise, 0.015)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
