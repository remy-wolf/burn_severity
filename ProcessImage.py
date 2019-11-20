from os import listdir
from os.path import isfile, join
from osgeo import gdal
import numpy as np
import json


# Reads working directory and outputs list of file paths + fileIDs
def readWordkingDir(workingDir, idDict):
    fileNames = [f for f in listdir(workingDir) if isfile(join(workingDir, f))]
    damageList = []
    imagePaths = []
    for key in idDict.keys():
        if key in fileNames:
            damageList.append(idDict[key])
            imagePaths.append(join(workingDir,key))

    return imagePaths, damageList


def readData(filePath):
    returnData = {}

    with open(filePath) as f:
        data = json.load(f)

    data = data["features"]

    for feature in data:
        returnData[feature["id"]] = feature["properties"]["damage"]

    return returnData



def agument():
    pass





def makeBatch():
    images = []
    workingDirectory = "C:\\Users\\Dillon\\Desktop\\Senior_Project"
    idDict = readData(workingDirectory+"\\data\\data_points.geojson")
    imagePaths, damageList = readWordkingDir(workingDirectory+"\\training_Images", idDict)

    for path in imagePaths:
        image = gdal.Open(path)
        npImage = np.array(image.ReadAsArray())

        try:
            assert npImage.shape[0]==3 and (npImage.shape[1]==122 or npImage.shape[1]==123) and (npImage.shape[2]==122 or npImage.shape[2]==123)
        except:
            print(npImage.shape)


        npImage = np.resize(npImage, (123, 123, 3))

        images.append(npImage)


    return images, np.array(damageList)

(makeBatch())
