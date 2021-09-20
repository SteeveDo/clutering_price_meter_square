# -*- coding: utf-8 -*-
"""
Utility functions.
"""
import pandas as pd
import numpy as np
import shapefile
import matplotlib.pyplot as plt
import statistics as st
import seaborn as sns
import conf as c

#To set off warnings
pd.options.mode.chained_assignment = None  # default='warn'

def read_shapefile(shapef):
    """
    Read a shapefile into a Pandas dataframe with a 'coords' 
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in shapef.fields][1:]
    records = shapef.records()
    shps = [s.points for s in shapef.shapes()]
    data_transac = pd.DataFrame(columns=fields, data=records)
    data_transac = data_transac.assign(coords=shps)
    return data_transac

def collect_data():
    """
    Read both transactional and cadastral data into 2 dataframes before cleaning
    and joining them
    """
    data_transac=pd.read_csv(c.path_transactional_data, sep="|", header=0,low_memory=False)
    data_geo_sf=shapefile.Reader(c.path_geo_data)
    data_geo=read_shapefile(data_geo_sf)
    
    return (data_transac,data_geo)

def merge_data(data_transac_cleaned,data_geo_cleaned):
    return

def cleaning_data(data_transac,data_geo):
    
    data_transac["Code departement"]= data_transac["Code departement"].map(str)
    data_transac["Nature mutation"]=data_transac["Nature mutation"].map(str)
    data_transac["Type local"]=data_transac["Type local"].map(str)
    data_transac["Prefixe de section"]=data_transac["Prefixe de section"].map(lambda x:"000")
    data_transac['Valeur fonciere']=data_transac['Valeur fonciere'].map(lambda x: float(str(x).split(sep=",")[0]))
    
    #Filtrage sur les locaux où le nombre de lots est inférieur au paramètre nombre_de_lot, ce qui correspond à un appartement
    #Filtrage sur les transactions sans valeur foncière, le departement etant le 75 et la nature de mutation etant une vente
    nombre_de_lot=c.nombre_de_lot
    temp_transac=data_transac[(data_transac["Valeur fonciere"].isna()==False) & (data_transac["Code departement"]=="75") & (data_transac["Nature mutation"]=="Vente") & (data_transac["Type local"]=="Appartement") & (data_transac["Nombre de lots"]<nombre_de_lot) ].copy()
    
    #Création d'un indicateur Arrondissement
    temp_transac['Arrondissement']=temp_transac['Code departement']+temp_transac['Code commune'].map(str)
    
    