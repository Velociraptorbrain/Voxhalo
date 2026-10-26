"""Builds assets/skin_bg.png (static artwork) and Source/Layout.h (control positions),
plus docs/ButterVox_UI_Preview.png (artwork with sample controls drawn on top).
Run:  python3 tools/build_skin.py
"""
import math, random, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
SS = 2
W, H = 2400, 960
GF = '/usr/share/fonts/truetype/google-fonts/'
POP_B, POP_M = GF + 'Poppins-Bold.ttf', GF + 'Poppins-Medium.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
def F(p, s): return ImageFont.truetype(p, int(s * SS))

INK = (74, 40, 18); CHOC = (104, 60, 28); CARAMEL = (150, 92, 38)
BUTTER = (255, 217, 96); BUTTER_L = (255, 238, 156); BUTTER_D = (240, 190, 60)
CREAM = (255, 247, 224); PERI = (112, 128, 224); TOMATO = (224, 84, 62)

def S(v): return int(round(v * SS))
def vgrad(w, h, c0, c1):
    t = np.linspace(0, 1, max(h, 1))[:, None, None]
    a = np.array(c0, float)[None, None, :] * (1 - t) + np.array(c1, float)[None, None, :] * t
    return Image.fromarray(np.repeat(a, max(w, 1), axis=1).astype('uint8'), 'RGB')
def rgrad(size, inner, outer, cx=0.5, cy=0.5):
    y, x = np.mgrid[0:size, 0:size] / float(size)
    dd = np.clip(np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / 0.7, 0, 1)[..., None]
    a = np.array(inner, float) * (1 - dd) + np.array(outer, float) * dd
    return Image.fromarray(a.astype('uint8'), 'RGB')

# ----- parameter ids in enum order (read from Params.h so the layout always matches) -----
params_h = open(os.path.join(ROOT, 'Source', 'Params.h')).read()
IDS = re.findall(r'\{\s*"([a-z]+)",\s*"[^"]+",\s*"', params_h)
IDX = {k: i for i, k in enumerate(IDS)}

img = None; d = None
LAY = {'ctl': [], 'rect': {}}

def rr(x0, y0, x1, y1, r, fill=None, outline=None, width=1): d.rounded_rectangle([S(x0), S(y0), S(x1), S(y1)], radius=S(r), fill=fill, outline=outline, width=max(1, S(width)))
def ln(x0, y0, x1, y1, fill, width=1): d.line([S(x0), S(y0), S(x1), S(y1)], fill=fill, width=max(1, S(width)))
def el(x0, y0, x1, y1, fill=None, outline=None, width=1): d.ellipse([S(x0), S(y0), S(x1), S(y1)], fill=fill, outline=outline, width=max(1, S(width)))
def poly(pts, fill=None, outline=None): d.polygon([(S(a), S(b)) for a, b in pts], fill=fill, outline=outline)
def txt(x, y, s, font, fill, anchor='mm', spacing=0):
    if spacing == 0: d.text((S(x), S(y)), s, font=font, fill=fill, anchor=anchor); return
    ws = [d.textlength(c, font=font) for c in s]; total = sum(ws) + S(spacing) * (len(s) - 1); cx = S(x) - total / 2
    for c, w in zip(s, ws): d.text((cx, S(y)), c, font=font, fill=fill, anchor='l' + anchor[1]); cx += w + S(spacing)
def glow(cx, cy, rx, ry, color, alpha, blur):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(layer).ellipse([S(cx - rx), S(cy - ry), S(cx + rx), S(cy + ry)], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(S(blur))); img.paste(layer, (0, 0), layer)
def paste_grad(x0, y0, x1, y1, r, c0, c1):
    g = vgrad(S(x1) - S(x0), S(y1) - S(y0), c0, c1); m = Image.new('L', g.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, g.size[0] - 1, g.size[1] - 1], radius=S(r), fill=255); img.paste(g, (S(x0), S(y0)), m)
def star(cx, cy, r, fill):
    poly([(cx, cy - r), (cx + r * 0.22, cy - r * 0.22), (cx + r, cy), (cx + r * 0.22, cy + r * 0.22), (cx, cy + r), (cx - r * 0.22, cy + r * 0.22), (cx - r, cy), (cx - r * 0.22, cy - r * 0.22)], fill=fill)
def drip(x, y, w, length, fill=BUTTER, ink=INK, o=6):
    for e, c in ((o, ink), (0, fill)):
        rr(x - w / 2 - e, y - e, x + w / 2 + e, y + length - w * 0.4 + e, w / 2 + e, fill=c)
        el(x - w * 0.78 - e, y + length - w * 1.5 - e, x + w * 0.78 + e, y + length + e, fill=c)
    el(x - w * 0.35, y + length - w * 1.25, x - w * 0.05, y + length - w * 0.9, fill=(255, 255, 255, 170))

def u(v): return round(v / 2.0, 2)   # design units -> editor units

# ---------------- controls ----------------
def value_frame(cx, y, w=90):
    rr(cx - w / 2, y, cx + w / 2, y + 38, 12, fill=CREAM, outline=INK, width=3.5)

def vslider(pid, cx, top, bot, level, label, value, label_y=318, vy=800, live=False):
    txt(cx, label_y, label, F(POP_M, 21), INK)
    for i in range(9):
        ty = bot - (bot - top) * i / 8; ll = 15 if i % 4 == 0 else 8
        ln(cx - 30 - ll, ty, cx - 30, ty, INK + (200,), 2.5); ln(cx + 30, ty, cx + 30 + ll, ty, INK + (200,), 2.5)
    value_frame(cx, vy)
    LAY['ctl'].append(dict(id=pid, knob=False, cx=u(cx), cy=0, top=u(top), bot=u(bot), r=0, vx=u(cx), vy=u(vy), vw=45, vh=19))
    if live:
        rr(cx - 12, top, cx + 12, bot, 12, fill=INK); rr(cx - 8, top + 4, cx + 8, bot - 4, 8, fill=CHOC)
        ty = bot - (bot - top) * level
        pts = [(cx - 8 + 16 * k / 12, ty + 4 * math.sin(k * 1.4)) for k in range(13)]
        poly(pts + [(cx + 8, bot - 4), (cx - 8, bot - 4)], fill=BUTTER)
        rr(cx - 36, ty - 26, cx + 36, ty + 26, 12, fill=INK); rr(cx - 32, ty - 22, cx + 32, ty + 22, 9, fill=CREAM)
        for off in (6, 13): ln(cx - 22, ty + off, cx + 22, ty + off, (222, 196, 140), 2)
        txt(cx, vy + 20, value, F(MONO, 19), INK)

def knob(pid, cx, cy, r, v, label, value, label_y, val_y, sparkle=False, live=False):
    for i in range(21):
        a = math.radians(-135 + 270 * i / 20); big = i % 5 == 0
        r0, r1 = r + 12, r + (28 if big else 20)
        ln(cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + r1 * math.sin(a), cy - r1 * math.cos(a), INK, 4 if big else 2.5)
    if sparkle:
        for (dx, dy, rs, c) in ((-r - 34, -r + 4, 14, PERI), (r + 34, -r + 20, 18, (255, 255, 255)), (r + 26, r - 16, 11, PERI), (-r - 26, r - 4, 15, (255, 255, 255)), (6, -r - 38, 12, PERI)):
            star(cx + dx, cy + dy, rs, c)
    txt(cx, label_y, label, F(POP_B, 19 if len(label) > 6 else 24), INK, 'mm', 1 if len(label) > 6 else 2)
    value_frame(cx, val_y, 100)
    LAY['ctl'].append(dict(id=pid, knob=True, cx=u(cx), cy=u(cy), top=0, bot=0, r=u(r), vx=u(cx), vy=u(val_y), vw=50, vh=19))
    if live:
        glow(cx + 6, cy + 14, r + 4, r + 2, (60, 30, 10), 150, 8)
        el(cx - r, cy - r, cx + r, cy + r, fill=INK); el(cx - r * 0.94, cy - r * 0.94, cx + r * 0.94, cy + r * 0.94, fill=CREAM)
        cap = rgrad(S(2 * r * 0.66), (255, 232, 130), (226, 150, 24), 0.38, 0.3); m = Image.new('L', cap.size, 0)
        ImageDraw.Draw(m).ellipse([0, 0, cap.size[0] - 1, cap.size[1] - 1], fill=255); img.paste(cap, (S(cx - r * 0.66), S(cy - r * 0.66)), m)
        el(cx - r * 0.66, cy - r * 0.66, cx + r * 0.66, cy + r * 0.66, outline=INK, width=5)
        a = math.radians(-135 + 270 * v)
        ln(cx, cy, cx + r * 0.6 * math.sin(a), cy - r * 0.6 * math.cos(a), INK, 8); el(cx - 8, cy - 8, cx + 8, cy + 8, fill=INK)
        txt(cx, val_y + 20, value, F(MONO, 19), INK)

def render(live):
    global img, d
    random.seed(3)
    LAY['ctl'] = []; LAY['rect'] = {}
    img = Image.new('RGB', (S(W), S(H)), CARAMEL); d = ImageDraw.Draw(img, 'RGBA')

    # --- caramel sunburst + diner floor ---
    for i in range(36):
        a0, a1 = 2 * math.pi * i / 36, 2 * math.pi * (i + 0.5) / 36
        poly([(1200, 560), (1200 + 2600 * math.cos(a0), 560 + 2600 * math.sin(a0)), (1200 + 2600 * math.cos(a1), 560 + 2600 * math.sin(a1))], fill=(176, 110, 46, 120))
    glow(W / 2, 480, 1300, 520, (255, 205, 110), 70, 160)
    for r_ in range(0, 5):
        for c_ in range(0, 41):
            if (r_ + c_) % 2 == 0: rr(c_ * 60, 900 + r_ * 20, c_ * 60 + 60, 920 + r_ * 20, 0, fill=(60, 32, 14, 130))
    vl = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(vl).rectangle([S(-200), S(-200), S(W + 200), S(H + 200)], outline=(40, 20, 8, 255), width=S(240))
    vl = vl.filter(ImageFilter.GaussianBlur(S(140))); img.paste(vl, (0, 0), vl); d = ImageDraw.Draw(img, 'RGBA')

    # --- the butter slab ---
    SX0, SX1, SY0, SY1 = 40, 2360, 150, 880
    rr(SX0 + 10, SY0 + 22, SX1 + 10, SY1 + 22, 70, fill=(40, 20, 8, 130))
    rr(SX0, SY0, SX1, SY1, 70, fill=INK)
    paste_grad(SX0 + 8, SY0 + 8, SX1 - 8, SY1 - 8, 62, BUTTER_L, BUTTER_D)
    paste_grad(SX0 + 8, SY0 + 8, SX1 - 8, SY0 + 70, 62, (255, 249, 200), BUTTER_L)
    rr(SX0 + 30, SY0 + 22, SX1 - 30, SY0 + 38, 8, fill=(255, 255, 255, 120))
    # top melt spill on the right
    for (dx, ln_, w_) in ((1850, 56, 30), (2010, 44, 24), (2290, 52, 28)): drip(dx, SY0 + 2, w_, ln_, fill=BUTTER_L)

    # --- header: logo + preset card ---
    logo = Image.open(os.path.join(ROOT, 'assets', 'ButterVox_logo.png')).convert('RGBA')
    lh = 205; lw = int(logo.width * lh / logo.height)
    logo = logo.resize((S(lw), S(lh)), Image.LANCZOS); img.paste(logo, (S(60), S(-22)), logo); d = ImageDraw.Draw(img, 'RGBA')
    txt(330, 204, 'SPREAD YOUR VOCALS THICK', F(POP_M, 19), INK, 'mm', 5)
    cx0, cx1 = 1000, 1740
    rr(cx0 + 8, 52, cx1 + 8, 148, 16, fill=(60, 30, 10, 120)); rr(cx0, 44, cx1, 140, 16, fill=INK); rr(cx0 + 5, 49, cx1 - 5, 135, 12, fill=CREAM)
    rr(cx0 + 5, 49, cx1 - 5, 135, 12, outline=(230, 205, 150), width=2)
    ln(cx0 + 18, 66, cx1 - 18, 66, TOMATO, 3)
    for k in range(3): ln(cx0 + 18, 90 + k * 20, cx1 - 18, 90 + k * 20, (150, 170, 235), 2)
    for (px_, py_, rs, c) in ((2290, 60, 24, (255, 255, 255)), (2220, 120, 14, PERI), (2340, 110, 10, PERI), (860, 36, 14, (255, 255, 255))): star(px_, py_, rs, c)
    LAY['rect']['preset'] = (u(cx0 + 20), u(72), u(cx1 - cx0 - 40), u(62))
    LAY['rect']['prev'] = (u(930 - 40), u(92 - 40), 40, 40)
    LAY['rect']['next'] = (u(1810 - 40), u(92 - 40), 40, 40)

    # --- sections ---
    SEC = [('CLEAN', 320), ('SQUASH', 320), ('TOAST', 260), ('ECHO', 640), ('MELT', 416), ('OUTPUT', 300)]
    xs = []; x = 72
    for name, w in SEC: xs.append((name, x, w)); x += w
    col, pad = 96, 16
    for i, (name, x0, w) in enumerate(xs):
        if i:
            ln(x0, SY0 + 90, x0, SY1 - 40, (206, 140, 28), 5)
            for t in range(SY0 + 110, SY1 - 50, 26): ln(x0 - 7, t, x0 + 7, t, (206, 140, 28), 3)
        el(x0 + w / 2 - 20, 214, x0 + w / 2 + 20, 254, fill=CREAM, outline=INK, width=3)
        txt(x0 + w / 2, 235, str(i + 1), F(POP_B, 22), INK)
        txt(x0 + w / 2, 276, name, F(POP_B, 26), INK, 'mm', 4)
    def cols(x0, n): return [x0 + pad + col * (k + 0.5) for k in range(n)]
    T0, B0 = 346, 770

    _, x0, w = xs[0]
    for cx, (pid, lv, lb, vl) in zip(cols(x0, 3), (('in', 0.60, 'Input', '0.0 dB'), ('lowcut', 0.34, 'Low Cut', '80 Hz'), ('deess', 0.30, 'De-Ess', '30%'))): vslider(pid, cx, T0, B0, lv, lb, vl, live=live)
    _, x0, w = xs[1]
    for cx, (pid, lv, lb, vl) in zip(cols(x0, 3), (('squash', 0.40, 'Squash', '40%'), ('attack', 0.20, 'Attack', '8 ms'), ('release', 0.50, 'Release', '160 ms'))): vslider(pid, cx, T0, B0, lv, lb, vl, live=live)

    _, x0, w = xs[2]; tc = cols(x0, 2)
    knob('drive', tc[0], 410, 44, 0.25, 'DRIVE', '15%', 318, 480, live=live)
    bx, by = tc[0], 650
    rr(bx - 62, by - 60, bx + 62, by + 64, 34, fill=INK); rr(bx - 57, by - 55, bx + 57, by + 59, 30, fill=(212, 146, 64)); rr(bx - 46, by - 44, bx + 46, by + 48, 24, fill=(250, 214, 140))
    rr(bx - 26, by - 22, bx + 26, by + 6, 8, fill=INK); rr(bx - 22, by - 18, bx + 22, by + 2, 6, fill=BUTTER); rr(bx - 17, by - 15, bx + 2, by - 9, 3, fill=(255, 255, 255, 220))
    txt(bx, by + 84, 'GOLDEN', F(POP_B, 18), INK, 'mm', 2)
    vslider('air', tc[1], T0, B0, 0.60, 'Air', '2.0 dB', live=live)

    _, x0, w = xs[3]
    knob('time', x0 + 120, 420, 56, 0.50, 'TIME', '320 ms', 318, 500, live=live)
    knob('feedback', x0 + w - 120, 420, 56, 0.35, 'FEEDBACK', '35%', 318, 500, live=live)
    lx0, lx1 = x0 + w / 2 - 98, x0 + w / 2 + 98
    rr(lx0 - 8, 332, lx1 + 8, 446, 18, fill=INK); rr(lx0, 340, lx1, 438, 12, fill=(46, 24, 10)); rr(lx0 + 4, 344, lx1 - 4, 354, 5, fill=(255, 255, 255, 40))
    LAY['rect']['lcd'] = (u(lx0), u(340), u(lx1 - lx0), u(98))
    LAY['rect']['sync'] = (u(x0 + w / 2 - 98), u(458), u(90), u(38))
    LAY['rect']['div'] = (u(x0 + w / 2 + 8), u(458), u(90), u(38))
    LAY['rect']['tap'] = (u(x0 + w / 2 - 98), u(516), u(196), u(54))
    for cx, (pid, lv, lb, vl) in zip(cols(x0, 6), (('echohi', 0.55, 'Hi Cut', '6 kHz'), ('echolo', 0.30, 'Lo Cut', '150 Hz'), ('modrate', 0.40, 'Rate', '0.6 Hz'), ('moddepth', 0.15, 'Depth', '15%'), ('spread', 0.50, 'Spread', '50%'), ('echomix', 0.25, 'Echo Mix', '25%'))):
        vslider(pid, cx, 636, 770, lv, lb, vl, label_y=606, live=live)

    _, x0, w = xs[4]; hc = cols(x0, 4)
    for cx, (pid, lv, lb, vl) in zip(hc[:3], (('size', 0.40, 'Size', '40%'), ('damp', 0.50, 'Damp', '50%'), ('verbmix', 0.15, 'Wet', '15%'))): vslider(pid, cx, T0, B0, lv, lb, vl, live=live)
    knob('glitter', hc[3], 420, 46, 0.62, 'GLITTER', '62%', 318, 500, sparkle=True, live=live)
    px, py = hc[3], 670
    el(px - 70, py - 18, px + 70, py + 36, fill=INK); el(px - 64, py - 14, px + 64, py + 30, fill=BUTTER); el(px - 40, py - 4, px + 40, py + 18, outline=BUTTER_D, width=3)
    for (dx, dy, rs, c) in ((-34, -42, 14, PERI), (30, -60, 18, (255, 255, 255)), (46, -18, 10, PERI), (-50, -12, 9, (255, 255, 255)), (4, -80, 11, PERI)): star(px + dx, py + dy, rs, c)

    _, x0, w = xs[5]; mcx = x0 + 104
    knob('mix', mcx, 410, 50, 1.0, 'MIX', '100%', 318, 480, live=live)
    mx, my = mcx, 650
    rr(mx - 80, my - 74, mx + 80, my + 64, 20, fill=INK); rr(mx - 74, my - 68, mx + 74, my + 58, 15, fill=CREAM)
    for i in range(11):
        a = math.radians(-50 + 100 * i / 10); r0, r1 = 62, 76 if i % 5 == 0 else 70
        ln(mx + r0 * math.sin(a), my + 38 - r0 * math.cos(a), mx + r1 * math.sin(a), my + 38 - r1 * math.cos(a), TOMATO if i >= 8 else INK, 3.5)
    txt(mx, my + 6, 'VU', F(POP_B, 24), CHOC)
    LAY['rect']['meter'] = (u(mx), u(my + 38), u(68), 0)
    if live:
        a = math.radians(-50 + 100 * 0.45); ln(mx, my + 38, mx + 68 * math.sin(a), my + 38 - 68 * math.cos(a), INK, 5); el(mx - 9, my + 29, mx + 9, my + 47, fill=INK)
    vslider('out', x0 + 232, T0 + 60, B0, 0.60, 'Output', '0 dB', live=live)

    # --- bottom drips ---
    for (dx, ln_, w_) in ((180, 44, 30), (520, 70, 26), (860, 38, 24), (1180, 84, 34), (1500, 52, 26), (1850, 66, 30), (2210, 46, 26)):
        drip(dx, SY1 - 6, w_, ln_, fill=BUTTER)
    if live:   # sample display, preset name and buttons so the preview looks like the real plug-in
        x0 = xs[3][1]; w = xs[3][2]
        txt(x0 + w / 2, 392, '1/8 D', F(MONO, 44), (255, 214, 90))
        rr(x0 + w / 2 - 98, 458, x0 + w / 2 - 8, 496, 12, fill=INK); rr(x0 + w / 2 - 94, 462, x0 + w / 2 - 12, 492, 9, fill=BUTTER); txt(x0 + w / 2 - 53, 477, 'SYNC', F(POP_B, 17), INK)
        rr(x0 + w / 2 + 8, 458, x0 + w / 2 + 98, 496, 12, fill=INK); rr(x0 + w / 2 + 12, 462, x0 + w / 2 + 94, 492, 9, fill=CREAM); txt(x0 + w / 2 + 53, 477, '1/8D', F(MONO, 17), INK)
        rr(x0 + w / 2 - 98, 516, x0 + w / 2 + 98, 570, 27, fill=INK); rr(x0 + w / 2 - 93, 521, x0 + w / 2 + 93, 565, 22, fill=PERI); txt(x0 + w / 2, 543, 'TAP', F(POP_B, 26), (255, 255, 255), 'mm', 3)
        txt(1370, 98, 'Velvet Hour', ImageFont.truetype(GF + 'Poppins-BoldItalic.ttf', S(40)), INK)
        for bx in (930, 1810):
            el(bx - 36, 56, bx + 36, 128, fill=INK); el(bx - 31, 61, bx + 31, 123, fill=BUTTER)
    return img.resize((W, H), Image.LANCZOS)

bg = render(False); bg.save(os.path.join(ROOT, 'assets', 'skin_bg.png'), optimize=True)
prev = render(True); os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True); prev.save(os.path.join(ROOT, 'docs', 'ButterVox_UI_Preview.png'))

# ---------------- Layout.h ----------------
ctl = sorted(LAY['ctl'], key=lambda c: IDX[c['id']])
assert len(ctl) == len(IDS), (len(ctl), len(IDS))
o = ['#pragma once', '// Generated by tools/build_skin.py. Positions are in editor units (the window is 1200 x 480).', 'namespace skin', '{',
     'struct Ctl { int param; bool knob; float cx, cy, top, bot, r, vx, vy, vw, vh; };',
     'struct Rc { float x, y, w, h; };', 'inline constexpr int kW = 1200, kH = 480;', '', 'inline constexpr Ctl kCtl[] =', '{']
for c in ctl:
    o.append('    { %d, %s, %.2ff, %.2ff, %.2ff, %.2ff, %.2ff, %.2ff, %.2ff, %.2ff, %.2ff }, // %s' % (IDX[c['id']], 'true' if c['knob'] else 'false', c['cx'], c['cy'], c['top'], c['bot'], c['r'], c['vx'], c['vy'], c['vw'], c['vh'], c['id']))
o += ['};', 'inline constexpr int kNumCtl = %d;' % len(ctl), '']
for k, v in LAY['rect'].items():
    o.append('inline constexpr Rc k%s { %.2ff, %.2ff, %.2ff, %.2ff };' % (k.capitalize(), *v))
o += ['} // namespace skin', '']
open(os.path.join(ROOT, 'Source', 'Layout.h'), 'w').write('\n'.join(o))
print('skin ok', len(ctl))
