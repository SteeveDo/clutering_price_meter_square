# Leonard-test

## Setup
**Pre-requisites:**

python 3.7 (If you don't have it - [Installation Guide](https://websiteforstudents.com/installing-the-latest-python-3-7-on-ubuntu-16-04-18-04/))

### Dependencies installation
To run scripts on your machine, it will be necessary to install python's
 dependency libraries. The file lists the dependencies is on requirements.txt
 Execute the following command to setup the requirements:
```
pip install -r requirements.txt
```

### Configuration

#### Fetching Data configuration
In order to fetch the data from the files update the `conf.py`
with the required path.
Here is the template.

```conf.py

conf = {
    # Data requirements
    'path_geo_data': <path of your shapefiles containing geographic data>,
    'path_transactional_data': <path of your csv file containing transactional data>,
}
```
#### Data Cleaning configuration
To customize the cleaning parameters see this template in `conf.py`

```
conf = {
    'amount_of_lot': 2,
    'cutoff_max_price':50000,
    'cutoff_min_price':7000,
    'perc_na':0.9,
    'prepared_data_path':'C:/Users/SD.HEUNAMBIAFENG/Downloads/Leonard-test/Leonard-test/Data_prepared.csv',
    
    }
```
# Training model configuration
To customize the training parameters see this template in `conf.py`

```
conf = {
    'test_size': <The test size to use in your data> [0,1],
    'random_state':<a number for your shuffling method>,
    'setting_model_mode': 'auto', #To set your model by yourself put 'manual'
    'neighbors': <number of neighbor for knn>,
    'metric': <"the distance metric in knn">,
    'weights':<"Method to weight your prediction"> ['distance','uniform'],
    'algorithm':<algorithm to use in your neighbor selection>,
    'model_path': <where your model will be saved>,
    }
```

#### The different steps of this project:

### 1-Understand the documentation of data

        The data dictionary was in the `notice-descriptive-du-fichier-dvf-20210809.pdf` file.
        Insights:
            -Each row represents a local and a type of culture nature
            -'No disposition'are only avaible for 'sell' type
            -'Code service CH', 'Reference document','Article CG 1,2,*','Identifiant local' are not avaible so we should drop them
            -We dont have the price per M2 so we should create an indicator for that
### 2-Explore the data

        I firstly looked at the amount of NaN and the type of data in my dataset.
        Insights: 
            
            -Many uninformative columns (Percentage of nan greater than 90%)
            -The field 'Valeur fonciere' contains some NaN to remove because it is mandatory to create our indicator of Price
            The nan was most likely located in some mutation type different than 'vente' so it wasn't a huge loss
            
            -The data types don't match the requirements in each column
            -The geographic data have all the coordinates for each row
            -All the fields needed to make the merge key were present in the 2 dataframes
            
            -The distributions of each district contained too much outliers( 1 Million per M2)
			
            -The observation of some prices on internet showed that we can have some prices between 7000€ and 50000€
        
### 3-Define the target
        
        The target was the 'price per M2' so a new field which was the ratio between the Prix and the Building area was created.
        
### 4-Prepare the data
        My steps were the following:
            
            -Setting the data types as needed
            -Create the joining key
            -Merge the two datasets(geographic data and transactional data) by using the joining key
            -Remove outliers by using a statistic method
                Insights:
                    This method wasn't sufficient to remove all the extreme values like 100K€/M2
                    so implement a cutoff on data by using the prices get on some websites (Seloger.com, etc)
                    
            -Remove once more outliers on the remaining data, to have something that looks like a normal distribution
        
### 5-Create, customize and test the KNN model: KNeighborsRegressor

        In order to build the model,the data file was splitted into  training and testing files. In order to have all districts present in the testing sample, the stratifying
        method by district was used.
        Many combinations of hyper parameters like number of neighbours, distance and weights were tested and the best model according to
        the ROOT MEAN SQUARE ERROR metric was selected. This metric has the benefit of being scaled as the target.
        
### 6-Save the model

        The model was saved with the pickle library with all the hyper parameters he got after training so that i can reload it to make prediction on the web interface.
        The final set of hyper parameters was : algorithm='ball_tree', metric='manhattan', n_neighbors=50, weights='distance'.
        
### 7-Create the end user application

        The model will be consumed through a web application. The user enters the adress, and the application gets its geographic associated coordinates to display
        the predicted price per M2. It also displays the minimum and maximum of the neighbors prices per M2 used for this prediction.
        
        This web application is made of:
            -An html page
            -A backend with Flask Framework

### 9-Test the entire pipeline: Enter adress and get a prediction
        
        In the web interface some adresses were tested and prices predictions were displayed.
    
### 10-Insights to be more efficient
        Get more data on 'Surface Carrez' to be more accurate
        Fit a model that can be able to select the district before getting the neighbors (maybe using a filter on the top of prediction)
        Get more data of the same timeframe to be more realistic
        Instead of taking the average of the coordinates associated to a parcel maybe it would be more precise with the distance computation
        