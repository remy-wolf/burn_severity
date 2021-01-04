# Structure_Burn_Severity

### To set up data:

python Extract.py
* This will create the .kml file that stores all of the image data as well as their damaged/not damaged labels.
* Download the .kml file from your drive. They will be found in whatever DRIVE_FOLDER is set to in Constants.py ("deep_gis" by default).
* Place the .kml files in DATA_FOLDER ("data/" by default).

python CreateImgs.py
* This will turn the .kml file into images (stored in "data/imgs" by default)

### To run the model:
python BurnClassifier.py
* Hyper-parameters can be found in Constants.py.
