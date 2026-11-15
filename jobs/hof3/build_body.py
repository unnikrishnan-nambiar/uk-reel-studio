# HYPE or FACT? full episode: new hook (6 s Hadi card while he listens) + minimal test layout. body.mov + timeline.json
import json, subprocess
U = '/mnt/user-data/uploads/'
H = U + 'edec3bf2729644ccbcb99b166dc88727_3.mp4'; I71 = U + 'IMG_0471.mov'; I76 = U + 'IMG_0476.mov'
# [src, in, out, scene, highlights(src_t, idx), captions(src_t_start, src_t_end, text, key)]
SEGS = [
 [I71, 5.6, 16.4, 'hook', [], [(12.0, 13.6, 'ഇതൊക്കെ ശരിക്കും work ചെയ്യുമോ,', 0), (13.6, 14.9, 'അതോ വെറും hype ആണോ?', 1), (14.9, 16.4, 'നമുക്കൊന്ന് ചെയ്ത് നോക്കിയാലോ', 0)]],
 [I76, 3.5, 9.5, 'guide', [], [(3.6, 5.3, 'ഹാദിയുടെ തന്നെ guide,', 0), (5.3, 6.8, 'ഹാദിയുടെ തന്നെ prompt', 0), (6.8, 9.5, 'എന്റെ പേര്, email ID ഒക്കെ കൊടുക്കുന്നു', 0)]],
 [I76, 10.7, 17.1, 'r1', [(11.6, 0), (14.6, 1)], [(10.7, 11.5, 'ഓക്കെ, result', 0), (11.5, 14.4, 'ഒരു site-ലും എന്റെ details ഇല്ല', 1), (14.5, 17.1, 'Claude പറയുന്നു, ഇത് mostly US sites ആണ്', 0)]],
 [I76, 17.4, 24.1, 'f1', [], [(17.5, 18.8, 'ചിലപ്പോൾ എന്റെ മാത്രം problem ആവും', 0), (18.8, 20.8, 'ഒരു friend-ന് try ചെയ്ത് നോക്കാം', 0), (20.8, 22.7, 'അവൻ ഒരു company-യുടെ founder ആണ്', 0), (22.7, 24.1, 'കുറേ websites-ൽ അവന്റെ number ഉണ്ടാവും', 0)]],
 [I76, 25.0, 32.7, 'f1b', [(25.4, 0), (26.6, 1)], [(25.1, 27.4, 'Claude permission ചോദിച്ചു, നല്ല കാര്യം', 1), (27.5, 30.5, 'വേറെ ഒരാളുടെ details ആണല്ലോ', 0), (31.0, 32.7, 'Permission ഉണ്ട് എന്ന് പറഞ്ഞു', 0)]],
 [I76, 32.9, 38.1, 'f2', [(33.4, 0), (34.2, 1)], [(33.0, 35.3, 'ഓക്കെ, same result', 0), (35.4, 38.1, 'ഇവിടെയും ഒന്നും കണ്ടില്ല', 1)]],
 [I76, 38.8, 49.9, 'india', [(44.5, 0), (46.1, 1), (47.6, 2)], [(38.9, 40.7, 'പക്ഷേ നമ്മുടെ real problem', 0), (40.8, 44.4, 'scam-ഉം spam calls-ഉം ആണ്', 1), (44.5, 46.0, '1909 വിളിച്ച് full DND on ആക്കുക', 0), (46.1, 47.5, 'Truecaller-ൽ number unlist ചെയ്യുക', 0), (47.6, 49.9, 'Scam call വന്നാൽ Chakshu-വിൽ report ചെയ്യുക', 0)]],
 [I76, 50.2, 52.7, 'india2', [(50.4, 3)], [(50.3, 52.7, 'പൈസ പോയാൽ ഉടനെ 1930 വിളിക്കുക', 1)]],
 [I76, 52.9, 55.5, 'answer', [], [(53.0, 55.5, 'India-ക്ക് ഇത് പക്കാ hype ആണ്', 1)]],
 [I76, 62.6, 67.3, 'cta', [], [(62.7, 67.3, '4 steps-ന്റെ full guide വേണമെങ്കിൽ comment DELETE', 0)]],
]
HK0, HK1 = 0.3, 6.3   # Hadi card on screen inside the hook (segment-local)
FPS = 60; parts = []; tl = []; t = 0.0
for i, (src, a, b, scene, hls, caps) in enumerate(SEGS):
    d = b - a; out = f'seg{i:02d}.mov'
    if scene == 'hook':
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{a}', '-t', f'{d}', '-i', I71, '-ss', '0', '-t', f'{HK1-HK0}', '-i', H, '-i', 'mask.png',
               '-filter_complex', f'[0:v]scale=1080:1920:flags=lanczos,fps={FPS}[bg];[1:v]scale=560:996:flags=lanczos,fps={FPS},format=rgba,setpts=PTS+{HK0}/TB[h];'
               f'[2:v]format=gray,scale=560:996[m];[h][m]alphamerge[hm];[bg][hm]overlay=26:510:enable=between(t\\,{HK0}\\,{HK1}):eof_action=pass,format=yuv420p,setsar=1[v];'
               f'[0:a]aresample=48000,highpass=f=80,afftdn=nf=-28,volume=enable=lt(t\\,{HK1}):volume=0.15[ua];[1:a]aresample=48000,adelay={int(HK0*1000)}|{int(HK0*1000)}[ha];'
               '[ua][ha]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5[a]', '-map', '[v]', '-map', '[a]', '-ac', '2',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-c:a', 'pcm_s16le', out]
    else:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{a}', '-t', f'{d}', '-i', src,
               '-vf', f'scale=1080:1920:flags=lanczos,fps={FPS},format=yuv420p,setsar=1',
               '-af', 'aresample=48000,highpass=f=80,afftdn=nf=-28,loudnorm=I=-16:TP=-1.5', '-ac', '2',
               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-c:a', 'pcm_s16le', out]
    subprocess.run(cmd, check=True)
    tl.append(dict(i=i, t0=round(t, 3), t1=round(t + d, 3), scene=scene, hl=[[round(t + s - a, 3), k] for s, k in hls],
                   caps=[[round(t + max(s, a) - a, 3), round(t + min(e, b) - a, 3), x, k] for s, e, x, k in caps]))
    parts.append(out); t += d
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'body.mov'], check=True)
for p in parts: subprocess.run(['rm', '-f', p])
json.dump(dict(dur=round(t, 3), segs=tl, hk=[HK0, HK1]), open('timeline.json', 'w'), indent=1, ensure_ascii=False); print('body', round(t, 2))
