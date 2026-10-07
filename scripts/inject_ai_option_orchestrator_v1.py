#!/usr/bin/env python3
"""Relie chaque option de chaque page à son IA spécialisée, au relais central et à l'avatar."""

from pathlib import Path

MARK = "GABON360-AI-OPTION-ORCHESTRATOR-V1"

PAYLOAD = r'''<!-- GABON360-AI-OPTION-ORCHESTRATOR-V1 -->
<script>
(function(){
if(window.__G360_AI_OPTION_ORCHESTRATOR_V1)return;
window.__G360_AI_OPTION_ORCHESTRATOR_V1=true;

var AI_BY_PAGE={
 map:'sig',nav:'navigation',sat:'satellite',drones:'drones',cameras:'cameras',
 maritime:'maritime',forests:'forests',alerts:'alerts',reports:'reports',
 stats:'stats',weather:'weather',sources:'sources',security:'cyber',
 avatar:'avatar',memory:'memory',crisis:'crisis',logistics:'logistics',
 fusion:'fusion','continuous-watch':'continuous-watch',orchestrator:'orchestrator',
 governance:'governance',access:'access',admin:'admin'
};

var OPTION_AI={};
var lastEvent=null;

function now(){return new Date().toISOString()}
function coords(){return window.GABON360_SELECTED_COORDINATES||{}}
function speak(text){
 try{
  var f=window.G360AvatarSpeak||window.G360Speak||(window.G360&&window.G360.speak);
  if(typeof f==='function'){f(text);return}
  if(window.speechSynthesis){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='fr-FR';window.speechSynthesis.speak(u)}
 }catch(_){}
}
function publish(e){
 lastEvent=e;
 try{
  if(window.GABON360_AI_RELAY) window.GABON360_AI_RELAY.publish(e.module,e.type||'ai-option-analysis',e);
 }catch(_){}
 window.dispatchEvent(new CustomEvent('gabon360:ai-event',{detail:e}));
 window.dispatchEvent(new CustomEvent('gabon360:ai-option',{detail:e}));
}
function analyze(page,action){
 var ai=AI_BY_PAGE[page]||page||'orchestrator';
 var e={
  module:page,
  specialized_ai:ai,
  type:'ai-option-analysis',
  source:'IA spécialisée '+ai,
  timestamp:now(),
  location:coords(),
  observation:'Option « '+String(action)+' » prise en charge par l’IA spécialisée '+ai+'.',
  confidence:null,
  severity:'INFO',
  status:'AI_PROCESSING',
  evidence:[],
  recommended_action:'L’IA spécialisée traite la fonction puis transmet le résultat au relais central.',
  requires_human_validation:true,
  avatar_target:'central'
 };
 OPTION_AI[page+'|'+action]=ai;
 publish(e);
 return e;
}
function important(e){
 return e && (e.severity==='HIGH'||e.severity==='CRITICAL'||e.status==='ANOMALY_PROBABLE'||e.status==='ALERT');
}
function route(e){
 if(!e)return;
 try{
  if(window.GABON360_AI_RELAY)window.GABON360_AI_RELAY.publish(e.module,'ai-notification',e);
 }catch(_){}
 if(important(e)){
  speak('GABON 360 AI. '+e.observation+'. Source : '+e.source+'. '+(e.requires_human_validation?'Validation humaine requise.':''));
 }
}
window.GABON360_AI_OPTION_ORCHESTRATOR={
 version:'1.0',
 map:AI_BY_PAGE,
 optionAI:OPTION_AI,
 analyze:analyze,
 publish:publish,
 route:route,
 last:function(){return lastEvent}
};

window.addEventListener('gabon360:page-action',function(ev){
 var d=ev&&ev.detail||{};
 if(d.page&&d.action) analyze(d.page,d.action);
});
window.addEventListener('gabon360:ai-event',function(ev){
 var d=ev&&ev.detail||{};
 if(d.module==='memory'||d.module==='cyber'||d.severity==='HIGH'||d.severity==='CRITICAL') route(d);
});
window.addEventListener('gabon360:ai-relay',function(ev){
 var d=ev&&ev.detail||{};
 var e=d.data||d;
 if(e && e.module) route(e);
});

/* Toutes les fonctions déclarées par le centre sont enregistrées comme options IA. */
function registerModules(){
 var modules=window.GABON360_MODULE_PAGES||{};
 Object.keys(modules).forEach(function(page){
  var ai=AI_BY_PAGE[page]||'orchestrator';
  (modules[page].actions||[]).forEach(function(action){
   OPTION_AI[page+'|'+action]=ai;
  });
 });
}
setTimeout(registerModules,0);
setTimeout(registerModules,500);
setTimeout(registerModules,1500);
})();
</script>
'''

def main():
    candidates=sorted(Path("android_project").rglob("index.html"), key=lambda p: ("assets" in p.parts, len(p.parts)))
    if not candidates:
        raise SystemExit("index.html introuvable")
    for p in candidates:
        t=p.read_text(encoding="utf-8", errors="ignore")
        if MARK in t:
            print("already:",p)
            return
        i=t.lower().rfind("</body>")
        if i < 0:
            continue
        p.write_text(t[:i]+PAYLOAD+"\n"+t[i:],encoding="utf-8")
        print("injected:",p)
        return
    raise SystemExit("Aucun index.html exploitable")

if __name__=="__main__":
    main()
