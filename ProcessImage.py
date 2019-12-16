from os import listdir
from os.path import isfile, join
from osgeo import gdal
import numpy as np
import json


# Reads working directory and outputs list of file paths + fileIDs
def readWorkingDir(workingDir, idDict):
    fileNames = [f for f in listdir(workingDir) if isfile(join(workingDir, f))]
    damageList = []
    imagePaths = []
    for key in idDict.keys():
        s = key+".tif"

        if s in fileNames:
            damageList.append(idDict[key])
            imagePaths.append(join(workingDir,s))



    return imagePaths, damageList


def readData(filePath):
    returnData = {}

    with open(filePath) as f:
        data = json.load(f)

    data = data["features"]

    for feature in data:
        returnData[feature["id"]] = feature["properties"]["damage"]


    return returnData







def makeBatch(idDictPath, imgsPath):
    images = []
    idDict = readData(idDictPath)
    imagePaths, damageList = readWorkingDir(imgsPath, idDict)

    for path in imagePaths:
        # load tiff image
        image = gdal.Open(path)
        # convert image to numpy array
        npImage = np.array(image.ReadAsArray())

        # D  W  H
        # -1 1  0
        npImage = npImage.transpose((2,1,0))


        try:
            # Ensure that shape conditions are met
            assert npImage.shape[2]==3 and (npImage.shape[1]==122 or npImage.shape[1]==123) and (npImage.shape[0]==122 or npImage.shape[0]==123)
            pass
        except:
            print(npImage.shape)


        npImage = np.resize(npImage, (123, 123, 3))
        images.append(npImage)


    return np.array(images), np.array(damageList)

