#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-MAP-COORDINATES-V3 -->'
P=r'''<!-- GABON360-MAP-COORDINATES-V3 -->
<style>#g360-coordinate-result{position:fixed;left:12px;top:72px;z-index:2147483000;background:#071522ee;color:#fff;border:1px solid #31506d;border-radius:10px;padding:7px 10px;font:12px system-ui,sans-serif;display:none}</style>
<script>
(function(){if(window.__G360_COORD_V3)return;window.__G360_COORD_V3=true;function boot(){var map=window.GABON360_REAL_LEAFLET_MAP;if(!map)return false;if(map.__g360Coord)return true;map.__g360Coord=true;var r=document.createElement('div');r.id='g360-coordinate-result';document.body.appendChild(r);map.on('click',function(e){var lat=e.latlng.lat,lon=e.latlng.lng;window.GABON360_SELECTED_COORDINATES={lat:lat,lon:lon,time:Date.now()};r.textContent='📍 '+lat.toFixed(6)+'°, '+lon.toFixed(6)+'°';r.style.display='block';window.dispatchEvent(new CustomEvent('gabon360:coordinates-selected',{detail:window.GABON360_SELECTED_COORDINATES}));if(window.G360Android&&window.G360Android.speak)window.G360Android.speak('Coordonnées sélectionnées. Latitude '+lat.toFixed(5)+' degrés. Longitude '+lon.toFixed(5)+' degrés.')});return true}var n=0,t=setInterval(function(){if(boot()||++n>60)clearInterval(t)},250);window.addEventListener('gabon360:map-ready',boot)})();
</script>
'''
def main():
 for p in sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts)):
  t=p.read_text(encoding='utf-8');
  if MARK in t: print('already',p);return
  i=t.lower().rfind('</body>')
  if i>=0:p.write_text(t[:i]+P+'\n'+t[i:],encoding='utf-8');print('injected',p);return
 raise SystemExit('No index.html found')
if __name__=='__main__':main()
