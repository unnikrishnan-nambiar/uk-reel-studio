import json
SIL=json.load(open('silences.json'))
def split(a,b,gap=0.22,pad=0.07):
    # trim range edges into speech, split on internal silences >= gap
    out=[];cur=a
    for s,e in SIL:
        if e<=a or s>=b: continue
        if s<=a+0.01: cur=max(cur,e-pad); continue
        if e>=b-0.01: out.append([cur,min(b,s+pad)]); cur=None; break
        if e-s>=gap: out.append([cur,s+pad]); cur=e-pad
    if cur is not None: out.append([cur,b])
    return [[round(x,2),round(y,2)] for x,y in out if y-x>=0.2]
H={'h1':(0.98,4.75),'h2':(6.1,10.5),'h3':(148.9,152.5)}
B=[(154.3,158.6),(26.7,34.3),(172.3,175.1),(179.0,188.4),(52.4,56.2),(57.8,60.0),(63.2,67.9),(206.0,216.2),
   (218.8,222.6),(225.8,229.9),(233.0,235.3),(237.8,244.7),(246.3,248.7),(124.0,131.8),(261.6,264.0)]
HOOKS={k:split(*v,gap=0.5) for k,v in H.items()}
BODY=[]; 
for r in B: BODY+=split(*r)
for k,v in HOOKS.items(): print(k,v)
print(BODY, sum(y-x for x,y in BODY))
json.dump(dict(HOOKS=HOOKS,BODY=BODY),open('segs.json','w'))
