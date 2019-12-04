from Extract import (init, clipTrainAndValidation,
                     getFCData, createDataSet, makeAndUploadData)# todo import specific functions
from model import initModel,train,getTFRecord
from ProcessImage import readData, makeBatch


def main():
    #makeAndUploadData()
    x, y = makeBatch()
    model = initModel(0.3)
    train(model, x, y, split=0.3, batch_size=100,
          learningRate=1.0e-5, epochs=10)


if __name__ == "__main__":
    main()