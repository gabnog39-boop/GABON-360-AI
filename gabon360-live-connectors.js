/* GABON 360 AI — connecteurs vérifiables : météo publique + accès imagerie satellite.
   La météo utilise Open-Meteo (internet requis). Les images satellites ne sont pas de la vidéo live :
   NASA GIBS/Worldview fournit des couches d'imagerie avec délais de disponibilité variables.
*/
(() => {
  "use strict";
  if (window.__G360_LIVE_CONNECTORS__) return;
  window.__G360_LIVE_CONNECTORS__ = true;
  const $ = (id) => document.getElementById(id);
  const live = window.G360_LIVE = {
    weather: null, weatherStatus: "non vérifiée",
    contextFor(id) {
      const parts = [];
      if (id === "meteo" || id === "accueil" || id === "centre" || id === "alertes" || id === "stats") {
        if (this.weather) parts.push("MÉTÉO ACTUELLE (Open-Meteo, relevée à "+this.weather.time+"): "+this.weather.summary+". Température "+this.weather.temp+" °C; vent "+this.weather.wind+" km/h; précipitations "+this.weather.rain+" mm.");
        else parts.push("Météo en direct non disponible dans cette session : "+this.weatherStatus+".");
      }
      if (id === "satellites") parts.push("IMAGERIE SATELLITE : accès au visualiseur NASA GIBS/Worldview. Ce n'est pas une vidéo satellite en direct; la fraîcheur varie selon la couche et le satellite. Vérifier l'heure d'acquisition affichée par le fournisseur.");
      return parts.join("\n");
    }
  };
  const style = document.createElement("style");
  style.textContent = ".g360-live-card{margin:12px;padding:14px;border:1px solid #31516b;border-radius:12px;background:#0b1724;color:#e7f2fc}.g360-live-card a{color:#8ed0ff}.g360-live-card button{padding:8px 12px;margin:5px 5px 5px 0;border-radius:8px;border:0;background:#087e55;color:white}.g360-live-muted{font-size:12px;color:#a8bfd2}";
  document.head.appendChild(style);
  function addCard(parent, id, title, html) {
    if (!parent || parent.querySelector(":scope > .g360-live-card[data-live-card='"+id+"']")) return;
    const card=document.createElement("section"); card.className="g360-live-card"; card.dataset.liveCard=id;
    card.innerHTML="<h3>"+title+"</h3>"+html; parent.appendChild(card);
  }
  function findPage(ids) { for (const id of ids) { const el=document.getElementById(id); if(el)return el; } return null; }
  function weatherCard() {
    const page=findPage(["g360-page-meteo","meteo","weather"]);
    if (!page) return;
    addCard(page,"weather","Météo — données publiques en direct",
      '<p id="g360-weather-status">En attente de la connexion météo…</p><div id="g360-weather-data">Aucune donnée reçue.</div><button type="button" id="g360-weather-refresh">Actualiser la météo</button><p class="g360-live-muted">Source : Open-Meteo. Internet requis. Position par défaut : Libreville; si le GPS est actif, la position du téléphone est utilisée.</p>');
    const btn=$("g360-weather-refresh"); if(btn && !btn.dataset.bound){btn.dataset.bound="1";btn.addEventListener("click",()=>fetchWeather(true));}
  }
  function statusCards() {
    const agents = window.G360_IA && Array.isArray(window.G360_IA.agents) ? window.G360_IA.agents : [];
    const pages = Array.from(document.querySelectorAll("#app > section[data-ia], #app > div[data-ia]"));
    pages.forEach(page => {
      const id = page.getAttribute("data-ia");
      const agent = agents.find(a => a.id === id);
      if (!agent || page.dataset.g360StatusAdded === "1") return;
      page.dataset.g360StatusAdded = "1";
      const card = document.createElement("section"); card.className = "g360-live-card"; card.dataset.liveCard = "module-status-" + id;
      const heading = document.createElement("h3"); heading.textContent = "État de connexion — " + agent.page;
      const ai = document.createElement("p"); ai.className = "g360-module-ai-status"; ai.textContent = "IA de page : noyau central détecté; réponse à tester.";
      const ds = document.createElement("p"); ds.className = "g360-module-data-status"; ds.textContent = "Sources externes : état non vérifié.";
      const btn = document.createElement("button"); btn.type = "button"; btn.textContent = "Consulter cette IA par l’avatar central";
      btn.addEventListener("click", () => { if (window.G360_IA && window.G360_IA.avatar) window.G360_IA.avatar.ask(id); else ai.textContent = "Noyau IA non chargé : réponse indisponible."; });
      card.append(heading, ai, ds, btn); page.appendChild(card);
    });
    pages.forEach(page => {
      const card = page.querySelector("[data-live-card^=module-status-]"); if (!card) return;
      const data = card.querySelector(".g360-module-data-status"); const id = page.getAttribute("data-ia");
      let msg = "Sources externes : non vérifiées ou non connectées.";
      if (id === "meteo") msg = live.weather ? "Météo publique connectée; dernière mesure " + live.weather.time + "." : "Météo publique : " + live.weatherStatus + ".";
      if (id === "satellites") msg = "Visualiseur NASA Worldview accessible; aucune vidéo satellite continue en direct n’est connectée.";
      if (["navigation","geoloc","garmin"].includes(id)) msg = window.__G360_LAST_GPS__ ? "GPS du téléphone : dernière position reçue; carte hors ligne à vérifier." : "GPS : aucune position reçue dans cette session.";
      if (id === "drones") msg = "Aucun flux de drone connecté dans cette version.";
      if (id === "frontieres") msg = "Aucun flux automatique de capteurs ou de postes frontaliers connecté.";
      if (id === "air") msg = "Aucun radar ou flux ADS-B connecté dans cette version.";
      if (id === "paiements") msg = "Aucune passerelle de paiement en direct configurée.";
      if (data) data.textContent = msg;
    });
  }
  function satelliteCard() {
    const page=findPage(["g360-page-satellites","satellites"]);
    if (!page) return;
    addCard(page,"satellite","Imagerie satellite — fournisseur réel",
      '<p>Le visualiseur public NASA GIBS / Worldview donne accès aux couches d’imagerie disponibles, avec l’heure d’acquisition indiquée par le fournisseur.</p><p class="g360-live-muted">Important : les satellites d’observation ne fournissent pas une vidéo continue en direct. Les images ont un délai de traitement et de revisite; l’accès à certaines images haute résolution exige un fournisseur et des identifiants.</p><p><a href="https://worldview.earthdata.nasa.gov/" target="_blank" rel="noopener">Ouvrir NASA Worldview</a> · <a href="https://www.earthdata.nasa.gov/learn/find-data/near-real-time" target="_blank" rel="noopener">Données satellites quasi temps réel</a></p><p id="g360-satellite-status">Accès externe disponible; aucun flux vidéo privé connecté.</p>');
  }
  async function fetchWeather(announce) {
    const status=$("g360-weather-status"), data=$("g360-weather-data");
    live.weatherStatus="requête en cours";
    if(status)status.textContent="Récupération des observations météo…";
    try {
      let lat=0.3901, lon=9.4544, place="Libreville";
      if (window.__G360_LAST_GPS__ && Number.isFinite(window.__G360_LAST_GPS__.lat) && Number.isFinite(window.__G360_LAST_GPS__.lon)) {
        lat=window.__G360_LAST_GPS__.lat; lon=window.__G360_LAST_GPS__.lon; place="position GPS";
      }
      const url="https://api.open-meteo.com/v1/forecast?latitude="+encodeURIComponent(lat)+"&longitude="+encodeURIComponent(lon)+"&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m&timezone=auto";
      const res=await fetch(url,{cache:"no-store"}); if(!res.ok)throw new Error("HTTP "+res.status);
      const j=await res.json(), c=j.current; if(!c)throw new Error("Aucune observation actuelle");
      const labels={0:"ciel dégagé",1:"principalement dégagé",2:"partiellement nuageux",3:"couvert",45:"brouillard",48:"brouillard givrant",51:"bruine légère",53:"bruine modérée",55:"bruine forte",61:"pluie faible",63:"pluie modérée",65:"pluie forte",71:"neige faible",73:"neige modérée",75:"neige forte",80:"averses faibles",81:"averses modérées",82:"averses fortes",95:"orage",96:"orage avec grêle faible",99:"orage avec grêle forte"};
      live.weather={place,time:c.time,temp:c.temperature_2m,feels:c.apparent_temperature,humidity:c.relative_humidity_2m,wind:c.wind_speed_10m,rain:c.precipitation,summary:labels[c.weather_code]||("code météo "+c.weather_code)};
      live.weatherStatus="actualisée";
      const html="<p><b>"+live.weather.place+"</b> — "+live.weather.summary+"</p><p>Température : <b>"+c.temperature_2m+" °C</b> (ressenti "+c.apparent_temperature+" °C)</p><p>Humidité : "+c.relative_humidity_2m+" % · Vent : "+c.wind_speed_10m+" km/h · Précipitations : "+c.precipitation+" mm</p><p class='g360-live-muted'>Heure de mesure : "+c.time+" · Source Open-Meteo</p>";
      if(data)data.innerHTML=html; if(status)status.textContent="Connexion météo réussie.";
      if(announce && window.G360_IA && window.G360_IA.avatar) {
        const agent=window.G360_IA.agents.find(a=>a.id==="meteo");
        if(agent)window.G360_IA.avatar.deliver(agent,"Météo actualisée pour "+place+" : "+live.weather.summary+", "+c.temperature_2m+" °C, vent "+c.wind_speed_10m+" km/h, précipitations "+c.precipitation+" mm. Mesure à "+c.time+".","live");
      }
      if(c.weather_code>=95 && window.G360_IA && window.G360_IA.avatar && !live.lastStormAlert) {
        live.lastStormAlert=true; const agent=window.G360_IA.agents.find(a=>a.id==="meteo");
        if(agent)window.G360_IA.avatar.deliver(agent,"Alerte météo automatique : un code d'orage est signalé pour "+place+". Conditions à vérifier auprès des services officiels. Mesure à "+c.time+".","live");
      }
    } catch(e) {
      live.weatherStatus="indisponible ("+String(e.message||e)+")";
      if(status)status.textContent="Météo non disponible. Vérifie la connexion Internet et réessaie.";
      if(data)data.textContent="Aucune donnée météo n’est inventée ni conservée comme observation en direct.";
    }
  }
  window.addEventListener("g360:gps-fix",e=>{if(e.detail){window.__G360_LAST_GPS__={lat:e.detail.lat,lon:e.detail.lon};}});
  function init() {
    // Associer toutes les pages créées dynamiquement à l'IA de leur domaine lorsqu'un agent existe.
    const aliases={satellites:"satellites",drones:"drones",navigation:"navigation",geoloc:"geoloc",cyber:"cyber",memoire:"memoire",alertes:"alertes",rapports:"rapports",stats:"stats",meteo:"meteo",parcs:"parcs",eaux:"eaux",frontieres:"frontieres",air:"air",centre:"centre",admin:"admin",users:"users",paiements:"paiements",missions:"missions",garmin:"garmin",territoire:"carte"};
    Object.entries(aliases).forEach(([page,agent])=>{const el=$("g360-page-"+page);if(el && !el.dataset.ia)el.dataset.ia=agent;});
    weatherCard(); satelliteCard(); statusCards();
    if($("g360-weather-status"))fetchWeather(false);
    if(window.G360_IA && typeof window.G360_IA.mount==="function")window.G360_IA.mount();
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
  new MutationObserver(()=>{weatherCard();satelliteCard();statusCards();if(window.G360_IA&&window.G360_IA.mount)window.G360_IA.mount();}).observe(document.body,{childList:true,subtree:true});
  window.setInterval(()=>{if($("g360-weather-status"))fetchWeather(false);},15*60*1000);
})();