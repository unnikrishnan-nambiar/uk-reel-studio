# Synthesised SFX track for the WIFI reel (TRADE style) (no samples needed). Cues are SOURCE times, mapped to body times.
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
CUES = [0.05,17.50,20.83,24.33,27.40,29.85,31.91,37.48,39.96,42.21,45.91,49.85,52.20,56.86,58.70,64.25,65.70,67.20,72.00,74.95,78.40,86.55,83.45,89.22]
for c in CUES:
    put(c - 0.10, whoosh(), 0.5)
    put(c + 0.16, pop(950), 0.32)
for h in (0.05,): put(h + 0.6, boom(0.6), 0.5)          # hook: 2X SPEED lands
for i in range(8): put(17.7 + i * 0.32, tick(2200), 0.25)            # lag spinner
for i in range(10): put(21.0 + i * 0.12, tick(3000), 0.2)            # download creeping
put(24.5, riser(0.7), 0.45); put(26.7, down(0.6), 0.45)               # router reset -> no change
put(29.95, pop(1300, 0.07), 0.5)                                       # message sent
put(33.0, pop(800, 0.08), 0.5)                                         # reply arrives
put(38.0, ding(1320), 0.5)                                             # upgraded tick
put(40.0, down(0.9), 0.5)                                              # still slow
for i in range(10): put(42.5 + i * 0.09, key(), 0.5)                   # paste prompt
for i in range(20): put(46.0 + i * 0.08, tick(2800), 0.2)             # gauge sweep
put(49.9, boom(0.8), 0.6); put(49.95, down(0.7), 0.4)                  # ONLY 40%
for i in range(4): put(58.9 + i * 0.35, pop(700 + i * 120), 0.3)     # apps appear
for i in range(4): put(64.4 + i * 0.25, pop(500, 0.06), 0.4)         # apps removed
put(65.2, riser(0.5), 0.55); put(65.72, boom(), 0.65)                 # BEST PART
put(69.2, boom(0.5), 0.4); put(69.25, tick(4200), 0.4)                 # clash zap
put(75.75, ding(1568, 0.7), 0.5)                                       # new channel
put(78.5, chime(), 0.45)                                               # asks permission
put(86.6, riser(0.6), 0.5); put(87.9, ding(1760, 0.8), 0.55)          # 40 -> 80
for i in range(4): put(83.9 + i * 0.12, key(), 0.6)                    # typing WIFI
put(90.2, pop(600, 0.06), 0.5); put(91.2, pop(600, 0.06), 0.5)        # follow / send
o = out[: int(DUR * SR)]; o = o / max(1e-6, np.abs(o).max()) * 0.7
D = os.path.dirname(os.path.abspath(__file__))
with wave.open(f'{D}/sfx.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype(np.int16).tobytes())
