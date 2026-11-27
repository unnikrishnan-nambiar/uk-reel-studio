import re, json, segs
src=open('../speak/overlay.html',encoding='utf-8').read()
src=src.replace('#hook{left:50%;top:190px','#hook{left:50%;top:230px')
head=src[:src.index('<script>')]; js=src[src.index('<script>'):]
js=re.sub(r'const SEGS=\[.*?\];',f'const SEGS={json.dumps(segs.ALL)};',js,flags=re.S)
js=re.sub(r'const CUES=\[.*?\]\];',lambda m:open('cues.js',encoding='utf-8').read(),js,flags=re.S)
js=re.sub(r'const HOOK=\{.*?\};',lambda m:"const HOOK={h1:'Don\\'t share Claude chats.<br>Your secret data is public online.',h2:'Don\\'t share Claude chats. Anyone<br>can get your secret data online.',h3:'Don\\'t share Claude chats. Anyone<br>can find your secret data easily.'};",js,flags=re.S)
js=re.sub(r'const SUB=\[.*?\]\];',lambda m:open('sub.js',encoding='utf-8').read(),js,flags=re.S)
u0=js.index('function win('); u1=js.index('window.setCaps')
js=js[:u0]+open('icons.js',encoding='utf-8').read()+'\n'+open('logos.js',encoding='utf-8').read()+'\n'+open('ui.js',encoding='utf-8').read()+js[u1:]
js=js.replace("if(c[4]&&!hk)return ui(s,c);else{$('ui').innerHTML='';$('ui').dataset.k=''}","if(c[4])return ui(s,c);$('ui').innerHTML='';$('ui').dataset.k=''")
assert 'if(c[4])return ui(s,c)' in js
open('overlay.html','w',encoding='utf-8').write(head+js); print('ok')
