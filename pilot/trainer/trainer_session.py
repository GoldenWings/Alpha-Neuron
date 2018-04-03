from datetime import datetime
from pilot.trainer.config import *


def store_command(command):
    timestamp = datetime.now()
    entry = command + " " + str(timestamp)
    with open(FILE_PATH, "w+") as writer:
        writer.write(entry+'\n')
