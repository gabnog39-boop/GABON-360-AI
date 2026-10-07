#!/usr/bin/env python3
from pathlib import Path

MARK = "GABON360-HORIZONTAL-PAGE-NAV-V1"

PAYLOAD = r'''<!-- GABON360-HORIZONTAL-PAGE-NAV-V1 -->
<style>
/* GABON 360 AI — navigation horizontale des pages */
#g360-pages-modal #g360-pages-card,
#g360-universal {
  touch-action: pan-y;
}
#g360-pages-modal #g360-page-view,
#g360-universal .g360-upage {
  overflow-x: hidden;
}
.g360-horizontal-hint{
  position:fixed;left:50%;bottom:10px;transform:translateX(-50%);
  z-index:2147483600;background:#071522e8;color:#eaf5ff;
  border:1px solid #31506d;border-radius:999px;padding:6px 11px;
  font:11px system-ui,sans-serif;pointer-events:none;opacity:0;
  transition:opacity .2s;
}
.g360-horizontal-hint.show{opacity:.9}
.g360-page-slide{will-change:transform}
</style>
<div id="g360-horizontal-hint" class="g360-horizontal-hint">← page précédente · page suivante →</div>
<script>
(function(){
  if(window.__G360_HORIZONTAL_PAGE_NAV_V1)return;
  window.__G360_HORIZONTAL_PAGE_NAV_V1=true;

  var ORDER=['map','nav','sat','drones','cameras','maritime','forests','alerts','reports','stats','weather','sources','security','memory','avatar'];
  var current=0, startX=0, startY=0, tracking=false, moved=false;
  var hint=document.getElementById('g360-horizontal-hint');

  function showHint(){
    if(!hint)return;
    hint.classList.add('show');
    clearTimeout(showHint._t);
    showHint._t=setTimeout(function(){hint.classList.remove('show')},1400);
  }
  function moduleIds(){
    if(window.GABON360_MODULE_PAGES) return Object.keys(window.GABON360_MODULE_PAGES);
    if(window.GABON360_NATIONAL_MODULES) return Object.keys(window.GABON360_NATIONAL_MODULES);
    return ORDER.slice();
  }
  function setCurrent(id){
    var ids=moduleIds(),i=ids.indexOf(id);
    if(i>=0)current=i;
  }
  function openId(id){
    setCurrent(id);
    if(typeof window.GABON360_NAVIGATE==='function'){
      window.GABON360_NAVIGATE(id);
      return true;
    }
    if(typeof window.GABON360_OPEN_MODULE_PAGE==='function'){
      window.GABON360_OPEN_MODULE_PAGE(id);
      return true;
    }
    return false;
  }
  function go(delta){
    var ids=moduleIds();
    if(!ids.length)return;
    current=(current+delta+ids.length)%ids.length;
    var id=ids[current];
    openId(id);
    showHint();
    window.dispatchEvent(new CustomEvent('gabon360:page-navigation',{
      detail:{direction:delta>0?'next':'previous',page:id,index:current,source:'manual-swipe'}
    }));
  }

  /* Gestes horizontaux: un balayage franc, sans bloquer le défilement vertical. */
  function attach(el){
    if(!el || el.__g360HorizontalAttached)return;
    el.__g360HorizontalAttached=true;
    el.addEventListener('touchstart',function(e){
      if(!e.touches||e.touches.length!==1)return;
      startX=e.touches[0].clientX; startY=e.touches[0].clientY;
      tracking=true;moved=false;
    },{passive:true});
    el.addEventListener('touchmove',function(e){
      if(!tracking||!e.touches||!e.touches.length)return;
      var dx=e.touches[0].clientX-startX,dy=e.touches[0].clientY-startY;
      if(Math.abs(dx)>14 && Math.abs(dx)>Math.abs(dy)*1.15)moved=true;
    },{passive:true});
    el.addEventListener('touchend',function(e){
      if(!tracking){return}
      tracking=false;
      if(!moved||!e.changedTouches||!e.changedTouches.length)return;
      var dx=e.changedTouches[0].clientX-startX;
      if(Math.abs(dx)<70)return;
      /* gauche -> page suivante; droite -> page précédente */
      go(dx<0?1:-1);
    },{passive:true});
  }

  function attachAll(){
    attach(document.getElementById('g360-pages-modal'));
    attach(document.getElementById('g360-universal'));
    attach(document.getElementById('g360-page-view'));
    document.querySelectorAll('[data-g360-page]').forEach(function(b){b.addEventListener('click',function(){setCurrent(b.dataset.g360Page)})});
  }

  /* Commandes vocales de l'Avatar */
  var oldCommand=window.GABON360_HANDLE_COMMAND;
  window.GABON360_HANDLE_COMMAND=function(raw){
    var q=String(raw||'').toLowerCase().trim();
    if(/page suivante|suivante|suivant|va[ -]?à la page suivante|ouvre la page suivante/.test(q)){
      go(1); return {ok:true,page:moduleIds()[current],navigation:'next'};
    }
    if(/page précédente|precedente|précédente|precedent|retourne à la page précédente|ouvre la page précédente/.test(q)){
      go(-1); return {ok:true,page:moduleIds()[current],navigation:'previous'};
    }
    if(/fais défiler vers la droite|glisse vers la droite/.test(q)){go(-1);return {ok:true,navigation:'previous'};}
    if(/fais défiler vers la gauche|glisse vers la gauche/.test(q)){go(1);return {ok:true,navigation:'next'};}
    return oldCommand?oldCommand(raw):{ok:false};
  };

  window.GABON360_PAGE_NEXT=function(){go(1)};
  window.GABON360_PAGE_PREVIOUS=function(){go(-1)};
  window.GABON360_PAGE_NAVIGATION={
    next:window.GABON360_PAGE_NEXT,
    previous:window.GABON360_PAGE_PREVIOUS,
    current:function(){return moduleIds()[current]||null}
  };

  attachAll();
  setTimeout(attachAll,500);
  setTimeout(attachAll,1500);
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'), key=lambda p: ('assets' in p.parts, len(p.parts)))
    if not candidates:
        raise SystemExit('index.html introuvable')
    for p in candidates:
        t=p.read_text(encoding='utf-8', errors='ignore')
        if MARK in t:
            print('already:',p)
            return
        i=t.lower().rfind('</body>')
        if i<0:
            continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
        print('installed:',p)
        return
    raise SystemExit('Aucun index.html exploitable')

if __name__=='__main__':
    main()
