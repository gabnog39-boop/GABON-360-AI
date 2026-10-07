#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-CYBERSECURITY-PAGE-V1 -->'
PAYLOAD=r'''<!-- GABON360-CYBERSECURITY-PAGE-V1 -->
<style>
#g360-cyber{position:fixed;inset:0;z-index:2147483010;display:none;background:#020811f8;color:#edf7ff;font:13px system-ui;overflow:auto}
#g360-cyber .box{width:min(1000px,96vw);margin:12px auto;background:#081725;border:1px solid #28465f;border-radius:15px;padding:12px}
#g360-cyber .head{display:flex;gap:8px;align-items:center;position:sticky;top:0;background:#081725ee;padding:7px;z-index:2}
#g360-cyber .head b{flex:1;font-size:18px}
#g360-cyber button{background:#10283b;color:#fff;border:1px solid #31546e;border-radius:9px;padding:9px;font-weight:700}
#g360-cyber .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
#g360-cyber .item{background:#07131f;border:1px solid #1d3448;border-radius:10px;padding:10px}
#g360-cyber .ok{color:#9ff0bf}.g360-cyber-warn{color:#ffd28a}
#g360-cyber pre{white-space:pre-wrap;word-break:break-word}
@media(max-width:650px){#g360-cyber .grid{grid-template-columns:1fr}}
</style>
<div id="g360-cyber"><div class="box"><div class="head"><b>🛡️ CYBERSÉCURITÉ — CENTRE DÉFENSIF</b><button id="g360-cyber-close">✕</button></div>
<div class="item">Surveillance défensive, intégrité, disponibilité, journalisation et diagnostic. Aucune action offensive ou intrusion automatique.</div>
<div class="grid">
<div class="item"><b>🟢 État du système</b><p id="g360-cyber-status">Diagnostic…</p></div>
<div class="item"><b>🌐 Réseau</b><p id="g360-cyber-network">Diagnostic…</p></div>
<div class="item"><b>📱 Appareil</b><p id="g360-cyber-device">Diagnostic…</p></div>
<div class="item"><b>🔐 Session</b><p id="g360-cyber-session">Diagnostic…</p></div>
</div>
<div class="item"><b>Fonctions défensives</b><div id="g360-cyber-actions" style="display:flex;flex-wrap:wrap;gap:7px;margin-top:8px">
<button data-cyber="health">🔎 Diagnostic</button><button data-cyber="integrity">🧩 Intégrité</button><button data-cyber="network">🌐 Réseau</button><button data-cyber="storage">💾 Stockage local</button><button data-cyber="audit">📋 Journal d’audit</button><button data-cyber="export">⬇️ Export audit</button>
</div></div>
<div class="item"><b>Résultat</b><pre id="g360-cyber-result">Prêt.</pre></div>
</div></div>
<script>
(function(){
if(window.__G360_CYBERSECURITY_PAGE_V1)return;
window.__G360_CYBERSECURITY_PAGE_V1=true;
var root=document.getElementById('g360-cyber'),result=document.getElementById('g360-cyber-result');
function rec(){try{return JSON.parse(localStorage.getItem('gabon360_cyber_audit')||'[]')}catch(e){return[]}}
function save(x){localStorage.setItem('gabon360_cyber_audit',JSON.stringify(x.slice(-300)))}
function audit(action,detail){var x=rec();x.push({time:new Date().toISOString(),action:action,detail:detail});save(x)}
function net(){return {online:navigator.onLine,connection:(navigator.connection&&navigator.connection.effectiveType)||'non exposé par Android/webview'}}
function health(){
var n=net(),s={online:n.online,language:navigator.language,userAgent:navigator.userAgent.slice(0,140),secureContext:window.isSecureContext,storageAvailable:false};
try{localStorage.setItem('__g360_test','1');localStorage.removeItem('__g360_test');s.storageAvailable=true}catch(e){}
document.getElementById('g360-cyber-status').textContent=(s.secureContext?'Contexte sécurisé':'Contexte non sécurisé')+' · stockage '+(s.storageAvailable?'OK':'indisponible');
document.getElementById('g360-cyber-network').textContent=(n.online?'Connecté':'Hors ligne')+' · réseau '+n.connection;
document.getElementById('g360-cyber-device').textContent=navigator.platform+' · langue '+navigator.language;
document.getElementById('g360-cyber-session').textContent='Session applicative active · secrets non stockés dans cette page';
result.textContent=JSON.stringify(s,null,2);audit('health',s)
}
function integrity(){
var scripts=[].slice.call(document.scripts).map(function(s){return s.src||'inline'});
var data={script_count:scripts.length,https:location.protocol==='https:',host:location.host,local_storage_keys:Object.keys(localStorage).filter(function(k){return !/^(__g360)/.test(k)}).length};
result.textContent=JSON.stringify(data,null,2);audit('integrity',data)
}
function storage(){
var keys=Object.keys(localStorage),rows=keys.map(function(k){return {key:k,length:(localStorage.getItem(k)||'').length}});
result.textContent=JSON.stringify({count:rows.length,items:rows},null,2);audit('storage',{count:rows.length})
}
function exportAudit(){var blob=new Blob([JSON.stringify(rec(),null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='gabon360-cyber-audit.json';a.click();audit('export','gabon360-cyber-audit.json')}
function run(a){if(a==='health')health();else if(a==='integrity')integrity();else if(a==='network'){var n=net();result.textContent=JSON.stringify(n,null,2);audit('network',n)}else if(a==='storage')storage();else if(a==='audit')result.textContent=JSON.stringify(rec().slice(-50),null,2);else if(a==='export')exportAudit()}
window.GABON360_OPEN_CYBERSECURITY=function(){root.style.display='block';health()};
document.getElementById('g360-cyber-close').onclick=function(){root.style.display='none'};
document.getElementById('g360-cyber-actions').onclick=function(e){var b=e.target.closest('[data-cyber]');if(b)run(b.dataset.cyber)};
})();
</script>
'''
def main():
    files=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' not in p.parts,len(p.parts)))
    if not files: raise SystemExit('index.html introuvable')
    for p in files:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i<0: continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('index.html exploitable introuvable')
if __name__=='__main__': main()
