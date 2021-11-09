import cv2
import os
#gyghsa
# path = r'C:\Users\Omer\Desktop\birb.png'
root_path = os.path.dirname(os.path.abspath(__file__))
path = cv2.imread(os.path.join(root_path, "index.jpeg"))
img = path
# variables
ix = -1
iy = -1
drawing = False
d = False
one = 0
two = 0


def draw_reactangle_with_drag(event, x, y, flags, param):
    global ix, iy, drawing, img, d, one, two
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
        one = x
        two = y


cv2.namedWindow(winname="Title of Popup Window")
cv2.setMouseCallback("Title of Popup Window", draw_reactangle_with_drag)

while True:
    cv2.imshow("Title of Popup Window", img)
    if cv2.waitKey(10) == 27:
        break
        cv2.destroyAllWindows()
    if d:
        cv2.imshow("Title of Popup Window", img)
        median = round((ix + one) / 2)
        pointA = (median, iy)
        pointB = (median, two)
        cv2.line(img, pointA, pointB, (0, 0, 255), thickness=2)
        cv2.imshow("Title of Popup Window", img)
        cv2.waitKey(0)
        break

cv2.destroyAllWindows()
