import os

# relevant directories
DATA_FOLDER = "data/"
DRIVE_FOLDER = "deep_gis"

# keras inputs
INPUT_SHAPE = (169, 169, 3)
CLASSES = ['no_damage', 'damage']
WEIGHTS = [10, 1]
BATCH_SIZE = 128
LEARNING_RATE = 5e-5
NUM_EPOCHS = 100
NUM_SAMPLES = 5000

# earth engine assets
AERIAL_IMG = "users/brendanpalmieri/aerialMosaic_resample_int16"
POINTS = "users/geofffricker/PostFirePoints"

# information needed to generate the datasets
TRAINING = {
    "name": "train",
    "filename": "train_table",
    "polygon": [
    [-121.61246009040491, 39.76224814367828],
    [-121.59046597648279, 39.76224814367828],
    [-121.59046597648279, 39.76652011837134],
    [-121.61246009040491, 39.76652011837134],
    [-121.61246009040491, 39.76224814367828]],
    "dest_folder": os.path.join(DATA_FOLDER, "train_imgs/")
}

VALID = {
    "name": "valid",
    "filename": "valid_table",
    "polygon": [
    [-121.59506929487134,39.78155804409371],
    [-121.58609998792554,39.78155804409371],
    [-121.58609998792554,39.78571339763988],
    [-121.59506929487134,39.78571339763988],
    [-121.59506929487134,39.78155804409371]],
    "dest_folder": os.path.join(DATA_FOLDER, "valid_imgs/")
}

DATASETS = {TRAINING["name"]: TRAINING, VALID["name"]: VALID}
    

