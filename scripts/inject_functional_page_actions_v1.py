#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-FUNCTIONAL-PAGE-ACTIONS-V1 -->'
P=r'''<!-- GABON360-FUNCTIONAL-PAGE-ACTIONS-V1 -->
<script>
(function(){
if(window.GABON360_FUNCTIONAL_PAGE_ACTIONS)return;
const KEY='gabon360_operational_records_v1';
const load=()=>{try{return JSON.parse(localStorage.getItem(KEY)||'{"reports":[],"events":[],"waypoints":[],"tracks":[]}')}catch(e){return {reports:[],events:[],waypoints:[],tracks:[]}}};
const save=x=>localStorage.setItem(KEY,JSON.stringify(x));
const out=t=>{const e=document.getElementById('g360-cresult');if(e)e.textContent=String(t)};
const speak=t=>{try{if(window.G360Android&&G360Android.speak){G360Android.speak(t);return}}catch(e){}try{speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(t))}catch(e){}};
const coords=()=>window.GABON360_SELECTED_COORDINATES||null;
function action(page,name){const db=load(),n=String(name).toLowerCase();
if(page==='map'){if(n.includes('clic')||n.includes('coordonnées')){out('Touchez la carte pour sélectionner les coordonnées.');return}if(n.includes('historique')){out('Historique local : '+db.events.length+' événement(s).');return}if(window.GABON360_REAL_LEAFLET_MAP){window.GABON360_REAL_LEAFLET_MAP.invalidateSize();out('Carte SIG active : zoom, déplacement et sélection par clic disponibles.')}else out('Carte SIG indisponible.');return}
if(page==='nav'){if(n.includes('gps')||n.includes('position')||n.includes('altitude')||n.includes('précision')){if(!navigator.geolocation){out('GPS/GNSS indisponible.');return}navigator.geolocation.getCurrentPosition(p=>{const c=p.coords;window.GABON360_SELECTED_COORDINATES={lat:c.latitude,lon:c.longitude,accuracy:c.accuracy,altitude:c.altitude,timestamp:Date.now()};window.dispatchEvent(new CustomEvent('gabon360:terrain-position',{detail:window.GABON360_SELECTED_COORDINATES}));out('Position GPS reçue\nLat: '+c.latitude+'\nLon: '+c.longitude+'\nPrécision: '+(c.accuracy??'—')+' m\nAltitude: '+(c.altitude??'—')+' m');speak('Position GPS reçue.');},e=>out('GPS indisponible : '+e.message),{enableHighAccuracy:true,timeout:15000,maximumAge:5000});return}if(n.includes('waypoint')){const c=coords();if(!c){out('Sélectionnez d’abord un point.');return}const w={lat:c.lat,lon:c.lon,created_at:new Date().toISOString()};db.waypoints.push(w);save(db);window.dispatchEvent(new CustomEvent('gabon360:terrain-waypoint',{detail:w}));out('Waypoint enregistré : '+c.lat+', '+c.lon);return}if(n.includes('tracé')){const c=coords();if(!c){out('Position indisponible.');return}const t={id:Date.now(),points:[c],created_at:new Date().toISOString()};db.tracks.push(t);save(db);window.dispatchEvent(new CustomEvent('gabon360:terrain-track',{detail:t}));out('Tracé démarré avec la position courante.');return}if(n.includes('vocal')){speak('Guidage vocal activé.');out('Guidage vocal activé.');return}if(n.includes('hors-ligne')){out('Mode hors-ligne : données locales accessibles.');return}out('Navigation : sélectionnez GPS, waypoint, tracé, GOTO ou guidage.');return}
if(page==='sat'){const r=window.GABON360_SATELLITE_RESULTS||[];if(n.includes('métadonnées')||n.includes('qualité')){out(r.length?JSON.stringify(r.slice(0,3),null,2):'Aucune métadonnée chargée.');return}if(n.includes('historique')){out('Historique satellite local : '+db.events.filter(x=>x.type==='satellite').length);return}if(n.includes('changement')){out('Comparaison possible lorsque deux observations compatibles sont disponibles.');return}out(r.length?'Observations chargées : '+r.length:'Aucune observation chargée. Utilisez le panneau satellite pour lancer une recherche.');return}
if(page==='weather'){if(n.includes('actuelle')||n.includes('prévision')){fetch('https://api.open-meteo.com/v1/forecast?latitude=0.3901&longitude=9.4544&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&forecast_days=3').then(r=>r.json()).then(d=>{const c=d.current||{};out('Météo publique – Libreville\nTempérature: '+(c.temperature_2m??'—')+' °C\nHumidité: '+(c.relative_humidity_2m??'—')+' %\nPluie: '+(c.precipitation??'—')+' mm\nVent: '+(c.wind_speed_10m??'—')+' km/h\nSource: Open-Meteo (modèle public).');window.dispatchEvent(new CustomEvent('gabon360:weather-result',{detail:d}))}).catch(e=>out('Météo indisponible : '+e.message));return}out('Historique météo local : aucune série enregistrée.');return}
if(page==='reports'){if(n.includes('nouveau')){const r={id:Date.now(),title:'Rapport GABON 360 AI',created_at:new Date().toISOString(),status:'draft',coordinates:coords()};db.reports.push(r);save(db);window.dispatchEvent(new CustomEvent('gabon360:report-created',{detail:r}));out('Rapport créé en brouillon. ID '+r.id);return}if(n.includes('historique')||n.includes('recherche')){out('Rapports : '+db.reports.length+'\n'+db.reports.map(r=>r.id+' — '+r.title+' — '+r.status).join('\n'));return}if(n.includes('export')){const blob=new Blob([JSON.stringify(db.reports,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='gabon360-rapports.json';a.click();out('Export des rapports lancé.');return}out('Rapport : utilisez Nouveau rapport, Historique ou Exporter.');return}
if(page==='alerts'){out('Alertes : proposées '+db.events.filter(x=>x.state==='proposed').length+' | à vérifier '+db.events.filter(x=>x.state==='verify').length+' | validées '+db.events.filter(x=>x.state==='validated').length+' | clôturées '+db.events.filter(x=>x.state==='closed').length);return}
if(page==='stats'){out('Statistiques locales\nRapports: '+db.reports.length+'\nÉvénements: '+db.events.length+'\nWaypoints: '+db.waypoints.length+'\nTracés: '+db.tracks.length+'\nObservations satellite: '+((window.GABON360_SATELLITE_RESULTS||[]).length));return}
if(page==='sources'){out('Sources\nSIG: '+(window.GABON360_REAL_LEAFLET_MAP?'ACTIF':'EN ATTENTE')+'\nGPS: '+(navigator.geolocation?'DISPONIBLE':'INDISPONIBLE')+'\nSatellite: '+((window.GABON360_SATELLITE_RESULTS||[]).length?'DONNÉES CHARGÉES':'EN ATTENTE')+'\nMétéo publique: ACTIF\nDrones/Caméras/Maritime: connexion autorisée à configurer.');return}
if(page==='drones'||page==='cameras'||page==='maritime'){out('Module prêt, mais aucune connexion réelle/autorisée n’est configurée. Aucune donnée fictive ne sera affichée.');return}
if(page==='security'){out('Sécurité : interface locale active. Authentification serveur obligatoire avant usage opérationnel.');return}
if(page==='avatar'){if(n.includes('parler'))speak('Bonjour. GABON 360 AI est prêt.');else out('Avatar IA : voix, écoute et navigation centrale disponibles.');return}
if(page==='forests'){out('Forêts et parcs : consultation des données cartographiques disponibles. Aucune menace n’est inventée.');return}
out('Action reçue : '+name)}
window.addEventListener('gabon360:page-action',e=>{const d=e.detail||{};action(d.page,d.action)});
window.GABON360_FUNCTIONAL_PAGE_ACTIONS={version:'1.0',dispatch:action,storage:KEY};
})();
</script>'''
def main():
    for p in sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts))):
        t=p.read_text(encoding='utf-8')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i>=0:p.write_text(t[:i]+P+'\n'+t[i:],encoding='utf-8');print('injected:',p);return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
