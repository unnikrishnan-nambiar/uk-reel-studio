import json,numpy as np,soundfile as sf,re
SR=48000;TL=json.load(open('timeline.json'));N=int(TL['dur']*SR);o=np.zeros(N,np.float32);r=np.random.default_rng(2)
def add(t,x,g):i=int(t*SR);j=min(N,i+len(x));o[i:j]+=g*x[:j-i]
def wh(d=.3):n=int(d*SR);f=np.cumsum(r.standard_normal(n));f-=np.convolve(f,np.ones(200)/200,'same');return f/np.abs(f).max()*np.sin(np.linspace(0,np.pi,n))**2
def pop(f=900):n=int(.09*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*f*t*(1-3*t))*np.exp(-t*70)
def ding(f=1320):n=int(.5*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*f*t)+.4*np.sin(4*np.pi*f*t))*np.exp(-t*7)
def B(s):
  for g in TL['segs']:
    if g['a']<=s<=g['b']: return g['t0']+s-g['a']
  return max([g['t1'] for g in TL['segs'] if s>g['b']] or [0])
cues=re.findall(r"\[(\d+\.?\d*),(\d+\.?\d*),'([^']*)','([^']*)','([^']*)'\]",open('overlay.html').read())
for a,b,w,q,fx in cues:
  t=B(float(a)); add(max(0,t-.05),wh(.35 if fx else .3),.35 if fx else .28); add(t+.05,pop(950),.45)
  if fx and fx!='score': add(t+.3,ding(),.15)
o=np.tanh(o*1.2)*.8; sf.write('sfx.wav',np.stack([o,o],1),SR); print('sfx',len(cues))
