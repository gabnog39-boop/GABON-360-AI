#!/usr/bin/env python3
from pathlib import Path

MARK = "GABON360-UNIVERSAL-MODULE-PAGES-V1"

PAYLOAD = r'''<!-- GABON360-UNIVERSAL-MODULE-PAGES-V1 -->
<style>
#g360-universal-launch{position:fixed;left:10px;top:70px;z-index:2147483000;background:#0b1a2a;color:#fff;border:1px solid #31506d;border-radius:11px;padding:9px 12px;font-weight:800}
/* Le catalogue principal est géré par la navigation nationale : ne pas afficher un second lanceur. */
#g360-universal-launch{display:none!important}
#g360-universal{position:fixed;inset:0;z-index:2147483500;display:none;background:#020913f5;color:#eef6ff;font:14px system-ui,sans-serif;overflow:auto}
#g360-universal .g360-upage{min-height:100%;box-sizing:border-box;padding:14px 12px 40px}
#g360-universal .g360-uhead{position:sticky;top:0;z-index:3;background:#081725ee;border-bottom:1px solid #31506d;padding:10px 0;display:flex;align-items:center;gap:8px}
#g360-universal .g360-uhead b{font-size:17px;flex:1}
#g360-universal button{background:#102337;color:#fff;border:1px solid #31506d;border-radius:9px;padding:9px 11px;margin:3px;touch-action:manipulation}
#g360-universal .g360-ugrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}
#g360-universal .g360-ucard{background:#071522;border:1px solid #193047;border-radius:12px;padding:11px}
#g360-universal .g360-ucard b{display:block;margin-bottom:5px}
#g360-universal .g360-status{background:#071522;border:1px solid #193047;border-radius:12px;padding:11px;margin-top:10px;white-space:pre-wrap;min-height:46px}
#g360-universal .g360-back{background:#18334d}
@media(max-width:650px){#g360-universal .g360-ugrid{grid-template-columns:1fr}}
</style>
<button id="g360-universal-launch">☰ Centre des fonctions</button>
<div id="g360-universal" aria-hidden="true"></div>
<script>
(function(){
if(window.__G360_UNIVERSAL_MODULE_PAGES_V1)return;
window.__G360_UNIVERSAL_MODULE_PAGES_V1=true;

var modules={
map:{icon:'🗺️',name:'Situation territoriale / SIG',actions:['Carte routière','Satellite','Parcs nationaux','Provinces / villes / villages','Routes / pistes','Rivières / hydrographie','Sélection par clic','Coordonnées','Historique / comparaison','Événements sur carte']},
nav:{icon:'🧭',name:'Navigation terrain',actions:['GPS/GNSS','Altitude','Précision','Boussole / cap','Waypoint','Enregistrer waypoint','Tracé','Enregistrer tracé','GOTO','Distance / cap','Guidage vocal','Mode hors-ligne']},
sat:{icon:'🛰️',name:'Surveillance satellite',actions:['Sentinel-2','Sentinel-1','Recherche zone','Recherche date','Nuages / qualité','Métadonnées','Historique','Comparaison','Détection de changement','Ouvrir observation','Source / catalogue']},
drones:{icon:'🚁',name:'Drones',actions:['État connexion','Batterie','Position','Altitude','Mission','Caméra','Flux réel','Planifier mission','Retour mission','Historique','Synchroniser']},
cameras:{icon:'📹',name:'Caméras',actions:['Sites','Connexion','Dernière transmission','Flux réel','Capture','Événement','Couverture','Historique','Qualité source']},
maritime:{icon:'🌊',name:'Surveillance maritime',actions:['Carte maritime','Côte','Ports','Zones protégées','Données navires autorisées','Position','Météo marine','Événements','Historique','Sources / qualité']},
forests:{icon:'🌳',name:'Forêts & parcs',actions:['13 parcs nationaux','Zones forestières','Patrouilles','Observations','Événements','Pressions / menaces','Historique','Statistiques','Carte des zones']},
alerts:{icon:'🚨',name:'Alertes & événements',actions:['Nouvelles alertes','Proposées','À vérifier','Validées','Clôturées','Gravité','Source','Heure','Localisation','Ouvrir sur carte','Historique','Journal de validation']},
reports:{icon:'📄',name:'Rapports',actions:['Nouveau rapport','Mission','Observation','Événement','Brouillon','Valider','Historique','Recherche','Exporter','Traçabilité']},
stats:{icon:'📊',name:'Statistiques',actions:['National','Province','Parc','Zone','Période','Évolution','Alertes','Missions','Observations','Sources','Actualiser']},
weather:{icon:'🌦️',name:'Météo',actions:['Situation actuelle','Prévisions','Zone','Température','Pluie','Vent','Humidité','Historique','Contexte opérationnel','Source / qualité']},
sources:{icon:'📡',name:'Sources & connexions',actions:['Satellites','Drones','Caméras','Maritime','Météo','SIG','Institutionnel','État','Qualité','Dernière réception','Tester','Synchroniser','Hors-ligne']},
security:{icon:'🛡️',name:'Accès / administration / audit',actions:['Utilisateurs','Rôles','Permissions','Lecture','Opération','Validation','Administration','Journal actions','Commandes IA','Configuration','Sécurité','Sessions']},
avatar:{icon:'🤖',name:'Avatar / IA centrale',actions:['Parler','Écouter','Micro','Voix','Stop voix','Conversation','Ouvrir une page','Expliquer la carte','Lire une alerte','Recevoir les sources','Historique commandes']},
memory:{icon:'🧠',name:'Mémoire territoriale — IA spécialisée',actions:['Historique territorial','Rechercher par zone','Rechercher par date','Comparer deux périodes','Évolution forêt / parc','Évolution eaux / littoral','Historique satellite','Historique alertes','Historique missions','Corrélations','Événements récurrents','Preuves / sources','Notifier l’avatar']}
};

var root=document.getElementById('g360-universal');
var launch=document.getElementById('g360-universal-launch');
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function status(t){var e=root.querySelector('.g360-status');if(e)e.textContent=t}
function show(){root.style.display='block';root.setAttribute('aria-hidden','false')}
function hide(){root.style.display='none';root.setAttribute('aria-hidden','true')}
function modulePage(id){
var m=modules[id];if(!m)return;
root.innerHTML='<div class="g360-upage"><div class="g360-uhead"><button class="g360-back">← Centre</button><b>'+m.icon+' '+esc(m.name)+'</b><button class="g360-close">✕</button></div><div class="g360-status">Page du module prête. Sélectionnez une fonction.</div><div class="g360-ugrid">'+m.actions.map(function(a,i){return '<div class="g360-ucard"><b>'+esc(a)+'</b><button data-g360-fn="'+id+'|'+i+'">Ouvrir la fonction</button></div>'}).join('')+'</div></div>';
show();
}
function center(){
root.innerHTML='<div class="g360-upage"><div class="g360-uhead"><b>GABON 360 AI — Centre des fonctions</b><button class="g360-close">✕</button></div><div class="g360-status">Chaque module possède sa propre page et ses fonctions.</div><div class="g360-ugrid">'+Object.keys(modules).map(function(id){var m=modules[id];return '<div class="g360-ucard"><b>'+m.icon+' '+esc(m.name)+'</b><span>'+m.actions.length+' fonctions</span><br><button data-g360-module="'+id+'">Ouvrir la page</button></div>'}).join('')+'</div></div>';
show();
}
function dispatch(id,action){
window.dispatchEvent(new CustomEvent('gabon360:page-action',{detail:{page:id,action:action}}));
}
function run(id,i){
var m=modules[id],a=m.actions[i]; if(!m||!a)return;
if(id==='avatar'){
if(a==='Parler'||a==='Voix'){if(window.G360AvatarSpeak)window.G360AvatarSpeak('Bonjour Ngoua Obame. GABON 360 AI est prêt.');else if(window.G360Android&&G360Android.speak)G360Android.speak('Bonjour Ngoua Obame. GABON 360 AI est prêt.');status('IA parle.');return}
if(a==='Écouter'||a==='Micro'){if(window.G360AvatarListen)window.G360AvatarListen();else if(window.G360Android&&G360Android.startListening)G360Android.startListening();status('Écoute en cours.');return}
if(a==='Stop voix'){if(window.G360AvatarStop)window.G360AvatarStop();else if(window.G360Android&&G360Android.stopSpeaking)G360Android.stopSpeaking();status('Voix arrêtée.');return}
}
if(id==='nav'&&(a==='GPS/GNSS'||a==='Altitude'||a==='Précision')){
if(navigator.geolocation){navigator.geolocation.getCurrentPosition(function(p){var c=p.coords;status('Position GPS reçue\nLatitude : '+c.latitude+'\nLongitude : '+c.longitude+'\nPrécision : '+(c.accuracy||'—')+' m\nAltitude : '+(c.altitude==null?'—':c.altitude)+' m');window.GABON360_SELECTED_COORDINATES={lat:c.latitude,lon:c.longitude,accuracy:c.accuracy,altitude:c.altitude,timestamp:Date.now()};dispatch(id,a)},function(e){status('GPS indisponible : '+e.message)},{enableHighAccuracy:true,timeout:15000,maximumAge:5000});}else status('GPS/GNSS indisponible sur cet appareil.');return;
}
if(id==='weather'){
if(a==='Situation actuelle'||a==='Prévisions'||a==='Température'||a==='Pluie'||a==='Vent'||a==='Humidité'){
fetch('https://api.open-meteo.com/v1/forecast?latitude=0.3901&longitude=9.4544&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&forecast_days=3').then(function(r){return r.json()}).then(function(d){var c=d.current||{};status('Météo publique — Libreville\nTempérature : '+(c.temperature_2m==null?'—':c.temperature_2m)+' °C\nHumidité : '+(c.relative_humidity_2m==null?'—':c.relative_humidity_2m)+' %\nPluie : '+(c.precipitation==null?'—':c.precipitation)+' mm\nVent : '+(c.wind_speed_10m==null?'—':c.wind_speed_10m)+' km/h');dispatch(id,a)}).catch(function(e){status('Météo indisponible : '+e.message)});return;
}}
if(id==='sat'&&(a==='Sentinel-2'||a==='Sentinel-1'||a==='Recherche zone'||a==='Recherche date'||a==='Nuages / qualité'||a==='Métadonnées'||a==='Source / catalogue')){
var r=window.GABON360_SATELLITE_RESULTS;var n=r?(Number(r.count)||((r.features||[]).length)):0;status(n?'Observations satellite disponibles : '+n+'\nUtilisez le panneau satellite pour actualiser.':'Aucune observation chargée. Lancez une recherche Copernicus.');dispatch(id,a);return;
}
if(id==='reports'&&a==='Nouveau rapport'){
var key='gabon360_operational_records_v1',db={reports:[],events:[],waypoints:[],tracks:[]};try{db=JSON.parse(localStorage.getItem(key)||JSON.stringify(db))}catch(e){}
var r={id:Date.now(),title:'Rapport GABON 360 AI',created_at:new Date().toISOString(),status:'draft',coordinates:window.GABON360_SELECTED_COORDINATES||null};db.reports.push(r);localStorage.setItem(key,JSON.stringify(db));status('Rapport créé en brouillon. ID : '+r.id);dispatch(id,a);return;
}
if(id==='reports'&&a==='Exporter'){
var key2='gabon360_operational_records_v1',raw=localStorage.getItem(key2)||'{}';var blob=new Blob([raw],{type:'application/json'}),link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='gabon360-donnees.json';link.click();status('Export local lancé.');return;
}
if(id==='memory'){
if(window.GABON360_OPEN_MEMORY_AI){window.GABON360_OPEN_MEMORY_AI();dispatch(id,a);return;}
status('IA Mémoire territoriale en cours de chargement.');dispatch(id,a);return;
}
if(id==='drones'||id==='cameras'||id==='maritime'){
status('Fonction prête, mais connexion réelle/autorisée requise. Aucune donnée fictive ne sera affichée.');dispatch(id,a);return;
}
status('Fonction « '+a+' » ouverte sur la page '+m.name+'. État : disponible selon la source connectée.');
dispatch(id,a);
}
launch.onclick=center;
root.addEventListener('click',function(e){
var b=e.target.closest('button');if(!b)return;
if(b.classList.contains('g360-close')){hide();return}
if(b.classList.contains('g360-back')){center();return}
if(b.dataset.g360Module){modulePage(b.dataset.g360Module);return}
if(b.dataset.g360Fn){var p=b.dataset.g360Fn.split('|');var id=p[0],i=Number(p[1]);var m=modules[id];if(m){run(id,i)}return}
});
window.GABON360_OPEN_MODULE_PAGE=modulePage;
window.GABON360_OPEN_FUNCTION_PAGE=function(id,i){modulePage(id);setTimeout(function(){var b=root.querySelector('[data-g360-fn="'+id+'|'+i+'"]');if(b)b.click()},0)};
window.GABON360_MODULE_PAGES=modules;
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'), key=lambda p: ('assets' not in p.parts, len(p.parts)))
    if not candidates:
        raise SystemExit('index.html introuvable')
    for p in candidates:
        t=p.read_text(encoding='utf-8', errors='ignore')
        if MARK in t:
            print('already:', p)
            return
        i=t.lower().rfind('</body>')
        if i<0:
            continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:], encoding='utf-8')
        print('installed:', p)
        return
    raise SystemExit('Aucun index.html exploitable')

if __name__=='__main__':
    main()
