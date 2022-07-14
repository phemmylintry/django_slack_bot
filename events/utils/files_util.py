import os
import random

path = "files/"


def return_random_file():
    files = [os.path.join(path, file) for file in os.listdir(path)]

    return random.choice(files)
