# Order of values:
# in, lowcut, deess, squash, attack, release, drive, air,
# time, feedback, echohi, echolo, modrate, moddepth, spread, echomix,
# size, damp, verbmix, glitter, mix, out
# sync: 0/1, div index: 0=1/16 1=1/8T 2=1/8 3=1/8D 4=1/4T 5=1/4 6=1/4D 7=1/2 8=1/1

PRESETS = [
 ("Soft Open",      [0,80,0.3,0.4,8,160,0.15,2,320,0.35,6000,150,0.6,0.15,0.5,0.25,0.4,0.5,0.15,0.0,1,0],   0,5, "A clean, polished beginning with a whisper of echo and room."),
 ("Velvet Hour",     [0,90,0.4,0.5,10,150,0.2,3,300,0.3,5500,160,0.5,0.15,0.4,0.22,0.45,0.5,0.18,0.05,1,0],  1,3, "Smooth, close lead vocal with a dotted echo that lingers like a slow exhale."),
 ("Close Talk",   [0,100,0.4,0.5,6,120,0.25,2,110,0.12,7000,200,0.3,0.05,0.2,0.3,0.2,0.6,0.05,0.0,1,0],  0,5, "Short golden slapback that sounds like someone leaning in to speak at your ear."),
 ("Slow Dance",   [0,100,0.4,0.45,8,150,0.1,3,375,0.45,6500,180,0.4,0.1,1.0,0.28,0.35,0.5,0.12,0.1,1,0], 1,5, "Quarter note echoes that sway from side to side."),
 ("Candlelight",      [-1,90,0.4,0.4,12,200,0.1,4,520,0.55,4500,200,0.8,0.3,0.7,0.3,0.85,0.4,0.4,0.3,1,-1],  0,5, "Big, warm bloom with slow repeats that glow and fade."),
 ("Smoke and Satin",   [0,90,0.3,0.5,10,180,0.45,1,250,0.42,3800,220,1.2,0.35,0.3,0.3,0.3,0.6,0.1,0.0,1,0],   1,2, "Warm, wobbly tape echoes with a soft haze around the edges."),
 ("Midnight Pulse",   [0,110,0.5,0.6,5,100,0.3,4,200,0.38,7500,250,0.2,0.05,0.6,0.3,0.3,0.5,0.1,0.05,1,0],    1,1, "Tight, glossy triplet echoes with an urgent heartbeat."),
 ("Hip Sway",     [0,100,0.4,0.5,8,140,0.2,3,280,0.4,6000,200,0.5,0.1,0.8,0.27,0.3,0.5,0.12,0.05,1,0],    1,3, "Dotted eighth echoes that swing wide, made for afrobeats grooves."),
 ("Amber Room",       [0,80,0.3,0.45,15,220,0.35,2,180,0.2,5000,150,0.4,0.1,0.3,0.15,0.55,0.6,0.25,0.0,1,0], 0,5, "A warm, close room with a hint of grit, like a lit-low lounge."),
 ("Last Call",       [0,70,0.2,0.3,20,250,0.1,1,240,0.22,4500,130,0.3,0.08,0.4,0.15,0.6,0.7,0.28,0.0,1,0],  0,5, "Gentle compression, a dim room and a soft echo for late-set intimacy."),
 ("Late Night Line", [0,300,0.3,0.7,3,80,0.7,-3,150,0.25,3000,400,0.5,0.1,0.2,0.2,0.1,0.8,0.05,0.0,1,2],    0,5, "Narrow, crunchy phone-call tone, close and a little secretive."),
 ("Slow Tide",  [0,90,0.3,0.4,10,200,0.15,-2,420,0.6,2800,180,2.5,0.8,0.6,0.35,0.5,0.8,0.2,0.15,1,0],   0,5, "Deep, rolling modulation with dark repeats that pull you under."),
 ("Golden Hour",      [0,100,0.5,0.55,6,120,0.25,6,400,0.25,8000,200,0.4,0.1,0.5,0.2,0.4,0.4,0.15,0.2,1,-1], 1,5, "Bright, forward and radiant with a clean quarter note echo."),
 ("Breathless",     [0,120,0.6,0.5,10,150,0.1,8,300,0.3,9000,250,0.6,0.2,0.6,0.25,0.6,0.3,0.25,0.35,1,0],   0,5, "Airy, shimmering top end for soft vocals right at the microphone."),
 ("Cathedral Hush",       [-1,90,0.4,0.4,15,250,0.05,3,600,0.4,5000,200,0.3,0.15,0.5,0.2,0.95,0.3,0.5,0.25,1,-2],0,5, "A vast stone hall with slow echoes, spacious and reverent."),
 ("Slow Burn",       [0,120,0.3,0.5,8,160,0.4,1,450,0.75,3500,300,0.4,0.2,0.8,0.5,0.4,0.6,0.15,0.05,1,-1],   1,6, "Long dotted quarter trails that build and smolder."),
 ("Love Letter Tape",  [0,150,0.2,0.6,12,180,0.65,-4,330,0.5,2500,300,1.5,0.5,0.3,0.3,0.25,0.9,0.1,0.0,1,0],  0,5, "Dusty, saturated cassette warmth, like a mixtape made by hand."),
 ("Pillow Talk",  [0,110,0.5,0.6,5,110,0.3,3,250,0.3,6000,200,0.3,0.05,0.9,0.5,0.3,0.5,0.1,0.1,1,0],     1,2, "Wide eighth note throws that whisper across the stereo field."),
 ("Champagne Shimmer",    [0,100,0.4,0.4,10,160,0.15,7,350,0.5,10000,250,3.0,0.4,0.7,0.3,0.75,0.2,0.35,0.7,1,-1],0,5, "Glittering, glassy modulation with a bright, effervescent reverb."),
 ("Satin Choir",      [0,90,0.4,0.5,10,170,0.25,4,480,0.5,5500,180,0.9,0.4,1.0,0.35,0.8,0.4,0.35,0.4,1,-1],  0,5, "Layered, swirling stereo repeats that sound like a velvet choir."),
]
assert len(PRESETS) == 20 and all(len(p[1]) == 22 for p in PRESETS)
