import cv2
import random

# Байесовский алгоритм 

image = cv2.imread("./images/squares/image_0.png", cv2.IMREAD_GRAYSCALE)

h, w = image.shape

pair_list = [[[random.randint(0, h-1), random.randint(0, w-1)], [random.randint(0, h-1), random.randint(0, w-1)]] for _ in range(40)]

vector = []

for coord in pair_list:
    p1 = image[coord[0][0]][coord[0][1]]
    p2 = image[coord[1][0]][coord[1][1]]

    if p1 > p2:
        bin_feature = 1
    else:
        bin_feature = 0
    vector.append(bin_feature)

print(vector)

#cv2.imshow("", image)
#cv2.waitKey()
#cv2.destroyAllWindows()

