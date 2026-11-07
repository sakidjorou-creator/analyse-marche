import time
import pandas as pd

def analyser_historique():
    print("\n--- 7. HISTORIQUE ET BLACK FRIDAY ---")
    debut_chrono = time.time()
    
    try:
        # Chargement de l'historique (plus de 20 000 lignes)
        chemin_hist = "donnees/historique_prix.csv"
        df_hist = pd.read_csv(chemin_hist)
        print(f"[OK] Fichier historique chargé : {len(df_hist)} lignes analysées.")
        
        # Conversion de la colonne date en datetime
        df_hist['date'] = pd.to_datetime(df_hist['date'])
        
        # Filtrer la semaine du Black Friday (24 au 30 novembre 2025)
        mask_bf = (df_hist['date'] >= '2025-11-24') & (df_hist['date'] <= '2025-11-30')
        df_bf = df_hist[mask_bf]
        
        print("\nComparaison du prix moyen annuel vs Semaine Black Friday (24-30 nov 2025) par enseigne :")
        if 'enseigne' in df_hist.columns and 'prix' in df_hist.columns:
            moyenne_annuelle = df_hist.groupby('enseigne')['prix'].mean()
            moyenne_bf = df_bf.groupby('enseigne')['prix'].mean()
            
            comparatif_hist = pd.DataFrame({
                'Prix Moyen Annuel (FCFA)': moyenne_annuelle,
                'Prix Moyen Black Friday (FCFA)': moyenne_bf
            })
            comparatif_hist['Écart (%)'] = ((comparatif_hist['Prix Moyen Black Friday'] - comparatif_hist['Prix Moyen Annuel']) / comparatif_hist['Prix Moyen Annuel']) * 100
            print(comparatif_hist.round(2))
        
        # --- SECTION 8 : COMPLEXITÉ ET TEMPS D'EXÉCUTION ---
        fin_chrono = time.time()
        temps_execution = fin_chrono - debut_chrono
        
        print("\n--- 8. COMPLEXITÉ ET PERFORMANCE ---")
        print(f"Mesure du temps d'exécution sur l'historique (> 20 000 lignes) : {temps_execution:.4f} secondes.")
        print("Choix de structures de données : Utilisation de DataFrames pandas vectorisés et de masques booliens pour optimiser le filtrage temporel et s'affranchir des boucles lentes.")
        
    except Exception as e:
        print(f"[ERREUR] Lors de l'analyse historique : {e}")