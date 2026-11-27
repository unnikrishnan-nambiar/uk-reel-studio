# Extract screen-recording clips as 30fps 1080x1920 JPG sequences (full screen), with personal info blurred.
import subprocess, os, shutil
C = {  # name: list of (file, t0, t1, cropY, blur boxes [x,y,w,h] in output px)
 'reddit': [('s4', 5.8, 9.8, 90, [])],
 'priv':   [('s1', 2.0, 4.2, 90, [])],
 'shared': [('s1', 4.0, 5.6, 90, []), ('s1', 29.0, 32.3, 300, [[40, 120, 620, 1370]])],
 'memory': [('s3', 0.2, 5.6, 90, [])],
 'improve':[('s2', 14.6, 18.6, 90, [])],
}
for k, parts in C.items():
    d = f'snip/{k}'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    n = 0
    for i, (f, a, b, cy, boxes) in enumerate(parts):
        vf = f'fps=30,scale=1080:-1,crop=1080:1920:0:{cy}'
        if boxes:
            chain = '[0:v]' + vf + '[base]'; last = 'base'
            for j, (x, y, w, h) in enumerate(boxes):
                chain += f';[{last}]split[a{j}][b{j}];[b{j}]crop={w}:{h}:{x}:{y},boxblur=28:3[bl{j}];[a{j}][bl{j}]overlay={x}:{y}[o{j}]'; last = f'o{j}'
            args = ['-filter_complex', chain, '-map', f'[{last}]']
        else:
            args = ['-vf', vf]
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', f'scr/{f}.mp4', *args, '-q:v', '3', '-start_number', str(n + 1), f'{d}/%03d.jpg'], check=True)
        n = len(os.listdir(d))
    print(k, n)
