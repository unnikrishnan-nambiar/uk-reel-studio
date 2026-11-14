# Crops screen stills, blurs personal data (OCR word matches + manual boxes), writes highlights (crop coords) to stills.json
import csv, re, json, cv2, numpy as np
D='/home/claude/uk-reel-studio/jobs/hof/'
import os
PW=[w.strip() for w in open(D+'stills/private_words.txt')] if os.path.exists(D+'stills/private_words.txt') else []  # names/cities to blur, kept out of git
PAT=re.compile(r'('+'|'.join([re.escape(w) for w in PW if w]+[r'gmail',r'@',r'\d{6,}',r'\.b\.'])+')',re.I)
S={
 'guide': dict(src=3,  crop=(550,200,1340,870), blur=[], hl=[(574,559,1290,606)]),
 'prompt':dict(src=62, crop=(770,520,1420,665), blur=[(790,594,1100,654)], hl=[]),
 'search':dict(src=104,crop=(730,170,1480,450), blur=[(888,264,1210,328)], hl=[(736,415,1396,440)]),
 'r1':    dict(src=116,crop=(730,300,1480,520), blur=[], hl=[(736,314,1392,358),(736,429,1410,453)]),
 'r2':    dict(src=116,crop=(730,525,1480,860), blur=[], hl=[(733,560,1470,700)]),
 'f1':    dict(src=185,crop=(730,175,1480,530), blur=[(888,244,1115,326)], hl=[(736,368,1250,406),(736,416,1394,440)]),
 'f2':    dict(src=232,crop=(730,170,1480,460), blur=[], hl=[(1305,178,1404,201),(736,199,1414,222)]),
}
out={}
for k,s in S.items():
    im=cv2.imread(D+f"scr/s{s['src']}.png"); boxes=list(s['blur'])
    for r in csv.DictReader(open(D+f"scr/o{s['src']}.tsv"),delimiter='\t',quoting=3):
        t=(r['text'] or '').strip()
        if t and PAT.search(t):
            x,y,w,h=int(r['left']),int(r['top']),int(r['width']),int(r['height']); boxes.append((x,y,x+w,y+h))
    for (x1,y1,x2,y2) in boxes:
        x1,y1,x2,y2=x1-6,y1-5,x2+6,y2+5
        roi=im[y1:y2,x1:x2]; b=cv2.GaussianBlur(cv2.resize(roi,(max(1,(x2-x1)//6),max(1,(y2-y1)//6))),(0,0),1.2)
        im[y1:y2,x1:x2]=cv2.GaussianBlur(cv2.resize(b,(x2-x1,y2-y1),interpolation=cv2.INTER_LINEAR),(0,0),3)
    cx,cy,cx2,cy2=s['crop']; c=im[cy:cy2,cx:cx2]
    c=cv2.resize(c,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(D+f'stills/{k}.png',c)
    out[k]=dict(w=cx2-cx,h=cy2-cy,hl=[[x-cx,y-cy,x2-cx,y2-cy] for x,y,x2,y2 in s['hl']],nblur=len(boxes))
    print(k,len(boxes),'blurred', [ (b) for b in boxes][:8])
json.dump(out,open(D+'stills/stills.json','w'))
