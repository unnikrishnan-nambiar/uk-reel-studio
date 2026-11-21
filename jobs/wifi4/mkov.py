import re, json, segs
s=open('overlay_src.html',encoding='utf-8').read()
s=re.sub(r'const SEGS=\[.*?\];',lambda m:'const SEGS='+json.dumps(segs.ALL)+';',s,count=1,flags=re.S)
s=re.sub(r'const SUB=\[.*?\]\];',lambda m:open('sub.js',encoding='utf-8').read().strip(),s,count=1,flags=re.S)
s=re.sub(r"const HOOK=\{.*?\};",lambda m:"const HOOK={h1:'1 Claude prompt doubled my wifi.<br>Don\\'t pay, your fix: free.'};",s,count=1,flags=re.S)
s=s.replace("[3.75,9.42,'','2X SPEED','h2'],[10.80,15.75,'','2X SPEED','h3'],","")
u0=s.index('const APPS='); u1=s.index('window.setCaps')
s=s[:u0]+open('ui.js',encoding='utf-8').read()+s[u1:]
open('overlay.html','w',encoding='utf-8').write(s); print('ok')
