# CMPUT622-MIA-Project-Repo
Repository for course project of CMPUT 622.
In order to reproduce our results, please perform below steps:

## Step 1
Go to "Data preprocessing - Uber and census data combining/" and then run the **Process_Uber_Census_Data.py** file. This will generate the "uber-raw-data-sep14_processed.csv" file which is the very basic dataset required. This dataset has been downloaded from Uber. The **Process_Uber_Census_Data.py** file reads the **US Census Tract Shape File.geojson** file as the shape file where polygon coordinates of the census dataset is located. Finally, **NewYork census data.csv** csv file is combined with **US Census Tract Shape File.geojson** file to create the processed the **uber-raw-data-sep14_processed.csv**

## Step 2
Execute this notebook available on the root: Create_User_Group.ipynb . It will read the **uber-raw-data-sep14_processed.csv** file and create several other files that will be used by the notebooks to create attack models. This notebook will generate data: uber_census.csv, uber_census_augmented.csv, uber_census_extra_features.csv, uber_census_multiclass.csv. You can find them inside "Membership Inference Attack Notebooks/"


## Step 3
Navigate to "Membership Inference Attack Notebooks/". All these notebooks should be opened in colab.

### Case study 1
Uber_Census_Privacy_Attack_Binary_Classifier.ipynb will use uber_census.csv file. Thus, when you are running this notebook, please upload the uber_census.csv in the root directory of the colab. This notebook is for basic membership inference attack on binary classifier with less number of features.

### Case study 2
Uber_Census_Privacy_Attack_binary_classifier_with_extra_features.ipynb will use uber_census_extra_features.csv file. Thus, when you are running this notebook, please upload the uber_census_extra_features.csv in the root directory of the colab. This notebook is for membership inference attack on binary classifier with increased number of features.

### Case study 3
Uber_Census_Privacy_Attack_multiclass.ipynb will use uber_census_multiclass.csv file. Thus, when you are running this notebook, please upload the uber_census_multiclass.csv in the root directory of the colab. This notebook is for membership inference attack on multiclass classifier.

### Case study 4
EXP1_Uber_Census_Privacy_Attack_With_Perturbation.ipynb will use uber_census_augmented_generated.csv file. Thus, when you are running this notebook, please upload the uber_census_augmented_generated.csv in the root directory of the colab. This notebook is for membership inference attack on binary classifier with perturbed data.
** Remember: In order to generate uber_census_augmented_generated.csv file, please run the **Synthetic Data Generation/perturbation.py** file. It will read the uber_census_augmented.csv file (generated earlier by Create_User_Group.ipynb notebook in step 2) and produce uber_census_augmented_generated.csv file by perturbing the records in the file.


