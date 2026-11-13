/* GABON 360 AI — navigation GPS hors réseau
 * Le GPS reçoit la position des satellites sans Internet. La carte elle-même doit être préchargée.
 */
(() => {
  "use strict";
  if (window.__G360_OFFLINE_NAV__) return;
  window.__G360_OFFLINE_NAV__ = true;
  const MAX_POINTS = 10000;
  const state = { running:false, points:[], last:null };
  const validPoint = p => p && Number.isFinite(Number(p.lat)) && Number(p.lat) >= -90 && Number(p.lat) <= 90 &&
    Number.isFinite(Number(p.lon)) && Number(p.lon) >= -180 && Number(p.lon) <= 180;
  function savePoints() {
    state.points = state.points.slice(-MAX_POINTS);
    try { localStorage.setItem("g360_offline_gps_points", JSON.stringify(state.points)); }
    catch (_) { status(false, "Stockage local indisponible ou saturé."); }
  }
  const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  function makeGpx() {
    const points = state.points.filter(validPoint);
    if (!points.length) return null;
    const escXml = value => String(value ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&apos;");
    const waypoints = points.filter(p => p.markedAt && Number.isFinite(Date.parse(p.markedAt))).map(p =>
      '<wpt lat="'+Number(p.lat).toFixed(7)+'" lon="'+Number(p.lon).toFixed(7)+'"><time>'+escXml(new Date(p.markedAt).toISOString())+'</time><name>Point terrain</name></wpt>'
    ).join("");
    const track = points.map(p =>
      '<trkpt lat="'+Number(p.lat).toFixed(7)+'" lon="'+Number(p.lon).toFixed(7)+'">'+
      (p.altitude != null && Number.isFinite(Number(p.altitude)) ? '<ele>'+Number(p.altitude).toFixed(1)+'</ele>' : '')+
      '<time>'+escXml(new Date(Number.isFinite(Number(p.time)) && Number(p.time)>0 ? Number(p.time) : Date.now()).toISOString())+'</time></trkpt>'
    ).join("");
    return '<?xml version="1.0" encoding="UTF-8"?>'+
      '<gpx version="1.1" creator="GABON 360 AI" xmlns="http://www.topografix.com/GPX/1/1">'+
      waypoints+'<trk><name>Patrouille GABON 360 AI</name><trkseg>'+track+'</trkseg></trk></gpx>';
  }
  function build() {
    if (document.getElementById("g360-offline-nav")) return;
    const root = document.createElement("section");
    root.id = "g360-offline-nav";
    root.style.cssText = "margin:12px;padding:14px;border:1px solid #2d684c;border-radius:14px;background:#0b1b19;color:#e8f5ee";
    root.innerHTML = '<h2 style="margin:0 0 6px">Navigation forêt — GPS satellite</h2><p style="margin:0 0 10px;font-size:13px">Position GPS sans Wi-Fi ni réseau mobile. Les cartes et itinéraires doivent être téléchargés à l’avance pour être consultables hors ligne.</p><div id="g360-gps-status" role="status">GPS non démarré</div><div id="g360-gps-coords" style="font-size:20px;font-weight:700;margin:10px 0">Latitude : —<br>Longitude : —</div><div id="g360-gps-details" style="font-size:13px">Précision : — · Vitesse : —</div><div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0"><button id="g360-gps-start" type="button">Démarrer le GPS</button><button id="g360-gps-stop" type="button">Arrêter</button><button id="g360-gps-mark" type="button">Enregistrer un point</button><button id="g360-gps-export" type="button">Exporter GPX</button><button id="g360-locus-import" type="button">Transmettre GPX à Locus</button><button id="g360-locus-open" type="button">Ouvrir position dans Locus</button><button id="g360-locus-start" type="button">Démarrer trace Locus</button><button id="g360-locus-pause" type="button">Pause Locus</button><button id="g360-locus-stop" type="button">Arrêter trace Locus</button></div><p id="g360-locus-status" style="font-size:13px">Locus Map : vérification de la connexion Android…</p><p id="g360-gps-count">0 point enregistré sur cet appareil.</p><div id="g360-gps-list" style="font-size:12px;max-height:140px;overflow:auto"></div>';
    const first = document.querySelector("header");
    if (first && first.parentNode) first.insertAdjacentElement("afterend", root);
    else document.body.insertBefore(root, document.body.firstChild);
    try {
      const saved = localStorage.getItem("g360_offline_gps_points");
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) state.points = parsed.filter(validPoint).slice(-MAX_POINTS);
      }
    } catch (_) { status(false, "Impossible de relire les points GPS enregistrés."); }
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
    const locusStatus = root.querySelector("#g360-locus-status");
    const locus = window.AndroidLocus;
    if (locusStatus) locusStatus.textContent = locus && locus.isInstalled()
      ? "Locus Map détecté sur ce téléphone."
      : "Locus Map non détecté. Installe Locus Map 4 pour utiliser le lien direct.";
    root.querySelector("#g360-locus-open").addEventListener("click", () => {
      if (!state.last) { status(false, "Démarre le GPS et attends une position avant d’ouvrir Locus."); return; }
      if (!window.AndroidLocus) { status(false, "Pont Locus Android absent. Installe la nouvelle version de GABON 360 AI."); return; }
      AndroidLocus.openAt(state.last.lat, state.last.lon, "GABON 360 AI — position terrain");
    });
    root.querySelector("#g360-locus-start").addEventListener("click", () => {
      if (!window.AndroidLocus || !AndroidLocus.isInstalled()) { status(false, "Locus Map n’est pas installé ou le pont Android est absent."); return; }
      AndroidLocus.startRecording();
    });
    root.querySelector("#g360-locus-pause").addEventListener("click", () => {
      if (!window.AndroidLocus || !AndroidLocus.isInstalled()) { status(false, "Locus Map n’est pas installé."); return; }
      AndroidLocus.pauseRecording();
    });
    root.querySelector("#g360-locus-stop").addEventListener("click", () => {
      if (!window.AndroidLocus || !AndroidLocus.isInstalled()) { status(false, "Locus Map n’est pas installé."); return; }
      AndroidLocus.stopRecording();
    });
    root.querySelector("#g360-gps-mark").addEventListener("click", () => {
      if (!state.last) { status(false, "Attends d’obtenir une position GPS avant d’enregistrer."); return; }
      state.points.push({...state.last, markedAt:new Date().toISOString()});
      savePoints();
      renderPoints();
      status(true, "Point enregistré localement sur le téléphone.");
    });
    root.querySelector("#g360-gps-export").addEventListener("click", () => {
      const gpx = makeGpx();
      if (!gpx) { status(false, "Aucun point GPS valide à exporter."); return; }
      const blob = new Blob([gpx],{type:"application/gpx+xml"});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a"); a.href=url; a.download="gabon360-patrouille.gpx"; a.click();
      setTimeout(()=>URL.revokeObjectURL(url),1000);
      status(true, state.points.length+" point(s) exporté(s) au format GPX.");
    });
    root.querySelector("#g360-locus-import").addEventListener("click", () => {
      const gpx = makeGpx();
      if (!gpx) { status(false, "Aucun point GPS valide à transmettre à Locus."); return; }
      if (!window.AndroidLocus || typeof AndroidLocus.importGpx !== "function") {
        status(false, "Le partage GPX Android nécessite la nouvelle version de l’application.");
        return;
      }
      AndroidLocus.importGpx(gpx);
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
    state.last={lat:d.lat,lon:d.lon,accuracy:d.accuracy??null,speed:d.speed??0,altitude:d.altitude??null,time:d.time||Date.now()};
    if (state.running) {
      const lastPoint = state.points[state.points.length - 1];
      const elapsed = lastPoint ? state.last.time - Number(lastPoint.time || 0) : Infinity;
      if (!lastPoint || elapsed >= 5000) {
        state.points.push({...state.last});
        savePoints();
        renderPoints();
      }
    }
    const coords=document.getElementById("g360-gps-coords"), details=document.getElementById("g360-gps-details");
    if(coords)coords.innerHTML="Latitude : "+d.lat.toFixed(6)+"<br>Longitude : "+d.lon.toFixed(6);
    if(details)details.textContent="Précision : "+(d.accuracy==null?"—":Math.round(d.accuracy)+" m")+" · Vitesse : "+(d.speed==null?"—":(d.speed*3.6).toFixed(1)+" km/h")+" · Altitude : "+(d.altitude==null?"—":Math.round(d.altitude)+" m");
    status(true,"Position GPS satellite reçue"+(state.running?" — suivi actif":""));
  });
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",build); else build();
})();
