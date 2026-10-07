#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-CYBER-AI-AVATAR-V1 -->'
PAYLOAD=r'''<!-- GABON360-CYBER-AI-AVATAR-V1 -->
<style>
#g360-cyber-ai{margin:10px 0;background:#06111b;border:1px solid #31516b;border-radius:12px;padding:10px}
#g360-cyber-ai .row{display:flex;flex-wrap:wrap;gap:7px;align-items:center}
#g360-cyber-ai button{background:#10283b;color:#fff;border:1px solid #31546e;border-radius:9px;padding:8px;font-weight:700}
#g360-cyber-ai .state{font-weight:800}
#g360-cyber-ai .ok{color:#9ff0bf}.g360-cyber-risk{color:#ffd28a}.g360-cyber-critical{color:#ff9d9d}
</style>
<script>
(function(){
if(window.__G360_CYBER_AI_AVATAR_V1)return;
window.__G360_CYBER_AI_AVATAR_V1=true;
var events=[],max=200,monitoring=false,timer=null;
var rules=[
 {id:'OFFLINE',label:'Perte de connectivité',severity:'INFO',test:function(e){return e.type==='network'&&e.online===false}},
 {id:'STORAGE',label:'Stockage local indisponible',severity:'HIGH',test:function(e){return e.type==='health'&&e.storageAvailable===false}},
 {id:'INSECURE',label:'Contexte non sécurisé',severity:'HIGH',test:function(e){return e.type==='health'&&e.secureContext===false}},
 {id:'SOURCE_ANOMALY',label:'État inhabituel d’une source',severity:'MEDIUM',test:function(e){return e.type==='source-status'&&e.state&&e.state!=='ready'}},
 {id:'AUTH_REQUIRED',label:'Source protégée sans autorisation',severity:'HIGH',test:function(e){return e.type==='protected-source'&&e.authorized===false}}
];
function add(e){e=e||{};e.time=e.time||new Date().toISOString();events.push(e);if(events.length>max)events.shift();try{localStorage.setItem('gabon360_cyber_ai_events',JSON.stringify(events))}catch(_){};analyze(e)}
function analyze(e){
 var hits=rules.filter(function(r){try{return r.test(e)}catch(_){return false}});
 if(!hits.length)return;
 hits.forEach(function(r){
  var msg='Cybersécurité IA : '+r.label+'. Niveau '+r.severity+'. Vérification humaine recommandée.';
  var detail={rule:r.id,label:r.label,severity:r.severity,event:e,voice:msg};
  try{window.GABON360_AI_RELAY&&window.GABON360_AI_RELAY.publish('security','cyber-ai-alert',detail)}catch(_){}
  try{window.dispatchEvent(new CustomEvent('gabon360:cyber-ai-alert',{detail:detail}))}catch(_){}
  speakAvatar(msg,r.severity);
 });
}
function speakAvatar(text,severity){
 var fn=window.G360AvatarSpeak||window.G360Speak||window.G360&&window.G360.speak;
 try{if(typeof fn==='function')fn(text);else if(window.speechSynthesis){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='fr-FR';window.speechSynthesis.speak(u)}}catch(_){}
 var status=document.getElementById('g360-cyber-ai-status');if(status){status.textContent='Alerte IA · '+severity;status.className='state '+(severity==='HIGH'||severity==='CRITICAL'?'g360-cyber-critical':'g360-cyber-risk')}
}
function load(){try{events=JSON.parse(localStorage.getItem('gabon360_cyber_ai_events')||'[]')}catch(_){events=[]}}
function start(){if(monitoring)return;monitoring=true;timer=setInterval(function(){var e={type:'health',secureContext:!!window.isSecureContext,storageAvailable:(function(){try{localStorage.setItem('__g360cyber','1');localStorage.removeItem('__g360cyber');return true}catch(_){return false}})()};add(e)},15000);setText('Surveillance IA active · analyse toutes les 15 s');try{window.GABON360_AI_RELAY&&window.GABON360_AI_RELAY.publish('security','cyber-ai-start',{voice:'Surveillance cybersécurité IA activée.'})}catch(_){}}
function stop(){monitoring=false;if(timer)clearInterval(timer);timer=null;setText('Surveillance IA en pause')}
function setText(t){var s=document.getElementById('g360-cyber-ai-status');if(s)s.textContent=t}
function openPanel(){
 var p=document.getElementById('g360-cyber-ai');if(p){p.style.display='block';setText(monitoring?'Surveillance IA active':'Surveillance IA prête')}
}
function install(){
 var root=document.getElementById('g360-cyber');if(!root||document.getElementById('g360-cyber-ai'))return;
 var d=document.createElement('div');d.id='g360-cyber-ai';d.innerHTML='<b>🤖 IA CYBERSÉCURITÉ — RELAIS AVEC AVATAR CENTRAL</b><p id="g360-cyber-ai-status" class="state ok">Initialisation…</p><div class="row"><button id="g360-cyber-ai-start">▶️ Activer la surveillance IA</button><button id="g360-cyber-ai-stop">⏸️ Pause</button><button id="g360-cyber-ai-test">🧪 Test défensif</button></div><small>Analyse défensive et explicable. Aucune intrusion, interception ou action offensive automatique.</small>';
 var box=root.querySelector('.box');if(box)box.insertBefore(d,box.children[1]||null);
 d.querySelector('#g360-cyber-ai-start').onclick=start;d.querySelector('#g360-cyber-ai-stop').onclick=stop;
 d.querySelector('#g360-cyber-ai-test').onclick=function(){add({type:'health',secureContext:!!window.isSecureContext,storageAvailable:true,test:true})};
}
window.GABON360_CYBER_AI={version:'1.0',start:start,stop:stop,open:openPanel,events:function(){return events.slice()},analyze:add};
load();
window.addEventListener('gabon360:ai-relay',function(e){var d=e&&e.detail||{};if(d.type==='network'||d.type==='health'||d.type==='protected-source'||d.type==='source-status')add(Object.assign({type:d.type},d.data||{}))});
window.addEventListener('gabon360:cyber-event',function(e){add((e&&e.detail)||{})});
window.addEventListener('gabon360:cyber-ai-alert',function(e){});
var obs=new MutationObserver(install);obs.observe(document.documentElement,{childList:true,subtree:true});
install();
})();
</script>
'''
def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in t:
            print('already:',p); return
        anchor='<!-- GABON360-CYBERSECURITY-PAGE-V1 -->'
        if anchor in t:
            t=t.replace(anchor,anchor+'\n'+PAYLOAD,1)
        else:
            i=t.lower().rfind('</body>')
            if i<0: continue
            t=t[:i]+PAYLOAD+'\n'+t[i:]
        p.write_text(t,encoding='utf-8'); print('injected:',p); return
    raise SystemExit('index.html exploitable introuvable')
if __name__=='__main__': main()
