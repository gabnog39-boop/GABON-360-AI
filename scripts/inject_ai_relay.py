#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-AI-RELAY-V1 -->'
PAYLOAD=r'''<!-- GABON360-AI-RELAY-V1 -->
<style>
#g360-ai-relay-status{position:fixed;right:10px;top:10px;z-index:2147483646;background:#071522;color:#dff;border:1px solid #31506d;border-radius:9px;padding:5px 8px;font:11px system-ui,sans-serif;max-width:52vw}
#g360-ai-relay-status b{color:#9ff2c2}.g360-relay-w{color:#ffd28a}
</style>
<div id="g360-ai-relay-status"><b>IA centrale</b> · relais initialisation…</div>
<script>
(function(){if(window.__G360_AI_RELAY_V1)return;window.__G360_AI_RELAY_V1=true;
var status=document.getElementById('g360-ai-relay-status');
var modules={map:'Carte SIG',nav:'Navigation terrain',sat:'Satellite',drones:'Drones',cameras:'Caméras',maritime:'Maritime',alerts:'Alertes',reports:'Rapports',stats:'Statistiques',weather:'Météo',sources:'Sources',security:'Sécurité',avatar:'Avatar/IA centrale'};
var health={};Object.keys(modules).forEach(function(k){health[k]={module:modules[k],state:'ready',last:null,count:0}});
function setStatus(t){if(status)status.innerHTML='<b>IA centrale</b> · '+t}
function emit(type,data){var detail={type:type,time:new Date().toISOString(),data:data||{},relay:'GABON360_AI_RELAY'};window.GABON360_AI_RELAY.history.push(detail);if(window.GABON360_AI_RELAY.history.length>100)window.GABON360_AI_RELAY.history.shift();window.dispatchEvent(new CustomEvent('gabon360:ai-relay',{detail:detail}));return detail}
function publish(module,type,data){if(!health[module])health[module]={module:modules[module]||module,state:'ready',last:null,count:0};health[module].last=new Date().toISOString();health[module].count++;health[module].state='ready';var e=emit(type,{module:module,payload:data||{}});if(data&&data.voice)window.dispatchEvent(new CustomEvent('gabon360:ai-speak',{detail:{text:String(data.voice),source:module}}));return e}
function navigate(id){if(window.GABON360_NAVIGATE){window.GABON360_NAVIGATE(id);publish('avatar','ai-navigation',{target:id});return true}return false}
function command(text){var q=String(text||'');var r=window.GABON360_HANDLE_COMMAND?window.GABON360_HANDLE_COMMAND(q):null;if(r&&r.ok){publish('avatar','ai-command',{text:q,target:r.page});return r}emit('ai-command-unresolved',{text:q});return r||{ok:false}}
window.GABON360_AI_RELAY={version:'1.0',modules:modules,health:health,history:[],publish:publish,navigate:navigate,command:command,emit:emit,healthSnapshot:function(){return JSON.parse(JSON.stringify(health))}};
var known=['satellite-results','coordinates-selected','ai-command','ai-speak','terrain-position','terrain-waypoint','terrain-track','weather-result','alert-created','alert-updated','report-created','source-status','drone-status','camera-status','maritime-status'];
known.forEach(function(name){window.addEventListener('gabon360:'+name,function(e){var d=e&&e.detail||{};var mod=(d.module||d.source||name.split('-')[0]);if(!modules[mod]){if(name.indexOf('satellite')===0)mod='sat';else if(name.indexOf('terrain')===0)mod='nav';else if(name.indexOf('weather')===0)mod='weather';else if(name.indexOf('alert')===0)mod='alerts';else if(name.indexOf('report')===0)mod='reports';else if(name.indexOf('source')===0)mod='sources';else if(name.indexOf('drone')===0)mod='drones';else if(name.indexOf('camera')===0)mod='cameras';else if(name.indexOf('maritime')===0)mod='maritime';else mod='avatar'}publish(mod,name,d);if(name==='ai-command')command(d.text||d.command||'')})});
window.addEventListener('gabon360:ai-command',function(e){var d=e&&e.detail||{};command(d.text||'')});
Object.keys(modules).forEach(function(k){publish(k,'module-ready',{module:k})});
setStatus('relais actif · '+Object.keys(modules).length+' modules connectés');
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARK in t:
            print('already:',p);return
        i=t.lower().rfind('</body>')
        if i>=0:
            p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8');print('injected:',p);return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
