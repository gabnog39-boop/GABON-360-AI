#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARKER='<!-- GABON360-SCROLL-FIX-V1 -->'
PAYLOAD=r'''<!-- GABON360-SCROLL-FIX-V1 -->
<style>
html,body{overflow-x:hidden!important;overflow-y:auto!important;height:auto!important;min-height:100%!important;-webkit-overflow-scrolling:touch!important;overscroll-behavior-y:auto!important}
body{touch-action:pan-y!important;position:relative!important}
/* Never let common app shells lock the whole document. */
body>*:not([data-g360-fixed]){max-height:none}
</style>
<script>
(function(){
  function enableScroll(){
    const h=document.documentElement,b=document.body;
    if(!h||!b)return;
    h.style.setProperty('overflow-y','auto','important');
    h.style.setProperty('height','auto','important');
    b.style.setProperty('overflow-y','auto','important');
    b.style.setProperty('height','auto','important');
    b.style.setProperty('min-height','100%','important');
    b.style.setProperty('touch-action','pan-y','important');
    // Keep scrolling on the document; overlays/modals keep their own internal scroll.
    document.addEventListener('touchmove',function(e){
      const t=e.target instanceof Element?e.target:null;
      if(t && t.closest && t.closest('[data-g360-scroll-lock]')) return;
      if(t && t.closest && t.closest('input,textarea,select,button')) return;
    },{passive:true});
  }
  enableScroll();
  window.addEventListener('load',enableScroll,{once:false});
  window.GABON360_SCROLL={version:'1.0',enabled:true};
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARKER in t:
            print('already:',p); return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8'); print('injected:',p); return
    raise SystemExit('No index.html found')

if __name__=='__main__': main()
