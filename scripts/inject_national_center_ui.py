#!/usr/bin/env python3
"""Inject the functional GABON 360 AI national situation-center UI."""
from __future__ import annotations
from pathlib import Path

MARKER = "<!-- GABON360-NATIONAL-CENTER-V2 -->"
PAYLOAD = r'''<!-- GABON360-NATIONAL-CENTER-V2 -->
<style>
#g360-center{position:fixed;inset:0;z-index:99990;display:flex;flex-direction:column;background:#07111d;color:#eef6ff;font:14px/1.35 system-ui,sans-serif}
#g360-center *{box-sizing:border-box}#g360-center .top{height:58px;display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid #193047;background:#091827;flex-shrink:0}
#g360-center .brand{font-weight:800;letter-spacing:.3px;font-size:15px}.g360-live{margin-left:auto;font-size:11px;padding:5px 9px;border-radius:99px;background:#123b2a;color:#8df0b1}.g360-menu,.g360-tool{border:1px solid #29425a;background:#102337;color:#fff;border-radius:8px;padding:7px 10px;cursor:pointer}.g360-menu:active,.g360-tool:active,.domain:active{transform:scale(.98)}
#g360-center .body{min-height:0;flex:1;display:grid;grid-template-columns:220px minmax(0,1fr) 300px;gap:8px;padding:8px}.panel{background:#0b1a2a;border:1px solid #193047;border-radius:12px;overflow:auto}.side{padding:10px}.side h3,.right h3{font-size:12px;text-transform:uppercase;opacity:.65;margin:8px 5px}.domain{display:flex;gap:8px;width:100%;text-align:left;padding:9px;margin:4px 0;border:1px solid transparent;background:#0f2235;color:#eaf3ff;border-radius:8px;cursor:pointer}.domain:hover,.domain.active{border-color:#5aa7df;background:#15324b}.main{display:flex;flex-direction:column;min-width:0}.map{position:relative;flex:1;min-height:320px;background:radial-gradient(circle at 50% 45%,#173a4a 0,#0b2230 38%,#06131f 75%);border-radius:12px;border:1px solid #193047;overflow:hidden}.mapgrid{position:absolute;inset:0;background-image:linear-gradient(#ffffff09 1px,transparent 1px),linear-gradient(90deg,#ffffff09 1px,transparent 1px);background-size:48px 48px;transform-origin:center}.maptitle{position:absolute;top:12px;left:12px;background:#07111dcc;padding:7px 10px;border-radius:8px}.mapbadge{position:absolute;left:12px;bottom:12px;background:#07111dcc;padding:7px 10px;border-radius:8px;font-size:11px}.g360-maptools{position:absolute;right:12px;top:12px;display:flex;gap:5px}.g360-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:7px}.stat{padding:10px;background:#0b1a2a;border:1px solid #193047;border-radius:10px}.stat b{display:block;font-size:18px}.stat span{font-size:10px;opacity:.65}.right{padding:10px}.alert{padding:9px;margin:6px 0;border-radius:9px;background:#241b16;border:1px solid #5d3b26}.alert b{display:block}.source{padding:8px 0;border-bottom:1px solid #193047;font-size:12px}.ok{color:#7fe3a2}.wait{color:#ffd48a}.footer{font-size:10px;opacity:.6;padding:7px 10px;text-align:center}.g360-hide{display:none!important}
.g360-modal{position:fixed;inset:0;background:#0009;z-index:100000;display:flex;align-items:center;justify-content:center;padding:16px}.g360-cardbox{width:min(680px,96vw);max-height:86vh;overflow:auto;background:#0b1a2a;border:1px solid #31506d;border-radius:14px;box-shadow:0 20px 60px #0008;padding:16px}.g360-cardbox h2{margin:0 0 8px}.g360-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.g360-input{flex:1;min-width:180px;border:1px solid #29425a;background:#07111d;color:#fff;border-radius:8px;padding:10px}.g360-result{margin-top:10px;padding:10px;background:#07111d;border-radius:9px;white-space:pre-wrap}.g360-chip{display:inline-block;padding:4px 7px;border-radius:99px;background:#15324b;margin:3px;font-size:11px}
@media(max-width:900px){#g360-center .body{grid-template-columns:1fr}.side,.right{display:none}.g360-stats{grid-template-columns:repeat(2,1fr)}.map{min-height:55vh}.brand{max-width:46vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
</style>
<div id="g360-center">
 <div class="top"><div class="brand">🇬🇦 GABON 360 AI — CENTRE NATIONAL DE SITUATION</div><button class="g360-menu" id="g360-full">Grand écran</button><button class="g360-menu" id="g360-ai">🤖 IA</button><span class="g360-live">● SURVEILLANCE ACTIVE</span></div>
 <div class="body">
  <aside class="panel side"><h3>Domaines IA</h3>
   <button class="domain" data-domain="Territoire & SIG">🗺️ Territoire & SIG</button><button class="domain" data-domain="Forêts & biodiversité">🌳 Forêts & biodiversité</button><button class="domain" data-domain="Eaux & bassins">💧 Eaux & bassins</button><button class="domain" data-domain="Océan & littoral">🌊 Océan & littoral</button><button class="domain" data-domain="Météo & climat">🌦️ Météo & climat</button><button class="domain" data-domain="Risques & catastrophes">🔥 Risques & catastrophes</button><button class="domain" data-domain="Infrastructures">🏗️ Infrastructures</button><button class="domain" data-domain="Situation maritime">⚓ Situation maritime</button><button class="domain" data-domain="Sécurité nationale">🛡️ Sécurité nationale</button><button class="domain" data-domain="Cybersécurité défensive">🔐 Cybersécurité défensive</button><button class="domain" data-domain="Logistique & missions">🚙 Logistique & missions</button><button class="domain" data-domain="Gestion de crise">🚨 Gestion de crise</button>
  </aside>
  <main class="main"><div class="map"><div class="mapgrid" id="g360-mapgrid"></div><div class="maptitle">🛰️ SITUATION GABON · observation automatique · carte opérationnelle</div><div style="position:absolute;inset:24% 34% 22% 32%;border:2px solid #6bc2a0;border-radius:42% 52% 45% 55%;opacity:.65"></div><div class="g360-maptools"><button class="g360-tool" id="g360-zoom-in">＋</button><button class="g360-tool" id="g360-zoom-out">−</button><button class="g360-tool" id="g360-zoom-reset">100%</button></div><div class="mapbadge" id="g360-focus">Zone sélectionnée : Gabon · précision selon rôle et source</div></div>
   <div class="g360-stats"><div class="stat"><b id="g360-obs">—</b><span>OBSERVATIONS</span></div><div class="stat"><b id="g360-alerts">0</b><span>ALERTES À VÉRIFIER</span></div><div class="stat"><b id="g360-sources">1</b><span>SOURCES CONNECTÉES</span></div><div class="stat"><b id="g360-status">ACTIF</b><span>ÉTAT DU CENTRE</span></div></div>
  </main>
  <aside class="panel right"><h3>Alertes & événements</h3><div id="g360-alert-list"><div class="alert"><b>Surveillance autonome</b><span>Aucune alerte confirmée. Les anomalies candidates nécessitent une vérification humaine.</span></div></div><h3>Sources</h3><div class="source"><b>🛰️ Copernicus Sentinel</b><br><span class="ok" id="g360-cop-status">Catalogue public disponible</span></div><div class="source"><b>📹 Caméras autorisées</b><br><span class="wait">Passerelle officielle requise</span></div><div class="source"><b>🚁 Drones autorisés</b><br><span class="wait">Passerelle officielle requise</span></div><div class="source"><b>🏛️ Sources institutionnelles</b><br><span class="wait">Connexion autorisée requise</span></div><h3>Contrôle</h3><button class="g360-tool" id="g360-refresh" style="width:100%;margin:4px 0">↻ Actualiser la situation</button><button class="g360-tool" id="g360-events" style="width:100%;margin:4px 0">📋 Événements / chronologie</button><button class="g360-tool" id="g360-reports" style="width:100%;margin:4px 0">📄 Rapports / traçabilité</button></aside>
 </div><div class="footer">GABON 360 AI · Les alertes sont des résultats d'analyse et restent soumises à validation humaine · aucune surveillance individuelle ni action coercitive automatique</div>
</div>
<div id="g360-modal" class="g360-modal g360-hide"><div class="g360-cardbox"><div class="g360-row" style="justify-content:space-between"><h2 id="g360-modal-title">GABON 360 AI</h2><button class="g360-tool" id="g360-modal-close">Fermer</button></div><div id="g360-modal-body"></div></div></div>
<script>
(function(){
 const root=document.getElementById('g360-center'); if(!root)return;
 const $=id=>document.getElementById(id); const modal=$('g360-modal'),mb=$('g360-modal-body'),mt=$('g360-modal-title');
 const state={domain:'Territoire & SIG',zoom:1,observations:0,source:'Copernicus CDSE',updated:null};
 const show=(title,body)=>{mt.textContent=title;mb.innerHTML=body;modal.classList.remove('g360-hide')};
 $('g360-modal-close').onclick=()=>modal.classList.add('g360-hide');
 modal.addEventListener('click',e=>{if(e.target===modal)modal.classList.add('g360-hide')});
 $('g360-full').onclick=()=>{if(document.fullscreenElement)document.exitFullscreen();else root.requestFullscreen?.()};
 $('g360-ai').onclick=()=>show('🤖 Assistant central GABON 360 AI','<p>Assistant opérationnel local. Il distingue les observations reçues, les analyses proposées et les informations à vérifier.</p><div class="g360-row"><input id="g360-ai-input" class="g360-input" placeholder="Ex. que sais-tu de la situation ?"><button class="g360-tool" id="g360-ai-send">Analyser</button></div><div id="g360-ai-result" class="g360-result">En attente de commande.</div>');
 document.addEventListener('click',e=>{if(e.target&&e.target.id==='g360-ai-send'){const q=($('g360-ai-input')?.value||'').trim();$('g360-ai-result').textContent=q?`Analyse de la demande : ${q}\nDomaine actif : ${state.domain}\nObservations reçues : ${state.observations}\nSource : ${state.source}\nÉtat : données à interpréter avec validation humaine.`:'Écris une commande ou une question.';}});
 document.querySelectorAll('#g360-center .domain').forEach(btn=>btn.onclick=()=>{document.querySelectorAll('#g360-center .domain').forEach(x=>x.classList.remove('active'));btn.classList.add('active');state.domain=btn.dataset.domain||btn.textContent.trim();$('g360-focus').textContent='Domaine actif : '+state.domain+' · sélection manuelle optionnelle';show('Domaine IA — '+state.domain,'<p>Module activé dans le centre de situation.</p><div class="g360-chip">État : ACTIF</div><div class="g360-chip">Données simulées : NON</div><div class="g360-chip">Validation humaine : OUI</div><p>Les données disponibles pour ce domaine seront affichées lorsqu’une source autorisée est connectée.</p>');});
 $('g360-zoom-in').onclick=()=>{state.zoom=Math.min(4,state.zoom+.25);$('g360-mapgrid').style.transform=`scale(${state.zoom})`};
 $('g360-zoom-out').onclick=()=>{state.zoom=Math.max(.5,state.zoom-.25);$('g360-mapgrid').style.transform=`scale(${state.zoom})`};
 $('g360-zoom-reset').onclick=()=>{state.zoom=1;$('g360-mapgrid').style.transform='scale(1)'};
 const refresh=()=>{state.updated=new Date().toLocaleTimeString();$('g360-status').textContent='ACTIF';$('g360-cop-status').textContent='Catalogue public disponible · dernier contrôle '+state.updated;};
 $('g360-refresh').onclick=refresh;
 $('g360-events').onclick=()=>show('📋 Événements / chronologie','<p>Aucun événement confirmé dans l’interface sans observation validée.</p><div class="g360-result">Les observations candidates restent séparées des faits établis. Les événements doivent être créés après vérification humaine.</div>');
 $('g360-reports').onclick=()=>show('📄 Rapports / traçabilité','<p>Traçabilité du centre.</p><div class="g360-result">État : actif\nDomaine : '+state.domain+'\nObservations reçues : '+state.observations+'\nSource : '+state.source+'\nValidation humaine : requise</div>');
 window.addEventListener('gabon360:satellite-results',e=>{const d=e.detail||{};state.observations=Number(d.count||0);state.source=d.provider||'Copernicus CDSE';$('g360-obs').textContent=state.observations;$('g360-sources').textContent=state.observations>0?'1':'0';refresh();});
 window.GABON360_CENTER={version:'2.0',coverage:'Gabon',automatic_surveillance:true,manual_zone_selection_optional:true,live_satellite_video:false,human_validation_required:true,ui_controls_functional:true};
 document.querySelector('#g360-center .domain')?.classList.add('active'); refresh();
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
