#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-PAGE-FUNCTIONALITY-V2 -->'

PAYLOAD=r'''<!-- GABON360-PAGE-FUNCTIONALITY-V2 -->
<style>
#g360-v2-launch{position:fixed;left:10px;bottom:14px;z-index:2147483005;background:#102a43;color:#fff;border:1px solid #42617b;border-radius:12px;padding:10px 13px;font:700 13px system-ui}
#g360-v2{position:fixed;inset:0;z-index:2147483006;display:none;background:#020913f7;color:#eef6ff;font:13px system-ui;overflow:auto}
#g360-v2-card{width:min(1000px,97vw);margin:10px auto;background:#081726;border:1px solid #31506d;border-radius:16px;padding:12px;box-sizing:border-box}
#g360-v2-head{position:sticky;top:0;z-index:4;background:#081726ee;padding:8px 0;display:flex;align-items:center;gap:8px}
#g360-v2-head b{flex:1;font-size:17px}
#g360-v2 button,#g360-v2 select,#g360-v2 input{background:#102337;color:#fff;border:1px solid #31506d;border-radius:9px;padding:8px;box-sizing:border-box}
#g360-v2 button{font-weight:700;touch-action:manipulation}
.g360-v2-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.g360-v2-box{background:#071522;border:1px solid #193047;border-radius:11px;padding:10px;margin:7px 0}
.g360-v2-actions{display:flex;flex-wrap:wrap;gap:6px;margin:7px 0}
.g360-v2-result{white-space:pre-wrap;min-height:42px}
.g360-v2-map{height:330px;border-radius:11px;overflow:hidden;margin:8px 0}
.g360-v2-ok{color:#9ff0bf}.g360-v2-wait{color:#ffd28a}.g360-v2-bad{color:#ff9f9f}
.g360-v2-list{max-height:240px;overflow:auto}
.g360-v2-item{border-bottom:1px solid #193047;padding:8px}
@media(max-width:680px){.g360-v2-grid{grid-template-columns:1fr}}
</style>
<button id="g360-v2-launch" type="button">⚙️ Outils renforcés</button>
<div id="g360-v2" aria-hidden="true"><div id="g360-v2-card"></div></div>
<script>
(function(){
if(window.__G360_PAGE_FUNCTIONALITY_V2)return;
window.__G360_PAGE_FUNCTIONALITY_V2=true;
var root=document.getElementById('g360-v2'),card=document.getElementById('g360-v2-card');
var KEY='gabon360_operational_records_v1';
function db(){try{return JSON.parse(localStorage.getItem(KEY)||'{"reports":[],"events":[],"waypoints":[],"tracks":[],"missions":[],"sources":[]}')}catch(e){return {reports:[],events:[],waypoints:[],tracks:[],missions:[],sources:[]}}}
function save(x){localStorage.setItem(KEY,JSON.stringify(x))}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function open(){root.style.display='block';root.setAttribute('aria-hidden','false')}
function close(){root.style.display='none';root.setAttribute('aria-hidden','true')}
function out(t){var e=card.querySelector('.g360-v2-result');if(e)e.textContent=String(t)}
function speak(t){try{if(window.G360AvatarSpeak){window.G360AvatarSpeak(t);return}}catch(e){}try{if(window.G360Android&&G360Android.speak){G360Android.speak(t);return}}catch(e){}try{speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(t))}catch(e){}}
function selected(){return window.GABON360_SELECTED_COORDINATES||null}
function hav(a,b){var R=6371000,p=Math.PI/180,la=a.lat*p,lb=b.lat*p,dl=(b.lat-a.lat)*p,do_=(b.lon-a.lon)*p,x=Math.sin(dl/2)**2+Math.cos(la)*Math.cos(lb)*Math.sin(do_/2)**2;return 2*R*Math.atan2(Math.sqrt(x),Math.sqrt(1-x))}
function mapClickSetup(map,fn){if(!map||map.__g360V2Click)return;map.__g360V2Click=true;map.on('click',fn)}
function mapLoader(host,center,zoom){return new Promise(function(resolve){if(!window.L){var css=document.createElement('link');css.rel='stylesheet';css.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';document.head.appendChild(css);var js=document.createElement('script');js.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';js.onload=function(){resolve(true)};js.onerror=function(){resolve(false)};document.head.appendChild(js)}else resolve(true)}).then(function(ok){if(!ok||!window.L)return null;var m=L.map(host).setView(center||[-0.65,11.65],zoom||6);L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'}).addTo(m);return m})}
function shell(title,body){card.innerHTML='<div id="g360-v2-head"><b>'+esc(title)+'</b><button id="g360-v2-close">✕</button></div>'+body;open();card.querySelector('#g360-v2-close').onclick=close}
function mapPage(){
shell('🗺️ Carte / SIG — sélection interactive','<div class="g360-v2-box">Touchez ou cliquez directement sur la carte pour placer un point. Les coordonnées WGS84 seront affichées et enregistrées localement.</div><div id="g360-v2-map" class="g360-v2-map"></div><div class="g360-v2-grid"><div class="g360-v2-box"><b>Point sélectionné</b><div id="g360-v2-coord">Aucun point.</div></div><div class="g360-v2-box"><b>Actions</b><div class="g360-v2-actions"><button id="g360-v2-savepoint">📌 Enregistrer point</button><button id="g360-v2-gps">📍 Ma position</button><button id="g360-v2-clearpoints">🗑 Effacer points</button></div></div></div><div class="g360-v2-box"><b>Points enregistrés</b><div id="g360-v2-list" class="g360-v2-list"></div></div><div class="g360-v2-box g360-v2-result">Touchez la carte.</div>');
var m=window.GABON360_REAL_LEAFLET_MAP||null;
function ready(mm){if(!mm)return;window.GABON360_REAL_LEAFLET_MAP=mm;var marker=null;function pick(e){var c={lat:e.latlng.lat,lon:e.latlng.lng,time:Date.now()};window.GABON360_SELECTED_COORDINATES=c;if(marker)mm.removeLayer(marker);marker=L.marker([c.lat,c.lon]).addTo(mm);card.querySelector('#g360-v2-coord').textContent=c.lat.toFixed(6)+'°, '+c.lon.toFixed(6)+'°';out('Point sélectionné : '+c.lat.toFixed(6)+'°, '+c.lon.toFixed(6)+'°');window.dispatchEvent(new CustomEvent('gabon360:coordinates-selected',{detail:c}));}
mapClickSetup(mm,pick);
card.querySelector('#g360-v2-savepoint').onclick=function(){var c=selected();if(!c){out('Sélectionnez d’abord un point sur la carte.');return}var d=db();d.waypoints=d.waypoints||[];d.waypoints.push({lat:c.lat,lon:c.lon,created_at:new Date().toISOString(),source:'carte'});save(d);renderList();out('Point enregistré : '+c.lat.toFixed(6)+', '+c.lon.toFixed(6));};
card.querySelector('#g360-v2-gps').onclick=function(){if(!navigator.geolocation){out('GPS indisponible.');return}navigator.geolocation.getCurrentPosition(function(p){var c={lat:p.coords.latitude,lon:p.coords.longitude,accuracy:p.coords.accuracy,altitude:p.coords.altitude,time:Date.now()};window.GABON360_SELECTED_COORDINATES=c;mm.setView([c.lat,c.lon],15);pick({latlng:L.latLng(c.lat,c.lon)});out('Position GPS : '+c.lat.toFixed(6)+', '+c.lon.toFixed(6)+' · précision '+(c.accuracy||'—')+' m')},function(e){out('GPS indisponible : '+e.message)},{enableHighAccuracy:true,timeout:15000,maximumAge:5000})};
card.querySelector('#g360-v2-clearpoints').onclick=function(){var d=db();d.waypoints=[];save(d);renderList();out('Points locaux effacés.')};
function renderList(){var d=db(),l=card.querySelector('#g360-v2-list');l.innerHTML=(d.waypoints||[]).slice(-50).reverse().map(function(w,i){return '<div class="g360-v2-item">📌 '+Number(w.lat).toFixed(6)+', '+Number(w.lon).toFixed(6)+'<br><small>'+esc(w.created_at||'')+'</small></div>'}).join('')||'Aucun point enregistré.'}
renderList();
if(m)ready(m);else mapLoader(card.querySelector('#g360-v2-map'),[-0.65,11.65],6).then(ready)
}
function satPage(){
shell('🛰️ Satellite — recherche Copernicus renforcée','<div class="g360-v2-grid"><div class="g360-v2-box"><label>Collection<select id="g360-sat-col"><option>sentinel-2-l2a</option><option>sentinel-2-l1c</option><option>sentinel-1-grd</option></select></label></div><div class="g360-v2-box"><label>Nuages max %<input id="g360-sat-cloud" type="number" value="60" min="0" max="100"></label></div><div class="g360-v2-box"><label>Date début<input id="g360-sat-from" type="date"></label></div><div class="g360-v2-box"><label>Date fin<input id="g360-sat-to" type="date"></label></div></div><div class="g360-v2-actions"><button id="g360-sat-search">🔎 Rechercher</button><button id="g360-sat-selected">📍 Utiliser le point carte</button><button id="g360-sat-reset">🇬🇦 Gabon entier</button></div><div id="g360-sat-result" class="g360-v2-box g360-v2-result">Aucune recherche lancée.</div><div id="g360-sat-list" class="g360-v2-list g360-v2-box"></div>');
var bbox=[8.5,-4,14.5,2.5];
function doSearch(){var col=card.querySelector('#g360-sat-col').value,cloud=Number(card.querySelector('#g360-sat-cloud').value||60),f=card.querySelector('#g360-sat-from').value,t=card.querySelector('#g360-sat-to').value;var body={collections:[col],bbox:bbox,limit:20,query:{'eo:cloud_cover':{lte:cloud}}};if(f&&t)body.datetime=f+'T00:00:00Z/'+t+'T23:59:59Z';var res=card.querySelector('#g360-sat-result'),list=card.querySelector('#g360-sat-list');res.textContent='Recherche Copernicus…';fetch('https://stac.dataspace.copernicus.eu/v1/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){if(!r.ok)throw Error('HTTP '+r.status);return r.json()}).then(function(d){var fs=Array.isArray(d.features)?d.features:[];window.GABON360_SATELLITE_RESULTS={provider:'Copernicus CDSE',live:false,count:fs.length,features:fs,received_at:new Date().toISOString()};res.textContent=fs.length+' observation(s) trouvée(s). Catalogue public, pas de vidéo satellite continue.';list.innerHTML=fs.map(function(x,i){var p=x.properties||{},cl=p['eo:cloud_cover'];return '<div class="g360-v2-item"><b>'+esc(x.id||'Observation')+'</b><br>'+esc(p.datetime||'date inconnue')+(cl!=null?' · nuages '+Number(cl).toFixed(1)+'%':'')+'<br><button data-sat-index="'+i+'">Voir métadonnées</button></div>'}).join('')||'Aucun résultat.'}).catch(function(e){window.GABON360_SATELLITE_RESULTS={provider:'Copernicus CDSE',live:false,count:0,features:[]};res.textContent='Catalogue indisponible : '+e.message+' — aucune donnée simulée.'})}
card.querySelector('#g360-sat-search').onclick=doSearch;
card.querySelector('#g360-sat-selected').onclick=function(){var c=selected();if(!c){out('Aucun point carte sélectionné.');return}bbox=[c.lon-0.05,c.lat-0.05,c.lon+0.05,c.lat+0.05];out('Zone satellite centrée sur '+c.lat.toFixed(6)+', '+c.lon.toFixed(6));};
card.querySelector('#g360-sat-reset').onclick=function(){bbox=[8.5,-4,14.5,2.5];out('Zone remise à tout le Gabon.')};
card.querySelector('#g360-sat-list').onclick=function(e){var b=e.target.closest('[data-sat-index]');if(!b)return;var fs=(window.GABON360_SATELLITE_RESULTS||{}).features||[],x=fs[Number(b.dataset.satIndex)];card.querySelector('#g360-sat-result').textContent=x?JSON.stringify({id:x.id,properties:x.properties,assets:Object.keys(x.assets||{})},null,2):'Observation introuvable.'};
}
function navPage(){if(window.GABON360_OPEN_MODULE_PAGE)window.GABON360_OPEN_MODULE_PAGE('nav');try{var b=document.getElementById('g360-garmin-open');if(b)b.click()}catch(e){}}
function localCrudPage(type,title,actions){
var d=db();
shell(title,'<div class="g360-v2-actions">'+actions.map(function(a){return '<button data-crud="'+esc(a)+'">'+esc(a)+'</button>'}).join('')+'</div><div class="g360-v2-box g360-v2-result">Choisissez une action.</div><div class="g360-v2-box"><b>Données locales</b><div id="g360-crud-list" class="g360-v2-list"></div></div>');
function render(){var arr=d[type]||[],l=card.querySelector('#g360-crud-list');l.innerHTML=arr.slice(-50).reverse().map(function(x){return '<div class="g360-v2-item">'+esc(JSON.stringify(x))+'</div>'}).join('')||'Aucun enregistrement.'}
card.querySelectorAll('[data-crud]').forEach(function(b){b.onclick=function(){var a=b.dataset.crud;if(a==='Créer mission'||a==='Nouvelle mission'){var x={id:Date.now(),status:'planned',created_at:new Date().toISOString(),coordinates:selected()||null};d.missions=d.missions||[];d.missions.push(x);save(d);render();out('Mission créée localement. Les commandes drone réelles restent verrouillées sans passerelle autorisée.')}else if(a==='Ajouter site'){var x={id:Date.now(),status:'configured',created_at:new Date().toISOString()};d.sources=d.sources||[];d.sources.push(x);save(d);render();out('Site enregistré localement, sans faux flux.')}else if(a==='Créer observation'){var x={id:Date.now(),coordinates:selected()||null,created_at:new Date().toISOString(),state:'draft'};d.events=d.events||[];d.events.push(x);save(d);render();out('Observation créée en brouillon.')}else if(a==='Actualiser'){render();out('Données locales actualisées.')}else if(a==='Exporter'){var blob=new Blob([JSON.stringify(d,null,2)],{type:'application/json'}),z=document.createElement('a');z.href=URL.createObjectURL(blob);z.download='gabon360-'+type+'.json';z.click();out('Export lancé.')}else out(a+' : prêt, sans inventer de données.')}});render()
}
function weatherPage(){shell('🌦️ Météo opérationnelle','<div class="g360-v2-actions"><button id="g360-weather-gps">📍 Position GPS</button><button id="g360-weather-lib">🇬🇦 Libreville</button></div><div class="g360-v2-box g360-v2-result">Sélectionnez une zone.</div>');function load(lat,lon,label){fetch('https://api.open-meteo.com/v1/forecast?latitude='+lat+'&longitude='+lon+'&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code&forecast_days=3').then(function(r){return r.json()}).then(function(d){var c=d.current||{};out(label+'\nTempérature : '+(c.temperature_2m??'—')+' °C\nHumidité : '+(c.relative_humidity_2m??'—')+' %\nPluie : '+(c.precipitation??'—')+' mm\nVent : '+(c.wind_speed_10m??'—')+' km/h\nCode météo : '+(c.weather_code??'—'))}).catch(function(e){out('Météo indisponible : '+e.message)})}card.querySelector('#g360-weather-lib').onclick=function(){load(0.3901,9.4544,'Libreville')};card.querySelector('#g360-weather-gps').onclick=function(){navigator.geolocation.getCurrentPosition(function(p){load(p.coords.latitude,p.coords.longitude,'Position GPS')},function(e){out('GPS indisponible : '+e.message)},{enableHighAccuracy:true,timeout:15000})}}
function maritimePage(){shell('🌊 Maritime — météo marine publique','<div class="g360-v2-box">Les données marines publiques sont des prévisions de modèle et ne remplacent pas une navigation nautique certifiée.</div><div class="g360-v2-actions"><button id="g360-marine-lib">🌊 Côte / Libreville</button><button id="g360-marine-point">📍 Point sélectionné</button></div><div class="g360-v2-box g360-v2-result">Aucune donnée.</div>');function load(lat,lon){fetch('https://marine-api.open-meteo.com/v1/marine?latitude='+lat+'&longitude='+lon+'&current=wave_height,wave_direction,wave_period,sea_surface_temperature,ocean_current_velocity,ocean_current_direction').then(function(r){return r.json()}).then(function(d){var c=d.current||{};out('Point '+lat.toFixed(5)+', '+lon.toFixed(5)+'\nVagues : '+(c.wave_height??'—')+' m\nDirection : '+(c.wave_direction??'—')+'°\nPériode : '+(c.wave_period??'—')+' s\nTempérature mer : '+(c.sea_surface_temperature??'—')+' °C\nCourant : '+(c.ocean_current_velocity??'—')+' km/h · '+(c.ocean_current_direction??'—')+'°')}).catch(function(e){out('Météo marine indisponible : '+e.message)})}card.querySelector('#g360-marine-lib').onclick=function(){load(0.35,9.45)};card.querySelector('#g360-marine-point').onclick=function(){var c=selected();if(c)load(c.lat,c.lon);else out('Sélectionnez d’abord un point sur la carte.')}} 
function dispatchPage(id){if(id==='map')mapPage();else if(id==='nav')navPage();else if(id==='sat')satPage();else if(id==='drones')localCrudPage('missions','🚁 Drones — préparation de missions',['Nouvelle mission','Actualiser','Exporter']);else if(id==='cameras')localCrudPage('sources','📹 Caméras — registre local',['Ajouter site','Actualiser','Exporter']);else if(id==='maritime')maritimePage();else if(id==='forests')localCrudPage('events','🌳 Forêts & parcs — observations',['Créer observation','Actualiser','Exporter']);else if(id==='reports')localCrudPage('reports','📄 Rapports — gestion locale',['Nouveau rapport','Actualiser','Exporter']);else if(id==='weather')weatherPage();else if(id==='stats')localCrudPage('events','📊 Statistiques — données locales',['Actualiser','Exporter']);else if(id==='sources')localCrudPage('sources','📡 Sources — registre et diagnostic',['Ajouter site','Actualiser','Exporter']);else if(id==='alerts')localCrudPage('events','🚨 Alertes — registre local',['Créer observation','Actualiser','Exporter']);else if(id==='security')localCrudPage('sources','🛡️ Sécurité / audit — registre local',['Actualiser','Exporter']);else if(id==='avatar')speak('Bonjour Ngoua Obame. GABON 360 AI est prêt.');else if(window.GABON360_OPEN_MODULE_PAGE)window.GABON360_OPEN_MODULE_PAGE(id)}
document.getElementById('g360-v2-launch').onclick=function(){dispatchPage('map')};
window.GABON360_OPEN_ENHANCED_PAGE=dispatchPage;
window.GABON360_ENHANCED_PAGE_VERSION='2.0';
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
