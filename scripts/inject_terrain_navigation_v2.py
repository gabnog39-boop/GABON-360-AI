#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-TERRAIN-NAV-V2 -->'
PAYLOAD=r'''<!-- GABON360-TERRAIN-NAV-V2 -->
<style>
#g360-terrain-v2-open{position:fixed!important;left:26px!important;bottom:14px!important;z-index:2147482000!important;background:#0b1a2a!important;color:#fff!important;border:1px solid #31506d!important;border-radius:14px!important;padding:12px 16px!important;font:600 14px system-ui,sans-serif!important;box-shadow:0 10px 28px #0009!important}
#g360-terrain-v2-modal{position:fixed!important;inset:0!important;z-index:2147482500!important;display:none!important;background:#020913ee!important;align-items:flex-start!important;justify-content:center!important;padding:10px!important;overflow:auto!important}
#g360-terrain-v2-card{width:min(900px,98vw)!important;max-height:96vh!important;overflow:auto!important;background:#091827!important;color:#eef6ff!important;border:1px solid #31506d!important;border-radius:16px!important;padding:12px!important;box-sizing:border-box!important;font:13px system-ui,sans-serif!important}
#g360-terrain-v2-map{height:330px!important;width:100%!important;border-radius:12px!important;overflow:hidden!important;border:1px solid #31506d!important;background:#152536!important}
.g360-t2-row{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important;margin:8px 0!important}.g360-t2-box{background:#071522!important;border:1px solid #193047!important;border-radius:11px!important;padding:9px!important}.g360-t2-actions{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:7px!important;margin:8px 0!important}.g360-t2-actions button,#g360-terrain-v2-close{border:1px solid #31506d!important;background:#102337!important;color:#fff!important;border-radius:9px!important;padding:9px!important;font-weight:600!important}.g360-t2-list{max-height:180px!important;overflow:auto!important}.g360-t2-item{display:flex!important;justify-content:space-between!important;align-items:center!important;gap:6px!important;padding:7px!important;border-bottom:1px solid #193047!important}.g360-t2-small{opacity:.78!important;font-size:11px!important}.g360-t2-ok{color:#9ff2c2!important}.g360-t2-warn{color:#ffd28a!important}
@media(max-width:560px){.g360-t2-actions{grid-template-columns:repeat(2,minmax(0,1fr))!important}.g360-t2-row{grid-template-columns:1fr!important}#g360-terrain-v2-map{height:300px!important}}
</style>
<button id="g360-terrain-v2-open" type="button">🧭 Navigation terrain</button>
<div id="g360-terrain-v2-modal" aria-hidden="true"><div id="g360-terrain-v2-card">
 <div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><h2 style="margin:2px 0">🧭 Navigation terrain — GNSS/GPS</h2><button id="g360-terrain-v2-close">✕</button></div>
 <div id="g360-t2-status" class="g360-t2-warn">GPS en attente. Appuyez sur « Démarrer GPS ».</div>
 <div class="g360-t2-row">
  <div class="g360-t2-box"><b>Position</b><div id="g360-t2-pos">—</div></div>
  <div class="g360-t2-box"><b>Altitude</b><div id="g360-t2-alt">—</div></div>
  <div class="g360-t2-box"><b>Précision</b><div id="g360-t2-acc">—</div></div>
  <div class="g360-t2-box"><b>🧭 Boussole / cap</b><div id="g360-t2-heading">—</div></div>
 </div>
 <div id="g360-terrain-v2-map"></div>
 <div class="g360-t2-actions">
  <button id="g360-t2-start">📡 Démarrer GPS</button><button id="g360-t2-center">🎯 Ma position</button><button id="g360-t2-pick">📍 Prendre un point</button>
  <button id="g360-t2-compass">🧭 Activer boussole</button><button id="g360-t2-track">⏺️ Démarrer tracé</button><button id="g360-t2-save-track">💾 Enregistrer tracé</button>
  <button id="g360-t2-stop-track">⏹️ Arrêter tracé</button><button id="g360-t2-save-wp">📌 Enregistrer waypoint</button><button id="g360-t2-goto">➡️ GOTO dernier point</button>
  <button id="g360-t2-voice">🔊 AI navigation</button><button id="g360-t2-stopvoice">🔇 Stop voix</button><button id="g360-t2-clear">🗑️ Effacer session</button>
 </div>
 <div class="g360-t2-row"><div class="g360-t2-box"><b>Point sélectionné</b><div id="g360-t2-picked">Aucun. Touchez la carte pour obtenir latitude/longitude.</div></div><div class="g360-t2-box"><b>GOTO</b><div id="g360-t2-goto-info">Aucun waypoint cible.</div></div></div>
 <div class="g360-t2-box"><b>📌 Waypoints enregistrés</b><div id="g360-t2-wplist" class="g360-t2-list">Aucun waypoint.</div></div>
 <div class="g360-t2-box" style="margin-top:8px"><b>🧭 Tracé courant</b><div id="g360-t2-trackinfo">Tracé arrêté · 0 point</div></div>
 <p class="g360-t2-small">Les coordonnées et la position affichées proviennent du téléphone lorsque le GNSS est disponible. Aucun emplacement fictif n'est créé. Les fonctions GOTO et tracé calculent uniquement à partir des points réellement reçus ou sélectionnés.</p>
</div></div>
<script>
(function(){
 var old=document.getElementById('g360-terrain-nav');if(old)old.style.display='none';var oldm=document.getElementById('g360-terrain-modal');if(oldm)oldm.style.display='none';
 var modal=document.getElementById('g360-terrain-v2-modal'),mapEl=document.getElementById('g360-terrain-v2-map');if(!modal||!mapEl)return;
 var pos=null,watch=null,trackOn=false,track=[],trackLine=null,marker=null,picked=null,heading=null,compassOn=false,lastVoice=0,leaf=null;
 var waypoints=[];try{waypoints=JSON.parse(localStorage.getItem('g360_waypoints_v2')||'[]')}catch(e){}
 function say(t){window.dispatchEvent(new CustomEvent('gabon360:ai-speak',{detail:{text:t,source:'terrain-navigation'}}));if('speechSynthesis' in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(t));}}
 function el(id){return document.getElementById(id)}
 function status(t,c){el('g360-t2-status').textContent=t;el('g360-t2-status').className=c||'g360-t2-ok'}
 function hav(a,b){var R=6371000,la1=a.lat*Math.PI/180,la2=b.lat*Math.PI/180,dl=(b.lat-a.lat)*Math.PI/180,do_=(b.lon-a.lon)*Math.PI/180;var x=Math.sin(dl/2)**2+Math.cos(la1)*Math.cos(la2)*Math.sin(do_/2)**2;return 2*R*Math.atan2(Math.sqrt(x),Math.sqrt(1-x))}
 function bearing(a,b){var p=Math.PI/180,y=Math.sin((b.lon-a.lon)*p)*Math.cos(b.lat*p),x=Math.cos(a.lat*p)*Math.sin(b.lat*p)-Math.sin(a.lat*p)*Math.cos(b.lat*p)*Math.cos((b.lon-a.lon)*p);return (Math.atan2(y,x)/p+360)%360}
 function fmt(p){return p.lat.toFixed(6)+'°, '+p.lon.toFixed(6)+'°'}
 function initMap(){if(leaf||!window.L)return;leaf=L.map(mapEl,{zoomControl:true}).setView([ -0.65,11.65],6);L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap'}).addTo(leaf);leaf.on('click',function(e){picked={lat:e.latlng.lat,lon:e.latlng.lng};el('g360-t2-picked').textContent=fmt(picked)+' · point choisi sur la carte';if(marker)leaf.removeLayer(marker);marker=L.marker([picked.lat,picked.lon]).addTo(leaf).bindPopup('Point sélectionné<br>'+fmt(picked)).openPopup();say('Point sélectionné. Latitude '+picked.lat.toFixed(5)+' degrés, longitude '+picked.lon.toFixed(5)+' degrés.')});}
 function loadLeaf(){if(window.L){initMap();return}var s=document.createElement('script');s.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';s.onload=initMap;document.head.appendChild(s);var c=document.createElement('link');c.rel='stylesheet';c.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';document.head.appendChild(c)}
 function gpsSuccess(p){pos={lat:p.coords.latitude,lon:p.coords.longitude,alt:p.coords.altitude,acc:p.coords.accuracy,time:p.timestamp};el('g360-t2-pos').textContent=fmt(pos);el('g360-t2-alt').textContent=Number.isFinite(pos.alt)?pos.alt.toFixed(1)+' m':'Non fournie';el('g360-t2-acc').textContent=Number.isFinite(pos.acc)?pos.acc.toFixed(1)+' m':'Non fournie';status('GPS actif · dernière position '+new Date(p.timestamp).toLocaleTimeString(),'g360-t2-ok');if(leaf){if(marker)leaf.removeLayer(marker);marker=L.marker([pos.lat,pos.lon]).addTo(leaf).bindPopup('Position GPS<br>'+fmt(pos));if(trackOn){track.push({lat:pos.lat,lon:pos.lon,time:pos.time});if(trackLine)leaf.removeLayer(trackLine);trackLine=L.polyline(track.map(x=>[x.lat,x.lon]));trackLine.addTo(leaf);el('g360-t2-trackinfo').textContent='Tracé actif · '+track.length+' point(s)';}}if(Date.now()-lastVoice>25000){lastVoice=Date.now();say('Position GPS reçue. '+fmt(pos)+'. Précision '+Math.round(pos.acc)+' mètres.');}}
 function gpsError(e){status('GPS indisponible · '+(e&&e.message?e.message:'autorisation ou signal GNSS manquant'),'g360-t2-warn');say('La position GPS n’est pas disponible. Vérifiez la localisation du téléphone et l’autorisation de GABON 360 AI.');}
 function startGps(){if(!navigator.geolocation){gpsError({message:'géolocalisation absente du WebView'});return}status('Recherche du signal GNSS…','g360-t2-warn');navigator.geolocation.getCurrentPosition(gpsSuccess,gpsError,{enableHighAccuracy:true,timeout:20000,maximumAge:0});if(watch===null)watch=navigator.geolocation.watchPosition(gpsSuccess,gpsError,{enableHighAccuracy:true,timeout:20000,maximumAge:2000})}
 function enableCompass(){if(compassOn)return;var handler=function(e){var h=e.webkitCompassHeading!=null?e.webkitCompassHeading:(e.absolute&&e.alpha!=null?(360-e.alpha):null);if(h==null)return;heading=h;el('g360-t2-heading').textContent=Math.round(h)+'°';};window.addEventListener('deviceorientationabsolute',handler,true);window.addEventListener('deviceorientation',handler,true);compassOn=true;status('Boussole active · orientation du téléphone reçue lorsque disponible','g360-t2-ok')}
 function renderWps(){var box=el('g360-t2-wplist');if(!waypoints.length){box.textContent='Aucun waypoint.';return}box.innerHTML=waypoints.map(function(w,i){return '<div class="g360-t2-item"><span><b>#'+(i+1)+' '+w.name+'</b><br><span class="g360-t2-small">'+fmt(w)+'</span></span><button data-goto="'+i+'">GOTO</button></div>'}).join('');box.querySelectorAll('[data-goto]').forEach(function(b){b.onclick=function(){goto(Number(b.dataset.goto))}})}
 function saveWp(){var p=picked||pos;if(!p){say('Aucun point réel ou sélectionné à enregistrer.');return}var name='WP-'+(waypoints.length+1)+'-'+new Date().toLocaleTimeString();waypoints.push({name:name,lat:p.lat,lon:p.lon,time:Date.now()});localStorage.setItem('g360_waypoints_v2',JSON.stringify(waypoints));renderWps();say('Waypoint enregistré. '+name+'. '+fmt(p));}
 function goto(i){var w=waypoints[i];if(!w){say('Aucun waypoint cible.');return}if(!pos){say('Position GPS actuelle indisponible.');return}var d=hav(pos,w),b=bearing(pos,w);el('g360-t2-goto-info').textContent=d<1000?Math.round(d)+' m · cap '+Math.round(b)+'°':' '+(d/1000).toFixed(2)+' km · cap '+Math.round(b)+'°';say('GOTO '+w.name+'. Distance '+(d<1000?Math.round(d)+' mètres':(d/1000).toFixed(2)+' kilomètres')+'. Cap '+Math.round(b)+' degrés.');if(leaf){leaf.setView([w.lat,w.lon],Math.max(leaf.getZoom(),13));if(marker)marker.bindPopup('GOTO '+w.name+'<br>'+fmt(w)).openPopup()}}
 function saveTrack(){if(!track.length){say('Aucun tracé réel à enregistrer.');return}localStorage.setItem('g360_track_last_v2',JSON.stringify(track));say('Tracé enregistré avec '+track.length+' points.');}
 function clearAll(){track=[];picked=null;if(trackLine&&leaf)leaf.removeLayer(trackLine);el('g360-t2-trackinfo').textContent='Tracé arrêté · 0 point';el('g360-t2-picked').textContent='Aucun. Touchez la carte pour obtenir latitude/longitude.';say('Session de navigation effacée. Les waypoints enregistrés restent conservés.');}
 el('g360-terrain-v2-open').onclick=function(){modal.style.display='flex';modal.setAttribute('aria-hidden','false');setTimeout(function(){loadLeaf();if(leaf)leaf.invalidateSize()},80);if(!pos)startGps()};el('g360-terrain-v2-close').onclick=function(){modal.style.display='none';modal.setAttribute('aria-hidden','true')};
 el('g360-t2-start').onclick=startGps;el('g360-t2-center').onclick=function(){if(!pos){say('Position GPS indisponible.');return}if(leaf){leaf.setView([pos.lat,pos.lon],16);if(marker)marker.openPopup()}};el('g360-t2-pick').onclick=function(){say('Touchez directement la carte pour prendre les coordonnées du point.');if(leaf)leaf.getContainer().style.cursor='crosshair'};el('g360-t2-compass').onclick=enableCompass;el('g360-t2-track').onclick=function(){trackOn=true;track=[];if(pos)track.push({lat:pos.lat,lon:pos.lon,time:Date.now()});el('g360-t2-trackinfo').textContent='Tracé actif · '+track.length+' point(s)';say('Enregistrement du tracé activé.');};el('g360-t2-stop-track').onclick=function(){trackOn=false;el('g360-t2-trackinfo').textContent='Tracé arrêté · '+track.length+' point(s)';say('Enregistrement du tracé arrêté.');};el('g360-t2-save-track').onclick=saveTrack;el('g360-t2-save-wp').onclick=saveWp;el('g360-t2-goto').onclick=function(){goto(waypoints.length-1)};el('g360-t2-voice').onclick=function(){if(pos)say('Navigation IA active. Position '+fmt(pos)+'. '+(heading!=null?'Cap actuel '+Math.round(heading)+' degrés.':'Boussole non disponible.'));else say('Navigation IA prête, mais la position GPS n’est pas encore disponible.');};el('g360-t2-stopvoice').onclick=function(){if('speechSynthesis'in window)speechSynthesis.cancel()};el('g360-t2-clear').onclick=clearAll;renderWps();
 window.GABON360_TERRAIN_NAV_V2={version:'2.0',mapClickCoordinates:true,compass:true,waypoints:true,trackRecording:true,goto:true,aiVoice:true};
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i<0: continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
