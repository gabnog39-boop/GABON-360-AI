# GABON 360 AI — audit fonctionnel page par page
Date : 9 novembre 2026
Branche : test-avatar-central
Base examinée : commit daa2482544ad70ee65dcf6f2ff5bcefc64eeacb1

## Résumé
Le dépôt contient une interface principale avec 8 onglets historiques, 14 formulaires de modules complémentaires, un noyau de 22 agents IA, plusieurs scripts transversaux et un projet Android WebView. Ces nombres ne signifient pas que 44 fonctions distinctes sont opérationnelles : plusieurs pages se recouvrent et certains modules ne font qu'enregistrer des demandes localement.

## Pages principales — état et travaux requis

| Page | Fonction existante vérifiée | Écart à combler |
|---|---|---|
| Accueil | Synthèse et IA accueil | Faire apparaître l'avatar principal directement dans l'accueil, montrer des indicateurs issus des enregistrements réels, états source et dernière mise à jour. |
| Alertes | Formulaire et file locale, notification vers l'avatar | Identifiant unique, niveau de validation, provenance, statut ouvert/en cours/clôturé, historique d'audit et synchronisation serveur. |
| Carte | Leaflet et carte, sélection/coordonnées | Couches fiables et datées, limites de parcs officielles, téléchargement hors ligne, légende, provenance et précision GPS. |
| Missions | Formulaires, fiches locales, import/export partiel | Cycle de mission, équipe, ordre de mission, GPX, départ/retour, points horodatés, stockage offline et sync différée. |
| Parcs | Page de consultation/registre | Référentiel officiel vérifié, fiches par parc, secteurs, observations et historique ; ne pas inventer des limites. |
| Garmin / GPX | Page d'échange et outils/scripts historiques | Tester import GPX réel, produire GPX standard depuis les traces GPS, vérifier compatibilité appareil/application Garmin. |
| Rapports | Création de rapports locaux | Génération à partir de fiches liées, pièces/preuves, auteur, validation, export et transmission serveur. |
| Utilisateurs | Liste et gestion de comptes en interface | Contrôle serveur des rôles, approbation propriétaire, révocation, MFA comptes privilégiés et journal d'audit. |

## Modules complémentaires — 14 formulaires locaux repérés

| Module | Capacité réelle actuelle | Connexion ou développement requis |
|---|---|---|
| Satellites | Enregistrer une demande d'observation | Accès image fournisseur, horodatage d'acquisition, couverture nuageuse, géoréférencement ; pas de vidéo satellite live. |
| Drones | Préparer/consigner une mission | Passerelle drone autorisée, télémétrie et flux uniquement après autorisation et configuration. |
| Navigation | Décrire départ/destination/risques | Routage cartographique hors ligne, navigation, GPX et tests terrain. |
| Géolocalisation | Consigner des coordonnées | GPS natif, qualité/accuracy, permission et suivi arrière-plan sécurisé. |
| Cybersécurité | Registre local d'incidents | Alertes système réelles, contrôle d'accès, logs serveur et procédures de réponse défensive. |
| Mémoire territoriale | Archiver des faits localement | Recherche, chronologie, géolocalisation, source et synchronisation. |
| Statistiques | Enregistrer des valeurs | Calcul automatique depuis les tables réelles, périodes et dédoublonnage ; ne pas confondre saisie et indicateur calculé. |
| Météo | Consigner des observations | Connecteur Open-Meteo existe dans le script ; vérifier réponse, coordonnées et heure avant statut connecté. |
| Eaux et océan | Enregistrer des observations | Référentiel des stations/cours d'eau, capteurs ou saisies validées, coordonnées et provenance. |
| Frontières | Enregistrer des signalements | Sources officielles autorisées, zones de référence, contrôle humain et protection des informations sensibles. |
| Espace aérien | Registre de signalements | Source autorisée/ADS-B ou données institutionnelles, limites d'usage et statut non connecté tant que non configuré. |
| Centre national | Saisie de situation | Agrégation des alertes, missions et rapports réels, horodatage, filtres et validation. |
| Administration | Journal local de paramètres/décisions | RBAC serveur, actions autorisées, audit inviolable et gestion des configurations. |
| Paiements | Suivi manuel des demandes/références | Prestataire de paiement, webhooks vérifiés côté serveur, rapprochement et statut confirmé serveur ; jamais valider sur simple saisie. |

## 22 agents IA — règle de raccordement
Les 22 identifiants déclarés dans gabon360-ia.js sont : accueil, carte, satellites, drones, navigation, geoloc, cyber, memoire, alertes, rapports, stats, meteo, parcs, eaux, frontieres, air, centre, admin, users, paiements, missions, garmin.

Chaque agent doit :
1. recevoir uniquement les données autorisées de sa page et afficher leur source ;
2. signaler explicitement les tables/API absentes ;
3. fournir son analyse à Avatar.deliver, sans canal parallèle non contrôlé ;
4. distinguer fait enregistré, observation, hypothèse IA et information validée ;
5. ne jamais présenter un module de saisie locale comme une source temps réel.

## Connecteurs et fonctions transversales
- Météo : le script prévoit Open-Meteo ; la disponibilité doit être mesurée à chaque appel.
- Imagerie : le script documente NASA GIBS/Worldview ; c'est de l'imagerie avec délais de disponibilité, pas un flux vidéo live.
- IA serveur : api/assistant.js exige session Supabase, profil actif et ANTHROPIC_API_KEY côté serveur. Vérifier aussi le modèle configuré et les erreurs fournisseur.
- Avatar : le noyau crée une interface flottante et relaie les messages ; vérifier qu'il est réellement intégré à l'écran d'accueil et que l'image d'origine est conservée.
- Navigation : le GPS natif existe au premier plan dans MainActivity, mais onPause arrête le suivi. La page exporte actuellement JSON et non GPX.
- Locus : aucune intégration Locus identifiable dans l'arborescence consultée ; à réaliser séparément avec l'API/contrat Android officiel compatible.
- Android : le manifeste référence les ressources mipmap de l'icône ; le workflow copie le JPG en drawable-nodpi, ce qui ne démontre pas l'utilisation du logo dans le lanceur.

## Ordre d'exécution conseillé
Phase 1 — cohérence de toutes les pages : navigation unique, page d'accueil avec avatar, état des sources et liens explicites entre 8 onglets, 14 modules et 22 agents.
Phase 2 — données locales fiables : schéma commun, identifiants, provenance, horodatage, validation, recherche, export et sauvegarde.
Phase 3 — terrain : GPS premier plan/arrière-plan, GPX standard, cartes préchargées et intégration Locus testée.
Phase 4 — connecteurs réels : météo, imagerie satellite, référentiels SIG officiels, services institutionnels autorisés et paiements.
Phase 5 — gouvernance : rôles serveur, accès propriétaire, abonnements, journal d'audit, MFA et révocation.
Phase 6 — validation : tests automatisés, tests de chaque page, tests offline/synchronisation, build Android, installation sur téléphone et vérification APK.

## Critères d'acceptation par page
Une page n'est terminée que si : elle s'ouvre sans erreur ; ses boutons font réellement l'action annoncée ; les données sont conservées ; les erreurs sont visibles ; les sources sont citées/horodatées ; son agent IA lit les mêmes données ; les données locales et serveur sont distinguées ; les droits sont vérifiés ; un test correspondant passe.

## Limites de cet audit
Cet audit porte sur les fichiers du dépôt et leurs contrats visibles. Il ne certifie ni accès à des données gouvernementales, ni flux satellite/drone/caméra, ni paiement réel, ni intégration Locus/Garmin, ni compilation APK, ni essai terrain. Les connexions nécessitent les autorisations, comptes, endpoints et essais correspondants.
