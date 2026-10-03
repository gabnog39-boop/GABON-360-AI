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
