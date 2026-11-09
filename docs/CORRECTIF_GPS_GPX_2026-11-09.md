# Correctif GPS / GPX — 9 novembre 2026

Branche : `test-avatar-central`
Fichier modifié : `gabon360-navigation-offline.js`

## Changements réellement intégrés
1. Le bouton d'export de trace produit désormais un fichier GPX 1.1 (`gabon360-patrouille.gpx`) plutôt qu'un fichier JSON renommé.
2. Les points marqués manuellement sont exportés comme waypoints GPX.
3. Les positions reçues pendant un suivi actif sont enregistrées automatiquement au maximum une fois toutes les cinq secondes.
4. La sauvegarde locale est plafonnée aux 10 000 derniers points pour limiter la croissance du stockage du navigateur.
5. Les coordonnées et horodatages sont écrits dans les trackpoints GPX ; l'altitude est omise lorsqu'elle est réellement absente.

## Compatibilité et limites
- Le correctif réutilise les événements existants `g360:gps-fix` et le pont AndroidGPS déjà présent dans `MainActivity.java`.
- Le suivi automatique ne fonctionne que lorsque l'utilisateur a démarré le suivi et que l'application reçoit les événements GPS.
- Le code Android arrête actuellement le suivi dans `onPause()` : aucune promesse de suivi écran éteint n'est faite.
- Aucun essai d'import sur un appareil Garmin ou Locus, aucun test terrain et aucune compilation APK n'ont encore été réalisés.
- L'intégration Locus, le service GPS Android en premier plan, les autres pages, les sources externes et l'avatar restent à développer ou valider.

## Contrôle après écriture
Le fichier a été relu depuis GitHub après le commit ; les marqueurs d'export GPX, d'enregistrement temporisé et de gestion de l'altitude absente sont présents.
