# Structure Burn Severity

Developed by the Cal Poly Deep GIS Lab, with contributions from Dillon Pinto, Andrew Fricker, Jonathan Ventura, and Remington Wolf. This repo is an extension of [Dillon's original repo](https://github.com/DillonPinto/Structure_Burn_Severity), with modifications to improve efficiency of data preprocessing and accuracy of the model. The original report from 2019 is included in this repo. 

Our goal with this project was to train a neural network to automatically classify structures as either damaged or undamaged. This project uses aerial imagery from Paradise, CA after the Camp Fire devastated the area in 2018 and a set of points denoting the location of structures. Using Google Earth Engine, we clip a small region from the imagery around each point to create the training and validation sets, then create a model using Keras/Tensorflow and train it using the data we generated.

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

Sample image of undamaged building:

![Undamaged Building](example_imgs/example_undamaged.jpeg?raw=true "Undamaged")


Sample image of damaged building:

![Damaged Building](example_imgs/example_damaged.jpeg?raw=true "Damaged")


Sample training run (peak validation accuracy of 0.9750):

![Training Run](example_imgs/sample_training_run.PNG?raw=true "Training run")
