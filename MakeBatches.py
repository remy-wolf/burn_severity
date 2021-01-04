import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
import random

def loadImgs(folder, classes):
    data = []
    for category in classes:
        path = os.path.join(folder, category)
        label = classes.index(category)
        for img in os.listdir(path):
            img_array = imread(os.path.join(path, img))
            data.append([img_array, label])
    return data

def makeBatches(folder, classes, input_shape, batch_size):
    data = loadImgs(folder, classes)
    random.shuffle(data)
	 # pre-shuffle data due to bug when using validation_split in ImageDataGenerator
	 # if we don't, training & validation batches have imbalanced ratio of classes

    imgs = []
    labels = []
    for img, label in data:
        imgs.append(img)
        labels.append(label)
        
    imgs = np.array(imgs).reshape(-1, input_shape[0], input_shape[1], input_shape[2])
    labels = to_categorical(labels)
    datagen = ImageDataGenerator(
        samplewise_center = True,
        width_shift_range = 0.1,
        height_shift_range = 0.1,
        horizontal_flip = True,
        vertical_flip = True,
        validation_split=0.1)
    
    datagen.fit(imgs)
    
    train_batches = datagen.flow(
        x = imgs,
        y = labels,
        batch_size = batch_size,
        shuffle = True,
		  subset = "training")
    
    valid_batches = datagen.flow(
        x = imgs,
        y = labels,
        batch_size = batch_size,
        shuffle = True,
        subset = "validation")

    return train_batches, valid_batches
