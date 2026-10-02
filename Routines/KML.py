import os
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

def LoadKML(filename: str) -> gpd.GeoDataFrame:



    dir = os.path.expanduser('~')
    path = os.path.join(dir, 'Downloads', 'DOWNLOADS - LUCAS', 'PIBIT', 'Simulations',"Datasets", 'Exemplos', filename)
    gdf_kml = gpd.read_file(path, engine='pyogrio')
    gdf_utm = gdf_kml.to_crs(gdf_kml.estimate_utm_crs()).explode(index_parts=False).reset_index(drop=True)

    return gdf_utm

def NearestPort(gdf_utm: gpd.GeoDataFrame,resultado_localidade, ports: str = 'Portos.csv') -> gpd.GeoDataFrame:

    dir = os.path.expanduser('~')
    path = os.path.join(dir, 'Downloads', 'DOWNLOADS - LUCAS', 'PIBIT', 'Simulations',"Datasets", ports)

    ports = pd.read_csv(path)
    gdf_ports = gpd.GeoDataFrame(ports, geometry=gpd.points_from_xy(ports['longitude'], ports['latitude']), crs="EPSG:4326")
    gdf_ports_utm = gdf_ports.to_crs(gdf_utm.crs)
    coords_ports = np.array(list(zip(gdf_ports_utm.geometry.x, gdf_ports_utm.geometry.y)))

    tree = cKDTree(coords_ports)
    centroids = gdf_utm.geometry.centroid
    coords_centroids = np.array(list(zip(centroids.x, centroids.y)))
    distances_m, nearest_indices = tree.query(coords_centroids)

    gdf_result = gdf_utm.copy()
    gdf_result["porto_mais_proximo"] = gdf_ports_utm["nome_geral"].iloc[nearest_indices].values
    gdf_result["terminal"] = gdf_ports_utm["nome_terminal"].iloc[nearest_indices].values
    gdf_result["distancia_km"] = np.round(distances_m / 1000.0, 2)

    porto = gdf_ports_utm['nome_geral'].iloc[nearest_indices[0]]

    resultado_localidade.set(f"Porto: {porto}")
    