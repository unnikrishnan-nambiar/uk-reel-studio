# Synthesised SFX track for the SPEAK reel (TRADE style) (no samples needed). Cues are SOURCE times, mapped to body times.
import numpy as np, wave, os
SR = 48000
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segs import ALL as SEGS
DUR = sum(e - a for a, e in SEGS)
def body(s):
    b = 0
    for a, e in SEGS:
        if a <= s <= e + 1e-6: return b + s - a
        b += e - a
    return None
rng = np.random.default_rng(7)
out = np.zeros((int(DUR * SR) + SR, 2), np.float32)
def env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r); return e
def put(s, x, g=1.0, pan=0.0):
    t = body(s)
    if t is None: return
    i = int(t * SR); x = x[: len(out) - i]
    out[i:i + len(x), 0] += x * g * (1 - max(0, pan)); out[i:i + len(x), 1] += x * g * (1 + min(0, pan))
def lp(x, k):  # cheap one-pole low-pass, k 0..1
    y = np.zeros_like(x); a = 0.0
    for i in range(len(x)): a += k * (x[i] - a); y[i] = a
    return y
def whoosh(d=0.35):
    n = int(d * SR); w = rng.standard_normal(n).astype(np.float32)
    t = np.linspace(0, 1, n); e = np.sin(np.pi * t) ** 2
    hi = w - lp(w, 0.08)
    return (hi * e * 0.5 + lp(w, 0.25) * e * 0.6) * 0.6
def pop(f0=900, d=0.09):
    n = int(d * SR); t = np.arange(n) / SR; f = f0 * np.exp(-t * 18)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.03)
def tick(f=3200):
    n = int(0.025 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * env(n, 0.0005, 0.006) + rng.standard_normal(n) * env(n, 0.0005, 0.003) * 0.3) * 0.6
def ding(f=1320, d=0.9):
    n = int(d * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * m * t) * a for m, a in [(1, 1), (2.01, .35), (3.0, .15)]) * env(n, 0.002, 0.28) * 0.5
def boom(d=0.8):
    n = int(d * SR); t = np.arange(n) / SR; f = 90 * np.exp(-t * 4) + 38
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.3) + lp(rng.standard_normal(n).astype(np.float32), 0.05) * env(n, 0.001, 0.08) * 0.8) * 0.9
def riser(d=0.6):
    n = int(d * SR); t = np.linspace(0, 1, n); w = rng.standard_normal(n).astype(np.float32)
    f = 200 + 1400 * t ** 2
    return (w - lp(w, 0.1 + 0.3 * float(0))) * t ** 2 * 0.25 + np.sin(2 * np.pi * np.cumsum(f) / SR) * t ** 2 * 0.25
def down(d=0.9):
    n = int(d * SR); t = np.arange(n) / SR; f = 700 * np.exp(-t * 2.2) + 80
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.5) * 0.45
def chime():
    return np.concatenate([ding(1568, 0.18)[: int(.12 * SR)], ding(2093, 0.7)]) * 0.8
def bell():
    n = int(1.4 * SR); t = np.arange(n) / SR; tr = 1 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t))
    return sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1250, 1), (2830, .4), (4100, .2)]) * env(n, 0.002, 0.45) * tr * 0.28
def key():
    n = int(0.04 * SR); return lp(rng.standard_normal(n).astype(np.float32), 0.5) * env(n, 0.0005, 0.008) * 0.9
# ---- cues (source times) ----
CUES=[0.06,4.48,9.02,13.69,20.33,24.14,28.79,34.41,36.84,40.40,41.92,44.14,47.0,49.56,50.95,54.08,56.79,60.09,63.34,70.55,71.65,76.05,89.65,91.30,93.55,98.11,100.39,101.05]
for c in CUES:
    put(c - 0.10, whoosh(), 0.5)
    put(c + 0.16, pop(950), 0.32)
for h in (0.06, 4.48, 9.02): put(h + 0.6, boom(0.6), 0.5)            # hook lands
for t in (16.6,17.0,17.4,17.8,18.2): put(t, pop(1200,0.06), 0.4)      # detail chips
put(18.9, ding(1568,0.6), 0.45)
for i in range(20): put(20.5 + i * 0.16, key(), 0.45)                 # slow typing
for i in range(3): put(26.3 + i*0.45, tick(4200), 0.5)                # details cut
put(32.8, pop(700,0.08), 0.5); put(32.85, chime(), 0.35)              # mail sent
put(34.5, down(0.7), 0.5)                                              # OOPS forgot
put(36.9, ding(1320,0.5), 0.4); put(38.1, down(0.6), 0.45)             # head ok / prompt no
put(40.5, boom(0.5), 0.45)                                             # blame AI
put(47.0, boom(0.6), 0.55)                                             # MY FAULT
put(51.8, riser(0.5), 0.4); put(52.2, ding(1760,0.8), 0.5)             # Flow logo
put(54.9, pop(1300,0.07), 0.5)                                         # free option
put(57.6, tick(4200), 0.5); put(58.4, ding(1568,0.6), 0.45)            # keyboard x / mic
put(60.7, riser(0.7), 0.4); put(61.0, boom(0.5), 0.5)                  # 4X
for i in range(20): put(65.3 + i*0.17, key(), 0.25)                    # text flowing
put(69.57, ding(1760,0.6), 0.45)                                       # nothing missed
put(70.15, riser(0.45), 0.6); put(70.55, boom(1.0), 0.8); put(70.6, chime(), 0.5)   # BEST PART
for i in range(12): put(72.4 + i*0.13, pop(1400+i*40,0.05), 0.35)     # punctuation pops
put(80.34, pop(1000,0.06), 0.4); put(80.86, pop(1100,0.06), 0.4); put(82.16, pop(800,0.06), 0.45)
put(84.6, down(0.5), 0.5); put(85.0, whoosh(0.3), 0.6)                 # Rahul removed, prompt shrinks
put(85.4, boom(0.6), 0.6); put(85.45, ding(1568,0.7), 0.55)            # FIXED ITSELF
put(88.0, chime(), 0.45)                                               # sent
put(89.7, boom(0.7), 0.55)                                             # NEXT GEN TECH
for i in range(4): put(91.75 + i * 0.12, key(), 0.6)                   # typing TYPE
for t in (93.7,94.9,96.4): put(t, pop(1200,0.06), 0.45)               # DM ticks
put(99.2, pop(600, 0.06), 0.5)                                         # send
put(101.1, boom(0.6), 0.5)                                             # 1 step ahead
o = out[: int(DUR * SR)]; o = o / max(1e-6, np.abs(o).max()) * 0.7
D = os.path.dirname(os.path.abspath(__file__))
with wave.open(f'{D}/sfx.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype(np.int16).tobytes())
