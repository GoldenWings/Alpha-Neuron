from keras.layers import Input
from keras.models import Model
from keras.layers import Convolution2D
from keras.layers import Dropout, Flatten, Dense
from keras.optimizers import Adam


def build_model(input_shape=(120, 160, 3)):
    opt = Adam()
    drop = 0.1

    img_in = Input(shape=input_shape,
                   name='img_in')  # First layer, input layer, Shape comes from camera.py resolution, RGB
    x = img_in
    x = Convolution2D(24, (5, 5), strides=(2, 2), activation='relu')(
        x)  # 24 features, 5 pixel x 5 pixel kernel (convolution, feauture) window, 2wx2h stride, relu activation
    x = Dropout(drop)(x)  # Randomly drop out (turn off) 10% of the neurons (Prevent overfitting)
    x = Convolution2D(32, (5, 5), strides=(2, 2), activation='relu')(
        x)  # 32 features, 5px5p kernel window, 2wx2h stride, relu activatiion
    x = Dropout(drop)(x)  # Randomly drop out (turn off) 10% of the neurons (Prevent overfitting)
    if input_shape[0] > 32:
        x = Convolution2D(64, (5, 5), strides=(2, 2), activation='relu')(
            x)  # 64 features, 5px5p kernal window, 2wx2h stride, relu
    else:
        x = Convolution2D(64, (3, 3), strides=(1, 1), activation='relu')(
            x)  # 64 features, 5px5p kernal window, 2wx2h stride, relu
    if input_shape[0] > 64:
        x = Convolution2D(64, (3, 3), strides=(2, 2), activation='relu')(
            x)  # 64 features, 3px3p kernal window, 2wx2h stride, relu
    elif input_shape[0] > 32:
        x = Convolution2D(64, (3, 3), strides=(1, 1), activation='relu')(
            x)  # 64 features, 3px3p kernal window, 2wx2h stride, relu
    x = Dropout(drop)(x)  # Randomly drop out (turn off) 10% of the neurons (Prevent overfitting)
    x = Convolution2D(64, (3, 3), strides=(1, 1), activation='relu')(
        x)  # 64 features, 3px3p kernal window, 1wx1h stride, relu
    x = Dropout(drop)(x)  # Randomly drop out (turn off) 10% of the neurons (Prevent overfitting)
    # Possibly add MaxPooling (will make it less sensitive to position in image).  Camera angle fixed,
    #  so may not to be needed

    x = Flatten(name='flattened')(x)  # Flatten to 1D (Fully connected)
    x = Dense(100, activation='relu')(x)  # Classify the data into 100 features, make all negatives 0
    x = Dropout(drop)(x)  # Randomly drop out (turn off) 10% of the neurons (Prevent overfitting)
    x = Dense(50, activation='relu')(x)  # Classify the data into 50 features, make all negatives 0
    x = Dropout(drop)(x)  # Randomly drop out 10% of the neurons (Prevent overfitting)
    # categorical output of the angle
    angle_out = Dense(15, activation='softmax', name='angle_out')(x)
    # Connect every input with every output and output 15 hidden units.
    # Use Softmax to give percentage. 15 categories and find best one based off percentage 0.0-1.0

    # continous output of throttle
    throttle_out = Dense(4, activation='softmax', name='throttle_out')(x)  # Reduce to 1 number,
    #  Positive number only

    model = Model(inputs=[img_in], outputs=[angle_out, throttle_out])
    model.compile(optimizer='adam',
                  loss={'angle_out': 'categorical_crossentropy',
                        'throttle_out': 'categorical_crossentropy'},
                  loss_weights={'angle_out': 0.5, 'throttle_out': 1.0})
    return model
