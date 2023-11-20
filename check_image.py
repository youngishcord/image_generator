import os
import cv2
import random
import pandas as pd
import numpy as np

random.seed(2)

def get_vector(image, pair: int, pair_list):

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

def analys(image_path):
    circles_class = pd.read_csv("./dataset_c.csv")
    square_class = pd.read_csv("./dataset_s.csv")

    if len(circles_class) != len(square_class):
        print("количество дескрипторов классов неравно")
        return

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = image.shape
    pair = len(circles_class)
    pair_list = [[[random.randint(0, h-1), random.randint(0, w-1)], [random.randint(0, h-1), random.randint(0, w-1)]] for _ in range(pair)]
    vector = get_vector(image, pair, pair_list)

    # print(vector)

    sq, ci = [], []
    
    for c, i in enumerate(vector):
        sq.append(square_class.iloc[c][str(i)])
        ci.append(circles_class.iloc[c][str(i)])

    a = np.prod(np.array(sq))
    b = np.prod(np.array(ci))

    if a > b:
        print("Это SQUARE")
        return "s"
    elif a < b:
        print("Это CIRCLE")
        return "c"
    else:
        print("Это неопределенность")


analys(f"./images/for_check_c/")
