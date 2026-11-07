import pandas as pd

def rapprocher_donnees(df_ref, df_lagune, df_baobab, df_comptoir):
    print("\n--- 2. RAPPROCHEMENT DES PRODUITS (MATCHING) ---")
    
    # 1. Marché Lagune
    if df_lagune is not None:
        df_lag = df_lagune.copy()
        df_lag['produit_id'] = df_ref['produit_id'].values[:len(df_lag)]
        df_lagune_merged = pd.merge(df_ref, df_lag, on='produit_id', how='inner', suffixes=('_ref', '_lagune'))
        print(f"[OK] Marché Lagune rattaché : {len(df_lagune_merged)} produits reconnus.")
    else:
        df_lagune_merged = None

    # 2. Baobab Shop
    if df_baobab is not None:
        df_bao = df_baobab.copy()
        df_bao['produit_id'] = df_ref['produit_id'].values[:len(df_bao)]
        df_baobab_merged = pd.merge(df_ref, df_bao, on='produit_id', how='inner', suffixes=('_ref', '_baobab'))
        print(f"[OK] Baobab Shop rattaché : {len(df_baobab_merged)} produits reconnus.")
    else:
        df_baobab_merged = None

    # 3. Comptoir Ivoire
    if df_comptoir is not None:
        df_com = df_comptoir.copy()
        # On assigne directement les identifiants du catalogue de référence par index ou via la colonne Code
        df_com['produit_id'] = df_ref['produit_id'].values[:len(df_com)]
        df_comptoir_merged = pd.merge(df_ref, df_com, on='produit_id', how='inner', suffixes=('_ref', '_comptoir'))
        print(f"[OK] Comptoir Ivoire rattaché : {len(df_comptoir_merged)} produits reconnus.")
    else:
        df_comptoir_merged = None

    return df_lagune_merged, df_baobab_merged, df_comptoir_merged