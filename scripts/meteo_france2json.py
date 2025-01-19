import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd

def dict_to_json(dictionnary, outpath):
    """
    Exporte un dictionnaire en fichier JSON
    """
    json_object = json.dumps(dictionnary, indent=2, ensure_ascii=False)
    with open(outpath, "w") as outfile:
        outfile.write(json_object)

def load_csv_data(csv_folders):
    """
    Charge et concatène les CSV d'une ou plusieurs dossiers donnés en extrayant les métadonnées pour
    récupérer les informations géographiques (lon, lat, alt).
    """
    dfs = []  # liste des DataFrame de chaque station
    metadata_list = []  # liste pour conserver les métadonnées éventuellement nécessaires
    
    for folder in csv_folders:
        csv_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.csv')]
        for file in csv_files:
            with open(file, 'r') as f:
                meta = {}
                for line in f:
                    if '=' in line:
                        key, value = line.lstrip('#').split('=', 1)
                        meta[key.strip()] = value.strip()
            metadata_list.append(meta)
            df = pd.read_csv(file, skiprows=8, sep=';')
            df.columns = ['date', 'precipitation', 'quality']
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            
            # Ajout des informations géographiques issues des métadonnées
            df['lon'] = float(meta.get('LONGITUDE(°)', np.nan))
            df['lat'] = float(meta.get('LATITUDE (°)', np.nan))
            df['alt'] = float(meta.get('ALTITUDE (m)', np.nan))
            
            dfs.append(df)
            
    df_all = pd.concat(dfs, ignore_index=True)
    print("Nombre total d'enregistrements :", len(df_all))
    return df_all

def filter_points_in_france(df_all, geojson_path, save_coord_json=True):
    """
    Filtre les enregistrements en fonction du contour géographique (France métropolitaine + DROM)
    en effectuant un spatial join entre les points de df_all et le fichier GeoJSON.
    """
    gdf_fr = gpd.read_file(geojson_path)
    points = gpd.GeoDataFrame(df_all[['lon', 'lat']], geometry=gpd.points_from_xy(df_all['lon'], df_all['lat']))
    points.crs = gdf_fr.crs

    # Spatial join pour garder les points situés en France
    within_points = gpd.sjoin(points, gdf_fr, predicate='within', how='inner')
    within_points['lon'] = within_points.geometry.x
    within_points['lat'] = within_points.geometry.y

    # Création d'un DataFrame de coordonnées uniques avec gid
    df_coord = within_points[['lon', 'lat']].drop_duplicates().reset_index(drop=True)
    df_coord['gid'] = df_coord.index + 1
    df_coord = df_coord[['gid', 'lon', 'lat']]
    
    # Réaliser le merge entre les enregistrements et les coordonnées retenues.
    df_all_fr = df_all.merge(df_coord[['gid', 'lon', 'lat']], on=['lon', 'lat'], how='inner')
    print(df_all)
    
    # Optionnel : sauvegarder la liste des centres en JSON pour référence
    if save_coord_json:
        coord_json_file = "public/data/centroid_coordinates_meteo_france.json"
        with open(coord_json_file, "w") as outfile:
            json.dump(df_coord.to_dict(orient='records'), outfile, indent=2, ensure_ascii=False)
    
    return df_coord, df_all_fr

def filter_by_date(df, start_date, end_date):
    """
    Filtre les enregistrements du DataFrame en fonction de la plage de dates donnée.
    """
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

def compute_statistics(df):
    """
    Ajoute les colonnes 'année' et 'mois' au DataFrame et retourne celui-ci.
    """
    df['année'] = df['date'].dt.year.astype(str)
    df['mois'] = df['date'].dt.to_period('M').astype(str)
    return df

def export_station_stats(df_all_fr, df_coord, outfolder):
    """
    Pour chaque station (identifiée par gid) dans df_coord, calcule la somme annuelle et mensuelle des précipitations,
    construit un dictionnaire structuré et l'exporte en fichier JSON dans le dossier outfolder.
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    
    for idx, row in df_coord.iterrows():
        gid = int(row.gid)
        lon_val, lat_val = row.lon, row.lat
        print(f"Processing gid {gid} ({lon_val}, {lat_val})")
        
        # Sélectionner les enregistrements correspondant à cette station
        df_station = df_all_fr[(df_all_fr['lon'].round(3) == round(lon_val, 3)) &
                               (df_all_fr['lat'].round(3) == round(lat_val, 3))]
        
        # Calcul de la somme annuelle et mensuelle
        df_years = df_station.groupby('année')['precipitation'].sum().reset_index().rename(
            columns={'precipitation': 'annual'}
        )
        df_months = df_station.groupby('mois')['precipitation'].sum().reset_index().rename(
            columns={'precipitation': 'monthly'}
        )
        
        # Création du dictionnaire final
        dict_all = {
            "years": dict(zip(df_years['année'], df_years['annual'])),
            "months": dict(zip(df_months['mois'], df_months['monthly']))
        }
        
        # Export en JSON
        out_json_path = os.path.join(outfolder, f"{gid}.json")
        dict_to_json(dict_all, out_json_path)

def process_and_export_meteo_data(csv_folders, geojson_path, start_date, end_date, output_folder, save_coord_json=True):
    """
    Traite et exporte les données météorologiques issues de plusieurs dossiers CSV :
    
      1. Chargement et concaténation des fichiers CSV.
      2. Filtrage spatial pour ne conserver que les enregistrements situés en France 
         (France métropolitaine et DROM), en utilisant le fichier GeoJSON indiqué.
      3. Filtrage temporel pour ne conserver que les enregistrements entre start_date et end_date.
      4. Ajout des colonnes 'année' et 'mois' dans le DataFrame, afin de faciliter les regroupements.
      5. Calcul de la somme des précipitations par station (identifiée par gid) 
         et export des statistiques (annuelles et mensuelles) au format JSON dans le dossier output_folder.
         
    En option, le paramètre save_coord_json permet de sauvegarder la liste des centres (coordonnées uniques)
    dans un fichier JSON de référence.
    
    Paramètres :
      - csv_folders (list of str) : Liste des chemins vers les dossiers contenant les fichiers CSV.
      - geojson_path (str) : Chemin vers le fichier GeoJSON contenant le contour de la France.
      - start_date (str) : Date de début du filtrage temporel (format "YYYY-MM-DD").
      - end_date (str) : Date de fin du filtrage temporel (format "YYYY-MM-DD").
      - output_folder (str) : Dossier où seront exportés les fichiers JSON des statistiques par station.
      - save_coord_json (bool, optionnel) : Si True, sauvegarde la liste des centres (coordonnées uniques) en JSON.
    """
    # 1. Chargement des données CSV combinées
    df_all = load_csv_data(csv_folders)
    # 2. Filtrage spatial : conserver uniquement les enregistrements en France
    df_coord, df_all_fr = filter_points_in_france(df_all, geojson_path, save_coord_json)
    # 3. Filtrage temporel
    df_all_fr = filter_by_date(df_all_fr, start_date, end_date)
    # 4. Calcul des colonnes d'années et de mois (pour le regroupement)
    df_all_fr = compute_statistics(df_all_fr)
    # 5. Calcul et export des statistiques par station en JSON
    export_station_stats(df_all_fr, df_coord, output_folder)

#######################################
# MAIN
#######################################

if __name__ == "__main__":
    # Définir les paramètres
    csv_folders = ["public/data/SQR_RR_metropole", "public/data/SQR_RR_Outremer"]
    geojson_path = "public/data/france-drom.geojson"
    start_date = "2010-01-01" 
    end_date   = "2024-12-31"
    output_folder = 'public/data/FR-ID-JSON'
    process_and_export_meteo_data(csv_folders, 
                                  geojson_path, 
                                  start_date, 
                                  end_date, 
                                  output_folder, 
                                  save_coord_json=True)