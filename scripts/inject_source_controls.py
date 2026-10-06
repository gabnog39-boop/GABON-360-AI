#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARKER='<!-- GABON360-SOURCE-CONTROLS-V1 -->'
PAYLOAD=r'''<!-- GABON360-SOURCE-CONTROLS-V1 -->
<style>
#g360-source-controls{position:fixed;right:14px;bottom:14px;z-index:99997;background:#0b1a2a;color:#eef6ff;border:1px solid #31506d;border-radius:12px;padding:8px;font:12px system-ui,sans-serif;box-shadow:0 10px 30px #0008}
#g360-source-controls button{border:1px solid #29425a;background:#102337;color:#fff;border-radius:8px;padding:7px 9px;margin:2px;cursor:pointer}
#g360-source-modal{position:fixed;inset:0;background:#0009;z-index:100002;display:none;align-items:center;justify-content:center;padding:14px}
#g360-source-card{width:min(700px,96vw);max-height:88vh;overflow:auto;background:#0b1a2a;border:1px solid #31506d;border-radius:14px;padding:16px;color:#eef6ff}
.g360-source-item{padding:12px;margin:7px 0;border:1px solid #193047;border-radius:10px;background:#071522}.g360-source-item b{display:block;margin-bottom:4px}.g360-ready{color:#8df0b1}.g360-pending{color:#ffd48a}
</style>
<div id="g360-source-controls"><button id="g360-source-open">📡 Sources / connexions</button></div>
<div id="g360-source-modal"><div id="g360-source-card"><div style="display:flex;justify-content:space-between;gap:8px"><h2 id="g360-source-title">Sources opérationnelles</h2><button id="g360-source-close">Fermer</button></div><div id="g360-source-body"></div></div></div>
<script>
(function(){
 const m=document.getElementById('g360-source-modal'),b=document.getElementById('g360-source-body');
 const show=h=>{b.innerHTML=h;m.style.display='flex'};
 document.getElementById('g360-source-close').onclick=()=>m.style.display='none';
 m.onclick=e=>{if(e.target===m)m.style.display='none'};
 const source=(icon,name,status,detail)=>`<div class="g360-source-item"><b>${icon} ${name}</b><span class="${status==='ACTIVE'?'g360-ready':'g360-pending'}">${status}</span><br>${detail}<br><button data-source="${name}">⚙️ Ouvrir / tester</button></div>`;
 document.getElementById('g360-source-open').onclick=()=>show(
  source('🛰️','Copernicus Sentinel','ACTIVE','Catalogue public connecté : observations et métadonnées.')+
  source('📡','Sources institutionnelles','EN ATTENTE','Le bouton est actif. Il ouvre le contrôle de connexion, mais une autorisation et une passerelle officielle sont nécessaires avant de recevoir des données réelles.')+
  source('🚁','Drones autorisés','EN ATTENTE','Le bouton est actif. Aucun flux fictif : connexion réelle uniquement après configuration d’une passerelle autorisée.')+
  source('📹','Caméras autorisées','EN ATTENTE','Le bouton est actif. Flux réel uniquement après configuration et autorisation de la source.')+
  source('🌦️','Météo publique','ACTIVE','Accès public à la demande.')+
  source('🗺️','Cartographie SIG','ACTIVE','Carte publique accessible ; couches opérationnelles ajoutées par sources autorisées.')+
  source('📶','Synchronisation hors-ligne','ACTIVE','Contrôle local de l’état de synchronisation.')
 );
 b.onclick=e=>{const x=e.target.closest('button[data-source]');if(!x)return;const n=x.dataset.source;alert(n+' : commande reçue. État actuel : '+(n==='Copernicus Sentinel'||n==='Météo publique'||n==='Cartographie SIG'||n==='Synchronisation hors-ligne'?'source disponible':'connexion en attente d’une passerelle/autorisation officielle')+'. Aucune donnée fictive ne sera affichée.');};
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARKER in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8'); print('injected:',p); return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__': main()
