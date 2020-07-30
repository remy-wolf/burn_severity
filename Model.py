import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#import tensorflow as tf
from keras.layers import Lambda, Conv2D, Dense, Flatten, MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras import regularizers, optimizers, Sequential
from math import ceil
import numpy as np
from keras.utils import to_categorical, plot_model
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from sklearn.metrics import roc_curve
from keras.models import load_model
from keras import regularizers
import matplotlib.pyplot as plt

from MakeBatches import makeBatch
from Constants import DATASETS

def plotTrainingHistory(history):
    # Plot training & validation accuracy values
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

def initModel(keep_prob, input_shape):
    # Create the neural network model for the problem

    model = Sequential()
    model.add(Lambda(lambda x: x / 127.5 - 1, input_shape=input_shape))
    # 128x128
    model.add(Conv2D(64, (3, 3), activation="relu", padding='same'))
    model.add(Conv2D(64, (3, 3), activation="relu", padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 64x64
    model.add(Conv2D(128, (3, 3), activation="relu", padding='same'))
    model.add(Conv2D(128, (3, 3), activation="relu", padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 32x32
    model.add(Conv2D(256, (3, 3), activation="relu", padding='same'))
    model.add(Conv2D(256, (3, 3), activation="relu", padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 16x16
    model.add(Conv2D(512, (3, 3), activation="relu", padding='same'))
    model.add(Conv2D(512, (3, 3), activation="relu", padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 8x8
    model.add(Conv2D(512, (3, 3), activation="relu", padding='same'))
    model.add(Conv2D(512, (3, 3), activation="relu", padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 4x4
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(2, activation='softmax'))

    return model
    
def train(model, data_dir, input_shape, classes, num_samples, batch_size, learningRate, epochs, weights):
    # plot_model(model, to_file='model.png')
    steps_per_epoch = ceil(num_samples/batch_size)

    #train_batches = makeBatches(DATASETS["train"], classes, input_shape, batch_size)
    #valid_batches = makeBatches(DATASETS["valid"], classes, input_shape, batch_size)
    train_folder = os.path.join(DATA_FOLDER, "split_imgs/train/")
    valid_folder = os.path.join(DATA_FOLDER, "split_imgs/val/")
    train_batches = makeBatch(train_folder, CLASSES, INPUT_SHAPE, BATCH_SIZE)
    valid_batches = makeBatch(valid_folder, CLASSES, INPUT_SHAPE, BATCH_SIZE)
    # Get input and compile
    checkpoint = ModelCheckpoint('model-{epoch:02d}.h5',monitor='val_loss',verbose=0, save_best_only=False,mode='auto')


    model.compile(loss ='categorical_crossentropy',
                  optimizer = optimizers.Adam(lr=learningRate),
                  metrics=['acc'])

    # Set model hyper-parameters and train
    history = model.fit_generator(
                        train_batches,
                        steps_per_epoch = steps_per_epoch,
                        epochs = epochs,
                        verbose = 1,
                        class_weight = weights,
                        validation_data = valid_batches)
                        #callbacks=[checkpoint])

    #plotTrainingHistory(history)

def plotROC(testy, lr_probs):
    lr_fpr, lr_tpr, _ = roc_curve(testy, lr_probs)
    plt.plot(lr_fpr, lr_tpr, marker='.', label='ROC')
    plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
    # axis labels
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # show the legend
    plt.legend()
    # show the plot
    plt.show()
    
def runPredictions(prediction,y):
    predictionSetSize = len(prediction)
    numCorrect = 0
    numNotDamagedCorrect = 0
    numNotDamaged = 0
    threshold = 1- 0.5


    for i in range(predictionSetSize):
        if (y[i][0] == 1):
            numNotDamaged += 1
            if (prediction[i][0] >= threshold) == True:
                numNotDamagedCorrect += 1

        if (prediction[i][0] >=threshold) == y[i][0]:
            numCorrect += 1


    print("\n")
    print(numCorrect, "correct out of", predictionSetSize, "\n Accuracy:", 100 * numCorrect / predictionSetSize)
    print("\n")
    print(numNotDamagedCorrect, "not damaged correct out of", numNotDamaged, "\naccuracy: ",
          100 * numNotDamagedCorrect / numNotDamaged)

def getClassifications(prediction, y):
    p=[]
    yout=[]
    for i in range(len(y)):
        p.append(prediction[i][1])
        yout.append(y[i][1])

    return yout,p

def runModel(workingDir, x_test, y_test, x_train, y_train):
    filePath = workingDir+"\\model-20.h5"
    model = load_model(filePath)
    y_test = to_categorical(y_test, num_classes=2)
    y_train = to_categorical(y_train, num_classes=2)

    print("\n\nValidation dataset")
    prediction = model.predict(x_test)
    runPredictions(prediction, y_test)

    y,p = getClassifications(prediction,y_test)
    plotROC(y,p)


    prediction = model.predict(x_train)
    y, p = getClassifications(prediction, y_train)
    plotROC(y, p)
