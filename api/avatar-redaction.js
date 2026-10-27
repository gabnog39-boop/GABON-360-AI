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
    system:"Tu es l'avatar central de GABON 360 AI, plateforme privée de suivi du territoire gabonais. Réponds en français, en quelques phrases, UNIQUEMENT à partir du contexte fourni. Si l'information manque, dis-le : n'invente aucune donnée, aucune source, aucun chiffre. Ne transforme jamais une suspicion en fait confirmé.",
    messages:[{role:"user",content:"Contexte (données réelles de la plateforme) :\n"+ctx+"\n\nQuestion : "+q}]})});
  const j=await r.json();if(!r.ok)return res.status(502).json({error:(j.error&&j.error.message)||"Erreur du service IA"});
  res.status(200).json({text:(j.content||[]).filter(c=>c.type==="text").map(c=>c.text).join("\n")});
 }catch(e){res.status(500).json({error:"Erreur interne"})}};
