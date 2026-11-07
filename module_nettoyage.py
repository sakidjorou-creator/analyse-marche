import pandas as pd
import json
import os

def charger_et_nettoyer():
    journal = []
    dossier = "donnees/"
    
    print("--- 1. CHARGEMENT ET NETTOYAGE DES DONNÉES ---")
    
    # 1. Catalogue de référence
    try:
        df_ref = pd.read_csv(f"{dossier}catalogue_reference.csv", encoding="utf-8")
        print(f"[OK] Catalogue de référence chargé : {len(df_ref)} produits.")
    except Exception as e:
        print(f"[ERREUR] Catalogue de référence : {e}")
        return None, None, None, None, []
    
    # 2. Marché Lagune
    try:
        df_lagune = pd.read_csv(f"{dossier}marche_lagune.csv", sep=";", encoding="utf-8")
        
        def nettoyer_prix_lagune(val):
            if pd.isna(val):
                return None
            val_str = str(val).replace('\xa0', '').replace('\u202f', '').replace(' ', '').replace('FCFA', '')
            try:
                return float(val_str)
            except ValueError:
                return None
                
        df_lagune['prix_net'] = df_lagune['prix'].apply(nettoyer_prix_lagune)
        
        for idx, row in df_lagune.iterrows():
            if pd.isna(row['prix_net']):
                journal.append(f"[Marché Lagune] Ligne {idx} ({row.get('designation', 'Inconnu')}) : Prix invalide ou manquant")
        
        print(f"[OK] Marché Lagune chargé : {len(df_lagune)} lignes.")
    except Exception as e:
        print(f"[ERREUR] Marché Lagune : {e}")
        df_lagune = None

    # 3. Baobab Shop
    try:
        with open(f"{dossier}baobab_shop.json", "r", encoding="utf-8") as f:
            baobab_data = json.load(f)
        df_baobab = pd.json_normalize(baobab_data["items"])
        
        df_baobab['prix_net'] = df_baobab['pricing.amount'] + df_baobab['pricing.delivery_fee']
        
        for idx, row in df_baobab.iterrows():
            if pd.isna(row['pricing.amount']):
                journal.append(f"[Baobab Shop] SKU {row.get('sku')} : Montant manquant (null)")
                
        print(f"[OK] Baobab Shop chargé : {len(df_baobab)} articles.")
    except Exception as e:
        print(f"[ERREUR] Baobab Shop : {e}")
        df_baobab = None

    # 4. Comptoir Ivoire
    try:
        excel_path = f"{dossier}comptoir_ivoire.xlsx"
        df_comptoir = pd.read_excel(excel_path, sheet_name="Tarifs octobre 2026", skiprows=2)
        
        def calculer_prix_comptoir(row):
            cat = row['Prix catalogue (FCFA)']
            rem = row['Remise (%)']
            if pd.isna(cat):
                return None
            remise_val = rem if not pd.isna(rem) else 0
            try:
                return float(str(cat).replace('\xa0', '').replace('\u202f', '').replace(' ', '')) * (1 - float(remise_val) / 100)
            except ValueError:
                return None
            
        df_comptoir['prix_net'] = df_comptoir.apply(calculer_prix_comptoir, axis=1)
        
        for idx, row in df_comptoir.iterrows():
            if pd.isna(row['Prix catalogue (FCFA)']):
                journal.append(f"[Comptoir Ivoire] Ligne {idx} : Prix catalogue manquant")
                
        print(f"[OK] Comptoir Ivoire chargé : {len(df_comptoir)} articles.")
    except Exception as e:
        print(f"[ERREUR] Comptoir Ivoire : {e}")
        df_comptoir = None

    print(f"\n--- JOURNAL DES ANOMALIES ({len(journal)} anomalies consignées) ---")
    for anomaly in journal[:3]:
        print(f"  - {anomaly}")
        
    return df_ref, df_lagune, df_baobab, df_comptoir, journal