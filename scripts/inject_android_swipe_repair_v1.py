#!/usr/bin/env python3
"""Renforce le balayage Android natif de page en page, sans bloquer le scroll vertical."""
from pathlib import Path

MARK = "GABON360-ANDROID-SWIPE-REPAIR-V1"
PAYLOAD = r"""
<!-- GABON360-ANDROID-SWIPE-REPAIR-V1 -->
<style>
html,body { overscroll-behavior-x: contain; }
#g360-universal, #g360-pages-modal, #g360-page-view { touch-action: pan-y; }
</style>
<script id="gabon360-android-swipe-repair-v1">
(function(){
  if(window.__G360_ANDROID_SWIPE_REPAIR_V1) return;
  window.__G360_ANDROID_SWIPE_REPAIR_V1 = true;
  var startX=0,startY=0,startT=0,tracking=false,consumed=false;
  var threshold=68,ratio=1.25,maxTime=900;
  var ignoreSelector='button,a,input,textarea,select,[role="button"],[data-no-page-swipe="true"],.g360-ucard';
  function currentId(){
    return window.GABON360_CURRENT_PAGE || 'avatar';
  }
  function order(){
    if(Array.isArray(window.GABON360_PAGE_ORDER) && window.GABON360_PAGE_ORDER.length) return window.GABON360_PAGE_ORDER;
    return ['avatar','map','nav','sat','drones','cameras','maritime','forests','alerts','reports','stats','weather','sources','security','memory'];
  }
  function navigate(delta){
    var nav=window.GABON360_PAGE_NAVIGATION;
    if(nav && typeof nav.next==='function' && typeof nav.previous==='function'){
      return delta>0 ? nav.next() : nav.previous();
    }
    var list=order(),idx=list.indexOf(currentId());
    if(idx<0) idx=0;
    idx=Math.max(0,Math.min(list.length-1,idx+delta));
    var id=list[idx], ok=false;
    try{
      if(id==='avatar' && typeof window.GABON360_OPEN_AVATAR_HOME==='function') ok=!!window.GABON360_OPEN_AVATAR_HOME();
      else if(typeof window.GABON360_OPEN_MODULE_PAGE==='function'){window.GABON360_OPEN_MODULE_PAGE(id);ok=true;}
      else if(typeof window.GABON360_OPEN_FUNCTION_PAGE==='function'){window.GABON360_OPEN_FUNCTION_PAGE(id);ok=true;}
      else if(typeof window.GABON360_NAVIGATE==='function'){window.GABON360_NAVIGATE(id);ok=true;}
    }catch(e){ ok=false; }
    if(ok) window.GABON360_CURRENT_PAGE=id;
    return ok;
  }
  function isIgnored(target){
    return !!(target && target.closest && target.closest(ignoreSelector));
  }
  document.addEventListener('touchstart',function(e){
    if(!e.touches || e.touches.length!==1 || isIgnored(e.target)){tracking=false;return;}
    var touch=e.touches[0];
    startX=touch.clientX;startY=touch.clientY;startT=Date.now();
    tracking=true;consumed=false;
  },{passive:true,capture:true});
  document.addEventListener('touchmove',function(e){
    if(!tracking || !e.touches || !e.touches.length)return;
    var t=e.touches[0],dx=t.clientX-startX,dy=t.clientY-startY;
    if(Math.abs(dy)>Math.abs(dx)*ratio) tracking=false;
  },{passive:true,capture:true});
  document.addEventListener('touchend',function(e){
    if(!tracking || consumed || !e.changedTouches || !e.changedTouches.length){tracking=false;return;}
    tracking=false;
    var t=e.changedTouches[0],dx=t.clientX-startX,dy=t.clientY-startY,elapsed=Date.now()-startT;
    if(elapsed>maxTime || Math.abs(dx)<threshold || Math.abs(dx)<Math.abs(dy)*ratio)return;
    consumed=true;
    /* Standard Android convention: finger moves right-to-left = next page. */
    navigate(dx<0 ? 1 : -1);
    window.dispatchEvent(new CustomEvent('gabon360:android-swipe',{detail:{direction:dx<0?'next':'previous',from:currentId()}}));
  },{passive:true,capture:true});
  window.GABON360_ANDROID_SWIPE_REPAIR={
    version:'1.0',
    convention:'left-swipe=next; right-swipe=previous',
    next:function(){return navigate(1)},
    previous:function(){return navigate(-1)}
  };
})();
</script>
"""

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' in p.parts,len(p.parts)))
    if not candidates: raise SystemExit('SWIPE REPAIR FAIL: index.html introuvable')
    p=candidates[0]
    html=p.read_text(encoding='utf-8',errors='ignore')
    if MARK in html:
        print('SWIPE REPAIR: déjà présent')
        return
    i=html.lower().rfind('</body>')
    if i<0: raise SystemExit('SWIPE REPAIR FAIL: </body> introuvable')
    p.write_text(html[:i]+PAYLOAD+chr(10)+html[i:],encoding='utf-8')
    print('SWIPE REPAIR: injected',p)

if __name__=='__main__':
    main()
