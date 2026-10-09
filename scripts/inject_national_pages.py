#!/usr/bin/env python3
"""Add manual national-center pages and AI page navigation to the unified GABON 360 AI UI.

This layer is intentionally honest: unavailable integrations are shown as waiting/offline;
no drone, camera, vessel, satellite or security event is fabricated.
"""
from __future__ import annotations
from pathlib import Path

MARKER = "<!-- GABON360-NATIONAL-PAGES-V1 -->"
PAYLOAD = r'''<!-- GABON360-NATIONAL-PAGES-V1 -->
<style>
#g360-pages{position:fixed;right:12px;bottom:12px;z-index:99997;display:flex;gap:5px;flex-wrap:wrap;max-width:48vw;justify-content:flex-end;font:12px system-ui,sans-serif}
/* Le catalogue principal remplace ces raccourcis pour éviter les menus concurrents. */
#g360-pages{display:none!important}
#g360-pages button{background:#102337;color:#fff;border:1px solid #31506d;border-radius:8px;padding:7px 9px;cursor:pointer}
#g360-pages button:hover{background:#183650}
#g360-pages-modal{position:fixed;inset:0;background:#000b;z-index:100005;display:none;align-items:center;justify-content:center;padding:12px;font:14px system-ui,sans-serif;color:#eef6ff}
#g360-pages-card{width:min(920px,97vw);max-height:91vh;overflow:auto;background:#081725;border:1px solid #31506d;border-radius:15px;padding:16px;box-shadow:0 20px 60px #000b}
#g360-pages-head{display:flex;gap:10px;align-items:center;justify-content:space-between;position:sticky;top:0;background:#081725;padding-bottom:9px;z-index:2}
#g360-pages-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}
.g360-page-card{background:#0b1d2d;border:1px solid #193a52;border-radius:11px;padding:12px;min-height:95px}
.g360-page-card b{display:block;font-size:15px;margin-bottom:5px}.g360-page-card small{opacity:.72}.g360-page-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}.g360-page-actions button{background:#112b40;color:#fff;border:1px solid #31506d;border-radius:7px;padding:6px 8px}
.g360-status-ok{color:#8df0b1}.g360-status-wait{color:#ffd48a}.g360-status-info{color:#9fd8ff}
#g360-page-view{margin-top:12px}.g360-view{background:#071522;border:1px solid #193a52;border-radius:11px;padding:13px}.g360-kv{display:grid;grid-template-columns:150px 1fr;gap:5px;margin:4px 0}.g360-input{width:100%;box-sizing:border-box;padding:9px;border-radius:8px;border:1px solid #31506d;background:#06101a;color:#fff}.g360-select{padding:9px;border-radius:8px;border:1px solid #31506d;background:#06101a;color:#fff}.g360-ai-row{display:flex;gap:7px;margin-top:10px}.g360-ai-row .g360-input{flex:1}
@media(max-width:680px){#g360-pages{max-width:75vw}#g360-pages-grid{grid-template-columns:1fr}.g360-kv{grid-template-columns:1fr}}
</style>
<div id="g360-pages">
 <button id="g360-pages-open">🏛️ Centre national</button>
 <button data-g360-page="map">🗺️ Carte</button>
 <button data-g360-page="nav">🧭 Navigation</button>
 <button data-g360-page="sat">🛰️ Satellites</button>
 <button data-g360-page="drones">🚁 Drones</button>
 <button data-g360-page="cameras">📹 Caméras</button>
 <button data-g360-page="maritime">🌊 Maritime</button>
 <button data-g360-page="security">🛡️ Sécurité</button>
</div>
<div id="g360-pages-modal"><div id="g360-pages-card">
 <div id="g360-pages-head"><div><b id="g360-pages-title">GABON 360 AI — Centre national de situation</b><div id="g360-pages-sub" style="opacity:.7;font-size:12px">Navigation manuelle · assistance IA sur demande</div></div><button id="g360-pages-close">Fermer</button></div>
 <div id="g360-pages-grid"></div>
 <div id="g360-page-view"></div>
</div></div>
<script>
(function(){
 const modal=document.getElementById('g360-pages-modal'), grid=document.getElementById('g360-pages-grid'), view=document.getElementById('g360-page-view');
 const title=document.getElementById('g360-pages-title'), sub=document.getElementById('g360-pages-sub');
 const modules={
  map:{icon:'🗺️',name:'Situation territoriale / Carte SIG',status:'ok',desc:'Carte, zones, parcs, villes, routes, cours d’eau et couches autorisées.',opts:['Ouvrir la carte','Choisir une zone','Historique / comparaison']},
  nav:{icon:'🧭',name:'Navigation terrain',status:'ok',desc:'Position GNSS, guidage, points de passage et contexte terrain selon les données disponibles.',opts:['Ma position','Guidage vocal','Points de passage']},
  sat:{icon:'🛰️',name:'Surveillance satellite',status:'ok',desc:'Recherche d’observations publiques et comparaison temporelle; pas de vidéo satellite continue.',opts:['Rechercher une observation','Historique','Métadonnées / qualité']},
  drones:{icon:'🚁',name:'Drones',status:'wait',desc:'Module préparé pour les drones autorisés; connexion opérationnelle à configurer plus tard.',opts:['État des drones','Missions','Historique']},
  cameras:{icon:'📹',name:'Surveillance caméra',status:'wait',desc:'Sites et caméras autorisés; aucun flux fictif si la passerelle n’est pas connectée.',opts:['Sites','État des connexions','Historique des événements']},
  maritime:{icon:'🌊',name:'Surveillance maritime',status:'wait',desc:'Côte, ports, zones maritimes et données nautiques provenant de sources autorisées.',opts:['Situation maritime','Sources / qualité','Historique']},
  alerts:{icon:'🚨',name:'Alertes & événements',status:'info',desc:'Événements proposés, à vérifier, validés ou clôturés avec source et horodatage.',opts:['Nouvelles alertes','À vérifier','Historique']},
  reports:{icon:'📄',name:'Rapports',status:'ok',desc:'Rapports, missions, observations et traçabilité.',opts:['Nouveau rapport','Historique','Exporter']},
  stats:{icon:'📊',name:'Statistiques',status:'ok',desc:'Indicateurs par zone et période à partir des données disponibles.',opts:['National','Province / zone','Évolution']},
  weather:{icon:'🌦️',name:'Météo',status:'ok',desc:'Données publiques disponibles; distinguer modèle et observation locale.',opts:['Situation actuelle','Prévisions','Historique']},
  sources:{icon:'📡',name:'Sources & connexions',status:'ok',desc:'État des sources, qualité, dernière réception et mode hors-ligne.',opts:['État des sources','Tester une source','Synchronisation']},
  security:{icon:'🛡️',name:'Sécurité & audit',status:'ok',desc:'Gestion des rôles, permissions et journal des actions de l’interface.',opts:['Utilisateurs / rôles','Permissions','Journal d’audit']}
 };
 const labels={ok:'ACTIF',wait:'EN ATTENTE',info:'OPÉRATIONNEL'};
 function open(){modal.style.display='flex';renderGrid()}
 function close(){modal.style.display='none'}
 function renderGrid(){grid.innerHTML=Object.entries(modules).map(([id,m])=>`<div class="g360-page-card"><b>${m.icon} ${m.name}</b><span class="g360-status-${m.status}">${labels[m.status]}</span><br><small>${m.desc}</small><div class="g360-page-actions">${m.opts.map((o,i)=>`<button data-opt="${id}:${i}">${o}</button>`).join('')}</div></div>`).join('');view.innerHTML='<div class="g360-view"><b>Navigation</b><br><small>Choisissez une page et une fonction. L’IA peut aussi ouvrir ces pages sur commande.</small></div>'}
 function showPage(id,opt){const m=modules[id];if(!m)return;title.textContent=m.icon+' '+m.name;sub.textContent='Page indépendante · commandes manuelles disponibles';let extra='';
  if(id==='drones'||id==='cameras'||id==='maritime')extra='<div class="g360-page-card"><span class="g360-status-wait">Connexion réelle requise</span><br>Aucune donnée, position, image ou événement n’est inventé. Cette page est prête à recevoir une source autorisée.</div>';
  if(id==='security')extra='<div class="g360-view"><b>Rôles</b><select class="g360-select" id="g360-role"><option>Observateur</option><option>Opérateur</option><option>Validateur</option><option>Administrateur</option></select><p id="g360-perm">Accès de démonstration local — à remplacer par une authentification serveur avant usage opérationnel.</p></div>';
  if(id==='alerts')extra='<div class="g360-view"><b>État des événements</b><div class="g360-kv"><span>Proposé</span><span>—</span></div><div class="g360-kv"><span>À vérifier</span><span>—</span></div><div class="g360-kv"><span>Validé</span><span>—</span></div><small>Aucune alerte n’est créée sans source ou action humaine.</small></div>';
  view.innerHTML=`<div class="g360-view"><h3 style="margin-top:0">${m.icon} ${m.name}</h3><p>${m.desc}</p><p><b>Fonction :</b> ${opt||'Vue générale'}</p><div class="g360-page-actions">${m.opts.map((o,i)=>`<button data-openopt="${id}:${i}">${o}</button>`).join('')}</div>${extra}</div>`;
 }
 function navigate(id){open();showPage(id,'Vue générale')}
 document.getElementById('g360-pages-open').onclick=open;document.getElementById('g360-pages-close').onclick=close;modal.addEventListener('click',e=>{if(e.target===modal)close()});
 document.querySelectorAll('[data-g360-page]').forEach(b=>b.onclick=()=>navigate(b.dataset.g360Page));
 grid.addEventListener('click',e=>{const b=e.target.closest('[data-opt]');if(!b)return;const [id,i]=b.dataset.opt.split(':');showPage(id,modules[id].opts[Number(i)])});
 view.addEventListener('click',e=>{const b=e.target.closest('[data-openopt]');if(!b)return;const [id,i]=b.dataset.openopt.split(':');showPage(id,modules[id].opts[Number(i)])});
 window.GABON360_NAVIGATE=navigate;
 window.GABON360_NATIONAL_MODULES=modules;
 // AI command bridge: other assistant code can call this function; this layer also provides a simple command box.
 window.GABON360_HANDLE_COMMAND=function(raw){const q=String(raw||'').toLowerCase();const aliases={map:['carte','territoire','sig'],nav:['navigation','terrain','position','guidage'],sat:['satellite','sentinel','observation satellite'],drones:['drone','drones'],cameras:['caméra','camera','caméras','cameras'],maritime:['maritime','mer','océan','ocean','port','navire'],alerts:['alerte','alertes','événement','evenement'],reports:['rapport','rapports'],stats:['statistique','statistiques'],weather:['météo','meteo','climat'],sources:['source','connexion','connexions'],security:['sécurité','securite','audit','utilisateur','permission']};for(const [id,words] of Object.entries(aliases)){if(words.some(w=>q.includes(w))){navigate(id);return {ok:true,page:id}}}if(q.includes('accueil')||q.includes('centre')){open();return {ok:true,page:'centre'}}return {ok:false,reason:'Page non reconnue'} };
 // Expose a small command box from the centre panel without taking control away from manual navigation.
 const command=document.createElement('div');command.style.cssText='position:fixed;left:12px;bottom:58px;z-index:99998;background:#081725;border:1px solid #31506d;border-radius:10px;padding:6px;display:flex;gap:5px;max-width:70vw';command.innerHTML='<input id="g360-ai-command" class="g360-input" placeholder="Commande IA : « ouvre la surveillance maritime »"><button id="g360-ai-go">IA</button>';document.body.appendChild(command);
 document.getElementById('g360-ai-go').onclick=()=>{const r=window.GABON360_HANDLE_COMMAND(document.getElementById('g360-ai-command').value);if(!r.ok)alert('Commande non reconnue. Exemple : « ouvre la page drones »');};
 document.getElementById('g360-ai-command').addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('g360-ai-go').click()});
})();
'''

def main()->None:
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        text=p.read_text(encoding='utf-8')
        if MARKER in text:
            print('already:',p); return
        i=text.lower().rfind('</body>')
        if i>=0:
            p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
            print('injected:',p); return
    raise SystemExit('No suitable index.html found')

if __name__=='__main__': main()
