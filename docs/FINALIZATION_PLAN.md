# GABON 360 AI — Finalisation fonctionnelle

## Objectif
Faire de GABON 360 AI un centre de situation territorial moderne, fiable, sécurisé et exploitable par des utilisateurs autorisés.

## Périmètre fonctionnel
- Tableau de bord national avec carte du Gabon.
- Couches SIG : provinces, départements, communes, localités, parcs, routes, cours d'eau et autres couches officiellement disponibles.
- Événements, alertes, missions, incidents et rapports.
- Historique temporel et comparaison des situations.
- État des sources : connectée, différée, historique, simulée ou indisponible.
- Assistant IA et avatar permanent avec statut explicite de la source des informations.
- Centre technique : API, base de données, synchronisation, stockage, cartographie, météo et sources autorisées.
- Mode dégradé et synchronisation différée pour les équipes autorisées sur le terrain.
- Audit complet des actions sensibles.

## Sécurité opérationnelle
Le système doit détecter et signaler des anomalies ou événements potentiels, mais toute qualification sensible et toute intervention restent soumises à une validation humaine et aux autorités compétentes.

Les fonctions de sécurité doivent inclure RBAC, MFA pour comptes privilégiés, sessions révocables, protection contre la répétition de requêtes, limitation de débit, séparation des environnements, chiffrement approprié, sauvegardes testées et journal d'audit intègre.

## Règle de vérité des données
Aucune interface ne doit présenter comme « LIVE » une donnée qui n'est pas réellement reçue d'une source connectée et autorisée. Les données simulées, historiques, différées et indisponibles doivent être clairement identifiées.

## Critères de finition
1. L'application Android se compile sans erreur.
2. Le tableau de bord s'ouvre et fonctionne hors ligne sur ses fonctions locales.
3. La carte et ses couches sont navigables et clairement identifiées.
4. Les événements ouvrent une fiche opérationnelle et conservent leur provenance.
5. Les alertes nécessitant une décision affichent explicitement le besoin de validation humaine.
6. Les modules rapports, missions, situation nationale et santé technique sont accessibles.
7. Les fonctions sensibles sont protégées par les rôles et l'audit.
8. Un APK final est produit par GitHub Actions et vérifié avant diffusion.
9. Les données et capacités réellement connectées sont distinguées des fonctions de démonstration.

## Priorité
La priorité est une version cohérente et fonctionnelle du produit unique, plutôt que l'accumulation de versions historiques visibles par l'utilisateur final.
