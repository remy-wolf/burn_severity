from Extract import (init, clipTrainAndValidation,
                     getFCData, createDataSet, makeAndUploadData)
from model import initModel,train, runModel
from ProcessImage import readData, makeBatch

#todo run median filter on each input image
#todo agument data and create larger data set (IMAGE GENERATOR)
#todo get higher res imagery

def main():
    workingDirectory = "C:\\Users\\Dillon\\Desktop\\Senior_Project"
    idDictPath = workingDirectory + "\\data\\data_points.geojson"
    trainingImgsPath= workingDirectory + "\\training_Images"

    testIdDictPath = workingDirectory + "\\data\\test_data_points.geojson"
    testingImgsPath = workingDirectory + "\\testing_Images"


    x_train, y_train = makeBatch(workingDirectory, idDictPath,trainingImgsPath)
    x_test, y_test = makeBatch(workingDirectory, testIdDictPath, testingImgsPath)

    model = initModel(0.3)
    train(model, x_train, y_train, split=0.3, batch_size=100,
          learningRate=1.0e-5, epochs=10)

    runModel(workingDirectory,x_test,y_test)



if __name__ == "__main__":
    main()