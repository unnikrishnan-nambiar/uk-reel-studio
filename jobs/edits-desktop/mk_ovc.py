import cv2, numpy as np, os, glob, sys
sys.path.insert(0, '/home/claude/uk-reel-studio/engine'); import grade
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('ovC', exist_ok=True)
for f in glob.glob('ovC/*.png'): os.remove(f)
L = [cv2.imread(f, -1).astype(np.float32) for f in sorted(glob.glob('logo/*.png'))]
W, H, FPS = 1080, 1920, 60
INTRO, MCP, CTA = (0.20, 1.90), (6.79, 10.56), (11.44, 17.64)
eo = lambda x: 1 - (1 - min(max(x, 0), 1)) ** 3
def rrect(w, h, r):
    m = np.zeros((h, w), np.uint8); cv2.rectangle(m, (r, 0), (w - r, h), 255, -1); cv2.rectangle(m, (0, r), (w, h - r), 255, -1)
    for cx, cy in [(r, r), (w - r, r), (r, h - r), (w - r, h - r)]: cv2.circle(m, (cx, cy), r, 255, -1, cv2.LINE_AA)
    return m.astype(np.float32) / 255
def paste(out, im, x0, y0, alpha=1.0):
    h, w = im.shape[:2]; a = im[..., 3:] / 255 * alpha; reg = out[y0:y0 + h, x0:x0 + w]
    reg[..., :3] = reg[..., :3] * (1 - a) + im[..., :3] * a; reg[..., 3:] = 255 * (a + reg[..., 3:] / 255 * (1 - a))
CW, CH = 760, 340; CARD = rrect(CW, CH, 44); CX, CY = 540, 420   # top card: above the laptop, inside the safe zone
def topcard(lg, k):
    img = np.zeros((CH, CW, 4), np.float32); img[..., :3] = 13; img[..., 3] = CARD * 235
    lgs = cv2.resize(lg, (560, 194)); paste(img, lgs, (CW - 560) // 2, 34)
    s = 0.85 + 0.15 * k; sw, sh = int(CW * s), int(CH * s); img = cv2.resize(img, (sw, sh)); img[..., 3] *= k
    return img, CX - sw // 2, CY - sh // 2
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
BG = (np.exp(-(((xx - 540) / 700) ** 2 + ((yy - 700) / 900) ** 2)) * 22 + 10)[..., None].repeat(3, 2)
# sharp laptop footage for the CTA part (the real shot there is a blurry pan + a monitor with other people's names)
need = {}
for n in range(int(round(CTA[0] * FPS)), int(round(CTA[1] * FPS))):
    need[n] = int(round((4.1 + (n / FPS - CTA[0]) * 0.85) * FPS))
cap = cv2.VideoCapture('src60.mp4'); CUR = [-1, None]
def getf(idx):
    while CUR[0] < idx:
        ok, f = cap.read(); CUR[0] += 1; CUR[1] = f
    return grade.grade(CUR[1], 0.3).astype(np.float32)
for n in range(int(round(INTRO[0] * FPS)), int(round(CTA[1] * FPS))):
    t = n / FPS; out = np.zeros((H, W, 4), np.float32)
    if INTRO[0] <= t < INTRO[1]:
        u = t - INTRO[0]; k = eo(u / 0.35) * min(1, (INTRO[1] - t) / 0.2)
        img, x0, y0 = topcard(L[min(int(u * 30), len(L) - 1)], k); paste(out, img, x0, y0)
    elif MCP[0] <= t < MCP[1]:
        u = t - MCP[0]; k = min(1, u / 0.15) * min(1, (MCP[1] - t) / 0.12)
        out[..., :3] = BG; out[..., 3] = 255 * k
        lg = L[0]; lgs = cv2.resize(lg, (770, 267)); paste(out, lgs, (W - 770) // 2, 300, eo(u / 0.4))   # still logo
    elif CTA[0] <= t < CTA[1]:
        u = t - CTA[0]
        fr = getf(need[n]); out[..., :3] = fr; out[..., 3] = 255 * min(1, u / 0.12)
        img, x0, y0 = topcard(L[min(int(u * 30), len(L) - 1)], eo(u / 0.35)); paste(out, img, x0, y0)
    else: continue
    cv2.imwrite(f'ovC/{n:05d}.png', np.clip(out, 0, 255).astype(np.uint8))
print('ovC', len(os.listdir('ovC')))
