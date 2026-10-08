#!/usr/bin/env python3
"""Additive Garmin-class outdoor navigation layer for GABON 360 AI.
Uses only capabilities actually available from the Android/WebView device:
GNSS, device orientation, local storage, Leaflet map and browser file APIs.
No proprietary Garmin code or data is copied.
"""
from pathlib import Path

MARK="<!-- GABON360-TERRAIN-GARMIN-CLASS-V1 -->"
PAYLOAD=r'''<!-- GABON360-TERRAIN-GARMIN-CLASS-V1 -->
<style>
#g360-garmin-open{position:fixed;right:18px;bottom:14px;z-index:2147482000;background:#102a43;color:#fff;border:1px solid #42617b;border-radius:14px;padding:12px 15px;font:700 14px system-ui}
#g360-garmin-modal{position:fixed;inset:0;z-index:2147482500;display:none;background:#020913f5;overflow:auto;padding:10px}
#g360-garmin-card{width:min(980px,98vw);margin:auto;background:#081726;color:#eef6ff;border:1px solid #31506d;border-radius:16px;padding:12px;font:13px system-ui;box-sizing:border-box}
.g360-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin:7px 0}
.g360-gbox{background:#071522;border:1px solid #193047;border-radius:10px;padding:8px}
.g360-ga{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin:8px 0}
.g360-ga button,.g360-gclose{background:#102337;color:#fff;border:1px solid #31506d;border-radius:9px;padding:9px;font-weight:700}
.g360-glist{max-height:150px;overflow:auto}.g360-gitem{padding:7px;border-bottom:1px solid #193047;display:flex;justify-content:space-between;gap:6px}
@media(max-width:620px){.g360-g{grid-template-columns:repeat(2,1fr)}.g360-ga{grid-template-columns:repeat(2,1fr)}}
</style>
<button id="g360-garmin-open" type="button">🧭 GPS terrain PRO</button>
<div id="g360-garmin-modal"><div id="g360-garmin-card">
<div style="display:flex;justify-content:space-between;align-items:center"><h2>🧭 Navigation terrain PRO</h2><button class="g360-gclose" id="g360-garmin-close">✕</button></div>
<div id="g360-gstatus">GPS arrêté</div>
<div id="g360-gmap" style="height:320px;border-radius:12px;overflow:hidden;margin:8px 0"></div>
<div class="g360-g">
<div class="g360-gbox"><b>Latitude / longitude</b><div id="g360-gpos">—</div></div>
<div class="g360-gbox"><b>Vitesse</b><div id="g360-gspeed">—</div></div>
<div class="g360-gbox"><b>Altitude</b><div id="g360-galt">—</div></div>
<div class="g360-gbox"><b>Précision</b><div id="g360-gacc">—</div></div>
<div class="g360-gbox"><b>Cap</b><div id="g360-ghead">—</div></div>
<div class="g360-gbox"><b>Distance parcourue</b><div id="g360-gdist">0 m</div></div>
<div class="g360-gbox"><b>Distance destination</b><div id="g360-gto">—</div></div>
<div class="g360-gbox"><b>ETA estimée</b><div id="g360-geta">—</div></div>
<div class="g360-gbox"><b>Dénivelé GPS</b><div id="g360-gelev">+0 / -0 m</div></div>
</div>
<div class="g360-ga">
<button id="g360-g-start">📡 Démarrer GPS</button><button id="g360-g-stop">⏹ Arrêter GPS</button><button id="g360-g-center">🎯 Centrer</button>
<button id="g360-g-record">⏺ Enregistrer trace</button><button id="g360-g-save">💾 Sauver trace</button><button id="g360-g-back">↩ Retour départ</button>
<button id="g360-g-wp">📌 Waypoint</button><button id="g360-g-route">🗺️ Route</button><button id="g360-g-goto">➡️ GOTO</button>
<button id="g360-g-offline">📦 Mode hors-ligne</button><button id="g360-g-gpx">⬇️ Export GPX</button><button id="g360-g-import">⬆️ Import GPX</button>
<button id="g360-g-near">🔎 Proximité</button><button id="g360-g-area">📐 Calcul surface</button><button id="g360-g-speak">🔊 Guide vocal</button><button id="g360-g-sat">🛰️ Couche satellite</button>
<button id="g360-g-clear">🗑 Effacer session</button>
</div>
<input id="g360-gpx-file" type="file" accept=".gpx,application/gpx+xml" style="display:none">
<div class="g360-gbox"><b>Waypoints / route active</b><div id="g360-glist" class="g360-glist">Aucun.</div></div>
<div class="g360-gbox" style="margin-top:7px"><b>Profil / trace</b><div id="g360-gtrace">Aucune trace active.</div></div>
<div class="g360-gbox" style="margin-top:7px"><b>État hors-ligne</b><div id="g360-goff">Cartographie locale disponible selon les données déjà chargées. Les fonds distants nécessitent le réseau.</div></div>
<p style="opacity:.75;font-size:11px">Fonctions de navigation inspirées des capacités générales des GPS outdoor : routes, traces, waypoints, retour départ, navigation point-à-point, cap, distance, altitude, GPX et mode dégradé. Les capteurs non présents sur le téléphone restent indisponibles.</p>
</div></div>
<script>
(function(){
var M=document.getElementById('g360-garmin-modal');if(!M)return;
var map=null,marker=null,watch=null,pos=null,start=null,trace=[],recording=false,last=null,total=0,up=0,down=0,heading=null,target=null,points=[],satLayer=null,satEnabled=false,lastOffRouteAlert=0,lastFixTime=0,voiceGuidance=false;
function $(x){return document.getElementById(x)}
function say(t){if(window.G360AvatarSpeak)window.G360AvatarSpeak(t);else if('speechSynthesis'in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(t))}}
function hav(a,b){var R=6371000,p=Math.PI/180,la=a.lat*p,lb=b.lat*p,dl=(b.lat-a.lat)*p,do_=(b.lon-a.lon)*p,x=Math.sin(dl/2)**2+Math.cos(la)*Math.cos(lb)*Math.sin(do_/2)**2;return 2*R*Math.atan2(Math.sqrt(x),Math.sqrt(1-x))}
function bear(a,b){var p=Math.PI/180,y=Math.sin((b.lon-a.lon)*p)*Math.cos(b.lat*p),x=Math.cos(a.lat*p)*Math.sin(b.lat*p)-Math.sin(a.lat*p)*Math.cos(b.lat*p)*Math.cos((b.lon-a.lon)*p);return (Math.atan2(y,x)/p+360)%360}
function fmt(p){return p.lat.toFixed(6)+', '+p.lon.toFixed(6)}
function relay(type,data){try{window.dispatchEvent(new CustomEvent('gabon360:'+type,{detail:Object.assign({module:'nav',source:'phone-gnss',timestamp:new Date().toISOString()},data||{})}))}catch(e){}}
function announce(t,sev){relay('terrain-alert',{message:t,severity:sev||'INFO',position:pos?{lat:pos.lat,lon:pos.lon}:null});if(voiceGuidance)say(t)}
function setOnlineStatus(){var n=$('g360-goff');if(n)n.textContent=(navigator.onLine?'Réseau internet disponible':'Hors réseau internet')+' · GPS et traces locales distincts des flux cartographiques distants.'}
function init(){if(map||!window.L)return;map=L.map($('g360-gmap')).setView([-0.65,11.65],6);L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap'}).addTo(map);satLayer=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,attribution:'Tiles © Esri'});map.on('click',function(e){points.push({lat:e.latlng.lat,lon:e.latlng.lng});render();say('Point ajouté à la route.');});}
function load(){if(window.L){init();return}var s=document.createElement('script');s.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';s.onload=init;document.head.appendChild(s);var c=document.createElement('link');c.rel='stylesheet';c.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';document.head.appendChild(c)}
function update(p){var c=p.coords;var q={lat:c.latitude,lon:c.longitude,alt:c.altitude,speed:c.speed||0,acc:c.accuracy};lastFixTime=Date.now();if(!start)start=q;if(last){var d=hav(last,q);if(recording)total+=d;if(Number.isFinite(q.alt)&&Number.isFinite(last.alt)){var dz=q.alt-last.alt;if(dz>0)up+=dz;else down-=dz}}last=q;pos=q;if(recording)trace.push({lat:q.lat,lon:q.lon,alt:q.alt,time:p.timestamp});$('g360-gpos').textContent=fmt(q);$('g360-gspeed').textContent=(q.speed*3.6).toFixed(1)+' km/h';$('g360-galt').textContent=Number.isFinite(q.alt)?q.alt.toFixed(1)+' m':'—';$('g360-gacc').textContent=q.acc.toFixed(1)+' m';$('g360-gdist').textContent=Math.round(total)+' m';$('g360-gelev').textContent='+'+Math.round(up)+' / -'+Math.round(down)+' m';$('g360-gstatus').textContent='GNSS actif · précision '+Math.round(q.acc)+' m · '+new Date(p.timestamp).toLocaleTimeString();relay('terrain-position',{position:{lat:q.lat,lon:q.lon,altitude:q.alt,speed:q.speed,accuracy:q.acc},recording:recording});if(q.acc>100)announce('Attention, la précision GPS est faible : '+Math.round(q.acc)+' mètres.','WARNING');if(target){var off=hav(q,target);if(off>250&&Date.now()-lastOffRouteAlert>60000){lastOffRouteAlert=Date.now();announce('Vous êtes à '+Math.round(off)+' mètres du point cible. Vérifiez votre itinéraire.','WARNING')}}if(map){if(marker)map.removeLayer(marker);marker=L.marker([q.lat,q.lon]).addTo(map);if(recording&&trace.length>1){if(window._gline)map.removeLayer(window._gline);window._gline=L.polyline(trace.map(x=>[x.lat,x.lon])).addTo(map)}}if(target){var d=hav(q,target),b=bear(q,target);$('g360-gto').textContent=d<1000?Math.round(d)+' m · '+Math.round(b)+'°':(d/1000).toFixed(2)+' km · '+Math.round(b)+'°';$('g360-geta').textContent=q.speed>0.5?Math.round(d/q.speed/60)+' min':'—';if(d<30)say('Vous êtes arrivé au waypoint.');}}
function startGps(){if(!navigator.geolocation){$('g360-gstatus').textContent='Géolocalisation indisponible';return}if(watch!==null)return;navigator.geolocation.getCurrentPosition(update,e=>{$('g360-gstatus').textContent='GPS indisponible · '+e.message},{enableHighAccuracy:true,timeout:20000,maximumAge:0});watch=navigator.geolocation.watchPosition(update,e=>{$('g360-gstatus').textContent='GPS · '+e.message},{enableHighAccuracy:true,timeout:20000,maximumAge:1000})}
function stopGps(){if(watch!==null){navigator.geolocation.clearWatch(watch);watch=null}$('g360-gstatus').textContent='GPS arrêté'}
function render(){var a=[];points.forEach((p,i)=>a.push('<div class="g360-gitem"><span>Point '+(i+1)+'<br>'+fmt(p)+'</span><b>'+((i&&hav(points[i-1],p)/1000).toFixed(2))+' km</b></div>'));$('g360-glist').innerHTML=a.join('')||'Aucun point.'}
function exportGpx(){var arr=trace.length?trace:points;if(!arr.length){say('Aucun point à exporter.');return}var body=arr.map(p=>'<trkpt lat="'+p.lat+'" lon="'+p.lon+'">'+(p.alt!=null?'<ele>'+p.alt+'</ele>':'')+'</trkpt>').join('');var xml='<?xml version="1.0"?><gpx version="1.1" creator="GABON 360 AI"><trk><name>GABON 360 AI</name><trkseg>'+body+'</trkseg></trk></gpx>';var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([xml],{type:'application/gpx+xml'}));a.download='gabon360-trace-'+Date.now()+'.gpx';a.click();URL.revokeObjectURL(a.href)}
function importGpx(text){var doc=new DOMParser().parseFromString(text,'application/xml'),els=[...doc.getElementsByTagName('trkpt')];if(!els.length)els=[...doc.getElementsByTagName('wpt')];trace=els.map(e=>({lat:+e.getAttribute('lat'),lon:+e.getAttribute('lon'),alt:+(e.querySelector('ele')?.textContent||NaN),time:Date.now()}));recording=false;$('g360-gtrace').textContent='GPX importé · '+trace.length+' points';if(map){if(window._gline)map.removeLayer(window._gline);window._gline=L.polyline(trace.map(x=>[x.lat,x.lon])).addTo(map);map.fitBounds(window._gline.getBounds())}say('Trace GPX importée. '+trace.length+' points.')}
$('g360-garmin-open').onclick=function(){M.style.display='block';setTimeout(()=>{load();if(map)map.invalidateSize()},50);startGps()};$('g360-garmin-close').onclick=()=>M.style.display='none';$('g360-g-start').onclick=startGps;$('g360-g-stop').onclick=stopGps;$('g360-g-center').onclick=()=>{if(pos&&map)map.setView([pos.lat,pos.lon],16)};$('g360-g-record').onclick=function(){recording=!recording;if(recording){trace=[];total=0;up=down=0;say('Enregistrement de trace activé.')}else say('Enregistrement de trace arrêté.');$('g360-gtrace').textContent=recording?'Trace active · 0 point':'Trace arrêtée · '+trace.length+' points'};$('g360-g-save').onclick=function(){localStorage.setItem('g360_garmin_track',JSON.stringify(trace));say('Trace enregistrée localement.')};$('g360-g-back').onclick=function(){if(start){target={lat:start.lat,lon:start.lon};say('Retour au point de départ activé.')}else say('Aucun départ enregistré.')};$('g360-g-wp').onclick=function(){if(pos){points.push({lat:pos.lat,lon:pos.lon});render();say('Waypoint enregistré.')}else say('Position GPS indisponible.')};$('g360-g-route').onclick=function(){say('Touchez la carte pour ajouter les points de la route.')} ;$('g360-g-goto').onclick=function(){if(points.length){target=points[points.length-1];say('Navigation GOTO vers le dernier point.')}else say('Aucun waypoint cible.')};$('g360-g-offline').onclick=function(){$('g360-goff').textContent='Mode terrain dégradé : GPS, traces, waypoints et GPX restent utilisables sans réseau. Les cartes distantes peuvent être indisponibles.';say('Mode hors-ligne terrain activé.')};$('g360-g-gpx').onclick=exportGpx;$('g360-g-import').onclick=()=>$('g360-gpx-file').click();$('g360-gpx-file').onchange=e=>{var f=e.target.files[0];if(f){var r=new FileReader();r.onload=()=>importGpx(r.result);r.readAsText(f)}};$('g360-g-near').onclick=function(){if(!pos){say('Position GPS indisponible.');return}if(map)map.setView([pos.lat,pos.lon],14);say('Recherche de proximité autour de votre position. Les points réellement présents sur la carte peuvent être consultés.')} ;$('g360-g-area').onclick=function(){if(points.length<3){say('Ajoutez au moins trois points pour calculer une surface.');return}var p=points,area=0;for(var i=0;i<p.length;i++){var j=(i+1)%p.length;area+=(p[i].lon*p[j].lat-p[j].lon*p[i].lat)}area=Math.abs(area)/2*111320*111320*Math.cos((p[0].lat+p[p.length-1].lat)/2*Math.PI/180);say('Surface approximative : '+(area/10000).toFixed(2)+' hectares.');$('g360-gtrace').textContent='Surface approximative · '+(area/10000).toFixed(2)+' ha'};$('g360-g-speak').onclick=function(){if(pos)say('Position '+fmt(pos)+'. Vitesse '+(pos.speed*3.6).toFixed(1)+' kilomètres heure.'+(target?' Distance destination '+Math.round(hav(pos,target))+' mètres.':''));else say('GPS indisponible.')};$('g360-g-clear').onclick=function(){points=[];trace=[];target=null;total=up=down=0;render();$('g360-gtrace').textContent='Session effacée.';if(window._gline&&map){map.removeLayer(window._gline);window._gline=null}say('Session de navigation effacée.')};
window.GABON360_TERRAIN_GARMIN_CLASS={version:'1.0',features:['GNSS','tracks','waypoints','routes','goto','back_to_start','off_course_ready','bearing','distance','eta','gps_altitude','elevation_gain_loss','gpx_import_export','area','offline_degraded','voice_guidance','map_click_route']};
})();
</script>'''

def main():
    paths=sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts))
    for p in paths:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
            print('injected:',p); return
    raise SystemExit('index.html introuvable')

if __name__=='__main__': main()
