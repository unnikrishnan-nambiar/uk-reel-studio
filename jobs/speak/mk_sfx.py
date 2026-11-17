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
CUES = [0.88,7.27,15.27,21.19,25.32,28.10,31.58,34.28,39.48,47.40,48.31,55.54,59.88,62.04,69.46,71.23,79.46,81.75,91.23,98.74,100.14,103.50]
for c in CUES:
    put(c - 0.10, whoosh(), 0.5)
    put(c + 0.16, pop(950), 0.32)
for h in (0.88, 7.27, 15.27): put(h + 0.6, boom(0.6), 0.5)            # hook: 90% BETTER lands
put(23.9, down(0.7), 0.4)                                               # stuck ?!
put(25.9, ding(1320, 0.5), 0.4); put(27.2, down(0.6), 0.45)            # head ok / tongue no
put(28.75, tick(4200), 0.5); put(28.8, boom(0.4), 0.35)                # 1 hour class crossed
put(31.6, boom(0.8), 0.6)                                               # NO TUTOR
for i in range(14): put(34.4 + i * 0.16, key(), 0.5)                   # typing project name
put(43.95, riser(0.5), 0.35); put(45.0, ding(1568, 0.6), 0.4)          # prompt highlight
put(47.42, boom(0.6), 0.55)                                             # THAT'S IT
put(50.0, down(0.5), 0.45); put(51.9, ding(1760, 0.7), 0.5)            # mic no / voice yes
put(55.7, chime(), 0.4)                                                 # ChatGPT question
put(59.95, pop(1300, 0.07), 0.5)                                        # my line
put(64.9, tick(4200), 0.55); put(64.92, boom(0.5), 0.5)                # interrupt!
put(69.2, riser(0.5), 0.55); put(69.48, boom(), 0.65)                  # BEST PART
put(71.65, down(0.5), 0.45); put(72.05, ding(1568, 0.7), 0.55)         # go -> went
for i in range(12): put(79.5 + i * 0.16, tick(2600), 0.25)            # timer
put(82.0, chime(), 0.45)                                                # reminder bell
put(93.0, pop(1100, 0.06), 0.5); put(93.4, chime(), 0.45)              # toggle on + banner
put(98.76, boom(0.7), 0.55)                                             # EXPERIENCE
for i in range(5): put(100.6 + i * 0.12, key(), 0.6)                    # typing SPEAK
put(104.6, pop(600, 0.06), 0.5)                                         # send
o = out[: int(DUR * SR)]; o = o / max(1e-6, np.abs(o).max()) * 0.7
D = os.path.dirname(os.path.abspath(__file__))
with wave.open(f'{D}/sfx.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype(np.int16).tobytes())
