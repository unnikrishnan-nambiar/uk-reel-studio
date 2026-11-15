# Short screen clips from the test recording: crop, OCR-blur personal data on every frame (+ neighbours), upscale 2x.
import cv2, re, os, sys, subprocess, numpy as np, pytesseract
from pytesseract import Output
D = '/home/claude/uk-reel-studio/jobs/hof/'
SRC = '/mnt/user-data/uploads/Recording_2026-11-14_163950.mp4'
OUT = '/mnt/user-data/outputs/hof-clips/'; os.makedirs(OUT, exist_ok=True)
PW = [w.strip() for w in open(D + 'stills/private_words.txt') if w.strip()]
PAT = re.compile(r'(' + '|'.join([re.escape(w) for w in PW] + [r'gmail', r'@', r'\d{5,}', r'\.b\.', r'nambiar\.', r'\+91']) + ')', re.I)
# name, start, end, crop (x1,y1,x2,y2) in full-frame px
CLIPS = [
    ('1-his-guide', 0.0, 9.0, (480, 60, 1440, 1032)),
    ('2-my-prompt', 60.0, 72.0, (700, 60, 1500, 1032)),
    ('3-claude-searching', 72.0, 98.0, (700, 60, 1500, 1032)),
    ('4-result-me', 100.0, 146.0, (700, 60, 1500, 1032)),
    ('5-friend-prompt-permission', 150.0, 200.0, (700, 60, 1500, 1032)),
    ('6-result-friend', 205.0, 238.0, (700, 60, 1500, 1032)),
    ('7-india-steps-his-guide', 240.0, 262.0, (480, 60, 1440, 1032)),
]
OCR_EVERY = 3     # OCR every 3rd frame (10/s) and apply boxes to neighbours
def boxes_for(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); g = cv2.resize(g, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    d = pytesseract.image_to_data(g, output_type=Output.DICT, config='--psm 3')
    out = []
    for i, t in enumerate(d['text']):
        t = (t or '').strip()
        if t and PAT.search(t):
            x, y, w, h = d['left'][i] // 2, d['top'][i] // 2, d['width'][i] // 2, d['height'][i] // 2
            out.append((x - 8, y - 6, x + w + 8, y + h + 6))
    return out
def blur(img, bs):
    H, W = img.shape[:2]
    for x1, y1, x2, y2 in bs:
        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(W, x2), min(H, y2)
        if x2 - x1 < 4 or y2 - y1 < 4: continue
        roi = img[y1:y2, x1:x2]; sm = cv2.resize(roi, (max(1, (x2 - x1) // 8), max(1, (y2 - y1) // 8)))
        img[y1:y2, x1:x2] = cv2.GaussianBlur(cv2.resize(sm, (x2 - x1, y2 - y1)), (0, 0), 3)
    return img
only = sys.argv[1:] or None
for name, a, b, (cx1, cy1, cx2, cy2) in CLIPS:
    if only and name not in only: continue
    cap = cv2.VideoCapture(SRC); cap.set(cv2.CAP_PROP_POS_MSEC, a * 1000)
    frames = []
    while cap.get(cv2.CAP_PROP_POS_MSEC) < b * 1000:
        ok, fr = cap.read()
        if not ok: break
        frames.append(fr[cy1:cy2, cx1:cx2].copy())
    cap.release()
    n = len(frames); bx = [None] * n
    for i in range(0, n, OCR_EVERY): bx[i] = boxes_for(frames[i])
    if bx[n - 1] is None: bx[n - 1] = boxes_for(frames[n - 1])
    keys = [i for i in range(n) if bx[i] is not None]
    w, h = cx2 - cx1, cy2 - cy1
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '30', '-i', '-',
                           '-vf', 'scale=iw*2:ih*2:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
                           '-movflags', '+faststart', OUT + name + '.mp4'], stdin=subprocess.PIPE)
    tot = 0
    for i, fr in enumerate(frames):
        near = [k for k in keys if abs(k - i) <= OCR_EVERY + 1]   # boxes from neighbouring OCR frames cover scrolling
        bs = [b_ for k in near for b_ in bx[k]]; tot += len(bs)
        ff.stdin.write(blur(fr, bs).tobytes())
    ff.stdin.close(); ff.wait(); print(name, n, 'frames, blur boxes', tot, flush=True)
