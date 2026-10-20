# Order of values:
# in, lowcut, deess, squash, attack, release, drive, air,
# time, feedback, echohi, echolo, modrate, moddepth, spread, echomix,
# size, damp, verbmix, mix, out
# sync: 0/1, div index: 0=1/16 1=1/8T 2=1/8 3=1/8D 4=1/4T 5=1/4 6=1/4D 7=1/2 8=1/1

PRESETS = [
 ("Init Clean",      [0,80,0.3,0.4,8,160,0.15,2, 320,0.35,6000,150,0.6,0.15,0.5,0.25, 0.4,0.5,0.15,1,0],   0,5, "Balanced starting point with gentle polish, a short echo and a touch of room."),
 ("Velvet Lead",     [0,90,0.4,0.5,10,150,0.2,3, 300,0.3,5500,160,0.5,0.15,0.4,0.22, 0.45,0.5,0.18,1,0],  1,3, "Smooth lead vocal with a dotted eighth echo locked to tempo."),
 ("Slapback Gold",   [0,100,0.4,0.5,6,120,0.25,2, 110,0.12,7000,200,0.3,0.05,0.2,0.3, 0.2,0.6,0.05,1,0],  0,5, "Short vintage slapback for rockabilly, soul and upfront pop."),
 ("Ping Pong Pop",   [0,100,0.4,0.45,8,150,0.1,3, 375,0.45,6500,180,0.4,0.1,1.0,0.28, 0.35,0.5,0.12,1,0], 1,5, "Quarter note echoes bouncing wide across the stereo field."),
 ("Dream Halo",      [-1,90,0.4,0.4,12,200,0.1,4, 520,0.55,4500,200,0.8,0.3,0.7,0.3, 0.85,0.4,0.4,1,-1],  0,5, "Big airy bloom for ambient vocals and pads of voice."),
 ("Tape Echo 1/8",   [0,90,0.3,0.5,10,180,0.45,1, 250,0.42,3800,220,1.2,0.35,0.3,0.3, 0.3,0.6,0.1,1,0],   1,2, "Warm, wobbly tape-style eighth note repeats."),
 ("Trap Triplets",   [0,110,0.5,0.6,5,100,0.3,4, 200,0.38,7500,250,0.2,0.05,0.6,0.3, 0.3,0.5,0.1,1,0],    1,1, "Tight, bright triplet echoes for trap and modern hip-hop hooks."),
 ("Afro Bounce",     [0,100,0.4,0.5,8,140,0.2,3, 280,0.4,6000,200,0.5,0.1,0.8,0.27, 0.3,0.5,0.12,1,0],    1,3, "Dotted eighth groove echo with wide bounce for afrobeats."),
 ("Soul Room",       [0,80,0.3,0.45,15,220,0.35,2, 180,0.2,5000,150,0.4,0.1,0.3,0.15, 0.55,0.6,0.25,1,0], 0,5, "Warm, close room with a hint of grit for soulful lines."),
 ("Jazz Club",       [0,70,0.2,0.3,20,250,0.1,1, 240,0.22,4500,130,0.3,0.08,0.4,0.15, 0.6,0.7,0.28,1,0],  0,5, "Light compression, natural room and a soft echo for intimate jazz."),
 ("Radio Telephone", [0,300,0.3,0.7,3,80,0.7,-3, 150,0.25,3000,400,0.5,0.1,0.2,0.2, 0.1,0.8,0.05,1,2],    0,5, "Narrow, crunchy broadcast tone for lo-fi intros and effect verses."),
 ("Underwater Mod",  [0,90,0.3,0.4,10,200,0.15,-2, 420,0.6,2800,180,2.5,0.8,0.6,0.35, 0.5,0.8,0.2,1,0],   0,5, "Deep chorus-style wobble with dark repeats."),
 ("Vocal Lift",      [0,100,0.5,0.55,6,120,0.25,6, 400,0.25,8000,200,0.4,0.1,0.5,0.2, 0.4,0.4,0.15,1,-1], 1,5, "Bright, forward vocal for choruses with a clean quarter note echo."),
 ("Whisper Air",     [0,120,0.6,0.5,10,150,0.1,8, 300,0.3,9000,250,0.6,0.2,0.6,0.25, 0.6,0.3,0.25,1,0],   0,5, "Breathy, sparkling top end for soft and close vocals."),
 ("Cathedral",       [-1,90,0.4,0.4,15,250,0.05,3, 600,0.4,5000,200,0.3,0.15,0.5,0.2, 0.95,0.3,0.5,1,-2],0,5, "Huge stone-hall space with slow echoes for dramatic moments."),
 ("Dub Throw",       [0,120,0.3,0.5,8,160,0.4,1, 450,0.75,3500,300,0.4,0.2,0.8,0.5, 0.4,0.6,0.15,1,-1],   1,6, "Long dotted quarter feedback trails for dub style word throws."),
 ("Lo-Fi Cassette",  [0,150,0.2,0.6,12,180,0.65,-4, 330,0.5,2500,300,1.5,0.5,0.3,0.3, 0.25,0.9,0.1,1,0],  0,5, "Dusty, saturated and wobbly like an old four track."),
 ("Hip-Hop Ad-Lib",  [0,110,0.5,0.6,5,110,0.3,3, 250,0.3,6000,200,0.3,0.05,0.9,0.5, 0.3,0.5,0.1,1,0],     1,2, "Wide eighth note throws that make ad-libs jump out of the mix."),
 ("Neon Shimmer",    [0,100,0.4,0.4,10,160,0.15,7, 350,0.5,10000,250,3.0,0.4,0.7,0.3, 0.75,0.2,0.35,1,-1],0,5, "Glittering fast modulation and a bright, glassy reverb."),
 ("Wide Choir",      [0,90,0.4,0.5,10,170,0.25,4, 480,0.5,5500,180,0.9,0.4,1.0,0.35, 0.8,0.4,0.35,1,-1],  0,5, "Layered, swirling stereo repeats that sound like a stacked choir."),
]
assert len(PRESETS) == 20 and all(len(p[1]) == 21 for p in PRESETS)
