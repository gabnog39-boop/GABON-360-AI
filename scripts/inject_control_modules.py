#!/usr/bin/env python3
"""Add the operational modules panel to the unified GABON 360 AI web UI."""
from __future__ import annotations
from pathlib import Path

MARKER = "<!-- GABON360-CONTROL-MODULES-V1 -->"
PAYLOAD = r'''<!-- GABON360-CONTROL-MODULES-V1 -->
<style>
#g360-modules{position:fixed;left:14px;bottom:14px;z-index:99996;background:#0b1a2a;color:#eef6ff;border:1px solid #31506d;border-radius:12px;padding:8px;box-shadow:0 10px 30px #0008;font:12px system-ui,sans-serif}
#g360-modules button{border:1px solid #29425a;background:#102337;color:#fff;border-radius:8px;padding:7px 9px;margin:2px;cursor:pointer}
#g360-modules button:hover{background:#15324b}.g360-cm{position:fixed;inset:0;background:#0009;z-index:100001;display:flex;align-items:center;justify-content:center;padding:14px}.g360-cm-card{width:min(760px,96vw);max-height:88vh;overflow:auto;background:#0b1a2a;border:1px solid #31506d;border-radius:14px;padding:16px;color:#eef6ff}.g360-cm-card h2{margin:0 0 10px}.g360-cm-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.g360-cm-item{padding:11px;border:1px solid #193047;border-radius:10px;background:#071522}.g360-cm-item b{display:block;margin-bottom:4px}.g360-cm-ok{color:#8df0b1}.g360-cm-wait{color:#ffd48a}.g360-cm-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.g360-cm-input{flex:1;min-width:180px;padding:9px;border-radius:8px;border:1px solid #29425a;background:#07111d;color:#fff}.g360-cm-map{width:100%;height:420px;border:0;border-radius:10px;background:#07111d}@media(max-width:650px){.g360-cm-grid{grid-template-columns:1fr}}
</style>
<div id="g360-modules"><button id="g360-modules-open">⚙️ Modules</button><button id="g360-map-open">🗺️ Carte SIG</button><button id="g360-weather-open">🌦️ Météo</button></div>
<div id="g360-cm-modal" class="g360-cm" style="display:none"><div class="g360-cm-card"><div class="g360-cm-row" style="justify-content:space-between"><h2 id="g360-cm-title">GABON 360 AI — Modules</h2><button id="g360-cm-close">Fermer</button></div><div id="g360-cm-body"></div></div></div>
<script>
(function(){
 const modal=document.getElementById('g360-cm-modal'),title=document.getElementById('g360-cm-title'),body=document.getElementById('g360-cm-body');
 const show=(t,h)=>{title.textContent=t;body.innerHTML=h;modal.style.display='flex'};
 document.getElementById('g360-cm-close').onclick=()=>modal.style.display='none';
 modal.addEventListener('click',e=>{if(e.target===modal)modal.style.display='none'});
 document.getElementById('g360-modules-open').onclick=()=>show('⚙️ Modules du centre',`<div class="g360-cm-grid">
 <div class="g360-cm-item"><b>🗺️ Territoire / SIG</b><span class="g360-cm-ok">Interface active</span><br>Carte détaillée accessible ci-dessous.</div>
 <div class="g360-cm-item"><b>🛰️ Satellite</b><span class="g360-cm-ok">Catalogue Copernicus connecté</span><br>Observations catalogue, pas de vidéo continue.</div>
 <div class="g360-cm-item"><b>🌦️ Météo / climat</b><span class="g360-cm-ok">Source publique disponible</span><br>Prévisions chargées à la demande.</div>
 <div class="g360-cm-item"><b>🤖 IA centrale</b><span class="g360-cm-ok">Interface active</span><br>Analyse présentée comme proposition et soumise à validation humaine.</div>
 <div class="g360-cm-item"><b>📋 Événements / rapports</b><span class="g360-cm-ok">Interface active</span><br>Chronologie et traçabilité locale.</div>
 <div class="g360-cm-item"><b>📡 Sources institutionnelles</b><span class="g360-cm-wait">Connexion autorisée requise</span><br>Aucune source institutionnelle n'est inventée.</div>
 <div class="g360-cm-item"><b>🚁 Drones / caméras</b><span class="g360-cm-wait">Passerelle officielle requise</span><br>Pas de flux fictif.</div>
 <div class="g360-cm-item"><b>🔐 Sécurité / accès</b><span class="g360-cm-ok">Contrôle d'interface actif</span><br>Les secrets ne doivent pas être embarqués dans l'APK.</div>
 <div class="g360-cm-item"><b>📶 Hors-ligne / synchronisation</b><span class="g360-cm-ok">État local disponible</span><br>Les données non synchronisées restent signalées comme locales.</div>
 <div class="g360-cm-item"><b>👤 Suivi individuel</b><span class="g360-cm-ok">Désactivé</span><br>Aucun suivi individuel automatique.</div>
 </div>`);
 document.getElementById('g360-map-open').onclick=()=>show('🗺️ Carte SIG détaillée',`<p>Carte publique OpenStreetMap du Gabon. Le niveau de détail dépend des données disponibles et de la connexion.</p><iframe class="g360-cm-map" title="Carte du Gabon" src="https://www.openstreetmap.org/export/embed.html?bbox=8.5%2C-4.0%2C14.5%2C2.5&layer=mapnik"></iframe><p style="font-size:11px;opacity:.7">Source cartographique : OpenStreetMap. Les couches opérationnelles autorisées doivent être ajoutées via leurs sources SIG officielles.</p>`);
 document.getElementById('g360-weather-open').onclick=async()=>{show('🌦️ Météo — Gabon','<p>Connexion à la source météo publique…</p>');try{const r=await fetch('https://api.open-meteo.com/v1/forecast?latitude=0.39&longitude=9.45&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code&timezone=Africa%2FLibreville');if(!r.ok)throw Error('HTTP '+r.status);const d=await r.json(),c=d.current||{};body.innerHTML='<div class="g360-cm-item"><b>Libreville / zone de référence</b><span class="g360-cm-ok">Données reçues</span><br>Température : '+(c.temperature_2m??'—')+' °C<br>Humidité : '+(c.relative_humidity_2m??'—')+' %<br>Précipitations : '+(c.precipitation??'—')+' mm<br>Vent : '+(c.wind_speed_10m??'—')+' km/h<br>Code météo : '+(c.weather_code??'—')+'<br><small>Source : Open-Meteo · données de modèle, pas une observation locale directe.</small></div>'}catch(e){body.innerHTML='<div class="g360-cm-item"><b>Météo indisponible</b><span class="g360-cm-wait">Aucune donnée simulée</span><br>Erreur réseau : '+(e.message||e)+'</div>'}};
})();
</script>
'''

def main() -> None:
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
