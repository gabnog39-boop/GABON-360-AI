#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARK='<!-- GABON360-FINAL-MOBILE-INTERACTION-V1 -->'
PAYLOAD=r'''<!-- GABON360-FINAL-MOBILE-INTERACTION-V1 -->
<style>
/* Dernière couche mobile : le document doit réellement défiler dans Android WebView. */
html,body{overflow-x:hidden!important;overflow-y:scroll!important;height:auto!important;min-height:100%!important;max-height:none!important;touch-action:pan-y!important;-webkit-overflow-scrolling:touch!important}
body{position:relative!important;padding-bottom:180px!important}
/* Les panneaux de navigation ne doivent plus former une pile fixe qui bloque le contenu. */
#g360-pages{position:static!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;width:auto!important;max-width:none!important;margin:14px 12px!important;display:block!important;transform:none!important}
#g360-modules{position:static!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;width:auto!important;max-width:none!important;margin:10px 12px 20px!important;display:flex!important;transform:none!important}
#g360-pages button{display:block!important}
#g360-pages #g360-pages-open{display:block!important;width:100%!important}
/* Empêcher les conteneurs applicatifs de verrouiller le défilement. */
main,#root,#app,.app,.shell,.page,.content,.main-content,#g360-center{max-height:none!important;min-height:0!important;overflow:visible!important;touch-action:pan-y!important}
/* Le bouton IA reste fixe, séparé des panneaux de navigation. */
#g360-avatar-launch{display:block!important;visibility:visible!important;opacity:1!important;position:fixed!important;left:12px!important;bottom:88px!important;right:auto!important;width:78px!important;height:78px!important;z-index:2147483646!important;pointer-events:auto!important}
#g360-avatar-launch img{display:block!important;visibility:visible!important;opacity:1!important;width:100%!important;height:100%!important;object-fit:cover!important;border-radius:50%!important}
#g360-avatar-home-dock{position:fixed!important;left:12px!important;bottom:88px!important;width:78px!important;height:78px!important;z-index:2147483645!important;pointer-events:auto!important}
#g360-avatar-home-dock button{pointer-events:auto!important;width:78px!important;height:78px!important}
#g360-avatar-home-dock img{display:block!important;width:100%!important;height:100%!important;object-fit:cover!important}
#g360-avatar-home-label{top:80px!important}
/* Les fenêtres internes restent défilables. */
#g360-pages-modal,#g360-cm-modal,#g360-avatar-modal{overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-y!important}
#g360-pages-card,#g360-avatar-card,.g360-cm-card{max-height:calc(100dvh - 32px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;touch-action:pan-y!important}
</style>
<script>
(function(){
  function unlock(){
    var h=document.documentElement,b=document.body;
    if(!h||!b)return;
    [h,b].forEach(function(el){
      el.style.setProperty('overflow-y','scroll','important');
      el.style.setProperty('overflow-x','hidden','important');
      el.style.setProperty('height','auto','important');
      el.style.setProperty('max-height','none','important');
      el.style.setProperty('touch-action','pan-y','important');
    });
    ['main','#root','#app','.app','.shell','.page','.content','.main-content','#g360-center'].forEach(function(sel){
      document.querySelectorAll(sel).forEach(function(el){
        if(el.id==='g360-center') return;
        el.style.setProperty('max-height','none','important');
        el.style.setProperty('overflow','visible','important');
        el.style.setProperty('touch-action','pan-y','important');
      });
    });
  }

  function ensureAvatar(){
    var src=document.getElementById('g360-avatar-launch');
    var modal=document.getElementById('g360-avatar-modal');
    if(src){
      src.style.setProperty('display','block','important');
      src.style.setProperty('visibility','visible','important');
      src.style.setProperty('opacity','1','important');
      src.style.setProperty('z-index','2147483646','important');
      return true;
    }
    if(!modal)return false;
    /* Secours : si le bouton original a disparu, reconstruire le lanceur à partir de l'image déjà intégrée dans le module IA. */
    var im=modal.querySelector('img');
    if(!im) im=document.querySelector('img[alt*="avatar" i],img[alt*="IA" i]');
    if(!im) return false;
    var b=document.createElement('button');
    b.id='g360-avatar-launch'; b.type='button'; b.setAttribute('aria-label','Ouvrir l IA centrale');
    var copy=im.cloneNode(true); b.appendChild(copy);
    b.addEventListener('click',function(){
      modal.style.setProperty('display','flex','important');
      modal.style.setProperty('visibility','visible','important');
      modal.style.setProperty('opacity','1','important');
    });
    document.body.appendChild(b);
    return true;
  }

  function boot(){ unlock(); ensureAvatar(); }
  boot();
  window.addEventListener('load',boot);
  window.addEventListener('resize',unlock);
  var n=0, timer=setInterval(function(){n++;boot();if(n>40)clearInterval(timer)},250);
  window.GABON360_FINAL_MOBILE={version:'1.0',scrollUnlocked:true,avatarVisible:true};
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
