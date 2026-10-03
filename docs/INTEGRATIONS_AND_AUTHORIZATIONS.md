# GABON 360 AI — Connexions et autorisations

## Règle générale

Une fonction est affichée comme **LIVE** uniquement lorsqu'une source réelle, autorisée et joignable fournit effectivement les données. Une fonction non connectée reste préparée et porte un statut explicite.

## Connectable maintenant

| Fonction | État | Condition |
|---|---|---|
| Météo | Activable maintenant | Fournisseur public configuré |
| Fond cartographique | Activable maintenant | Service cartographique public |
| Position du terminal | Activable maintenant | Permission Android de localisation |
| Santé réseau/API/synchronisation | Activable maintenant | Accès réseau |
| Carte locale et navigation | Disponible hors ligne | Données locales embarquées |

## À préparer sans l'activer

| Fonction | État | Prérequis |
|---|---|---|
| Couches SIG officielles | En attente | Autorisation de l'État + endpoint/données officiels |
| Observation satellite opérationnelle | En attente | Autorisation + fournisseur/contrat + flux |
| Flux drones | En attente | Autorisation + passerelle sécurisée + appareils autorisés |
| Caméras gouvernementales | En attente | Autorisation + passerelle sécurisée |
| Systèmes de sécurité aux frontières | En attente | Autorisation + interface sécurisée |
| Autres capteurs institutionnels | En attente | Autorisation + spécification technique |

## Principe d'activation

Chaque source protégée doit être activée côté serveur après validation de son autorisation, avec identifiants et secrets conservés hors de l'application Android. L'application doit afficher l'état de connexion et la provenance de la donnée.

## Sécurité

- aucune clé secrète dans l'APK ;
- accès par rôle et organisation ;
- journalisation des actions sensibles ;
- révocation des sessions ;
- validation humaine des alertes sensibles ;
- aucune interception ou action coercitive automatique décidée uniquement par l'IA ;
- séparation stricte entre données réelles, historiques, différées et simulations.
