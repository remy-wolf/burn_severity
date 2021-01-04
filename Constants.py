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
KEEP_PROB = 0.5

# earth engine assets/inputs
AERIAL_IMG = "users/brendanpalmieri/aerialMosaic_resample_int16"
POINTS = "users/geofffricker/PostFirePoints"
POLYGON = "users/remywolf/burn-sev-aerial-img"
BUFFER_SIZE = 30