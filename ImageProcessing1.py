import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
# path = r'C:\Users\Omer\Desktop\birb.png'
root_path = os.path.dirname(os.path.abspath(__file__))
path = cv2.imread(os.path.join(root_path, "index.jpeg"))
img = path
# variables
ix = -1
iy = -1
jx = 0
jy = 0
px=-1
py = -1

drawing = False
d = False
p= True


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
    global p,px,py
    if event == cv2.EVENT_LBUTTONDOWN:
        p = False
        px = x
        py = y





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
        median2 = round ((iy + jy)/2)
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

        #medial line bending
        img = cache
        axisa = abs(median - px)
        axisb = round(abs(iy-jy)/2)
        if (median>px):
            cv2.ellipse(img, (median, median2),(axisa,axisb),0,90,270,(0,0,255),2 )
        else:
            cv2.ellipse(img, (median, median2), (axisa, axisb), 180, 90, 270, (0, 0, 255), 2)
        # Displaying the image
        cv2.imshow("Title of Popup Window", img)
        cv2.waitKey(0)
        break

cv2.destroyAllWindows()

