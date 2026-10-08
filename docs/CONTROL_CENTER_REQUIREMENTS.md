# Exigences du centre national de situation

## 1. Vue territoriale

- carte du Gabon avec couches activables ;
- provinces, départements, communes, localités ;
- parcs et autres zones protégées ;
- routes, pistes, cours d'eau et autres couches SIG autorisées ;
- position des missions et événements avec niveau de précision adapté au rôle ;
- historique temporel et comparaison de périodes.

## 2. Cycle de traitement d'une information

```text
Source autorisée
    ↓
Réception / horodatage
    ↓
Contrôle qualité
    ↓
Analyse IA
    ↓
Détection ou corrélation proposée
    ↓
Niveau de confiance + état
    ↓
Vérification humaine si nécessaire
    ↓
Événement / alerte / mission / rapport
    ↓
Audit et archivage
```

L'IA assiste l'opérateur ; elle ne doit pas transformer seule une hypothèse en fait établi.

## 3. Gestion de crise

Prévoir des objets structurés pour :

- incidents ;
- crises ;
- plans d'action ;
- responsables ;
- missions ;
- ressources ;
- chronologie ;
- comptes rendus ;
- pièces justificatives ;
- clôture et retour d'expérience.

## 4. Résilience

Le système doit prévoir :

- fonctionnement dégradé et hors-ligne côté terrain ;
- file de synchronisation ;
- idempotence ;
- reprise après coupure ;
- contrôle des doublons ;
- sauvegardes et restauration testée ;
- surveillance de la santé des services et sources.

## 5. Qualité des données

Chaque source doit pouvoir indiquer :

- identité de la source ;
- autorisation ;
- dernière réception ;
- latence ;
- disponibilité ;
- couverture déclarée ;
- qualité ;
- statut réel/simulation ;
- date de dernière vérification.

La disponibilité technique d'une source ne constitue pas une preuve de couverture géographique continue.

## 6. Protection des personnes

- minimiser les données personnelles ;
- appliquer le principe du moindre privilège ;
- masquer les données sensibles selon le rôle ;
- conserver une trace des accès aux données sensibles ;
- interdire les usages non autorisés de reconnaissance ou de suivi individuel ;
- prévoir des mécanismes de suppression, rétention et archivage conformes au cadre juridique applicable.

## 7. Gouvernance

Le compte propriétaire doit pouvoir :

- administrer les rôles ;
- suspendre un service ;
- révoquer des sessions ;
- consulter les audits ;
- approuver les changements sensibles ;
- maintenir une séparation entre administration, analyse et exploitation terrain.

Toute action sensible doit être traçable avec acteur, date/heure, objet, résultat et justification lorsque nécessaire.

## 8. Interface

Le tableau de bord doit privilégier une lecture rapide :

- situation nationale ;
- alertes ;
- événements ;
- missions ;
- état des sources ;
- cybersécurité ;
- météo ;
- rapports ;
- assistant/avatar ;
- commandes vocales et textuelles ;
- mode démonstration clairement signalé.


## 9. Agents spécialisés et relais proactif vers l'avatar central

Chaque page et chaque option doit déclarer son agent spécialisé, son événement, ses droits, ses sources et sa politique de validation. Un registre technique ne signifie pas à lui seul qu'un modèle autonome est déployé : chaque agent doit être relié à un moteur ou à une règle réellement exécutée et testée.

Flux obligatoire :

```text
Source autorisée / action utilisateur / contrôle technique
  → horodatage et contrôle qualité
  → IA spécialisée de la page et de l'option
  → événement structuré, preuve, confiance et statut
  → relais central et corrélation
  → avatar central
  → notification visible à l'humain, sans question préalable
  → synthèse vocale si disponible, avec priorité et file d'attente
```

Règles du relais :

- transmettre à l'avatar les informations nouvelles, les résultats négatifs utiles, les erreurs, les pertes de connexion et les états de santé des sources ;
- ne pas attendre que l'humain ouvre la page ou pose une question ;
- afficher la source, la date/heure, le statut réel/historique/simulé, le niveau de confiance et les preuves disponibles ;
- prioriser les alertes critiques, puis importantes, puis les informations ordinaires ; regrouper les événements répétitifs pour éviter de saturer la voix ;
- conserver l'historique des notifications et permettre de consulter l'événement d'origine ;
- en l'absence de données, signaler explicitement « aucune donnée nouvelle reçue » ou « source indisponible » sans inventer d'observation ;
- informer sans autorisation de lecture ne signifie jamais contourner les rôles d'accès aux données sensibles ;
- toute commande d'action sensible (contrôle d'un drone/caméra, modification de droits, suppression, activation de service, mesure coercitive) exige les permissions et confirmations prévues ; aucune action sensible ne doit être déclenchée par la seule prédiction d'une IA.

## 10. Modules complémentaires à vérifier et livrer

- fusion et corrélation multi-source ;
- qualité, fraîcheur, couverture et provenance des données ;
- gestion de crise, chronologie, responsables, plans d'action et retour d'expérience ;
- preuves et intégrité des médias/observations ;
- mode hors-ligne, file de synchronisation, reprise et déduplication ;
- sauvegardes, restauration vérifiée et état des services ;
- erreurs de fonctionnement, maintenance et santé des connecteurs ;
- notifications proactives de toutes les pages vers l'avatar central ;
- tests automatiques des pages, options, boutons, droits, relais et états sans connexion.

Ces modules doivent être marqués « intégré », « testé », « à réparer » ou « dépendant d'une source externe ». Ne pas les déclarer opérationnels uniquement parce qu'ils figurent dans un registre.
