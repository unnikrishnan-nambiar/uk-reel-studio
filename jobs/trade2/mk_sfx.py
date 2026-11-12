# Synthesised SFX track for the TRADE reel (no samples needed). Cues are SOURCE times, mapped to body times.
import numpy as np, wave, os
SR = 48000
SEGS = [[0.58,4.34],[4.74,6.37],[6.86,15.63],[16.04,21.96],[22.45,25.47],[25.86,27.44],[28.10,34.44],[34.80,36.40],[36.75,39.24],[39.47,40.98],[41.38,45.29],[45.64,48.02],[48.45,52.61],[53.08,56.62],[57.36,58.49],[58.73,61.15]]
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
CUES = [0.58,3.06,4.74,6.86,8.32,9.80,10.82,12.40,13.58,16.17,19.17,22.45,24.17,25.86,28.10,31.78,33.16,36.75,38.0,39.47,41.38,45.64,48.45,53.08,55.60,57.36,58.73,60.05]
for c in CUES:
    put(c - 0.12, whoosh(), 0.55)
    put(c + 0.16, pop(950), 0.35)
put(0.58, boom(0.6), 0.5)                               # hard open
for i in range(11): put(14.0 + i * 0.1, tick(2600 + i * 90), 0.35)   # skill tiles light up
for k in range(4): put(16.32 + k * 0.08 + .05, pop(700 + k * 120), 0.3)  # team cards
for i in range(26): put(19.9 + i * 0.07 * (1 + i / 40), tick(3400), 0.22, pan=(-0.4 if i % 2 else 0.4))  # chart counter
put(22.6, ding(1320), 0.5); put(24.3, ding(990), 0.5)     # entry / exit
put(25.3, riser(0.56), 0.6); put(25.86, boom(), 0.7)     # time machine
for i in range(40): put(28.6 + i * 0.065, tick(2900), 0.18, pan=(-0.3 if i % 2 else 0.3))  # replay counter
put(31.85, ding(1760, 0.6), 0.35); put(33.25, down(0.6), 0.35)  # wins / losses
put(38.05, bell(), 0.55)                                  # stay alert
put(41.4, chime(), 0.45); put(41.6, ding(880, 0.5), 0.3)  # breaking news stinger
put(46.35, down(), 0.6); put(46.4, boom(0.9), 0.55)       # NVIDIA −8%
put(48.7, chime(), 0.5)                                   # Claude morning alert
for i in range(5): put(55.75 + i * 0.1, key(), 0.6)        # typing TRADE
put(56.3, pop(1200, 0.07), 0.45)
put(57.45, chime(), 0.4)                                  # DM arrives
put(59.22, pop(600, 0.06), 0.5); put(60.62, pop(600, 0.06), 0.5)   # follow / save taps
o = out[: int(DUR * SR)]; o = o / max(1e-6, np.abs(o).max()) * 0.7
D = os.path.dirname(os.path.abspath(__file__))
with wave.open(f'{D}/sfx.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype(np.int16).tobytes())
print('sfx', DUR)
