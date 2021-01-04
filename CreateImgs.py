import xmltodict
import os
import numpy as np
import split_folders
from PIL import Image

from Constants import IMG_SIZE, INPUT_SHAPE, DATASETS, DATA_FOLDER, CLASSES

""" Each band is a (roughly) 170 x 170 matrix of pixels. In the .kml file, this is stored as a string.
    We want to convert this string to a numpy array and then save it as an image.
    Some of the images are slightly less or slightly more than 170 pixels in a given dimension, so we
    crop the images to 169 x 169 to standardize the data, then resize the images to 128 x 128 so that
    they play nicely with the model. """
    
    #right now we assume the data is formatted nicely. may need to add error checking in the future
    
def processKML(data, img_size, target_size, classes):
    kml_file = os.path.join(DATA_FOLDER, data) + ".kml"
    dest_folder = os.path.join(DATA_FOLDER, "imgs/")
    with open(kml_file) as kml:
        table = xmltodict.parse(kml.read())['kml']['Document']['Placemark']
        for img in table:
            createImg(img, dest_folder, img_size, target_size, classes)
        kml.close()
 
def createImg(img_data, dest_folder, img_size, target_size, classes):
    bands = np.empty(target_size[2], dtype = np.object)
    for cur_band in range(len(bands)):
        data = img_data['ExtendedData']['Data'][cur_band + 2]['value'] # the original unformatted string from the kml file
        band = np.empty((img_size[0], img_size[1]), dtype = np.uint8)
        cur_row = 0
        row_start = 2
        while (row_start < len(data) and cur_row < img_size[0]):
            row_end = row_start + 1
            while (data[row_end] != ']'):
                row_end += 1;
            band[cur_row] = np.fromstring(data[row_start : row_end], dtype=np.uint8, sep=',')[0 : img_size[1]] # trim row to size
            row_start = row_end + 4 # skip each in-between sequence of '], ['
            cur_row += 1
        bands[cur_band] = band
    img_array = np.dstack([bands[2], bands[0], bands[1]]).astype(np.uint8) # for some reason, bands are stored b2, b3, b1 in the kml file, so we need to reorder them
    img_folder = os.path.join(dest_folder, classes[int(img_data['ExtendedData']['Data'][1]['value'])]) # place image into no_damage and damage folders
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    Image.fromarray(img_array).resize((target_size[0], target_size[1])).save(os.path.join(img_folder, img_data['ExtendedData']['Data'][0]['value']) + ".jpeg") # id of the image
    
if __name__ == "__main__":
    processKML("data_table", IMG_SIZE, INPUT_SHAPE, CLASSES)
