# CMPUT622-MIA-Project-Repo
Repository for course project of CMPUT 622.
In order to reproduce our results, please perform below steps:

## Step 1
Go to "Data preprocessing - Uber and census data combining/" and then run the **Process_Uber_Census_Data.py** file. This will generate the "uber-raw-data-sep14.csv" file which is the very basic dataset required. This dataset has been downloaded from Uber. The **Process_Uber_Census_Data.py** file reads the **US Census Tract Shape File.geojson** file as the shape file where polygon coordinates of the census dataset is located. Finally, **NewYork census data.csv** csv file is combined with **US Census Tract Shape File.geojson** file to create the processed the **uber-raw-data-sep14_processed.csv**


