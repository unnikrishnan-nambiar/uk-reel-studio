# python3 render.py test t1,t2,...   -> test.jpg (overlay composited on body frames)
# python3 render.py full             -> ov.mov (alpha overlay, 60 fps) then final mux happens in final.sh
import json, sys, subprocess, os, io
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
TL = json.load(open('timeline.json')); ST = json.load(open('stills/stills.json'))
html = open('overlay.html').read().replace('__TL__', json.dumps(TL)).replace('__ST__', json.dumps(ST))
open('_ov.html', 'w').write(html)
FPS = 60
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + D + '/_ov.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    def shot(t):
        pg.evaluate(f'frame({t})')
        pg.evaluate('Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r})))')
        return pg.screenshot(omit_background=True, type='png')
    if sys.argv[1] == 'test':
        ts = [float(x) for x in sys.argv[2].split(',')]; tiles = []
        for t in ts:
            fr = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', 'body.mov', '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
            bg = Image.open(io.BytesIO(fr)).convert('RGBA'); ov = Image.open(io.BytesIO(shot(t))).convert('RGBA')
            tiles.append(Image.alpha_composite(bg, ov).convert('RGB').resize((360, 640)))
        cols = 6; rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new('RGB', (360 * cols, 640 * rows), 'black')
        for i, im in enumerate(tiles): sheet.paste(im, ((i % cols) * 360, (i // cols) * 640))
        sheet.save('test.jpg', quality=85); print('test.jpg')
    else:
        n = int(TL['dur'] * FPS)
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-i', 'body.mov', '-f', 'image2pipe', '-framerate', str(FPS), '-vcodec', 'png', '-i', '-',
                               '-i', 'sfx.wav', '-filter_complex',
                               '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[0:a][2:a]amix=inputs=2:weights=1 0.32:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]',
                               '-map', '[v]', '-map', '[a]', '-r', str(FPS), '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-profile:v', 'high',
                               '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                               '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', 'hof.mp4'], stdin=subprocess.PIPE)
        for i in range(n):
            ff.stdin.write(shot(i / FPS))
            if i % 600 == 0: print('frame', i, '/', n, flush=True)
        ff.stdin.close(); ff.wait(); print('OVDONE')
    b.close()
