import os
import cv2
import random
import pandas as pd
import numpy as np

random.seed(2)

def get_vector(image, pair: int, pair_list):
    im = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    vector = []

    for coord in pair_list:
        p1 = im[coord[0][0]][coord[0][1]]
        p2 = im[coord[1][0]][coord[1][1]]

        if p1 > p2:
            bin_feature = 1
        else:
            bin_feature = 0
        vector.append(bin_feature)

    return vector

def analys(folder):
    circles_class = pd.read_csv("./dataset_c.csv")
    square_class = pd.read_csv("./dataset_s.csv")

    if len(circles_class) != len(square_class):
        print("количество дескрипторов классов неравно")
        return

    image = cv2.imread(folder+os.listdir(folder)[0], cv2.IMREAD_GRAYSCALE)
    h, w = image.shape
    pair = len(circles_class)
    pair_list = [[[random.randint(0, h-1), random.randint(0, w-1)], [random.randint(0, h-1), random.randint(0, w-1)]] for _ in range(pair)]

    cir = 0
    squ = 0

    dir_data = os.listdir(folder)
    for image in dir_data:
        vector = get_vector(folder+image, pair, pair_list)

        sq, ci = [], []
        
        for c, i in enumerate(vector):
            sq.append(square_class.iloc[c][str(i)])
            ci.append(circles_class.iloc[c][str(i)])

        a = np.prod(np.array(sq))
        b = np.prod(np.array(ci))

        if a > b:
            print("Это SQUARE")
            squ += 1
        elif a < b:
            print("Это CIRCLE")
            cir += 1
        else:
            print("Это неопределенность")

    print(f"Кол-во квадратов: {squ}; Кол-во кругов: {cir}")


analys(f"./images/for_check_s/")
