#todo fill this out
INPUT_SHAPE = 1
NORM_VAL = 128 # Normalize pixel values being passed in
# TODO FILL ABOVE







def initModel(keep_prob):
    # todo fit to classification model

    # Create the neural network model for the problem
    model = Sequential()
    model.add(Lambda(lambda x: x/NORM_VAL, input_shape=INPUT_SHAPE))
    model.add(Conv2D(64,  5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(128, 5, 5, activation='elu', subsample=(2, 2)))
    model.add(Conv2D(256, 5, 5, activation='elu'))
    model.add(Dropout(keep_prob))
    model.add(Flatten())
    model.add(Dense(200, activation='elu', bias=True))
    model.add(Dense(100, activation='elu', bias=True))
    model.add(Dense(50, activation='elu', bias=True))
    model.add(Dense(10, activation='elu', bias=True))
    model.add(Dense(1, activation='softmax'))

    return model





def train(model, batch_size, x_train, y_train, x_valid, y_valid):

    # todo fill values below
    epochs = 10
    samples_per_epoch = 500 # todo correct this
    learningRate = 1.0e-4
    # todo fill values above


    # Get ipnput and compile
    checkpoint = ModelCheckpoint('model-{epoch:02d}.h5', monitor='val_loss', verbose=0, save_best_only=False,
                                 mode='auto')

    model.compile(loss='mean_squared_error', optimizer = optimizers.Nadam(lr=learningRate))
    model.fit_generator(INSERT_BATCH_HERE, samples_per_epoch,
                        epochs, max_q_size=1, validation_data=INSERT_VALIDATION_BATCH_HERE,
                        nb_val_samples=len(x_valid), callbacks=[checkpoint], verbose=1)




