from Extract import makeAndUploadData
from model import initModel, train, runModel
#from ProcessImage import readData, makeBatch
from Constants import DATA_FOLDER, INPUT_SHAPE, CLASSES, NUM_SAMPLES, BATCH_SIZE, LEARNING_RATE, NUM_EPOCHS, WEIGHTS
import sys

def main():
    model = initModel(0.5, INPUT_SHAPE)
    train(model, dir = DATA_FOLDER, input_shape = INPUT_SHAPE, classes = CLASSES, num_samples = NUM_SAMPLES, batch_size = BATCH_SIZE, learningRate = LEARNING_RATE, epochs = NUM_EPOCHS, weights = WEIGHTS)
    # Input parameters

    # Set working directory where files are located
    #workingDirectory = "C:\\Users\\Dillon\\Desktop\\Senior_Project"


    #trainingImgsPath = workingDirectory + "\\training_Images"
    #idDictPath = workingDirectory + "\\data\\data_points.geojson"


    #x_train, y_train = makeBatch(idDictPath, trainingImgsPath)


    #testIdDictPath = workingDirectory + "\\data\\test_data_points.geojson"
    #testingImgsPath = workingDirectory + "\\testing_Images"


    #x_test, y_test = makeBatch(testIdDictPath, testingImgsPath)
    #print("Batches made\nInitializing model...")

    # model = initModel(0.5, INPUT_SHAPE)
    # train(model,
    #       x_train,
    #       y_train,
    #       num_samples=20000,
    #       batch_size=128,
    #       learningRate = 5e-5,
    #       epochs=100)

    #runModel(workingDirectory, x_test, y_test, x_train, y_train)

#steps: table -> imgs -> train -> test
if __name__ == "__main__":
    """Commands: python BurnClassifier.py create | train | test"""
    main()