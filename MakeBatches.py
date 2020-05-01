import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical

def loadImgs(folder, classes):
    data = []
    for category in classes:
        path = os.path.join(folder, category)
        label = classes.index(category)
        for img in os.listdir(path):
            img_array = imread(os.path.join(path, img))
            data.append([img_array, label])
    return data

def makeBatches(dataset, classes, input_shape, batch_size):
    data = loadImgs(dataset["dest_folder"], classes)
    
    imgs = []
    labels = []
    for img, label in data:
        imgs.append(img)
        labels.append(label)
        
    imgs = np.array(imgs).reshape(-1, input_shape[0], input_shape[1], input_shape[2])
    labels = to_categorical(labels)
    batches = ImageDataGenerator(
        samplewise_center = True,
        width_shift_range = 0.1,
        height_shift_range = 0.1,
        horizontal_flip = True,
        vertical_flip = True)
    
    batches.fit(imgs)
    
    batches = batches.flow(
        x = imgs,
        y = labels,
        batch_size = batch_size,
        shuffle = True)
    return batches