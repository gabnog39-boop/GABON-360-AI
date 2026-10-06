#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re

MARK='<!-- GABON360-MOBILE-RUNTIME-FIX-V2 -->'
# Runtime V2 is intentionally kept in a standalone injector so the consolidated source remains reusable.
# It creates a dedicated WebView scroll host, keeps the avatar above the scroll layer,
# exposes a visible microphone control when browser speech recognition exists, and bridges
# vertical swipes that start on the Leaflet map to the page scroll host.
PAYLOAD=r'''<!-- GABON360-MOBILE-RUNTIME-FIX-V2 -->
<style>
html,body{width:100%!important;height:100%!important;max-width:100%!important;overflow:hidden!important;margin:0!important;padding:0!important}
#g360-mobile-scroll-host{position:relative!important;width:100%!important;height:100dvh!important;max-height:100dvh!important;overflow-y:auto!important;overflow-x:hidden!important;-webkit-overflow-scrolling:touch!important;overscroll-behavior-y:contain!important;touch-action:pan-y!important;box-sizing:border-box!important}
#g360-mobile-scroll-host>*{max-width:100%!important;box-sizing:border-box!important}
#g360-avatar-launch,#g360-avatar-home-dock,#g360-avatar-mic-dock,#g360-terrain-nav,#g360-terrain-modal,#g360-pages-modal,#g360-cm-modal,#g360-avatar-modal{z-index:2147483000!important}
#g360-avatar-launch{position:fixed!important;left:12px!important;bottom:96px!important;width:76px!important;height:76px!important;display:block!important;visibility:visible!important;opacity:1!important;border-radius:50%!important;padding:0!important;overflow:hidden!important;pointer-events:auto!important}
#g360-avatar-launch img{width:100%!important;height:100%!important;object-fit:cover!important;display:block!important;border-radius:50%!important}
#g360-avatar-mic-dock{position:fixed!important;left:94px!important;bottom:104px!important;display:flex!important;gap:6px!important;z-index:2147483001!important}
#g360-avatar-mic-dock button{width:48px!important;height:48px!important;border-radius:50%!important;border:1px solid #31506d!important;background:#0b1a2a!important;color:#fff!important;font-size:22px!important;box-shadow:0 8px 20px #0009!important}
#g360-avatar-mic-status{position:fixed!important;left:94px!important;bottom:74px!important;background:#071522!important;color:#d9f7ea!important;border:1px solid #31506d!important;border-radius:8px!important;padding:4px 7px!important;font:11px system-ui,sans-serif!important;z-index:2147483001!important}
</style>
<script>
(function(){
 function fixedish(el){return el&&el.id&&/modal|avatar-launch|avatar-home-dock|terrain-nav|terrain-modal|pages-modal|cm-modal|mic-dock|mic-status/.test(el.id)}
 function makeHost(){if(document.getElementById('g360-mobile-scroll-host'))return document.getElementById('g360-mobile-scroll-host');var b=document.body;if(!b)return null;var h=document.createElement('div');h.id='g360-mobile-scroll-host';Array.prototype.slice.call(b.children).forEach(function(el){var t=(el.tagName||'').toLowerCase();if(/script|style|link|meta|title/.test(t)||fixedish(el))return;h.appendChild(el)});b.insertBefore(h,b.firstChild);return h}
 function unlock(){var h=makeHost(),b=document.body,d=document.documentElement;if(!h||!b||!d)return;d.style.setProperty('overflow','hidden','important');b.style.setProperty('overflow','hidden','important');b.style.setProperty('height','100%','important');h.style.setProperty('height','100dvh','important');h.style.setProperty('max-height','100dvh','important');h.style.setProperty('overflow-y','auto','important');h.style.setProperty('overflow-x','hidden','important');h.style.setProperty('touch-action','pan-y','important')}
 function avatar(){var a=document.getElementById('g360-avatar-launch'),m=document.getElementById('g360-avatar-modal');if(a&&a.parentElement!==document.body)document.body.appendChild(a);if(a){a.style.setProperty('position','fixed','important');a.style.setProperty('display','block','important');a.style.setProperty('visibility','visible','important');a.style.setProperty('opacity','1','important');a.style.setProperty('z-index','2147483000','important');return}if(!m)return;var im=m.querySelector('img')||document.querySelector('img[alt*="avatar" i],img[alt*="IA" i]');if(!im)return;a=document.createElement('button');a.id='g360-avatar-launch';a.type='button';a.setAttribute('aria-label','Ouvrir l IA centrale');a.appendChild(im.cloneNode(true));a.onclick=function(){m.style.setProperty('display','flex','important');m.style.setProperty('visibility','visible','important');m.style.setProperty('opacity','1','important')};document.body.appendChild(a)}
 function mic(){if(document.getElementById('g360-avatar-mic-dock'))return;var d=document.createElement('div');d.id='g360-avatar-mic-dock';var b=document.createElement('button');b.id='g360-avatar-mic';b.type='button';b.textContent='🎙️';b.setAttribute('aria-label','Parler à l IA');d.appendChild(b);document.body.appendChild(d);var s=document.createElement('div');s.id='g360-avatar-mic-status';s.textContent='Micro prêt';document.body.appendChild(s);var R=window.SpeechRecognition||window.webkitSpeechRecognition;if(!R){s.textContent='Micro: reconnaissance non disponible';return}var r=new R(),on=false;r.lang='fr-FR';r.continuous=false;r.interimResults=false;r.onstart=function(){on=true;b.textContent='⏹️';s.textContent='Écoute en cours…'};r.onend=function(){on=false;b.textContent='🎙️';s.textContent='Micro prêt'};r.onerror=function(e){on=false;b.textContent='🎙️';s.textContent='Micro: '+(e.error||'erreur')};r.onresult=function(e){var t=e.results[0][0].transcript.trim();if(!t)return;s.textContent='Commande reçue';var i=document.querySelector('input[placeholder*="commande" i],textarea[placeholder*="commande" i]');if(i){i.value=t;i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))}window.dispatchEvent(new CustomEvent('gabon360:ai-command',{detail:{text:t,source:'microphone'}}));var low=t.toLowerCase();if(/navigation terrain/.test(low)){var n=document.getElementById('g360-terrain-open');if(n)n.click()}if(/accueil/.test(low)){var h=document.getElementById('g360-mobile-scroll-host');if(h)h.scrollTop=0}};b.onclick=function(){if(on)r.stop();else try{r.start()}catch(e){s.textContent='Micro: autorisation requise'}}}
 function mapBridge(){var h=document.getElementById('g360-mobile-scroll-host');if(!h)return;document.querySelectorAll('.leaflet-container').forEach(function(m){if(m.dataset.g360Bridge)return;m.dataset.g360Bridge='1';var y=0;m.addEventListener('touchstart',function(e){if(e.touches.length===1)y=e.touches[0].clientY},{passive:true});m.addEventListener('touchmove',function(e){if(e.touches.length!==1)return;var ny=e.touches[0].clientY,dy=ny-y;if(Math.abs(dy)>4){h.scrollTop-=dy;y=ny;e.preventDefault()}},{passive:false})})}
 function boot(){unlock();avatar();mic();mapBridge()}boot();window.addEventListener('load',boot);window.addEventListener('resize',unlock);var n=0,t=setInterval(function(){boot();if(++n>30)clearInterval(t)},300);window.GABON360_MOBILE_RUNTIME_V2={version:'2.0',dedicatedScrollHost:true,avatarRelocated:true,microphoneLauncher:true,mapVerticalScrollBridge:true}
})();
</script>
'''

def inject_html():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARK in t: return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8'); return
    raise SystemExit('No suitable index.html found')

def patch_manifest():
    for p in Path('android_project').rglob('AndroidManifest.xml'):
        t=p.read_text(encoding='utf-8')
        changed=False
        for perm in ['android.permission.ACCESS_FINE_LOCATION','android.permission.ACCESS_COARSE_LOCATION','android.permission.RECORD_AUDIO']:
            if perm not in t:
                marker='</manifest>'
                t=t.replace(marker,f'    <uses-permission android:name="{perm}" />\n{marker}',1); changed=True
        if changed:p.write_text(t,encoding='utf-8')

def main():
    inject_html();patch_manifest();print('Mobile runtime V2 injected')
if __name__=='__main__':main()
