import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture('resources/carPArking.mp4')

width, height = 107, 48

#y1, y2 = 60, 95


def checkParkingSpace(imgpro):
    spaceCounter = 0

    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # Getting pos from poslist and display rectangles
    # for i, pos in posList:
    for i, pos in enumerate(posList):
        x, y = pos
        imgCrop = imgpro[y:y + height, x:x + width]
        # cv2.imshow(str(x*y), imgCrop)

        # To count no of pixels
        count = cv2.countNonZero(imgCrop)

        if count < 860:
            color = (0, 255, 0)  # Green
            thickness = 4
            spaceCounter += 1
             #print("X",x)
             #print("Y", y)
            # cvzone.putTextRect(vid, x, (x, y + height - 3), scale=1, thickness=1, offset=0, colorR=color)

        else:
            color = (0, 0, 255)  # Red
            thickness = 2
            # spaceCounter -= 1

        cv2.rectangle(vid, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # To write pixel count on img
        cvzone.putTextRect(vid, str(count), (x, y + height - 3), scale=1, thickness=1, offset=0,
                           colorR=color)  # (img, name, pos, scale, thickness, offset, clr)

        y1, y2 = 55, 100

        # seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        # for s in seq:
        #     if y1 + (50 * s) <= y <= y2 + (50 * s):

        if 46 <= x <= 64 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 1', (x, y + 15), scale=1, thickness=1, offset=0, colorR=color)

        if 140 <= x <= 180 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 2', (x, y + 15), scale=1, thickness=1, offset=0, colorR=color)

        if 370 <= x <= 423 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 3', (x, y + 15), scale=1, thickness=1, offset=0, colorR=color)

        if 495 <= x <= 527 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 4', (x, y + 15), scale=1, thickness=1, offset=0, colorR=color)

        if 730 <= x <= 771 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 5', (x, y + 15), scale=1, thickness=1, offset=0, colorR=color)

        if 889 <= x <= 929 and color == (0, 255, 0):
            cvzone.putTextRect(vid, f'Free: col 6', (x, y + 15), scale=1, thickness=1, offset=0, colorR=color)

        for s in seq:
            if y1 + (50 * s) <= y <= y2 + (50 * s) and color == (0, 255, 0):
                cvzone.putTextRect(vid, f'row {s+1 }', (x, y + 27), scale=1, thickness=1, offset=1, colorR=color)

    # Displaying remaining spaces
    # cvzone.putTextRect(vid, str(spaceCounter), (100, 50), scale=2, thickness=3, offset=9, colorR=(0, 255, 0))
    cvzone.putTextRect(vid, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3, thickness=3, offset=9,
                       colorR=(0, 255, 0))


with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:

    # To loop the video
    # current position(frame) == total no of frames of the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # Reset the frame(to zero), if they reach the total amount of frame of the video
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, vid = cap.read()

    imgGray = cv2.cvtColor(vid, cv2.COLOR_RGB2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # convert to binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25,
                                         16)  # (img, max value, method, binary inverse, blocksize)

    # to remove noise
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    # for pos in posList:
    #     cv2.rectangle(vid, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    cv2.imshow("Parking Video", vid)
    # cv2.imshow("BlurredVideo", imgBlur)
    # cv2.imshow("ImgThreshold", imgThreshold)
    # cv2.imshow("ImgMedian", imgMedian)
    cv2.waitKey(10)