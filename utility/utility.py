import numpy as np


def normalize(x, new_min, new_max, old_min, old_max):
    new_x = (new_max - new_min) / (old_max - old_min) * (x - old_max) + new_max
    return round(new_x, 2)


def denormalize(normalized, minimum, maximum):
    denormalized = ((normalized + 1) * (maximum - minimum) + (2 * minimum)) / 2
    return denormalized


def clamp(n, minimum, maximum):
    if n < minimum:
        return minimum
    if n > maximum:
        return maximum
    return n


def linear_bin(a, N=15, offset=1, R=2.0):
    '''
    create a bin of length N
    map val A to range R
    offset one hot bin by offset, commonly R/2
    '''
    a = a + offset
    b = round(a / (R / (N - offset)))
    arr = np.zeros(N)
    b = clamp(b, 0, N - 1)
    arr[int(b)] = 1
    return arr


def linear_unbin(arr, N=15, offset=-1, R=2.0):
    '''
    preform inverse linear_bin, taking
    one hot encoded arr, and get max value
    rescale given R range and offset
    '''
    b = np.argmax(arr)
    a = b * (R / (N + offset)) + offset
    return a
