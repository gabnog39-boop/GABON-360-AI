#!/usr/bin/env python3
"""Inject the public Copernicus satellite discovery panel into the APK web UI.

The injector is build-time and self-contained: it does not embed credentials and
it never presents catalog metadata as continuous live video.
"""
from __future__ import annotations
from pathlib import Path

INJECTOR_VERSION = "1.1"
MARKER = "<!-- GABON360-SATELLITE-PANEL-V1 -->"
PAYLOAD = r'''<!-- GABON360-SATELLITE-PANEL-V1 -->
<style>
#g360-satellite-panel{position:fixed;right:14px;bottom:14px;z-index:99999;width:min(390px,calc(100vw - 28px));max-height:62vh;overflow:auto;background:rgba(8,16,28,.96);color:#eef6ff;border:1px solid rgba(77,170,255,.45);border-radius:16px;box-shadow:0 12px 36px rgba(0,0,0,.42);font:14px/1.4 system-ui,sans-serif;backdrop-filter:blur(10px)}
#g360-satellite-panel .g360-head{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.1)}
#g360-satellite-panel .g360-title{font-weight:700}.g360-pill{font-size:11px;padding:3px 7px;border-radius:999px;background:#173b2a;color:#9ff0bf}
#g360-satellite-panel .g360-body{padding:12px 14px}.g360-row{display:flex;gap:8px;align-items:center;margin-bottom:9px}.g360-row select,.g360-row button{border-radius:9px;border:1px solid rgba(255,255,255,.16);padding:8px;background:#152236;color:#fff}.g360-row button{cursor:pointer;font-weight:600}.g360-status{font-size:12px;opacity:.82;margin:6px 0 10px}.g360-card{padding:9px 10px;margin:7px 0;border-radius:10px;background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.08)}.g360-card b{display:block;margin-bottom:3px}.g360-meta{font-size:11px;opacity:.72}.g360-note{font-size:11px;opacity:.68;margin-top:10px}
</style>
<div id="g360-satellite-panel" aria-label="Données satellites publiques Copernicus">
  <div class="g360-head"><span class="g360-title">🛰️ Satellites — Gabon</span><span class="g360-pill">PUBLIC / CATALOGUE</span></div>
  <div class="g360-body">
    <div class="g360-row"><select id="g360-sat-collection"><option value="sentinel-2-l2a">Sentinel-2 L2A</option><option value="sentinel-2-l1c">Sentinel-2 L1C</option><option value="sentinel-1-grd">Sentinel-1 GRD</option></select><button id="g360-sat-refresh" type="button">Actualiser</button></div>
    <div id="g360-sat-status" class="g360-status">Prêt à interroger le catalogue Copernicus…</div>
    <div id="g360-sat-results"></div>
    <div class="g360-note">Observations/catalogue reçues : pas de vidéo satellite continue et aucune action automatique.</div>
  </div>
</div>
<script>
(function(){
  const ENDPOINT='https://stac.dataspace.copernicus.eu/v1/search';
  const BBOX=[8.5,-4.0,14.5,2.5];
  const s=document.getElementById('g360-sat-status'),o=document.getElementById('g360-sat-results'),c=document.getElementById('g360-sat-collection'),b=document.getElementById('g360-sat-refresh');
  if(!s||!o||!c||!b)return;
  const esc=v=>String(v??'').replace(/[&<>\"']/g,q=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[q]));
  function publish(features){
    window.GABON360_SATELLITE_RESULTS={provider:'copernicus_data_space_ecosystem',area:'Gabon',live:false,received_at:new Date().toISOString(),count:features.length,features:features};
    window.dispatchEvent(new CustomEvent('gabon360:satellite-results',{detail:window.GABON360_SATELLITE_RESULTS}));
  }
  async function load(){
    s.textContent='Connexion au catalogue Copernicus…';o.innerHTML='';b.disabled=true;
    try{
      const r=await fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({collections:[c.value],bbox:BBOX,limit:8,query:{'eo:cloud_cover':{lte:60}}})});
      if(!r.ok)throw Error('HTTP '+r.status);
      const d=await r.json(),f=Array.isArray(d.features)?d.features:[];publish(f);
      s.textContent=f.length+' observation(s) trouvée(s) — Copernicus CDSE';
      o.innerHTML=f.length?f.map(i=>{const p=i.properties||{},cl=p['eo:cloud_cover'];return '<div class="g360-card"><b>'+esc(i.id||'Observation')+'</b><div class="g360-meta">'+esc(p.datetime||'date inconnue')+(cl!=null?' · nuages '+Number(cl).toFixed(1)+'%':'')+'</div></div>'}).join(''):'<div class="g360-card">Aucune observation correspondante.</div>';
    }catch(e){publish([]);s.textContent='Catalogue indisponible : '+(e&&e.message?e.message:'erreur réseau');o.innerHTML='<div class="g360-card">Aucune donnée simulée ne sera affichée.</div>'}finally{b.disabled=false}
  }
  b.onclick=load;c.onchange=load;load();
})();
</script>
'''

def main() -> None:
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARKER in t:
            print('already:',p);return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8');print('injected:',p);return
    raise SystemExit('No suitable index.html found')

if __name__=='__main__': main()
