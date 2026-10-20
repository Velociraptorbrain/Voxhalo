from PIL import Image, ImageDraw, ImageFilter
import os
S = 2048
out = os.path.join(os.path.dirname(__file__), '..', 'assets')

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def base():
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    # diagonal gradient violet -> magenta -> coral
    grad = Image.new('RGBA', (S, S))
    px = grad.load()
    c1, c2, c3 = (74, 52, 255), (232, 64, 190), (255, 120, 80)
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S)
            c = lerp(c1, c2, t * 2) if t < 0.5 else lerp(c2, c3, (t - 0.5) * 2)
            px[x, y] = c + (255,)
    m = Image.new('L', (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle((int(S*0.06), int(S*0.06), int(S*0.94), int(S*0.94)), radius=int(S*0.21), fill=255)
    img.paste(grad, (0, 0), m)
    d = ImageDraw.Draw(img)
    # glow behind ring
    glow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((S*0.26, S*0.10, S*0.74, S*0.58), outline=(110, 245, 255, 230), width=int(S*0.045))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(S*0.025)))
    d = ImageDraw.Draw(img)
    # halo ring
    d.ellipse((S*0.26, S*0.10, S*0.74, S*0.58), outline=(255, 255, 255, 255), width=int(S*0.032))
    # three vertical sliders
    for i, (x, h) in enumerate([(0.33, 0.62), (0.5, 0.45), (0.67, 0.7)]):
        cx = S * x
        top, bot = S*0.64, S*0.87
        d.rounded_rectangle((cx - S*0.012, top, cx + S*0.012, bot), radius=int(S*0.012), fill=(20, 16, 70, 200))
        ty = bot - (bot - top) * h
        d.rounded_rectangle((cx - S*0.009, ty, cx + S*0.009, bot), radius=int(S*0.009), fill=(120, 240, 255, 255))
        d.rounded_rectangle((cx - S*0.05, ty - S*0.022, cx + S*0.05, ty + S*0.022), radius=int(S*0.018), fill=(255, 255, 255, 255))
    return img

app = base()
sizes = [(16,16),(32,32),(64,64),(128,128),(256,256),(512,512),(1024,1024)]
app.resize((512, 512), Image.LANCZOS).save(os.path.join(out, 'icon_512.png'))
app.resize((1024, 1024), Image.LANCZOS).save(os.path.join(out, 'voxhalo_1024.png'))
app.resize((1024, 1024), Image.LANCZOS).save(os.path.join(out, 'voxhalo.icns'), sizes=sizes)

# installer icon: same artwork with a download-arrow badge
inst = base()
d = ImageDraw.Draw(inst)
cx, cy, r = S*0.74, S*0.74, S*0.2
d.ellipse((cx-r-S*0.02, cy-r-S*0.02, cx+r+S*0.02, cy+r+S*0.02), fill=(255, 255, 255, 255))
d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(20, 200, 150, 255))
w = S*0.035
d.rectangle((cx-w, cy-r*0.55, cx+w, cy+r*0.1), fill=(255, 255, 255, 255))
d.polygon([(cx-r*0.5, cy), (cx+r*0.5, cy), (cx, cy+r*0.55)], fill=(255, 255, 255, 255))
d.rectangle((cx-r*0.5, cy+r*0.68, cx+r*0.5, cy+r*0.78), fill=(255, 255, 255, 255))
inst.resize((1024, 1024), Image.LANCZOS).save(os.path.join(out, 'voxhalo_installer.icns'), sizes=sizes)
inst.resize((1024, 1024), Image.LANCZOS).save(os.path.join(out, 'voxhalo_installer_1024.png'))
print('icons ok')
