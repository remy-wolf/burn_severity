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


    # todo make sure bands should be attached to feature collection and not imagery
    bands = ['b1', 'b2', 'b3']
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

    return feature.buffer(5).bounds()

def setDamage0(feature):
    return feature.set('damage',0)


def setDamage1(feature):
    return feature.set('damage',1)


def separateLearningData(damageFilter, noDamageFilter, structurePoints, roiPoly):

    # todo comment this function

    damagedStructs = structurePoints.filterBounds(roiPoly).filter(damageFilter)


    notDamagedStructs = structurePoints.filterBounds(roiPoly).filter(noDamageFilter)




    # Set Damage to binary value
    notDamagedStructs = notDamagedStructs.map(setDamage0)
    damagedStructs = damagedStructs.map(setDamage1)

    return notDamagedStructs.merge(damagedStructs)



# todo fill out docstring for processImage function
def getFCData(structurePoints, trainingPoly, validationPoly):
    """
    f
    :return:
    """

    structurePoints = structurePoints.map(bufferPoints)

    # Create Filter objects that will be used inside the FeatureCollection filter method.
    # This filter will be able to sort through the DAMAGE column in the collection and
    # return a collection that contains records that have "No Damage" or "Destroyed (>50%)"
    #
    damageFilter = ee.Filter.eq('DAMAGE',  'Destroyed (>50%)')
    noDamageFilter = ee.Filter.eq("DAMAGE", "No Damage")

    trainingPoints   = separateLearningData(damageFilter, noDamageFilter, structurePoints, trainingPoly)
    validationPoints = separateLearningData(damageFilter, noDamageFilter, structurePoints, validationPoly)

    return trainingPoints, validationPoints





def createDataSet(aerialImage, dataPoints, prefix):


    # Sample the image at the points and add a random column.
    aerialImage = aerialImage#.select(['b1', 'b2', 'b3'])

    training = aerialImage.sampleRegions(
        collection=dataPoints, properties=['damage'], scale=0.5)


    exportTask = ee.batch.Export.image.toDrive(
        aerialImage,
        "Test export",
        folder="batch_images",
        fileNamePrefix=prefix,
        fileFormat='GeoTIFF'
    )

    # Print all tasks.
    print(ee.batch.Task.list())
    exportTask.start()
    # Poll the training task until it's done.
    while exportTask.active():
        print('Polling for task (id: {}, state: {}).'.format(exportTask.id, exportTask.state))
        time.sleep(30)

    print('Done with training export.')
    print(exportTask.state)






"""
    def toDrive(image, description='myExportImageTask', folder=None,
                fileNamePrefix=None, dimensions=None, region=None,
                scale=None, crs=None, crsTransform=None,
                maxPixels=None, shardSize=None, fileDimensions=None,
                skipEmptyTiles=None, fileFormat=None, formatOptions=None,
                **kwargs):
"""



# todo insert stuff below into own function
"""

# Declare task
export_task = ee.batch.Export.image.toDrive(
                    fireImage, 
                    'imageToDriveExample',
                    "batch_images",
                    None, 
                    None, 
                    None)

# Print all tasks.
print(ee.batch.Task.list())

# Poll the training task until it's done.
import time
while export_task.active():
  print('Polling for task (id: {}).'.format(export_task.id))
  time.sleep(30)

print('Done with training export.')
print(export_task.state)
"""