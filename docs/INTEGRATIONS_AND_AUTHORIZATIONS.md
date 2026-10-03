# GABON 360 AI — Connexions, autorisations et boutons d'activation

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

| Fonction | Bouton conservé | Prérequis |
|---|---|---|
| Couches SIG officielles | **Activer la source officielle** | Autorisation de l'État + endpoint/données officiels |
| Observation satellite opérationnelle | **Activer satellite** | Autorisation + fournisseur/contrat + flux |
| Flux drones | **Activer drones** | Autorisation + passerelle sécurisée + appareils autorisés |
| Caméras gouvernementales | **Activer caméras** | Autorisation + passerelle sécurisée |
| Systèmes de sécurité aux frontières | **Activer source frontière** | Autorisation + interface sécurisée |
| Autres capteurs institutionnels | **Activer la source** | Autorisation + spécification technique |

## Comportement des boutons
Les boutons protégés restent visibles dans l'interface mais sont verrouillés tant que l'autorisation, la passerelle ou les identifiants requis ne sont pas disponibles. L'écran doit indiquer clairement : **« Autorisation requise — activation indisponible »**.

Lorsque l'autorisation officielle est obtenue, l'administrateur habilité pourra configurer la source côté serveur puis activer le bouton, sans reconstruire toute l'application.

## Contrôle côté serveur
Chaque activation protégée doit vérifier : identité de l'organisation, rôle de l'utilisateur, autorisation de la source, configuration de la passerelle, certificats/secrets nécessaires, état de santé de la connexion et journal d'audit. Les secrets ne sont jamais stockés dans l'APK.

## Sécurité et vérité des données
- aucune clé secrète dans l'APK ;
- accès par rôle et organisation ;
- journalisation des actions sensibles ;
- révocation des sessions ;
- validation humaine des alertes sensibles ;
- aucune action coercitive automatique décidée uniquement par l'IA ;
- séparation stricte entre données réelles, historiques, différées et simulations ;
- **aucune source verrouillée ou non connectée ne doit être affichée comme LIVE**.
