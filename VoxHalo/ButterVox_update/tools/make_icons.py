"""Makes the Butter Vox app icon and installer icon from the logo's B."""
import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, '..', 'assets')
N = 1024
def vgrad(w, h, c0, c1):
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(c0, float)[None, None, :] * (1 - t) + np.array(c1, float)[None, None, :] * t
    return Image.fromarray(np.repeat(a, w, axis=1).astype('uint8'), 'RGB')

def base():
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    g = vgrad(N, N, (176, 112, 46), (104, 60, 26)).convert('RGBA')
    m = Image.new('L', (N, N), 0); ImageDraw.Draw(m).rounded_rectangle((60, 60, N - 60, N - 60), radius=210, fill=255)
    img.paste(g, (0, 0), m)
    glow = Image.new('RGBA', (N, N), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse((170, 130, 860, 820), fill=(255, 214, 110, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(90)); img = Image.alpha_composite(img, glow)
    img.putalpha(m)
    logo = Image.open(os.path.join(A, 'ButterVox_logo_nosparkle.png')).convert('RGBA')
    lw = 860; b = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    img.alpha_composite(b, ((N - b.width) // 2, (N - b.height) // 2 - 30))
    d = ImageDraw.Draw(img)
    def star(cx, cy, r, c):
        d.polygon([(cx, cy - r), (cx + r * .22, cy - r * .22), (cx + r, cy), (cx + r * .22, cy + r * .22), (cx, cy + r), (cx - r * .22, cy + r * .22), (cx - r, cy), (cx - r * .22, cy - r * .22)], fill=c)
    star(790, 250, 60, (255, 244, 200, 255)); star(860, 350, 30, (255, 244, 200, 255)); star(200, 270, 38, (255, 244, 200, 255)); star(250, 770, 30, (255, 244, 200, 255))
    return img

sizes = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]
app = base()
app.resize((512, 512), Image.LANCZOS).save(os.path.join(A, 'icon_512.png'))
app.save(os.path.join(A, 'buttervox_1024.png'))
app.save(os.path.join(A, 'buttervox.icns'), sizes=sizes)

inst = base(); d = ImageDraw.Draw(inst)
cx, cy, r = 760, 760, 190
d.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=(255, 255, 255, 255))
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(112, 128, 224, 255))
w = 34
d.rectangle((cx - w, cy - r * .55, cx + w, cy + r * .08), fill=(255, 255, 255, 255))
d.polygon([(cx - r * .5, cy - 6), (cx + r * .5, cy - 6), (cx, cy + r * .52)], fill=(255, 255, 255, 255))
d.rectangle((cx - r * .5, cy + r * .66, cx + r * .5, cy + r * .76), fill=(255, 255, 255, 255))
inst.save(os.path.join(A, 'buttervox_installer.icns'), sizes=sizes)
inst.save(os.path.join(A, 'buttervox_installer_1024.png'))
print('icons ok')
