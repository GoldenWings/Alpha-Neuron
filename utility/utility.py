def normalize(x, new_min, new_max, old_min, old_max):
    new_x = (new_max - new_min) / (old_max - old_min) * (x - old_max) + new_max
    return round(new_x, 2)
