# 5 AI words reel: cut silences, tonemap HLG -> SDR, body.mov + timeline.json
import json, subprocess
SRC = '/mnt/user-data/uploads/3BB577B9-AA30-4170-ACD6-1D3A776A1527.mp4'
TM = 'zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,eq=saturation=1.08:contrast=1.03,format=yuv420p'
# [in, out, scene]
SEGS = [[0.4, 65.5, 'all']]   # no cuts: he wants every heading and full sentences kept
# captions in SOURCE time: (start, end, text, key)
CAPS = [
 (0.6, 1.7, 'അടുത്ത 60 സെക്കൻഡിൽ', 0), (1.7, 3.8, 'AI-യിൽ അറിഞ്ഞിരിക്കേണ്ട 5 സാധനം', 1), (3.9, 6.6, 'First: Artificial Intelligence', 1),
 (6.8, 10.4, 'കമ്പ്യൂട്ടറിന് മനുഷ്യനെപ്പോലെ മനസ്സിലാക്കാനും സംസാരിക്കാനുമുള്ള കഴിവ്', 0), (10.6, 12.8, 'ഒരുപാട് വായിച്ചു പഠിച്ച ഒരു brain', 1),
 (13.1, 14.7, 'Second: ChatGPT, Claude', 1), (14.8, 18.1, 'ChatGPT OpenAI-യുടെ കട, Claude Anthropic-ന്റെ', 0), (18.1, 20.2, 'Gemini Google-ന്റെ കട', 0),
 (20.6, 22.9, 'Third: Models, കടയിലെ chef', 1), (23.0, 25.9, 'ചിലർ fast, ചിലർ smart', 0), (26.0, 28.0, 'ChatGPT-ൽ GPT models', 0), (28.0, 30.3, 'Claude-ൽ Opus, Sonnet', 0),
 (30.4, 33.5, 'App അല്ല, model ആണ് answer-ന്റെ quality', 1),
 (33.6, 34.7, 'Fourth: Tokens', 1), (34.8, 36.7, 'AI വാക്കുകൾ മുഴുവനായല്ല വായിക്കുന്നത്', 0), (36.7, 39.0, 'ചെറിയ കഷണങ്ങൾ: അതാണ് token', 1), (39.1, 42.4, 'നിങ്ങളുടെ limit-ഉം API cost-ഉം token-ൽ', 0),
 (42.4, 45.75, 'English-നേക്കാൾ Malayalam-ന് കൂടുതൽ tokens വേണം', 1),
 (45.9, 48.6, 'Fifth: Prompt, നിങ്ങൾ AI-യോട് പറയുന്ന order', 1), (48.6, 51.2, '"എന്തെങ്കിലും താ" എന്ന് പറഞ്ഞാൽ എന്തെങ്കിലും കിട്ടും', 0),
 (51.3, 56.9, 'Clear ആയി പറഞ്ഞാൽ: chicken biryani, half plate', 0), (57.0, 59.25, 'Clear prompt = clear answer', 1),
 (59.3, 62.8, '5-ൽ എത്ര കിട്ടി? 5/5 ആണെങ്കിൽ AI basics set', 1), (62.9, 65.3, 'Detailed guide വേണമെങ്കിൽ comment ചെയ്യൂ', 0)]
FPS = 60; parts = []; tl = []; t = 0.0
for i, (a, b, sc) in enumerate(SEGS):
    d = b - a; out = f'seg{i:02d}.mov'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a}', '-t', f'{d}', '-i', SRC, '-vf', f'{TM},fps={FPS},setsar=1',
                    '-af', 'aresample=48000,highpass=f=80,afftdn=nf=-28,loudnorm=I=-16:TP=-1.5', '-ac', '2',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-c:a', 'pcm_s16le', out], check=True)
    caps = [[round(t + max(s, a) - a, 3), round(t + min(e, b) - a, 3), x, k] for s, e, x, k in CAPS if s < b and e > a]
    tl.append(dict(i=i, t0=round(t, 3), t1=round(t + d, 3), a=a, b=b, scene=sc, caps=caps)); parts.append(out); t += d
open('list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'body.mov'], check=True)
for p in parts: subprocess.run(['rm', '-f', p])
json.dump(dict(dur=round(t, 3), segs=tl), open('timeline.json', 'w'), indent=1, ensure_ascii=False); print('body', round(t, 2))
