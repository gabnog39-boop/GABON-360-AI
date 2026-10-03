# GABON 360 AI — Défense en profondeur

## But

Protéger le centre de surveillance contre la compromission d'un compte, d'un appareil, d'une connexion réseau ou d'une source de données. La sécurité doit reposer sur plusieurs barrières indépendantes : aucune barrière unique ne doit suffire à prendre le contrôle du système.

## 1. Identité et accès

- comptes nominatifs uniquement ;
- MFA obligatoire pour les rôles privilégiés ;
- principe du moindre privilège ;
- sessions courtes et révocables ;
- séparation stricte des rôles opérateur, analyste, administrateur et propriétaire ;
- double validation pour les changements critiques ;
- révocation immédiate d'un compte ou d'une session compromise ;
- aucun mot de passe ou secret permanent dans l'APK.

## 2. Protection du serveur

- API uniquement via HTTPS ;
- validation stricte des entrées ;
- limitation de débit ;
- protection contre les requêtes rejouées et les doublons ;
- séparation des environnements développement, test et production ;
- sauvegardes chiffrées et restauration régulièrement testée ;
- journalisation des opérations sensibles.

## 3. Protection de l'application Android

L'application mobile est considérée comme un terminal non fiable :

- aucune clé maître dans l'APK ;
- aucun privilège serveur accordé sur la seule base d'un appareil ;
- tokens courts et révocables ;
- vérification serveur de toutes les opérations sensibles ;
- détection des versions obsolètes ;
- possibilité de suspendre une session ou un appareil compromis.

## 4. Protection des données

Chaque donnée importante doit conserver sa provenance : source, heure, état, qualité, traitement et validation. Une donnée reçue d'une source compromise ou inconnue ne doit pas pouvoir devenir automatiquement une information validée.

Les données critiques doivent être protégées contre la modification silencieuse et les journaux d'audit doivent être protégés contre l'altération.

## 5. Sources et capteurs

Chaque source autorisée doit avoir :

- un propriétaire ou responsable ;
- une autorisation ;
- un identifiant ;
- un état de connexion ;
- une date de dernière réception ;
- un niveau de qualité ;
- un statut `LIVE`, `DIFFERE`, `HISTORIQUE`, `SIMULE` ou `INDISPONIBLE`.

Une source inconnue, usurpée ou incohérente est isolée et signalée. Elle ne doit pas pouvoir injecter directement une alerte validée.

## 6. Détection de compromission

Le centre doit surveiller les anomalies telles que :

- connexions inhabituelles ;
- changement soudain de privilèges ;
- multiplication de tentatives d'authentification ;
- modification inattendue de configuration ;
- création massive d'événements ;
- activité anormale d'une source ;
- incohérences d'horodatage ou de provenance ;
- erreurs répétées d'intégrité ou de synchronisation.

Les signaux doivent déclencher une alerte de sécurité et une enquête humaine, pas une action automatique irréversible.

## 7. Mode confinement

Prévoir un mode de confinement permettant à un administrateur habilité de :

1. isoler une source suspecte ;
2. révoquer les sessions concernées ;
3. bloquer temporairement les opérations sensibles ;
4. préserver les journaux et preuves techniques ;
5. basculer vers une sauvegarde ou un service de secours ;
6. rétablir progressivement les fonctions après vérification.

## 8. Continuité

Le centre doit rester exploitable en cas de panne réseau ou de perte temporaire d'une source. Les données en attente sont mises en file, signées ou contrôlées selon le mécanisme retenu, puis synchronisées sans créer de doublons.

## 9. Règle fondamentale

GABON 360 AI ne doit jamais dépendre d'un seul serveur, d'un seul compte administrateur, d'une seule source de données ou d'une seule connexion réseau pour sa sécurité.

La protection recherchée est une **défense en profondeur**, avec contrôle humain, traçabilité, séparation des privilèges et capacité de récupération.
