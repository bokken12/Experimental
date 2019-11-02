import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def tem_match(orig, src, template):
    # img = src
    # img2 = img.copy()
    # template = templ
    w, h = template.shape[::-1]
    # orig_res = None
    methods = ['cv.TM_CCOEFF_NORMED']
    # for meth in methods:
    img = src.copy()
    resize_i = img.copy()
    method = eval(methods[0])
    print(method)    
    for i in range(4):
        resize_i = cv.resize(img, None,fx=1/2**(0.5*i), fy=1/2**(0.5*i), interpolation = cv.INTER_AREA)
        print(resize_i.shape)

        # Apply template Matching
        res = cv.matchTemplate(resize_i, template, method)
        if i == 0:
            orig_res = res

        threshold = 0.68
        loc = np.where( res >= threshold)
        print(loc)
        for pt in zip(*loc[::-1]):
            print(pt)
            cv.rectangle(orig, (pt[0]*int(2**(0.5*i)),pt[1]*int(2**(0.5*i))), ((pt[0] + w), (pt[1] + h)), (0,0,255), 1)
            break
    cv.imshow('Matching Result', orig_res)
    cv.imshow('Detected Point', orig)

cap = cv.VideoCapture('test480.mp4')
#cap = cv.VideoCapture('gate.mp4')
templ = cv.imread('red.jpg')
#templ = cv.imread('right.jpg')
# buoy = cv.imread('buoy.png')
# orig = cv.imread('orig.png')
i = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    templ_gray = cv.cvtColor(templ, cv.COLOR_BGR2GRAY)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('temp', templ_gray)

    tem_match(frame,frame_gray, templ_gray)

    cv.waitKey(100)
    i += 1
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
