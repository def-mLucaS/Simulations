import pandas as pd
import numpy as np
import os
import pyproj
from pathlib import Path
from shapely.geometry import Polygon


def CountAero(gdf_utm, energy_desired):

    path = "C:\\Users\\Lucas\\Downloads\\DOWNLOADS - LUCAS\\PIBIT\\Simulations\\Datasets\\Aerogeradores.csv"
    df_original = pd.read_csv(path)
    df = df_original.copy()
    poligono = gdf_utm.geometry.iloc[0]

    geod = pyproj.Geod(ellps='WGS84')
    area, _ = geod.geometry_area_perimeter(poligono)
    area = abs(area) / 1e6

    densi_mw = 7.0
    potencia_max_area = area * densi_mw
    potencia_total = energy_desired * 1000
    potencia_aero = df['Potencia_nominal_(MW)']
    min_quantidade = np.ceil(potencia_total/potencia_aero)
    max_espaco = np.floor(potencia_max_area / potencia_aero)

    min_quantidade = np.nan_to_num(min_quantidade, nan=0, posinf=0, neginf=0)
    max_espaco = np.nan_to_num(max_espaco, nan=0, posinf=0, neginf=0)

    df['Numerco de Aerogeradores necessários'] = min_quantidade.astype(int)
    df['Quantidade Maxima de espaço'] = max_espaco.astype(int)

    return df


