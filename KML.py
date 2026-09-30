import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import kdtree


def LoadKML(filename: str):
    gdf_kml = gpd.read_file(filename, engine='pyogrio')
    gdf_utm = gdf_kml.to_crs(gdf_kml.estimate_utm_crs()).explode(index_parts=False).reset_index(drop=True)
    return gdf_utm

def NearestPort(kml, gdf_kml):
    ports = pd.read_csv("Simulations\\Portos.csv")
    gdf_ports = gpd.GeoDataFrame(ports, geometry=gpd.points_from_xy(ports['longitude'], ports['latitude']), crs='EPSG:4326')
    crs_utm = gdf_kml.estimate_utm_crs()
    gdf_ports_utm = gdf_ports.to_crs(crs_utm)
    coords_ports = np.array(list(zip(gdf_ports_utm.geometry.x, gdf_ports_utm.geometry.y)))
    tree = kdtree(coords_ports)
    centroids_kml = gdf_kml.geometry.centroid
    coords_centroids = np.array(list(zip(centroids_kml.x, centroids_kml.y)))
    distancies_m, indicies_proximos = tree.query(coords_centroids)
    gdf_kml["porto_mais_proximo"] = gdf_portos_utm["nome_geral"].iloc[indicies_proximos].values
    gdf_kml["terminal"] = gdf_portos_utm["nome_terminal"].iloc[indicies_proximos].values
    gdf_kml["distancia_km"] = np.round(distancies_m / 1000.0, 2)
    nearest_port = row['porto_mais_proximo']
    return nearest_port