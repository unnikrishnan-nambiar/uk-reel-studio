import subprocess, os, shutil
from PIL import Image, ImageFilter
U='/mnt/user-data/uploads/'; T='/mnt/user-data/attachments/08f0bc37-97d1-51a2-831a-506d676f4e25/'
A=U+'ScreenRecording_11-19-2026_12-10-46_1.mp4'; B=U+'ScreenRecording_11-19-2026_12-18-23_1.mp4'
C=T+'29c06d12-ScreenRecording_11-19-2026_12-19-34_1.mp4'; D=T+'21d77b07-ScreenRecording_11-19-2026_12-22-03_1.mp4'
E=T+'284f4d0a-ScreenRecording_11-19-2026_12-19-52_1.mov'
def ext(name,f,a,b,sp,start=1):
    os.makedirs(name,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',f,'-vf',
        f'setpts=PTS/{sp},fps=30,scale=1080:-2,crop=1080:1920:0:214','-q:v','3','-start_number',str(start),f'{name}/%04d.jpg'],check=True)
    return len(os.listdir(name))
def blur(name,boxes,cond=None):
    for fn in sorted(os.listdir(name)):
        p=f'{name}/{fn}'; im=Image.open(p).convert('RGB')
        if cond and not cond(im): continue
        for bx in boxes: im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(12)),bx)
        im.save(p,quality=88)
for d in ['prompt','type','code','scr','add','done','short','vk']: shutil.rmtree(d,ignore_errors=True)
ext('prompt',A,2.3,5.4,1.2)
ext('type',A,33.4,36.0,2.4)
ext('code',B,5.5,9.4,2.2); blur('code',[(30,1080,1050,1760)])
ext('scr',C,3.35,4.7,0.55)
ext('add',E,1.5,5.0,1.7)
ext('done',C,0.0,1.5,1.0)
ext('short',D,0.0,2.3,1.0)
ext('vk',E,0.0,1.4,0.6)
DOCK=[(190,1830,300,1905),(428,1830,538,1905)]
home=lambda im: sum(im.getpixel((120,700)))<600
blur('done',DOCK+[(410,474,670,528),(410,1555,670,1607)])
blur('vk',DOCK+[(160,474,420,528)])
blur('add',DOCK+[(160,474,420,528)],home)
for d in ['prompt','type','code','scr','add','done','short','vk']: print(d,len(os.listdir(d)))
