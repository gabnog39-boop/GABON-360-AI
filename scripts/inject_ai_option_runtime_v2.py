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

    block = r'''
<!-- GABON360-AI-OPTION-RUNTIME-V2 -->
<script>
(function () {
  "use strict";
  const MARKER = "GABON360-AI-OPTION-RUNTIME-V2";
  const ORDER = ["avatar","map","nav","sat","drones","cameras","maritime","forests","alerts","reports","stats","weather","sources","security","memory"];

  const AI_BY_PAGE = {
    avatar:"avatar", map:"sig", nav:"navigation", sat:"satellite",
    drones:"drones", cameras:"cameras", maritime:"maritime", forests:"forests",
    alerts:"alerts", reports:"reports", stats:"stats", weather:"weather",
    sources:"sources", security:"cyber", memory:"memory",
    water:"water", risks:"risk", infrastructures:"infrastructure",
    crisis:"crisis", logistics:"logistics", fusion:"fusion",
    continuous:"continuous-watch", orchestrator:"orchestrator",
    governance:"governance", access:"access", admin:"admin"
  };

  const state = window.GABON360_AI_OPTION_RUNTIME = window.GABON360_AI_OPTION_RUNTIME || {
    currentPage:"avatar", events:[], notifications:[], active:true
  };

  function now(){ return new Date().toISOString(); }
  function pageAI(page){ return AI_BY_PAGE[page] || page || "orchestrator"; }

  function avatarSpeak(text){
    try {
      if (typeof window.G360AvatarSpeak === "function") { window.G360AvatarSpeak(text); return true; }
      if (typeof window.G360Speak === "function") { window.G360Speak(text); return true; }
      if (window.speechSynthesis) {
        const u = new SpeechSynthesisUtterance(text);
        u.lang = "fr-FR"; window.speechSynthesis.cancel(); window.speechSynthesis.speak(u); return true;
      }
    } catch(e) {}
    return false;
  }

  function notify(event){
    const important = ["CRITICAL","ALERT","HIGH","WARNING","IMPORTANT","ALERTE"].includes(String(event.severity||"").toUpperCase());
    state.events.push(event);
    if (state.events.length > 300) state.events.shift();
    if (important) {
      state.notifications.push(event);
      if (state.notifications.length > 100) state.notifications.shift();
      const prefix = event.severity === "CRITICAL" ? "ALERTE CRITIQUE" : "Notification GABON 360 AI";
      const text = prefix + ". " + event.observation +
        ". Source: " + (event.source || "non précisée") +
        ". Heure: " + (event.timestamp || now()) +
        (event.requires_human_validation ? ". Validation humaine requise." : ".");
      avatarSpeak(text);
    }
    try { window.dispatchEvent(new CustomEvent("gabon360:ai-option-event",{detail:event})); } catch(e) {}
    try {
      if (window.GABON360_AI_RELAY && typeof window.GABON360_AI_RELAY.publish === "function")
        window.GABON360_AI_RELAY.publish(event.module || event.ai || "orchestrator", event.event || "ai-option-event", event);
    } catch(e) {}
    return event;
  }

  function dispatch(page, option, data){
    const event = Object.assign({
      module:page,
      option:option,
      ai:pageAI(page),
      event:"option-action",
      timestamp:now(),
      source:"interface-mobile",
      observation:"Action " + option + " traitée par l'IA " + pageAI(page),
      confidence:null,
      severity:"INFO",
      status:"AI_MANAGED",
      evidence:[],
      recommended_action:null,
      requires_human_validation:true
    }, data || {});
    return notify(event);
  }

  function setPage(page){
    if (!page) return;
    state.currentPage = page;
    dispatch(page,"page-opened",{event:"page-opened",observation:"Page ouverte et prise en charge par son IA spécialisée.",severity:"INFO"});
  }

  function bind(){
    document.addEventListener("click", function(e){
      const el = e.target && e.target.closest ? e.target.closest("[data-ai-option]") : null;
      if (!el) return;
      const page = el.getAttribute("data-ai-page") || state.currentPage || "avatar";
      const option = el.getAttribute("data-ai-option") || "action";
      const validation = el.getAttribute("data-human-validation");
      dispatch(page, option, {
        event:el.getAttribute("data-ai-event") || "option-action",
        observation:el.getAttribute("data-ai-observation") || ("Option " + option + " exécutée."),
        severity:el.getAttribute("data-ai-severity") || "INFO",
        requires_human_validation: validation !== "false"
      });
    }, true);

    document.addEventListener("gabon360:page-navigation", function(e){
      setPage((e.detail && e.detail.current) || state.currentPage);
    });
  }

  window.GABON360_AI_OPTION_DISPATCH = dispatch;
  window.GABON360_AI_OPTION_NOTIFY = notify;
  window.GABON360_AI_OPTION_PAGE_AI = pageAI;
  window.GABON360_AI_OPTION_HEALTH = function(){
    return {status:"active", currentPage:state.currentPage, events:state.events.length,
      proactiveAvatar:true, centralRelay:true, humanValidationBoundary:true};
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded",bind);
  else bind();
  console.log(MARKER + " actif");
})();
</script>
'''
    html += "
" + block + "
"
    path.write_text(html, encoding="utf-8")
    print("Runtime IA optionnel V2 intégré dans", path)


if __name__ == "__main__":
    main()
