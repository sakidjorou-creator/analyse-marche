# Projet d'Analyse Comparative de Marché

## 1. Introduction et Objectif
Ce projet académique consiste à concevoir un programme Python modulaire permettant d'analyser et de comparer les prix de plusieurs boutiques en ligne face à un catalogue de référence, afin d'identifier la meilleure offre par produit, d'analyser un panier d'achat type et d'étudier l'historique des prix.

## 2. Architecture du Projet
Le code est structuré en plusieurs modules indépendants et spécialisés pour garantir robustesse, maintenabilité et zéro erreur d'exécution :
- **`main.py`** : Script orchestrateur centralisant le lancement du pipeline complet.
- **`module_nettoyage.py`** : Chargement des sources hétérogènes (CSV, JSON, Excel), normalisation des données (casse, espaces) et consignation des anomalies dans un journal.
- **`module_matching.py`** : Rapprochement exact des produits par identifiant de référence.
- **`module_comparatif.py`** : Comparaison des prix, calcul des écarts, gestion des ruptures de stock / prix non exploitables, et analyse du panier de rentrée.
- **`module_historique.py`** : Analyse temporelle des prix (comparaison de la semaine du Black Friday vs moyenne annuelle) et mesure de la complexité algorithmique.

## 3. Gestion des Pièges et Robustesse
- **Casse et espaces** : Normalisation systématique des chaînes de caractères.
- **Prix manquants ou invalides** : Détection, exclusion et consignation dans le journal des anomalies.
- **Ruptures de stock** : Exclusion stricte des produits indisponibles ou dont le prix est nul de la sélection de l'offre la moins chère.

## 4. Résultats et Exportation
Les résultats finaux de l'analyse comparative sont automatiquement exportés et mis à jour sous forme de rapport structuré dans le sous-dossier :
- `resultats/comparatif_final.csv`

## 5. Instructions d'Exécution
Pour lancer l'intégralité du pipeline d'analyse, assure-toi d'avoir installé les dépendances nécessaires (`pandas`, `openpyxl`) puis exécute la commande suivante dans ton terminal :
```bash
python main.py