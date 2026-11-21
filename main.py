#!/usr/bin/env python3
"""THE UNDERLEAF — poster wisata vintage untuk tempat fiktif.

Program menggambar poster 1024x1024 dan menulis /output/entry.png.
Satu-satunya teks di gambar: nama tempat "THE UNDERLEAF".
Fonta dibundel di ./assets (Playfair Display 900 untuk nama).
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = "/output/entry.png"

# --- palet ---
CREAM = (245, 233, 200)
GOLD = (212, 175, 105)
GOLD_BRIGHT = (255, 214, 106)
DEEP = (10, 38, 30)          # hijau hutan gelap
MOSS = (29, 74, 51)
BARK = (43, 32, 22)
BARK_LT = (74, 56, 36)
GLOW = (255, 196, 90)        # cahaya bioluminesen hangat
GLOW_GREEN = (159, 232, 112)
MIST = (190, 220, 190)

random.seed(20261121)


def vgrad(size, top, bottom):
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (size[0], y)], fill=c)
    return img


def glow_layer(size, cx, cy, radius, color, peak=200):
    """Radial glow disc, RGBA."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(peak * (1 - i / steps) ** 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=color + (a,))
    return layer


def main():
    img = vgrad((W, H), (8, 30, 24), (24, 62, 42))
    d = ImageDraw.Draw(img, "RGBA")

    # --- kanopi: gugusan daun gelap di sudut atas, di belakang nama ---
    for cx, cy, rx, ry, col in [
        (60, 60, 190, 120, (16, 58, 38)), (980, 50, 200, 120, (16, 58, 38)),
        (180, 20, 150, 80, (22, 70, 44)), (860, 18, 150, 80, (22, 70, 44)),
        (40, 200, 120, 90, (14, 50, 34)), (990, 210, 120, 90, (14, 50, 34)),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col + (255,))
    # urat daun tipis
    for _ in range(26):
        x = random.randint(0, 220) if random.random() < 0.5 else random.randint(804, 1024)
        y = random.randint(0, 260)
        d.line([(x, y), (x + random.randint(-40, 40), y + random.randint(10, 50))],
               fill=(46, 110, 70, 160), width=2)

    # --- sinar cahaya dari kanopi (god rays) ---
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    for x0, wdt, alpha in [(300, 60, 26), (470, 34, 20), (640, 70, 24), (760, 30, 16)]:
        rd.polygon([(x0, 0), (x0 + wdt, 0), (x0 + wdt + 90, H), (x0 + 90, H)],
                   fill=(255, 220, 130, alpha))
    rays = rays.filter(ImageFilter.GaussianBlur(18))
    img.paste(rays, (0, 0), rays)
    d = ImageDraw.Draw(img, "RGBA")

    # --- batang pohon raksasa: dua dinding batang kiri & kanan ---
    # dinding kiri
    d.polygon([(70, 250), (330, 250), (300, 980), (40, 980)], fill=BARK + (255,))
    # dinding kanan
    d.polygon([(694, 250), (954, 250), (984, 980), (724, 980)], fill=BARK + (255,))
    # tepi dalam batang (garis cahaya tepi)
    d.line([(330, 250), (300, 980)], fill=(120, 92, 58, 255), width=6)
    d.line([(694, 250), (724, 980)], fill=(120, 92, 58, 255), width=6)
    # tekstur kulit kayu: garis vertikal bergelombang
    for x0 in range(90, 320, 22):
        pts = [(x0 + random.randint(-8, 8), y) for y in range(250, 981, 60)]
        d.line(pts, fill=(20, 14, 9, 140), width=5)
        pts2 = [(x0 + 10 + random.randint(-6, 6), y) for y in range(250, 981, 70)]
        d.line(pts2, fill=BARK_LT + (120,), width=3)
    for x0 in range(710, 950, 22):
        pts = [(x0 + random.randint(-8, 8), y) for y in range(250, 981, 60)]
        d.line(pts, fill=(20, 14, 9, 140), width=5)
        pts2 = [(x0 + 10 + random.randint(-6, 6), y) for y in range(250, 981, 70)]
        d.line(pts2, fill=BARK_LT + (120,), width=3)
    # lumut di batang
    for _ in range(40):
        x = random.choice([random.randint(80, 320), random.randint(710, 950)])
        y = random.randint(260, 950)
        r = random.randint(6, 22)
        d.ellipse([x - r, y - r // 2, x + r, y + r // 2], fill=(58, 110, 62, 110))

    # --- lubang batang: kota bercahaya di dalam ---
    # bukaan melengkung (lengkung atas)
    opening = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(opening)
    od.pieslice([300, 190, 724, 620], 180, 360, fill=(0, 0, 0, 255))
    od.rectangle([300, 405, 724, 980], fill=(0, 0, 0, 255))
    # isi bukaan dengan gradasi cahaya hangat
    inner = vgrad((424, 790), (255, 190, 80), (120, 70, 30))
    inner = inner.convert("RGBA")
    inner.putalpha(opening.split()[3].crop((300, 190, 724, 980)))
    img.paste(inner, (300, 190), inner)
    d = ImageDraw.Draw(img, "RGBA")

    # glow kuat di tengah lubang
    img.paste(glow_layer((W, H), 512, 620, 330, (255, 190, 90), 120), (0, 0),
              glow_layer((W, H), 512, 620, 330, (255, 190, 90), 120))
    d = ImageDraw.Draw(img, "RGBA")

    # cahaya hangat di puncak lubang + kanopi gantung di dalam lengkung
    # (mengisi area emas polos di puncak; semua titik dihitung di dalam
    #  batas lengkung: puncak lengkung di y=190 tengah, ~237 di x=380)
    img.paste(glow_layer((W, H), 512, 300, 190, (255, 200, 110), 90), (0, 0),
              glow_layer((W, H), 512, 300, 190, (255, 200, 110), 90))
    d = ImageDraw.Draw(img, "RGBA")
    for cx, top_y, r in [(380, 262, 38), (470, 240, 52), (560, 238, 54), (650, 264, 36)]:
        d.ellipse([cx - r, top_y - r // 2, cx + r, top_y + r // 2], fill=(24, 66, 40, 255))
        d.ellipse([cx - r // 2, top_y - r // 3, cx + r // 2, top_y + r // 3],
                  fill=(38, 96, 56, 255))
    # sulur gantung dengan lentera buah bercahaya
    for x, ln in [(410, 46), (470, 66), (540, 58), (610, 70), (660, 44)]:
        y0 = 272
        d.line([(x, y0), (x, y0 + ln)], fill=(30, 60, 36, 255), width=3)
        d.ellipse([x - 6, y0 + ln - 6, x + 6, y0 + ln + 6], fill=GOLD_BRIGHT + (255,))
    # jalan layang tinggi di puncak kota (bukan jendela melayang)
    d.rectangle([400, 352, 624, 364], fill=(30, 20, 12, 255))
    d.line([(400, 364), (624, 364)], fill=(212, 175, 105, 200), width=2)
    for wx in (412, 462, 512, 562, 600):
        d.rectangle([wx, 330, wx + 13, 348], fill=(255, 214, 106, 255))

    # kota di dalam lubang: platform + jendela bioluminesen
    win_colors = [(255, 214, 106), (255, 190, 80), (159, 232, 112), (255, 230, 160)]
    platforms = [
        (330, 470, 694, 486), (350, 560, 674, 576), (330, 650, 694, 666),
        (360, 740, 664, 756), (340, 830, 684, 846),
    ]
    for (x0, y0, x1, y1) in platforms:
        d.rectangle([x0, y0, x1, y1], fill=(30, 20, 12, 255))
        d.line([(x0, y1), (x1, y1)], fill=(212, 175, 105, 200), width=2)
        # jendela di atas platform
        n = (x1 - x0) // 34
        for i in range(n):
            wx = x0 + 10 + i * 34 + random.randint(-4, 4)
            wy = y0 - 26 - random.randint(0, 14)
            ww, wh = random.randint(10, 16), random.randint(14, 24)
            col = random.choice(win_colors)
            d.rectangle([wx, wy, wx + ww, wy + wh], fill=col + (255,))
            # siluet balkon kecil di beberapa jendela
            if random.random() < 0.35:
                d.line([(wx - 2, wy + wh + 4), (wx + ww + 2, wy + wh + 4)],
                       fill=(20, 14, 9, 255), width=3)
    # menara kota: badan persegi + atap kubah + jendela bercahaya
    # (bukan segitiga — segitiga sebelumnya terbaca seperti pohon pinus)
    d.rectangle([466, 392, 506, 470], fill=(34, 24, 14, 255))
    d.pieslice([466, 366, 506, 396], 180, 360, fill=(34, 24, 14, 255))
    d.ellipse([483, 358, 489, 364], fill=GOLD_BRIGHT + (255,))  # finial
    d.rectangle([478, 404, 494, 420], fill=GOLD_BRIGHT + (255,))
    d.rectangle([478, 432, 494, 448], fill=(255, 190, 80, 255))
    d.line([(466, 392), (506, 392)], fill=(212, 175, 105, 200), width=2)
    # jembatan lengkung di atas platform kedua: dek + rel + tiang + lampu.
    # Ujung dek mendarat tepat di permukaan platform (y=560).
    d.arc([430, 536, 600, 608], 200, 340, fill=(40, 28, 16, 255), width=6)
    d.arc([430, 520, 600, 592], 200, 340, fill=(212, 175, 105, 220), width=3)
    for ang in range(205, 336, 15):
        th_ = math.radians(ang)
        x = 515 + 85 * math.cos(th_)
        y_deck = 572 + 36 * math.sin(th_)
        y_rail = 556 + 36 * math.sin(th_)
        d.line([(x, y_rail), (x, y_deck)], fill=(60, 40, 20, 255), width=3)
    for ang in (215, 250, 290, 325):
        th_ = math.radians(ang)
        x = 515 + 85 * math.cos(th_)
        y = 556 + 36 * math.sin(th_)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=GOLD_BRIGHT + (255,))
    # lampu gantung kecil
    for _ in range(14):
        x = random.randint(340, 684)
        y = random.randint(430, 800)
        r = random.randint(3, 6)
        d.ellipse([x - r, y - r, x + r, y + r], fill=random.choice(win_colors) + (255,))

    # --- akar di dasar batang (akar tengah dikecilkan & diratakan agar
    # glow di dasar lubang tidak tertutup) ---
    for cx, spread, top_y in [(180, 150, 880), (512, 110, 918), (850, 150, 880)]:
        d.polygon([(cx - spread, 980), (cx - 40, top_y), (cx + 40, top_y),
                   (cx + spread, 980)], fill=(36, 26, 17, 255))
    # tanah / horizon bawah: kabut + jamur bercahaya
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mist)
    for cx, cy, rx in [(300, 940, 260), (700, 950, 280), (512, 975, 340)]:
        md.ellipse([cx - rx, cy - 26, cx + rx, cy + 26], fill=MIST + (46,))
    mist = mist.filter(ImageFilter.GaussianBlur(16))
    img.paste(mist, (0, 0), mist)
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(26):  # kunang-kunang / spora
        x = random.randint(60, 964)
        y = random.randint(860, 990)
        r = random.randint(2, 5)
        col = random.choice([(255, 214, 106), (159, 232, 112), (200, 240, 180)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (220,))
    # jamur bercahaya di akar (diperbesar + halo cahaya di balik tudung)
    for x, y, s in [(150, 930, 20), (880, 935, 22), (250, 955, 15), (790, 960, 17),
                    (340, 948, 12), (700, 950, 13)]:
        d.ellipse([x - s * 2, y - s, x + s * 2, y + s], fill=(255, 200, 90, 60))
        d.pieslice([x - s, y - s, x + s, y + s // 2], 180, 360,
                   fill=(255, 214, 106, 255))
        sw, sh = max(3, s // 5), s // 2 + 4
        d.rectangle([x - sw, y, x + sw, y + sh], fill=(240, 230, 200, 255))

    # --- NAMA TEMPAT: besar, di atas, satu-satunya teks ---
    font_path = os.path.join(BASE, "assets", "PlayfairDisplay-900.ttf")
    font = ImageFont.truetype(font_path, 118)
    name = "THE UNDERLEAF"
    # atur ukuran agar muat dengan margin
    while True:
        bb = d.textbbox((0, 0), name, font=font)
        if bb[2] - bb[0] <= 900 or font.size <= 60:
            break
        font = ImageFont.truetype(font_path, font.size - 4)
    bb = d.textbbox((0, 0), name, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    tx, ty = (W - tw) // 2 - bb[0], 78 - bb[1]
    # bayangan emas lembut + teks krem
    d.text((tx + 4, ty + 5), name, font=font, fill=(120, 90, 30, 255))
    d.text((tx, ty), name, font=font, fill=CREAM + (255,))
    # garis emas di bawah nama + berlian kecil.
    # PENTING: ty adalah garis ascender font (bukan puncak tinta); dasar
    # tinta yang sebenarnya = ty + bb[3]. Garis diletak 18px di bawahnya.
    rule_y = ty + bb[3] + 18
    d.line([(W // 2 - 300, rule_y), (W // 2 - 24, rule_y)], fill=GOLD + (255,), width=3)
    d.line([(W // 2 + 24, rule_y), (W // 2 + 300, rule_y)], fill=GOLD + (255,), width=3)
    cx = W // 2
    d.polygon([(cx, rule_y - 9), (cx + 9, rule_y), (cx, rule_y + 9), (cx - 9, rule_y)],
              fill=GOLD_BRIGHT + (255,))

    # --- bingkai poster vintage ---
    d.rectangle([18, 18, W - 19, H - 19], outline=CREAM + (255,), width=5)
    d.rectangle([34, 34, W - 35, H - 35], outline=GOLD + (255,), width=2)

    # --- grain halus (risograph): bintik jarang, entropi rendah agar PNG tetap kecil ---
    for _ in range(2600):
        x = random.randint(20, W - 20)
        y = random.randint(20, H - 20)
        v = random.choice([(255, 240, 210), (0, 0, 0)])
        d.point((x, y), fill=v + (18,))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
