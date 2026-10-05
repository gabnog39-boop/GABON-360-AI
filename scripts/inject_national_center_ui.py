#!/usr/bin/env python3
"""Inject the GABON 360 AI national situation-center shell into the Android UI."""
from __future__ import annotations
from pathlib import Path

MARKER = "<!-- GABON360-NATIONAL-CENTER-V1 -->"
PAYLOAD = r'''<!-- GABON360-NATIONAL-CENTER-V1 -->
<style>
#g360-center{position:fixed;inset:0;z-index:99990;display:flex;flex-direction:column;background:#07111d;color:#eef6ff;font:14px/1.35 system-ui,sans-serif}
#g360-center *{box-sizing:border-box}#g360-center .top{height:58px;display:flex;align-items:center;gap:12px;padding:8px 14px;border-bottom:1px solid #193047;background:#091827}
#g360-center .brand{font-weight:800;letter-spacing:.4px;font-size:16px}.g360-live{margin-left:auto;font-size:11px;padding:5px 9px;border-radius:99px;background:#123b2a;color:#8df0b1}.g360-menu{border:1px solid #29425a;background:#102337;color:#fff;border-radius:8px;padding:7px 10px}
#g360-center .body{min-height:0;flex:1;display:grid;grid-template-columns:220px minmax(0,1fr) 300px;gap:8px;padding:8px}.panel{background:#0b1a2a;border:1px solid #193047;border-radius:12px;overflow:auto}.side{padding:10px}.side h3,.right h3{font-size:12px;text-transform:uppercase;opacity:.65;margin:8px 5px}.domain{display:flex;gap:8px;width:100%;text-align:left;padding:9px;margin:4px 0;border:1px solid transparent;background:#0f2235;color:#eaf3ff;border-radius:8px}.domain:hover{border-color:#31506d}.main{display:flex;flex-direction:column;min-width:0}.map{position:relative;flex:1;min-height:320px;background:radial-gradient(circle at 50% 45%,#173a4a 0,#0b2230 38%,#06131f 75%);border-radius:12px;border:1px solid #193047;overflow:hidden}.mapgrid{position:absolute;inset:0;background-image:linear-gradient(#ffffff09 1px,transparent 1px),linear-gradient(90deg,#ffffff09 1px,transparent 1px);background-size:48px 48px}.maptitle{position:absolute;top:12px;left:12px;background:#07111dcc;padding:7px 10px;border-radius:8px}.g360-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:7px}.stat{padding:10px;background:#0b1a2a;border:1px solid #193047;border-radius:10px}.stat b{display:block;font-size:18px}.stat span{font-size:10px;opacity:.65}.right{padding:10px}.alert{padding:9px;margin:6px 0;border-radius:9px;background:#241b16;border:1px solid #5d3b26}.alert b{display:block}.source{padding:8px 0;border-bottom:1px solid #193047;font-size:12px}.ok{color:#7fe3a2}.wait{color:#ffd48a}.footer{font-size:10px;opacity:.6;padding:7px 10px;text-align:center}.g360-hide{display:none!important}
@media(max-width:900px){#g360-center .body{grid-template-columns:1fr}.side,.right{display:none}.g360-stats{grid-template-columns:repeat(2,1fr)}.map{min-height:55vh}}
</style>
<div id="g360-center">
 <div class="top"><div class="brand">🇬🇦 GABON 360 AI — CENTRE NATIONAL DE SITUATION</div><button class="g360-menu" id="g360-full">Grand écran</button><span class="g360-live">● SURVEILLANCE ACTIVE</span></div>
 <div class="body">
  <aside class="panel side"><h3>Domaines IA</h3>
   <button class="domain">🗺️ Territoire & SIG</button><button class="domain">🌳 Forêts & biodiversité</button><button class="domain">💧 Eaux & bassins</button><button class="domain">🌊 Océan & littoral</button><button class="domain">🌦️ Météo & climat</button><button class="domain">🔥 Risques & catastrophes</button><button class="domain">🏗️ Infrastructures</button><button class="domain">⚓ Situation maritime</button><button class="domain">🛡️ Sécurité nationale</button><button class="domain">🔐 Cybersécurité défensive</button><button class="domain">🚙 Logistique & missions</button><button class="domain">🚨 Gestion de crise</button></aside>
  <main class="main"><div class="map"><div class="mapgrid"></div><div class="maptitle">🛰️ SITUATION GABON · observation automatique · carte opérationnelle</div><div style="position:absolute;inset:24% 34% 22% 32%;border:2px solid #6bc2a0;border-radius:42% 52% 45% 55%;opacity:.65"></div></div>
   <div class="g360-stats"><div class="stat"><b id="g360-obs">—</b><span>OBSERVATIONS</span></div><div class="stat"><b id="g360-alerts">0</b><span>ALERTES À VÉRIFIER</span></div><div class="stat"><b id="g360-sources">1</b><span>SOURCES CONNECTÉES</span></div><div class="stat"><b id="g360-status">ACTIF</b><span>ÉTAT DU CENTRE</span></div></div>
  </main>
  <aside class="panel right"><h3>Alertes & événements</h3><div id="g360-alert-list"><div class="alert"><b>Surveillance autonome</b><span>Aucune alerte confirmée. Les anomalies candidates nécessitent une vérification humaine.</span></div></div><h3>Sources</h3><div class="source"><b>🛰️ Copernicus Sentinel</b><br><span class="ok">Catalogue public disponible</span></div><div class="source"><b>📹 Caméras autorisées</b><br><span class="wait">Passerelle officielle requise</span></div><div class="source"><b>🚁 Drones autorisés</b><br><span class="wait">Passerelle officielle requise</span></div><div class="source"><b>🏛️ Sources institutionnelles</b><br><span class="wait">Connexion autorisée requise</span></div></aside>
 </div><div class="footer">GABON 360 AI · Les alertes sont des résultats d'analyse et restent soumises à validation humaine · Pas de suivi individuel ni d'action coercitive automatique</div>
</div>
<script>
(function(){
 const root=document.getElementById('g360-center'); if(!root)return;
 const full=document.getElementById('g360-full');
 full.onclick=()=>{if(document.fullscreenElement)document.exitFullscreen();else root.requestFullscreen?.()};
 window.addEventListener('gabon360:satellite-results',e=>{const d=e.detail||{};document.getElementById('g360-obs').textContent=d.count??0;document.getElementById('g360-sources').textContent=d.count>0?'1':'0';});
 window.GABON360_CENTER={version:'1.0',coverage:'Gabon',automatic_surveillance:true,manual_zone_selection_optional:true,live_satellite_video:false,human_validation_required:true};
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
