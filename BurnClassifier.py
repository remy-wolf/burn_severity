import sys
import os

from Extract import makeAndUploadData
from Model import initModel, train, runModel
from Constants import KEEP_PROB, DATA_FOLDER, INPUT_SHAPE, CLASSES, NUM_SAMPLES, BATCH_SIZE, LEARNING_RATE, NUM_EPOCHS, WEIGHTS

import matplotlib.pyplot as plt

def main():
    model = initModel(KEEP_PROB, INPUT_SHAPE)
    train(model, os.path.join(DATA_FOLDER, "imgs/"), INPUT_SHAPE, CLASSES, NUM_SAMPLES, BATCH_SIZE, LEARNING_RATE, NUM_EPOCHS, WEIGHTS)

#steps: table -> imgs -> train -> test
if __name__ == "__main__":
    main()
