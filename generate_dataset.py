import os
import cv2
import random
import pandas as pd

random.seed(2)

# Байесовский алгоритм 
def get_vector(path: str, pair: int):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    h, w = image.shape

    pair_list = [[[random.randint(0, h-1), random.randint(0, w-1)], [random.randint(0, h-1), random.randint(0, w-1)]] for _ in range(pair)]

    vector = []

    for coord in pair_list:
        p1 = image[coord[0][0]][coord[0][1]]
        p2 = image[coord[1][0]][coord[1][1]]

        if p1 > p2:
            bin_feature = 1
        else:
            bin_feature = 0
        vector.append(bin_feature)

    return vector

def get_dataset(folder: str, descriptors: int):
    dir_data = os.listdir(folder)
    arr = [0 for _ in range(descriptors)]
    for image in dir_data:
        arr = list(map(sum, zip(arr, get_vector(folder+image, descriptors))))
        # print(arr)

    df = pd.DataFrame({
        "0": [(descriptors - a)/descriptors for a in arr],
        "1": [a/descriptors for a in arr]
    })
    
    df.to_csv("./dataset.csv", index=False)
    return

get_dataset("./images/squares/", 60)