#!/usr/bin/env python3
"""Injecte l'architecture IA spécialisée -> relais -> avatar dans l'APK."""

from pathlib import Path

MARK = "<!-- GABON360-SPECIALIZED-AI-ARCHITECTURE-V1 -->"

PAYLOAD = r'''<!-- GABON360-SPECIALIZED-AI-ARCHITECTURE-V1 -->
<style>
#g360-ai-architecture{margin:10px 0;padding:10px;border:1px solid #31516b;border-radius:12px;background:#06111b;color:#e9f7ff;font:12px system-ui,sans-serif}
#g360-ai-architecture .g360-ai-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-top:8px}
#g360-ai-architecture .g360-ai-node{padding:7px;border:1px solid #29465d;border-radius:8px;background:#0b1c2a}
#g360-ai-architecture .g360-ai-state{font-weight:800;color:#9ff0bf}
#g360-ai-architecture .g360-ai-event{margin-top:8px;padding:8px;border-radius:8px;background:#091724;border:1px solid #28455c}
@media(max-width:720px){#g360-ai-architecture .g360-ai-grid{grid-template-columns:1fr 1fr}}
</style>
<div id="g360-ai-architecture">
  <b>🧠 IA SPÉCIALISÉES — RELAIS CENTRAL — AVATAR</b>
  <div class="g360-ai-state" id="g360-ai-architecture-state">Initialisation…</div>
  <div class="g360-ai-grid" id="g360-ai-architecture-grid"></div>
  <div class="g360-ai-event" id="g360-ai-architecture-event">Aucun événement prioritaire.</div>
</div>
<script>
(function(){
if(window.__G360_SPECIALIZED_AI_V1)return;
window.__G360_SPECIALIZED_AI_V1=true;

var definitions=[
 ['sig','SIG / Carte'],['satellite','Satellite'],['forests','Forêts'],['water','Eaux'],
 ['maritime','Maritime'],['weather','Météo'],['risk','Risques'],['infrastructure','Infrastructures'],
 ['navigation','Navigation'],['drones','Drones'],['cameras','Caméras'],['alerts','Alertes'],
 ['reports','Rapports'],['stats','Statistiques'],['sources','Sources'],['cyber','Cybersécurité'],
 ['crisis','Crise'],['logistics','Logistique'],['memory','Mémoire'],['fusion','Fusion'],
 ['continuous-watch','Surveillance continue'],['orchestrator','Orchestrateur national'],
 ['governance','Gouvernance'],['access','Abonnements'],['admin','Administration'],['avatar','Avatar']
];

var grid=document.getElementById('g360-ai-architecture-grid');
var state=document.getElementById('g360-ai-architecture-state');
var eventBox=document.getElementById('g360-ai-architecture-event');

function render(){
 if(!grid)return;
 grid.innerHTML='';
 definitions.forEach(function(d){
   var n=document.createElement('div');
   n.className='g360-ai-node';
   n.id='g360-ai-node-'+d[0].replace(/[^a-z0-9]/gi,'-');
   n.innerHTML='<b>'+d[1]+'</b><br><span>IA prête · relais central</span>';
   grid.appendChild(n);
 });
}
function speak(text){
 var fn=window.G360AvatarSpeak||window.G360Speak||(window.G360&&window.G360.speak);
 try{
   if(typeof fn==='function'){fn(text);return}
   if(window.speechSynthesis){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='fr-FR';window.speechSynthesis.speak(u)}
 }catch(_){}
}
function normalize(d){
 d=d||{};
 return {
   module:String(d.module||d.source||'unknown'),
   source:String(d.source||d.module||'GABON 360 AI'),
   timestamp:d.timestamp||new Date().toISOString(),
   location:d.location||{},
   observation:String(d.observation||d.message||d.type||'Événement reçu'),
   confidence:typeof d.confidence==='number'?d.confidence:null,
   severity:String(d.severity||'INFO'),
   status:String(d.status||'AI_DETECTED'),
   evidence:Array.isArray(d.evidence)?d.evidence:[],
   recommended_action:d.recommended_action||null,
   requires_human_validation:d.requires_human_validation!==false
 };
}
function receive(d){
 var e=normalize(d);
 var node=document.getElementById('g360-ai-node-'+e.module.replace(/[^a-z0-9]/gi,'-'));
 if(node){node.innerHTML='<b>'+e.module+'</b><br><span>'+e.status+' · '+e.severity+'</span>'}
 eventBox.innerHTML='<b>'+e.severity+'</b> · '+e.observation+
   (e.confidence!==null?' · confiance '+Math.round(e.confidence*100)+'%':'')+
   '<br><small>Source : '+e.source+' · '+new Date(e.timestamp).toLocaleString('fr-FR')+
   (e.requires_human_validation?' · validation humaine requise':'')+'</small>';
 if(e.severity==='CRITICAL'||e.severity==='HIGH'){
   speak('GABON 360 AI. '+e.observation+'. Source : '+e.source+'. '+(e.requires_human_validation?'Une validation humaine est requise.':''));
 }
 try{
   if(window.GABON360_AI_RELAY)window.GABON360_AI_RELAY.publish(e.module,'ai-notification',e);
 }catch(_){}
}
window.GABON360_SPECIALIZED_AI={
 version:'1.0',
 definitions:definitions,
 publish:function(event){receive(event)}
};
window.addEventListener('gabon360:ai-relay',function(ev){
 var d=ev&&ev.detail||{};
 if(d.type==='ai-notification'||d.type==='cyber-ai-alert'||d.type==='cross-domain-anomaly'){
   receive(d.data||d);
 }
});
window.addEventListener('gabon360:cyber-ai-alert',function(ev){receive(ev.detail||{})});
window.addEventListener('gabon360:ai-event',function(ev){receive(ev.detail||{})});
render();
if(state)state.textContent='26 IA spécialisées prêtes · relais central actif · avatar connecté';
})();
</script>
'''

def main():
    candidates = sorted(
        Path("android_project").rglob("index.html"),
        key=lambda p: ("assets" in p.parts, len(p.parts)),
    )
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if MARK in text:
            print("already:", path)
            return
        i = text.lower().rfind("</body>")
        if i < 0:
            continue
        path.write_text(text[:i] + PAYLOAD + "\n" + text[i:], encoding="utf-8")
        print("injected:", path)
        return
    raise SystemExit("No suitable index.html found")
if __name__ == "__main__":
    main()
