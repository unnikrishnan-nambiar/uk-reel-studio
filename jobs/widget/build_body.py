# Cut src60.mp4 into the edit order in segs.ALL (re-ordering allowed), write cut60.mp4 + body.wav + edit.json.
import subprocess, json, os
from segs import ALL
parts = []; t = 0.0; segs = []
for i, (a, b) in enumerate(ALL):
    out = f'p{i:02d}.mov'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a}', '-t', f'{b - a}', '-i', 'src60.mp4', '-vf', 'fps=60,setsar=1',
                    '-af', 'aresample=48000,afade=t=in:d=0.012,afade=t=out:st=%.3f:d=0.012' % (b - a - 0.012), '-ac', '2',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-c:a', 'pcm_s16le', out], check=True)
    segs.append(dict(src0=a, src1=b, out0=round(t, 3), out1=round(t + b - a, 3))); parts.append(out); t += b - a
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'cut60.mov'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'cut60.mov', '-an', '-c:v', 'copy', 'cut60.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'cut60.mov', '-vn', 'body.wav'], check=True)
for p in parts + ['cut60.mov']: os.remove(p)
json.dump(dict(segs=segs, dur=round(t, 3)), open('edit.json', 'w'), indent=1); json.dump([], open('caps_body.json', 'w'))
print('dur', round(t, 2))
