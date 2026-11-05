import cv2,numpy as np,os
os.chdir('/root/uk-reel-studio/jobs/gemini'); os.makedirs('ovC',exist_ok=True)
B=[('claim',2.4,4.45,0.3,1.0),('claim',4.45,7.32,9.4,0.5),('claim',14.2,16.67,17.5,1.0),('thumbs',23.2,24.75,0.0,1.0)]
for name,b0,b1,s0,sp in B:
    cap=cv2.VideoCapture(f'broll/{name}.mp4'); N=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames={}
    need=[int((s0+(n/60-b0)*sp)*60) for n in range(int(round(b0*60)),int(round(b1*60)))]
    i=0
    while i<=max(need):
        ok,fr=cap.read()
        if not ok: break
        if i in need: frames[i]=fr
        i+=1
    for n in range(int(round(b0*60)),int(round(b1*60))):
        b=n/60; fi=int((s0+(b-b0)*sp)*60); fr=frames[fi] if fi in frames else frames[max(k for k in frames if k<=fi)]
        fr=cv2.resize(fr,(1080,1920)).astype(np.float32)
        k=min(1,(b-b0)/0.35); e=1-(1-k)**3; s=1.06-0.06*e
        M=cv2.getRotationMatrix2D((540,960),0,s); fr=cv2.warpAffine(fr,M,(1080,1920),borderMode=cv2.BORDER_REFLECT)
        a=min(1,(b-b0)/0.15)*min(1,(b1-b)/0.15)
        out=np.dstack([np.clip(fr,0,255).astype(np.uint8),np.full((1920,1080),int(a*255),np.uint8)])
        cv2.imwrite(f'ovC/{n:05d}.png',out)
print('done',len(os.listdir('ovC')))
