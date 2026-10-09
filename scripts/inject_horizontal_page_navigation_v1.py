#!/usr/bin/env python3
from pathlib import Path

MARK = "GABON360-HORIZONTAL-PAGE-NAV-V1"

PAYLOAD = r'''<!-- GABON360-HORIZONTAL-PAGE-NAV-V1 -->
<style>
/* NAVIGATION: pages gauche/droite; contenu et lecture des options haut/bas. */
html,body{width:100%;max-width:100%;overflow-x:hidden!important}
body{overflow-y:auto!important;touch-action:pan-y!important}
#g360-universal,#g360-universal .g360-upage,#g360-page-view,#g360-pages-modal,#g360-pages-modal #g360-pages-card,#g360-complete-modal,#g360-complete-card,#g360-complete-view{
 max-height:100dvh;overflow-y:auto!important;overflow-x:hidden!important;
 -webkit-overflow-scrolling:touch;overscroll-behavior-y:contain;touch-action:pan-y;
}
#g360-universal .g360-ugrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
#g360-universal .g360-uoptions,#g360-options-strip,.g360-horizontal-options{
 display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;gap:8px;max-width:100%;
 overflow-y:auto!important;overflow-x:hidden!important;white-space:normal;overscroll-behavior-y:contain;
 -webkit-overflow-scrolling:touch;touch-action:pan-y;padding:8px 4px 12px;
}
#g360-complete-view .g360-cview>p{
 display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;gap:8px;max-width:100%;
 overflow-y:visible!important;overflow-x:hidden!important;white-space:normal;touch-action:pan-y;padding:8px 2px 12px;
}
#g360-complete-view .g360-cview>p>button,#g360-universal .g360-uoptions>*,#g360-options-strip>*,.g360-horizontal-options>*{
 flex:0 0 auto;max-width:100%;width:100%;white-space:normal;text-align:left;
}
#g360-complete-view .g360-cview{overflow:visible}
.g360-vertical-hint{position:sticky;bottom:8px;z-index:10;width:max-content;max-width:90%;margin:8px auto;background:#071522e8;color:#eaf5ff;border:1px solid #31506d;border-radius:999px;padding:6px 11px;font:11px system-ui,sans-serif;pointer-events:none}
@media(max-width:680px){#g360-universal .g360-ugrid{grid-template-columns:1fr}}
</style>
<script>
(function(){
 if(window.__G360_PAGE_HORIZONTAL_VERTICAL_OPTIONS_V2)return;
 window.__G360_PAGE_HORIZONTAL_VERTICAL_OPTIONS_V2=true;
 function vertical(el){
  if(!el)return;
  el.style.setProperty('overflow-y','auto','important');
  el.style.setProperty('overflow-x','hidden','important');
  el.style.setProperty('touch-action','pan-y','important');
  el.style.setProperty('-webkit-overflow-scrolling','touch');
 }
 function verticalOptions(el){
  if(!el)return;
  el.style.setProperty('display','flex','important');
  el.style.setProperty('flex-direction','column','important');
  el.style.setProperty('flex-wrap','nowrap','important');
  el.style.setProperty('overflow-y','auto','important');
  el.style.setProperty('overflow-x','hidden','important');
  el.style.setProperty('touch-action','pan-y','important');
  el.style.setProperty('white-space','normal','important');
 }
 function apply(){
  [document.body,document.getElementById('g360-universal'),document.getElementById('g360-page-view'),document.getElementById('g360-complete-modal'),document.getElementById('g360-complete-card'),document.getElementById('g360-complete-view'),document.getElementById('g360-pages-modal'),document.getElementById('g360-pages-card')].forEach(vertical);
  document.querySelectorAll('#g360-universal .g360-uoptions,#g360-options-strip,.g360-horizontal-options,#g360-complete-view .g360-cview>p').forEach(verticalOptions);
 }
 apply();
 new MutationObserver(apply).observe(document.documentElement,{childList:true,subtree:true});
 window.GABON360_SCROLL_BEHAVIOR={pages:'horizontal-left-right',options:'vertical-top-bottom',version:2};
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
