#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-CONTROL-HARDENING-V1 -->'
PAYLOAD=r'''<!-- GABON360-CONTROL-HARDENING-V1 -->
<style>
#g360-ops-bar{position:fixed;right:10px;top:58px;z-index:99990;display:flex;gap:5px;align-items:center;background:#061522dd;border:1px solid #31506d;border-radius:10px;padding:6px 8px;color:#dff;font:11px system-ui,sans-serif;backdrop-filter:blur(8px)}
#g360-ops-dot{width:8px;height:8px;border-radius:50%;background:#18e77b;box-shadow:0 0 8px #18e77b}
#g360-control-panel{display:none;position:fixed;inset:0;z-index:100030;background:#000b;align-items:center;justify-content:center;padding:12px}
#g360-control-card{width:min(820px,96vw);max-height:90vh;overflow:auto;background:#061522;color:#eafff5;border:1px solid #2adf9b66;border-radius:18px;padding:15px;font:13px system-ui,sans-serif}
#g360-control-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:12px}
.g360-health{border:1px solid #31506d;border-radius:10px;padding:9px;background:#081c2a}.g360-health b{display:block;margin-bottom:4px}.g360-health small{color:#9fc3d9}.g360-status{float:right;font-size:11px;color:#9fe5c7}
#g360-audit{margin-top:12px;border-top:1px solid #31506d;padding-top:10px;color:#a8c6d8;max-height:180px;overflow:auto}
@media(max-width:600px){#g360-ops-bar{top:50px;right:6px}#g360-control-grid{grid-template-columns:1fr}}
</style>
<div id="g360-ops-bar"><span id="g360-ops-dot"></span><b>CENTRE</b><span id="g360-ops-clock">--:--:--</span><button id="g360-ops-open">État</button></div>
<div id="g360-control-panel"><div id="g360-control-card">
<div style="display:flex;justify-content:space-between;gap:8px;align-items:center"><b>🛡️ ÉTAT OPÉRATIONNEL — GABON 360 AI</b><button id="g360-control-close">Fermer</button></div>
<div style="margin-top:8px;color:#9fc3d9">Les indicateurs ci-dessous décrivent uniquement les sources et fonctions réellement connectées. Aucun flux, événement ou position n'est inventé.</div>
<div id="g360-control-grid">
<div class="g360-health"><b>🛰️ Satellites <span class="g360-status" id="h-sat">PUBLIC</span></b><small>Catalogue Copernicus disponible selon réseau.</small></div>
<div class="g360-health"><b>🗺️ SIG <span class="g360-status">ACTIF</span></b><small>Cartographie et sélection de zones.</small></div>
<div class="g360-health"><b>🧭 GNSS <span class="g360-status" id="h-gps">ATTENTE</span></b><small>Position fournie seulement avec autorisation du téléphone.</small></div>
<div class="g360-health"><b>🚁 Drones <span class="g360-status">ATTENTE</span></b><small>Aucun drone connecté sans passerelle autorisée.</small></div>
<div class="g360-health"><b>📹 Caméras <span class="g360-status">ATTENTE</span></b><small>Aucun flux vidéo fictif.</small></div>
<div class="g360-health"><b>🌊 Maritime <span class="g360-status">ATTENTE</span></b><small>Sources maritimes à connecter et authentifier.</small></div>
<div class="g360-health"><b>🌦️ Météo <span class="g360-status">PUBLIC</span></b><small>Données publiques, avec leur source et leur qualité.</small></div>
<div class="g360-health"><b>🤖 IA centrale <span class="g360-status">PRÊTE</span></b><small>Analyse, dialogue et navigation ; validation humaine requise.</small></div>
</div>
<div id="g360-audit"><b>Journal de session</b><div id="g360-audit-lines">Centre initialisé.</div></div>
</div></div>
<script>
(function(){
 const panel=document.getElementById('g360-control-panel'),open=document.getElementById('g360-ops-open'),close=document.getElementById('g360-control-close'),clock=document.getElementById('g360-ops-clock'),lines=document.getElementById('g360-audit-lines');
 const log=[]; function add(msg){const t=new Date().toLocaleTimeString('fr-FR');log.unshift(t+' — '+msg);if(log.length>20)log.pop();lines.innerHTML=log.map(x=>'<div>'+x.replace(/[<>]/g,'')+'</div>').join('');}
 function tick(){clock.textContent=new Date().toLocaleTimeString('fr-FR');} setInterval(tick,1000);tick();
 open.onclick=()=>{panel.style.display='flex';add('Ouverture de l’état opérationnel');};close.onclick=()=>{panel.style.display='none';add('Fermeture de l’état opérationnel');};
 window.GABON360_CONTROL={log:add,setGPS:(on)=>{document.getElementById('h-gps').textContent=on?'ACTIF':'ATTENTE';}};
 window.dispatchEvent(new CustomEvent('gabon360:control-ready'));
})();
</script>
'''
def main():
    candidates=[]
    for root in [Path('android_project'),Path('.')]:
        if root.exists(): candidates += [p for p in root.rglob('index.html') if '.git' not in p.parts and 'build' not in p.parts]
    if not candidates: raise SystemExit('Aucun index.html trouvé')
    p=candidates[0]; text=p.read_text(encoding='utf-8')
    if MARK in text: print('Déjà renforcé'); return
    text=text.replace('</body>',PAYLOAD+'\n</body>',1) if '</body>' in text else text+'\n'+PAYLOAD
    p.write_text(text,encoding='utf-8'); print('Centre renforcé:',p)
if __name__=='__main__': main()
