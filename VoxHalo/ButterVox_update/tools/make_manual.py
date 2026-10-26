import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from presets_data import PRESETS
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether, Flowable)

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'docs', 'ButterVox_User_Manual.pdf')
ICON = os.path.join(HERE, '..', 'assets', 'buttervox_1024.png')
UIPREV = os.path.join(HERE, '..', 'docs', 'ButterVox_UI_Preview.png')

VIOLET = colors.HexColor('#7a4a22'); CYAN = colors.HexColor('#a9741f'); PINK = colors.HexColor('#c0602a')
AMBER = colors.HexColor('#d8a017'); MINT = colors.HexColor('#b58a2a'); CORAL = colors.HexColor('#a8501e')
INK = colors.HexColor('#3b2210'); SOFT = colors.HexColor('#fff6dd')

ss = getSampleStyleSheet()
body = ParagraphStyle('b', parent=ss['BodyText'], fontName='Helvetica', fontSize=10.2, leading=14.6, textColor=INK, spaceAfter=6)
h1 = ParagraphStyle('h1', parent=ss['Heading1'], fontName='Helvetica-Bold', fontSize=21, leading=25, textColor=VIOLET, spaceBefore=4, spaceAfter=10)
h2 = ParagraphStyle('h2', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=13.5, leading=17, textColor=INK, spaceBefore=10, spaceAfter=5)
small = ParagraphStyle('s', parent=body, fontSize=8.8, leading=12, spaceAfter=0)
cell = ParagraphStyle('c', parent=body, fontSize=8.8, leading=11.5, spaceAfter=0)
cellb = ParagraphStyle('cb', parent=cell, fontName='Helvetica-Bold')
bullet = ParagraphStyle('bl', parent=body, leftIndent=14, bulletIndent=2, spaceAfter=3)

def P(t, s=body): return Paragraph(t, s)
def B(items): return [Paragraph(t, bullet, bulletText='\u2022') for t in items]

def page(c, d):
    c.saveState()
    c.setFont('Helvetica', 8.5); c.setFillColor(colors.HexColor('#8a6a40'))
    c.drawString(0.8*inch, 0.5*inch, 'Butter Vox User Manual  |  Version 1.0')
    c.drawRightString(letter[0]-0.8*inch, 0.5*inch, f'Page {d.page}')
    c.setStrokeColor(colors.HexColor('#e6d3a0')); c.line(0.8*inch, 0.65*inch, letter[0]-0.8*inch, 0.65*inch)
    c.restoreState()

def cover(c, d):
    c.saveState()
    w, h = letter
    steps = 60
    for i in range(steps):
        t = i/steps
        r = 0.36 + (0.98-0.36)*t; g = 0.20 + (0.78-0.20)*t; b = 0.08 + (0.28-0.08)*t
        c.setFillColorRGB(r, g, b); c.rect(0, h*(1-(i+1)/steps), w, h/steps+1, stroke=0, fill=1)
    c.restoreState()

class Table2(Flowable): pass

def tbl(data, widths, head=VIOLET, zebra=True):
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('BACKGROUND', (0,0), (-1,0), head), ('TEXTCOLOR', (0,0), (-1,0), colors.white),
          ('VALIGN', (0,0), (-1,-1), 'TOP'), ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#e3cf9a')),
          ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
          ('TOPPADDING', (0,0), (-1,-1), 3.5), ('BOTTOMPADDING', (0,0), (-1,-1), 3.5)]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0: st.append(('BACKGROUND', (0,i), (-1,i), SOFT))
    t.setStyle(TableStyle(st)); return t

class UIMap(Flowable):
    """Schematic of the plug-in layout."""
    def __init__(self, w=6.9*inch, h=2.9*inch): super().__init__(); self.w, self.h = w, h
    def wrap(self, aw, ah): return self.w, self.h
    def draw(self):
        c = self.canv; w, h = self.w, self.h
        c.setFillColor(colors.HexColor('#12163a')); c.roundRect(0, 0, w, h, 8, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont('Helvetica-Bold', 14); c.drawString(14, h-24, 'VOXHALO')
        c.setFont('Helvetica', 7); c.setFillColor(colors.HexColor('#9aa0d0')); c.drawString(14, h-34, 'VOCAL CHAIN + HYBRID ECHO')
        c.setFillColor(colors.HexColor('#252b5a')); c.roundRect(w*0.4, h-32, w*0.22, 18, 4, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont('Helvetica', 7); c.drawCentredString(w*0.51, h-26, 'Preset browser   < >')
        groups = [('INPUT + CLEAN', 3, CYAN), ('SQUASH', 3, PINK), ('GLOW', 2, AMBER), ('ECHO', 8, VIOLET), ('HALO', 3, MINT), ('OUTPUT', 2, CORAL)]
        total = sum(g[1] for g in groups) + 1.6*len(groups)
        unit = (w-20) / total; x = 10
        for name, n, col in groups:
            pw = n*unit + 1.2*unit
            c.setFillColor(col); c.setFillAlpha(0.16); c.roundRect(x, 10, pw-4, h-52, 6, stroke=0, fill=1); c.setFillAlpha(1)
            c.setStrokeColor(col); c.setLineWidth(0.8); c.roundRect(x, 10, pw-4, h-52, 6, stroke=1, fill=0)
            c.setFillColor(col); c.setFont('Helvetica-Bold', 6.5); c.drawString(x+5, h-60, name)
            for k in range(n):
                cx = x + 0.6*unit + (k+0.5)*unit - 2
                c.setFillColor(colors.HexColor('#060914')); c.roundRect(cx-1.5, 22, 3, h-100, 1.5, stroke=0, fill=1)
                level = 0.25 + 0.5*((k*37 + len(name)*13) % 10)/10
                c.setFillColor(col); c.roundRect(cx-1.5, 22, 3, (h-100)*level, 1.5, stroke=0, fill=1)
                c.setFillColor(colors.white); c.roundRect(cx-5, 22+(h-100)*level-3, 10, 6, 2, stroke=0, fill=1)
            x += pw

class FlowChain(Flowable):
    def __init__(self, w=6.9*inch, h=1.15*inch): super().__init__(); self.w, self.h = w, h
    def wrap(self, aw, ah): return self.w, self.h
    def draw(self):
        c = self.canv
        stages = [('IN', INK), ('LOW CUT', CYAN), ('DE-ESS', CYAN), ('SQUASH', PINK), ('TOAST', AMBER), ('AIR', AMBER), ('ECHO', VIOLET), ('MELT', MINT), ('MIX / OUT', CORAL)]
        n = len(stages); bw = (self.w - (n-1)*8) / n
        for i, (name, col) in enumerate(stages):
            x = i*(bw+8)
            c.setFillColor(col); c.roundRect(x, 30, bw, 34, 6, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont('Helvetica-Bold', 6.6); c.drawCentredString(x+bw/2, 43, name)
            if i < n-1:
                c.setStrokeColor(INK); c.setLineWidth(1); c.line(x+bw, 47, x+bw+8, 47)
        c.setFillColor(INK); c.setFont('Helvetica', 7.5)
        c.drawString(0, 12, 'Dry input is tapped after the Input knob and blended back in by the Mix slider. The Melt reverb listens to the post-echo signal.')

def build():
    doc = BaseDocTemplate(OUT, pagesize=letter, leftMargin=0.8*inch, rightMargin=0.8*inch, topMargin=0.8*inch, bottomMargin=0.85*inch,
                          title='Butter Vox User Manual', author='Butter Vox Audio')
    w, h = letter
    f_cover = Frame(0.8*inch, 0.8*inch, w-1.6*inch, h-1.6*inch, id='c')
    f_body = Frame(0.8*inch, 0.8*inch, w-1.6*inch, h-1.6*inch, id='b')
    doc.addPageTemplates([PageTemplate(id='cover', frames=[f_cover], onPage=cover, autoNextPageTemplate='body'),
                          PageTemplate(id='body', frames=[f_body], onPage=page)])
    S = []
    # cover
    tw = ParagraphStyle('tw', fontName='Helvetica-Bold', fontSize=46, leading=50, textColor=colors.white)
    ts = ParagraphStyle('ts', fontName='Helvetica', fontSize=17, leading=22, textColor=colors.HexColor('#f4efff'))
    S += [Spacer(1, 0.9*inch), Image(ICON, 2.6*inch, 2.6*inch), Spacer(1, 0.4*inch), Paragraph('Butter Vox', tw),
          Paragraph('Vocal Chain + Melting Echo', ts), Spacer(1, 0.2*inch),
          Paragraph('User Manual  |  Version 1.0  |  macOS (Audio Unit, VST3, Standalone)', ParagraphStyle('t3', parent=ts, fontSize=11.5)), PageBreak()]

    # welcome
    S += [P('Welcome to Butter Vox', h1),
          P('Butter Vox is a complete vocal chain in one window. It cleans, compresses, warms and brightens a voice, then adds a modulated stereo echo and a melting reverb with a glittering shimmer. Every control is a vertical slider, grouped into colour-coded sections so you can read the whole chain at a glance.'),
          P('The plug-in is built for lead vocals, ad-libs, loop-station layers and spoken word. Twenty recipe presets cover jazz, soul, hip-hop, trap, afrobeats and ambient sounds, and every preset is a starting point you can reshape.'),
          P('Highlights', h2)] + B([
          '<b>One slab of butter, six sections:</b> Input + Clean, Squash, Toast, Echo, Melt and Output.',
          '<b>Hybrid echo:</b> free time, tempo sync or tap tempo, ping-pong spread, filters inside the feedback loop and tape-style modulation.',
          '<b>Glitter:</b> an octave-up shimmer that sparkles inside the Melt reverb.',
          '<b>Resizable and sharp:</b> drag the bottom-right corner to scale the interface from half size to double size.',
          '<b>Tooltips everywhere:</b> hover any control for a plain-language explanation.',
          '<b>Live meter:</b> the vintage VU meter follows your output level.',
          '<b>20 presets</b> reachable from the preset menu, the arrow buttons or your DAW\'s own preset list.']) + [
          P('Interface map', h2), Image(UIPREV, 6.9*inch, 6.9*inch*960/2400), Spacer(1, 6),
          P('The picture above shows the interface. Sections run left to right in signal order. The Echo section carries the display, the Sync switch, the note-length menu and the TAP button.', small), PageBreak()]

    # install
    S += [P('Installation (macOS)', h1),
          P('<b>System requirements:</b> macOS 11 or later, Apple Silicon or Intel (universal build). A host that supports Audio Unit or VST3 plug-ins, such as Logic Pro, GarageBand, Ableton Live, Reaper or Studio One. Butter Vox is a stereo plug-in.'),
          P('Using the installer', h2)] + B([
          'Open <b>ButterVox-1.0.0.dmg</b> and double-click <b>ButterVox-1.0.0.pkg</b>.',
          'Follow the prompts. Enter your Mac password when asked.',
          'The installer places the files shown in the table below.',
          'Restart your DAW. Logic Pro scans new Audio Units automatically on launch.']) + [
          Spacer(1, 4),
          tbl([[P('File', cellb), P('Location', cellb)],
               [P('Butter Vox.component (Audio Unit)', cell), P('/Library/Audio/Plug-Ins/Components', cell)],
               [P('Butter Vox.vst3', cell), P('/Library/Audio/Plug-Ins/VST3', cell)],
               [P('Butter Vox.app (Standalone)', cell), P('/Applications', cell)],
               [P('This manual (PDF)', cell), P('/Library/Application Support/Butter Vox', cell)]],
              [2.9*inch, 4.0*inch]),
          P('First launch and Gatekeeper', h2),
          P('Builds that are not notarized by Apple show a warning the first time. Control-click (or right-click) the installer, choose Open, then confirm. If macOS still blocks a plug-in, open System Settings, Privacy and Security, and choose Open Anyway next to the Butter Vox message.'),
          P('Using Butter Vox in your DAW', h2)] + B([
          '<b>Logic Pro:</b> add an Audio FX slot, choose Audio Units, then Butter Vox Audio, then Butter Vox. If it does not appear, open Logic Pro, Settings, Plug-in Manager and press Reset and Rescan Selection.',
          '<b>Ableton Live:</b> enable VST3 and Audio Units in Preferences, Plug-ins, then rescan.',
          '<b>Standalone app:</b> open Butter Vox from Applications, pick your audio interface in the settings button, and sing. Use headphones to avoid feedback.']) + [
          P('Uninstalling', h2),
          P('Delete the three items listed in the table above (the plug-in files and the app). No other files are installed.'), PageBreak()]

    # quick start
    S += [P('Quick start', h1)] + B([
          '<b>1. Pick a preset.</b> Use the menu at the top or the &lt; and &gt; buttons. Start with Soft Open or Velvet Hour.',
          '<b>2. Set Input.</b> Sing a loud phrase and lower Input until the signal stays comfortably away from clipping.',
          '<b>3. Shape the voice.</b> Raise Low Cut until the boom disappears, add De-Ess if S sounds sharp, then bring up Squash until the level feels steady.',
          '<b>4. Add colour.</b> A little Drive adds warmth. Air lifts the top end or softens a bright microphone.',
          '<b>5. Add space.</b> Turn Echo Mix up for repeats, Wet up for room and Glitter up for sparkle. Turn on Sync to lock the echo to your tempo.',
          '<b>6. Balance.</b> Use Mix to blend with the dry voice and Output to set the final level.']) + [
          P('Handy tips', h2)] + B([
          'Double-click any slider to return it to its default value.',
          'Click a value under a slider to type an exact number. Typing 2k sets 2 kHz.',
          'Hold Shift while dragging for fine control.',
          'Hover over any control for a tooltip.',
          'Resize the window by dragging the bottom-right corner.',
          'Double-click any knob or slider to reset it. Presets load instantly and are saved with your DAW project, along with any tweaks you made.']) + [PageBreak()]

    # signal flow
    S += [P('Signal flow', h1), FlowChain(), Spacer(1, 6),
          P('Processing runs in the order shown. Cleaning comes first so rumble and harsh sibilance never reach the compressor or the echo. The echo feeds the reverb, so every repeat pools into the room.')]

    # controls
    params = [
      ('INPUT + CLEAN', CYAN, [('Input','-24 to +12 dB','0 dB','Gain into the chain. Set it so peaks stay clear of clipping.'),
                              ('Low Cut','20 to 400 Hz','80 Hz','High-pass filter that removes rumble, plosives and proximity boom.'),
                              ('De-Ess','0 to 100%','30%','Reduces harsh S and T sounds above about 6.5 kHz.')]),
      ('SQUASH', PINK, [('Squash','0 to 100%','40%','One-knob compressor. Higher settings lower the threshold, raise the ratio and add automatic makeup gain.'),
                        ('Attack','0.1 to 80 ms','8 ms','How quickly compression starts. Slower keeps more punch.'),
                        ('Release','20 to 800 ms','160 ms','How quickly compression lets go. Longer is smoother.')]),
      ('TOAST', AMBER, [('Drive','0 to 100%','15%','Warm saturation that adds harmonics and presence. Think light, golden, dark and burnt toast.'),
                       ('Air','-6 to +9 dB','+2 dB','High shelf at 9 kHz. Positive values add sparkle, negative values soften.')]),
      ('ECHO', VIOLET, [('Time','20 to 1500 ms','320 ms','Delay time. Greyed out while Sync is on.'),
                        ('Feedback','0 to 95%','35%','Number of repeats. A safety limiter keeps high settings under control.'),
                        ('Hi Cut','1 to 20 kHz','6 kHz','Low-pass filter in the feedback loop. Each repeat grows darker.'),
                        ('Lo Cut','20 to 1000 Hz','150 Hz','High-pass filter in the feedback loop. Keeps repeats light and clear of the vocal.'),
                        ('Rate','0.05 to 8 Hz','0.6 Hz','Speed of the delay-time modulation.'),
                        ('Depth','0 to 100%','15%','Amount of modulation, up to plus or minus 8 ms. Opposite phase on left and right adds width.'),
                        ('Spread','0 to 100%','50%','Stereo ping-pong. At 100% the echoes alternate fully between left and right.'),
                        ('Echo Mix','0 to 100%','25%','Level of the echo added to the vocal.'),
                        ('Sync / Division','Off, 1/16 to 1/1','Off, 1/4','Locks the echo to the DAW tempo. T is triplet and D is dotted. Without tempo information the plug-in assumes 120 BPM.'),
                        ('TAP','n/a','n/a','Tap a few times to set the echo time. Sync switches off so your tapped time is heard.')]),
      ('MELT', MINT, [('Size','0 to 100%','40%','Room size, from a small booth to a cathedral.'),
                      ('Damp','0 to 100%','50%','High-frequency absorption. Higher is darker.'),
                      ('Wet','0 to 100%','15%','Level of the Melt reverb.'),
                      ('Glitter','0 to 100%','0%','Octave-up shimmer inside the reverb. Raise it for sparkle and glassy glow.')]),
      ('OUTPUT', CORAL, [('Mix','0 to 100%','100%','Blend between the dry input and the full chain.'),
                         ('Output','-24 to +12 dB','0 dB','Final level.')]),
    ]
    S += [P('Control reference', h1)]
    for name, col, rows in params:
        data = [[P('Control', cellb), P('Range', cellb), P('Default', cellb), P('What it does', cellb)]]
        for r in rows: data.append([P('<b>%s</b>' % r[0], cell), P(r[1], cell), P(r[2], cell), P(r[3], cell)])
        S.append(KeepTogether([P(name, h2), tbl(data, [1.05*inch, 1.15*inch, 0.8*inch, 3.9*inch], head=col), Spacer(1, 4)]))
    S.append(PageBreak())

    # presets
    divs = ['1/16','1/8T','1/8','1/8D','1/4T','1/4','1/4D','1/2','1/1']
    S += [P('Factory presets', h1), P('Twenty presets ship with Butter Vox. Names in the Echo column show the tempo-synced note length where Sync is on.')]
    data = [[P('#', cellb), P('Name', cellb), P('Echo', cellb), P('Character', cellb)]]
    for i, (name, vals, sync, div, desc) in enumerate(PRESETS, 1):
        echo = divs[div] if sync else '%d ms' % vals[8]
        data.append([P(str(i), cell), P('<b>%s</b>' % name, cell), P(echo, cell), P(desc, cell)])
    S += [tbl(data, [0.35*inch, 1.45*inch, 0.7*inch, 4.4*inch]), PageBreak()]

    # recipes
    S += [P('Recipes and tips', h1),
          P('Lead vocal polish', h2), P('Start with Velvet Hour. Set Low Cut near 90 Hz, De-Ess to taste, Squash around 50% and a little Drive. Keep Echo Mix under 25% so words stay clear.'),
          P('Loop-station layers', h2), P('Use Spread near 100% on background layers and a lower Mix on the lead. Layer presets such as Satin Choir and Candlelight turn simple loops into stacked harmonies.'),
          P('Making echoes sit behind the voice', h2), P('Raise Lo Cut and lower Hi Cut in the Echo section. Thinner, darker repeats leave room for the lead vocal.'),
          P('Ad-libs and throws', h2), P('Use Pillow Talk or Slow Burn, then automate Echo Mix in your DAW so only the last word of a phrase repeats.'),
          P('Tape feel', h2), P('Combine Drive at 40 to 50%, Depth at 30 to 40% and Hi Cut near 3.5 kHz.'),
          P('Gain staging', h2), P('Squash adds automatic makeup gain. Check the level after changing it and use Output to match the bypassed level for fair comparisons.'),
          P('Troubleshooting', h1),
          tbl([[P('Problem', cellb), P('Solution', cellb)],
               [P('Plug-in missing in Logic Pro', cell), P('Restart Logic Pro, then use Settings, Plug-in Manager, Reset and Rescan Selection. Confirm Butter Vox.component sits in /Library/Audio/Plug-Ins/Components.', cell)],
               [P('Plug-in missing in another DAW', cell), P('Enable VST3 scanning in the DAW preferences and rescan.', cell)],
               [P('macOS blocks the installer', cell), P('Control-click the installer, choose Open, or use Open Anyway in Privacy and Security.', cell)],
               [P('Echo timing drifts from the beat', cell), P('Turn Sync on and make sure the DAW project tempo is set. Hosts that share no tempo give 120 BPM.', cell)],
               [P('Feedback squeal in Standalone', cell), P('Use headphones or lower the input level. Mute the monitor speakers.', cell)],
               [P('Mono track', cell), P('Butter Vox is a stereo plug-in. Place it on a stereo track or an aux send. Most hosts upmix a mono track automatically.', cell)]],
              [2.0*inch, 4.9*inch]),
          P('Technical specifications', h1),
          tbl([[P('Item', cellb), P('Detail', cellb)],
               [P('Formats', cell), P('Audio Unit (effect), VST3, Standalone app', cell)],
               [P('Architecture', cell), P('Universal (arm64 and x86_64), macOS 11 or later', cell)],
               [P('Channels', cell), P('Stereo in, stereo out', cell)],
               [P('Latency', cell), P('0 samples', cell)],
               [P('Maximum echo time', cell), P('2.9 seconds (tempo-synced times are clamped to this)', cell)],
               [P('Reverb tail', cell), P('Reported to the host as 6 seconds', cell)],
               [P('Interface size', cell), P('600 x 240 up to 2400 x 960 points, fixed aspect ratio', cell)],
               [P('Presets', cell), P('20 factory presets, host program list supported', cell)]],
              [2.0*inch, 4.9*inch]),
          Spacer(1, 10), P('Butter Vox is a trademark of its author. Audio Unit is a trademark of Apple Inc. VST is a trademark of Steinberg Media Technologies GmbH. All other names belong to their owners.', small)]
    doc.build(S)
    print('manual ok')

build()
