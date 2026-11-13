/* GABON 360 AI — MODULES ADDITIFS
   Ce fichier ajoute une console de modules sans remplacer le index.html existant.
   Les observations créées ici sont locales au navigateur; aucune source distante n'est simulée.
*/
(() => {
  "use strict";
  if (window.__G360_ADDON_LOADED__) return;
  window.__G360_ADDON_LOADED__ = true;

  const modules = [
    {id:"territoire", name:"Carte territoriale", role:"Consigner une observation territoriale et ses coordonnées.", inputs:["Parc / province / secteur","Coordonnées (facultatif)","Observation"]},
    {id:"navigation", name:"Navigation terrain", role:"Préparer un déplacement, noter les risques et les points de passage.", inputs:["Départ","Destination","Consignes / risques"]},
    {id:"satellites", name:"Satellites", role:"Enregistrer une demande d'imagerie. Aucun flux satellite n'est connecté par ce module.", inputs:["Zone à observer","Période souhaitée","Objectif de la demande"]},
    {id:"cyber", name:"Cybersécurité", role:"Consigner un incident ou un risque informatique à examiner.", inputs:["Système concerné","Niveau de priorité","Description de l'incident"]},
    {id:"memoire", name:"Mémoire territoriale", role:"Archiver des faits, décisions et références pour consultation ultérieure.", inputs:["Lieu / sujet","Référence / date","Note à archiver"]},
    {id:"surveillance", name:"Surveillance territoriale", role:"Centraliser une observation de terrain. Les caméras et capteurs doivent être connectés séparément.", inputs:["Zone / équipement","Type d'observation","Description"]},
    {id:"drones", name:"Drones", role:"Préparer une mission ou signaler un besoin de contrôle. Aucun drone n'est piloté ici.", inputs:["Zone de mission","Objectif","Autorisation / remarques"]},
    {id:"maritime", name:"Surveillance maritime", role:"Consigner un signalement maritime à vérifier.", inputs:["Zone maritime","Type de signalement","Détails"]},
    {id:"analyse", name:"Analyse des données", role:"Formuler une question et enregistrer une demande d'analyse.", inputs:["Jeu de données / source","Question d'analyse","Résultat ou hypothèse à vérifier"]},
    {id:"alertes", name:"Alertes et anomalies", role:"Créer une alerte et la transmettre à la file de l'avatar central.", inputs:["Titre de l'alerte","Priorité","Lieu et description"]},
    {id:"rapports", name:"Rapports", role:"Préparer une note de rapport à partir d'informations saisies.", inputs:["Titre du rapport","Période / zone","Résumé des faits"]},
    {id:"meteo", name:"Météo", role:"Noter une demande météo. Les prévisions réelles nécessitent un fournisseur météo connecté.", inputs:["Lieu","Période","Observation / besoin"]}
  ];
  const storeKey = "g360_addon_records_v1";
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const load = () => { try { return JSON.parse(localStorage.getItem(storeKey) || "[]"); } catch { return []; } };
  const save = rows => { try { localStorage.setItem(storeKey, JSON.stringify(rows.slice(-300))); } catch {} };
  const style = document.createElement("style");
  style.textContent = `
  #g360-addon-launch{position:fixed;right:14px;bottom:18px;z-index:9998;border:1px solid #48d8b1;border-radius:999px;background:#073a38;color:#fff;padding:12px 16px;font-weight:700;box-shadow:0 5px 22px #0006}
  #g360-addon{position:fixed;inset:0;z-index:9999;background:#07121cf2;color:#e8f2f7;font:14px/1.45 system-ui,sans-serif;display:none;overflow:auto;padding:14px;box-sizing:border-box}
  #g360-addon *{box-sizing:border-box} #g360-addon .g360-wrap{max-width:900px;margin:0 auto}
  #g360-addon .g360-top{display:flex;align-items:center;justify-content:space-between;gap:10px;position:sticky;top:-14px;background:#07121c;padding:12px 0;border-bottom:1px solid #29404e}
  #g360-addon h2,#g360-addon h3{margin:8px 0} #g360-addon p{color:#b7c9d4}
  #g360-addon button,#g360-addon input,#g360-addon select,#g360-addon textarea{font:inherit}
  #g360-addon button{cursor:pointer;border:1px solid #355565;background:#123044;color:#f4fbff;border-radius:9px;padding:9px 12px}
  #g360-addon .g360-primary{background:#087b68;border-color:#35d2ad} #g360-addon .g360-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:9px;margin:12px 0}
  #g360-addon .g360-mod{min-height:76px;text-align:left} #g360-addon .g360-mod strong{display:block}
  #g360-addon .g360-card{border:1px solid #294554;border-radius:12px;padding:13px;margin:12px 0;background:#0b1e2a}
  #g360-addon label{display:block;margin:10px 0 5px;color:#c8d9e1}
  #g360-addon input,#g360-addon select,#g360-addon textarea{width:100%;border:1px solid #355565;border-radius:8px;background:#071721;color:#fff;padding:10px}
  #g360-addon textarea{min-height:82px} #g360-addon .g360-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
  #g360-addon .g360-note{font-size:12px;color:#a8c1cc} #g360-addon .g360-record{border-top:1px solid #294554;padding:10px 0}
  #g360-addon .g360-pill{display:inline-block;border-radius:99px;padding:2px 8px;background:#173c4a;color:#9de8d6;font-size:12px}
  `;
  document.head.appendChild(style);

  const launcher = document.createElement("button");
  launcher.id = "g360-addon-launch";
  launcher.type = "button";
  launcher.textContent = "＋ Modules IA";
  launcher.setAttribute("aria-label", "Ouvrir les modules additionnels GABON 360 AI");

  const root = document.createElement("section");
  root.id = "g360-addon";
  root.setAttribute("role", "dialog");
  root.setAttribute("aria-modal", "true");
  root.setAttribute("aria-label", "Modules additionnels GABON 360 AI");
  root.innerHTML = `<div class="g360-wrap">
    <div class="g360-top"><div><strong>GABON 360 AI</strong><div class="g360-note">Modules additionnels — mode local</div></div><button type="button" id="g360-close">Fermer ✕</button></div>
    <div id="g360-home">
      <div class="g360-card"><h2>Console des modules</h2><p>Choisis un module pour saisir une observation, préparer une demande ou créer une alerte. Les données sont enregistrées dans ce navigateur.</p><span class="g360-pill">Pas de flux externe simulé</span></div>
      <div class="g360-grid" id="g360-modules"></div>
      <div class="g360-card"><h3>Relais vers l’avatar central</h3><p>Les nouvelles alertes locales apparaissent ici. La voix ne démarre qu’après une action de l’utilisateur, selon les règles du navigateur.</p><div class="g360-row"><button class="g360-primary" type="button" id="g360-enable-voice">Activer / tester la voix</button><button type="button" id="g360-speak-next">Faire lire la prochaine alerte</button></div><div id="g360-queue"></div></div>
      <div class="g360-card"><h3>Historique local</h3><div id="g360-history"></div><div class="g360-row"><button type="button" id="g360-export">Exporter les données JSON</button><button type="button" id="g360-clear">Effacer l’historique local</button></div></div>
    </div>
    <div id="g360-form-area" hidden></div>
    <p class="g360-note">Limites : ce module ne se connecte pas à des satellites, caméras, drones, API ou base de données distante. Pour un service réel, il faudra brancher les connecteurs autorisés côté serveur.</p>
  </div>`;
  document.body.appendChild(launcher);
  document.body.appendChild(root);

  let activeModule = null;
  let voiceReady = false;
  let queue = [];
  const home = root.querySelector("#g360-home");
  const formArea = root.querySelector("#g360-form-area");
  const modulesBox = root.querySelector("#g360-modules");

  modulesBox.innerHTML = modules.map(m => `<button class="g360-mod" type="button" data-mod="${m.id}"><strong>${esc(m.name)}</strong><span class="g360-note">${esc(m.role)}</span></button>`).join("");

  function openPanel(){ root.style.display = "block"; renderHistory(); renderQueue(); }
  function closePanel(){ root.style.display = "none"; }
  launcher.addEventListener("click", openPanel);
  root.querySelector("#g360-close").addEventListener("click", closePanel);
  root.addEventListener("keydown", e => { if (e.key === "Escape") closePanel(); });
  modulesBox.addEventListener("click", e => {
    const b = e.target.closest("[data-mod]"); if (!b) return;
    activeModule = modules.find(m => m.id === b.dataset.mod);
    showForm(activeModule);
  });

  function showForm(m) {
    home.hidden = true; formArea.hidden = false;
    formArea.innerHTML = `<div class="g360-card"><button type="button" id="g360-back">← Retour aux modules</button><h2>${esc(m.name)}</h2><p>${esc(m.role)}</p>
      <form id="g360-entry"><label>Titre / référence</label><input name="title" required maxlength="160" placeholder="Donne un titre clair">
      <label>Priorité</label><select name="priority"><option value="information">Information</option><option value="normale">Normale</option><option value="élevée">Élevée</option><option value="critique">Critique</option></select>
      ${m.inputs.map((v,i)=>`<label>${esc(v)}</label><textarea name="field${i}" ${i===m.inputs.length-1?"required":""} maxlength="4000" placeholder="${esc(v)}"></textarea>`).join("")}
      <div class="g360-row"><button class="g360-primary" type="submit">Enregistrer ${m.id==="alertes"?"et transmettre l’alerte":"la fiche"}</button><button type="button" id="g360-cancel">Annuler</button></div></form></div>`;
    formArea.querySelector("#g360-back").addEventListener("click", backHome);
    formArea.querySelector("#g360-cancel").addEventListener("click", backHome);
    formArea.querySelector("#g360-entry").addEventListener("submit", e => {
      e.preventDefault();
      const data = new FormData(e.currentTarget);
      const record = {id: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now())+Math.random()), module:m.id, moduleName:m.name, title:String(data.get("title")).trim(), priority:String(data.get("priority")), fields:m.inputs.map((label,i)=>({label,value:String(data.get("field"+i)||"").trim()})), createdAt:new Date().toISOString(), status:"nouveau"};
      const rows = load(); rows.push(record); save(rows);
      if (m.id === "alertes" || record.priority === "critique" || record.priority === "élevée") {
        queue.push(record); window.dispatchEvent(new CustomEvent("g360:central-alert", {detail:record}));
        renderQueue();
      }
      backHome(); renderHistory();
      const msg = m.id === "alertes" ? "Alerte enregistrée et ajoutée à la file locale de l’avatar central." : "Fiche enregistrée localement.";
      alert(msg);
    });
  }
  function backHome(){ activeModule=null; formArea.hidden=true; formArea.innerHTML=""; home.hidden=false; renderHistory(); renderQueue(); }
  function recordSummary(r) { return `${r.moduleName} — ${r.title}. Priorité : ${r.priority}. ${r.fields.map(f=>f.label+": "+f.value).join(". ")}`; }
  function renderQueue() {
    const box = root.querySelector("#g360-queue");
    box.innerHTML = queue.length ? queue.map((r,i)=>`<div class="g360-record"><strong>${esc(r.title)}</strong> <span class="g360-pill">${esc(r.priority)}</span><div class="g360-note">${esc(r.moduleName)} · ${new Date(r.createdAt).toLocaleString()}</div><div class="g360-row"><button type="button" data-speak="${i}">Lire cette alerte</button><button type="button" data-done="${i}">Marquer traitée</button></div></div>`).join("") : '<p class="g360-note">Aucune alerte en attente.</p>';
    box.querySelectorAll("[data-speak]").forEach(b=>b.addEventListener("click",()=>speakRecord(queue[Number(b.dataset.speak)])));
    box.querySelectorAll("[data-done]").forEach(b=>b.addEventListener("click",()=>{queue.splice(Number(b.dataset.done),1);renderQueue();}));
  }
  function renderHistory() {
    const box = root.querySelector("#g360-history"); const rows = load().slice().reverse().slice(0,15);
    box.innerHTML = rows.length ? rows.map(r=>`<div class="g360-record"><strong>${esc(r.title)}</strong> <span class="g360-pill">${esc(r.priority)}</span><div class="g360-note">${esc(r.moduleName)} · ${new Date(r.createdAt).toLocaleString()}</div><div>${esc(r.fields.map(f=>f.value).filter(Boolean).join(" · ").slice(0,260))}</div></div>`).join("") : '<p class="g360-note">Aucune fiche enregistrée.</p>';
  }
  function speakRecord(r) {
    if (!r) return;
    const text = recordSummary(r);
    if (!("speechSynthesis" in window)) { alert("La synthèse vocale n’est pas disponible dans ce navigateur."); return; }
    const u = new SpeechSynthesisUtterance("Alerte du centre GABON 360 AI. " + text);
    u.lang = "fr-FR"; u.rate = 0.94; window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
  }
  root.querySelector("#g360-enable-voice").addEventListener("click", () => {
    voiceReady = true;
    if ("speechSynthesis" in window) {
      const u = new SpeechSynthesisUtterance("Voix de GABON 360 AI activée pour les alertes locales.");
      u.lang="fr-FR"; window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
    } else alert("La synthèse vocale n’est pas disponible dans ce navigateur.");
  });
  root.querySelector("#g360-speak-next").addEventListener("click", () => speakRecord(queue[0]));
  root.querySelector("#g360-export").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(load(),null,2)], {type:"application/json"});
    const url = URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download="gabon360-modules-local.json"; a.click(); URL.revokeObjectURL(url);
  });
  root.querySelector("#g360-clear").addEventListener("click", () => {
    if (confirm("Effacer toutes les fiches locales enregistrées par ce module ? Cette action est irréversible.")) { save([]); queue=[]; renderHistory(); renderQueue(); }
  });
  window.addEventListener("g360:central-alert", e => {
    // Point de relais documenté pour que l'avatar existant puisse s'abonner sans être remplacé.
    // La lecture automatique n'est pas forcée : Chrome exige souvent une interaction préalable.
    const r=e.detail;
    window.dispatchEvent(new CustomEvent("g360:avatar-message", {detail:{source:"modules-addon", priority:r.priority, text:recordSummary(r), record:r}}));
  });
})();
