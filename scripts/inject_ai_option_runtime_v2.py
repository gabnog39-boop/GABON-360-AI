from pathlib import Path

MARKER = "GABON360-AI-OPTION-RUNTIME-V2"


def find_index():
    files = sorted(Path("android_project").rglob("index.html"), key=lambda p: len(p.parts))
    if not files:
        raise SystemExit("index.html introuvable")
    return files[0]


def main():
    path = find_index()
    html = path.read_text(encoding="utf-8", errors="ignore")
    if MARKER in html:
        print("AI option runtime V2 déjà présent")
        return
    block = r"""
<!-- GABON360-AI-OPTION-RUNTIME-V2 -->
<script>
(function () {
  "use strict";
  if (window.__G360_OPTION_RUNTIME_V2) return;
  window.__G360_OPTION_RUNTIME_V2 = true;
  const MARKER = "GABON360-AI-OPTION-RUNTIME-V2";
  const AI_BY_PAGE = {
    avatar:"avatar", map:"sig", nav:"navigation", sat:"satellite",
    drones:"drones", cameras:"cameras", maritime:"maritime", forests:"forests",
    alerts:"alerts", reports:"reports", stats:"stats", weather:"weather",
    sources:"sources", security:"cyber", memory:"memory", water:"water",
    risks:"risk", infrastructures:"infrastructure", crisis:"crisis",
    logistics:"logistics", fusion:"fusion", continuous:"continuous-watch",
    orchestrator:"orchestrator", governance:"governance", access:"access", admin:"admin"
  };
  const STORE_KEY = "g360_ai_pending_v2";
  const state = window.GABON360_AI_OPTION_RUNTIME = window.GABON360_AI_OPTION_RUNTIME || {
    currentPage:"avatar", events:[], notifications:[], active:true
  };
  let speaking = false, lastSpokenAt = 0, repeatTimer = null;
  function now(){ return new Date().toISOString(); }
  function pageAI(page){ return AI_BY_PAGE[page] || page || "orchestrator"; }
  function readPending(){
    try { const x = JSON.parse(localStorage.getItem(STORE_KEY) || "[]"); return Array.isArray(x) ? x : []; }
    catch(e) { return []; }
  }
  function savePending(items){ try { localStorage.setItem(STORE_KEY, JSON.stringify(items.slice(-100))); } catch(e) {} }
  state.pending = readPending();
  function important(event){
    return ["CRITICAL","ALERT","HIGH","WARNING","IMPORTANT","ALERTE"].includes(String(event.severity||"").toUpperCase());
  }
  function signature(e){ return [e.module,e.event,e.observation,e.source].map(x=>String(x||"").trim().toLowerCase()).join("|"); }
  function ensurePanel(){
    let panel = document.getElementById("g360-ai-pending-v2");
    if(panel) return panel;
    panel = document.createElement("section");
    panel.id = "g360-ai-pending-v2";
    panel.setAttribute("aria-live","polite");
    panel.style.cssText = "position:fixed;left:10px;right:10px;bottom:12px;z-index:2147483000;max-height:34vh;overflow:auto;background:#071522;color:#f3f8ff;border:1px solid #4d7896;border-radius:12px;padding:10px;font:14px system-ui;box-shadow:0 4px 20px #0008;display:none";
    document.body.appendChild(panel);
    return panel;
  }
  function renderPending(){
    const panel = ensurePanel(), items = state.pending;
    if(!items.length){ panel.style.display="none"; return; }
    panel.style.display="block";
    const top = items.slice().sort((a,b)=>rank(b)-rank(a))[0];
    panel.textContent = "";
    const head = document.createElement("div");
    head.style.cssText="font-weight:700;margin-bottom:6px";
    head.textContent = "GABON 360 AI · "+items.length+" information(s) non consultée(s)";
    panel.appendChild(head);
    const btn = document.createElement("button");
    btn.type="button"; btn.style.cssText="display:block;width:100%;text-align:left;padding:9px;margin:5px 0;background:#102b40;color:#fff;border:1px solid #54758c;border-radius:8px";
    btn.textContent = (String(top.severity||"INFO").toUpperCase())+" — "+String(top.observation||"Nouvelle information")+" · Ouvrir les détails";
    btn.addEventListener("click",()=>acknowledge(top.id));
    panel.appendChild(btn);
    const hint=document.createElement("small"); hint.textContent="Les informations restent ici jusqu’à leur ouverture."; panel.appendChild(hint);
  }
  function rank(e){ const s=String(e.severity||"").toUpperCase(); return s==="CRITICAL"?4:(s==="HIGH"||s==="ALERT"||s==="ALERTE")?3:(s==="WARNING"||s==="IMPORTANT")?2:1; }
  function speak(text){
    if(speaking || Date.now()-lastSpokenAt < 4000) return false;
    try {
      const done=()=>{ speaking=false; lastSpokenAt=Date.now(); };
      if(typeof window.G360AvatarSpeak==="function"){ speaking=true; window.G360AvatarSpeak(text); lastSpokenAt=Date.now(); setTimeout(done, Math.min(20000,Math.max(3500,text.length*65))); return true; }
      if(typeof window.G360Speak==="function"){ speaking=true; window.G360Speak(text); lastSpokenAt=Date.now(); setTimeout(done, Math.min(20000,Math.max(3500,text.length*65))); return true; }
      if(window.speechSynthesis && typeof SpeechSynthesisUtterance!=="undefined"){
        if(window.speechSynthesis.speaking) return false;
        const u=new SpeechSynthesisUtterance(text); u.lang="fr-FR"; u.onend=done; u.onerror=done;
        speaking=true; window.speechSynthesis.speak(u); lastSpokenAt=Date.now(); return true;
      }
    } catch(e){ speaking=false; }
    return false;
  }
  function acknowledge(id){
    const item=state.pending.find(x=>x.id===id);
    if(!item) return;
    state.pending=state.pending.filter(x=>x.id!==id); savePending(state.pending); renderPending();
    item.consultedAt=now(); item.status="CONSULTED";
    try{ window.dispatchEvent(new CustomEvent("gabon360:ai-notification-consulted",{detail:item})); }catch(e){}
    const dlg=document.createElement("div");
    dlg.style.cssText="position:fixed;inset:8% 5%;z-index:2147483001;overflow:auto;background:#081724;color:#fff;border:1px solid #62819a;border-radius:14px;padding:16px;font:15px system-ui;box-shadow:0 6px 28px #000b";
    const title=document.createElement("h3"); title.textContent=String(item.severity||"INFO")+" · Détail de l’information"; dlg.appendChild(title);
    [["Information",item.observation],["Module",item.module],["Source",item.source],["Heure",item.timestamp],["Statut",item.status],["Confiance",item.confidence==null?"Non précisée":Math.round(item.confidence*100)+"%"],["Action recommandée",item.recommended_action||"À évaluer"],["Validation humaine",item.requires_human_validation===false?"Non requise":"Requise"]].forEach(pair=>{const p=document.createElement("p");const b=document.createElement("b");b.textContent=pair[0]+": ";p.appendChild(b);p.appendChild(document.createTextNode(String(pair[1]||"Non précisé")));dlg.appendChild(p);});
    const close=document.createElement("button"); close.type="button";close.textContent="Fermer · information consultée";close.style.cssText="padding:10px;width:100%;background:#176047;color:white;border:0;border-radius:8px";close.addEventListener("click",()=>dlg.remove());dlg.appendChild(close);document.body.appendChild(dlg);
  }
  function notify(event){
    const e=Object.assign({timestamp:now(),severity:"INFO",status:"AI_RECEIVED"},event||{});
    state.events.push(e); if(state.events.length>300) state.events.shift();
    if(important(e)){
      const sig=signature(e);
      const exists=state.pending.some(x=>x.signature===sig);
      if(!exists){
        e.id=e.id||("g360-"+Date.now()+"-"+Math.random().toString(36).slice(2,8)); e.signature=sig; e.createdAt=now(); e.status="PENDING";
        state.pending.push(e); if(state.pending.length>100)state.pending.shift(); savePending(state.pending);
      }
      renderPending();
      if(!exists) speak((String(e.severity).toUpperCase()==="CRITICAL"?"Alerte critique. ":"Nouvelle information importante. ")+String(e.observation||"Information reçue")+". Source : "+String(e.source||"non précisée")+". Ouvre l’alerte pour consulter les détails.");
    }
    try{window.dispatchEvent(new CustomEvent("gabon360:ai-option-event",{detail:e}));}catch(err){}
    try{if(window.GABON360_AI_RELAY&&typeof window.GABON360_AI_RELAY.publish==="function")window.GABON360_AI_RELAY.publish(e.module||e.ai||"orchestrator",e.event||"ai-option-event",e);}catch(err){}
    return e;
  }
  function dispatch(page,option,data){
    return notify(Object.assign({module:page,option:option,ai:pageAI(page),event:"option-action",timestamp:now(),source:"interface-mobile",observation:"Action "+option+" enregistrée pour l’IA "+pageAI(page),confidence:null,severity:"INFO",status:"AI_MANAGED",evidence:[],recommended_action:null,requires_human_validation:true},data||{}));
  }
  function setPage(page){if(!page)return;state.currentPage=page;dispatch(page,"page-opened",{event:"page-opened",observation:"Page ouverte.",severity:"INFO"});}
  function bind(){
    document.addEventListener("click",function(e){
      const el=e.target&&e.target.closest?e.target.closest("[data-ai-option]"):null;if(!el)return;
      dispatch(el.getAttribute("data-ai-page")||state.currentPage||"avatar",el.getAttribute("data-ai-option")||"action",{
        event:el.getAttribute("data-ai-event")||"option-action",
        observation:el.getAttribute("data-ai-observation")||("Option "+(el.getAttribute("data-ai-option")||"action")+" sélectionnée."),
        severity:el.getAttribute("data-ai-severity")||"INFO",
        requires_human_validation:el.getAttribute("data-human-validation")!=="false"
      });
    },true);
    document.addEventListener("gabon360:page-navigation",e=>setPage((e.detail&&e.detail.current)||state.currentPage));
    renderPending();
  }
  window.GABON360_AI_OPTION_DISPATCH=dispatch;
  window.GABON360_AI_OPTION_NOTIFY=notify;
  window.GABON360_AI_OPTION_ACKNOWLEDGE=acknowledge;
  window.GABON360_AI_OPTION_PAGE_AI=pageAI;
  window.GABON360_AI_OPTION_HEALTH=()=>({status:"active",currentPage:state.currentPage,events:state.events.length,pending:state.pending.length,proactiveAvatar:true,centralRelay:!!window.GABON360_AI_RELAY,humanValidationBoundary:true});
  window.addEventListener("gabon360:ai-event",e=>{if(e&&e.detail&&important(e.detail))notify(e.detail);});
  window.addEventListener("gabon360:ai-notification",e=>{if(e&&e.detail)notify(e.detail);});
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",bind);else bind();
  repeatTimer=setInterval(()=>{if(state.pending.length){renderPending();const top=state.pending.slice().sort((a,b)=>rank(b)-rank(a))[0];speak("Rappel GABON 360 AI. Une information reste non consultée : "+String(top.observation||"alerte")+". Ouvre-la pour voir les détails.");}},45000);
  console.log(MARKER+" actif");
})();
</script>
"""
    html += "\n" + block + "\n"
    path.write_text(html, encoding="utf-8")
    print("Runtime IA avec alertes persistantes intégré dans", path)


if __name__ == "__main__":
    main()
