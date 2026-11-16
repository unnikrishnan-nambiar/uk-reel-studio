# Snippets from the wifi screen recording: crop, OCR-blur private words (neighbour SSIDs, company/Zscaler, username), upscale 2x.
import cv2, re, os, sys, subprocess, numpy as np, pytesseract
from pytesseract import Output
SRC = '/mnt/user-data/uploads/20261116-0319-49_0575988.mp4'
OUT = '/mnt/user-data/outputs/wifi-snippets/'; os.makedirs(OUT, exist_ok=True)
PAT = re.compile(r'(airtel|gudiya|jaden|kiara|shdr|zscaler|company|nambiar|cnamb|users\\|gmail)', re.I)
HOLD = {'5-neighbour-channels': 2.5}
CLIPS = [  # name, start, end, crop x1,y1,x2,y2 (full frame px)
    ('1-paste-prompt',        0.0,  6.0, (200, 80, 990, 430)),
    ('2-seven-steps',         6.0, 14.0, (70, 460, 990, 870)),
    ('3-plan-speed-62pct',   23.0, 30.0, (60, 170, 700, 800)),
    ('4-unknown-device',    103.2, 110.0, (60, 170, 700, 800)),
    ('5-neighbour-channels',134.9, 137.6, (60, 0, 980, 560)),
    ('6-asks-permission',   139.0, 146.0, (60, 250, 700, 830)),
    ('7-diagnosis-62mbps',  178.2, 181.6, (60, 0, 980, 720)),
]
EVERY = 3
def boxes(img):
    g = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    d = pytesseract.image_to_data(g, output_type=Output.DICT, config='--psm 3')
    out = []
    for i, t in enumerate(d['text']):
        t = (t or '').strip()
        if t and PAT.search(t):
            x, y, w, h = d['left'][i]//2, d['top'][i]//2, d['width'][i]//2, d['height'][i]//2
            out.append((x-8, y-6, x+w+8, y+h+6))
    return out
def blur(img, bs):
    H, W = img.shape[:2]
    for x1, y1, x2, y2 in bs:
        x1, y1, x2, y2 = max(0,x1), max(0,y1), min(W,x2), min(H,y2)
        if x2-x1 < 4 or y2-y1 < 4: continue
        r = img[y1:y2, x1:x2]; s = cv2.resize(r, (max(1,(x2-x1)//8), max(1,(y2-y1)//8)))
        img[y1:y2, x1:x2] = cv2.GaussianBlur(cv2.resize(s, (x2-x1, y2-y1)), (0,0), 3)
    return img
only = sys.argv[1:]
for name, a, b, (x1, y1, x2, y2) in CLIPS:
    if only and name not in only: continue
    cap = cv2.VideoCapture(SRC); cap.set(cv2.CAP_PROP_POS_MSEC, a*1000); fr = []
    while cap.get(cv2.CAP_PROP_POS_MSEC) < b*1000:
        ok, f = cap.read()
        if not ok: break
        fr.append(f[y1:y2, x1:x2].copy())
    cap.release()
    fr += [fr[-1].copy() for _ in range(int(HOLD.get(name, 0)*30))]
    n = len(fr); bx = {i: boxes(fr[i]) for i in list(range(0, n, EVERY)) + [n-1]}
    w, h = (x2-x1)//2*2, (y2-y1)//2*2
    ff = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{x2-x1}x{y2-y1}','-r','30','-i','-',
        '-vf',f'crop={w}:{h}:0:0,scale=iw*2:ih*2:flags=lanczos,format=yuv420p','-c:v','libx264','-crf','16','-preset','medium','-movflags','+faststart',OUT+name+'.mp4'], stdin=subprocess.PIPE)
    tot = 0
    for i, f in enumerate(fr):
        bs = sum((bx[k] for k in bx if abs(k-i) <= EVERY+1), [])
        tot += len(bs); ff.stdin.write(blur(f, bs).tobytes())
    ff.stdin.close(); ff.wait(); print(name, n, 'frames, boxes', tot, flush=True)
