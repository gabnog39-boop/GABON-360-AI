# GABON 360 AI — audit technique vérifiable
Date : 2026-11-09
Branche examinée : test-avatar-central
Commit examiné : b84445ddbb73600fc5ec15b273d3db6e1993ee93

## Périmètre et méthode
Audit en lecture des fichiers du dépôt GitHub. Aucun test sur téléphone, aucune compilation Android et aucune connexion à un compte Locus/Garmin n'ont été exécutés pendant cet audit. Les états ci-dessous ne doivent donc pas être interprétés comme une recette de validation terrain.

## Constats vérifiés

### 1. GPS Android
- Le fichier `android/app/src/main/java/ga/gabon360/ai/MainActivity.java` contient une interface JavaScript `AndroidGPS` avec les méthodes `start()`, `stop()` et `isAvailable()`.
- Il utilise `LocationManager.GPS_PROVIDER` et transmet les coordonnées à la WebView par les événements `g360:gps-fix` et `g360:gps-status`.
- Le module `gabon360-navigation-offline.js` écoute bien ces deux événements et enregistre les points dans `localStorage`.
- Limite explicite : `onPause()` arrête le suivi. Le suivi écran éteint / arrière-plan n'est donc pas assuré. Il faudra un service Android de premier plan avec permissions et notification persistante, puis des tests réels.
- L'autorisation GPS est demandée au démarrage et aussi lorsque l'utilisateur demande le démarrage du GPS. Le comportement doit être vérifié sur les versions Android visées.

### 2. Locus Map
- Aucun fichier ou dépendance Locus identifiable par son nom n'apparaît dans l'arborescence de 162 entrées de ce commit.
- Le module actuel gère une position GPS et des points locaux ; cela ne constitue pas une intégration Locus.
- Travail requis : choisir le contrat d'intégration Android officiel adapté à la version de Locus installée, gérer les intents/API disponibles, les retours d'erreur, l'export/import GPX et les tests sur appareil. Ne pas déclarer l'intégration faite avant ces essais.

### 3. Garmin / GPX
- Le dépôt contient des scripts de préparation de navigation Garmin et le noyau IA déclare un agent Garmin/GPX.
- Le module GPS consulté exporte actuellement un JSON nommé `gabon360-trace-gps.json`, pas un fichier GPX.
- Il faut implémenter et tester un vrai export GPX standard (waypoints, trackpoints, horodatages, coordonnées) et vérifier l'import dans les appareils/applications Garmin pris en charge.

### 4. Avatar et 22 IA
- `gabon360-ia.js` déclare 22 agents.
- Le code prévoit un canal central `G360_IA.avatar.deliver` et une analyse locale fondée sur les données disponibles.
- Plusieurs agents ont une liste de sources de données vide (notamment satellites, drones, météo, frontières, espace aérien et paiements dans la déclaration consultée). Leur présence dans la liste ne prouve pas qu'ils reçoivent des données opérationnelles.
- La synthèse vocale Web Speech est prévue côté navigateur ; aucun pont natif `AndroidTTS` n'a été trouvé dans le `MainActivity.java` examiné.
- Le démarrage automatique de la voix doit respecter le geste utilisateur et les restrictions Android/WebView.

### 5. Icône Android
- Le workflow `.github/workflows/build-apk-test.yml` copie `icons/gabon360-icon.jpg` vers `res/drawable-nodpi/gabon360_icon.jpg`.
- Le manifeste Android référence `@mipmap/ic_launcher` et `@mipmap/ic_launcher_round`.
- La simple copie dans `drawable-nodpi` ne prouve donc pas que le lanceur Android utilise l'icône officielle. Il faut générer les ressources mipmap adaptées et vérifier l'icône sur un APK installé.

### 6. Compilation APK
- Le workflow de test installe Java 17, Gradle 8.9 et Android SDK 35, puis exécute `assembleDebug`.
- Il vérifie que `android/app/build/outputs/apk/debug/app-debug.apk` existe avant de publier un artefact.
- Le fichier workflow existe ; cela ne prouve pas qu'un run récent a réussi. Le résultat doit être contrôlé dans GitHub Actions et le SHA-256 de l'APK conservé.

### 7. Données réelles et sécurité
- `docs/INTEGRATIONS_AND_AUTHORIZATIONS.md` impose de distinguer sources réelles, historiques, différées, simulées et indisponibles.
- Les modules satellites, drones, caméras et sources institutionnelles doivent rester verrouillés tant que les autorisations, contrats, endpoints et identifiants serveur ne sont pas configurés.
- `api/assistant.js` dépend de la variable serveur `ANTHROPIC_API_KEY`, d'une session Supabase valide et d'un profil actif. Une réponse IA serveur n'est donc pas garantie par la seule présence du fichier.

## Ordre recommandé des travaux
1. Corriger l'icône Android de façon à ce que le lanceur utilise effectivement le visuel officiel.
2. Ajouter le suivi GPS arrière-plan via un service de premier plan, sans perdre le suivi existant au premier plan.
3. Ajouter des tests automatisés des événements GPS et un protocole de test terrain (fix, précision, perte GPS, reprise, batterie).
4. Implémenter l'export GPX et valider l'import dans les outils Garmin ciblés.
5. Implémenter l'intégration Locus avec l'API/intent officiel, après validation de la compatibilité de la version installée.
6. Ajouter le pont TTS Android seulement si les tests WebView démontrent qu'il est nécessaire ; préserver le choix vocal et le consentement.
7. Tester le relais IA serveur, les permissions, les profils et la provenance des données.
8. Lancer le workflow APK sur cette branche, vérifier le succès, installer l'APK et tester l'accueil/avatar/navigation sur un appareil réel.

## Conclusion
Le GPS Android au premier plan est déjà présent dans le commit examiné : il ne faut pas le réécrire inutilement. Les principaux écarts vérifiés concernent le suivi arrière-plan, l'intégration Locus absente, l'export GPX absent du module GPS consulté et l'utilisation effective de l'icône officielle par le lanceur Android. Aucun APK n'est déclaré validé par cet audit.
