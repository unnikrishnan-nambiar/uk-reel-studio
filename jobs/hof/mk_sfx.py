# Simple template SFX: whoosh on card/scene changes, pop on quote cards, swish on India cards, stamp on verdict.
import json, numpy as np, soundfile as sf
SR = 48000; TL = json.load(open('timeline.json')); N = int((TL['dur'] + 1) * SR); out = np.zeros(N, np.float32)
rng = np.random.default_rng(3)
def add(t, x, g=1.0):
    i = int(t * SR); j = min(N, i + len(x)); out[i:j] += g * x[:j - i]
def env(n, a=0.01, r=None):
    e = np.ones(n); k = int(a * SR); e[:k] = np.linspace(0, 1, k); e *= np.exp(-np.linspace(0, r or 4, n)); return e
def whoosh(d=0.35):
    n = int(d * SR); w = rng.standard_normal(n); f = np.cumsum(w); f -= np.convolve(f, np.ones(200) / 200, 'same')
    return (f / np.abs(f).max() * np.sin(np.linspace(0, np.pi, n)) ** 2).astype(np.float32)
def pop(f=900, d=0.09):
    n = int(d * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t * (1 - t * 3)) * env(n, 0.002, 7)).astype(np.float32)
def stamp():
    n = int(0.6 * SR); t = np.arange(n) / SR
    thump = np.sin(2 * np.pi * (90 - 40 * t) * t) * np.exp(-t * 9)
    hit = rng.standard_normal(n) * np.exp(-t * 30) * 0.5
    return (thump + hit).astype(np.float32)
def ding(f=1320):
    n = int(0.5 * SR); t = np.arange(n) / SR; return ((np.sin(2*np.pi*f*t) + .4*np.sin(2*np.pi*2*f*t)) * np.exp(-t * 7)).astype(np.float32)
S = TL['segs']
add(0.05, stamp(), 0.5); add(0.15, pop(700), 0.5)               # heading drops in
for g in S:
    if g['layout'] == 'split': add(max(0, g['t0'] - 0.05), whoosh(), 0.35); add(g['t0'] + 0.7, pop(1000), 0.35)
    if g['scene'] == 'go': add(g['t0'], whoosh(0.5), 0.45); add(g['t0'] + 0.1, pop(600), 0.5)
seg = {g['scene']: g for g in S}
for sc, src in [('india', 106.4), ('india', 116.6), ('india2', 123.7), ('india2', 126.5)]:
    g = seg[sc]; add(g['t0'] + src - g['a'] - 0.15, whoosh(0.3), 0.4)
v = seg['verdict']['t0'] + 1.3; add(v, stamp(), 0.9); add(v + 0.12, ding(), 0.35)
out = np.tanh(out * 1.2) * 0.8; sf.write('sfx.wav', np.stack([out, out], 1), SR); print('sfx ok')
