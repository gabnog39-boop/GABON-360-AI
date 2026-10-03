# Baseline de sécurité GABON 360 AI

## Identité et accès

- rôles explicites et principe du moindre privilège ;
- MFA pour les comptes à privilèges ;
- sessions courtes et révocables ;
- rotation des secrets ;
- aucune clé ou mot de passe dans l'APK ;
- séparation des environnements développement, test et production.

## API

- HTTPS obligatoire en production ;
- validation stricte des entrées ;
- limitation de débit sur les endpoints sensibles ;
- protection contre rejeu et doublons ;
- journalisation sans exposer de secrets ;
- réponses d'erreur ne révélant pas d'informations internes.

## Données

- chiffrement en transit ;
- chiffrement au repos lorsque requis ;
- sauvegardes chiffrées ;
- politique de rétention ;
- contrôle d'accès aux pièces justificatives et médias ;
- intégrité vérifiable des preuves importantes.

## Audit

Chaque opération sensible doit pouvoir être reliée à :

`acteur → rôle → organisation → action → objet → date/heure → résultat`

Les journaux d'audit doivent être protégés contre la modification non autorisée et leur intégrité doit être vérifiable.

## IA et alertes

Le moteur IA doit conserver au minimum :

- source ;
- horodatage ;
- version du modèle/règle ;
- entrée ou référence d'entrée ;
- résultat ;
- niveau de confiance ;
- état de validation ;
- opérateur ayant validé ou rejeté lorsque applicable.

Une prédiction ou anomalie IA ne doit pas être présentée comme un fait confirmé sans validation appropriée.

## Vidéo, drones et capteurs

Les intégrations doivent utiliser uniquement des sources autorisées et documentées. Chaque flux doit avoir un propriétaire, une politique d'accès et un statut de connexion.

Le système doit afficher clairement si une donnée est :

- LIVE et réellement connectée ;
- reçue avec retard ;
- historique ;
- simulée ;
- indisponible.

## Continuité

Prévoir :

- health checks ;
- surveillance des dépendances ;
- sauvegardes ;
- restauration testée ;
- reprise après incident ;
- mode dégradé ;
- procédure de révocation en cas de compromission.

## Règle fondamentale

GABON 360 AI doit être un système de supervision et d'aide à la décision **auditable, proportionné et contrôlé par des personnes habilitées**. Il ne doit pas fournir une capacité de surveillance clandestine ni déclencher automatiquement des mesures coercitives sur la seule base d'une détection algorithmique.
