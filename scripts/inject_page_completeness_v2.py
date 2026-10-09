#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-PAGE-COMPLETENESS-V2 -->'
P=r'''<!-- GABON360-PAGE-COMPLETENESS-V2 -->
<style>
#g360-complete-open{position:fixed;right:12px;top:70px;z-index:2147482500;background:#0b1a2a;color:#fff;border:1px solid #31506d;border-radius:10px;padding:9px 11px;font-weight:700}
#g360-complete-modal{position:fixed;inset:0;z-index:2147482600;display:none;background:#020913ee;padding:10px;overflow:auto;color:#eef6ff;font:13px system-ui,sans-serif}
#g360-complete-card{width:min(980px,98vw);margin:auto;background:#081725;border:1px solid #31506d;border-radius:16px;padding:12px;max-height:96vh;overflow:auto}
#g360-complete-head{position:sticky;top:0;background:#081725;z-index:2;display:flex;justify-content:space-between;gap:8px;padding-bottom:8px}
#g360-complete-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.g360-cpage{background:#071522;border:1px solid #193047;border-radius:11px;padding:10px}.g360-cpage b{display:block;font-size:15px;margin-bottom:4px}.g360-cpage small{opacity:.75}.g360-cbtns{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.g360-cbtns button,#g360-complete-close{background:#102337;color:#fff;border:1px solid #31506d;border-radius:8px;padding:7px 9px}.g360-cview{margin-top:10px;background:#071522;border:1px solid #193047;border-radius:11px;padding:11px}.g360-cok{color:#9ff2c2}.g360-cwait{color:#ffd28a}.g360-cinfo{color:#9fd8ff}
@media(max-width:650px){#g360-complete-grid{grid-template-columns:1fr}}
</style>
<button id="g360-complete-open">☰ Toutes les pages</button>
<div id="g360-complete-modal"><div id="g360-complete-card"><div id="g360-complete-head"><div><b>GABON 360 AI — Pages complètes</b><div style="opacity:.7">Chaque page possède son propre ensemble d'options. Les fonctions dépendant d'une source réelle restent explicitement en attente.</div></div><button id="g360-complete-close">✕</button></div><div id="g360-complete-grid"></div><div id="g360-complete-view"></div></div></div>
<script>
(function(){
const M={
 map:{i:'🗺️',n:'Situation territoriale / SIG',s:'ACTIF',o:['Carte routière','Satellite','Parcs nationaux','Provinces / villes / villages','Routes / pistes','Rivières / hydrographie','Sélection par clic','Coordonnées','Historique / comparaison','Événements sur carte']},
 nav:{i:'🧭',n:'Navigation terrain',s:'ACTIF',o:['GPS/GNSS','Altitude','Précision','Boussole / cap','Clic coordonnées','Waypoint','Enregistrer waypoint','Tracé','Enregistrer tracé','GOTO','Distance / cap','Guidage vocal','Mode hors-ligne']},
 sat:{i:'🛰️',n:'Surveillance satellite',s:'ACTIF',o:['Sentinel-2','Sentinel-1','Recherche zone','Recherche date','Nuages / qualité','Métadonnées','Historique','Comparaison','Détection de changement','Ouvrir observation','Source / catalogue']},
 drones:{i:'🚁',n:'Drones',s:'EN ATTENTE',o:['Drones autorisés','État connexion','Batterie','Position','Altitude','Mission','Caméra','Flux réel','Planifier mission','Retour mission','Historique','Synchroniser']},
 cameras:{i:'📹',n:'Caméras',s:'EN ATTENTE',o:['Sites','Caméras autorisées','Connexion','Dernière transmission','Flux réel','Capture','Événement','Couverture','Historique','Qualité source']},
 maritime:{i:'🌊',n:'Surveillance maritime',s:'EN ATTENTE',o:['Carte maritime','Côte','Ports','Zones protégées','Données navires autorisées','Position','Météo marine','Événements','Historique','Sources / qualité']},
 forests:{i:'🌳',n:'Forêts & parcs',s:'ACTIF',o:['13 parcs nationaux','Zones forestières','Patrouilles','Observations','Événements','Pressions / menaces','Historique','Statistiques','Carte des zones']},
 alerts:{i:'🚨',n:'Alertes & événements',s:'ACTIF',o:['Nouvelles alertes','Proposées','À vérifier','Validées','Clôturées','Gravité','Source','Heure','Localisation','Ouvrir sur carte','Historique','Journal de validation']},
 reports:{i:'📄',n:'Rapports',s:'ACTIF',o:['Nouveau rapport','Mission','Observation','Événement','Brouillon','Valider','Historique','Recherche','Exporter','Traçabilité']},
 stats:{i:'📊',n:'Statistiques',s:'ACTIF',o:['National','Province','Parc','Zone','Période','Évolution','Alertes','Missions','Observations','Sources','Actualiser']},
 weather:{i:'🌦️',n:'Météo',s:'ACTIF',o:['Situation actuelle','Prévisions','Zone','Température','Pluie','Vent','Humidité','Historique','Contexte opérationnel','Source / qualité']},
 sources:{i:'📡',n:'Sources & connexions',s:'ACTIF',o:['Satellites','Drones','Caméras','Maritime','Météo','SIG','Institutionnel','État','Qualité','Dernière réception','Tester','Synchroniser','Hors-ligne']},
 security:{i:'🛡️',n:'Accès / administration / audit',s:'ACTIF',o:['Utilisateurs','Rôles','Permissions','Lecture','Opération','Validation','Administration','Journal actions','Commandes IA','Configuration','Sécurité','Sessions']},
 avatar:{i:'🤖',n:'Avatar / IA centrale',s:'ACTIF',o:['Parler','Écouter','Micro','Voix','Stop voix','Conversation','Ouvrir une page','Expliquer la carte','Lire une alerte','Recevoir les sources','Historique commandes']}
};
const modal=document.getElementById('g360-complete-modal'),grid=document.getElementById('g360-complete-grid'),view=document.getElementById('g360-complete-view');
function render(){grid.innerHTML=Object.entries(M).map(([id,m])=>'<div class="g360-cpage"><b>'+m.i+' '+m.n+'</b><span class="'+(m.s==='ACTIF'?'g360-cok':'g360-cwait')+'">'+m.s+'</span><small><br>'+m.o.length+' fonctions prévues sur cette page</small><div class="g360-cbtns"><button data-page="'+id+'">Ouvrir la page</button><button data-list="'+id+'">Voir toutes les options</button></div></div>').join('')}
function openPage(id){const m=M[id];if(!m)return;view.innerHTML='<div class="g360-cview"><b>'+m.i+' '+m.n+'</b><p>'+m.o.map((x,i)=>'<button data-action="'+id+'|'+i+'" style="margin:3px">'+x+'</button>').join('')+'</p><div id="g360-cresult" class="g360-cview">Sélectionnez une fonction.</div></div>'}
function action(id,i){
 const m=M[id],x=m&&m.o[i];if(!m||!x)return;
 /* Route each option to the real module handler instead of only changing a label. */
 if(typeof window.GABON360_OPEN_NAMED_FUNCTION==='function'){
   modal.style.display='none';modal.setAttribute('aria-hidden','true');
   window.GABON360_OPEN_NAMED_FUNCTION(id,x);
   window.dispatchEvent(new CustomEvent('gabon360:page-action',{detail:{page:id,action:x}}));
   return;
 }
 if(typeof window.GABON360_OPEN_FUNCTION_PAGE==='function'){
   modal.style.display='none';modal.setAttribute('aria-hidden','true');
   window.GABON360_OPEN_FUNCTION_PAGE(id,i);
   window.dispatchEvent(new CustomEvent('gabon360:page-action',{detail:{page:id,action:x}}));
   return;
 }
 const result=document.getElementById('g360-cresult');
 if(result)result.textContent='Option « '+x+' » sélectionnée. Le module correspondant doit être chargé.';
 window.dispatchEvent(new CustomEvent('gabon360:page-action',{detail:{page:id,action:x}}));
}
document.getElementById('g360-complete-open').onclick=function(){modal.style.display='block';modal.setAttribute('aria-hidden','false');render()};
document.getElementById('g360-complete-close').onclick=function(){modal.style.display='none';modal.setAttribute('aria-hidden','true')};
grid.addEventListener('click',function(e){
 let b=e.target.closest('[data-page],[data-list]');if(!b)return;
 if(b.dataset.page){
   const id=b.dataset.page;
   if(typeof window.GABON360_OPEN_MODULE_PAGE==='function'){
     modal.style.display='none';modal.setAttribute('aria-hidden','true');
     window.GABON360_OPEN_MODULE_PAGE(id);
   }else openPage(id);
 }else openPage(b.dataset.list);
});
view.addEventListener('click',function(e){let b=e.target.closest('[data-action]');if(!b)return;let a=b.dataset.action.split('|');action(a[0],Number(a[1]))});
window.GABON360_PAGE_CATALOG=M;window.GABON360_PAGE_COMPLETENESS_V2={version:'2.0',pages:Object.keys(M),noDecorativeButtons:true};
})();
</script>
'''

def main():
    for p in sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts))):
        t=p.read_text(encoding='utf-8')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+P+'\n'+t[i:],encoding='utf-8'); print('injected:',p); return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
