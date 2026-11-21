# Cut src60.mp4 into segs.ALL with face zoom cuts, write cut60.mp4 + body.wav + edit.json.
import subprocess, json, os
from segs import ALL, ZOOM
def zoom_at(t):
    z = 1.0
    for s, v in ZOOM:
        if t >= s - 1e-6: z = v
    return z
parts = []; t = 0.0; segs = []
for i, (a, b) in enumerate(ALL):
    cuts = [a] + [s for s, _ in ZOOM if a < s < b] + [b]
    for j, (x, y) in enumerate(zip(cuts[:-1], cuts[1:])):
        z = zoom_at(x); out = f'p{i:02d}_{j}.mov'
        vf = 'fps=60,setsar=1' if z == 1.0 else f'crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*0.40,scale=1080:1920:flags=lanczos,fps=60,setsar=1'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{x}', '-t', f'{y - x}', '-i', 'src60.mp4', '-vf', vf,
                        '-af', 'aresample=48000,afade=t=in:d=0.008,afade=t=out:st=%.3f:d=0.008' % (y - x - 0.008), '-ac', '2',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-c:a', 'pcm_s16le', out], check=True)
        parts.append(out)
    segs.append(dict(src0=a, src1=b, out0=round(t, 3), out1=round(t + b - a, 3))); t += b - a
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'cut60.mov'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'cut60.mov', '-an', '-c:v', 'copy', 'cut60.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'cut60.mov', '-vn', 'body.wav'], check=True)
for p in parts + ['cut60.mov']: os.remove(p)
json.dump(dict(segs=segs, dur=round(t, 3)), open('edit.json', 'w'), indent=1); json.dump([], open('caps_body.json', 'w'))
print('dur', round(t, 2))
