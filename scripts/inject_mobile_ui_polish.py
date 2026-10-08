#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARKER='<!-- GABON360-MOBILE-POLISH-V1 -->'
PAYLOAD=r'''<!-- GABON360-MOBILE-POLISH-V1 -->
<style>
/* Final mobile layout normalization: one scrollable document, no stacked fixed toolbars. */
html,body{width:100%!important;max-width:100%!important;overflow-x:hidden!important;overflow-y:auto!important;height:auto!important;min-height:100%!important;position:relative!important}
body{padding-bottom:150px!important;box-sizing:border-box!important}
/* Keep the main content in normal flow. */
main,#root,#app,.app,.shell,.page,.content,.main-content{max-width:100%!important;box-sizing:border-box!important}
/* National launcher: compact single entry point instead of a pile of buttons over the dashboard. */
#g360-pages{left:12px!important;right:12px!important;bottom:74px!important;top:auto!important;max-width:none!important;width:auto!important;display:block!important;background:rgba(6,21,34,.96)!important;border:1px solid #31506d!important;border-radius:12px!important;padding:7px!important;box-shadow:0 8px 24px #0009!important}
#g360-pages button{display:none!important}
#g360-pages #g360-pages-open{display:block!important;width:100%!important;margin:0!important;padding:10px!important;font-size:14px!important}
/* Existing modules bar becomes a single compact launcher, avoiding collision with national navigation. */
#g360-modules{left:12px!important;right:12px!important;bottom:12px!important;top:auto!important;width:auto!important;display:flex!important;gap:7px!important;justify-content:flex-start!important;overflow-x:auto!important;overflow-y:hidden!important;overscroll-behavior-x:contain!important;box-sizing:border-box!important;padding:6px!important;scrollbar-width:thin!important;z-index:100000!important}
#g360-modules button{display:inline-flex!important;flex:0 0 auto!important;align-items:center!important;justify-content:center!important;min-width:76px!important;min-height:44px!important;margin:0!important;padding:8px 10px!important;font-size:12px!important;white-space:nowrap!important;touch-action:manipulation!important}
#g360-pages{z-index:100020!important;max-height:60dvh!important;overflow-y:auto!important}
#g360-pages #g360-pages-open{min-height:44px!important}
#g360-avatar-launch{bottom:78px!important;left:12px!important;width:56px!important;height:56px!important;z-index:100010!important}
#g360-satellite-open{bottom:78px!important;right:12px!important;min-height:44px!important;z-index:100010!important}
button,a,[role=button],input,select,textarea{touch-action:manipulation}
/* AI command strip is hidden on the dashboard because the central avatar is the command entry point. */
#g360-ai-command{display:none!important}
#g360-ai-go{display:none!important}
/* Avatar launcher stays above the navigation bar without covering content. */
#g360-avatar-launch{left:12px!important;bottom:126px!important;width:72px!important;height:72px!important;z-index:100010!important}
/* Modals always have their own scroll and safe mobile padding. */
#g360-pages-modal,#g360-cm-modal,#g360-avatar-modal{overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;align-items:flex-start!important;padding-top:12px!important;padding-bottom:24px!important;box-sizing:border-box!important}
#g360-pages-card,#g360-avatar-card,.g360-cm-card{max-height:calc(100vh - 36px)!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important;box-sizing:border-box!important}
#g360-pages-grid{grid-template-columns:1fr!important}
@media(min-width:681px){#g360-pages{left:auto!important;right:18px!important;width:auto!important;max-width:420px!important}#g360-modules{left:18px!important;right:auto!important;width:auto!important}}
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
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' in p.parts,len(p.parts)))
    for p in candidates:
        text=p.read_text(encoding='utf-8')
        if MARKER in text:
            print('already:',p); return
        i=text.lower().rfind('</body>')
        if i>=0:
            p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
            print('injected:',p); return
    raise SystemExit('No suitable index.html found')

if __name__=='__main__': main()
