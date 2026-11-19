import subprocess, os, shutil
from PIL import Image, ImageFilter
U='/mnt/user-data/uploads/'; T='/mnt/user-data/attachments/08f0bc37-97d1-51a2-831a-506d676f4e25/'
A=U+'ScreenRecording_11-19-2026_12-10-46_1.mp4'; B=U+'ScreenRecording_11-19-2026_12-18-23_1.mp4'
C=T+'29c06d12-ScreenRecording_11-19-2026_12-19-34_1.mp4'; D=T+'21d77b07-ScreenRecording_11-19-2026_12-22-03_1.mp4'
E=T+'284f4d0a-ScreenRecording_11-19-2026_12-19-52_1.mov'
def ext(name,f,a,b,cw,cx,cy,sp=1.0,start=1):
    ch=round(cw/0.5625); os.makedirs(name,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',f,'-vf',
        f'setpts=PTS/{sp},fps=30,scale=1080:-2,crop={cw}:{ch}:{cx}:{cy},scale=1080:1920:flags=lanczos','-q:v','3','-start_number',str(start),f'{name}/%04d.jpg'],check=True)
    return len(os.listdir(name))
def blur(name,boxes,cond=None):
    for fn in sorted(os.listdir(name)):
        p=f'{name}/{fn}'; im=Image.open(p).convert('RGB')
        if cond and not cond(im): continue
        for bx in boxes: im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(14)),bx)
        im.save(p,quality=88)
for d in ['prompt','type','code','scr','paste','add','short','vk']: shutil.rmtree(d,ignore_errors=True)
ext('prompt',A,3.4,6.0,960,60,560)        # paste the prompt into the chat box
ext('type',A,20.6,23.0,960,60,100)        # Claude's questions + typing "Water tracker"
ext('code',B,7.4,9.4,960,60,640); blur('code',[(30,690,1050,1560)])          # "Your script is ready... Copy"
ext('scr',C,3.3,4.7,1000,40,100,sp=0.6)     # the app's scripts list
ext('paste',B,14.2,15.4,800,0,150)         # empty new script page
n=ext('add',E,1.6,3.7,1000,40,150)         # long-press -> add widget -> gallery
ext('add',C,0.0,1.5,1000,40,150,start=n+1) # widget on the home screen
ext('short',D,0.9,2.3,760,0,300,sp=0.6)           # Shortcuts: Vellam Kudichu
ext('vk',E,0.0,1.4,760,0,150,sp=0.6)       # Vellam Kudi widget 3/8
blur('vk',[(290,760,530,840)])
blur('add',[(400,570,700,650),(400,1740,700,1820)],lambda im: sum(im.getpixel((60,300)))<300)
for d in ['prompt','type','code','scr','paste','add','short','vk']: print(d,len(os.listdir(d)))
