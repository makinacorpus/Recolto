import pandas as pd
import json
from pathlib import Path
import time


def dict_to_json(dictionary, outpath):
  """
  Export JSON file from dictionary
  """
  json_object = json.dumps(dictionary, indent=2, ensure_ascii=False)
  with open(outpath, "w") as outfile:
    outfile.write(json_object)


def update_json(json_file, new_years, new_months):
  # Load JSON file
  with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

  # Add new years and months in data
  for year, value in new_years.items():
    if year not in data["years"]:
      data["years"][year] = value

  for month, value in new_months.items():
    if month not in data["months"]:
      data["months"][month] = value

  # Write the new JSON file
  with open(json_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)


def load_grid(csv_grid_safran_path):
  # Read French continental grid
  df_grid = pd.read_csv(csv_grid_safran_path, sep=";", decimal=",")
  df_grid.rename(columns={
    "GID": "gid",
    "LAT_DG": "lat",
    "LON_DG": "lng",
    'LAMBX (hm)': 'LAMBX',
    'LAMBY (hm)': 'LAMBY'
  }, inplace=True)

  df_grid['gid'] = df_grid.index + 1

  # Write the grid in a JSON file
  with open(centroid_csv_json, "w") as outfile:
    json.dump(df_grid.to_dict(orient='records'), outfile, indent=2, ensure_ascii=False)

  print('Grid loaded ---- ')

  return df_grid


def load_csv_and_create_dataframe(csv_gzip, end_date, type_data='PRELIQ_Q'):
  """
  Get values from weather file
  """
  columns_to_keep = ['LAMBX', 'LAMBY', 'DATE'] + [type_data]
  df = pd.read_csv(csv_gzip, sep=";", decimal=".", compression="gzip", usecols=columns_to_keep, parse_dates=['DATE'])
  print(f'Data from {csv_gzip} loaded ---- ')

  if df['DATE'].max() > pd.to_datetime(end_date):
    df = df.set_index('DATE').sort_index().loc[:end_date]
    df = df.reset_index()

  df['YEARS'] = df['DATE'].dt.year.astype(str)
  df['MONTHS'] = df['DATE'].dt.to_period('M').astype(str)

  return df, type_data


def compute_statistics_on_grid(i, df, type_data, df_grid, outfolder):
  """
  Compute the sum of precipitation in each grid cell (identified by its gid), then export the statistics (annual and
  monthly) in JSON format to the output_folder.
  """

  # Join the data with the grid
  df_fr = df.merge(df_grid[['gid', 'LAMBX', 'LAMBY']], on=['LAMBX', 'LAMBY'], how='inner')

  outfolder = Path(outfolder)
  outfolder.parent.mkdir(parents=True, exist_ok=True)

  # For each cell on the grid
  for _, row in df_grid.iterrows():
    gid = int(row.gid)
    lambx_val, lamby_val = row.LAMBX, row.LAMBY

    # Get value
    df_station = df_fr[
      (df_fr['LAMBX'] == lambx_val) &
      (df_fr['LAMBY'] == lamby_val)
      ]

    # Compute cumulative statistics
    df_years = df_station.groupby('YEARS')[type_data].sum().reset_index()
    df_months = df_station.groupby('MONTHS')[type_data].sum().reset_index()

    dict_all = {
      "years": df_years.set_index('YEARS')[type_data].to_dict(),
      "months": df_months.set_index('MONTHS')[type_data].to_dict()
    }

    # Path of JSON file
    out_json_path = outfolder / f"{gid}.json"

    # Export or update JSON file
    if i == 0:
      dict_to_json(dict_all, out_json_path)
    else:
      update_json(out_json_path, dict_all["years"], dict_all["months"])


if __name__ == "__main__":
  data_path = Path("../public/data/QUOT_SIM2")
  csv_list = paths = sorted(data_path.iterdir())
  csv_grid_safran_path = "../public/data/coordonnees_grille_safran_lambert-2-etendu.csv"
  centroid_csv_json = "../public/data/centroid_coordinates_safran.json"
  output_folder = '../public/data/FR-ID-JSON'
  end_date = "2024-12-31"

  start = time.time()
  df_grid = load_grid(csv_grid_safran_path)
  print(time.ctime(time.time() - start)[11:19])

  for i, csv in enumerate(csv_list):
    print(f'File n°{i+1} / {len(csv_list)}')
    df, type_data = load_csv_and_create_dataframe(csv, end_date, 'PRELIQ_Q')
    compute_statistics_on_grid(i, df, type_data, df_grid, output_folder)
    print(time.ctime(time.time() - start)[11:19])
    # if i > 0:
    #  break
