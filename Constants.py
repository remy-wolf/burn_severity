import os

# relevant directories
DATA_FOLDER = "data/"
DRIVE_FOLDER = "deep_gis"

# keras inputs
IMG_SIZE = (169, 169)
INPUT_SHAPE = (128, 128, 3)
CLASSES = ['no_damage', 'damage']
WEIGHTS = [10, 1]
BATCH_SIZE = 20
LEARNING_RATE = 3e-4
NUM_EPOCHS = 20
NUM_SAMPLES = 16000

# earth engine assets/inputs
AERIAL_IMG = "users/brendanpalmieri/aerialMosaic_resample_int16"
POINTS = "users/geofffricker/PostFirePoints"
POLYGON = "users/remywolf/burn-sev-aerial-img"
BUFFER_SIZE = 30

# information needed to generate the datasets
TRAINING = {
    "name": "train",
    "filename": "train_table",
    "polygon": [
        [-121.61246009040491, 39.76224814367828],
        [-121.58194701473388, 39.76224814367828],
        [-121.58194701473388, 39.752221128885004],
        [-121.61246009040491, 39.752221128885004],
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

TEST = {
    "name": "test",
    "filename": "test_table",
    "polygon": [
        [-121.63364380980842,39.7667863839369], 
        [-121.6265627780091,39.7667863839369],
        [-121.6265627780091,39.770414866089745], 
        [-121.63364380980842,39.770414866089745],
        [-121.63364380980842,39.7667863839369]],
    "dest_folder": os.path.join(DATA_FOLDER, "test_imgs/")
}
    
DATASETS = {TRAINING["name"]: TRAINING, VALID["name"]: VALID, TEST["name"]: TEST}
    

