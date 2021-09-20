# -*- coding: utf-8 -*-
"""
Usage:
    python score_data.py "adress"
    output prediction confidence_value_low confidence_value_high

"""


import pandas as pd
import pickle
import numpy as np
import requests
import sys

import conf as c 

def predict(adress):
    
    #Loading knn model and the entire dataset
    model=pickle.load(open(c.conf['model_path'],'rb'))
    data=pd.read_csv(c.conf["prepared_data_path"])
    
    #retrieve coordinates (x,y) by using api of data gouv and adress
    base_url = "https://api-adresse.data.gouv.fr/search/?"
    params = {'q' : adress}
    response =  requests.get(base_url, params=params)
    coords = response.json()
    
    x = coords['features'][0]['properties']['x']
    y = coords['features'][0]['properties']['y']
    
    #Get the price predicted by our model
    prediction=float(np.round(model.predict(np.array([[x, y]])),0)[0])
    
    #Minimum and maximum price in his neighbours
    min_price = int(np.round(data.iloc[model.kneighbors(np.array([[x, y]]))[1][0]]['Prix_m2'].min(),0))
    max_price = int(np.round(data.iloc[model.kneighbors(np.array([[x, y]]))[1][0]]['Prix_m2'].max(),0))
    
    
    print(f"Longitude x (Projection Lambert 93) : {x}")
    print(f"Latitude y (Projection Lambert 93) : {y}")
    print(f"Prédiction moyenne prix/m² : {prediction} €")
    print(f"Prédiction prix/m² min: {min_price} €")
    print(f"Prédiction prix/m² max: {max_price} €")
    
    return prediction,min_price , max_price
    
if __name__ == "__main__":
    predict()
    sys.exit()