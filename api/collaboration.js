// Consultation serveur authentifiée des 22 rôles GABON 360 AI.
// Le moteur effectue un triage déterministe des preuves transmises; il ne simule
// ni modèles autonomes ni flux capteurs non connectés.
const SB = "https://ztucadvgowsdixomoikm.supabase.co";
const KEY = "sb_publishable_J1gbjWaEuekRUZ2Z2VpUrQ_CXS645jS";
const ROUTES = {
  accueil:["centre","alertes","stats","rapports"], carte:["geoloc","satellites","parcs","frontieres"],
  satellites:["carte","parcs","eaux","memoire","alertes"], drones:["carte","geoloc","missions","alertes"],
  navigation:["geoloc","missions","garmin","parcs"], geoloc:["carte","navigation","missions","alertes"],
  cyber:["users","admin","centre","alertes"], memoire:["parcs","alertes","missions","rapports","stats"],
  alertes:["centre","memoire","carte","rapports","missions"], rapports:["memoire","missions","stats","centre"],
  stats:["alertes","missions","rapports","centre"], meteo:["navigation","missions","parcs","eaux","alertes"],
  parcs:["satellites","drones","carte","missions","memoire"], eaux:["satellites","meteo","carte","alertes"],
  frontieres:["carte","geoloc","drones","air","alertes"], air:["drones","carte","frontieres","alertes"],
  centre:["accueil","alertes","memoire","stats","rapports"], admin:["cyber","users","paiements","centre"],
  users:["cyber","admin","centre"], paiements:["admin","users","cyber"],
  missions:["navigation","geoloc","parcs","meteo","garmin","rapports"], garmin:["missions","navigation","geoloc","memoire"]
};
const TOPICS = [
  [/satell|sentinel|ndvi|image/i,["satellites","carte","parcs","eaux","memoire"]],
  [/forêt|foret|déforest|deforest|parc|biodivers/i,["parcs","satellites","carte","memoire","alertes"]],
  [/eau|rivière|riviere|fleuve|océan|ocean|côte|cote|inond/i,["eaux","meteo","satellites","carte","alertes"]],
  [/gps|position|coordonn|waypoint|gpx|garmin|itinéraire|itineraire/i,["geoloc","navigation","garmin","missions","carte"]],
  [/drone|caméra|camera|vidéo|video|aérien|aerien/i,["drones","air","carte","frontieres","alertes"]],
  [/frontière|frontiere|limite|transfrontal/i,["frontieres","carte","geoloc","drones","air"]],
  [/météo|meteo|pluie|vent|température|temperature|climat/i,["meteo","missions","parcs","eaux","alertes"]],
  [/cyber|sécurité|securite|connexion|compte|accès|acces|mot de passe/i,["cyber","users","admin","centre"]],
  [/paiement|abonnement|facture/i,["paiements","admin","users"]],
  [/mission|patrouille|équipe|equipe|rapport/i,["missions","navigation","garmin","rapports","memoire"]]
];
const CAPABILITIES = {
  accueil:["situation","synthese","event"],carte:["geometry","bbox","coordinates","location"],
  satellites:["catalog","sentinel","image","ndvi","derived_indicators"],drones:["drone","video","flight","telemetry"],
  navigation:["route","track","waypoint","position"],geoloc:["coordinates","lat","lon","gps","location"],
  cyber:["security","auth","audit","vulnerability","log"],memoire:["history","timestamp","observed_at","event_type"],
  alertes:["severity","priority","alert","finding"],rapports:["report","observation","evidence","finding"],
  stats:["count","metric","indicator","value"],meteo:["weather","precipitation","temperature","wind","forecast"],
  parcs:["forest","vegetation","park","biodiversity","ndvi"],eaux:["water","river","basin","flood","coastal","marine"],
  frontieres:["border","boundary","crossing","frontier"],air:["airspace","aircraft","flight","aviation"],
  centre:["source","timestamp","observation","event","finding"],admin:["role","permission","admin","account"],
  users:["user","profile","account","session"],paiements:["payment","subscription","invoice","transaction"],
  missions:["mission","patrol","team","route","track"],garmin:["gpx","garmin","waypoint","track","coordinates"]
};
function clean(value, depth=0) {
  if (depth > 3) return null;
  if (typeof value === "string") return value.slice(0, 350);
  if (typeof value === "number" || typeof value === "boolean") return value;
  if (Array.isArray(value)) return value.slice(0, 20).map(v => clean(v, depth+1));
  if (value && typeof value === "object") {
    const out = {};
    Object.keys(value).slice(0, 35).forEach(k => {
      if (/token|password|secret|authorization|email|phone/i.test(k)) return;
      out[k.slice(0,60)] = clean(value[k], depth+1);
    });
    return out;
  }
  return null;
}
function keySet(value, out=new Set()) {
  if (Array.isArray(value)) value.slice(0,30).forEach(v=>keySet(v,out));
  else if (value && typeof value === "object") Object.entries(value).forEach(([k,v])=>{out.add(k.toLowerCase());keySet(v,out);});
  return out;
}
module.exports = async (req,res) => {
  if (req.method !== "POST") return res.status(405).json({error:"Méthode non autorisée"});
  try {
    const token=(req.headers.authorization||"").replace(/^Bearer\s+/i,"");
    if(!token) return res.status(401).json({error:"Connexion requise"});
    const u=await fetch(SB+"/auth/v1/user",{headers:{apikey:KEY,Authorization:"Bearer "+token}});
    if(!u.ok) return res.status(401).json({error:"Session invalide"});
    const uid=(await u.json()).id;
    const p=await fetch(SB+"/rest/v1/profiles?id=eq."+uid+"&select=statut",{headers:{apikey:KEY,Authorization:"Bearer "+token}});
    const profiles=await p.json();
    if(!profiles[0]||profiles[0].statut!=="actif") return res.status(403).json({error:"Compte non actif"});
    const body=typeof req.body==="string"?JSON.parse(req.body):(req.body||{});
    const source=String(body.agent||"accueil");
    if(!Object.prototype.hasOwnProperty.call(CAPABILITIES,source)) return res.status(400).json({error:"Agent inconnu"});
    const question=String(body.question||"").slice(0,500);
    const evidence=Array.isArray(body.evidence)?body.evidence.slice(0,80).map(v=>clean(v)).filter(v=>v&&typeof v==="object"):[];
    const selected=[source,...(ROUTES[source]||ROUTES.accueil)];
    TOPICS.forEach(([pattern,agents])=>{if(pattern.test(question))agents.forEach(id=>{if(!selected.includes(id))selected.push(id);});});
    const agents=selected.slice(0,7).map(id=>{
      const expected=CAPABILITIES[id];
      const relevant=evidence.filter(item=>{
        const keys=keySet(item);
        const words=Object.values(item).filter(v=>typeof v==="string").join(" ").toLowerCase();
        return expected.some(term=>keys.has(term)||words.includes(term));
      }).slice(0,8);
      return {id,status:relevant.length?"evidence_received_for_review":"no_relevant_evidence",
        evidence_count:relevant.length,evidence:relevant,
        engine:"authenticated-shared-evidence-triage-v1",
        autonomous_model_connected:false,requires_human_validation:true};
    });
    return res.status(200).json({
      ok:true,source_agent:source,question,agents,planned_count:agents.length,
      evidence_received:evidence.length,evidence_matched:agents.reduce((n,a)=>n+a.evidence_count,0),
      execution:"deterministic_evidence_triage",
      note:"Aucun modèle autonome ni flux externe n'est déclaré connecté par cette route."
    });
  } catch(e) {
    return res.status(500).json({error:"Erreur interne de consultation"});
  }
};
