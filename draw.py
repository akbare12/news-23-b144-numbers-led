#!/usr/bin/env python3
"""news-23 b144 numbers-led: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, numbers-led: big number grid first, then heroes, cards,
map + ALSO, DATE CHECK. Drawn illustrations, not photographs."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
BG = (250, 246, 236)
INK = (26, 26, 26)
RED = (176, 42, 48)
GOLD = (184, 134, 11)
NAVY = (31, 78, 121)
TEAL = (14, 124, 123)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def fit(d, text, path, size, maxw, minsize=8):
    """Largest font size (<= size) that fits maxw, else shrink to minsize."""
    s = size
    while s > minsize:
        f = font(path, s)
        if d.textlength(text, font=f) <= maxw:
            return f
        s -= 1
    return font(path, minsize)

def wrap(d, text, f, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(d, x, y, text, fill):
    f = font(SANSB, 9)
    w = d.textlength(text, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return w

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 12  # left margin; content width 1000

# ---------- masthead ----------
d.text((MX, 8), "THE WORLD TODAY", font=font(SERIF, 46), fill=INK)
d.text((W - MX - d.textlength("MONDAY 23 NOVEMBER 2026", font=font(SANSB, 15)),
        24), "MONDAY 23 NOVEMBER 2026", font=font(SANSB, 15), fill=GOLD)
d.line([(MX, 56), (W - MX, 56)], fill=GOLD, width=2)

# ---------- kicker strip ----------
d.rectangle([MX, 60, W - MX, 78], fill=RED)
kick = "AI rout hits Asia   ·   UN chief urges AI rules   ·   US lead over China at record low   ·   Anthropic IPO $107.3B"
d.text((MX + 8, 64), kick, font=font(SANSB, 13), fill=(255, 255, 255))

# ---------- BIG number grid (2 rows x 5 cols) ----------
nums = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
colw = 200
for i, (val, lab) in enumerate(nums):
    cx = MX + (i % 5) * colw
    cy = 84 + (i // 5) * 44
    vf = fit(d, val, SANSB, 20, colw - 8)
    d.text((cx, cy), val, font=vf, fill=INK)
    lf = fit(d, lab, SANS, 9, colw - 8)
    d.text((cx, cy + 24), lab, font=lf, fill=(90, 90, 90))
    if i % 5:
        d.line([(cx - 6, cy + 2), (cx - 6, cy + 38)], fill=(210, 205, 195), width=1)

# ---------- region bar ----------
regions = [
    ("ASIA-PACIFIC 7", 226, NAVY),
    ("AMERICAS 8", 258, RED),
    ("MIDDLE EAST 6", 193, (123, 45, 139)),
    ("EUROPE 5", 161, TEAL),
    ("AFRICA 3", 97, (46, 125, 50)),
    ("WORLD 2", 65, GOLD),
]
rx = MX
ry = 178
for name, wdt, col in regions:
    d.rectangle([rx, ry, rx + wdt, ry + 18], fill=col)
    tf = fit(d, name, SANSB, 11, wdt - 6)
    d.text((rx + 4, ry + 3), name, font=tf, fill=(255, 255, 255))
    rx += wdt

# ---------- THE DAY IN UTC strip ----------
d.text((MX, 200), "THE DAY IN UTC", font=font(SANSB, 10), fill=NAVY)
utc = "~00:00 Kospi dives    ~05:30 Guterres opens    ~09:00 Power Index    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles"
d.text((MX + 110, 200), utc, font=font(SANS, 10), fill=(90, 90, 90))
d.text((W - MX - d.textlength("~ APPROX", font=font(SANS, 10)), 200),
       "~ APPROX", font=font(SANS, 10), fill=(120, 120, 120))

# ---------- hero scenes ----------
# art y 216..336 (120 tall), headline y 340, body y 366/380, source+chip y 396
HY = 216
colw3 = 330
gap = 5
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (head, body, src) in enumerate(heroes):
    x0 = MX + i * (colw3 + gap)
    x1 = x0 + colw3
    if i == 0:
        # Kospi skyline + falling chart
        d.rectangle([x0, HY, x1, HY + 120], fill=(16, 42, 67))
        import random
        random.seed(7)
        bx = x0 + 8
        while bx < x1 - 14:
            bw = random.randint(14, 26)
            bh = random.randint(30, 78)
            d.rectangle([bx, HY + 120 - bh, bx + bw, HY + 120], fill=(38, 84, 130))
            for wy in range(HY + 120 - bh + 6, HY + 112, 12):
                for wx in range(bx + 3, bx + bw - 3, 7):
                    if random.random() < 0.6:
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
            bx += bw + 4
        d.text((x0 + 10, HY + 6), "-3.3%", font=font(SANSB, 34), fill=(255, 255, 255))
        pts = [(x0 + 120, HY + 30), (x0 + 160, HY + 44), (x0 + 200, HY + 40),
               (x0 + 240, HY + 62), (x0 + 280, HY + 58), (x0 + 315, HY + 84)]
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.rectangle([x0, HY + 104, x1, HY + 120], fill=(0, 0, 0))
        cap = "KOSPI 4,708.54 · -161 PTS · SAMSUNG -3.1%"
        d.text((x0 + 6, HY + 107), cap, font=font(SANSB, 10), fill=(255, 214, 90))
    elif i == 1:
        # Guterres: green, big 150 + gold text + globe
        d.rectangle([x0, HY, x1, HY + 120], fill=(24, 96, 52))
        d.text((x0 + 10, HY + 4), "150", font=font(SANSB, 44), fill=(255, 214, 90))
        d.text((x0 + 10, HY + 52), "DELEGATES", font=font(SANSB, 15), fill=(255, 214, 90))
        d.text((x0 + 10, HY + 70), "BACK A RISK", font=font(SANSB, 15), fill=(255, 214, 90))
        d.text((x0 + 10, HY + 88), "FRAMEWORK", font=font(SANSB, 15), fill=(255, 214, 90))
        cx, cy, r = x0 + 268, HY + 58, 46
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 238, 214))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(24, 96, 52), width=2)
        for k in range(-2, 3):
            d.arc([cx - r, cy - r + k * 18, cx + r, cy + r + k * 18],
                  0, 360, fill=(120, 170, 120))
        d.ellipse([cx - 14, cy - r, cx + 14, cy + r], outline=(120, 170, 120), width=1)
        d.rectangle([x0, HY + 104, x1, HY + 120], fill=(0, 0, 0))
        d.text((x0 + 6, HY + 107), "BRIDGETOWN SUMMIT, BARBADOS",
               font=font(SANSB, 10), fill=(255, 214, 90))
    else:
        # Power Index bars
        d.rectangle([x0, HY, x1, HY + 120], fill=(245, 240, 228))
        d.text((x0 + 10, HY + 4), "NARROWEST SINCE 2018", font=font(SANSB, 11), fill=INK)
        d.text((x1 - 10 - d.textlength("GAP 5.3", font=font(SANSB, 11)), HY + 4),
               "GAP 5.3", font=font(SANSB, 11), fill=RED)
        bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 236),
                ("40.5", "INDIA", GOLD, 130)]
        by = HY + 26
        for val, name, col, bw in bars:
            d.text((x0 + 10, by), val, font=font(SANSB, 13), fill=INK)
            d.rectangle([x0 + 52, by + 2, x0 + 52 + bw, by + 16], fill=col)
            nf = font(SANSB, 11)
            d.text((x0 + 52 + bw - d.textlength(name, font=nf) - 6, by + 3),
                   name, font=nf, fill=(255, 255, 255))
            by += 26
        d.text((x0 + 10, by + 2), "ASIA POWER INDEX 2026 · LOWY INSTITUTE",
               font=font(SANS, 9), fill=(90, 90, 90))
        d.rectangle([x0, HY + 104, x1, HY + 120], fill=(0, 0, 0))
        d.text((x0 + 6, HY + 107), "ASIA POWER INDEX 2026 · LOWY INSTITUTE",
               font=font(SANSB, 10), fill=(255, 255, 255))
    # headline (fit 1 line if possible, else 2 lines)
    hf = fit(d, head, SANSB, 16, colw3, minsize=12)
    if d.textlength(head, font=hf) <= colw3:
        d.text((x0, HY + 126), head, font=hf, fill=INK)
        body_y = HY + 148
    else:
        lines = wrap(d, head, hf, colw3)
        d.text((x0, HY + 126), lines[0], font=hf, fill=INK)
        if len(lines) > 1:
            d.text((x0, HY + 144), lines[1], font=hf, fill=INK)
        body_y = HY + 164
    bf = font(SANS, 11)
    blines = wrap(d, body, bf, colw3)[:2]
    for j, ln in enumerate(blines):
        d.text((x0, body_y + j * 14), ln, font=bf, fill=(60, 60, 60))
    src_y = body_y + 30
    d.text((x0, src_y), src, font=font(SANS, 9), fill=(120, 120, 120))
    chip(d, x1 - 62, src_y - 1, "REPORTED", NAVY)

# ---------- MORE OF THE DAY bar ----------
d.rectangle([MX, 452, W - MX, 470], fill=(0, 0, 0))
d.text((MX + 8, 456), "MORE OF THE DAY  —  10 STORIES", font=font(SANSB, 12),
       fill=(255, 255, 255))

# ---------- 10 cards (2 rows x 5 cols) ----------
cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", False),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", False),
    ("3", "WHITE HOUSE", "IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", False),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", False),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", False),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", False),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", False),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", False),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED", "Kyiv: 3 Kh-101s crossed.", "AP", True),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", True),
]
cardw = 200
for i, (num, cat, head, body, src, claim) in enumerate(cards):
    cx = MX + (i % 5) * cardw
    cy = 476 + (i // 5) * 62
    d.text((cx, cy), num, font=font(SANSB, 11), fill=RED)
    catw = d.textlength(num, font=font(SANSB, 11)) + 6
    cf = fit(d, cat, SANSB, 10, cardw - catw - 8)
    d.text((cx + catw, cy + 1), cat, font=cf, fill=RED)
    hf = fit(d, head, SANSB, 12, cardw - 8, minsize=10)
    d.text((cx, cy + 16), head, font=hf, fill=INK)
    d.text((cx, cy + 32), body, font=font(SANS, 10), fill=(60, 60, 60))
    d.text((cx, cy + 46), src, font=font(SANS, 9), fill=(120, 120, 120))
    chip(d, cx + cardw - 66, cy + 45, "CLAIM" if claim else "REPORTED",
         RED if claim else NAVY)

# ---------- WHERE IT HAPPENED bar ----------
d.rectangle([MX, 604, W - MX, 622], fill=(0, 0, 0))
d.text((MX + 8, 608), "WHERE IT HAPPENED", font=font(SANSB, 12), fill=(255, 255, 255))

# ---------- map + ALSO ----------
mapx, mapy, mapw, maph = MX, 628, 400, 190
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(250, 246, 236))
# Americas blob (left)
d.polygon([(mapx + 20, mapy + 20), (mapx + 110, mapy + 8), (mapx + 150, mapy + 40),
           (mapx + 130, mapy + 90), (mapx + 90, mapy + 130), (mapx + 60, mapy + 150),
           (mapx + 40, mapy + 110), (mapx + 15, mapy + 70)], fill=(198, 226, 190))
# Eurasia blob (right)
d.polygon([(mapx + 180, mapy + 15), (mapx + 300, mapy + 8), (mapx + 390, mapy + 30),
           (mapx + 380, mapy + 90), (mapx + 330, mapy + 120), (mapx + 260, mapy + 110),
           (mapx + 200, mapy + 90), (mapx + 170, mapy + 50)], fill=(198, 226, 190))
pins = [
    (1, 96, 96), (2, 66, 132), (3, 330, 60), (4, 96, 44), (5, 108, 66),
    (6, 262, 44), (7, 236, 84), (8, 246, 62), (9, 268, 66), (10, 226, 62),
    (11, 316, 84), (12, 300, 100), (13, 262, 100),
]
pf = font(SANSB, 9)
for n, px, py in pins:
    d.ellipse([mapx + px - 8, mapy + py - 8, mapx + px + 8, mapy + py + 8],
              fill=RED, outline=(255, 255, 255), width=1)
    tw = d.textlength(str(n), font=pf)
    d.text((mapx + px - tw / 2, mapy + py - 6), str(n), font=pf, fill=(255, 255, 255))
d.text((mapx, mapy + maph + 4),
       "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5 New York · 6 Kyiv · 7 Paris",
       font=font(SANS, 9), fill=(90, 90, 90))
d.text((mapx, mapy + maph + 16),
       "8 London · 9 Warsaw · 10 Manchester · 11 Beirut · 12 Gaza · 13 Khartoum",
       font=font(SANS, 9), fill=(90, 90, 90))

also = [
    ("14. Paris: 100+ back 2% billionaire tax", False),
    ("15. Manchester: 12,000 cleared", False),
    ("16. Zelenskyy: 165 missiles in a week", False),
    ("17. COP31: the day after Antalya pact rejected", False),
    ("18. Israel unity talks resume", False),
    ("19. Gaza: two killed in Israeli strike", False),
    ("20. West Bank settler attacks", False),
    ("21. Iran war: no deal in sight", False),
    ("22. Lebanon seizes 264 kg explosives", False),
    ("23. Bahrain: strike hits plant, 2 hurt", False),
    ("24. Benghazi: UN demands probe", True),
    ("25. Sudan: defences down drones", True),
    ("26. DRC: fighting traps Ebola teams", False),
    ("27. Bangladesh: Hasina jailed if returns", False),
    ("28. Seoul minister quits over AI exam row", False),
    ("29. SK Telecom -7.3% as hype cools", False),
    ("30. China eases margin rules", False),
    ("31. Seoul readies 10T-won fund", False),
]
ax = 430
d.text((ax, 628), "ALSO ON MONDAY", font=font(SANSB, 12), fill=INK)
af = font(SANS, 10)
for j, (txt, claim) in enumerate(also):
    ay = 644 + j * 11
    d.text((ax, ay), txt, font=af, fill=INK)
    if claim:
        cw = d.textlength(txt, font=af)
        d.text((ax + cw + 4, ay), "[CLAIM]", font=font(SANSB, 10), fill=RED)

# ---------- DATE CHECK red box ----------
bx0, by0, bx1, by1 = MX, 856, W - MX, 946
d.rectangle([bx0, by0, bx1, by1], outline=RED, width=2)
d.text((bx0 + 8, by0 + 6), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  ·  STORIES DATED 23 NOV ONLY",
       font=font(SANSB, 12), fill=RED)
d.text((bx0 + 8, by0 + 28),
       "LEFT OUT — NOT 23 NOV:  Dems reach 258 (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
       font=font(SANS, 11), fill=INK)
d.text((bx0 + 8, by0 + 44),
       "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar ruling (19 Nov)",
       font=font(SANS, 11), fill=INK)
d.text((bx0 + 8, by0 + 66),
       "NOT YET —  Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
       font=font(SANS, 11), fill=INK)

# ---------- footer ----------
d.text((MX, 954),
       "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · ESPN · Lowy Institute (Asia Power Index 2026).",
       font=font(SANS, 9), fill=(90, 90, 90))
d.text((MX, 968),
       "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, independently unconfirmed · ONGOING = still developing.",
       font=font(SANS, 9), fill=(90, 90, 90))
d.text((MX, 982),
       "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font(SANS, 9), fill=(90, 90, 90))
d.line([(MX, 998), (W - MX, 998)], fill=GOLD, width=2)
d.text(((W - d.textlength("THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions",
       font=font(SANSB, 11))) / 2, 1004),
       "THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions",
       font=font(SANSB, 11), fill=GOLD)

img.save("entry.png")
print("saved entry.png", img.size)
