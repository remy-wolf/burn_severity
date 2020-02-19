# Structure_Burn_Severity

### To set up data:

python Extract.py
* This will create the .kml file that stores all of the image data as well as their damaged/not damaged labels.
* Run this twice to create both the training and validation tables.
* The code will call makeAndUploadData(POINTS, DRIVE_FOLDER, DATASETS["train"]), replace DATASETS["train"] with DATASETS["valid"] to create validation data on the second run.
* Download the .kml files from your drive. They will be found in whatever DRIVE_FOLDER is set to in Constants.py ("deep_gis" by default).
* Place the .kml files in DATA_FOLDER ("data/" by default).

python CreateImgs.py
* This will turn the .kml files into images.
* Run this twice to create both the training and validation image sets.
* The code will call processKML(DATASETS["train"], INPUT_SHAPE, CLASSES), replace DATASETS["train"] with DATASETS["valid"] to create validation data on the second run.

### To run the model:
python BurnClassifier.py
* Hyper-parameters can be found in Constants.py. Currently, the validation loss/accuracy do not seem to be converging.