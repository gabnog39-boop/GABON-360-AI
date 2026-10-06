#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARK='<!-- GABON360-MOBILE-RUNTIME-FIX-V2 -->'
PAYLOAD=r'''<!-- GABON360-MOBILE-RUNTIME-FIX-V2 -->
<style>
/* V2: dedicated Android WebView scroll host. */
html,body{width:100%!important;height:100%!important;max-width:100%!important;overflow:hidden!important;margin:0!important;padding:0!important}
#g360-mobile-scroll-host{position:relative!important;width:100%!important;height:100dvh!important;max-height:100dvh!important;overflow-y:auto!important;overflow-x:hidden!important;-webkit-overflow-scrolling:touch!important;overscroll-behavior-y:contain!important;touch-action:pan-y!important;box-sizing:border-box!important}
#g360-mobile-scroll-host>*{max-width:100%!important;box-sizing:border-box!important}
/* Keep the central avatar and dialogs above the scroll host. */
#g360-avatar-launch,#g360-avatar-home-dock,#g360-avatar-mic-dock,#g360-terrain-nav,#g360-terrain-modal,#g360-pages-modal,#g360-cm-modal,#g360-avatar-modal{z-index:2147483000!important}
#g360-avatar-launch{position:fixed!important;left:12px!important;bottom:96px!important;width:76px!important;height:76px!important;display:block!important;visibility:visible!important;opacity:1!important;border-radius:50%!important;padding:0!important;overflow:hidden!important;pointer-events:auto!important}
#g360-avatar-launch img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;border-radius:50%!important}
#g360-avatar-mic-dock{position:fixed!important;left:94px!important;bottom:104px!important;display:flex!important;gap:6px!important;z-index:2147483001!important}
#g360-avatar-mic-dock button{width:48px!important;height:48px!important;border-radius:50%!important;border:1px solid #31506d!important;background:#0b1a2a!important;color:#fff!important;font-size:22px!important;box-shadow:0 8px 20px #0009!important}
#g360-avatar-mic-status{position:fixed!important;left:94px!important;bottom:74px!important;background:#071522!important;color:#d9f7ea!important;border:1px solid #31506d!important;border-radius:8px!important;padding:4px 7px!important;font:11px system-ui,sans-serif!important;z-index:2147483001!important}
</style>
<script>
(function(){
  function fixedish(el){
    if(!el||!el.id)return false;
    return /modal|avatar-launch|avatar-home-dock|terrain-nav|terrain-modal|pages-modal|cm-modal|mic-dock|mic-status/.test(el.id);
  }
  function makeScrollHost(){
    if(document.getElementById('g360-mobile-scroll-host')) return document.getElementById('g360-mobile-scroll-host');
    var body=document.body; if(!body)return null;
    var host=document.createElement('div'); host.id='g360-mobile-scroll-host';
    var nodes=Array.prototype.slice.call(body.children);
    nodes.forEach(function(el){
      var tag=(el.tagName||'').toLowerCase();
      if(tag==='script'||tag==='style'||tag==='link'||tag==='meta'||tag==='title'||fixedish(el)) return;
      host.appendChild(el);
    });
    body.insertBefore(host,body.firstChild);
    return host;
  }
  function unlock(){
    var h=makeScrollHost(),b=document.body,d=document.documentElement;
    if(!h||!b||!d)return;
    d.style.setProperty('overflow','hidden','important');
    b.style.setProperty('overflow','hidden','important');
    b.style.setProperty('height','100%','important');
    h.style.setProperty('height','100dvh','important');
    h.style.setProperty('max-height','100dvh','important');
    h.style.setProperty('overflow-y','auto','important');
    h.style.setProperty('overflow-x','hidden','important');
    h.style.setProperty('touch-action','pan-y','important');
  }
  function moveAvatarToBody(){
    var a=document.getElementById('g360-avatar-launch');
    if(a && a.parentElement!==document.body) document.body.appendChild(a);
    if(a){a.style.setProperty('position','fixed','important');a.style.setProperty('display','block','important');a.style.setProperty('visibility','visible','important');a.style.setProperty('opacity','1','important');a.style.setProperty('z-index','2147483000','important');}
    var modal=document.getElementById('g360-avatar-modal');
    if(!a && modal){
      var im=modal.querySelector('img')||document.querySelector('img[alt*="avatar" i],img[alt*="IA" i]');
      if(im){
        a=document.createElement('button');a.id='g360-avatar-launch';a.type='button';a.setAttribute('aria-label','Ouvrir l IA centrale');
        a.appendChild(im.cloneNode(true));
        a.onclick=function(){modal.style.setProperty('display','flex','important');modal.style.setProperty('visibility','visible','important');modal.style.setProperty('opacity','1','important');};
        document.body.appendChild(a);
      }
    }
  }
  function installMic(){
    if(document.getElementById('g360-avatar-mic-dock')) return;
    var dock=document.createElement('div');dock.id='g360-avatar-mic-dock';
    var mic=document.createElement('button');mic.id='g360-avatar-mic';mic.type='button';mic.textContent='🎙️';mic.setAttribute('aria-label','Parler à l IA');
    dock.appendChild(mic);document.body.appendChild(dock);
    var st=document.createElement('div');st.id='g360-avatar-mic-status';st.textContent='Micro prêt';document.body.appendChild(st);
    var Rec=window.SpeechRecognition||window.webkitSpeechRecognition;
    var rec=null,listening=false;
    function fillCommand(text){
      var input=document.querySelector('#g360-ai-command input, input#g360-ai-command, textarea#g360-ai-command, input[placeholder*="commande" i], textarea[placeholder*="commande" i]');
      if(input){input.value=text;input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}));}
      window.dispatchEvent(new CustomEvent('gabon360:ai-command',{detail:{text:text,source:'microphone'}}));
      var low=text.toLowerCase();
      if(/navigation terrain|navigation du terrain/.test(low)){var b=document.getElementById('g360-terrain-open');if(b)b.click();}
      if(/retour.*accueil|accueil/.test(low)){window.scrollTo&&window.scrollTo(0,0);var h=document.getElementById('g360-mobile-scroll-host');if(h)h.scrollTop=0;}
    }
    if(!Rec){st.textContent='Reconnaissance vocale indisponible';mic.textContent='🎙️';mic.disabled=true;return;}
    rec=new Rec();rec.lang='fr-FR';rec.continuous=false;rec.interimResults=false;
    rec.onstart=function(){listening=true;mic.textContent='⏹️';st.textContent='Écoute en cours…';};
    rec.onend=function(){listening=false;mic.textContent='🎙️';st.textContent='Micro prêt';};
    rec.onerror=function(e){listening=false;mic.textContent='🎙️';st.textContent='Micro: '+(e.error||'erreur');};
    rec.onresult=function(e){var t='';for(var i=e.resultIndex;i<e.results.length;i++)t+=e.results[i][0].transcript+' ';t=t.trim();if(t){st.textContent='Commande reçue';fillCommand(t);}};
    mic.onclick=function(){if(listening){rec.stop();return;}try{rec.start();}catch(e){st.textContent='Micro: autorisation requise';}};
  }
  function mapTouchBridge(){
    var host=document.getElementById('g360-mobile-scroll-host');if(!host)return;
    document.querySelectorAll('.leaflet-container').forEach(function(map){if(map.dataset.g360TouchBridge)return;map.dataset.g360TouchBridge='1';var y=0,x=0;
      map.addEventListener('touchstart',function(e){if(e.touches.length===1){y=e.touches[0].clientY;x=e.touches[0].clientX;}},{passive:true});
      map.addEventListener('touchmove',function(e){if(e.touches.length!==1)return;var dy=e.touches[0].clientY-y,dx=e.touches[0].clientX-x;if(Math.abs(dy)>Math.abs(dx)&&Math.abs(dy)>3){host.scrollTop-=dy;y=e.touches[0].clientY;e.preventDefault();}},{passive:false});
    });
  }
  function boot(){unlock();moveAvatarToBody();installMic();mapTouchBridge();}
  boot();window.addEventListener('load',boot);window.addEventListener('resize',unlock);
  var n=0,t=setInterval(function(){boot();if(++n>30)clearInterval(t)},300);
  window.GABON360_MOBILE_RUNTIME_V2={version:'2.0',dedicatedScrollHost:true,avatarRelocated:true,microphoneLauncher:true,mapVerticalScrollBridge:true};
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts))
    if not candidates: raise SystemExit('No index.html found')
    for p in candidates:
        text=p.read_text(encoding='utf-8')
        if MARK in text:
            print('already:',p); return
        i=text.lower().rfind('</body>')
        if i<0: continue
        p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__': main()
