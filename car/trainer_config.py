import os
BATCH_SIZE = 128
TRAIN_TEST_SPLIT = 0.8
MODEL_PATH = '/home/pi/Development/Alpha-Neuron/pilot/models/'


def count_models():
    count = 0
    for name in os.listdir(MODEL_PATH):
        if os.path.isfile(os.path.join(MODEL_PATH, name)):
            if os.path.splitext(name)[1] == '.hd5':
                count += 1
    return count
