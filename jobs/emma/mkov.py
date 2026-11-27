import re, json, segs
src=open('../speak/overlay.html',encoding='utf-8').read()
src=src.replace('#hook{left:50%;top:190px','#hook{left:50%;top:230px').replace('.word{position:absolute;left:0;right:0;','.word{position:absolute;left:60px;right:140px;').replace('#sub{left:80px;right:140px;top:1370px','#sub{left:80px;right:150px;top:1370px')
head=src[:src.index('<script>')]; js=src[src.index('<script>'):]
js=re.sub(r'const SEGS=\[.*?\];',f'const SEGS={json.dumps(segs.ALL)};',js,flags=re.S)
js=re.sub(r'const CUES=\[.*?\]\];',lambda m:open('cues.js',encoding='utf-8').read(),js,flags=re.S)
js=re.sub(r'const HOOK=\{.*?\};',lambda m:"const HOOK={h1:'Don\\'t trust Nora. She cheated me.<br>She\\'s AI, not a human.'};",js,flags=re.S)
js=re.sub(r'const SUB=\[.*?\]\];',lambda m:open('sub.js',encoding='utf-8').read(),js,flags=re.S)
u0=js.index('function win('); u1=js.index('window.setCaps')
js=js[:u0]+open('icons.js',encoding='utf-8').read()+'\n'+open('logos.js',encoding='utf-8').read()+'\n'+open('helpers.js',encoding='utf-8').read()+open('ui.js',encoding='utf-8').read()+js[u1:]
js=js.replace("if(c[4]&&!hk)return ui(s,c);else{$('ui').innerHTML='';$('ui').dataset.k=''}","if(c[4])return ui(s,c);$('ui').innerHTML='';$('ui').dataset.k=''")
assert 'if(c[4])return ui(s,c)' in js
js=js.replace("setWord(bt,c[3],c[3].length>9?120:160,960)","setWord(bt,c[3],c[3].length>9?110:150,820)")
open('overlay.html','w',encoding='utf-8').write(head+js); print('ok')
