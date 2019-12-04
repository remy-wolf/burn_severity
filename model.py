import tensorflow as tf
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
from keras.callbacks import ModelCheckpoint
from keras import regularizers, optimizers, Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
#todo CHANGE DIMENSIONS
IMAGE_CHANNELS, IMAGE_WIDTH, IMAGE_HEIGHT  =  3, 123, 123
INPUT_SHAPE = (IMAGE_CHANNELS, IMAGE_WIDTH, IMAGE_HEIGHT)
NORM_VAL = 127.5 # Normalize pixel values being passed in
# TODO FILL ABOVE





def getTFRecord(fileName):
    PATH = "C:\\Users\\Dillon\Desktop\\Senior_Project\\data\\{}.tfrecord.gz".format(fileName)
    trainDataset = tf.data.TFRecordDataset(PATH, compression_type='GZIP')
    print("-----------------------------------\n\n"+iter(trainDataset).next())



def initModel(keep_prob):
    # Create the neural network model for the problem
    model = Sequential()
    model.add(Lambda(lambda x: x/NORM_VAL - 1, input_shape=INPUT_SHAPE))
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





def train(model, batch_size, x_train, y_train, x_valid = None, y_valid= None):

    # todo fill values below
    split = 0.7
    epochs = 10
    samples_per_epoch = 500 # todo correct this
    learningRate = 1.0e-4
    # todo fill values above


    y_train = to_categorical(y_train, num_classes=2, dtype='float32')



    # Get ipnput and compile
    checkpoint = ModelCheckpoint('model-{epoch:02d}.h5',monitor='val_loss',verbose=0, save_best_only=False,mode='auto')

    model.compile(loss='binary_crossentropy', optimizer = optimizers.Nadam(lr=learningRate))

    model.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epochs, verbose=1, callbacks=checkpoint,
        validation_split=split, initial_epoch=0 , max_queue_size=10, use_multiprocessing=True)




