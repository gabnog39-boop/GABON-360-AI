# GABON 360 AI

**Centre intégré de situation et de supervision territoriale du Gabon**

Concepteur et initiateur : **Gabriel Ngoua Obame**

## Objectif

GABON 360 AI a vocation à réunir dans une seule application les fonctions de cartographie, situation territoriale, observation autorisée, événements, alertes, missions, rapports, statistiques, météo, assistant IA et traçabilité opérationnelle.

Le système doit distinguer en permanence :

- données réellement reçues ;
- données en cours d'analyse ;
- détections ou anomalies proposées par l'IA ;
- informations à vérifier ;
- informations validées par un opérateur habilité ;
- données de démonstration ou de simulation.

Aucune donnée simulée ne doit être présentée comme une observation réelle.

## Architecture cible

```text
GABON 360 AI
├── android/                 # application Android unifiée
├── server/                  # API, authentification, logique métier
├── gis/                     # couches géographiques et contrats de données
├── docs/                    # architecture, sécurité et exploitation
└── .github/workflows/       # compilation et contrôles qualité
```

Le dépôt contient actuellement le projet Android consolidé utilisé par le workflow de compilation. La consolidation progressive vers cette architecture cible doit se faire sans casser la version fonctionnelle existante.

## Fonctions prioritaires

1. Centre national de situation
2. Carte du Gabon et couches administratives, parcs, routes, cours d'eau, villes et autres données SIG autorisées
3. Événements, alertes et chronologie
4. Missions et suivi des opérations autorisées
5. Sources d'observation et état de santé des sources
6. Moteur IA d'analyse et de corrélation avec validation humaine
7. Rapports et preuves avec traçabilité
8. Cybersécurité, contrôle d'accès, audit et révocation
9. Assistant/avatar permanent
10. Mode hors-ligne avec synchronisation contrôlée
11. Tableau de qualité et de disponibilité des données
12. Météo et autres services externes via fournisseurs explicitement configurés

## Principes de sécurité

- contrôle d'accès par rôle et organisation ;
- authentification forte pour les fonctions sensibles ;
- secrets uniquement côté serveur ;
- chiffrement des communications ;
- journal d'audit et traçabilité ;
- validation humaine des décisions sensibles ;
- aucune surveillance clandestine ni suivi individuel non autorisé ;
- aucune action coercitive automatique déclenchée uniquement par une prédiction IA ;
- statut explicite de chaque source et de chaque information ;
- séparation stricte entre démonstration et données opérationnelles.

## État actuel

Le workflow GitHub Actions construit l'APK à partir du ZIP Android consolidé canonique. Les évolutions doivent privilégier un produit unique et maintenable plutôt qu'une multiplication de versions visibles.

Voir `docs/CONTROL_CENTER_REQUIREMENTS.md` et `docs/SECURITY_BASELINE.md` pour les exigences complémentaires.
