// ===== Variant animations (V2 = red-alert, face-level; V3 = white cards / search) =====
const WC=(inner,st)=>`<div class="a" style="${st};border-radius:34px;background:#fff;color:#0d0d0d;box-shadow:0 0 0 6px #0d0d0d,0 16px 40px rgba(0,0,0,.45);overflow:hidden">${inner}</div>`;
const WFS=inner=>`<div class="a fsc" style="inset:0;background:#f4f4f6;background-image:linear-gradient(rgba(0,0,0,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,0,.05) 2px,transparent 2px);background-size:60px 60px">${inner}</div>`;
const SVI=(n,sz,col='#0d0d0d',sw=2)=>`<svg width="${sz}" height="${sz}" viewBox="0 0 24 24" fill="none" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${TI[n]}</svg>`;
const ROW=(icon,txt,id,col='#0d0d0d',extra='')=>`<div id="${id}" style="display:flex;align-items:center;gap:20px;padding:16px 26px;border-top:2px solid #eee;opacity:0">${SVI(icon,52,col)}<span style="font:700 40px IN;color:#0d0d0d">${txt}</span>${extra}</div>`;
const TG=(id,on=true)=>`<span id="${id}" style="margin-left:auto;width:110px;height:60px;border-radius:30px;background:${on?'#45dd6c':'#c9c9d6'};position:relative;border:4px solid #0d0d0d;flex:none"><i style="position:absolute;top:4px;left:${on?'52px':'4px'};width:44px;height:44px;border-radius:50%;background:#fff;border:3px solid #0d0d0d"></i></span>`;
const setTG=(id,off)=>{const e=$(id);if(!e)return;e.style.background=off>.5?'#c9c9d6':'#45dd6c';e.firstElementChild.style.left=(52-48*off)+'px'};
const SC3=(nm,chip)=>`<div class="a fsc" style="inset:0;background:#f4f4f6;background-image:linear-gradient(rgba(0,0,0,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,0,.05) 2px,transparent 2px);background-size:60px 60px"><div id="ph3" style="position:absolute;left:216px;top:150px;width:648px;height:1152px;border-radius:56px;border:16px solid #0d0d0d;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.35);background:#fff"><div id="kb" style="position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;transform:scale(.6)"><img id="scr" src="snip/${nm}/001.jpg" style="position:absolute;left:0;top:0;width:1080px;height:1920px"><div id="hl" style="position:absolute;border:12px solid #FFD84D;border-radius:30px;box-shadow:0 0 0 6px #0d0d0d;opacity:0"></div></div></div>${chip?`<div class="a" id="stp" style="left:0;right:0;top:1790px;text-align:center">${chip}</div>`:''}</div>`;
function uiAlt(s,c){const k=c[4],el=$('ui'),a=c[0],b=c[1],V=VAR;let h=null;const lt=s-a,P=cl((s-a)/(b-a));
 const pop=(id,t,d=.35)=>{const q=back(p(s,t,d));const e=$(id);if(!e)return;e.style.opacity=cl(q*2);e.style.transform=`scale(${Math.max(.01,q)})`};
 const show=(id,t,d=.3,dy=30)=>{const e=$(id);if(!e)return;const q=eo(p(s,t,d));e.style.opacity=q;e.style.transform=`translateY(${(1-q)*dy}px)`};
 const fade=(id,t,d=.3)=>{const e=$(id);if(e)e.setAttribute('opacity',eo(p(s,t,d)))};
 const sg=(id,x,y,sc)=>{const e=$(id);if(e)e.setAttribute('transform',`translate(${x} ${y}) scale(${Math.max(.01,sc)}) translate(${-x} ${-y})`)};
 const type=(id,txt,t0,dur)=>{const e=$(id);if(e)e.textContent=txt.slice(0,Math.round(cl((s-t0)/dur)*txt.length))};
 const SCR=['FSreddit','FSpriv','FSshared','FSmemory','FSimprove'];
 // ---------- V2 : red alert, face-level ----------
 if(V==='v2'){
  if(k==='FSshare')h=SV(`${LO('claude',110,170,150,'cc2')}<g id="ar2" opacity="0">${I('share',290,170,90,'#fff')}</g><g id="lk2" opacity="0"><rect x="360" y="130" width="300" height="80" rx="40" fill="#FFD84D" stroke="#0d0d0d" stroke-width="6"/><text x="510" y="182" text-anchor="middle" font-family="IN" font-weight="800" font-size="32" fill="#0d0d0d">claude.ai/share/…</text></g><g id="gl2" opacity="0">${I('world',830,170,190,'#ff4b72','','#1b1b22')}</g>${[0,1,2,3,4].map(i=>`<g class="u2" opacity="0">${I('user',0,0,72,'#fff','','#1b1b22')}</g>`).join('')}<g id="lw2" opacity="0">${TX(480,420,'ANYONE CAN OPEN IT',60,'#ff4b72')}</g>`);
  if(k==='FSpdf')h=SV(`<g id="pd2">${I('file-type-pdf',190,190,190,'#ff4b72','','#1b1b22')}</g>${TX(190,390,'AI PRIVACY TIPS',38,'#fff')}<g id="cb2" opacity="0"><rect x="380" y="140" width="560" height="110" rx="55" fill="#fff" stroke="#0d0d0d" stroke-width="7"/>${LO('instagram',450,195,70)}<text id="ct2" x="510" y="215" font-family="IN" font-weight="800" font-size="54" fill="#0d0d0d"></text></g>`);
  if(k==='pers')h=SV([['photo','PHOTOS'],['id','NAMES'],['stethoscope','MEDICAL'],['building-bank','BANK']].map(([n,t],i)=>`<g id="q${i}" opacity="0">${I(n,130+i*235,170,120,'#fff','','#1b1b22')}<g class="al">${I('alert-triangle',180+i*235,110,56,'#ff4b72')}</g>${TX(130+i*235,330,t,36,'#ff4b72')}</g>`).join(''));
  if(k==='office')h=SV(`<g id="bf2">${I('briefcase',300,180,200,'#fff','','#1b1b22')}</g>${[0,1,2,3].map(i=>`<circle class="dp" r="16" fill="#ff4b72" stroke="#0d0d0d" stroke-width="4"/>`).join('')}<g id="ow2" opacity="0">${I('world',720,200,170,'#ff4b72','','#1b1b22')}</g>`);
  if(k==='thirty')h=SV(`<g id="sw2">${I('clock',330,200,230,'#FFD84D','','#1b1b22')}</g>${TX(680,250,'30 SEC',110,'#FFD84D','middle','t2')}`);
  if(k==='sens')h=SV(`${I('heart',230,200,140,'#ff4b72','','#1b1b22')}${I('pray',480,200,140,'#FFD84D','','#1b1b22')}<g id="lc2" opacity="0">${I('lock',730,200,150,'#45dd6c','','#1b1b22')}</g>`);
  if(k==='train')h=SV(`${[0,1,2,3,4,5].map(i=>`<g class="cv" opacity="0">${I(['message-circle','photo','file-text','id','message-2','user'][i],0,0,72,'#fff')}</g>`).join('')}<rect x="80" y="300" width="560" height="14" rx="7" fill="#555"/>${LO('claude',780,230,180,'tc2')}`);
  if(k==='years')h=SV(`${[0,1,2,3,4].map(i=>`<circle class="yd" cx="${200+i*140}" cy="170" r="50" fill="#1b1b22" stroke="#0d0d0d" stroke-width="8"/>`).join('')}${[0,1,2,3,4].map(i=>TX(200+i*140,190,String(i+1),56,'#fff')).join('')}${TX(480,340,'YEARS STORED',70,'#ff4b72','middle','yl2')}`);
  if(k==='money')h=SV(`<g id="ms2">${I('cash',300,200,220,'#45dd6c','','#1b1b22')}</g>${[0,1,2,3,4,5].map(i=>`<g class="c2" opacity="0">${I('coin',0,0,64,'#FFD84D')}</g>`).join('')}<g id="no2" opacity="0"><circle cx="700" cy="200" r="130" fill="#ff4b72" stroke="#0d0d0d" stroke-width="10"/>${TX(700,240,'NO',120,'#fff')}</g>`);
  if(k==='toggles')h=SV(['SHARED','SENSITIVE','TRAINING'].map((t,i)=>`<g transform="translate(150,${70+i*120})">${TX(0,30,t,56,'#fff','start')}<g id="xk${i}" opacity="0">${I('x',600,10,80,'#ff4b72')}</g><g id="ck${i}" opacity="0">${I('circle-check',600,10,80,'#45dd6c')}</g></g>`).join(''));
  if(k==='send')h=SV(`${I('share',200,200,160,'#FFD84D','','#1b1b22')}${[0,1,2,3].map(i=>`<g id="sf${i}" opacity="0">${I('user',520+i*120,140+(i%2)*120,100,'#2fd0f2','','#1b1b22')}</g>`).join('')}`);
 }
 // ---------- V3 : white cards / search ----------
 if(V==='v3'){
  const chips={FSreddit:'',FSpriv:'SETTINGS › PRIVACY',FSshared:'1 · SHARED → PRIVATE',FSmemory:'2 · SENSITIVE TOPICS → OFF',FSimprove:'3 · HELP IMPROVE AI → OFF'};
  if(SCR.includes(k))h=SC3({FSreddit:'reddit',FSpriv:'priv',FSshared:'shared',FSmemory:'memory',FSimprove:'improve'}[k],k==='FSreddit'?CH(`${LH('reddit',44,'vertical-align:-9px;margin-right:10px')}r/ClaudeAI · ${LH('google',40,'vertical-align:-8px;margin:0 10px')}search`,'#0d0d0d','#fff','','font-size:38px'):CH(chips[k],'#0d0d0d','#FFD84D','','font-size:40px'));
  if(k==='FSshare')h=WFS(`${WC(`<div style="display:flex;align-items:center;gap:18px;padding:26px 30px;border-bottom:3px solid #eee">${LH('google',60)}<span style="flex:1;font:700 42px IN;color:#0d0d0d;background:#f1f1f4;border-radius:999px;padding:16px 28px"><span id="q3"></span><span style="display:inline-block;width:4px;height:44px;background:#4285F4;vertical-align:-8px"></span></span></div>${[0,1,2,3].map(i=>`<div id="r3${i}" style="opacity:0;padding:22px 30px;border-bottom:2px solid #f0f0f0;${i==1?'background:#fff6d6':''}"><div style="display:flex;align-items:center;gap:14px">${LH('claude',40)}<span style="font:700 32px IN;color:#555">claude.ai › share</span>${i==1?'<span style="margin-left:auto;font:800 30px IN;color:#fff;background:#ff4b72;border-radius:999px;padding:6px 18px">YOUR CHAT</span>':''}</div><div style="font:700 40px IN;color:#1a0dab;margin-top:8px">claude.ai/share/${['75a5fcbc','ec8b0563','33dd4a49','0d877a61'][i]}…</div></div>`).join('')}`,'left:70px;top:200px;width:940px')}<div class="a" id="an3" style="left:0;right:0;top:1160px;text-align:center;opacity:0">${CH('ANYONE CAN OPEN IT','#ff4b72','#fff')}</div>`);
  if(k==='FSpdf')h=WFS(`${WC(`<div style="background:#0d0d0d;color:#FFD84D;font:800 48px IN;padding:30px 36px">AI PRIVACY TIPS</div>${['Shared links → private','Sensitive memory → off','Training → off','+ more tips'].map((t,i)=>ROW('circle-check',t,'pt'+i,'#45dd6c')).join('')}`,'left:120px;top:220px;width:840px')}<div class="a" id="cb3" style="left:90px;top:1000px;width:900px;height:120px;border-radius:999px;background:#fff;box-shadow:0 0 0 6px #0d0d0d;display:flex;align-items:center;gap:24px;padding:0 34px;box-sizing:border-box;opacity:0">${LH('instagram',66)}<span id="ct3" style="font:800 56px IN;color:#0d0d0d"></span><span style="margin-left:auto;font:800 38px IN;color:#FF0069">Post</span></div>`);
  if(k==='pers')h=WC(`<div style="display:flex;align-items:center;gap:16px;padding:20px 26px">${LH('claude',48)}<span style="font:800 40px IN">Uploading…</span></div>${[['photo','Family photos'],['id','Names & details'],['stethoscope','Medical history'],['building-bank','Bank history']].map(([n,t],i)=>ROW(n,t,'u3'+i,'#0d0d0d',`<span style="margin-left:auto">${SVI('circle-check',44,'#45dd6c',2.6)}</span>`)).join('')}`,'left:150px;top:150px;width:780px');
  if(k==='office')h=WC(`<div style="display:flex;align-items:center;gap:16px;padding:20px 26px">${SVI('briefcase',52)}<span style="font:800 40px IN">Office files</span></div>${['Q3_sales.xlsx','Client_list.pdf','Salary_sheet.xlsx'].map((t,i)=>ROW(i==1?'file-type-pdf':'file-type-xls',t,'f3'+i,i==1?'#EC1C24':'#34A853')).join('')}`,'left:180px;top:170px;width:720px');
  if(k==='thirty')h=WC(`<div style="padding:30px 36px"><div style="display:flex;justify-content:space-between;font:800 48px IN"><span>Fix it</span><span id="sc3">0s</span></div><div style="margin-top:22px;height:34px;border-radius:17px;background:#eee;border:4px solid #0d0d0d;overflow:hidden"><div id="pb3" style="height:100%;width:0;background:#FFD84D"></div></div></div>`,'left:170px;top:230px;width:740px');
  if(k==='sens')h=WC(`<div style="padding:20px 26px;font:800 40px IN">Claude's memory</div>${[['heart','Health'],['pray','Religion']].map(([n,t],i)=>ROW(n,t,'m3'+i,'#ff4b72',`<span style="margin-left:auto;font:800 32px IN;color:#fff;background:#0d0d0d;border-radius:999px;padding:8px 20px">NOT SAVED</span>`)).join('')}`,'left:190px;top:200px;width:700px');
  if(k==='train')h=WC(`<div style="padding:24px 30px;font:800 40px IN;display:flex;align-items:center;gap:16px">${LH('claude',48)}Help improve our AI models</div>${ROW('message-circle','Train on my chats','tr3','#0d0d0d',TG('tg3',true))}`,'left:110px;top:220px;width:860px');
  if(k==='years')h=SV(`<path d="M120 200 H840" stroke="#fff" stroke-width="10" stroke-linecap="round"/>${[0,1,2,3,4].map(i=>`<circle class="yd3" cx="${120+i*180}" cy="200" r="34" fill="#1b1b22" stroke="#0d0d0d" stroke-width="8"/>${TX(120+i*180,300,'YEAR '+(i+1),34,'#fff')}`).join('')}`);
  if(k==='money')h=WC(`<div style="padding:24px 30px;font:800 40px IN;display:flex;align-items:center;gap:16px">${LH('claude',48)}Help improve our AI models</div>${ROW('cash','They already made a lot','mo3','#45dd6c')}${ROW('message-circle','Train on my chats','tr3','#0d0d0d',TG('tg3',true))}`,'left:110px;top:200px;width:860px');
  if(k==='toggles')h=WC(['Shared links public','Sensitive memory','Train on my chats'].map((t,i)=>ROW(['link','brain','message-circle'][i],t,'tw'+i,'#0d0d0d',TG('tt'+i,true))).join(''),'left:110px;top:190px;width:860px');
  if(k==='send')h=WC(`<div style="padding:20px 26px;font:800 40px IN;display:flex;align-items:center;gap:14px">${LH('instagram',48)}Send to</div>${['Claude user 1','Claude user 2','Claude user 3'].map((t,i)=>ROW('user-circle',t,'d3'+i,'#0d0d0d',`<span style="margin-left:auto;font:800 32px IN;color:#fff;background:#0095f6;border-radius:14px;padding:10px 24px">Send</span>`)).join('')}`,'left:170px;top:190px;width:740px');
 }
 if(h===null)return null;
 {const sb=$('sub'),sc=SCR.includes(k)||(V==='v3'&&(k==='FSshare'||k==='FSpdf'));if(sb){sb.style.background=sc?'rgba(13,13,13,.88)':'';sb.style.borderRadius=sc?'24px':'';sb.style.boxShadow=sc?'0 0 0 14px rgba(13,13,13,.88)':'';sb.style.top=sc?'1620px':''}}
 if(el.dataset.k!==k+a+V){el.dataset.k=k+a+V;el.innerHTML=h}
 const out=cl((b-s)/.12);
 [...el.children].forEach((e,i)=>{if(e.classList.contains('fsc')){const q=eo(p(s,a,.16));e.style.opacity=q*out;e.style.transform=`scale(${1.06-.06*q})`;return}
   const q=p(s,a+.03+i*.08,.32);e.style.opacity=eo(q)*out;e.style.transform=V==='v2'?`translateX(${(1-eo(q))*-80}px) rotate(${(1-eo(q))*-4}deg)`:`translateY(${(1-eo(q))*-60}px) scale(${.92+.08*back(q)})`});
 // ----- animation -----
 if(V==='v2'){
  if(k==='FSshare'){pop('cc2',a+.1);fade('ar2',182.1,.2);fade('lk2',183.0,.25);fade('gl2',185.8,.25);const g=$('gl2');if(g)g.firstElementChild.firstElementChild.style.transform=`rotate(${lt*30}deg)`;document.querySelectorAll('.u2').forEach((e,i)=>{const q=back(p(s,187.0+i*.1,.3));e.setAttribute('transform',`translate(${640+i*80},${300+(i%2)*40}) scale(${Math.max(.01,q)})`);e.setAttribute('opacity',cl(q*2))});fade('lw2',187.4,.25)}
  if(k==='FSpdf'){const q=back(p(s,a+.1,.4));sg('pd2',190,190,q);fade('cb2',129.3,.3);type('ct2','PRIVACY',130.4,.6)}
  if(k==='pers'){[30.3,30.95,32.15,33.1].forEach((t,i)=>{fade('q'+i,t,.25);const al=$('q'+i).querySelector('.al');if(al)al.setAttribute('opacity',(Math.floor((s-t)*4)%2&&s>t+.4)?1:.35)})}
  if(k==='office'){document.querySelectorAll('.dp').forEach((e,i)=>{const f=((lt*.9)+i/4)%1;e.setAttribute('cx',300+f*420);e.setAttribute('cy',230+Math.sin(f*Math.PI)*-120+f*20);e.setAttribute('opacity',Math.sin(f*Math.PI))});fade('ow2',a+.6,.3)}
  if(k==='thirty'){$('sw2').firstElementChild.firstElementChild.style.transform=`rotate(${lt*180}deg)`;$('t2').style.transform=`scale(${.7+.3*back(p(s,a+.4,.35))})`}
  if(k==='sens'){fade('lc2',213.4,.25);const e=$('lc2');if(e)e.firstElementChild.firstElementChild.style.transform=`scale(${.5+.5*back(p(s,213.4,.35))})`}
  if(k==='train'){document.querySelectorAll('.cv').forEach((e,i)=>{const f=((lt*.6)+i/6)%1;e.setAttribute('transform',`translate(${100+f*560},250) scale(${1-f*.4})`);e.setAttribute('opacity',Math.sin(f*Math.PI))});$('tc2').style.transform=`scale(${1+.05*Math.sin(lt*8)})`}
  if(k==='years'){document.querySelectorAll('.yd').forEach((e,i)=>e.setAttribute('fill',s>a+.3+i*.3?'#ff4b72':'#1b1b22'))}
  if(k==='money'){document.querySelectorAll('.c2').forEach((e,i)=>{const t0=242.05+i*.15,f=cl((s-t0)/.6);e.setAttribute('transform',`translate(${220+i*35},${-30+eo(f)*200})`);e.setAttribute('opacity',f>0?1-f*.3:0)});fade('no2',243.55,.2);sg('no2',700,200,back(p(s,243.55,.35)))}
  if(k==='toggles'){[0,1,2].forEach(i=>{const t=246.5+i*.45;fade('xk'+i,a+.1,.2);if(s>t){$('xk'+i).setAttribute('opacity',0);fade('ck'+i,t,.2)}})}
  if(k==='send'){[0,1,2,3].forEach(i=>{fade('sf'+i,a+.4+i*.2,.2);sg('sf'+i,520+i*120,140+(i%2)*120,back(p(s,a+.4+i*.2,.35)))})}
 }
 if(V==='v3'){
  if(SCR.includes(k)){const nm={FSreddit:'reddit',FSpriv:'priv',FSshared:'shared',FSmemory:'memory',FSimprove:'improve'}[k];const n=SCN[nm];const fi=1+Math.min(n-1,Math.floor(P*(n-1)));const src='snip/'+nm+'/'+String(fi).padStart(3,'0')+'.jpg';
   $('ph3').style.transform=`rotate(${-3+3*eo(P)}deg) scale(${1+.03*P})`;
   const hl=$('hl');
   if(k==='FSreddit'){hl.style.opacity=eo(p(s,155.9,.25));if(s<157.6)BX(10,25,360,110);else BX(20,520,1040,880)}
   if(k==='FSpriv'){hl.style.opacity=eo(p(s,58.7,.25));BX(60,1070,960,240)}
   if(k==='FSshared'){if(P<48/147){hl.style.opacity=eo(p(s,a+.25,.2));BX(30,760,1020,290)}else{hl.style.opacity=1-eo(cl((P-.75)/.08));BX(640,1195,250,110)}}
   if(k==='FSmemory'){if(P<.38||P>.7){hl.style.opacity=eo(p(s,a+.2,.25));BX(40,940,1000,430)}else BX(80,1300,920,110)}
   if(k==='FSimprove'){hl.style.opacity=eo(p(s,a+.4,.25));if(P<.56)BX(30,1390,1020,140);else BX(30,820,1020,240)}
   const im=$('scr');if(!im.src.endsWith(src)){im.src=src;return im.decode().catch(()=>{})}}
  if(k==='FSshare'){type('q3','site:claude.ai/share',a+.3,1.3);[0,1,2,3].forEach(i=>show('r3'+i,182.0+i*.45,.3,20));show('an3',187.3,.3)}
  if(k==='FSpdf'){[0,1,2,3].forEach(i=>show('pt'+i,124.6+i*.5,.3,20));show('cb3',129.3,.3,40);type('ct3','PRIVACY',130.4,.6)}
  if(k==='pers'){[29.6,30.95,32.15,33.1].forEach((t,i)=>show('u3'+i,t,.3,20))}
  if(k==='office'){[0,1,2].forEach(i=>show('f3'+i,a+.4+i*.55,.3,20))}
  if(k==='thirty'){const f=cl((s-(a+.3))/(b-a-.5));$('pb3').style.width=(f*100)+'%';$('sc3').textContent=Math.round(f*30)+'s'}
  if(k==='sens'){[0,1].forEach(i=>show('m3'+i,212.8+i*.6,.3,20))}
  if(k==='train'){show('tr3',a+.3,.3,20)}
  if(k==='years'){document.querySelectorAll('.yd3').forEach((e,i)=>e.setAttribute('fill',s>a+.2+i*.3?'#FFD84D':'#1b1b22'))}
  if(k==='money'){show('mo3',242.05,.3,20);show('tr3',a+.3,.3,20);setTG('tg3',eo(p(s,243.9,.3)))}
  if(k==='toggles'){[0,1,2].forEach(i=>{show('tw'+i,a+.1+i*.12,.25,20);setTG('tt'+i,eo(p(s,246.6+i*.45,.3)))})}
  if(k==='send'){[0,1,2].forEach(i=>show('d3'+i,a+.3+i*.3,.3,20))}
 }
 return true}
