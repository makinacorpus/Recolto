import pandas as pd
import json
import os


def dict_to_json(dictionnary, outpath):
    """
    Exporte un dictionnaire en fichier JSON
    """
    json_object = json.dumps(dictionnary, indent=2, ensure_ascii=False)
    with open(outpath, "w") as outfile:
        outfile.write(json_object)

def load_csv_and_create_datarame(csv_compress):
    """
    Charge le csv compressé, crée le dataframe et extrait les valeurs des preciitations.
    """  
    columns_to_keep = ['LAMBX', 'LAMBY', 'DATE', 'PRENEI_Q', 'PRELIQ_Q', 'PE_Q']
    df = pd.read_csv(csv_compress, sep=";", decimal=".", compression="gzip")
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
    df_preci = df[columns_to_keep]

    print(df_preci.head())
    return df_preci

def filter_by_date(df_preci, start_date, end_date):
    """
    Conservation des enregistrements compris entre start_date et end_date.
    """
    return df_preci[(df_preci['DATE'] >= start_date) & (df_preci['DATE'] <= end_date)]

def locate_safran_points_csv(df_preci, csv_grid_safran_path, centroid_csv_json):
    "Emploi des coordonnées issues de la grille Safran."

    grid_sfr_cood = pd.read_csv(csv_grid_safran_path, sep=";", decimal=".")
    grid_sfr_cood.rename(columns={
    'LAMBX (hm)': 'LAMBX', 
    'LAMBY (hm)': 'LAMBY'
    }, inplace=True)
    
    grid_sfr_cood['GID'] = grid_sfr_cood.index + 1
    grid_sfr_cood = grid_sfr_cood[['GID', 'LAMBX', 'LAMBY']]

    #sauvegarder la liste des centres en JSON pour référence
    with open(centroid_csv_json, "w") as outfile:
        json.dump(grid_sfr_cood.to_dict(orient='records'), outfile, indent=2, ensure_ascii=False)
    
    # Réaliser le merge entre les enregistrements et les coordonnées retenues.
    df_preci_fr = df_preci.merge(grid_sfr_cood[['GID', 'LAMBX', 'LAMBY']], on=['LAMBX','LAMBY'], how='inner')

    return grid_sfr_cood, df_preci_fr


def compute_statistics(df_preci_fr):
    """
    Ajout des colonnes année et mois dans le DataFrame pour faciliter les regroupements.
    """
    df_preci_fr['YEARS'] = df_preci_fr['DATE'].dt.year.astype(str)
    df_preci_fr['MONTHS'] = df_preci_fr['DATE'].dt.to_period('M').astype(str)
    return df_preci_fr

def export_station_stats(df_preci_fr, df_coord, outfolder):
    """
    Calcul de la somme des précipitations par station (identifiée par son gid) puis export 
    des statistiques (annuelles et mensuelles) au format JSON dans le dossier output_folder.
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    
    # Boucle pour calculer les statistiques pour chaque station
    for _ , row in df_coord.iterrows():
        gid = int(row.GID)
        lambx_val, lamby_val = row.LAMBX, row.LAMBY
        print(f"Processing GID {gid} at coordinates ({lambx_val}, {lamby_val})")

        # Filtrer les données pour la station actuelle
        df_station = df_preci_fr[
            (df_preci_fr['LAMBX'] == lambx_val) &
            (df_preci_fr['LAMBY'] == lamby_val )
        ]
        
        # Calcul des statistiques annuelles
        df_years = df_station.groupby('YEARS')[['PRENEI_Q', 'PRELIQ_Q', 'PE_Q']].sum().reset_index()
        df_years = df_years.rename(columns={
            'PRENEI_Q': 'annual_PRENEI_Q',
            'PRELIQ_Q': 'annual_PRELIQ_Q',
            'PE_Q': 'annual_PE_Q'
        })
        
        # Calcul des statistiques mensuelles
        df_months = df_station.groupby('MONTHS')[['PRENEI_Q', 'PRELIQ_Q', 'PE_Q']].sum().reset_index()
        df_months = df_months.rename(columns={
            'PRENEI_Q': 'monthly_PRENEI_Q',
            'PRELIQ_Q': 'monthly_PRELIQ_Q',
            'PE_Q': 'monthly_PE_Q'
        })
        
        # Préparer le dictionnaire pour JSON
        dict_all = {
            "years": df_years.set_index('YEARS').to_dict(orient='index'),
            "months": df_months.set_index('MONTHS').to_dict(orient='index')
        }
        
        # Chemin du fichier JSON pour la station
        out_json_path = os.path.join(outfolder, f"{gid}.json")
        
        # Export en JSON
        dict_to_json(dict_all, out_json_path)

    print("Traitement terminé !")

def process_and_export_meteo_data(csv_compress, 
                                  csv_grid_safran_path, 
                                  start_date, 
                                  end_date,
                                  centroid_csv_json,
                                  output_folder):
    """
Ce script permet de traiter et d’exporter les données météorologiques de SIM Safran au format csv comprimé. 
Il réalise les opérations suivantes :

1. Chargement du CSV compressé et Création d’un DataFrame et extraction des précipitations.
2. Filtrage temporel.
3. Utilisation de la grille Safran
4. Ajout de colonnes temporelles
5. Calcul et export des statistiques

    Paramètres :
      - csv_compress (str) : Chemins vers le dossier contenant CSV compressé.
      - csv_grid_safran_path (str) : Chemin vers le fichier csv contenant la grille Safran.
      - start_date (str) : Date de début du filtrage temporel (format "YYYY-MM-DD").
      - end_date (str) : Date de fin du filtrage temporel (format "YYYY-MM-DD").
      - output_folder (str) : Dossier où seront exportés les fichiers JSON des statistiques par station.
      - centroid_csv_json : Sauvegarde la liste des centres (coordonnées uniques) en JSON.
    """
    # 1. Chargement des données CSV combinées
    df_preci = load_csv_and_create_datarame(csv_compress)
    # 2.Filtrage temporel pour ne conserver que les enregistrements entre start_date et end_date.
    df_preci_filter = filter_by_date(df_preci, start_date, end_date)
    df_coord, df_preci_fr = locate_safran_points_csv(df_preci_filter, csv_grid_safran_path, centroid_csv_json)
    # 5. Calcul des colonnes d'années et de mois (pour le regroupement)
    df_preci_fr_comp = compute_statistics(df_preci_fr)
    # 6. Calcul et export des statistiques par station en JSON
    export_station_stats(df_preci_fr_comp, df_coord, output_folder)




#######################################
# MAIN
#######################################

if __name__ == "__main__":
    # Définir les paramètres
    csv_compress ="publ/QUOT_SIM2_previous-2020-202412.csv.gz"
    csv_grid_safran_path = "public/data/coordonnees_grille_safran_lambert-2-etendu.csv"
    centroid_csv_json = "public/data/centroid_coordinates_SIM_LAMBX_LAMBY.json"
    start_date = "2024-01-01" 
    end_date   = "2024-12-31"
    output_folder = 'public/data/FR-ID-JSON_SIM_LAMBX_LAMBY'

    
    process_and_export_meteo_data(csv_compress,  
                                  csv_grid_safran_path, 
                                  start_date, 
                                  end_date,
                                  centroid_csv_json,
                                  output_folder
                                  )
