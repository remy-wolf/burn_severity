import ee
import folium
import time

def init():

    """
    This function initializes the API connection to Google Earth Engine and collects stored data from it
    to be processed


    @param (None)
    @return (ee.Image aerialImage, ee.FeatureCollection points,
             ee.Geometry.Polygon trainingPolygon, ee.Geometry.Polygon validationPolygon)
             -> Returns aerialImagery, structure points feature class, and two polygons used for creating
                training and validation sets via clipping of the aerial Image.

    """
    ee.Initialize()

    trainingPolygon=ee.Geometry.Polygon([
    [-121.61246009040491, 39.76224814367828],
    [-121.59046597648279, 39.76224814367828],
    [-121.59046597648279, 39.76652011837134],
    [-121.61246009040491, 39.76652011837134],
    [-121.61246009040491, 39.76224814367828]])


    validationPolygon = ee.Geometry.Polygon([[-121.59506929487134,39.78155804409371],
    [-121.58609998792554,39.78155804409371],
    [-121.58609998792554,39.78571339763988],
    [-121.59506929487134,39.78571339763988],
    [-121.59506929487134,39.78155804409371]])

    aerialImage = ee.Image('users/brendanpalmieri/aerialMosaic_resample_int16')

    points = ee.FeatureCollection("users/geofffricker/PostFirePoints")


    return aerialImage, points, trainingPolygon, validationPolygon





def clipTrainAndValidation(image, trainingPoly, validationPoly):
    """
    Training and validation images are created from clipping the satellite imagery
    based on the two polygons passed in.

    @param (ee.Image image, ee.Geometry trainingPoly, ee.Geometry validationPoly)
        -> (original image, training polygon, validationPolygon)
    @return (ee.Image training, ee.Image validation) -> training and validation imagery

    """

    training   = image.clip(trainingPoly)
    validation = image.clip(validationPoly)

    return training, validation





def bufferPoints(feature):
    """
    This function is called by ee.FeatureCollection.map() to process each Feature
    with the same instructions. Returns a bounding box for each Feature/Point.

    @param ee.Feature feature -> a single feature passed in from a FeatureCollection
    @return ee.Feature feature.buffer(5).bounds() -> This enlarges the point to a Polygon by
            5 units of distance of the projection (or meters if none specified). Then return
            a bounding box for each feature
    """

    return feature.buffer(30).bounds()

def setDamage0(feature):
    return feature.set('damage',0)


def setDamage1(feature):
    return feature.set('damage',1)


def separateLearningData(damageFilter, noDamageFilter, structurePoints, roiPoly):


    damagedStructs = structurePoints.filterBounds(roiPoly).filter(damageFilter)

    notDamagedStructs = structurePoints.filterBounds(roiPoly).filter(noDamageFilter)

    # Set Damage to binary value
    notDamagedStructs = notDamagedStructs.map(setDamage0)
    damagedStructs = damagedStructs.map(setDamage1)

    return notDamagedStructs.merge(damagedStructs)


def getAllFCData(structurePoints):
    damageFilter = ee.Filter.eq('DAMAGE', 'Destroyed (>50%)')
    noDamageFilter = ee.Filter.eq("DAMAGE", "No Damage")

    damagedStructs = structurePoints.filter(damageFilter)
    notDamagedStructs = structurePoints.filter(noDamageFilter)

    # Set Damage to binary value
    notDamagedStructs = notDamagedStructs.map(setDamage0)
    damagedStructs = damagedStructs.map(setDamage1)

    return notDamagedStructs.merge(damagedStructs)



def getFCData(structurePoints, trainingPoly, validationPoly):

    structurePoints = structurePoints.map(bufferPoints)


    # Create Filter objects that will be used inside the FeatureCollection filter method.
    # This filter will be able to sort through the DAMAGE column in the collection and
    # return a collection that contains records that have "No Damage" or "Destroyed (>50%)"
    #
    damageFilter = ee.Filter.eq('DAMAGE',  'Destroyed (>50%)')
    noDamageFilter = ee.Filter.eq("DAMAGE", "No Damage")

    trainingPoints = getAllFCData(structurePoints)
    #trainingPoints   = separateLearningData(damageFilter, noDamageFilter, structurePoints, trainingPoly)
    #validationPoints = separateLearningData(damageFilter, noDamageFilter, structurePoints, validationPoly)
    validationPoints = None

    return trainingPoints, validationPoints








def startEEImageQueue(aerialImage, numOfPoints, allFeatures, folder):

    for i in range(numOfPoints):
        fileName = allFeatures[i]["id"]
        geo = allFeatures[i]["geometry"]["coordinates"]

        export_task = ee.batch.Export.image.toDrive(image=aerialImage.select(['b1', 'b2', 'b3']),
                                                    description=fileName,
                                                    fileNamePrefix = fileName,
                                                    folder=folder,
                                                    region=geo,
                                                    scale=0.25)
        # Print all tasks.
        export_task.start()
        print("Started id = ",fileName," ",numOfPoints-i-1," left")




def makeImageCollection(aerialImage, trainingPoints, testingPoints):

    numOfPoints = len(trainingPoints.getInfo()["features"])
    allFeatures = trainingPoints.getInfo()["features"]
    startEEImageQueue(aerialImage, numOfPoints,allFeatures, "0.25_DATA/training_data_scale_0.25")

    """
    numOfPoints = len(testingPoints.getInfo()["features"])
    allFeatures = testingPoints.getInfo()["features"]
    startEEImageQueue(aerialImage, numOfPoints,allFeatures, "0.25_DATA/validation_data_scale_0.25")
    """


def makeAndUploadData():
    aerialImage, structurePoints, trainingPoly, validationPoly = init()
    trainingImage, validationImage = clipTrainAndValidation(aerialImage, trainingPoly, validationPoly)
    trainingPoints, validationPoints = getFCData(structurePoints, trainingPoly, validationPoly)

    #allPoints = getAllFCData(structurePoints)
    #makeImageCollection(aerialImage, allPoints, structurePoints)

    makeImageCollection(aerialImage, trainingPoints, validationPoints)



