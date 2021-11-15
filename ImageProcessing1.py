import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, floor
#import scipy.ndimage

# path = r'C:\Users\Omer\Desktop\birb.png'
root_path = os.path.dirname(os.path.abspath(__file__))
path = cv2.imread(os.path.join(root_path, "index.jpeg"))
img = path
# variables
ix = -1
iy = -1
jx = 0
jy = 0
px = -1
py = -1

drawing = False
d = False
p = True


def draw_reactangle_with_drag(event, x, y, flags, param):
    global ix, iy, drawing, img, d, jx, jy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = cv2.imread(os.path.join(root_path, "index.jpeg"))
            cv2.rectangle(
                img2, pt1=(ix, iy), pt2=(x, y), color=(255, 0, 0), thickness=2
            )
            img = img2

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img2 = cv2.imread(os.path.join(root_path, "index.jpeg"))
        cv2.rectangle(img2, pt1=(ix, iy), pt2=(x, y), color=(0, 255, 0), thickness=2)
        img = img2
        d = True
        jx = x
        jy = y


def draw_curve(event, x, y, flags, param):
    global p, px, py
    if event == cv2.EVENT_LBUTTONDOWN:
        p = False
        px = x
        py = y


def interpolate_img(rectangle_img, x_intersection, y_intersection, interpolation_flag):

    rec_height = abs(jy - iy)
    if rec_height % 2 != 0:
        rec_height += 1
    rec_length = abs(jx - ix)
    print(rectangle_img.shape)
    interpolated_img = np.zeros((rec_height, rec_length, 3), np.uint8)
    parab_heights = get_parab_heights(x_intersection, y_intersection, rec_height)
    print("parab_heights:",parab_heights)
    print("length parab height",len(parab_heights))
    print (rec_height)
#I added a boolean that checks if it is right or left interpolation
    if not rightinterpolation:
        for k in range(rec_height):
            reached_parabola = False
            max_offset = floor(parab_heights[k])
            parabola_intersection = max_offset + rec_length / 2

            offset = 0
            offset_reduction = 0
            for i in range(rec_length):
                # pixel = rectangle_img[k][rec_length - i - 1]
                new_pixel = interpolate(
                    rectangle_img, (k, rec_length - i - 1), offset, interpolation_flag
                )
                ## as if we're iterating through the image right to left
                interpolated_img[k][rec_length - i - 1] = new_pixel
                if not reached_parabola:
                    offset = round(max_offset * (i / parabola_intersection))
                else:
                    offset_reduction -= 1
                    offset = max_offset * (offset_reduction / (rec_length - parabola_intersection))
                if offset >= max_offset:
                    reached_parabola = True
                    offset_reduction = rec_length - parabola_intersection
                offset = round(offset)
        return interpolated_img
    #until here it is suppose to be ok

# Omer's Changes!!!!!!!!!!!!!
    else:
        for k in range(rec_height):
            reached_parabola = False
            max_offset = floor(parab_heights[k])
            parabola_intersection = (rec_length / 2) - max_offset
            offset = 0
            offset_reduction = 0
            for i in range(rec_length):
                # pixel = rectangle_img[k][rec_length - i - 1]
                new_pixel = interpolate(
                    rectangle_img, (k, rec_length-i-1), offset, interpolation_flag
                )
                ## as if we're iterating through the image right to left
                interpolated_img[k][rec_length-i-1] = new_pixel
                if not reached_parabola:
                    offset = round(max_offset * (i / parabola_intersection))*-1
                else:
                    offset_reduction += 1
                    offset = max_offset * (offset_reduction /(rec_length - parabola_intersection))*-1
                if offset >= max_offset:
                    reached_parabola = True
                   # offset_reduction = rec_length - parabola_intersection
                    offset_reduction = parabola_intersection
                offset = round(offset)
        return interpolated_img


# Omer's Changes!!!!!!!!!!!!!


def get_parab_heights(x_intersection, y_intersection, rectangle_height):
    return [
        get_height(y, x_intersection, y_intersection)
        for y in range(-y_intersection, y_intersection)
    ]


def get_height(y, x_intersection, y_intersection):
    return sqrt((1 - ((y ** 2) / y_intersection ** 2)) * (x_intersection ** 2))


def interpolate(rectangle_img, pixel_coordinates, offset, interpolation_flag):
    height = pixel_coordinates[0]
    width = pixel_coordinates[1] + offset
    if interpolation_flag == "nn":
        pixels = find_k_nearest(rectangle_img, 1, (width, height))
        weights = np.full(shape=(1, 1), fill_value=1, dtype=float)
        return np.dot(pixels, weights).transpose()
    if interpolation_flag == "bilinear":
        pixels = find_k_nearest(rectangle_img, 4, (width, height))
        weights = np.full(shape=(4, 1), fill_value=0.25, dtype=float)
        return np.dot(pixels, weights).transpose()
    if interpolation_flag == "bicubic":
        pixels = find_k_nearest(rectangle_img, 16, (width, height))
        weights = np.full(shape=(16, 1), fill_value=1 / 16, dtype=float)
        return np.dot(pixels, weights).transpose()
    return


def find_k_nearest(img, k, target):
    res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nonzero = cv2.findNonZero(res)
    distances = np.sqrt(
        (nonzero[:, :, 0] - target[0]) ** 2 + (nonzero[:, :, 1] - target[1]) ** 2
    )
    distances = distances.flatten()
    k_nearest = np.argpartition(distances, k)
    pixel_locations = nonzero[k_nearest[:k]]
    # print(pixel_locations)
    pixel_colors = np.ndarray(shape=(k, 3))
    for i in range(k):
        pixel_colors[i] = img[pixel_locations[i][0, 1], pixel_locations[i][0, 0]]
    return pixel_colors.transpose()


cv2.namedWindow(winname="Title of Popup Window")
cv2.setMouseCallback("Title of Popup Window", draw_reactangle_with_drag)


while True:
    cv2.imshow("Title of Popup Window", img)
    if cv2.waitKey(10) == 27:
        break
        cv2.destroyAllWindows()
    if d:
        cv2.imshow("Title of Popup Window", img)
        median = round((ix + jx) / 2)
        median2 = round((iy + jy) / 2)
        pointA = (median, iy)
        pointB = (median, jy)
        cache = img.copy()
        cv2.line(img, pointA, pointB, (0, 0, 255), thickness=2)
        cv2.imshow("Title of Popup Window", img)
        cv2.setMouseCallback("Title of Popup Window", draw_curve)
        while p:
            if cv2.waitKey(10) == 27:
                break
                cv2.destroyAllWindows()

        ##medial line bending
        img = cache
        axisa = abs(median - px)
        axisb = round(abs(iy - jy) / 2)
        #checks if we should iteroplate to the left or to the right
        rightinterpolation = median < px
        print ("right?", rightinterpolation)
        if not rightinterpolation:
            cv2.ellipse(
                img, (median, median2), (axisa, axisb), 0, 90, 270, (0, 0, 255), 2
            )
        else:
            cv2.ellipse(
                img, (median, median2), (axisa, axisb), 180, 90, 270, (0, 0, 255), 2
            )
        # Displaying the image
        cv2.imshow("Title of Popup Window", img)
        print(jy)
        print(iy)
        print(jx)
        print(ix)
        if abs(jy-iy)%2!=0:
            if jy%2!=0:
                jy=jy-1
            else:
                iy=iy+1
        print("height", abs(jy - iy))
        new_img = interpolate_img(img[iy:jy, ix:jx], axisa, axisb, "bicubic")
        cv2.imshow("Title of Popup Window", new_img)
        cv2.waitKey(0)
        break

cv2.destroyAllWindows()
