import ee

AERIAL_IMG = "users/brendanpalmieri/aerialMosaic_resample_int16"
POINTS = "users/geofffricker/PostFirePoints"

TRAINING_POLY = [
    [-121.61246009040491, 39.76224814367828],
    [-121.59046597648279, 39.76224814367828],
    [-121.59046597648279, 39.76652011837134],
    [-121.61246009040491, 39.76652011837134],
    [-121.61246009040491, 39.76224814367828]]
    
VALID_POLY = [
    [-121.59506929487134,39.78155804409371],
    [-121.58609998792554,39.78155804409371],
    [-121.58609998792554,39.78571339763988],
    [-121.59506929487134,39.78571339763988],
    [-121.59506929487134,39.78155804409371]]
    
DRIVE_FOLDER = "deep_gis"

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

def filterPoints(points, region):
    points = points.filterBounds(region).map(bufferPoints)
    damageFilter = ee.Filter.eq('DAMAGE', 'Destroyed (>50%)')
    noDamageFilter = ee.Filter.eq("DAMAGE", "No Damage")

    damagedStructs = points.filter(damageFilter)
    notDamagedStructs = points.filter(noDamageFilter)

    # Set Damage to binary value
    notDamagedStructs = notDamagedStructs.map(setDamage0)
    damagedStructs = damagedStructs.map(setDamage1)

    points = notDamagedStructs.merge(damagedStructs)
    # Create Filter objects that will be used inside the FeatureCollection filter method.
    # This filter will be able to sort through the DAMAGE column in the collection and
    # return a collection that contains records that have "No Damage" or "Destroyed (>50%)"

    return points

def startEEImageQueue(points, folder, fileName):
    clippedImgs = points.map(clipImgs)
    export_task = ee.batch.Export.table.toDrive(collection = clippedImgs,
                                                description = fileName,
                                                fileFormat = "KML",
                                                folder = folder)
    export_task.start()
    
def clipImgs(feature):
    aerialImg = ee.Image(AERIAL_IMG)
    # is there a way to do this without grabbing the image every time?
    return (aerialImg
                .sampleRectangle(region = feature.geometry(), properties = None, defaultValue = 0)
                .set('damage', feature.getNumber('damage')))
                

def makeAndUploadData(points, polygon, filename):
    ee.Initialize()
    polygon = ee.Geometry.Polygon(polygon)
    points = filterPoints(ee.FeatureCollection(points), polygon)
    startEEImageQueue(points, DRIVE_FOLDER, filename)

if __name__ == "__main__":
    makeAndUploadData(POINTS, VALID_POLY, "validation_table")