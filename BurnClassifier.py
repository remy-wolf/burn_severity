from Extract import makeAndUploadData
from model import initModel, train, runModel
#from ProcessImage import readData, makeBatch

DATA_FOLDER = "data/"
INPUT_SHAPE = (169, 169, 3)
CLASSES = ['damage', 'no_damage']
BATCH_SIZE = 128
LEARNING_RATE = 5e-5
NUM_EPOCHS = 100
NUM_SAMPLES = 20000

def main():
    model = initModel(0.5, INPUT_SHAPE)
    train(model, dir = DATA_FOLDER, input_shape = INPUT_SHAPE, classes = CLASSES, num_samples = NUM_SAMPLES, batch_size = BATCH_SIZE, learningRate = LEARNING_RATE, epochs = NUM_EPOCHS)
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

if __name__ == "__main__":
    main()