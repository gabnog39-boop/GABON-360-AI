#!/usr/bin/env python3
from pathlib import Path

MARK = "GABON360-HORIZONTAL-PAGE-NAV-V1"

PAYLOAD = r'''<!-- GABON360-HORIZONTAL-PAGE-NAV-V1 -->
<style>
/* Les pages se lisent verticalement; seuls les rubans d'options défilent horizontalement. */
html,body{max-width:100%;overflow-x:hidden!important}
body{overflow-y:auto!important;touch-action:pan-y!important}
#g360-universal,#g360-universal .g360-upage,#g360-page-view,#g360-pages-modal #g360-pages-card,#g360-complete-modal,#g360-complete-card,#g360-complete-view{
 max-height:100dvh;overflow-y:auto!important;overflow-x:hidden!important;
 -webkit-overflow-scrolling:touch;overscroll-behavior-y:contain;touch-action:pan-y;
}
#g360-universal .g360-ugrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}
#g360-complete-view .g360-cview>p,
#g360-universal .g360-uoptions,
#g360-options-strip,.g360-horizontal-options{
 display:flex!important;flex-wrap:nowrap!important;gap:8px;max-width:100%;overflow-x:auto!important;overflow-y:hidden!important;
 white-space:nowrap;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;scroll-snap-type:x proximity;touch-action:pan-x;
 padding:8px 2px 12px;scrollbar-width:thin;
}
#g360-complete-view .g360-cview>p>button,
#g360-universal .g360-uoptions>*,
#g360-options-strip>*,.g360-horizontal-options>*{flex:0 0 auto;scroll-snap-align:start;max-width:85vw}
#g360-complete-view .g360-cview{overflow:visible}
.g360-horizontal-hint{position:sticky;bottom:8px;z-index:10;width:max-content;max-width:90%;margin:8px auto;background:#071522e8;color:#eaf5ff;border:1px solid #31506d;border-radius:999px;padding:6px 11px;font:11px system-ui,sans-serif;pointer-events:none}
@media(max-width:680px){#g360-universal .g360-ugrid{grid-template-columns:1fr}}
</style>
<script>
(function(){
 if(window.__G360_VERTICAL_PAGES_HORIZONTAL_OPTIONS_V1)return;
 window.__G360_VERTICAL_PAGES_HORIZONTAL_OPTIONS_V1=true;
 function setVertical(root){
  if(!root)return;
  root.style.setProperty('overflow-y','auto','important');
  root.style.setProperty('overflow-x','hidden','important');
  root.style.setProperty('touch-action','pan-y','important');
 }
 function makeHorizontal(el){
  if(!el||el.dataset.g360HorizontalOptions==='1')return;
  el.dataset.g360HorizontalOptions='1';
  el.style.setProperty('display','flex','important');
  el.style.setProperty('flex-wrap','nowrap','important');
  el.style.setProperty('overflow-x','auto','important');
  el.style.setProperty('overflow-y','hidden','important');
  el.style.setProperty('touch-action','pan-x','important');
  el.style.setProperty('-webkit-overflow-scrolling','touch');
  el.style.setProperty('scroll-snap-type','x proximity');
 }
 function apply(){
  [document.body,document.getElementById('g360-universal'),document.getElementById('g360-page-view'),document.getElementById('g360-complete-modal'),document.getElementById('g360-complete-card'),document.getElementById('g360-complete-view'),document.getElementById('g360-pages-modal'),document.getElementById('g360-pages-card')].forEach(setVertical);
  document.querySelectorAll('#g360-complete-view .g360-cview>p,#g360-universal .g360-uoptions,#g360-options-strip,.g360-horizontal-options').forEach(makeHorizontal);
 }
 apply();
 new MutationObserver(apply).observe(document.documentElement,{childList:true,subtree:true});
 window.GABON360_SCROLL_BEHAVIOR={page:'vertical',options:'horizontal',version:1};
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
