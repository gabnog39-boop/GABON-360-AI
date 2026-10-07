#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-NAVIGATION-PAGE-BRIDGE-V1 -->'
PAYLOAD=r'''<!-- GABON360-NAVIGATION-PAGE-BRIDGE-V1 -->
<script>
(function(){
if(window.__G360_NAVIGATION_PAGE_BRIDGE_V1)return;
window.__G360_NAVIGATION_PAGE_BRIDGE_V1=true;
var previous=window.GABON360_OPEN_ENHANCED_PAGE;
window.GABON360_OPEN_ENHANCED_PAGE=function(id){
  if(id==='nav'){
    try{var u=document.getElementById('g360-universal');if(u)u.style.display='none';}catch(e){}
    try{var b=document.getElementById('g360-garmin-open');if(b){b.click();return true;}}catch(e){}
  }
  if(typeof previous==='function')return previous(id);
  return false;
};
})();
</script>
'''
def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    if not candidates: raise SystemExit('index.html introuvable')
    for p in candidates:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i<0: continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('Aucun index.html exploitable')
if __name__=='__main__':main()
