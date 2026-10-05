# Surveillance autonome GABON 360 AI

Le centre surveille automatiquement le territoire du Gabon à partir de sources publiques ou autorisées.

## Cycle

1. Découverte des nouvelles observations Sentinel-2 dans le catalogue public.
2. Déduplication et conservation d'un état local.
3. Lorsqu'un processeur autorisé fournit des indicateurs dérivés, comparaison temporelle avec la référence précédente.
4. Analyse centrale et génération de candidats d'anomalie.
5. Les candidats sont publiés avec niveau de confiance, preuve, géométrie et statut `À vérifier`.
6. L'application Android peut récupérer le contrat de situation et centrer la carte sur un événement.

## Limites

- Le catalogue public n'est pas une vidéo satellite continue.
- Une entrée de catalogue seule ne constitue pas une alerte.
- Les alertes nécessitent une analyse d'observation et une validation humaine.
- Les flux caméra, drone, satellite protégés ou gouvernementaux restent désactivés tant qu'une connexion autorisée n'est pas configurée.
- Aucun suivi individuel ni action coercitive automatique n'est effectué.
