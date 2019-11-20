from Extract import (init, clipTrainAndValidation,
                     getFCData, createDataSet, makeAndUploadData)# todo import specific functions
from model import initModel,train,getTFRecord
from ProcessImage import readData, makeBatch

def main():
    #makeAndUploadData()

    x, y = makeBatch()
    model = initModel(0.3)
    #train(model, len(y), x, y)


if __name__ == "__main__":
    main()