#!/usr/bin/env python3
"""Final deterministic mobile overlay repair, applied after every other UI injector."""
from pathlib import Path

MARK = "GABON360-FINAL-OVERLAY-REPAIR-V1"
PAYLOAD = r'''<!-- GABON360-FINAL-OVERLAY-REPAIR-V1 -->
<style>
/* Satellite catalogue must never cover the dashboard on startup. */
#g360-satellite-panel { display:none!important; }
#g360-satellite-panel.g360-visible { display:block!important; }
#g360-satellite-open {
  position:fixed!important;
  right:12px!important;
  bottom:82px!important;
  z-index:100020!important;
  max-width:calc(100vw - 24px)!important;
}
#g360-satellite-panel.g360-visible {
  position:fixed!important;
  left:12px!important;
  right:12px!important;
  bottom:148px!important;
  width:auto!important;
  max-height:55dvh!important;
  z-index:100030!important;
  box-sizing:border-box!important;
}
#g360-satellite-panel .g360-body { max-height:calc(55dvh - 55px)!important; overflow:auto!important; }
#g360-satellite-panel.g360-hidden { display:none!important; }
@media (max-width:680px) {
  #g360-avatar-home-button { right:12px!important; bottom:18px!important; width:48px!important; height:48px!important; }
  #g360-avatar-launch { left:12px!important; bottom:18px!important; width:54px!important; height:54px!important; }
}
/* A closed overlay must not intercept taps even if another injector leaves its styles behind. */
#g360-universal[aria-hidden="true"],
#g360-v2[aria-hidden="true"],
#g360-pages-modal[aria-hidden="true"],
#g360-cm-modal[aria-hidden="true"],
#g360-avatar-modal[aria-hidden="true"] {
  display:none!important; visibility:hidden!important; pointer-events:none!important;
}
</style>
<script id="g360-final-overlay-repair">
(function(){
  if(window.__G360_FINAL_OVERLAY_REPAIR_V1)return;
  window.__G360_FINAL_OVERLAY_REPAIR_V1=true;
  function setup(){
    var panel=document.getElementById('g360-satellite-panel');
    var launcher=document.getElementById('g360-satellite-open');
    if(panel){
      panel.classList.remove('g360-visible');
      panel.classList.add('g360-hidden');
      panel.setAttribute('aria-hidden','true');
    }
    if(launcher){
      launcher.classList.add('g360-visible');
      launcher.setAttribute('aria-expanded','false');
      launcher.onclick=function(){
        if(!panel)return;
        panel.classList.remove('g360-hidden');
        panel.classList.add('g360-visible');
        panel.setAttribute('aria-hidden','false');
        launcher.classList.remove('g360-visible');
        launcher.setAttribute('aria-expanded','true');
      };
    }
    var close=document.getElementById('g360-sat-close');
    if(close && panel && launcher){
      close.onclick=function(){
        panel.classList.remove('g360-visible');
        panel.classList.add('g360-hidden');
        panel.setAttribute('aria-hidden','true');
        launcher.classList.add('g360-visible');
        launcher.setAttribute('aria-expanded','false');
      };
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup,{once:true});
  else setup();
  window.addEventListener('load',setup,{once:true});
  window.GABON360_OVERLAY_REPAIR_STATUS={version:'1.0',satellitePanelClosedOnStartup:true,closedOverlaysDoNotBlock:true};
})();
</script>
'''

def main():
    required = ['GABON360-SATELLITE-PANEL-V1']
    candidates = sorted(Path('android_project').rglob('index.html'), key=lambda p: ('assets' not in p.parts, len(p.parts), str(p)))
    scored=[]
    for p in candidates:
        t=p.read_text(encoding='utf-8',errors='ignore')
        scored.append((sum(x in t for x in required),p,t))
    scored.sort(key=lambda x:(x[0],-len(x[1].parts),str(x[1])),reverse=True)
    if not scored or scored[0][0] < len(required):
        raise SystemExit('OVERLAY-REPAIR FAIL: consolidated index with satellite panel not found')
    _,p,t=scored[0]
    if MARK in t:
        print('OVERLAY-REPAIR already installed:',p); return
    i=t.lower().rfind('</body>')
    if i<0: raise SystemExit('OVERLAY-REPAIR FAIL: </body> missing')
    p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
    print('OVERLAY-REPAIR installed:',p)

if __name__ == '__main__': main()
