import json
S=json.load(open('sil2.json'))
sp=[];prev=0
for a,b in S:
    if a>prev+0.03: sp.append([prev,a])
    prev=b
sp.append([prev,274.0])
def seg(a,b,gap=0.35,pre=0.10,post=0.16):
    R=[r for r in sp if r[1]>a+0.05 and r[0]<b-0.05]
    out=[]
    for r in R:
        if out and r[0]-out[-1][1]<gap: out[-1][1]=r[1]
        else: out.append(list(r))
    return [[round(x-pre,2),round(y+post,2)] for x,y in out]
H={'h1':(0.98,4.75),'h2':(6.1,10.5),'h3':(148.9,152.5)}
B=[(154.3,158.6),(26.7,34.3),(172.3,175.1),(179.0,188.4),(52.4,56.2),(57.8,60.0),(63.2,67.9),(206.0,216.2),
   (218.8,222.6),(225.8,229.9),(233.0,235.3),(237.8,244.7),(246.3,248.7),(124.0,131.8),(261.6,264.0)]
HOOKS={k:seg(*v) for k,v in H.items()}
for k,v in HOOKS.items(): print(k,v)
BODY=[]
for r in B:
    s=seg(*r); print(r,'->',s); BODY+=s
# sanity: no overlaps within source
allp=sorted([x for v in HOOKS.values() for x in v]+BODY)
for x,y in zip(allp,allp[1:]):
    if x[1]>y[0]: print('OVERLAP',x,y)
json.dump(dict(HOOKS=HOOKS,BODY=BODY),open('segs2.json','w'))
print(round(sum(y-x for x,y in BODY),2))
