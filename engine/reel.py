#!/usr/bin/env python3
"""uk-reel-studio pipeline. One job folder per reel: jobs/<name>/job.json + overlay.html.

  python3 engine/reel.py prep   input/<video> jobs/<name>   # 60fps source, transcript, silences, contact sheet
  python3 engine/reel.py cut    jobs/<name>                 # body cut from job.json body_segs
  python3 engine/reel.py masks  jobs/<name>                 # ISNet person masks for panel ranges
  python3 engine/reel.py overlay jobs/<name> [P|T|C]        # render overlay passes (resumable)
  python3 engine/reel.py test   jobs/<name> 2.0,9.5,24      # contact sheet of composite at body times
  python3 engine/reel.py comp   jobs/<name>                 # composite body video + audio
  python3 engine/reel.py hook   jobs/<name>                 # static outlined hook clip
  python3 engine/reel.py join   jobs/<name>                 # hook + body -> output/<name>.mp4 (+ share copy)
  python3 engine/reel.py all    jobs/<name>                 # cut, masks, overlay, comp, hook, join
  python3 engine/reel.py score  "hook text"                 # hook score (target >= 90)
"""
import sys, os, json, subprocess, shutil, glob, math
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
W, H, FPS = 1080, 1920, 60
WORKERS = int(os.environ.get('REEL_WORKERS', '2'))

def sh(cmd, **k):
    print('+', cmd if isinstance(cmd, str) else ' '.join(cmd), flush=True)
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, **k)

def load(job):
    j = json.load(open(os.path.join(job, 'job.json')))
    j['_dir'] = os.path.abspath(job); return j

def seg_map(j):
    out, o = [], 0.0
    for a, b in j['body_segs']:
        out.append(dict(src0=a, src1=b, out0=o, out1=o + b - a)); o += b - a
    return out, o

def src2body(j, s):
    segs, _ = seg_map(j)
    for g in segs:
        if g['src0'] - 0.06 <= s <= g['src1'] + 0.06:
            return round(max(g['out0'], s - g['src0'] + g['out0']), 3)
    raise SystemExit(f'caption time {s} is not inside any body segment')

def captions(j):
    """job caps: [[src_time, "text {KEY}"], ...] in SOURCE time -> [[t0,t1,text]] body time."""
    segs, dur = seg_map(j); C = j.get('caps', []); out = []
    for i, (s, tx) in enumerate(C):
        t0 = src2body(j, s); t1 = src2body(j, C[i + 1][0]) if i + 1 < len(C) else dur
        for g in segs:
            if g['out0'] <= t0 < g['out1']: t1 = min(t1, g['out1'] + 0.05)
        out.append([t0, t1, tx])
    return out

# ---------------------------------------------------------------- prep
def prep(video, job):
    os.makedirs(job, exist_ok=True); D = os.path.abspath(job)
    sh(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=60,format=yuv420p',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-c:a', 'aac', '-b:a', '256k', f'{D}/src60.mp4'])
    sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/src60.mp4', '-ac', '1', '-ar', '16000', f'{D}/a16.wav'])
    r = subprocess.run(['ffmpeg', '-i', f'{D}/a16.wav', '-af', 'silencedetect=n=-32dB:d=0.25', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', r)]; en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', r)]
    sil = [[a, b] for a, b in zip(st, en)]; json.dump(sil, open(f'{D}/silences.json', 'w'))
    sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/src60.mp4', '-vf', 'fps=0.5,scale=216:384,tile=11x2', '-frames:v', '1', f'{D}/sheet.jpg'])
    sh([sys.executable, os.path.join(ROOT, 'engine', 'transcribe.py'), f'{D}/a16.wav', f'{D}/words.json'])
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{D}/src60.mp4'], capture_output=True, text=True).stdout)
    print('\nDuration', round(dur, 2), 's\nSilences (>0.25s):', ' '.join(f'{a:.2f}-{b:.2f}' for a, b in sil))
    speech, last = [], 0.0
    for a, b in sil + [[dur, dur]]:
        if a - last > 0.2: speech.append([round(max(0, last - 0.06), 2), round(min(dur, a + 0.06), 2)])
        last = b
    print('Speech segments (suggested body_segs / hook):', json.dumps(speech))
    print(f'Contact sheet: {D}/sheet.jpg')

# ---------------------------------------------------------------- cut
def cut(j):
    D = j['_dir']; S = j['body_segs']
    sel = '+'.join(f'between(t,{a},{b})' for a, b in S)
    sh(f"ffmpeg -v error -y -i {D}/src60.mp4 -vf \"select='{sel}',setpts=N/60/TB\" -af \"aselect='{sel}',asetpts=N/SR/TB\" -r 60 -c:v libx264 -preset veryfast -crf 12 -c:a pcm_s16le {D}/cut60.mov")
    sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/cut60.mov', '-an', '-c:v', 'copy', f'{D}/cut60.mp4'])
    sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/cut60.mov', '-vn', f'{D}/body.wav'])
    segs, dur = seg_map(j); json.dump(dict(segs=segs, dur=dur), open(f'{D}/edit.json', 'w'), indent=1)
    json.dump(captions(j), open(f'{D}/caps_body.json', 'w'))
    print('body duration', round(dur, 2))

# ---------------------------------------------------------------- masks
def masks(j, k=None, m=None):
    D = j['_dir']
    if k is None:
        ps = [subprocess.Popen([sys.executable, __file__, 'masks', D, str(i), str(WORKERS)]) for i in range(WORKERS)]
        for p in ps: p.wait()
        return
    import onnxruntime as ort, cv2
    os.makedirs(f'{D}/pm2', exist_ok=True)
    o = ort.SessionOptions(); o.intra_op_num_threads = 2
    S = ort.InferenceSession(os.path.join(ROOT, 'models', 'isnet-general-use.onnx'), o, providers=['CPUExecutionProvider'])
    R = j['panel_ranges']; _, dur = seg_map(j)
    st = j.get('mask_step', 1)
    need = [n for n in range(int(dur * 30) + 1) if n % st == 0 and any(a <= n / 30 <= b for a, b in R)]
    ns = set(n for i, n in enumerate(need) if i % m == k)
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', f'{D}/cut60.mp4', '-vf', 'fps=30', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    Y0, Y1 = j.get('mask_rows', [0, 1400]); i = 0
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        if i in ns and not os.path.exists(f'{D}/pm2/{i:04d}.png'):
            img = np.frombuffer(b, np.uint8).reshape(H, W, 3); crop = img[Y0:Y1]
            x = cv2.resize(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB), (1024, 1024)).astype(np.float32) / 255 - 0.5
            mm = S.run(None, {S.get_inputs()[0].name: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
            mm = (mm - mm.min()) / (mm.max() - mm.min() + 1e-6)
            full = np.zeros((H, W), np.float32); full[Y0:Y1] = cv2.resize(mm, (W, Y1 - Y0))
            cv2.imwrite(f'{D}/pm2/{i:04d}.png', (full * 255).astype(np.uint8))
        i += 1
    print('masks worker', k, 'done', len(ns))

# ---------------------------------------------------------------- overlay
def card_at(j, t):
    for c in j.get('cards', []):
        if c['t0'] <= t < c['t1']:
            return c['scene'], min(c.get('s1', 99), c.get('s0', 0) + (t - c['t0']) * c.get('speed', 1.0)), c.get('scale', 0.85)
    return None, None, None

def overlay(j, mode=None, k=None, m=None, only=None):
    D = j['_dir']; _, dur = seg_map(j); NF = int(dur * FPS)
    if mode is None:
        for md in ('P', 'T', 'B', 'C'):
            for _ in range(2):  # second round fills frames a crashed worker skipped
                ps = [subprocess.Popen([sys.executable, __file__, 'overlay', D, md, str(i), str(WORKERS)]) for i in range(WORKERS)]
                for p in ps: p.wait()
        return
    from playwright.sync_api import sync_playwright
    out = f'{D}/ov{mode}'; os.makedirs(out, exist_ok=True)
    caps = json.load(open(f'{D}/caps_body.json')); theme = j.get('theme', 'white')
    frames = only if only is not None else [n for n in range(NF) if n % m == k]
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--allow-file-access-from-files']); pg = b.new_page(viewport={'width': W, 'height': H})
        pg.on('pageerror', lambda e: print('PAGE ERROR', e))
        if mode != 'C':
            pg.goto(f'file://{D}/overlay.html?pass={mode}&theme={theme}'); pg.evaluate('c=>setCaps(c)', caps)
            pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        cur = None
        for n in frames:
            f = f'{out}/{n:05d}.png'
            if only is None and os.path.exists(f): continue
            t = n / FPS
            if mode == 'C':
                s, st, sc = card_at(j, t)
                if s is None: continue
                if s != cur:
                    pg.goto(f'file://{ROOT}/templates/scenes/scenes.html?s={s}&k={sc}&theme={theme}'); pg.wait_for_timeout(400); cur = s
                pg.evaluate(f'frame({st})'); pg.screenshot(path=f)
            else:
                pg.evaluate(f'frame({t})'); pg.screenshot(path=f, omit_background=True)
        b.close()

# ---------------------------------------------------------------- composite
def comp(j, test_times=None):
    import cv2, grade, hdr
    D = j['_dir']; os.chdir(D); _, dur = seg_map(j); N = int(dur * FPS)
    TR = j['tr']; KS, YO, PB = j.get('ks', 0.72), j['yo'], j.get('pb', 1000)
    def z_at(t):
        z = 0.0
        for a, b, f, to in TR:
            if t >= b: z = to
            elif t >= a:
                u = (t - a) / (b - a); u = 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2
                return f + (to - f) * u
        return z
    def rgba(p):
        if not os.path.exists(p): return None
        o = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        if o is None: return None
        if o.shape[2] < 4: return (hdr.sdr2hlg(o) if hdr.ON else o.astype(np.float32)), np.ones(o.shape[:2] + (1,), np.float32)
        if o[:, :, 3].max() == 0: return None
        c = o[:, :, :3]
        return (hdr.sdr2hlg(c) if hdr.ON else c.astype(np.float32)), o[:, :, 3:4].astype(np.float32) / 255
    def over(base, r, shift=0):
        if r is None: return base
        c, a = r
        if shift:
            c = np.roll(c, shift, 0); a = np.roll(a, shift, 0)
            if shift < 0: a[shift:] = 0
        return base * (1 - a) + c * a
    xx = np.arange(W, dtype=np.float32); LASTP = [None]
    pf = None
    for n in range(N):
        if os.path.exists(f'ovP/{n:05d}.png'):
            o = cv2.imread(f'ovP/{n:05d}.png', -1)
            if o is not None and o.shape[2] == 4 and o[990, 540, 3] > 250: pf = o; break
    PAPER = np.repeat((pf[990, :, :3] if pf is not None else np.full((W, 3), 238, np.uint8)).astype(np.float32)[None], H, 0)
    if hdr.ON: PAPER = hdr.sdr2hlg(PAPER)
    frames = [int(round(t * FPS)) for t in test_times] if test_times else list(range(N))
    want = set(frames); tiles = []
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'cut60.mp4', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    enc = None if test_times else subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', 'body_v.mp4'], stdin=subprocess.PIPE)
    n = 0
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        if n in want:
            t = n / FPS
            src = grade.grade(np.frombuffer(b, np.uint8).reshape(H, W, 3), j.get('grade', 0.3)).astype(np.float32)
            z = z_at(t)
            if z <= 0.001:
                img = src; m = None; BB = j.get('bg_blur', 0)
                rb = rgba(f'ovB/{n:05d}.png')  # optional 'behind the person' layer (full face only)
                if rb is not None or BB:
                    mi = int(round(t * 30)); mp = None
                    for d in (0, 1, -1, 2, -2, 3, -3):
                        if os.path.exists(f'pm2/{mi + d:04d}.png'): mp = f'pm2/{mi + d:04d}.png'; break
                    if mp:
                        m = cv2.imread(mp, 0).astype(np.float32) / 255
                        m = cv2.GaussianBlur(np.clip((m - 0.08) / 0.8, 0, 1), (0, 0), 0.9)[:, :, None]
                if BB and m is not None:  # cinematic: soft, slightly darker background behind the person
                    sm = cv2.resize(src, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
                    bg = cv2.resize(cv2.GaussianBlur(sm, (0, 0), BB / 4), (W, H), interpolation=cv2.INTER_LINEAR) * j.get('bg_dim', 0.9)
                    img = src * m + bg * (1 - m)
                if rb is not None:
                    img = over(img, rb)
                    if m is not None: img = img * (1 - m) + src * m
            else:
                k = 1 - (1 - KS) * z; yo = YO * z
                sw, shh = int(round(W * k)), int(round(H * k)); x0 = (W - sw) / 2
                M = np.float32([[k, 0, x0], [0, k, yo]])
                vid = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_AREA if k < 1 else cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                pbv = int(PB * z); top = max(int(yo), pbv); bot = min(int(yo + shh), H - 36); R = 44
                rr = np.zeros((H, W), np.uint8)
                cv2.rectangle(rr, (int(x0) + R, top), (int(x0 + sw) - R, bot), 255, -1); cv2.rectangle(rr, (int(x0), top + R), (int(x0 + sw), bot - R), 255, -1)
                for cx, cy in [(int(x0) + R, top + R), (int(x0 + sw) - R, top + R), (int(x0) + R, bot - R), (int(x0 + sw) - R, bot - R)]:
                    cv2.circle(rr, (cx, cy), R, 255, -1, cv2.LINE_AA)
                ex = cv2.GaussianBlur(rr.astype(np.float32) / 255, (0, 0), 1.2)[:, :, None]
                img = PAPER * (1 - ex) + vid * ex
                pb = int(PB * z)
                rp = rgba(f'ovP/{n:05d}.png')
                if rp is None: rp = LASTP[0]
                else: LASTP[0] = rp
                img = over(img, rp, shift=pb - PB)
                mi = int(round(t * 30)); mp = f'pm2/{mi:04d}.png'
                if not os.path.exists(mp):
                    for d in (1, -1, 2, -2, 3, -3):
                        if os.path.exists(f'pm2/{mi + d:04d}.png'): mp = f'pm2/{mi + d:04d}.png'; break
                if os.path.exists(mp) and pb > 0:
                    m = cv2.imread(mp, 0).astype(np.float32) / 255
                    m = np.clip((m - 0.08) / 0.8, 0, 1); m = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR); m = cv2.GaussianBlur(m, (0, 0), 0.7)
                    band = np.zeros((H, 1), np.float32); lo = max(0, pb - 110)
                    if pb > lo: band[lo:pb] = np.linspace(0, 1, pb - lo)[:, None] ** 0.3
                    band[pb:bot] = 1
                    exs = np.clip(np.minimum(xx - x0, x0 + sw - xx) / 2, 0, 1)[None, :, None]
                    m = (m * band)[:, :, None] * exs
                    dec_ = vid.copy(); dec_[:pb] = vid[:pb] * (0.35 + 0.65 * np.clip(m[:pb] * 1.4, 0, 1))
                    img = img * (1 - m) + dec_ * m
            img = over(img, rgba(f'ovC/{n:05d}.png'))
            img = over(img, rgba(f'ovT/{n:05d}.png'))
            o = np.clip(img + 0.5, 0, 255).astype(np.uint8)
            if enc: enc.stdin.write(o.tobytes())
            else: tiles.append(cv2.resize(o, (270, 480)))
            if enc and n % 300 == 0: print('frame', n, '/', N, flush=True)
        n += 1
        if test_times and n > max(frames): break
    if enc:
        enc.stdin.close(); enc.wait()
        sh(['ffmpeg', '-v', 'error', '-y', '-i', 'body.wav', '-af', 'highpass=f=70,acompressor=threshold=-24dB:ratio=2.2:attack=8:release=140,loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '48000', '-ac', '2', 'body_a.wav'])
        sh(['ffmpeg', '-v', 'error', '-y', '-i', 'body_v.mp4', '-i', 'body_a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', 'body.mp4'])
    else:
        dec.kill()
        rows = [np.hstack(tiles[i:i + 6] + [np.zeros_like(tiles[0])] * (6 - len(tiles[i:i + 6]))) for i in range(0, len(tiles), 6)]
        cv2.imwrite('test.jpg', np.vstack(rows)); print('wrote', os.path.join(D, 'test.jpg'))

# ---------------------------------------------------------------- hook
def hook(j):
    import cv2, grade
    from playwright.sync_api import sync_playwright
    D = j['_dir']; c = dict(j['hook']); HD = f'{D}/hook'; shutil.rmtree(HD, ignore_errors=True); os.makedirs(HD + '/ov')
    dur = c['b'] - c['a']
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(c['a']), '-t', f'{dur:.3f}', '-i', f'{D}/src60.mp4', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '60', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', HD + '/g.mp4'], stdin=subprocess.PIPE)
    N = 0
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        enc.stdin.write(grade.grade(np.frombuffer(b, np.uint8).reshape(H, W, 3), j.get('grade', 0.3)).tobytes()); N += 1
    enc.stdin.close(); enc.wait()
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': W, 'height': H})
        pg.goto(f'file://{ROOT}/templates/hook.html'); pg.evaluate('c=>setup(c)', c)
        for i in range(N):
            pg.evaluate(f'frame({i / 60})'); pg.screenshot(path=f'{HD}/ov/{i:05d}.png', omit_background=True)
        if c.get('fx'):  # optional per-job animation layer, drawn UNDER the hook box
            pg.goto(f"file://{D}/{c['fx']}")
            for i in range(N):
                pg.evaluate(f'frame({i / 60})'); fx = cv2.imdecode(np.frombuffer(pg.screenshot(omit_background=True), np.uint8), -1).astype(np.float32)
                ov = cv2.imread(f'{HD}/ov/{i:05d}.png', -1).astype(np.float32); ao = ov[:, :, 3:] / 255; af = fx[:, :, 3:] / 255
                aout = ao + af * (1 - ao); rgb = (ov[:, :, :3] * ao + fx[:, :, :3] * af * (1 - ao)) / np.maximum(aout, 1e-4)
                cv2.imwrite(f'{HD}/ov/{i:05d}.png', np.dstack([rgb, aout * 255]).clip(0, 255).astype(np.uint8))
        br.close()
    import hdr
    if hdr.ON:
        for i in range(N):
            o = cv2.imread(f'{HD}/ov/{i:05d}.png', -1); o[:, :, :3] = np.clip(hdr.sdr2hlg(o[:, :, :3]) + 0.5, 0, 255).astype(np.uint8)
            cv2.imwrite(f'{HD}/ov/{i:05d}.png', o)
    sh(['ffmpeg', '-v', 'error', '-y', '-i', HD + '/g.mp4', '-framerate', '60', '-i', HD + '/ov/%05d.png', '-filter_complex',
        f"[0:v]scale='trunc(1080*(1+0.04*t/{dur:.3f})/2)*2':'trunc(1920*(1+0.04*t/{dur:.3f})/2)*2':eval=frame,crop=1080:1920,setsar=1[z];[z][1:v]overlay=format=auto,format=yuv420p[v]",
        '-map', '[v]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-r', '60', '-an', HD + '/v.mp4'])
    sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['a']), '-t', f'{N / 60:.4f}', '-i', f'{D}/src60.mp4', '-vn', '-ac', '2', '-ar', '48000', '-af',
        'highpass=f=70,acompressor=threshold=-24dB:ratio=2.2:attack=8:release=140,loudnorm=I=-14:TP=-1.5:LRA=7,afade=t=in:d=0.03,afade=t=out:st=%.3f:d=0.06' % (N / 60 - 0.07), HD + '/a.wav'])
    sh(['ffmpeg', '-v', 'error', '-y', '-i', HD + '/v.mp4', '-i', HD + '/a.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', HD + '/hook.mp4'])

def hook_preview(j):
    """Frame 0 of the hook as an image, to check before the full render."""
    from playwright.sync_api import sync_playwright
    import cv2
    D = j['_dir']; c = j['hook']
    sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['a'] + 0.05), '-i', f'{D}/src60.mp4', '-frames:v', '1', f'{D}/hook_f0.png'])
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--allow-file-access-from-files']); pg = br.new_page(viewport={'width': W, 'height': H})
        pg.goto(f'file://{ROOT}/templates/hook.html'); pg.evaluate('c=>setup(c)', c); pg.evaluate('frame(0.1)')
        pg.screenshot(path=f'{D}/hook_t.png', omit_background=True); br.close()
    f = cv2.imread(f'{D}/hook_f0.png').astype(float); o = cv2.imread(f'{D}/hook_t.png', -1); a = o[:, :, 3:] / 255.
    cv2.imwrite(f'{D}/hook_preview.jpg', cv2.resize((f * (1 - a) + o[:, :, :3] * a).astype(np.uint8), (540, 960))); print('wrote', f'{D}/hook_preview.jpg')

# ---------------------------------------------------------------- join
def join(j):
    D = j['_dir']; name = j['name']; os.makedirs(f'{ROOT}/output', exist_ok=True)
    out = f'{ROOT}/output/{name}.mp4'; G = 'eq=brightness=0.01:saturation=1.03'
    import hdr
    if hdr.ON:  # intermediates are BT.601-matrix RGB carrying HLG/BT.2020 code values -> 10-bit HLG HEVC
        HV = ['-c:v', 'libx265', '-preset', 'medium', '-pix_fmt', 'yuv420p10le', '-tag:v', 'hvc1', '-color_primaries', 'bt2020', '-color_trc', 'arib-std-b67', '-colorspace', 'bt2020nc', '-color_range', 'tv']
        XP = 'colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:hdr10=0'
        CV = 'scale=in_color_matrix=bt601:in_range=tv,format=gbrp16le,scale=out_color_matrix=bt2020:out_range=tv,format=yuv420p10le'
        sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/hook/hook.mp4', '-i', f'{D}/body.mp4', '-filter_complex',
            f'[0:v]fps=60,setsar=1[a];[1:v]fps=60,setsar=1[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au];[v]{CV}[vo];[au]loudnorm=I=-14:TP=-1.5:LRA=9[ao]',
            '-map', '[vo]', '-map', '[ao]', *HV, '-crf', '16', '-x265-params', XP + ':log-level=error', '-r', '60', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', out])
        sh(['ffmpeg', '-v', 'error', '-y', '-i', out, *HV, '-crf', '20', '-x265-params', XP + ':vbv-maxrate=8000:vbv-bufsize=16000:log-level=error', '-r', '60', '-c:a', 'copy', '-movflags', '+faststart', f'{ROOT}/output/{name}-share.mp4'])
    else:
        sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/hook/hook.mp4', '-i', f'{D}/body.mp4', '-filter_complex',
            f'[0:v]fps=60,setsar=1[a];[1:v]fps=60,setsar=1[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au];[v]{G},format=yuv420p[vo];[au]loudnorm=I=-14:TP=-1.5:LRA=9[ao]',
            '-map', '[vo]', '-map', '[ao]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-r', '60', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', out])
        sh(['ffmpeg', '-v', 'error', '-y', '-i', out, '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-maxrate', '6M', '-bufsize', '12M', '-r', '60', '-c:a', 'copy', '-movflags', '+faststart', f'{ROOT}/output/{name}-share.mp4'])
    sh(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', 'fps=1,scale=180:320,tile=10x5', '-frames:v', '1', f'{ROOT}/output/{name}-sheet.jpg'])
    print('DONE', out)

if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0]
    if cmd == 'prep': prep(a[1], a[2])
    elif cmd == 'score': sh([sys.executable, os.path.join(ROOT, 'engine', 'hookscore.py'), '--hook', ' '.join(a[1:])])
    else:
        j = load(a[1])
        if cmd == 'cut': cut(j)
        elif cmd == 'masks': masks(j, *(map(int, a[2:4])) if len(a) > 3 else ())
        elif cmd == 'overlay':
            if len(a) > 4: overlay(j, a[2], int(a[3]), int(a[4]))
            elif len(a) == 3:  # one pass, all workers
                ps = [subprocess.Popen([sys.executable, __file__, 'overlay', a[1], a[2], str(i), str(WORKERS)]) for i in range(WORKERS)]
                [p.wait() for p in ps]
            else: overlay(j)
        elif cmd == 'preview':  # render overlay frames at body times for checking
            ts = [float(x) for x in a[2].split(',')]
            for md in 'PTC': overlay(j, md, only=[int(round(t * FPS)) for t in ts])
            comp(j, ts)
        elif cmd == 'test': comp(j, [float(x) for x in a[2].split(',')])
        elif cmd == 'comp': comp(j)
        elif cmd == 'hookpreview': hook_preview(j)
        elif cmd == 'hook': hook(j)
        elif cmd == 'join': join(j)
        elif cmd == 'all':
            cut(j); masks(j); overlay(j); comp(load(a[1])); hook(j); join(j)
        else: print(__doc__)
