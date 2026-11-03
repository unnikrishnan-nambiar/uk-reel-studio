"""Word timings with free open models (sherpa-onnx). English -> Parakeet; any other language -> Omnilingual (1600+ languages).
usage: python3 transcribe.py <audio16k.wav> <out_words.json> [--chars out_chars.json]
Prints the transcript with indexes and start times. Times are seconds."""
import sherpa_onnx, soundfile as sf, numpy as np, json, sys, os
M=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'models');ENV={'asr':'omni' if os.path.exists(M+'/omni/tokens.txt') else 'none'}; a,sr=sf.read(sys.argv[1],dtype='float32')
if ENV['asr']=='parakeet':
    d=M+'/parakeet/'
    rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder.int8.onnx',decoder=d+'decoder.int8.onnx',joiner=d+'joiner.int8.onnx',tokens=d+'tokens.txt',model_type='nemo_transducer',num_threads=2)
    joiner=lambda tok: tok.startswith(' ')
elif ENV['asr']=='omni':
    d=M+'/omni/'; rec=sherpa_onnx.OfflineRecognizer.from_omnilingual_asr_ctc(model=d+'model.int8.onnx',tokens=d+'tokens.txt',num_threads=2)
    joiner=None
else: sys.exit('No speech model in models/omni. Run ./setup.sh first.')
# split at quiet points so each chunk is <= ~12 s
hop=sr//100; db=20*np.log10(np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0,len(a)-hop,hop)])+1e-9)
cuts=[0]; last=0
while last < len(db)-1200:
    lo,hi=last+600,min(last+1200,len(db)-1); k=lo+int(np.argmin(db[lo:hi])); cuts.append(k); last=k
cuts.append(len(db)); W=[]; C=[]
for c0,c1 in zip(cuts[:-1],cuts[1:]):
    t0=c0/100; s=rec.create_stream(); s.accept_waveform(sr,a[int(c0*hop):int(c1*hop)]); rec.decode_stream(s); r=s.result
    cur=None
    for tok,t in zip(r.tokens,r.timestamps):
        tt=round(t0+t,2); C.append([tok,tt])
        if joiner:  # parakeet: new word when token starts with a space
            if joiner(tok) or cur is None:
                if cur: W.append(cur)
                cur={'w':tok.strip(),'s':tt}
            else: cur['w']+=tok
        else:       # omnilingual: characters, blank token = word break
            if tok.strip()=='':
                if cur: W.append(cur); cur=None
                continue
            if cur is None: cur={'w':tok,'s':tt}
            else: cur['w']+=tok
    if cur: W.append(cur)
json.dump(W,open(sys.argv[2],'w'),ensure_ascii=False)
if '--chars' in sys.argv: json.dump(C,open(sys.argv[sys.argv.index('--chars')+1],'w'),ensure_ascii=False)
print(' '.join(w['w'] for w in W)); print(); print(' '.join(f"{i}:{w['w']}@{w['s']}" for i,w in enumerate(W)))
