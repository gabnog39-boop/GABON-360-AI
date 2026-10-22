/* GABON 360 AI — extensions des pages du centre de contrôle.
   Les formulaires enregistrent les fiches localement sur l'appareil. Les flux réels
   (satellite, météo, drones, frontières, aérien, paiements) nécessitent leurs API.
*/
(() => {
  "use strict";
  const modules = [
    ["satellites","Satellites","Imagerie et demandes d'observation",["Zone / coordonnées","Période","Objectif","Source ou référence"]],
    ["drones","Drones","Préparation et suivi administratif des missions",["Zone de mission","Objectif","Autorisation / opérateur","Référence de mission"]],
    ["navigation","Navigation terrain","Itinéraires, risques et points de passage",["Départ / coordonnées","Destination / coordonnées","Risques et consignes","Référence de mission"]],
    ["geoloc","Géolocalisation","Position et relevés GPS",["Lieu / secteur","Latitude","Longitude","Précision GPS (m)"]],
    ["cyber","Cybersécurité","Registre des incidents et contrôles",["Système concerné","Priorité","Type d'incident","Description / mesures"]],
    ["memoire","Mémoire territoriale","Archivage et recherche de faits de terrain",["Lieu / sujet","Date / référence","Catégorie","Note / source"]],
    ["stats","Statistiques","Indicateurs issus des fiches enregistrées",["Indicateur","Valeur","Période","Commentaire"]],
    ["meteo","Météo et risques","Consignation des conditions et risques météo",["Zone","Conditions observées","Risque","Heure / source"]],
    ["eaux","Eaux et océan","Observations des cours d'eau et du littoral",["Cours d'eau / zone côtière","Coordonnées","Niveau / état","Observation"]],
    ["frontieres","Frontières nationales","Signalements et contrôles de secteurs frontaliers",["Secteur / poste","Coordonnées","Type de signalement","Compte rendu"]],
    ["air","Espace aérien","Registre de signalements aériens",["Zone / coordonnées","Type d'objet ou événement","Heure","Source / vérification"]],
    ["centre","Centre national de situation","Synthèse des signalements et missions",["Zone / province","Situation","Niveau de priorité","Action demandée"]],
    ["admin","Administration","Journal des décisions et paramètres administratifs",["Décision / paramètre","Valeur ou référence","Responsable","Commentaire"]],
    ["paiements","Abonnements et paiements","Suivi manuel des demandes et références de paiement",["Compte / organisme","Offre demandée","Référence de paiement","Statut à vérifier"]]
  ];
  const existing = [
    ["ho","Accueil","Synthèse et accès général"],["al","Alertes","Signalements et alertes"],
    ["mp","Carte","Carte et points cartographiques"],["ms","Missions","Patrouilles et traces GPS"],
    ["pk","Parcs","Parcs nationaux"],["gx","Garmin / GPX","Import et export GPX"],
    ["rp","Rapports","Rapports et comptes rendus"],["us","Utilisateurs","Comptes et rôles"]
  ];
  const $ = s => document.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const storageKey = "g360_centre_records_v1";
  const load = () => { try { return JSON.parse(localStorage.getItem(storageKey) || "[]"); } catch (_) { return []; } };
  const save = rows => { try { localStorage.setItem(storageKey, JSON.stringify(rows)); return true; } catch (_) { return false; } };
  function announce(text, id) {
    window.dispatchEvent(new CustomEvent("g360:avatar-message", {detail:{source:id || "centre-controle", text}}));
  }
  function showPage(id) {
    document.querySelectorAll("#app > .g360-extra-page").forEach(el => el.classList.toggle("hide", el.id !== "g360-page-"+id));
    document.querySelectorAll("#app > .tabs button[data-g360-tab]").forEach(el => el.classList.toggle("on", el.dataset.g360Tab === id));
    document.querySelectorAll("#app > div[id^='v-']").forEach(el => el.classList.add("hide"));
    document.querySelectorAll("#app > .tabs button[id^='t-']").forEach(el => el.classList.remove("on"));
    const legacy = document.getElementById("v-"+id);
    if (legacy) legacy.classList.remove("hide");
    const legacyTab = document.getElementById("t-"+id);
    if (legacyTab) legacyTab.classList.add("on");
    if (id === "centre") renderSummary();
    if (id === "stats") renderStats();
    if (id === "memoire") renderRecords("memoire");
  }
  function renderRecords(id) {
    const out = document.getElementById("g360-records-"+id); if (!out) return;
    const rows = load().filter(x => x.module === id).slice().reverse().slice(0,30);
    out.innerHTML = rows.length ? rows.map(x => '<article class="card"><b>'+esc(x.title || x.moduleName)+'</b><div class="note">'+esc(new Date(x.createdAt).toLocaleString("fr-FR"))+' · '+esc(x.status)+'</div><p>'+esc(x.values.filter(Boolean).join(" · "))+'</p></article>').join("") : '<p class="note">Aucune fiche enregistrée sur cet appareil.</p>';
  }
  function renderSummary() {
    const el = document.getElementById("g360-summary-centre"); if (!el) return;
    const rows = load(); const counts = {};
    rows.forEach(x => counts[x.moduleName] = (counts[x.moduleName] || 0) + 1);
    el.innerHTML = '<p><b>'+rows.length+'</b> fiche(s) locale(s) enregistrée(s).</p><p class="note">Ce tableau ne représente pas des flux nationaux en direct. Les données ne deviennent partagées qu'après connexion d'un serveur.</p>'+
      (Object.keys(counts).length ? '<ul>'+Object.entries(counts).map(([k,v])=>'<li>'+esc(k)+': '+v+'</li>').join("")+'</ul>' : '<p>Aucune fiche locale pour le moment.</p>');
  }
  function renderStats() {
    const el = document.getElementById("g360-stats-data"); if (!el) return;
    const rows=load(), by={}; rows.forEach(x=>by[x.moduleName]=(by[x.moduleName]||0)+1);
    el.innerHTML='<p><b>'+rows.length+'</b> fiches locales au total</p>'+(Object.keys(by).length?'<ul>'+Object.entries(by).map(([k,v])=>'<li>'+esc(k)+': '+v+'</li>').join("")+'</ul>':'<p>Aucune donnée à compter.</p>');
  }
  function createPage(m) {
    const [id,name,desc,fields] = m;
    const sec=document.createElement("section"); sec.id="g360-page-"+id; sec.className="g360-extra-page card hide"; sec.setAttribute("data-ia",id);
    sec.innerHTML='<h2>'+esc(name)+'</h2><p>'+esc(desc)+'</p><p class="note">Mode local : les fiches sont enregistrées sur ce téléphone. Une connexion à des sources externes est nécessaire pour les données en direct.</p>'+
      '<form id="g360-form-'+id+'">'+fields.map((f,i)=>'<label for="g360-'+id+'-'+i+'">'+esc(f)+'</label><input id="g360-'+id+'-'+i+'" name="f'+i+'" placeholder="'+esc(f)+'" '+(i===0?'required':'')+' />').join("")+
      '<label for="g360-status-'+id+'">Statut</label><select id="g360-status-'+id+'"><option>À vérifier</option><option>En cours</option><option>Traité</option><option>Archivé</option></select><button class="p" type="submit">Enregistrer la fiche</button></form>'+
      '<div class="row"><button type="button" id="g360-export-'+id+'">Exporter les fiches</button><button type="button" id="g360-ask-'+id+'">Consulter l’IA de la page</button></div><h3>Historique local</h3><div id="g360-records-'+id+'"></div>';
    $("#app").appendChild(sec);
    const form=sec.querySelector("form");
    form.addEventListener("submit", e=>{
      e.preventDefault();
      const values=fields.map((_,i)=>sec.querySelector('[name="f'+i+'"]').value.trim());
      if (!values[0]) { alert("Renseigne au moins le premier champ."); return; }
      const rows=load(); rows.push({id:Date.now()+"-"+Math.random().toString(36).slice(2,8),module:id,moduleName:name,title:values[0],values,status:sec.querySelector("select").value,createdAt:new Date().toISOString()});
      if (!save(rows)) { alert("Stockage local indisponible : aucune fiche n'a été enregistrée."); return; }
      form.reset(); renderRecords(id); renderSummary(); renderStats(); announce("Nouvelle fiche enregistrée dans "+name+". "+values.filter(Boolean).join(". "),id);
    });
    sec.querySelector("#g360-export-"+id).addEventListener("click",()=>{
      const rows=load().filter(x=>x.module===id); const blob=new Blob([JSON.stringify(rows,null,2)],{type:"application/json"});
      const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="gabon360-"+id+"-fiches.json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    });
    sec.querySelector("#g360-ask-"+id).addEventListener("click",()=>{
      const rows=load().filter(x=>x.module===id);
      const text=name+" — "+rows.length+" fiche(s) locale(s). "+(rows.length?("Dernière fiche : "+rows[rows.length-1].values.filter(Boolean).join(", ")+"."):"Aucune fiche enregistrée pour le moment.")+" Les connexions aux données en direct doivent encore être configurées si elles ne sont pas disponibles.";
      if(window.G360_IA && window.G360_IA.avatar) window.G360_IA.avatar.deliver(window.G360_IA.agents.find(a=>a.id===id)||{id,page:name},text,"local");
      else announce(text,id);
    });
  }
  function init() {
    const app=$("#app"), tabs=app && app.querySelector(".tabs"); if(!app||!tabs) return;
    modules.forEach(m=>{
      if(!document.getElementById("g360-page-"+m[0])) createPage(m);
      if(!tabs.querySelector('[data-g360-tab="'+m[0]+'"]')){
        const b=document.createElement("button");b.type="button";b.dataset.g360Tab=m[0];b.textContent=m[1];b.addEventListener("click",()=>showPage(m[0]));tabs.insertBefore(b,tabs.querySelector("#out2"));
      }
      renderRecords(m[0]);
    });
    const iaForLegacy={ho:"accueil",al:"alertes",mp:"carte",ms:"missions",pk:"parcs",gx:"garmin",rp:"rapports",us:"users"};
    existing.forEach(([id,label])=>{
      const b=document.getElementById("t-"+id); if(b){b.classList.remove("hide");b.dataset.g360Tab=id;b.addEventListener("click",()=>showPage(id));}
      const page=document.getElementById("v-"+id); if(page && iaForLegacy[id]) page.setAttribute("data-ia",iaForLegacy[id]);
    });
    const home=document.getElementById("v-ho");
    if(home && !document.getElementById("g360-all-modules")){
      const box=document.createElement("div");box.id="g360-all-modules";box.className="card";
      box.innerHTML='<h2>Centre de contrôle — tous les modules</h2><p class="note">Accès direct aux pages disponibles.</p><div class="row" style="flex-wrap:wrap">'+existing.concat(modules.map(m=>[m[0],m[1]])).map(([id,label])=>'<button type="button" data-g360-open="'+esc(id)+'">'+esc(label)+'</button>').join("")+'</div>';
      home.appendChild(box);box.querySelectorAll("[data-g360-open]").forEach(b=>b.addEventListener("click",()=>showPage(b.dataset.g360Open)));
    }
    renderSummary();renderStats();
    if(window.G360_IA && typeof window.G360_IA.mount==="function") window.G360_IA.mount();
  }
  window.G360_CENTRE={modules,showPage,loadRecords:load,announce};
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",init); else init();
  window.addEventListener("g360:avatar-message", e=>{if(e.detail && e.detail.source==="modules-addon") return;});
})();