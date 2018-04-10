import os

DATA_PATH = '/home/pi/Development/Alpha-Neuron/Training Data/'
IMAGE_PATH = '/home/pi/Development/Alpha-Neuron/Training Data/Images/'


def count_datasets():
    count = 0
    for name in os.listdir(DATA_PATH):
        if os.path.isfile(os.path.join(DATA_PATH, name)):
            if os.path.splitext(name)[1] == '.csv':
                count += 1
    return count


def count_images():
    count = 0
    for name in os.listdir(IMAGE_PATH):
        if os.path.isfile(os.path.join(IMAGE_PATH, name)):
            if os.path.splitext(name)[1] == '.jpg':
                count += 1
    return count
