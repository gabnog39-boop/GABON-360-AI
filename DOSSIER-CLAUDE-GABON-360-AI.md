# DOSSIER DE TRANSMISSION À CLAUDE — GABON 360 AI
Version de référence : branche `test-avatar-central`
Dépôt : https://github.com/gabnog39-boop/GABON-360-AI
Dernière base vérifiée avant intégration documentaire : commit `949a90d4737e410039662ad1fa85fd6b239559d6` (29 octobre 2026).

## 1. Objet
Ce dossier accompagne le code source réel du dépôt. Il demande un audit technique complet puis des corrections contrôlées pour faire évoluer GABON 360 AI vers un centre intégré de surveillance et de gestion du territoire gabonais. Il ne faut pas présenter une maquette comme un système opérationnel.

## 2. Règles impératives de protection
- Travailler exclusivement sur une copie/branche de test issue de `test-avatar-central`.
- Ne jamais modifier `main` / `principal`, ni fusionner vers ces branches.
- Commencer par un audit en lecture seule et dresser l'inventaire des fichiers, dépendances, services, clés de configuration (sans révéler de secrets), API et fonctions.
- Ne supprimer, écraser, renommer ou remplacer aucun fichier ni fonction existante sans justification, proposition de diff et autorisation explicite.
- Préserver les parcours de connexion, e-mail/mot de passe, rôles, paiements et mécanismes de sécurité existants.
- Ne jamais inventer de résultats de tests. Distinguer clairement : opérationnel testé, partiel, simulé/démonstration, absent, bloqué par une dépendance ou un accès.
- Ne pas publier de secrets, clés API, jetons, mots de passe ou données personnelles dans le code, les rapports ou les journaux.

## 3. Vision fonctionnelle
GABON 360 AI vise un centre de contrôle national couvrant :
- les 9 provinces, les 13 parcs nationaux et leurs périphéries ;
- les forêts, concessions et zones d'exploitation ;
- les territoires ruraux et communautés ;
- les rivières, bassins versants, zones humides ;
- le littoral, les zones côtières et marines ;
- les frontières, corridors écologiques et espaces aériens concernés.
Les sources de données doivent être identifiées et leur couverture, fréquence, licence, précision et latence documentées. Ne pas annoncer une surveillance nationale en temps réel si les flux ne sont pas effectivement raccordés.

## 4. Les 22 assistants IA à inventorier et tester
1. Accueil
2. Carte
3. Satellites
4. Drones
5. Navigation
6. Géolocalisation
7. Cyber
8. Mémoire territoriale
9. Alertes
10. Rapports
11. Statistiques
12. Météo
13. Parcs
14. Eaux / océans
15. Frontières
16. Espace aérien
17. Centre national
18. Administration
19. Utilisateurs
20. Paiements
21. Missions
22. Garmin

Pour chacune : préciser son rôle, ses entrées, ses sorties, son interface, ses API/dépendances, son stockage, ses permissions, son mode hors ligne, ses tests et son état réel. Vérifier qu'il ne s'agit pas seulement d'un formulaire local ou d'une réponse simulée.

## 5. Avatar central — interlocuteur unique
- La page d'accueil doit être l'avatar central.
- Conserver strictement l'image originale fournie pour l'avatar ; ne pas la remplacer ni la redessiner.
- L'icône de l'application doit employer le logo officiel GABON 360 fourni dans le projet.
- L'avatar est l'interlocuteur humain central : les assistants transmettent leurs résultats à l'avatar (mécanisme existant de type `Avatar.deliver` à vérifier), au lieu de parler chacun séparément à l'utilisateur.
- Vérifier écoute micro, réponse écrite, voix française, annonces, gestion des alertes, historique et erreurs réseau.
- Améliorer si possible clignement, expressions, synchronisation labiale et gestes sans dégrader l'image d'origine.
- Voix masculine française préférée ; voix féminine acceptable si la plateforme ne permet pas mieux.
- Toute annonce proactive doit être contrôlable, traçable et réglable par rôle.

## 6. Observation du territoire et données
Examiner les possibilités réelles de connexion aux données satellites, drones, cartes, météo, capteurs et rapports de terrain. Pour chaque connecteur, fournir fournisseur, URL/API, conditions d'accès, coût éventuel, licence, fréquence, couverture, horodatage, précision, quotas et procédure de panne.
Distinguer images satellites périodiques, produits d'observation, détections automatiques et vidéo réellement en direct. Une anomalie détectée (ex. défrichement, piste, campement ou activité suspecte) est une alerte à vérifier, jamais une preuve automatique d'infraction.
Les alertes doivent comporter source, coordonnées, date/heure, niveau de confiance, zone concernée, historique, statut de vérification et responsable.

## 7. Navigation forestière, Locus Map et Garmin
Fonctions à préserver et développer :
- navigation GPS en forêt, cartes hors ligne téléchargées avant mission ;
- points/waypoints, coordonnées, itinéraires, traces et fichiers GPX ;
- préparation et suivi des missions et équipes ;
- photos/observations géolocalisées, stockage local et synchronisation différée ;
- remontée des informations vers le centre et l'avatar central.
Vérifier les API/SDK, licences et capacités réelles de Locus Map et des appareils Garmin. Ne pas supposer qu'une intégration complète existe sans test sur matériel compatible.

## 8. Communication hors réseau entre patrouilles et centre
Étudier une solution permettant aux équipes de s'échanger des messages en forêt sans réseau mobile ni Wi-Fi : radio adaptée, LoRa/mesh ou autre architecture réaliste. Décrire portée mesurée, relais de proche en proche, stockage local, store-and-forward, accusés de réception, horodatage, identité des équipes, chiffrement, autonomie, fréquence réglementaire, coût et limites.
Le GPS seul ne transmet pas de messages. La messagerie satellite exige un terminal, un fournisseur, un abonnement et une couverture compatibles. Ne pas promettre que le téléphone Android courant assure cette fonction.

## 9. Architecture, sécurité et exploitation
Auditer l'application web, Android/WebView, API serveur, base de données, authentification, rôles, paiements, stockage, journaux, gestion des erreurs, mode hors ligne, performances et déploiement. Vérifier notamment les contrats requête/réponse entre client et API, les routes réellement présentes, les variables d'environnement et la configuration de production. Ne jamais afficher de secrets.
Documenter les rôles propriétaire, administrateur, superviseur et utilisateur selon les règles réellement implémentées. Protéger les données sensibles de localisation des patrouilles et les données institutionnelles.

## 10. Plan de travail et livrables exigés
Phase A — audit en lecture seule : inventaire complet, diagramme d'architecture, tableau des 22 IA et matrice des fonctions (testé/partiel/simulé/absent).
Phase B — plan de correction : risques classés, dépendances, coûts/accès nécessaires, fichiers concernés et diffs proposés.
Phase C — corrections isolées : uniquement sur branche de travail dédiée, petits lots, tests après chaque lot, aucune régression.
Phase D — validation : tests unitaires, intégration, sécurité, navigateur mobile Android, mode hors ligne et tests matériels quand disponibles.
Phase E — livraison : code complet, journal des changements, rapport des tests avec preuves/logs, limites restantes, guide de configuration/déploiement et procédure de compilation/signature APK.
Ne livrer un APK que si la compilation a réellement réussi. Sinon fournir les commandes et prérequis exacts, sans prétendre qu'un APK existe.

## 11. Critères d'acceptation
- L'application démarre et ses parcours principaux sont testés.
- L'avatar central est bien l'accueil et reçoit les messages des assistants.
- Les 22 assistants sont inventoriés individuellement avec état réel prouvé.
- Les cartes, alertes, missions, rapports, utilisateurs et paiements sont vérifiés selon les accès disponibles.
- Les fonctions Locus/Garmin et hors réseau sont testées sur équipements compatibles ou clairement déclarées non validées.
- Aucune fonction existante n'a été supprimée sans accord.
- Aucune modification de `main` / `principal`.
- Un rapport distingue sans ambiguïté les fonctions opérationnelles, partielles, simulées et absentes.

## 12. Instruction directe à Claude
Examine le dépôt entier et ce document. Commence par l'audit en lecture seule. Ne te limite pas à `index.html` et ne reconstruis pas une maquette isolée. N'écris aucun changement avant d'avoir présenté l'inventaire, les constats, les risques et le plan de correction. Ensuite, travaille uniquement sur une branche de test distincte, préserve l'existant et livre les preuves de tests. Si une ressource, un compte, une clé, un appareil ou un abonnement manque, indique-le clairement au lieu de simuler son fonctionnement.
