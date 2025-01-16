import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
import xclim.indices.generic as xi

from dask.diagnostics import ProgressBar

import json
import os


def dict_to_json(dictionnary, outpath):
    """
    Useful function to export a dictionnary to a json file
    """
    json_object = json.dumps(dictionnary, indent=2, ensure_ascii=False)
    
    with open(outpath, "w") as outfile:
        outfile.write(json_object)


# chemin vers les netcdf de précipitations en entrée
infiles = "dataset-insitu-gridded-observations-global-and-regional-02c1e04d-86d1-4d82-9bca-904493c39079/*.nc"

# ouverture des netcdf en un seul dataset
ds = xr.open_mfdataset(infiles)

# ouverture du fichier des contours de la France (métropolitaine et DROM)
# permet de ne sélectionner que les cellules du netcdf qui correspondent
gdf_fr = gpd.read_file('france-drom.geojson')

# Récupération des coordonnées qui concernent la France métropolitaine + DROM
lon_list = list(ds.lon.values)*len(ds.lat)
lat_list = np.repeat(list(ds.lat.values),len(ds.lon))

points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(lon_list, lat_list))
points.crs = gdf_fr.crs
within_points = gpd.sjoin(points, gdf_fr, predicate = 'within')

within_points['lon'] = within_points.geometry.x
within_points['lat'] = within_points.geometry.y

df_coord = within_points[['lon','lat']].drop_duplicates(subset=['lon','lat']).reset_index(drop=True)
df_coord['gid'] = df_coord.index+1

## Sauvegarde des coordonnées au format csv si nécessaire
# df_coord.to_csv('centroid_coordinates_all.csv',sep=',',index=False)

df_coord = df_coord[['gid','lon','lat']]

# Serializing json
json_object = json.dumps(df_coord.to_dict(orient='records', index=True), indent=2, ensure_ascii=False)

# Ecriture du json
with open("centroid_coordinates_all.json", "w") as outfile:
    outfile.write(json_object)

# Sélection des cellules d'intérêt dans le dataset avec toutes les données de précipitations
longitudes = list(df_coord.lon)
latitudes = list(df_coord.lat)

x = xr.DataArray(list(df_coord.lon), dims=['location'])
y = xr.DataArray(list(df_coord.lat), dims=['location'])

ds_fr = ds.sel(lon=x, lat=y, method='nearest').sel(time=slice("2001-01-01","2020-12-31"))

# On sauvegarde vers un fichier netcdf intermédiaire pour se
# débarasser des chunks mis en place automatiquement avec une
# ouverture des fichiers avec `open_mfdataset()`.  
# Les chunks avec Dask ralentissent ici nos calculs de façon importante.
# On sauvegarde donc les données pour les réouvrir sans chunk.
# Malgré temps de sauvegarde, ça vaut carrément le coup de le faire !

out_file = 'pr_fr-drom_2001-2020.netcdf'

if os.path.exists(out_file):
    os.remove(out_file)

# Attention, cette sauvegarde nécessite d'avoir au moins 12Go de mémoire dispo !
write_job = ds_fr.to_netcdf(out_file, compute=False)
with ProgressBar():
    print(f"Writing to {out_file}")
    write_job.compute()

# Ouverture du dataset sur la France
ds = xr.open_dataset(out_file)
var = list(ds_fr.data_vars)[-1]

da = ds[var]

# Calcul des statistiques
df_stat_years = (
    xi.statistics(da, 'sum', 'YS')
    .to_dataframe()
    .reset_index()
)

df_stat_months = (
    xi.statistics(da, 'sum', 'MS')
    .to_dataframe()
    .reset_index()
)

# Indique où sauvegarder les json qui vont être générés pour chaque cellule
outfolder = 'FR-ID-JSON'
if not os.path.exists(outfolder):
    os.mkdir(outfolder)

# Boucle sur les paires de longitudes/latitudes situées en France, qui ont été recensées dans df_coord
for index, row in df_coord.iterrows():
    # ID de la paire de coordonnées
    print(f"Processing gid {round(row.gid)}")
    
    # Formatage du dictionnaire des années
    df_years = df_stat_years.loc[(df_stat_years.lon==row.lon) & (df_stat_years.lat==row.lat)][['time',var]]
    df_years['time-years'] = df_years.time.astype(str).str[:4]
    df_years = df_years.rename(columns={var:'years'}).drop(columns=['time']).set_index('time-years')
    dict_years = df_years.to_dict(orient='dict', index=True)
    
    # Formatage du dictionnaire des mois
    df_months = df_stat_months.loc[(df_stat_months.lon==row.lon) & (df_stat_months.lat==row.lat)][['time',var]]
    df_months['time-months'] = df_months.time.astype(str).str[:7]
    df_months = df_months.rename(columns={var:'months'}).drop(columns=['time']).set_index('time-months')
    dict_months = df_months.to_dict(orient='dict', index=True)
    
    # Réunion des deux dictionnaires en un seul
    dict_all = dict(dict_years, **dict_months)
    
    # Export en fichier json
    dict_to_json(dict_all, f"{outfolder}/{round(row.gid)}.json")
