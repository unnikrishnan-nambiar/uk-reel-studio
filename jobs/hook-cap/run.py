import subprocess,sys
from playwright.sync_api import sync_playwright
SRC='/mnt/user-data/uploads/IMG_0471.mov'; HAD='/mnt/user-data/uploads/edec3bf2729644ccbcb99b166dc88727_3.mp4'
A,D,FPS,IN0,IN1=11.6,4.8,60,0.5,2.4
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file:///home/claude/uk-reel-studio/jobs/hook-cap/ov.html');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(500)
    ff=subprocess.Popen(['ffmpeg','-v','error','-y','-ss',str(A),'-t',str(D),'-i',SRC,'-ss','0','-t',str(IN1-IN0),'-i',HAD,'-i','mask.png',
      '-f','image2pipe','-framerate',str(FPS),'-vcodec','png','-i','-',
      '-filter_complex',f'[0:v]scale=1080:1920,fps=60[b];[1:v]scale=360:640,fps=60,format=rgba,setpts=PTS+{IN0}/TB[h];[2:v]format=gray,scale=360:640[m];[h][m]alphamerge[hm];'
      f'[b][hm]overlay=40:580:enable=between(t\\,{IN0}\\,{IN1}):eof_action=pass[b2];[b2][3:v]overlay=format=auto,format=yuv420p[v];[0:a]highpass=f=80,afftdn=nf=-28,loudnorm=I=-14:TP=-1.5[a]',
      '-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-c:a','aac','-b:a','256k','-movflags','+faststart','/mnt/user-data/outputs/hook-captions-preview.mp4'],stdin=subprocess.PIPE)
    for i in range(int(D*FPS)):
        pg.evaluate(f'frame({i/FPS})');ff.stdin.write(pg.screenshot(omit_background=True,type='png'))
    ff.stdin.close();ff.wait()
    b.close()
