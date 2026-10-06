#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-REAL-MAP-V1 -->'
PAYLOAD=r'''<!-- GABON360-REAL-MAP-V1 -->
<style>
#g360-real-map{position:absolute;inset:0;z-index:2;border-radius:12px;overflow:hidden;background:#071522}
#g360-real-map .leaflet-control-attribution{font-size:9px}
#g360-real-map-tools{position:absolute;right:12px;top:48px;z-index:1000;display:flex;gap:5px;flex-wrap:wrap}
#g360-real-map-tools button{border:1px solid #31506d;background:#102337;color:#fff;border-radius:8px;padding:7px 9px;font-weight:600}
#g360-real-map-status{position:absolute;left:12px;bottom:12px;z-index:1000;background:#07111de8;color:#dff;border:1px solid #31506d;border-radius:8px;padding:6px 8px;font-size:10px}
#g360-real-map .leaflet-control-zoom{margin-top:55px!important}
</style>
<script>
(function(){
 const BOUNDS=[[-4.0,8.5],[2.5,14.5]];
 function boot(){
  const host=document.querySelector('#g360-center .map'); if(!host||document.getElementById('g360-real-map'))return !!host;
  host.querySelectorAll('.mapgrid, .maptitle, .mapbadge, .g360-maptools').forEach(e=>e.remove());
  const box=document.createElement('div');box.id='g360-real-map';
  box.innerHTML='<div id="g360-real-map-tools"><button id="g360-map-road">🗺️ Carte</button><button id="g360-map-sat">🛰️ Satellite</button><button id="g360-map-gabon">🇬🇦 Gabon</button></div><div id="g360-real-map-status">Carte du Gabon · routes, rivières et lieux selon les données disponibles</div>';
  host.appendChild(box);
  if(!window.L){
   const css=document.createElement('link');css.rel='stylesheet';css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';document.head.appendChild(css);
   const js=document.createElement('script');js.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';js.onload=init;document.head.appendChild(js);
  }else init();
  function init(){
   if(!window.L||box.dataset.ready)return;box.dataset.ready='1';
   const map=L.map(box,{zoomControl:true,preferCanvas:true}).setView([-0.65,11.65],6);
   const roads=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'}).addTo(map);
   const sat=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:18,attribution:'Imagery © Esri'});
   L.rectangle(BOUNDS,{color:'#2adf9b',weight:1,fill:false,interactive:false}).addTo(map);
   map.fitBounds(BOUNDS,{padding:[18,18]});
   document.getElementById('g360-map-road').onclick=()=>{if(!map.hasLayer(roads))roads.addTo(map);if(map.hasLayer(sat))map.removeLayer(sat);document.getElementById('g360-real-map-status').textContent='Carte Gabon · routes, rivières et lieux · zoom actif'};
   document.getElementById('g360-map-sat').onclick=()=>{if(map.hasLayer(roads))map.removeLayer(roads);if(!map.hasLayer(sat))sat.addTo(map);document.getElementById('g360-real-map-status').textContent='Imagerie satellite publique · pas de vidéo satellite en direct'};
   document.getElementById('g360-map-gabon').onclick=()=>map.fitBounds(BOUNDS,{padding:[18,18]});
   window.GABON360_REAL_MAP={version:'1.0',center:[-0.65,11.65],bounds:BOUNDS,zoom:true,roads:true,rivers:true,satellite_layer:true};
   window.dispatchEvent(new CustomEvent('gabon360:map-ready'));
  }
  return true;
 }
 if(!boot()){let n=0;const t=setInterval(()=>{if(boot()||++n>40)clearInterval(t)},200)}
})();
</script>
'''
def main():
 candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
 for p in candidates:
  t=p.read_text(encoding='utf-8')
  if MARK in t: print('already:',p);return
  i=t.lower().rfind('</body>')
  if i>=0:
   p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8');print('injected:',p);return
 raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
