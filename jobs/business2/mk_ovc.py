# ovC: his real screen recordings, full screen (1080x1920). DNS TXT verification value is blurred.
import cv2, numpy as np, os, glob, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('ovC', exist_ok=True)
for f in glob.glob('ovC/*.png'): os.remove(f)
FPS = 60
def fit(img, y0):
    s = cv2.resize(img, (1080, int(round(img.shape[0] * 1080 / img.shape[1]))), interpolation=cv2.INTER_AREA)
    return s[y0:y0 + 1920]
def seq(path, t0, t1, n):
    d = t1 - t0
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', path, '-vf', f'setpts=PTS*{n / FPS / d:.6f},fps={FPS}',
                        '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    return p
def land(f):  # OpenAI's landscape demo: crop the middle, scale to width, sit it on a white card
    c = cv2.resize(f[:, 500:2122], (1080, int(round(1206 * 1080 / 1622))), interpolation=cv2.INTER_AREA)
    o = np.full((1920, 1080, 3), 250, np.uint8); o[450:450 + c.shape[0]] = c; return o
def blur_txt(f):
    f = f.copy(); r = f[1620:1920, 60:1150]
    f[1620:1920, 60:1150] = cv2.GaussianBlur(cv2.resize(cv2.resize(r, None, fx=.04, fy=.04), (r.shape[1], r.shape[0])), (0, 0), 14); return f
def write(b0, b1, frames):
    for i, n in enumerate(range(int(round(b0 * FPS)), int(round(b1 * FPS)))):
        cv2.imwrite(f'ovC/{n:05d}.png', frames[min(i, len(frames) - 1)])
# body time ranges <- source recording ranges
for path, t0, t1, b0, b1, y, fx in [
    ('rec/r1.mp4', 2.0, 9.6, 5.77, 7.50, 40, None),      # asks ChatGPT: best interior designer in Malappuram
    ('rec/r1.mp4', 13.5, 20.5, 7.50, 9.30, 40, None),    # searching -> answer
    ('rec/r1.mp4', 22.5, 33.5, 9.30, 11.14, 40, None),   # the list ChatGPT recommends
    ('../business/rec/r2.mp4', 34.0, 38.0, 18.87, 20.70, 120, None),  # business hub: Add your business to ChatGPT
    ('../business/rec/r2.mp4', 71.0, 74.5, 20.70, 22.41, 120, blur_txt),  # verify (TXT value blurred)
    ('rec/r2.mp4', 26.9, 30.2, 22.41, 26.48, 'L', None),  # OpenAI demo: dashboard
    ('rec/r2.mp4', 14.0, 16.6, 29.80, 32.30, 'L', None)]:  # verify
    N = int(round((b1 - b0) * FPS)); p = seq(path, t0, t1, N); W, H = (2622, 1206) if y == 'L' else (1206, 2622); last = None
    for i, n in enumerate(range(int(round(b0 * FPS)), int(round(b1 * FPS)))):
        b = p.stdout.read(W * H * 3)
        if len(b) == W * H * 3:
            f = np.frombuffer(b, np.uint8).reshape(H, W, 3); last = land(f) if y == 'L' else fit(fx(f) if fx else f, y)
        cv2.imwrite(f'ovC/{n:05d}.png', last)
    p.stdout.close(); p.wait()
print('ovC', len(os.listdir('ovC')))
