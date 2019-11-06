from Extract import init, clipTrainAndValidation, getFCData, createDataSet# todo import specific functions
from model import init, train

def main():
    aerialImage, structurePoints, trainingPoly, validationPoly = init()
    trainingImage, validationImage = clipTrainAndValidation(aerialImage, trainingPoly, validationPoly)
    trainingPoints, validationPoints = getFCData(structurePoints, trainingPoly, validationPoly)

    createDataSet(trainingImage, trainingPoints,"training")
    createDataSet(validationImage, validationPoints,"testing")

    # todo change normalization value, if needed
    model = initModel(keep_prob=0.5)
    trainModel()

    # todo more stuff with training and validation image




if __name__ == "__main__":
    main()