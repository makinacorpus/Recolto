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


def load_csv_and_create_dataframe(csv_compress, type_data='PRELIQ_Q'):
  """
  Charge le csv compressé, crée le dataframe et extrait les valeurs des preciitations.
  """
  columns_to_keep = ['LAMBX', 'LAMBY', 'DATE'] + [type_data]
  df = pd.read_csv(csv_compress, sep=";", decimal=".", compression="gzip", usecols=columns_to_keep,
                   parse_dates=['DATE'])

  print("DataFraime: \n", df.head())
  return df, type_data


def filter_by_date(df, start_date, end_date):
  """
  Conservation des enregistrements compris entre start_date et end_date.
  """
  #return df_preci[(df_preci['DATE'] >= start_date) & (df_preci['DATE'] <= end_date)]
  return df.set_index('DATE').loc[start_date:end_date]

def locate_safran_points_csv(df, csv_grid_safran_path, centroid_csv_json):
  "Emploi des coordonnées issues de la grille Safran."

  grid_sfr_coords = pd.read_csv(csv_grid_safran_path, sep=";", decimal=",")
  grid_sfr_coords.rename(columns={
    "GID": "gid",
    "LAT_DG": "lat",
    "LON_DG": "lng",
    'LAMBX (hm)': 'LAMBX',
    'LAMBY (hm)': 'LAMBY'
  }, inplace=True)

  grid_sfr_coords['gid'] = grid_sfr_coords.index + 1
  # grid_sfr_cood = grid_sfr_cood[['GID', 'LAMBX', 'LAMBY', 'LAT_DG', 'LON_DG']]

  # sauvegarder la liste des centres en JSON pour référence
  with open(centroid_csv_json, "w") as outfile:
    json.dump(grid_sfr_coords.to_dict(orient='records'), outfile, indent=2, ensure_ascii=False)

  # Réaliser le merge entre les enregistrements et les coordonnées retenues.
  df_fr = df.merge(grid_sfr_coords[['gid', 'LAMBX', 'LAMBY']], on=['LAMBX', 'LAMBY'], how='inner')

  return grid_sfr_coords, df_fr


def configure_pq_selection(df_fr, type_data):
  """
  Configure la sélection et le traitement de PE_Q
  """
  df_processed = df_fr.copy()

  if type_data == 'PEQ':
    df_processed[type_data] = df_processed[type_data].clip(lower=0)

  print("PEQ CONFIG:\n", df_processed)
  return df_processed


def compute_statistics(df_fr, type_data, df_coord, outfolder):
  """
  Calcul de la somme des précipitations en chaque cellule de la grille (identifiée par son gid) puis export
  des statistiques (annuelles et mensuelles) au format JSON dans le dossier output_folder.
  """
  if not os.path.exists(outfolder):
    os.makedirs(outfolder)

  df_fr['YEARS'] = df_fr['DATE'].dt.year.astype(str)
  df_fr['MONTHS'] = df_fr['DATE'].dt.to_period('M').astype(str)

  # Boucle pour calculer les statistiques pour chaque station
  for _, row in df_coord.iterrows():
    gid = int(row.gid)
    lambx_val, lamby_val = row.LAMBX, row.LAMBY
    print(f"Processing GID {gid} at coordinates ({lambx_val}, {lamby_val})")

    # Filtrer les données pour la station actuelle
    df_station = df_fr[
      (df_fr['LAMBX'] == lambx_val) &
      (df_fr['LAMBY'] == lamby_val)
      ]

    # Calcul des statistiques annuelles
    df_years = df_station.groupby('YEARS')[type_data].sum().reset_index()

    # Calcul des statistiques mensuelles
    df_months = df_station.groupby('MONTHS')[type_data].sum().reset_index()

    # Préparer le dictionnaire pour export JSON
    dict_all = {
      "years": df_years.set_index('YEARS')[type_data].to_dict(),
      "months": df_months.set_index('MONTHS')[type_data].to_dict()
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
                                  output_folder,
                                  type_data):
  """
  Ce script permet de traiter et d’exporter les données météorologiques de SIM Safran au format csv compressé.
  Il réalise les opérations suivantes :

  1. Chargement du CSV compressé et Création d’un DataFrame et extraction des précipitations.
  2. Filtrage temporel.
  3. Utilisation de la grille Safran
  4. Pré-traitement si utilisation de PE_Q
  5. Calcul et export des statistiques

  Paramètres :
    - csv_compress (str) : Chemins vers le dossier contenant CSV compressé.
    - csv_grid_safran_path (str) : Chemin vers le fichier csv contenant la grille Safran.
    - start_date (str) : Date de début du filtrage temporel (format "YYYY-MM-DD").
    - end_date (str) : Date de fin du filtrage temporel (format "YYYY-MM-DD").
    - output_folder (str) : Dossier où seront exportés les fichiers JSON des statistiques par station.
    - centroid_csv_json : Sauvegarde la liste des centres (coordonnées uniques) en JSON.
    -use_PRENEI_Q_and_PEQ,(bool): Indique si les colonnes 'PRENEI_Q' et 'PE_Q' doit être incluse.
    -use_negative_PEQ (bool): Indique si les valeurs négatives de 'PE_Q' doivent être mises à zéro.
  """
  # 1. Chargement des données CSV compressé
  df, type_data = load_csv_and_create_dataframe(csv_compress, type_data)
  # 2.Filtrage temporel pour ne conserver que les enregistrements entre start_date et end_date.
  df_filter = filter_by_date(df, start_date, end_date)
  # 3 Utlisation des coordonnées issues de la grille Safran
  df_coord, df_fr = locate_safran_points_csv(df_filter, csv_grid_safran_path, centroid_csv_json)
  # 4 Configure la sélection et le traitement de PE_Q
  peq_config = configure_pq_selection(df_fr, type_data)
  # 5. Calcul et export des statistiques en JSON
  compute_statistics(peq_config, type_data, df_coord, output_folder)


#######################################
# MAIN
#######################################

if __name__ == "__main__":
  # Définir les paramètres
  csv_compress = "../public/data/QUOT_SIM2_previous-2020-202501.csv.gz"
  csv_grid_safran_path = "../public/data/coordonnees_grille_safran_lambert-2-etendu.csv"
  centroid_csv_json = "../public/data/centroid_coordinates_safran.json"
  start_date = "2020-01-01"
  end_date = "2024-12-01"
  output_folder = '../public/data/FR-ID-JSON'

  process_and_export_meteo_data(csv_compress,
                                csv_grid_safran_path,
                                start_date,
                                end_date,
                                centroid_csv_json,
                                output_folder,
                                'PRELIQ_Q'
                                )
