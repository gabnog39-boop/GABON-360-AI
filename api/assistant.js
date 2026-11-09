// Relais facultatif : IA de rédaction de l'avatar (nécessite la variable ANTHROPIC_API_KEY dans Vercel).
const SB="https://ztucadvgowsdixomoikm.supabase.co",KEY="sb_publishable_J1gbjWaEuekRUZ2Z2VpUrQ_CXS645jS";
module.exports=async(req,res)=>{
 const k=process.env.ANTHROPIC_API_KEY;
 if(req.method==="GET")return res.status(200).json({ok:!!k});
 if(!k)return res.status(503).json({error:"Clé API non configurée"});
 try{
  const tok=(req.headers.authorization||"").replace(/^Bearer\s+/i,"");if(!tok)return res.status(401).json({error:"Connexion requise"});
  const u=await fetch(SB+"/auth/v1/user",{headers:{apikey:KEY,Authorization:"Bearer "+tok}});if(!u.ok)return res.status(401).json({error:"Session invalide"});
  const uid=(await u.json()).id;
  const p=await fetch(SB+"/rest/v1/profiles?id=eq."+uid+"&select=statut",{headers:{apikey:KEY,Authorization:"Bearer "+tok}});const pr=await p.json();
  if(!pr[0]||pr[0].statut!=="actif")return res.status(403).json({error:"Compte non actif"});
  const b=typeof req.body==="string"?JSON.parse(req.body):(req.body||{});const q=String(b.q||"").slice(0,500),ctx=String(b.ctx||"").slice(0,6000);
  const r=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers:{"content-type":"application/json","x-api-key":k,"anthropic-version":"2023-06-01"},
   body:JSON.stringify({model:process.env.ANTHROPIC_MODEL||"claude-sonnet-5-5",max_tokens:500,
    system:"Tu es l'avatar central de GABON 360 AI. Tu coordonnes 22 rôles spécialisés partageant le même contexte : accueil (synthèse nationale), carte (SIG), satellites (Sentinel et imagerie), drones, navigation, géoloc, cyber, mémoire territoriale, alertes, rapports, statistiques, météo, parcs, eaux et océan, frontières, espace aérien, centre national, administration, utilisateurs, paiements, missions et Garmin/GPX. Pour chaque demande, identifie les rôles pertinents, examine leurs éléments de contexte, confronte les informations communes et rends une seule synthèse à l'humain. N'affirme pas qu'un rôle a effectué une analyse si aucune donnée correspondante n'est fournie. Réponds en français, clairement et brièvement, UNIQUEMENT à partir du contexte fourni. Si une source manque, indique précisément qu'elle n'est pas connectée ou qu'aucune donnée n'est disponible. N'invente aucune donnée, source, coordonnée, statistique ou alerte. Ne transforme jamais une suspicion en fait confirmé. Distingue toujours les données locales, les métadonnées de catalogue et les observations physiques confirmées. Toute alerte sensible exige validation humaine.",
    messages:[{role:"user",content:"Contexte (données réelles de la plateforme) :\n"+ctx+"\n\nQuestion : "+q}]})});
  const j=await r.json();if(!r.ok)return res.status(502).json({error:(j.error&&j.error.message)||"Erreur du service IA"});
  res.status(200).json({text:(j.content||[]).filter(c=>c.type==="text").map(c=>c.text).join("\n")});
 }catch(e){res.status(500).json({error:"Erreur interne"})}};
