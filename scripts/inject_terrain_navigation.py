#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

MARKER='<!-- GABON360-TERRAIN-NAV-V1 -->'
PAYLOAD=r'''<!-- GABON360-TERRAIN-NAV-V1 -->
<style>
#g360-terrain-nav{position:fixed;left:14px;bottom:14px;z-index:99998;background:#0b1a2a;color:#eef6ff;border:1px solid #31506d;border-radius:12px;padding:8px;font:12px system-ui,sans-serif;box-shadow:0 10px 30px #0008}
#g360-terrain-nav button{border:1px solid #29425a;background:#102337;color:#fff;border-radius:8px;padding:8px 10px;margin:2px;cursor:pointer}
#g360-terrain-modal{position:fixed;inset:0;background:#000b;z-index:100004;display:none;align-items:center;justify-content:center;padding:12px}
#g360-terrain-card{width:min(760px,97vw);max-height:92vh;overflow:auto;background:#0b1a2a;border:1px solid #31506d;border-radius:14px;padding:14px;color:#eef6ff;font:13px system-ui,sans-serif}
#g360-terrain-map{height:310px;border:1px solid #31506d;border-radius:10px;overflow:hidden;margin:10px 0}
#g360-terrain-map iframe{width:100%;height:100%;border:0}
.g360-nav-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.g360-nav-box{padding:10px;border:1px solid #193047;border-radius:10px;background:#071522}.g360-nav-muted{opacity:.78}
</style>
<div id="g360-terrain-nav"><button id="g360-terrain-open">🧭 Navigation terrain</button></div>
<div id="g360-terrain-modal"><div id="g360-terrain-card">
 <div style="display:flex;justify-content:space-between;gap:8px;align-items:center"><h2 style="margin:0">🧭 Navigation terrain</h2><button id="g360-terrain-close">Fermer</button></div>
 <p id="g360-terrain-status" class="g360-nav-muted">GNSS/GPS : en attente d'autorisation.</p>
 <div class="g360-nav-grid">
  <div class="g360-nav-box"><b>Position</b><div id="g360-terrain-pos">—</div></div>
  <div class="g360-nav-box"><b>Altitude</b><div id="g360-terrain-alt">—</div></div>
  <div class="g360-nav-box"><b>Précision</b><div id="g360-terrain-acc">—</div></div>
  <div class="g360-nav-box"><b>État hors-ligne</b><div>Carte de base : réseau requis pour l'affichage OSM. Les fonctions GNSS restent disponibles si le téléphone les fournit.</div></div>
 </div>
 <div id="g360-terrain-map"><iframe id="g360-terrain-frame" title="Carte de navigation terrain" loading="lazy"></iframe></div>
 <div>
  <button id="g360-terrain-locate">📍 Obtenir ma position</button>
  <button id="g360-terrain-voice">🔊 Guidage vocal</button>
  <button id="g360-terrain-stopvoice">⏹️ Arrêter la voix</button>
 </div>
 <p class="g360-nav-muted">Les coordonnées, l'altitude et les alertes ne sont affichées que lorsqu'une donnée réelle est fournie par le téléphone ou une source autorisée. Aucune position ou alerte fictive n'est générée.</p>
</div></div>
<script>
(function(){
 const modal=document.getElementById('g360-terrain-modal');
 const status=document.getElementById('g360-terrain-status');
 const posEl=document.getElementById('g360-terrain-pos');
 const altEl=document.getElementById('g360-terrain-alt');
 const accEl=document.getElementById('g360-terrain-acc');
 const frame=document.getElementById('g360-terrain-frame');
 let last=null, watchId=null;
 const say=t=>{window.dispatchEvent(new CustomEvent('gabon360:ai-speak',{detail:{text:t}}));if('speechSynthesis' in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(t));}};
 function map(lat,lon){const d=.08;frame.src='https://www.openstreetmap.org/export/embed.html?bbox='+(lon-d)+'%2C'+(lat-d)+'%2C'+(lon+d)+'&layer=mapnik&marker='+lat+'%2C'+lon;}
 function success(p){last=p;const c=p.coords;posEl.textContent=c.latitude.toFixed(6)+'°, '+c.longitude.toFixed(6)+'°';altEl.textContent=(Number.isFinite(c.altitude)?c.altitude.toFixed(1)+' m':'Non fournie par le GNSS');accEl.textContent=(Number.isFinite(c.accuracy)?c.accuracy.toFixed(1)+' m':'Non fournie');status.textContent='GNSS/GPS : position reçue à '+new Date(p.timestamp).toLocaleTimeString();map(c.latitude,c.longitude);say('Navigation terrain active. Position GPS reçue. Latitude '+c.latitude.toFixed(4)+' degrés, longitude '+c.longitude.toFixed(4)+' degrés.');}
 function error(e){status.textContent='GNSS/GPS indisponible : '+(e&&e.message?e.message:'autorisation refusée ou signal indisponible')+'.';say('La position GPS n’est pas disponible. Vérifiez l’autorisation de localisation et le signal GNSS.');}
 function locate(){if(!navigator.geolocation){error({message:'la géolocalisation n’est pas supportée par ce WebView'});return}status.textContent='GNSS/GPS : recherche de position…';navigator.geolocation.getCurrentPosition(success,error,{enableHighAccuracy:true,timeout:15000,maximumAge:5000});if(watchId===null)watchId=navigator.geolocation.watchPosition(success,error,{enableHighAccuracy:true,maximumAge:5000,timeout:20000});}
 document.getElementById('g360-terrain-open').onclick=()=>{modal.style.display='flex';say('Navigation terrain ouverte. Je recherche votre position GPS.');if(last)map(last.coords.latitude,last.coords.longitude);else locate()};
 document.getElementById('g360-terrain-close').onclick=()=>modal.style.display='none';
 modal.onclick=e=>{if(e.target===modal)modal.style.display='none'};
 document.getElementById('g360-terrain-locate').onclick=locate;
 document.getElementById('g360-terrain-voice').onclick=()=>{if(!last){say('Position GPS non disponible. Autorisez la localisation et attendez un signal.');return}const c=last.coords;say('Position reçue. Latitude '+c.latitude.toFixed(4)+' degrés, longitude '+c.longitude.toFixed(4)+' degrés. '+(Number.isFinite(c.altitude)?'Altitude '+Math.round(c.altitude)+' mètres.':'Altitude non fournie.'))};
 document.getElementById('g360-terrain-stopvoice').onclick=()=>{if('speechSynthesis' in window)speechSynthesis.cancel()};
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARKER in t:
            print('already:',p); return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8');print('injected:',p);return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
