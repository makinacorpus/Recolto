import pandas as pd
import geopandas as gpd

waterstress_geojson = '../public/data/waterstress.geojson' # File with results to be used in Récolt'Ô
hybas_eu_shp = '../public/data/hybas_eu_lev01-12_v1c/hybas_eu_lev06_v1c.shp' #LEVEL 6
aqueduct_csv = '../public/data/Aqueduct40_waterrisk_download_Y2023M07D05/CVS/Aqueduct40_future_annual_y2023m07d05.csv'
geo_id = 'pfaf_id'

# Metadata from Aqueduct project : https://github.com/wri/Aqueduct40/blob/master/data_dictionary_water-risk-atlas.md
indicator = 'ws' # Water stress
scenario = 'pes' #Pessimistic (others : bau = Business as Usual / opt = Optimistic)
year = '30' # for 2030 (others : 50 for 2050, 80 for 2080)

# Load hydrological bassin on Europe
hybas_eu = gpd.read_file(hybas_eu_shp, columns=[str.upper(geo_id), 'geometry'])
hybas_eu.columns = map(str.lower, hybas_eu.columns)

# Choose the water stress indicator to use
ws_str = f'{scenario}{year}_{indicator}_x_l' # pes30_ws_x_l
print(ws_str)

# Read indicators and associate its with the hydrological bassin geometries
aqueduct = pd.read_csv(aqueduct_csv, usecols=[geo_id, ws_str])
aqueduct_hybas = hybas_eu.merge(aqueduct, on=geo_id)
print(aqueduct_hybas.head())

# Export in GEOJSON
aqueduct_hybas.to_file(waterstress_geojson, driver="GeoJSON")
