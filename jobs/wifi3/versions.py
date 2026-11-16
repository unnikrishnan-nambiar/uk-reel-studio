# Cut the composited body.mp4 (H1,H2,H3,body) into 3 versions: one hook + body. Mix SFX, HDR (HLG) encode master + share.
import json, subprocess, os
D = '/home/claude/uk-reel-studio/jobs/wifi3'; O = '/home/claude/uk-reel-studio/output'; U = '/mnt/user-data/outputs'
S = json.load(open(f'{D}/edit.json'))['segs']; END = json.load(open(f'{D}/edit.json'))['dur']
H = {'h1': (S[0]['out0'], S[0]['out1']), 'h2': (S[1]['out0'], S[1]['out1']), 'h3': (S[2]['out0'], S[2]['out1'])}
B0 = S[3]['out0']
CV = 'scale=in_color_matrix=bt601:in_range=tv,format=gbrp16le,scale=out_color_matrix=bt2020:out_range=tv,format=yuv420p10le'
HV = ['-c:v', 'libx265', '-pix_fmt', 'yuv420p10le', '-tag:v', 'hvc1', '-color_primaries', 'bt2020', '-color_trc', 'arib-std-b67', '-colorspace', 'bt2020nc', '-color_range', 'tv']
XP = 'colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:hdr10=0:log-level=error'
for k, (a, b) in H.items():
    fc = (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v0];[0:v]trim={B0}:{END},setpts=PTS-STARTPTS[v1];"
          f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a0];[0:a]atrim={B0}:{END},asetpts=PTS-STARTPTS[a1];"
          f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[s0];[1:a]atrim={B0}:{END},asetpts=PTS-STARTPTS[s1];"
          f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][va];[s0][s1]concat=n=2:v=0:a=1,volume=0.32[sx];"
          f"[va][sx]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aa];[v]fps=60,setsar=1,{CV}[vv]")
    m = f'{O}/wifi-{k}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/body.mp4', '-i', f'{D}/sfx.wav', '-filter_complex', fc, '-map', '[vv]', '-map', '[aa]',
                    *HV, '-preset', 'fast', '-crf', '17', '-x265-params', XP, '-r', '60', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', m], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', m, *HV, '-preset', 'veryfast', '-crf', '21', '-x265-params', XP + ':vbv-maxrate=8000:vbv-bufsize=16000',
                    '-c:a', 'copy', '-movflags', '+faststart', f'{O}/wifi-{k}-share.mp4'], check=True)
    subprocess.run(['cp', m, f'{U}/wifi-hook{k[1]}.mp4']); subprocess.run(['cp', f'{O}/wifi-{k}-share.mp4', f'{U}/wifi-hook{k[1]}-share.mp4'])
    print('done', k, flush=True)
