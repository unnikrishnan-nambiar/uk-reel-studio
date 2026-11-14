# HYPE or FACT? minimal (Tunde-style) cut: body.mov + timeline.json
import json, subprocess
U = '/mnt/user-data/uploads/'
H = U + 'edec3bf2729644ccbcb99b166dc88727_3.mp4'   # Hadi's reel = test subject
I71 = U + 'IMG_0471.mov'; I76 = U + 'IMG_0476.mov'
# [src, in, out, scene, highlights(src_t, still_hl_index)]
SEGS = [
 ['intro', 0.0, 6.6, 'intro', []],       # i71 2.0-8.6 video + Hadi card (Hadi audio)
 [I71, 12.8, 16.4, 'title', []],
 [I76, 3.5, 9.5, 'guide', []],
 [I76, 10.7, 17.1, 'r1', [(11.6, 0), (14.6, 1)]],
 [I76, 17.4, 24.1, 'f1', []],
 [I76, 25.0, 29.9, 'f1b', [(25.4, 0), (26.6, 1)]],
 [I76, 32.9, 38.1, 'f2', [(33.4, 0), (34.2, 1)]],
 [I76, 38.8, 49.9, 'india', [(43.0, 0), (45.2, 1), (47.6, 2)]],
 [I76, 50.2, 52.7, 'india2', [(50.4, 3)]],
 [I76, 52.9, 55.5, 'answer', []],
 [I76, 62.6, 67.3, 'cta', []],
]
FPS = 60; parts = []; tl = []; t = 0.0
for i, (src, a, b, scene, hls) in enumerate(SEGS):
    d = b - a; out = f'seg{i:02d}.mov'
    if scene == 'intro':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', '2.0', '-t', f'{d}', '-i', I71, '-ss', '0', '-t', f'{d}', '-i', H, '-i', 'mask.png',
               '-filter_complex', f'[0:v]scale=1080:1920:flags=lanczos,fps={FPS}[bg];[1:v]scale=580:1031:flags=lanczos,fps={FPS},format=rgba[h];'
               f'[2:v]format=gray,scale=580:1031[m];[h][m]alphamerge[hm];[bg][hm]overlay=26:312:shortest=1,format=yuv420p,setsar=1[v];'
               '[1:a]aresample=48000,loudnorm=I=-16:TP=-1.5[a]', '-map', '[v]', '-map', '[a]', '-ac', '2',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-c:a', 'pcm_s16le', out]
    else:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{a}', '-t', f'{d}', '-i', src,
               '-vf', f'scale=1080:1920:flags=lanczos,fps={FPS},format=yuv420p,setsar=1',
               '-af', 'aresample=48000,highpass=f=80,afftdn=nf=-28,loudnorm=I=-16:TP=-1.5', '-ac', '2',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-c:a', 'pcm_s16le', out]
    subprocess.run(cmd, check=True)
    tl.append(dict(i=i, t0=round(t, 3), t1=round(t + d, 3), scene=scene, hl=[[round(t + s - a, 3), k] for s, k in hls]))
    parts.append(out); t += d
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'body.mov'], check=True)
for p in parts: subprocess.run(['rm', '-f', p])
json.dump(dict(dur=round(t, 3), segs=tl), open('timeline.json', 'w'), indent=1); print('body', round(t, 2))
