# -*- coding: utf-8 -*-
"""
Usage:
    python train_model.py
    output <output-file.csv>

"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import pickle
import numpy as np
import sys

import conf as c 

def main():
    
    data= pd.read_csv(c.conf['prepared_data_path'], low_memory=False)
    
    temp_data=data[["coords_X","coords_Y","Arrondissement","Prix_m2"]]
    
    
    #Stratify our data by arrondissement
    
    x_train,x_test,y_train,y_test=train_test_split(temp_data[["coords_X","coords_Y","Prix_m2"]],temp_data["Arrondissement"],test_size=c.conf['test_size'], random_state=c.conf['random_state'], stratify=temp_data["Arrondissement"])
    
    #Train set
    X_train=MinMaxScaler().fit_transform(x_train[["coords_X","coords_Y"]])
    X_test=MinMaxScaler().fit_transform(x_test[["coords_X","coords_Y"]])
    
    #Test set
    Y_train=x_train["Prix_m2"]
    Y_test=x_test["Prix_m2"]
    
    if(c.conf['setting_model_mode']=='manual'):
        model=KNeighborsRegressor(n_neighbors=c.conf['neighbors'], metric=c.conf['metric'], weights=c.conf['weights'], algorithm=c.conf['algorithm'])
        
    else:
        #This script try different approaches for the knn and gives the best model
        Liste_models=[]
        Liste_erreur=[]
        Liste_param=[]
        
        for n_neighbors in [10,30,50,60,70,80,90,100,150,200]:
            for weights in ['uniform','distance']:
                    for metric in ['euclidean','manhattan']:
                        for algorithm in ['auto', 'ball_tree', 'kd_tree', 'brute']:
                            model=KNeighborsRegressor(n_neighbors=n_neighbors, metric=metric, weights=weights, algorithm=algorithm)
                            Liste_models.append(model)
                            Liste_param.append([n_neighbors, metric, weights, algorithm])
                            
                            #Training
                            model.fit(X_train,Y_train)
                            
                            #Compute error for each model by using RMSE metric
                            erreur=np.sqrt(mean_squared_error(Y_test.values,model.predict(X_test)))
                            Liste_erreur.append(erreur)
        mini=0
        for i in range(0,len(Liste_models)):
            if(Liste_erreur[i] < Liste_erreur[mini]):
                mini=i
        best_model=Liste_models[mini]
        
        model=best_model
        
      
    model.fit(MinMaxScaler().fit_transform(data[["coords_X","coords_Y"]]), data["Prix_m2"])
        
    pickle.dump(model, open(c.conf['model_path'], 'wb'))


if __name__ == "__main__":
    main()
    sys.exit()

    
    
    