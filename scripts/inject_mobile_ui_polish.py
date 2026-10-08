#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARKER='<!-- GABON360-MOBILE-POLISH-V5 -->'
PAYLOAD=r'''<!-- GABON360-MOBILE-POLISH-V5 -->
<style>
/* V5: single, predictable mobile layout; avoid contradictory fixed-position overrides. */
*,*::before,*::after{box-sizing:border-box}
html,body{width:100%;max-width:100%;min-height:100%;margin:0;overflow-x:hidden}
body{padding-bottom:150px!important}
img,video,canvas,iframe{max-width:100%}
button,a,[role=button],input,select,textarea{touch-action:manipulation}
main,#root,#app,.app,.shell,.page,.content,.main-content{max-width:100%;min-width:0}
#g360-pages-modal,#g360-cm-modal,#g360-avatar-modal{z-index:100100!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;align-items:flex-start!important;padding:12px 12px 24px!important}
#g360-pages-card,#g360-avatar-card,.g360-cm-card{width:min(100%,560px)!important;max-width:100%!important;max-height:calc(100dvh - 36px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
#g360-pages-grid{grid-template-columns:1fr!important}
#g360-pages{position:fixed!important;left:12px!important;right:12px!important;top:auto!important;bottom:82px!important;width:auto!important;max-width:none!important;max-height:55dvh!important;overflow-y:auto!important;z-index:100020!important;background:rgba(6,21,34,.97)!important;border:1px solid #31506d!important;border-radius:12px!important;padding:7px!important;box-shadow:0 8px 24px #0009!important}
#g360-pages button{display:flex;align-items:center;justify-content:flex-start;width:100%;min-height:44px;margin:3px 0;padding:10px 12px;white-space:normal;text-align:left}
#g360-pages #g360-pages-open{display:block;width:100%;min-height:44px;margin:0;padding:10px}
#g360-modules{position:fixed!important;left:12px!important;right:12px!important;top:auto!important;bottom:8px!important;width:auto!important;max-width:none!important;display:flex;gap:7px;justify-content:flex-start;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;z-index:100000!important;padding:6px!important;background:rgba(6,21,34,.95)!important;border-radius:12px}
#g360-modules button{display:inline-flex;flex:0 0 auto;align-items:center;justify-content:center;min-width:76px;min-height:44px;margin:0;padding:8px 10px;font-size:12px;white-space:nowrap}
#g360-avatar-launch{position:fixed!important;left:12px!important;bottom:164px!important;top:auto!important;width:56px!important;height:56px!important;max-width:calc(100vw - 24px)!important;z-index:100010!important}
#g360-satellite-open{position:fixed!important;right:12px!important;bottom:164px!important;top:auto!important;left:auto!important;max-width:132px!important;min-height:44px!important;z-index:100010!important}
#g360-micro-launch,#g360-mic-launch,#g360-voice-launch{position:fixed!important;left:12px!important;bottom:94px!important;top:auto!important;max-width:64px!important;z-index:100010!important}
#g360-ai-command{position:relative!important;left:auto!important;right:auto!important;bottom:auto!important;width:100%!important;max-width:100%!important;visibility:visible;pointer-events:auto}
#g360-ai-go{position:relative!important;bottom:auto!important;visibility:visible;pointer-events:auto}
@media(max-width:680px){body{padding-bottom:170px!important}#g360-pages{bottom:66px!important;max-height:58dvh!important}#g360-avatar-launch{bottom:154px!important}#g360-satellite-open{bottom:154px!important}}
</style>
<script>
(function(){
 function normalize(){
  const h=document.documentElement,b=document.body;
  if(!h||!b)return;
  h.style.setProperty('overflow-x','hidden','important');
  h.style.setProperty('overflow-y','auto','important');
  h.style.setProperty('height','auto','important');
  b.style.setProperty('overflow-x','hidden','important');
  b.style.setProperty('overflow-y','auto','important');
  b.style.setProperty('height','auto','important');
  b.style.setProperty('min-height','100%','important');
  b.style.setProperty('touch-action','pan-y','important');
 }
 normalize();
 window.addEventListener('load',normalize);
 window.addEventListener('resize',normalize);
 window.GABON360_MOBILE_UI={version:'1.0',scroll:true,overlapFix:true};
})();
</script>
'''

def main():
    import re
    root=Path('android_project')
    candidates=sorted(root.rglob('index.html'),key=lambda p:len(p.parts))
    if not candidates:
        raise SystemExit('No suitable index.html found')
    updated=0
    for p in candidates:
        original=p.read_text(encoding='utf-8')
        # Remove prior mobile polish blocks, then append the current block last.
        text=re.sub(r'<!-- GABON360-MOBILE-POLISH-V\d+ -->.*?</script>', '', original, flags=re.S)
        i=text.lower().rfind('</body>')
        if i>=0:
            p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
            print('replaced and moved final mobile polish to end:',p)
            updated+=1
    if updated == 0:
        raise SystemExit('No index.html with a closing body tag found')
    print('mobile polish applied to',updated,'HTML file(s)')

if __name__=='__main__': main()
