/* GABON 360 AI — navigation GPS hors réseau
 * Le GPS reçoit la position des satellites sans Internet. La carte elle-même doit être préchargée.
 */
(() => {
  "use strict";
  if (window.__G360_OFFLINE_NAV__) return;
  window.__G360_OFFLINE_NAV__ = true;
  const state = { running:false, points:[] };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  function build() {
    if (document.getElementById("g360-offline-nav")) return;
    const root = document.createElement("section");
    root.id = "g360-offline-nav";
    root.style.cssText = "margin:12px;padding:14px;border:1px solid #2d684c;border-radius:14px;background:#0b1b19;color:#e8f5ee";
    root.innerHTML = '<h2 style="margin:0 0 6px">Navigation forêt — GPS satellite</h2><p style="margin:0 0 10px;font-size:13px">Position GPS sans Wi-Fi ni réseau mobile. Les cartes et itinéraires doivent être téléchargés à l’avance pour être consultables hors ligne.</p><div id="g360-gps-status" role="status">GPS non démarré</div><div id="g360-gps-coords" style="font-size:20px;font-weight:700;margin:10px 0">Latitude : —<br>Longitude : —</div><div id="g360-gps-details" style="font-size:13px">Précision : — · Vitesse : —</div><div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0"><button id="g360-gps-start" type="button">Démarrer le GPS</button><button id="g360-gps-stop" type="button">Arrêter</button><button id="g360-gps-mark" type="button">Enregistrer un point</button><button id="g360-gps-export" type="button">Exporter la trace</button></div><p id="g360-gps-count">0 point enregistré sur cet appareil.</p><div id="g360-gps-list" style="font-size:12px;max-height:140px;overflow:auto"></div>';
    const first = document.querySelector("header");
    if (first && first.parentNode) first.insertAdjacentElement("afterend", root);
    else document.body.insertBefore(root, document.body.firstChild);
    const saved = localStorage.getItem("g360_offline_gps_points");
    if (saved) { try { state.points = JSON.parse(saved); } catch (_) {} }
    root.querySelector("#g360-gps-start").addEventListener("click", () => {
      state.running = true;
      if (window.AndroidGPS && typeof AndroidGPS.start === "function") AndroidGPS.start();
      else status(false, "Cette version Android ne fournit pas encore le pont GPS natif. Reconstruire l’APK avec AndroidGPS.");
    });
    root.querySelector("#g360-gps-stop").addEventListener("click", () => {
      state.running = false;
      if (window.AndroidGPS && typeof AndroidGPS.stop === "function") AndroidGPS.stop();
      status(false, "Suivi arrêté");
    });
    root.querySelector("#g360-gps-mark").addEventListener("click", () => {
      if (!state.last) { status(false, "Attends d’obtenir une position GPS avant d’enregistrer."); return; }
      state.points.push({...state.last, markedAt:new Date().toISOString()});
      try { localStorage.setItem("g360_offline_gps_points", JSON.stringify(state.points)); } catch (_) {}
      renderPoints();
      status(true, "Point enregistré localement sur le téléphone.");
    });
    root.querySelector("#g360-gps-export").addEventListener("click", () => {
      const data = JSON.stringify({format:"GABON 360 AI GPS track",points:state.points},null,2);
      const blob = new Blob([data],{type:"application/json"});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a"); a.href=url; a.download="gabon360-trace-gps.json"; a.click();
      setTimeout(()=>URL.revokeObjectURL(url),1000);
    });
    renderPoints();
  }
  function status(ok, message) {
    const el = document.getElementById("g360-gps-status");
    if (el) { el.textContent = (ok ? "● " : "○ ") + message; el.style.color = ok ? "#80e5a8" : "#ffd27a"; }
  }
  function renderPoints() {
    const c=document.getElementById("g360-gps-count"), l=document.getElementById("g360-gps-list");
    if(c)c.textContent=state.points.length+" point(s) enregistré(s) localement.";
    if(l)l.textContent=state.points.slice(-5).map((p,i)=> (state.points.length-Math.min(5,state.points.length)+i+1)+". "+Number(p.lat).toFixed(6)+", "+Number(p.lon).toFixed(6)).join(" · ");
  }
  window.addEventListener("g360:gps-status", e => { if(e.detail) status(!!e.detail.ok,e.detail.message||"État GPS inconnu"); });
  window.addEventListener("g360:gps-fix", e => {
    const d=e.detail||{}; if(typeof d.lat!=="number"||typeof d.lon!=="number")return;
    state.last={lat:d.lat,lon:d.lon,accuracy:d.accuracy||null,speed:d.speed||0,altitude:d.altitude||null,time:d.time||Date.now()};
    const coords=document.getElementById("g360-gps-coords"), details=document.getElementById("g360-gps-details");
    if(coords)coords.innerHTML="Latitude : "+d.lat.toFixed(6)+"<br>Longitude : "+d.lon.toFixed(6);
    if(details)details.textContent="Précision : "+(d.accuracy==null?"—":Math.round(d.accuracy)+" m")+" · Vitesse : "+(d.speed==null?"—":(d.speed*3.6).toFixed(1)+" km/h")+" · Altitude : "+(d.altitude==null?"—":Math.round(d.altitude)+" m");
    status(true,"Position GPS satellite reçue"+(state.running?" — suivi actif":""));
  });
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",build); else build();
})();
