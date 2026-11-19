import subprocess, os
from PIL import Image, ImageDraw, ImageFilter
U='/mnt/user-data/uploads/'; T='/mnt/user-data/attachments/08f0bc37-97d1-51a2-831a-506d676f4e25/'
A=U+'ScreenRecording_11-19-2026_12-10-46_1.mp4'; B=U+'ScreenRecording_11-19-2026_12-18-23_1.mp4'
C=T+'29c06d12-ScreenRecording_11-19-2026_12-19-34_1.mp4'; D=T+'21d77b07-ScreenRecording_11-19-2026_12-22-03_1.mp4'
S=[('prompt',A,2.6,7.0,2.2,0),('type',A,19.5,23.5,2.0,0),('code',B,0.0,4.0,2.0,0),('scr',B,12.0,17.0,2.0,0),
   ('add',B,18.0,30.0,4.0,1),('done',B,38.0,41.5,1.2,1),('short',D,0.0,2.3,1.0,0),('vk',C,6.0,9.4,1.0,1)]
for name,f,a,b,sp,home in S:
    os.makedirs(name,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',f,'-vf',
        f'setpts=PTS/{sp},fps=30,scale=1080:-2,crop=1080:1920:0:214','-q:v','3',f'{name}/%04d.jpg'],check=True)
    if home:  # hide notification badge counts in the dock
        for fn in os.listdir(name):
            p=f'{name}/{fn}'; im=Image.open(p)
            for cx in (245,483):
                box=(cx-55,1830,cx+55,1905); r=im.crop(box).filter(ImageFilter.GaussianBlur(14)); im.paste(r,box)
            im.save(p,quality=88)
    print(name,len(os.listdir(name)))
# widget cut-outs for the liquid-glass cards
def cut(src,box,out):
    im=Image.open(src).convert('RGBA').crop(box); m=Image.new('L',im.size,0)
    ImageDraw.Draw(m).rounded_rectangle((0,0,im.size[0]-1,im.size[1]-1),radius=int(min(im.size)*0.17),fill=255); im.putalpha(m); im.save(out)
cut('c1.png',(80,272,1124,760),'w_water.png'); cut('c1.png',(80,876,1124,1964),'w_gym.png'); cut('c9.png',(82,272,568,760),'w_vk.png')
