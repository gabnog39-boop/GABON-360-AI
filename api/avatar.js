// Route /api/avatar — point d'entrée utilisé par index.html (checkLlm / llmAsk).
// Délègue à api/assistant.js : même contrat {q, ctx} -> {text}, mêmes contrôles
// (session Supabase valide, compte « actif », clé ANTHROPIC_API_KEY côté serveur uniquement).
module.exports = require("./assistant.js");
