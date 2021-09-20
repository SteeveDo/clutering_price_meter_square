# -*- coding: utf-8 -*-
"""
Utility functions.
"""
import pandas as pd
import numpy as np
import shapefile
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

def Outlier(df_func):
    """
    The purpose is to indicate which prices are out of a confidence range
    The rule chosen is the following one: ' Price < Q1 - 1.5(Q3-Q1) or x > Q3 + 1.5(Q3-Q1)' where Q1 and Q3 are respectively the 1st and 3rd quartiles
    of each distribution
    """
    Modifs=[]
    data=df_func.groupby(["commune"])["Prix_m2"].describe()
    for com in df_func["commune"].unique():
        Q1= data["25%"][com]
        
        Q2= data["50%"][com]
        
        Q3= data["75%"][com]
        
        dg=df_func[df_func["commune"]==com]["Prix_m2"].map(lambda x: ((x < (Q1 - 1.5*(Q3-Q1)) ) | (x > (Q3 + 1.5*(Q3-Q1)) ) ))
        
        Modifs.append(dg)
    return Modifs

def remove_outliers(data):
    """
    Use the outlier result to remove the outliers in a dataframe and return the result
    """
    df=data

    for outlier in Outlier(df):
        for out in outlier.index:
            df.loc[out, "Outlier"]= outlier[out]

    return df[df["Outlier"]==False]


def collect_data():
    """
    Read both transactional and cadastral data into 2 dataframes
    """
    data_transac=pd.read_csv(c.conf['path_transactional_data'], sep="|", header=0,low_memory=False)
    data_geo_sf=shapefile.Reader(c.conf['path_geo_data'])
    data_geo=read_shapefile(data_geo_sf)
    
    return (data_transac,data_geo)


def merge_data(data_transac,data_geo):
    """
    Join the 2 dataframes from cadastral data and transactional data into one
    """
    
    data_transac["Code departement"]= data_transac["Code departement"].map(str)
    data_transac["Nature mutation"]=data_transac["Nature mutation"].map(str)
    data_transac["Type local"]=data_transac["Type local"].map(str)
    data_transac["Prefixe de section"]=data_transac["Prefixe de section"].map(lambda x:"000")
    data_transac['Valeur fonciere']=data_transac['Valeur fonciere'].map(lambda x: float(str(x).split(sep=",")[0]))
    
    
    #Filter on local that have less than the "amount of lots " parameter in conf, that matchs an appartement
    #Filter on empty land value, department should be 75 and mutation nature should be "sell"
    
    n=c.conf['amount_of_lots']
    temp_transac=data_transac[(data_transac["Valeur fonciere"].isna()==False) & (data_transac["Code departement"]=="75") & (data_transac["Nature mutation"]=="Vente") & (data_transac["Type local"]=="Appartement") & (data_transac["Nombre de lots"]<n) ].copy()
    
    #Creating an indicator Arrondissement
    temp_transac['Arrondissement']=temp_transac['Code departement']+temp_transac['Code commune'].map(str)
    
    #The key to join the datframes is a concatenation of: "Code departement", "Code commune","prefixe" "section" "numero"
    temp_transac["jointure"]=temp_transac["Arrondissement"].map(str)+ temp_transac["Prefixe de section"].map(str)+ temp_transac["Section"].map(str)+temp_transac["No plan"].map(str)
    
    data_geo["jointure"]=data_geo["commune"].map(str)+"000"+data_geo["section"].map(str)+data_geo["numero"].map(str)
    
    #Setting index for joining dataframes
    temp_transac=temp_transac.set_index("jointure")
    temp_geo= data_geo.set_index("jointure")
    
    #Merging dataframes
    data_merged= temp_transac.join(temp_geo, how="inner")
    
    
    return data_merged


def cleaning_data(data_to_clean):
    
    """
    Apply some transformations to the merged data and return a cleaned dataframe
    """
    data_to_clean["Prix_m2"]=data_to_clean["Valeur fonciere"]/data_to_clean["Surface reelle bati"]
    
    #1st erasing of Outliers
    data_to_clean["Outlier"]=False
    temp_data=remove_outliers(data_to_clean)
    print(temp_data)
    #A cutoff on price out of a reality range
    temp_data_cutoff=temp_data[(temp_data["Prix_m2"] > c.conf['cutoff_min_price']) & (temp_data["Prix_m2"] < c.conf['cutoff_max_price'])]
    
    #2nd erasing of Outliers
    temp_data_cutoff["Outlier"]=False
    temp_data_cutoff_clean=remove_outliers(temp_data_cutoff)
    
    #Setting geographic coordinates
    #We should obtain a centroid for each parcel
    
    temp_data_cutoff_clean["coords"]=temp_data_cutoff_clean["coords"].map(lambda x: [np.mean([x[i][0] for i in range(0,len(x)) ]),np.mean([x[i][1] for i in range(0,len(x))])])
    
    #Creating two columns X and Y for each coordinate
    temp_data_cutoff_clean["coords_X"]=temp_data_cutoff_clean["coords"].map(lambda x: x[0])
    temp_data_cutoff_clean["coords_Y"]=temp_data_cutoff_clean["coords"].map(lambda x: x[1])
    
    #Droping columns with too much NaN
    columns_to_remove=(temp_data_cutoff_clean.isna().sum()/temp_data_cutoff_clean.shape[0])[(temp_data_cutoff_clean.isna().sum()/temp_data_cutoff_clean.shape[0])>c.conf['perc_na']].index
    data_merged_drop_column= temp_data_cutoff_clean.drop(columns_to_remove,axis=1)
    
    return data_merged_drop_column




    
    
    
    