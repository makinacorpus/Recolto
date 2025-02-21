import pandas as pd
import geopandas as gpd
from pyproj import Transformer
import json
import os


def dict_to_json(dictionnary, outpath):
    """
    Exporte un dictionnaire en fichier JSON
    """
    json_object = json.dumps(dictionnary, indent=2, ensure_ascii=False)
    with open(outpath, "w") as outfile:
        outfile.write(json_object)


def load_csv_and_create_dataframe(csv_compress_list, pc_pierrick=False):
    """
    Charge le csv compressé, crée le dataframe et extrait les valeurs des
    precipitations.
    """  
    columns_to_keep = [
        'LAMBX', 'LAMBY', 'DATE', 'PRENEI_Q', 'PRELIQ_Q', 'PE_Q'
    ]
    dtypes = {
        'LAMBX': 'float32',
        'LAMBY': 'float32',
        'DATE': 'str',
        'PRENEI_Q': 'float32',
        'PRELIQ_Q': 'float32',
        'PE_Q': 'float32'
    }
    df_list = []

    # for each file in the list
    for file in csv_compress_list:
        if pc_pierrick:
            df = pd.read_csv(
                file,
                sep=";",
                encoding="latin1",
                usecols=columns_to_keep,
                dtype=dtypes
            )
        else:
            df = pd.read_csv(
                file,
                sep=";",
                decimal=".",
                compression="gzip",
                usecols=columns_to_keep,
                dtype=dtypes
            )
        df_list.append(df)
        print(f"\nLoaded {file} with {len(df)} lines.")

    # Concatenate the dataframes
    df = pd.concat(df_list, ignore_index=True)

    # Convert DATE to datetime
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')
    print(df.head())
    return df


def filter_by_date(df_preci, start_date, end_date):
    """
    Conservation des enregistrements compris entre start_date et end_date.
    """
    return df_preci[
        (df_preci['DATE'] >= start_date) & (df_preci['DATE'] <= end_date)
    ]


def convert_lambert2_to_long_lat(df_preci):
    """
    Conversion de coordonnées lambert etendu 2 en longitude et  latitude
    """

    # Configurer le transformateur pour passer de EPSG:27572 (Lambert II
    # étendu) à EPSG:4326 (WGS 84)
    # Appliquer la transformation, x100 pour convertir les coordonnées
    # Lambert (hm) en mètres
    transformer = Transformer.from_crs(
        "EPSG:27572",
        "EPSG:4326",
        always_xy=True
    )
    df_preci = df_preci.copy()
    df_preci['LON'], df_preci['LAT'] = transformer.transform(
        df_preci['LAMBX'] * 100,
        df_preci['LAMBY'] * 100
    )
    columns= [
        'LAMBX', 'LAMBY', 'LON', 'LAT', 'DATE', 'PRENEI_Q', 'PRELIQ_Q', 'PE_Q'
    ]
    df_preci = df_preci[columns].round(3)
    print(df_preci.head())
    return df_preci


def locate_safran_points_geojson(df_preci, geojson_path, centroid_geojson_json):
    """
    Filtre les enregistrements en fonction du contour géographique choisie
    """

    gdf_fr = gpd.read_file(geojson_path) 
    points = gpd.GeoDataFrame(
        df_preci[['LON', 'LAT']],
        geometry=gpd.points_from_xy(df_preci['LON'], df_preci['LAT']),
        crs="EPSG:4326" 
    )

    # Vérifiez le CRS de la couche France (gdf_fr.crs) :
    points = points.to_crs(gdf_fr.crs)

    # Spatial join pour garder les points situés en France
    within_points = gpd.sjoin(points, gdf_fr, predicate='within', how='inner')
    within_points['LON'] = within_points.geometry.x
    within_points['LAT'] = within_points.geometry.y

    # Création d'un DataFrame de coordonnées uniques avec gid
    df_coord = within_points[
        ['LON', 'LAT']
    ].drop_duplicates().reset_index(drop=True)
    df_coord['GID'] = df_coord.index + 1
    df_coord = df_coord[['GID', 'LON', 'LAT']]

    # Sauvegarder la liste des centres en JSON pour référence
    with open(centroid_geojson_json, "w") as outfile:
        json.dump(
            df_coord.to_dict(orient='records'),
            outfile,
            indent=2,
            ensure_ascii=False
        )

    # Réaliser le merge entre les enregistrements et les coordonnées retenues.
    df_preci_fr = df_preci.merge(
        df_coord[['GID', 'LON', 'LAT']],
        on=['LON', 'LAT'],
        how='inner'
    )
    print(df_preci_fr.head())

    return gdf_fr, df_coord, df_preci_fr


def compute_statistics(df_preci_fr):
    """
    Ajoute les colonnes 'année' et 'mois' au DataFrame et retourne celui-ci.
    """
    df_preci_fr['YEARS'] = df_preci_fr['DATE'].dt.year.astype(str)
    df_preci_fr['MONTHS'] = df_preci_fr['DATE'].dt.to_period('M').astype(str)
    return df_preci_fr


def export_station_stats(df_preci_fr_comp, df_coord, outfolder):
    """
    Pour chaque station (identifiée par gid) dans df_coord, calcule la somme
    annuelle et mensuelle des précipitations,
    construit un dictionnaire structuré et l'exporte en fichier JSON dans le dossier outfolder.
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    
    # Boucle pour calculer les statistiques pour chaque station
    for _ , row in df_coord.iterrows():
        gid = int(row.GID)
        lon_val, lat_val = row.LON, row.LAT
        print(f"Processing GID {gid} at coordinates ({lon_val}, {lat_val})")

        # Filtrer les données pour la station actuelle
        df_station = df_preci_fr_comp[
            (df_preci_fr_comp['LON'] == lon_val) &
            (df_preci_fr_comp['LAT'] == lat_val)
        ]
        
        # Calcul des statistiques annuelles
        df_years = df_station.groupby('YEARS')[
            ['PRENEI_Q', 'PRELIQ_Q', 'PE_Q']
        ].sum().reset_index()
        df_years = df_years.rename(columns={
            'PRENEI_Q': 'annual_PRENEI_Q',
            'PRELIQ_Q': 'annual_PRELIQ_Q',
            'PE_Q': 'annual_PE_Q'
        })
        
        # Calcul des statistiques mensuelles
        df_months = df_station.groupby('MONTHS')[
            ['PRENEI_Q', 'PRELIQ_Q', 'PE_Q']
        ].sum().reset_index()
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


def process_and_export_meteo_data(
    csv_compress_list,
    geojson_path,
    start_date,
    end_date,
    centroid_geojson_json,
    output_folder,
    pc_pierrick=False
):
    """
    Ce script permet de traiter et d’exporter les données météorologiques de
    SIM Safran au format csv comprimé. 
    Il réalise les opérations suivantes :

    1. Chargement du CSV compressé et Création d’un DataFrame et extraction
    des précipitations.
    2. Filtrage temporel.
    3. Conversion lambert en lon/lat
    4. Filtre les enregistrements en fonction du contour géographique 
    5. Ajout de colonnes temporelles
    5. Calcul et export des statistiques

    Paramètres :
    - csv_compress_list (str) : Chemins vers le dossier contenant CSV compressé.
    - geojson_path(str) : Chemin vers le fichier geojson contenant la grille.
    - start_date (str) : Date de début du filtrage temporel (format
    "YYYY-MM-DD").
    - end_date (str) : Date de fin du filtrage temporel (format "YYYY-MM-DD").
    - output_folder (str) : Dossier où seront exportés les fichiers JSON
    des statistiques par station.
    - centroid_geojson_json: Sauvegarde la liste des centres
    (coordonnées uniques) en JSON.
    """
    # 1. Chargement des données CSV combinées
    df_preci = load_csv_and_create_dataframe(csv_compress_list, pc_pierrick)

    # 2. Filtrage temporel
    df_preci_filter = filter_by_date(df_preci, start_date, end_date)

    # 3.  Conversion en longitude et altitude
    df_preci_conv = convert_lambert2_to_long_lat(df_preci_filter)

    # 4. Filtrage spatial : conserver uniquement les enregistrements en France
    _, df_coord, df_preci_fr = locate_safran_points_geojson(
        df_preci_conv,
        geojson_path,
        centroid_geojson_json
    )

    # 5. Calcul des colonnes d'années et de mois (pour le regroupement)
    df_preci_fr_comp = compute_statistics(df_preci_fr)

    # 6. Calcul et export des statistiques par station en JSON
    export_station_stats(df_preci_fr_comp, df_coord, output_folder)


#######################################
# MAIN
#######################################

if __name__ == "__main__":

    # Script sur PC de Pierrick
    pc_pierrick = True
    print("Script sur pc de Pierrick")
    print("\nCurrent working directory:", os.getcwd())

    # Définir les paramètres
    # csv_compress ="public/data/QUOT_SIM2_previous-2020-202412.csv.gz"
    csv_compress_list =[
        "../.data/meteo_france/QUOT_SIM2_previous-2020-202412.csv",
        "../.data/meteo_france/SIM2_2010_2019.csv",
        "../.data/meteo_france/SIM2_2000_2009.csv"
    ]
    centroid_geojson_json = "public/data/centroid_coordinates_SIM_LON_LAT.json"
    geojson_path = (
        "public/data/FRANCE_DOM_GEOJSON/departements_metropole.geojson"
    )
    start_date = "2000-01-01" 
    end_date   = "2024-12-31"
    output_folder = 'public/data/FR-ID-JSON_SIM_LON_LAT_PB'

    # Execute the function
    process_and_export_meteo_data(
        csv_compress_list, 
        geojson_path, 
        start_date, 
        end_date,
        centroid_geojson_json, 
        output_folder,
        pc_pierrick
    )
