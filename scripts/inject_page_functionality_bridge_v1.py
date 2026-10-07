#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-PAGE-FUNCTIONALITY-BRIDGE-V1 -->'
PAYLOAD=r'''<!-- GABON360-PAGE-FUNCTIONALITY-BRIDGE-V1 -->
<script>
(function(){
if(window.__G360_PAGE_FUNCTIONALITY_BRIDGE_V1)return;
window.__G360_PAGE_FUNCTIONALITY_BRIDGE_V1=true;
function go(page){
  try{
    if(window.GABON360_OPEN_ENHANCED_PAGE){
      window.GABON360_OPEN_ENHANCED_PAGE(page);
      return true;
    }
  }catch(e){}
  return false;
}
function createReport(){
  var key='gabon360_operational_records_v1',d;
  try{d=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){d={}};
  d.reports=Array.isArray(d.reports)?d.reports:[];
  var c=window.GABON360_SELECTED_COORDINATES||null;
  var r={id:Date.now(),title:'Rapport GABON 360 AI',created_at:new Date().toISOString(),status:'draft',coordinates:c};
  d.reports.push(r);localStorage.setItem(key,JSON.stringify(d));
  return r;
}
window.addEventListener('gabon360:page-action',function(e){
  var d=e.detail||{},page=d.page,action=String(d.action||'').toLowerCase();
  if(page==='reports'&&action.indexOf('nouveau')>=0){
    var r=createReport();
    if(go('reports'))setTimeout(function(){
      var x=document.querySelector('#g360-v2 .g360-v2-result');
      if(x)x.textContent='Rapport créé en brouillon. ID '+r.id;
    },30);
    return;
  }
  if(page)go(page);
});
window.GABON360_PAGE_BRIDGE_V1={version:'1.0',open:go};
})();
</script>
'''
def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    if not candidates: raise SystemExit('index.html introuvable')
    for p in candidates:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in t:
            print('already:',p); return
        i=t.lower().rfind('</body>')
        if i<0: continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('Aucun index.html exploitable')
if __name__=='__main__': main()
