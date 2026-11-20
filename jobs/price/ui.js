const CHEK='<svg width="54" height="54" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#45dd6c"/><path d="M6.5 12.5l3.5 3.5 7.5-8" stroke="#0d0d0d" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const LINK='<svg width="40" height="40" viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" stroke="#0d0d0d" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>';
function chart(key,w,h,col,id){const d=CH[key],mn=Math.min(...d),mx=Math.max(...d),pad=14;
  const X=i=>pad+i*(w-2*pad)/(d.length-1),Y=v=>pad+(mx-v)*(h-2*pad)/((mx-mn)||1);
  let pth='M'+d.map((v,i)=>X(i).toFixed(1)+' '+Y(v).toFixed(1)).join(' L');
  const li=d.indexOf(mn);
  return {svg:`<svg width="${w}" height="${h}" style="overflow:visible"><defs><linearGradient id="g${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity=".55"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient><clipPath id="c${id}"><rect id="cr${id}" x="0" y="-20" width="0" height="${h+40}"/></clipPath></defs>
   <g clip-path="url(#c${id})"><path d="${pth} L${X(d.length-1)} ${h} L${X(0)} ${h} Z" fill="url(#g${id})"/><path d="${pth}" fill="none" stroke="${col}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/></g>
   <circle id="lo${id}" cx="${X(li)}" cy="${Y(mn)}" r="14" fill="#45dd6c" stroke="#0d0d0d" stroke-width="4" opacity="0"/></svg>`,lx:X(li),ly:Y(mn),w}}
function drawChart(id,s,a,dur,w){const r=$('cr'+id);if(r)r.setAttribute('width',w*eo(p(s,a,dur)))}
function ui(s,c){const k=c[4],el=$('ui'),a=c[0];let h='';
 if(k==='h1'||k==='h2'){h=`<img class="a" src="snip/spk_cut.png" style="left:640px;top:470px;width:400px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5))">`}
 if(k==='tags'){h=['SALE','50% OFF','60% OFF'].map((t,i)=>`<div class="win a" style="left:${70+i*330}px;top:${310+(i%2)*60}px;transform-origin:center"><span class="pill" style="font-size:44px;padding:16px 28px;transform:rotate(${[-6,4,-3][i]}deg)">${t}</span></div>`).join('')}
 if(k==='later'){h=`<div class="win a" style="left:90px;top:270px"><span class="pill" style="font-size:40px;background:#ff4b72;color:#fff">YOU BOUGHT</span></div>
   <svg id="arr" class="a" style="left:330px;top:350px" width="420" height="260"><path d="M20 20 C 180 20, 240 230, 390 230" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="100" id="arp" style="filter:drop-shadow(0 0 3px #000)"/></svg>
   <div class="win a" id="lat" style="left:620px;top:560px"><span class="pill" style="font-size:40px;background:#45dd6c">PRICE DROPPED</span></div>`}
 if(k.startsWith('ch:')){const key=k.slice(3),C=chart(key,940,360,key==='fryer'?'#FFD84D':'#ff4b72','m');
   h=`<div class="win a" style="left:70px;top:250px">${C.svg}</div>`
    +(key==='fryer'?`<div class="win a" id="lol" style="left:${70+C.lx-40}px;top:${250+C.ly+30}px"><span class="pill" style="font-size:34px;background:#45dd6c">LOWEST ₹4,854</span></div>`:
      `<div class="win a" id="up" style="left:120px;top:205px"><span class="pill" style="font-size:32px;background:#ff4b72;color:#fff">PRICE UP ↑</span></div><div class="win a" id="dn" style="left:600px;top:640px"><span class="pill" style="font-size:32px;background:#45dd6c">"SALE" PRICE ↓</span></div>`)}
 if(k==='sched'){h=`<div class="win a" style="left:160px;top:250px"><img src="snip/sched.png" style="width:760px;border-radius:28px;display:block"></div>
   <div class="a" style="left:0;right:0;top:600px;text-align:center;font:800 64px IN;text-shadow:0 3px 14px rgba(0,0,0,.8)">Price watch · <span style="color:#FFD84D">every day</span></div>`}
 if(k==='prompt'){h=`<div class="win a" style="left:0;right:0;top:300px;text-align:center"><span class="pill" style="font-size:48px;padding:18px 34px">THE PROMPT</span></div>
   <div class="a" style="left:0;right:0;top:420px;text-align:center;font:800 90px/1 IN;text-shadow:0 3px 14px rgba(0,0,0,.8)">+</div>
   <div class="win a" style="left:0;right:0;top:540px;text-align:center"><span class="pill" style="font-size:42px;padding:16px 30px;background:#fff">${LINK}flipkart.com/jbl-flip-7</span></div>`}
 if(k==='notif'){h=`<div class="a" id="ban" style="left:70px;top:260px;width:940px;border-radius:40px;background:rgba(245,245,247,.97);color:#0d0d0d;padding:28px 34px;box-sizing:border-box;box-shadow:0 20px 50px rgba(0,0,0,.45)">
   <div style="font:700 28px IN;color:#666;letter-spacing:.04em">ChatGPT · now</div><div style="font:800 46px/1.2 IN;margin-top:8px">Price drop: JBL Flip 7</div><div style="font:700 36px/1.3 IN;color:#333;margin-top:6px">Lowest price with your card offer. Buy now.</div></div>`}
 if(k==='order'){h=`<div class="win a" style="left:90px;top:240px"><div style="position:relative"><img src="snip/order.png" style="width:900px;border-radius:26px;display:block"><div id="hl" class="a" style="left:10px;right:10px;bottom:6px;height:78px;background:rgba(255,216,77,.6);mix-blend-mode:multiply;transform-origin:left;border-radius:10px"></div></div></div>`}
 if(k==='alertcard'){h=['Card offers you can apply','Price chart','Price history'].map((t,i)=>`<div class="a" id="r${i}" style="left:110px;top:${290+i*120}px;display:flex;align-items:center;gap:24px;font:800 58px IN;text-shadow:0 3px 14px rgba(0,0,0,.8)">${CHEK}${t}</div>`).join('')}
 if(k==='three'){const it=[['watch','WATCH','₹15,500','#ff4b72'],['shoes','SHOES','₹4,347','#ff4b72'],['fryer','AIR FRYER','₹4,854','#FFD84D']];
   h=it.map(([key,nm,lo,col],i)=>{const C=chart(key,300,200,col,'t'+i);return `<div class="a" id="tc${i}" style="left:${45+i*340}px;top:250px;width:310px;text-align:center"><div style="font:800 44px IN;margin-bottom:12px;text-shadow:0 3px 12px rgba(0,0,0,.8)">${nm}</div><div class="win" style="display:inline-block">${C.svg}</div><div style="margin-top:14px"><span class="pill" style="font-size:28px;background:#45dd6c">LOWEST ${lo}</span></div></div>`}).join('')}
 if(k==='toggle'){h=`<div class="a" style="left:0;right:0;top:330px;display:flex;align-items:center;justify-content:center;gap:40px"><span style="font:800 64px IN;text-shadow:0 3px 14px rgba(0,0,0,.8)">Price watch</span><div id="tg" style="width:190px;height:108px;border-radius:54px;background:#34c759;position:relative;box-shadow:0 10px 30px rgba(0,0,0,.4)"><div id="kn" style="position:absolute;top:8px;left:90px;width:92px;height:92px;border-radius:50%;background:#fff"></div></div></div>`}
 if(k==='wa'){h=`<div class="a" style="left:0;right:0;top:280px;display:flex;justify-content:center"><svg width="300" height="300" viewBox="0 0 24 24" style="filter:drop-shadow(0 14px 30px rgba(0,0,0,.5))"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z" fill="#25D366"/><path d="M8.6 7.2c.3-.6.6-.6.9-.6h.6c.2 0 .5 0 .7.6l.9 2.1c.1.3 0 .5-.1.7l-.6.7c-.2.2-.2.4 0 .7.6 1 1.6 2 2.8 2.6.3.1.5.1.7-.1l.7-.8c.2-.3.5-.3.7-.2l2 .9c.3.1.4.3.4.6 0 .9-.6 1.8-1.6 2-1 .3-3.2-.2-5.2-2-2.2-2-2.9-4.1-2.9-5 0-.7.3-1.6.8-2.2z" fill="#fff"/></svg></div>`}
 if(k==='wa2'){h=`<div class="a" style="left:80px;right:80px;top:250px;display:flex;flex-direction:column;gap:22px">
   <div class="bub" id="m1" style="align-self:flex-end;background:#d9fdd3;color:#0d0d0d;font-size:36px">Track this price for me: flipkart.com/jbl-flip-7</div>
   <div class="bub" id="m2" style="align-self:flex-start;background:#fff;color:#0d0d0d;font-size:36px"><b style="color:#128C7E">Instinct</b><br>Price dropped! Buy now?</div></div>`}
 if(k==='comment'){h=`<div class="a" style="left:90px;top:300px;width:900px;height:110px;border-radius:999px;background:rgba(30,30,50,.8);box-shadow:0 0 0 2px rgba(255,255,255,.18);display:flex;align-items:center;gap:22px;padding:0 34px;box-sizing:border-box"><span style="width:58px;height:58px;border-radius:50%;background:conic-gradient(#ff4b72,#9a6bff,#2fd0f2,#ffc21f,#ff4b72)"></span><span id="cmt" style="font:800 46px IN;color:#FFD84D"></span><span id="cur" style="width:4px;height:50px;background:#fff"></span></div>`}
 if(k==='fs'){h=`<div class="a" style="left:0;right:0;top:300px;display:flex;justify-content:center;gap:26px"><span class="btn" id="bS" style="background:#FFD84D;color:#0d0d0d"><svg width="40" height="40" viewBox="0 0 24 24"><path d="M3 11 L21 3 L14 21 L11 13 Z" fill="#0d0d0d"/></svg>SEND TO A FRIEND</span></div>`}
 if(el.dataset.k!==k+a){el.dataset.k=k+a;el.innerHTML=h}
 const lt=s-a;
 [...el.children].forEach((e,i)=>{const st=(k==='three'||k==='alertcard'||k==='wa2'||k==='later')?99:a+.03+i*.12;const q=p(s,st,.32);
   if(st<99){e.style.opacity=eo(q)*cl((c[1]-s)/.12);e.style.transform=`translateY(${(1-eo(q))*50}px) scale(${.85+.15*back(q)})`}else e.style.opacity=cl((c[1]-s)/.12)});
 if(k.startsWith('ch:')){drawChart('m',s,a+.2,2.4,940);const fr=k==='ch:fryer';
   if(fr){const q=back(p(s,a+2.4,.35));$('lol').style.opacity=cl(q);$('lol').style.transform=`scale(${q})`;$('lom').setAttribute('opacity',cl(q))}
   else{[['up',a+1.0],['dn',a+2.3]].forEach(([id,t])=>{const q=back(p(s,t,.35));$(id).style.opacity=cl(q)*cl((c[1]-s)/.12);$(id).style.transform=`scale(${q})`})}}
 if(k==='later'){const sh=(id,t)=>{const q=back(p(s,t,.3));$(id).style.opacity=cl(q);$(id).style.transform=`scale(${q})`};
   el.children[0].style.opacity=eo(p(s,a,.3));$('arp').setAttribute('stroke-dashoffset',100-100*eo(p(s,18.4,1.2)));sh('lat',19.7)}
 if(k==='three'){[61.2,61.7,62.1].forEach((t,i)=>{const q=p(s,t,.35);$('tc'+i).style.opacity=eo(q)*cl((c[1]-s)/.12);$('tc'+i).style.transform=`translateY(${(1-eo(q))*50}px)`;drawChart('t'+i,s,t+.1,1.4,300);$('lot'+i).setAttribute('opacity',cl(p(s,t+1.5,.2)))})}
 if(k==='alertcard'){[55.6,57.9,58.5].forEach((t,i)=>{const q=p(s,t,.3);$('r'+i).style.opacity=eo(q)*cl((c[1]-s)/.12);$('r'+i).style.transform=`translateX(${(1-eo(q))*-60}px)`})}
 if(k==='wa2'){[['m1',77.0],['m2',79.6]].forEach(([id,t])=>{const q=p(s,t,.3);$(id).style.opacity=eo(q)*cl((c[1]-s)/.12);$(id).style.transform=`translateY(${(1-eo(q))*40}px)`})}
 if(k==='notif'){const q=eo(p(s,a+.05,.35));$('ban').style.transform=`translateY(${(1-q)*-200}px)`}
 if(k==='order'){$('hl').style.transform=`scaleX(${eo(p(s,52.8,.6))})`}
 if(k==='toggle'){const on=s<a+.9;$('tg').style.background=on?'#34c759':'#8e8e93';$('kn').style.left=(on?90:8)+(on?0:0)+'px'}
 if(k==='comment'){$('cmt').textContent='PRICE'.slice(0,Math.floor(cl((lt-.4)/.6)*5));$('cur').style.opacity=(Math.floor(s*3)%2)?1:0}
 if(k==='fs'){$('bS').style.transform=`scale(${lt>1.0&&lt<1.15?.93:1})`}
}
