# Hype or Fact template: cut camera segments into body.mp4 (1080x1920, 60 fps) + timeline.json
# Segment = [source, in, out, layout(full|split), still or scene, captions[(src_t, text)]]
import json, subprocess
U = '/mnt/user-data/uploads/'
A = '/mnt/user-data/attachments/08f0bc37-97d1-51a2-831a-506d676f4e25/'
SRC = {'hadi': U + 'edec3bf2729644ccbcb99b166dc88727_3.mp4', 'i44': U + 'IMG_0444.mov',
       'i45': A + 'e3f04783-IMG_0445.mov', 'c4': U + 'E0FEF7D8-2795-418F-9F5E-DA00991660DC_4.mov',
       'c5': U + 'E0FEF7D8-2795-418F-9F5E-DA00991660DC_5.mov'}
SEGS = [
 ['hadi', 0.00, 2.30, 'full', 'claim', []],
 ['i44', 7.30, 10.95, 'full', 'ask', [(8.6, 'Does this really work?'), (9.6, "Let's {TEST} it")]],
 ['i45', 0.40, 2.30, 'full', 'go', []],
 ['c4', 0.60, 2.80, 'split', 'guide', [(0.7, 'First, {HIS GUIDE}')]],
 ['c4', 23.30, 26.60, 'split', 'prompt', [(23.4, 'Same steps,'), (24.6, 'the {FIRST PROMPT}')]],
 ['c4', 96.50, 102.80, 'split', 'search', [(96.6, 'It checks every'), (97.9, '{DATA BROKER} site'), (100.0, 'for my name and details')]],
 ['c4', 121.00, 129.30, 'split', 'r1', [(121.1, 'Result:'), (122.0, "couldn't find {ANY SITE}"), (124.2, 'with my details'), (126.1, "\"doesn't mean you're"), (127.6, "not listed\"")]],
 ['c4', 130.10, 136.20, 'split', 'r1b', [(130.2, 'These sites mostly'), (132.4, 'cover the {US}')]],
 ['c5', 9.60, 20.50, 'split', 'f1', [(9.7, "Let's try a"), (10.6, "{FRIEND'S} details"), (14.4, 'Claude checks'), (15.4, '{PERMISSION} first')]],
 ['c5', 57.80, 66.00, 'split', 'f2', [(57.9, 'Name {HIDDEN}'), (59.6, "it's not my data"), (63.5, 'Same result:'), (64.5, '{NOTHING FOUND}')]],
 ['c5', 93.30, 102.20, 'split', 'r2', [(93.4, 'Truecaller may'), (94.6, 'have your number'), (96.4, "It's built for the {US}"), (99.0, 'not for {INDIA}'), (100.6, 'In India, do this')]],
 ['c5', 106.30, 118.70, 'full', 'india', [(106.4, 'Turn on {FULL DND}'), (108.0, 'call {1909}'), (110.9, 'Blocks promo'), (112.4, 'calls and SMS'), (116.6, '{UNLIST} on Truecaller')]],
 ['c5', 123.60, 128.80, 'full', 'india2', [(123.7, '{REPORT} scam calls'), (126.5, 'Lost money? {1930}')]],
 ['c5', 129.70, 136.90, 'full', 'verdict', [(129.8, 'So basically'), (131.0, 'it {DIDN\'T WORK}'), (132.9, 'Worked for you?'), (134.3, 'Tell me')]],
 ['c5', 149.30, 153.50, 'full', 'end', [(149.4, '{FOLLOW} for'), (150.8, 'more real tests')]],
]
FPS = 60
parts = []; tl = []; t = 0.0
for i, (k, a, b, lay, scene, caps) in enumerate(SEGS):
    d = b - a; out = f'seg{i:02d}.mp4'
    if k == 'hadi':
        vf = 'scale=1080:1920:flags=lanczos'
    elif lay == 'split':
        # bottom 1020 px shows the face; top 900 px is the dark panel for the screen card
        vf = 'crop=1080:1020:0:450,pad=1080:1920:0:900:color=0x0d0d0d'
    else:
        vf = 'scale=1080:1920:flags=lanczos'
    af = 'aresample=48000,highpass=f=80,afftdn=nf=-28' if k != 'hadi' else 'aresample=48000'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a}', '-t', f'{d}', '-i', SRC[k],
                    '-vf', vf + f',fps={FPS},format=yuv420p,setsar=1', '-af', af + ',loudnorm=I=-16:TP=-1.5',
                    '-ac', '2', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-c:a', 'pcm_s16le',
                    '-f', 'mov', out], check=True)
    tl.append(dict(i=i, src=k, a=a, b=b, t0=round(t, 3), t1=round(t + d, 3), layout=lay, scene=scene,
                   caps=[[round(t + (s - a), 3), txt] for s, txt in caps]))
    parts.append(out); t += d
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c:v', 'copy',
                '-c:a', 'pcm_s16le', 'body.mov'], check=True)
json.dump(dict(dur=round(t, 3), segs=tl), open('timeline.json', 'w'), indent=1)
print('body', round(t, 2), 's')
