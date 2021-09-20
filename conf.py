conf = {
    # Data requirements
    'path_geo_data': "C:/Users/SD.HEUNAMBIAFENG/Downloads/cadastre-75-parcelles-shp/parcelles.shp",
    'path_transactional_data': "C:/Users/SD.HEUNAMBIAFENG/Downloads/valeursfoncieres-2020.txt",

    # Feature engineering configuration
    'amount_of_lot': 2,
    'cutoff_max_price':50000,
    'cutoff_min_price':7000,
    'perc_na':0.9,
    'prepared_data_path':'C:/Users/SD.HEUNAMBIAFENG/Downloads/Leonard-test/Leonard-test/Data_prepared.csv',
    # Training model configuration
    'test_size': 0.1,
    'random_state':49,
    'setting_model_mode': 'auto',#To set your model by yourself put 'manual'
    'neighbors': 70,
    'metric': 'euclidean',
    'weights':'distance',
    'algorithm':'ball_tree',
    'model_path': 'C:/Users/SD.HEUNAMBIAFENG/Downloads/Leonard-test/Leonard-test/Model_immobilier.pkl'
}