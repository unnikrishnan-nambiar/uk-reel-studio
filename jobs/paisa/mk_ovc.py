# ovC: his real screen recordings, full screen (1080x1920). Personal figures in r2 are blurred.
import cv2, numpy as np, os, glob, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('ovC', exist_ok=True)
for f in glob.glob('ovC/*.png'): os.remove(f)
FPS = 60
def fit(img, y0):  # 1206x2622 -> 1080 wide, crop 1920 rows from y0 (scaled coords)
    s = cv2.resize(img, (1080, int(round(img.shape[0] * 1080 / img.shape[1]))), interpolation=cv2.INTER_AREA)
    return s[y0:y0 + 1920]
def grab(path, t):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', path, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    return cv2.imdecode(np.frombuffer(p.stdout, np.uint8), 1)
def seq(path, t0, t1, n):  # n frames evenly from t0..t1 via one decode
    d = t1 - t0
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', path, '-vf', f'setpts=PTS*{n / FPS / d:.6f},fps={FPS}',
                        '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True)
    W, H = 1206, 2622; a = np.frombuffer(p.stdout, np.uint8); k = len(a) // (W * H * 3)
    fr = a[:k * W * H * 3].reshape(k, H, W, 3)
    return [fr[min(i, k - 1)] for i in range(n)]
def write(b0, b1, frames):
    for i, n in enumerate(range(int(round(b0 * FPS)), int(round(b1 * FPS)))):
        cv2.imwrite(f'ovC/{n:05d}.png', frames[min(i, len(frames) - 1)])
# 1) r2 still: his financial baseline, every figure and category blurred
st = grab('rec/r2.mp4', 0.5).copy()
y0, y1 = 1300, 2310                               # table rows (full-res)
reg = st[y0:y1, 30:1180]; st[y0:y1, 30:1180] = cv2.GaussianBlur(cv2.resize(cv2.resize(reg, None, fx=.035, fy=.035), (reg.shape[1], reg.shape[0])), (0, 0), 16)
b0, b1 = 10.70, 12.90; N = int(round((b1 - b0) * FPS)); out = []
for i in range(N):
    z = 1 + 0.04 * i / N; s = cv2.resize(st, None, fx=z, fy=z); cy = int((s.shape[0] - st.shape[0]) / 2); cx = int((s.shape[1] - st.shape[1]) / 2)
    out.append(fit(s[cy:cy + st.shape[0], cx:cx + st.shape[1]], 250))
write(b0, b1, out)
# 2) r3: create the Finance project   3) r1: attach + prompt   4) r1: sent, ChatGPT replies
for path, t0, t1, b0, b1, y in [('rec/r3.mp4', 1.0, 11.0, 25.20, 28.90, 60), ('rec/r1.mp4', 20.0, 27.0, 28.90, 31.40, 150), ('rec/r1.mp4', 29.0, 35.0, 31.40, 33.11, 150)]:
    N = int(round((b1 - b0) * FPS)); write(b0, b1, [fit(f, y) for f in seq(path, t0, t1, N)])
print('ovC', len(os.listdir('ovC')))
