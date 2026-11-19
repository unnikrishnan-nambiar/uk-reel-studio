import re, json, segs
src=open('../wifi3/overlay.html',encoding='utf-8').read()
head=src[:src.index('<script>')]
head=head.replace('<div id="bot" class="word"></div>','<div id="bot" class="word"></div>\n  <div id="top2" class="word"></div>')
head=head.replace('</style>','''.glass{position:absolute;border-radius:52px;padding:16px;box-sizing:border-box;
 background:linear-gradient(135deg,rgba(255,255,255,.42),rgba(255,255,255,.10) 45%,rgba(255,255,255,.22));
 border:2px solid rgba(255,255,255,.65);box-shadow:inset 0 2px 0 rgba(255,255,255,.85),inset 0 -2px 6px rgba(255,255,255,.25),0 24px 60px rgba(0,0,0,.35)}
.glass img{display:block;width:100%;border-radius:38px}
.glass::after{content:"";position:absolute;left:8%;top:6px;width:55%;height:22%;border-radius:40px;background:linear-gradient(180deg,rgba(255,255,255,.55),rgba(255,255,255,0));pointer-events:none}
.gtext{font:800 46px IN;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.35)}
#fsimg{left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.dark{background:linear-gradient(135deg,rgba(25,35,60,.62),rgba(10,15,30,.45))!important}
</style>''')
js=src[src.index('<script>'):]
js=re.sub(r'const SEGS=\[.*?\];',f'const SEGS={json.dumps(segs.ALL)};',js,flags=re.S)
js=re.sub(r'const CUES=\[.*?\]\];',lambda m:open('cues.js',encoding='utf-8').read(),js,flags=re.S)
js=re.sub(r'const HOOK=\{.*?\};',lambda m:"const HOOK={h1:'Claude made my iPhone widget<br>in 2 minutes.',h2:'Now anyone can make<br>an iPhone widget with Claude.',h3:'No coding. Make your own<br>working iPhone widget.'};",js,flags=re.S)
js=re.sub(r'const SUB=\[.*?\]\];',lambda m:open('sub.js',encoding='utf-8').read(),js,flags=re.S)
u0=js.index('const APPS='); u1=js.index('window.setCaps')
js=js[:u0]+open('ui.js',encoding='utf-8').read()+js[u1:]
js=js.replace("""  if(c[3]){setWord(bt""","""  const t2=$('top2');if(c[2]){setWord(t2,c[2],200,980);t2.style.top='210px';animWord(t2,s,c[0]+.1,c[1])}else{t2.innerHTML='';t2.dataset.k=''}
  if(c[3]){setWord(bt""")
js=js.replace("if(c[4]&&!hk)return ui(s,c);else{$('ui').innerHTML='';$('ui').dataset.k=''}","if(hk)return ui(s,[c[0],c[1],'','','hookw']);if(c[4])return ui(s,c);$('ui').innerHTML='';$('ui').dataset.k=''")
js=js.replace("if(!c){bt.innerHTML='';bt.dataset.k='';$('ui')","if(!c){bt.innerHTML='';bt.dataset.k='';$('top2').innerHTML='';$('top2').dataset.k='';$('ui')")
assert "hookw" in js and "top2" in js
open('overlay.html','w',encoding='utf-8').write(head+js)
print('ok')
