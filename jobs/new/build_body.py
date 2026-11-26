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
        N0 = max(1, round((y - x) * 60))
        if i == 0 and j == 0:  # smooth eased push-in on the very first shot
            vf = f"zoompan=z='1+0.24*(3*pow(on/{N0},2)-2*pow(on/{N0},3))':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.40':d=1:s=1080x1920:fps=60,setsar=1"
        else:
          vf = 'fps=60,setsar=1' if z == 1.0 else f'crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*0.40,scale=1080:1920:flags=lanczos,fps=60,setsar=1'
        N = max(1, round((y - x) * 60)); D = N / 60  # exact frame count; audio trimmed/padded to the same length (no A/V drift)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{x}', '-t', f'{D + 0.1}', '-i', 'src60.mp4', '-vf', vf, '-frames:v', str(N),
                        '-af', 'aresample=48000,apad,atrim=0:%.6f,asetpts=N/SR/TB,afade=t=in:d=0.008,afade=t=out:st=%.3f:d=0.008' % (D, D - 0.008), '-ac', '2',
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
