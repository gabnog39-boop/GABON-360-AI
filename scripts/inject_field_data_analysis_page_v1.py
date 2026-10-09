#!/usr/bin/env python3
"""Ajoute une page dédiée à l'analyse des données remontées du terrain."""
from pathlib import Path

MARK = "GABON360-FIELD-DATA-ANALYSIS-V1"
PAYLOAD = r'''<!-- GABON360-FIELD-DATA-ANALYSIS-V1 -->
<style>
#g360-field-analysis{display:none;position:fixed;inset:0;z-index:2147483605;background:#020913;color:#eef7ff;font:14px system-ui,sans-serif;overflow:auto}
#g360-field-analysis *{box-sizing:border-box}
#g360-field-analysis .g360-fa-wrap{max-width:1100px;margin:auto;padding:12px 12px 36px}
#g360-field-analysis .g360-fa-head{position:sticky;top:0;z-index:3;display:flex;align-items:center;gap:8px;background:#071522f5;border-bottom:1px solid #31506d;padding:9px 0}
#g360-field-analysis .g360-fa-head b{flex:1;font-size:17px}
#g360-field-analysis button,#g360-field-analysis input,#g360-field-analysis select{background:#10263a;color:#fff;border:1px solid #31506d;border-radius:9px;padding:9px;max-width:100%}
#g360-field-analysis button{font-weight:700;touch-action:manipulation}
#g360-field-analysis .g360-fa-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:10px}
#g360-field-analysis .g360-fa-card{min-width:0;background:#081827;border:1px solid #23435b;border-radius:12px;padding:11px}
#g360-field-analysis .g360-fa-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:10px}
#g360-field-analysis .g360-fa-kpi{background:#0b2031;border:1px solid #24465e;border-radius:10px;padding:9px}
#g360-field-analysis .g360-fa-kpi strong{display:block;font-size:22px}
#g360-field-analysis .g360-fa-muted{color:#a8bfd0;font-size:12px}
#g360-field-analysis .g360-fa-record{border-top:1px solid #23435b;padding:9px 0;overflow-wrap:anywhere}
#g360-field-analysis .g360-fa-status{white-space:pre-wrap;line-height:1.45}
#g360-field-analysis .g360-fa-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:8px}
@media(max-width:650px){#g360-field-analysis .g360-fa-grid{grid-template-columns:1fr}#g360-field-analysis .g360-fa-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}#g360-field-analysis .g360-fa-head b{font-size:14px}}
</style>
<div id="g360-field-analysis" aria-hidden="true">
 <div class="g360-fa-wrap">
  <div class="g360-fa-head"><button id="g360-fa-back">← Centre</button><b>📡 ANALYSE DES DONNÉES TERRAIN</b><button id="g360-fa-close">✕</button></div>
  <div class="g360-fa-card g360-fa-status" id="g360-fa-status">Analyse initialisée. Les résultats dépendront des observations réellement enregistrées ou des sources connectées.</div>
  <div class="g360-fa-kpis">
   <div class="g360-fa-kpi"><strong id="g360-fa-total">0</strong><span class="g360-fa-muted">Enregistrements trouvés</span></div>
   <div class="g360-fa-kpi"><strong id="g360-fa-geo">0</strong><span class="g360-fa-muted">Avec coordonnées</span></div>
   <div class="g360-fa-kpi"><strong id="g360-fa-sources">0</strong><span class="g360-fa-muted">Sources distinctes</span></div>
   <div class="g360-fa-kpi"><strong id="g360-fa-alerts">0</strong><span class="g360-fa-muted">Alertes à vérifier</span></div>
  </div>
  <div class="g360-fa-grid">
   <section class="g360-fa-card">
    <b>🔎 Filtrer les données terrain</b>
    <p><input id="g360-fa-query" placeholder="Zone, parc, observation, source"></p>
    <p><select id="g360-fa-domain"><option value="">Tous les domaines</option><option value="forest">Forêts / parcs</option><option value="water">Eaux / littoral</option><option value="wildlife">Faune</option><option value="patrol">Patrouilles / missions</option><option value="satellite">Satellite</option><option value="camera">Caméras / drones</option><option value="alert">Alertes / incidents</option></select></p>
    <p><label>Depuis <input id="g360-fa-from" type="date"></label> <label>Jusqu'au <input id="g360-fa-to" type="date"></label></p>
    <div class="g360-fa-actions"><button id="g360-fa-analyze">Analyser les enregistrements</button><button id="g360-fa-refresh">Actualiser</button></div>
   </section>
   <section class="g360-fa-card">
    <b>🧠 Résultat de l'analyse</b>
    <div id="g360-fa-summary" class="g360-fa-status" style="margin-top:8px">Aucune analyse effectuée.</div>
    <div class="g360-fa-actions"><button id="g360-fa-alert">Préparer une alerte</button><button id="g360-fa-report">Créer un rapport</button><button id="g360-fa-avatar">Transmettre à l'avatar</button></div>
   </section>
  </div>
  <section class="g360-fa-card" style="margin-top:10px"><b>📚 Données analysées et provenance</b><div class="g360-fa-muted">Les enregistrements sont lus depuis le stockage local de l'application. Les données non disponibles ne sont pas inventées.</div><div id="g360-fa-records" style="margin-top:8px">Aucun enregistrement chargé.</div></section>
 </div>
</div>
<script>
(function(){
if(window.__G360_FIELD_ANALYSIS_V1)return;window.__G360_FIELD_ANALYSIS_V1=true;
var root=document.getElementById('g360-field-analysis'),status=document.getElementById('g360-fa-status'),summary=document.getElementById('g360-fa-summary'),recordsBox=document.getElementById('g360-fa-records'),last=[];
var keys=['gabon360_operational_records_v1','gabon360_territorial_memory_v1','gabon360_patrol_records_v1','gabon360_reports_v1','gabon360_events_v1','gabon360_observations_v1'];
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function parse(v){try{return JSON.parse(v)}catch(e){return null}}
function asArray(v){if(Array.isArray(v))return v;if(v&&typeof v==='object'){var a=[];Object.keys(v).forEach(function(k){if(Array.isArray(v[k]))a=a.concat(v[k])});return a}return []}
function load(){
 var all=[],seen={};
 keys.forEach(function(k){var raw=null;try{raw=localStorage.getItem(k)}catch(e){}if(!raw)return;var data=parse(raw);asArray(data).forEach(function(r){if(!r||typeof r!=='object')return;var item=Object.assign({},r,{_store:k});var sig=JSON.stringify([item.timestamp||item.date||'',item.observation||item.description||item.event_type||item.type||'',item.source||'',item.lat||item.latitude||'']);if(!seen[sig]){seen[sig]=1;all.push(item)}})});
 return all;
}
function text(r){return [r.observation,r.message,r.description,r.event_type,r.type,r.domain,r.source,r.location&&JSON.stringify(r.location),r.zone,r.province,r.park].filter(Boolean).join(' ')}
function dateOf(r){var d=r.timestamp||r.date||r.created_at||r.datetime||'';var n=Date.parse(d);return isFinite(n)?n:null}
function coords(r){var l=r.location||{};var lat=r.lat!=null?r.lat:(r.latitude!=null?r.latitude:l.lat);var lon=r.lon!=null?r.lon:(r.lng!=null?r.lng:(r.longitude!=null?r.longitude:(l.lon!=null?l.lon:l.lng)));return lat!=null&&lon!=null&&isFinite(Number(lat))&&isFinite(Number(lon))}
function domainMatches(r,d){if(!d)return true;var t=text(r).toLowerCase();var map={forest:/foret|forêt|parc|arbre|deforestation|déforestation/,water:/eau|riviere|rivière|ocean|océan|littoral|mer/,wildlife:/faune|animal|espece|espèce|braconnage/,patrol:/patrouille|mission|ecogarde|écogarde/,satellite:/satellite|sentinel|copernicus/,camera:/camera|caméra|drone|video|vidéo/,alert:/alerte|incident|menace|anomalie/};return map[d]?map[d].test(t):true}
function filtered(){
 var q=(document.getElementById('g360-fa-query').value||'').toLowerCase().trim(),dom=document.getElementById('g360-fa-domain').value,from=document.getElementById('g360-fa-from').value,to=document.getElementById('g360-fa-to').value;
 return load().filter(function(r){var t=text(r).toLowerCase();if(q&&t.indexOf(q)<0)return false;if(!domainMatches(r,dom))return false;var d=dateOf(r);if(from&&(!d||d<Date.parse(from+'T00:00:00')))return false;if(to&&(!d||d>Date.parse(to+'T23:59:59')))return false;return true})
}
function open(){root.style.display='block';root.setAttribute('aria-hidden','false');refresh()}
function close(){root.style.display='none';root.setAttribute('aria-hidden','true')}
function speak(t){try{var f=window.G360AvatarSpeak||window.G360Speak||(window.G360&&window.G360.speak);if(typeof f==='function'){f(t);return}if(window.G360Android&&window.G360Android.speak){window.G360Android.speak(t);return}if(window.speechSynthesis){var u=new SpeechSynthesisUtterance(t);u.lang='fr-FR';window.speechSynthesis.speak(u)}}catch(e){}}
function refresh(){
 last=filtered();var geo=last.filter(coords).length,sources={};last.forEach(function(r){sources[r.source||r._store||'source inconnue']=1});
 var alerts=last.filter(function(r){return /alert|critical|high|anomal|menace|incident/i.test([r.severity,r.status,r.type,r.event_type].join(' '))}).length;
 document.getElementById('g360-fa-total').textContent=last.length;document.getElementById('g360-fa-geo').textContent=geo;document.getElementById('g360-fa-sources').textContent=Object.keys(sources).length;document.getElementById('g360-fa-alerts').textContent=alerts;
 recordsBox.innerHTML=last.length?last.slice().reverse().slice(0,100).map(function(r){var loc=r.location&&typeof r.location==='object'?JSON.stringify(r.location):'';return '<div class="g360-fa-record"><b>'+esc(r.event_type||r.type||r.domain||'Observation')+'</b> · '+esc(r.status||'statut non renseigné')+'<br>'+esc(r.observation||r.message||r.description||'Description absente')+'<br><small>'+esc(r.source||r._store)+' · '+esc(r.timestamp||r.date||r.created_at||'date non renseignée')+' · '+esc(loc||((coords(r))?((r.lat||r.latitude)+', '+(r.lon||r.lng||r.longitude)):'coordonnées absentes'))+'</small></div>'}).join(''):'Aucun enregistrement correspondant trouvé dans les registres locaux. Cela ne prouve pas qu'aucune activité terrain n'existe : les données peuvent ne pas avoir été synchronisées vers ce téléphone.';
 status.textContent='Registres locaux consultés : '+keys.length+'. Enregistrements disponibles : '+last.length+'. Sources externes : non supposées connectées.';
}
function analyze(){refresh();var n=last.length,g=last.filter(coords).length,alerts=last.filter(function(r){return /alert|critical|high|anomal|menace|incident/i.test([r.severity,r.status,r.type,r.event_type].join(' '))}).length;
 var textResult=n?'Analyse descriptive de '+n+' enregistrement(s).\n• '+g+' enregistrement(s) avec coordonnées.\n• '+alerts+' élément(s) signalé(s) comme alerte/incident à vérifier.\n• Les sources et dates sont affichées dans la liste.\n\nLimite : ce résumé ne confirme pas une anomalie environnementale. Vérifier les preuves, la qualité de la source et la validation humaine.':'Aucune donnée correspondant aux filtres n’est enregistrée localement. Synchroniser les fiches terrain ou connecter une source autorisée avant toute conclusion.';
 summary.textContent=textResult;status.textContent='Analyse terminée à '+new Date().toLocaleString('fr-FR')+'. Résultat calculé uniquement à partir des enregistrements disponibles.';
 return {module:'field-analysis',source:'Analyse locale des données terrain',timestamp:new Date().toISOString(),observation:textResult,severity:alerts?'HIGH':'INFO',status:'ANALYSIS_SUMMARY',evidence:last.slice(0,50),requires_human_validation:true};
}
function publish(type){var e=analyze();e.type=type;try{window.dispatchEvent(new CustomEvent('gabon360:ai-event',{detail:e}));window.dispatchEvent(new CustomEvent('gabon360:page-action',{detail:{page:'field-analysis',action:type}}))}catch(_){}if(type==='avatar'){speak(e.observation);return}try{var d=parse(localStorage.getItem('gabon360_operational_records_v1'))||{};var k=type==='report'?'reports':'events';if(!Array.isArray(d[k]))d[k]=[];d[k].push(e);localStorage.setItem('gabon360_operational_records_v1',JSON.stringify(d));status.textContent=(type==='report'?'Brouillon de rapport enregistré localement.':'Événement préparatoire enregistré localement.')+' '+status.textContent}catch(_){status.textContent='Analyse prête, mais impossible d’enregistrer dans le stockage local.'}}
document.getElementById('g360-fa-back').onclick=close;document.getElementById('g360-fa-close').onclick=close;document.getElementById('g360-fa-analyze').onclick=analyze;document.getElementById('g360-fa-refresh').onclick=refresh;document.getElementById('g360-fa-alert').onclick=function(){publish('alert')};document.getElementById('g360-fa-report').onclick=function(){publish('report')};document.getElementById('g360-fa-avatar').onclick=function(){publish('avatar')};
window.GABON360_OPEN_DATA_ANALYSIS=open;window.GABON360_FIELD_ANALYSIS={open:open,close:close,refresh:refresh,analyze:analyze};
window.addEventListener('gabon360:field-data-updated',refresh);
})();
</script>
'''

def main():
    candidates = sorted(Path("android_project").rglob("index.html"), key=lambda p: ("assets" in p.parts, len(p.parts)))
    if not candidates:
        raise SystemExit("index.html introuvable")
    for p in candidates:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if MARK in t:
            print("already:", p)
            return
        i = t.lower().rfind("</body>")
        if i < 0:
            continue
        p.write_text(t[:i] + PAYLOAD + "\\n" + t[i:], encoding="utf-8")
        print("injected:", p)
        return
    raise SystemExit("Aucun index.html exploitable")

if __name__ == "__main__":
    main()
