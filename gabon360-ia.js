/* GABON 360 AI — Noyau IA : une IA par page et par option, toutes reliées à l'avatar central.
   Règle : aucune IA ne parle à l'humain directement. Tout passe par l'avatar (Avatar.deliver).
   Honnêteté : mode "local" = règles + données de l'application. Une vraie IA serveur n'est
   annoncée connectée que si G360_IA.endpoint répond réellement. */
(function () {
  const AGENTS = [
    ['accueil','Accueil','Synthèse nationale','alertes,missions,observations'],
    ['carte','Carte','Couches et lieux','alertes,observations'],
    ['satellites','Satellites','Imagerie (Sentinel-2)',''],
    ['drones','Drones','Vols et vidéos',''],
    ['navigation','Navigation terrain','Itinéraires et traces','missions'],
    ['geoloc','Géolocalisation','Position GPS','missions'],
    ['cyber','Cybersécurité','Accès et journaux','profiles'],
    ['memoire','Mémoire territoriale','Historique des événements','alertes,observations,missions'],
    ['alertes','Alertes','Alertes terrain','alertes'],
    ['rapports','Rapports','Rapports et validation','rapports'],
    ['stats','Statistiques','Chiffres clés','alertes,missions,observations,rapports'],
    ['meteo','Météo','Conditions et risques',''],
    ['parcs','Parcs nationaux','13 parcs','observations'],
    ['eaux','Eaux et océan','Cours d\'eau, côte','observations'],
    ['frontieres','Frontières','Frontière nationale',''],
    ['air','Espace aérien','Surveillance aérienne',''],
    ['centre','Centre national','Situation globale','alertes,missions,rapports'],
    ['admin','Administration','Réglages propriétaire','profiles'],
    ['users','Utilisateurs','Comptes et rôles','profiles'],
    ['paiements','Paiements','Abonnements (vérifiés serveur)',''],
    ['missions','Missions','Patrouilles et GPX','missions'],
    ['garmin','Garmin / GPX','Échanges de fichiers','missions,observations']
  ].map(([id, page, role, data]) => ({ id, page, role, data: data ? data.split(',') : [] }));

  const G = (window.G360_IA = { agents: AGENTS, endpoint: null, current: null });

  // --- Données : l'application fournit window.G360.data(nom) -> tableau (sinon : rien) ---
  const read = (n) => { try { return (window.G360 && window.G360.data && window.G360.data(n)) || null; } catch (e) { return null; } };

  // --- Analyse locale d'une IA de page (pas de fausse IA : uniquement des faits comptés) ---
  function analyse(a) {
    const lines = a.data.map((n) => {
      const d = read(n);
      if (!d) return "• " + n + " : source externe non reliée.";
      const last = d[0] && (d[0].created_at || d[0].date || d[0].debut);
      return "• " + n + " : " + d.length + " enregistrement(s)" + (last ? ", dernier le " + String(last).slice(0, 10) : "") + ".";
    });
    // Lire les fiches réellement enregistrées par les pages du centre sur cet appareil.
    let local = [];
    try {
      if (window.G360_CENTRE && typeof window.G360_CENTRE.loadRecords === "function") {
        const aliases = {accueil:["centre","alertes","missions","rapports"],carte:["territoire","navigation"],geoloc:["geoloc","navigation"],users:["users"],parcs:["parcs","territoire"],garmin:["garmin","navigation"],alertes:["alertes"],rapports:["rapports"],missions:["missions"],centre:["centre","alertes","missions","rapports"],stats:["stats"]};
        const ids = aliases[a.id] || [a.id];
        local = window.G360_CENTRE.loadRecords().filter(r => ids.includes(r.module));
      }
    } catch (_) {}
    if (local.length) {
      lines.push("• fiches locales de cette page : " + local.length + " enregistrement(s).");
      local.slice(-3).reverse().forEach(r => lines.push("  - " + String(r.createdAt || "").slice(0,10) + " · " + String(r.title || r.moduleName || "Fiche") + " · " + String((r.values || []).filter(Boolean).join(" ; ")).slice(0,220)));
    }
    if (!lines.length) lines.push("• aucune source de données reliée à cette IA pour le moment.");
    if (!local.length && a.data.some(n => !read(n))) lines.push("• les sources externes non connectées ne fournissent pas de données en direct.");
    return a.page + " — état vérifiable des données :\n" + lines.join("\n");
  }

  // --- IA serveur optionnelle (Supabase Edge Function). Jamais annoncée sans réponse réelle. ---
  async function remote(a, q) {
    if (!G.endpoint) return null;
    try {
      const r = await fetch(G.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: a.id, page: a.page, question: q, contexte: analyse(a) }) });
      if (!r.ok) return null;
      const j = await r.json();
      return j && j.reponse ? j.reponse : null;
    } catch (e) { return null; }
  }

  // --- AVATAR CENTRAL : seul canal vers l'humain ---
  const css = `#g360-av{position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#0b1f14;color:#fff;border-top:3px solid #fcd116;border-radius:16px 16px 0 0;padding:12px;display:none;max-height:75vh;overflow:auto;font:15px system-ui}
#g360-av .h{display:flex;gap:10px;align-items:center}#g360-av img{width:56px;height:56px;border-radius:50%;object-fit:cover;object-position:top;border:2px solid #fcd116}
#g360-av .b{white-space:pre-wrap;margin:10px 0;line-height:1.4}#g360-av input{width:100%;box-sizing:border-box;padding:10px;border-radius:8px;border:0;margin-top:6px}
#g360-av button{background:#009e60;color:#fff;border:0;border-radius:8px;padding:8px 12px;margin:4px 4px 0 0}
.g360-ia{background:#009e60;color:#fff;border:1px solid #fcd116;border-radius:12px;font:600 12px system-ui;padding:3px 8px;margin-left:6px;cursor:pointer}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const box = document.createElement('div'); box.id = 'g360-av';
  box.innerHTML = '<div class="h"><img id="g360-img" alt="Avatar"><div><b>Avatar GABON 360</b><br><small id="g360-via"></small></div><button id="g360-x" style="margin-left:auto">✕</button></div><div class="b" id="g360-txt"></div><input id="g360-q" placeholder="Poser une question à cette IA…"><button id="g360-go">Demander</button><button id="g360-say">🔊 Écouter</button>';
  document.body.appendChild(box);
  const $ = (i) => document.getElementById(i);
  const src = document.querySelector('[data-avatar] img, #avatar img, img.avatar');
  if (src) $('g360-img').src = src.src; // même image que l'avatar central, visage non modifié

  const Avatar = (G.avatar = {
    // L'avatar reçoit la réponse d'une IA de page et la donne à l'humain.
    deliver(agent, text, mode) {
      G.current = agent;
      $('g360-via').textContent = 'via IA « ' + agent.page + ' » · ' + (mode === 'serveur' ? 'IA serveur' : 'mode local (données de l\'application)');
      $('g360-txt').textContent = text; box.style.display = 'block';
      window.dispatchEvent(new CustomEvent('g360:avatar-message', {detail:{source:'ia-core', text, agent:agent.id, mode}}));
    },
    async ask(id, q) {
      const a = AGENTS.find((x) => x.id === id); if (!a) return;
      const r = q ? await remote(a, q) : null;
      Avatar.deliver(a, r || (q ? "Je n'ai pas d'IA serveur connectée : voici l'état réel de la page.\n" : '') + analyse(a), r ? 'serveur' : 'local');
    },
    say() { const t = $('g360-txt').textContent; if (!('speechSynthesis' in window) || !t) return;
      const u = new SpeechSynthesisUtterance(t); u.lang = 'fr-FR'; speechSynthesis.cancel(); speechSynthesis.speak(u); }
  });
  $('g360-x').onclick = () => (box.style.display = 'none');
  $('g360-go').onclick = () => G.current && Avatar.ask(G.current.id, $('g360-q').value.trim());
  $('g360-say').onclick = Avatar.say;

  // --- Chaque page / option reçoit son bouton IA relié à l'avatar ---
  // Balisage : <section data-ia="alertes"> ... </section>  ou  <button data-ia="rapports">…</button>
  G.mount = function () {
    document.querySelectorAll('[data-ia]').forEach((el) => {
      if (el.querySelector(':scope > .g360-ia')) return;
      const id = el.getAttribute('data-ia'), a = AGENTS.find((x) => x.id === id);
      if (!a) { console.warn('IA inconnue :', id); return; }
      const b = document.createElement('button'); b.className = 'g360-ia'; b.textContent = '🤖 IA';
      b.title = 'IA ' + a.page; b.onclick = (e) => { e.stopPropagation(); Avatar.ask(id); };
      el.appendChild(b);
    });
  };
  document.addEventListener('DOMContentLoaded', G.mount); if (document.readyState !== 'loading') G.mount();
  new MutationObserver(G.mount).observe(document.body, { childList: true, subtree: true });

  // Veille proactive : surveille uniquement les sources de données déjà reliées à l'application.
  // Aucun événement n'est inventé et les données existantes ne sont pas annoncées au démarrage.
  G.proactive = { enabled: true, intervalMs: 20000, baselineReady: false, last: Object.create(null) };
  G.setProactive = function(enabled) { G.proactive.enabled = !!enabled; return G.proactive.enabled; };
  function scanNewRecords() {
    if (!G.proactive.enabled) return;
    const changed = [];
    AGENTS.forEach(a => a.data.forEach(table => {
      const rows = read(table);
      if (!Array.isArray(rows)) return;
      const signature = rows.map(r => String(r && (r.id || r.uuid || r.created_at || r.date || r.titre || r.title) || '')).join('|') + '#' + rows.length;
      const key = a.id + ':' + table;
      if (Object.prototype.hasOwnProperty.call(G.proactive.last, key) && G.proactive.last[key] !== signature) {
        const oldCount = Number((G.proactive.last[key].match(/#(\d+)$/) || [])[1] || 0);
        changed.push({agent:a, table, diff:Math.max(0, rows.length-oldCount)});
      }
      G.proactive.last[key] = signature;
    }));
    if (!G.proactive.baselineReady) { G.proactive.baselineReady = true; return; }
    const unique = new Map();
    changed.forEach(c => { const p=unique.get(c.agent.id); if (!p || c.diff>p.diff) unique.set(c.agent.id,c); });
    unique.forEach(c => {
      const message = 'Nouvelle information reçue pour ' + c.agent.page + ' : ' +
        (c.diff ? c.diff + ' nouvel enregistrement(s) détecté(s) dans ' + c.table + '.' : 'les données de ' + c.table + ' ont été mises à jour.') +
        ' Cette information doit être vérifiée.';
      Avatar.deliver(c.agent, message, 'local');
    });
  }
  try { scanNewRecords(); } catch(e) { console.warn('Veille proactive indisponible',e); }
  window.setInterval(() => { try { scanNewRecords(); } catch(e) { console.warn('Veille proactive indisponible',e); } }, G.proactive.intervalMs);
})();
