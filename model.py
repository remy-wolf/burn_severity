import tensorflow as tf
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
from keras.callbacks import ModelCheckpoint
from keras import regularizers, optimizers, Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import load_model


# Input parameters
IMAGE_CHANNELS, IMAGE_WIDTH, IMAGE_HEIGHT  =  3, 123, 123
INPUT_SHAPE = (IMAGE_CHANNELS, IMAGE_WIDTH, IMAGE_HEIGHT)
NORM_VAL = 127.5 # Normalize pixel values being passed in


def initModel(keep_prob):
    # Create the neural network model for the problem
    model = Sequential()
    model.add(Lambda(lambda x: x/127.5 - 1, input_shape=INPUT_SHAPE))
    model.add(Conv2D(64,  (3, 3), activation="elu", strides=(2, 2), data_format='channels_first'))
    model.add(Conv2D(64,  (3, 3), activation="elu", strides=(2, 2)))
    model.add(Conv2D(256, (3, 3), activation="elu"))
    model.add(Dropout(keep_prob))
    model.add(Flatten())
    model.add(Dense(200, activation="elu", use_bias=True))
    model.add(Dense(100, activation="elu", use_bias=True))
    model.add(Dense(50, activation="elu", use_bias=True))
    model.add(Dense(10, activation="elu", use_bias=True))
    model.add(Dense(2, activation="softmax"))

    return model





def train(model, x, y, split, batch_size, learningRate, epochs):



    y = to_categorical(y, num_classes=2)



    # Get input and compile
    checkpoint = ModelCheckpoint('model-{epoch:02d}.h5',monitor='val_loss',verbose=0, save_best_only=False,mode='auto')
    #todo
    model.compile(loss='categorical_crossentropy', optimizer = optimizers.Nadam(lr=learningRate), metrics=['acc'])

    print("\n\n\n------------------Fit--------------------------------------\n\n\n")
    model.fit(x=x, y=y, epochs=epochs,validation_split=split, batch_size=batch_size, verbose=1, callbacks=[checkpoint])





def runModel(workingDir, x_test, y_test):
    filePath = workingDir+"\\model-10.h5"
    model = load_model(filePath)
    y = to_categorical(y_test, num_classes=2)

    prediction = model.predict(x_test)

    prediction >= prediction

    # print(prediction)

