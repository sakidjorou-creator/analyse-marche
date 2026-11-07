import os
import pandas as pd

def comparer_prix(df_ref, df_lagune, df_baobab, df_comptoir):
    print("\n--- 3. COMPARATIF DES PRIX ET ANALYSE ---")
    
    try:
        # Base : Catalogue de référence
        df_comparatif = df_ref[['produit_id', 'nom', 'categorie']].copy()
        
        # 1. Intégration Marché Lagune
        if df_lagune is not None and 'prix_net' in df_lagune.columns:
            temp_lag = df_lagune[['produit_id', 'prix_net']].rename(columns={'prix_net': 'Prix_Lagune'})
            df_comparatif = pd.merge(df_comparatif, temp_lag, on='produit_id', how='left')
        else:
            df_comparatif['Prix_Lagune'] = None

        # 2. Intégration Baobab Shop
        if df_baobab is not None and 'prix_net' in df_baobab.columns:
            temp_bao = df_baobab[['produit_id', 'prix_net']].rename(columns={'prix_net': 'Prix_Baobab'})
            df_comparatif = pd.merge(df_comparatif, temp_bao, on='produit_id', how='left')
        else:
            df_comparatif['Prix_Baobab'] = None

        # 3. Intégration Comptoir Ivoire
        if df_comptoir is not None and 'prix_net' in df_comptoir.columns:
            temp_com = df_comptoir[['produit_id', 'prix_net']].rename(columns={'prix_net': 'Prix_Comptoir'})
            df_comparatif = pd.merge(df_comparatif, temp_com, on='produit_id', how='left')
        else:
            df_comparatif['Prix_Comptoir'] = None

        prix_cols = ['Prix_Lagune', 'Prix_Baobab', 'Prix_Comptoir']

        # Détermination sécurisée du meilleur prix (exclut les ruptures et prix non exploitables)
        def trouver_moins_cher(row):
            valides = {}
            for col in prix_cols:
                nom_enseigne = col.replace('Prix_', '')
                valeur = row[col]
                # Vérifie que le prix existe et est strictement supérieur à 0 (pas de prix nul/négatif/rupture)
                if pd.notna(valeur) and valeur > 0:
                    valides[nom_enseigne] = valeur

            if not valides:
                return "Indisponible", None
            
            min_enseigne = min(valides, key=valides.get)
            return min_enseigne, valides[min_enseigne]

        resultats_min = df_comparatif.apply(trouver_moins_cher, axis=1)
        df_comparatif['Enseigne_Moins_Chere'] = [res[0] for res in resultats_min]
        df_comparatif['Meilleur_Prix'] = [res[1] for res in resultats_min]

        print(f"[OK] Comparatif sécurisé généré avec succès pour {len(df_comparatif)} produits.")
        return df_comparatif

    except Exception as e:
        print(f"[ERREUR] Lors de la comparaison sécurisée : {e}")
        return None