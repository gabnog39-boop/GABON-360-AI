#!/usr/bin/env python3
"""Injecte la page dédiée Mémoire territoriale pilotée par son IA spécialisée."""

from pathlib import Path

MARK = "GABON360-MEMORY-AI-PAGE-V1"

PAYLOAD = r'''<!-- GABON360-MEMORY-AI-PAGE-V1 -->
<style>
#g360-memory-ai{display:none;position:fixed;inset:0;z-index:2147483600;background:#020913f7;color:#edf7ff;font:14px system-ui,sans-serif;overflow:auto}
#g360-memory-ai .g360-mem-page{min-height:100%;box-sizing:border-box;padding:12px 12px 42px}
#g360-memory-ai .g360-mem-head{position:sticky;top:0;z-index:4;display:flex;gap:7px;align-items:center;background:#071522f5;border-bottom:1px solid #31506d;padding:9px 0}
#g360-memory-ai .g360-mem-head b{flex:1;font-size:17px}
#g360-memory-ai button,#g360-memory-ai input,#g360-memory-ai select{background:#0c2032;color:#fff;border:1px solid #31506d;border-radius:8px;padding:8px}
#g360-memory-ai .g360-mem-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:10px}
#g360-memory-ai .g360-mem-card{background:#071522;border:1px solid #1e3b51;border-radius:11px;padding:10px}
#g360-memory-ai .g360-mem-card h3{margin:0 0 7px}
#g360-memory-ai .g360-mem-status{white-space:pre-wrap;min-height:54px}
#g360-memory-ai .g360-mem-record{margin-top:7px;padding:8px;border-radius:8px;background:#091b2a;border:1px solid #1d3c54}
#g360-memory-ai .g360-mem-green{border-left:4px solid #39d98a}
#g360-memory-ai .g360-mem-yellow{border-left:4px solid #f0c95b}
#g360-memory-ai .g360-mem-orange{border-left:4px solid #f39a4a}
@media(max-width:650px){#g360-memory-ai .g360-mem-grid{grid-template-columns:1fr}}
</style>
<div id="g360-memory-ai" aria-hidden="true">
 <div class="g360-mem-page">
  <div class="g360-mem-head">
   <button id="g360-memory-back">← Centre</button>
   <b>🧠 MÉMOIRE TERRITORIALE — IA SPÉCIALISÉE</b>
   <button id="g360-memory-close">✕</button>
  </div>
  <div class="g360-mem-card g360-mem-status" id="g360-memory-status">IA Mémoire territoriale initialisée.</div>
  <div class="g360-mem-grid">
   <div class="g360-mem-card">
    <h3>🔎 Rechercher l'historique</h3>
    <input id="g360-memory-query" placeholder="zone, province, parc, événement">
    <select id="g360-memory-domain"><option value="">Tous les domaines</option><option>forêts</option><option>eaux</option><option>maritime</option><option>risques</option><option>satellite</option><option>missions</option></select>
    <button id="g360-memory-search">Analyser</button>
   </div>
   <div class="g360-mem-card">
    <h3>🕒 Comparer deux périodes</h3>
    <input id="g360-memory-a" type="date"><input id="g360-memory-b" type="date">
    <button id="g360-memory-compare">Comparer</button>
   </div>
   <div class="g360-mem-card">
    <h3>📍 Zone sélectionnée</h3>
    <div id="g360-memory-zone">Aucune zone sélectionnée.</div>
    <button id="g360-memory-use-map">Utiliser la dernière coordonnée carte/GPS</button>
   </div>
   <div class="g360-mem-card">
    <h3>🔁 Récurrences</h3>
    <button id="g360-memory-recurrences">Rechercher les événements récurrents</button>
    <div id="g360-memory-results"></div>
   </div>
  </div>
  <div class="g360-mem-card" style="margin-top:9px">
   <h3>📚 Registre historique local</h3>
   <div id="g360-memory-records"></div>
  </div>
 </div>
</div>
<script>
(function(){
if(window.__G360_MEMORY_AI_PAGE_V1)return;
window.__G360_MEMORY_AI_PAGE_V1=true;
var root=document.getElementById('g360-memory-ai');
var status=document.getElementById('g360-memory-status');
var recordsBox=document.getElementById('g360-memory-records');
var results=document.getElementById('g360-memory-results');
var KEY='gabon360_territorial_memory_v1';
function db(){try{return JSON.parse(localStorage.getItem(KEY)||'[]')}catch(e){return[]}}
function save(a){localStorage.setItem(KEY,JSON.stringify(a))}
function speak(t){try{var f=window.G360AvatarSpeak||window.G360Speak||(window.G360&&window.G360.speak);if(typeof f==='function')f(t);else if(window.speechSynthesis){var u=new SpeechSynthesisUtterance(t);u.lang='fr-FR';window.speechSynthesis.speak(u)}}catch(e){}}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function open(){root.style.display='block';root.setAttribute('aria-hidden','false');render()}
function close(){root.style.display='none';root.setAttribute('aria-hidden','true')}
function render(){
var a=db();
recordsBox.innerHTML=a.length?a.slice().reverse().map(function(r){
 var cls=r.status==='RECORDED'?'g360-mem-green':(r.status==='AI_ANALYSIS'?'g360-mem-yellow':'g360-mem-orange');
 return '<div class="g360-mem-record '+cls+'"><b>'+esc(r.domain||'inconnu')+'</b> · '+esc(r.event_type||'observation')+'<br>'+esc(r.observation||'')+'<br><small>Source : '+esc(r.source||'—')+' · '+esc(r.timestamp||'—')+' · '+esc(r.status||'—')+'</small></div>'
}).join('')||'<div>Aucun historique enregistré. Aucune donnée fictive n’est ajoutée.</div>';
}
function publish(e,priority){
 try{if(window.GABON360_AI_RELAY)window.GABON360_AI_RELAY.publish('memory','historical-context',e)}catch(x){}
 window.dispatchEvent(new CustomEvent('gabon360:ai-event',{detail:e}));
 if(priority){speak('GABON 360 AI. '+e.observation+'. Source : '+e.source+'. Une validation humaine est requise.')}
}
function analyze(){
var q=(document.getElementById('g360-memory-query').value||'').toLowerCase();
var d=document.getElementById('g360-memory-domain').value;
var a=db().filter(function(r){return (!d||r.domain===d)&&(!q||JSON.stringify(r).toLowerCase().indexOf(q)>=0)});
status.textContent='Analyse IA : '+a.length+' enregistrement(s) correspondant(s).';
results.innerHTML=a.length?a.map(function(r){return '<div class="g360-mem-record"><b>'+esc(r.event_type)+'</b> — '+esc(r.observation)+'<br><small>'+esc(r.timestamp)+' · '+esc(r.source)+'</small></div>'}).join(''):'Aucun enregistrement correspondant. L’IA ne fabrique pas de résultat.';
publish({module:'memory',source:'Mémoire territoriale',timestamp:new Date().toISOString(),observation:'Analyse historique effectuée : '+a.length+' enregistrement(s) correspondant(s).',severity:'INFO',status:'AI_ANALYSIS',confidence:null,location:window.GABON360_SELECTED_COORDINATES||{},evidence:[],requires_human_validation:true},false);
}
function compare(){
var aa=document.getElementById('g360-memory-a').value,bb=document.getElementById('g360-memory-b').value;
var a=db(), dayA=aa?aa+'T00:00:00':'0000-01-01T00:00:00', dayB=bb?bb+'T23:59:59':'9999-12-31T23:59:59';
var before=a.filter(function(r){return r.timestamp>=dayA&&r.timestamp<=dayB});
status.textContent='Comparaison IA préparée sur '+before.length+' enregistrement(s). Pour une comparaison scientifique complète, chaque période doit disposer de sources datées comparables.';
publish({module:'memory',source:'Mémoire territoriale',timestamp:new Date().toISOString(),observation:'Comparaison historique préparée entre les dates sélectionnées.',severity:'INFO',status:'AI_ANALYSIS',confidence:null,location:window.GABON360_SELECTED_COORDINATES||{},evidence:before.map(function(r){return {id:r.id,source:r.source,timestamp:r.timestamp}}),requires_human_validation:true},false);
}
function recurrences(){
var a=db(),g={};
a.forEach(function(r){var l=r.location||{},k=(l.lat||'?')+':'+(l.lon||'?')+'|'+(r.event_type||'observation');g[k]=(g[k]||[]).concat(r)});
var found=Object.keys(g).filter(function(k){return g[k].length>=3});
results.innerHTML=found.length?found.map(function(k){var rows=g[k];return '<div class="g360-mem-record g360-mem-orange"><b>Anomalie probable</b><br>'+esc(k)+' · '+rows.length+' occurrences<br><small>Première : '+esc(rows[0].timestamp)+' · Dernière : '+esc(rows[rows.length-1].timestamp)+'</small></div>'}).join(''):'Aucune récurrence ≥ 3 trouvée dans les données enregistrées.';
if(found.length){var e={module:'memory',source:'IA Mémoire territoriale',timestamp:new Date().toISOString(),observation:'Récurrence historique détectée : '+found.length+' groupe(s) avec au moins trois occurrences.',severity:'HIGH',status:'ANOMALY_PROBABLE',confidence:null,location:window.GABON360_SELECTED_COORDINATES||{},evidence:[],requires_human_validation:true};publish(e,true)}
}
document.getElementById('g360-memory-search').onclick=analyze;
document.getElementById('g360-memory-compare').onclick=compare;
document.getElementById('g360-memory-recurrences').onclick=recurrences;
document.getElementById('g360-memory-use-map').onclick=function(){var c=window.GABON360_SELECTED_COORDINATES;if(c){document.getElementById('g360-memory-zone').textContent='Latitude '+c.lat+' · Longitude '+c.lon+' · précision '+(c.accuracy||'—')+' m'}else document.getElementById('g360-memory-zone').textContent='Aucune coordonnée disponible.'};
document.getElementById('g360-memory-close').onclick=close;
document.getElementById('g360-memory-back').onclick=function(){close();if(window.GABON360_OPEN_MODULE_PAGE)window.GABON360_OPEN_MODULE_PAGE('map')};
window.GABON360_OPEN_MEMORY_AI=open;
window.GABON360_MEMORY_AI={version:'1.0',open:open,analyze:analyze,compare:compare,recurrences:recurrences};
window.addEventListener('gabon360:memory-record',function(ev){var r=ev.detail||{};var a=db();a.push(r);save(a);render()});
window.addEventListener('gabon360:ai-relay',function(ev){var d=ev.detail||{};if(d.module==='memory'){render();status.textContent='IA Mémoire territoriale : événement reçu par le relais central.'}});
render();
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
        if i < 0:
            continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:], encoding='utf-8')
        print('injected:', p)
        return
    raise SystemExit('Aucun index.html exploitable')

if __name__=='__main__':
    main()
