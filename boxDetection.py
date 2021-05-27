from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imagehash





vidcap = cv2.VideoCapture('test.mp4')
lastimagehash = None
success,image = vidcap.read()
sec = 0
frameRate = 0.5
count = -1
while success:
    count += 1
    sec += frameRate
    sec = round(sec, 2)
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    success,image = vidcap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # # show the grayscale image, if you want to show, uncomment 2 below lines
    # cv2.imwrite("gray.jpg",gray)

    # perform the canny edge detector to detect image edges
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)

    # # show the detected edges
    # cv2.imwrite("edges.jpg",edges)


    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rects = [cv2.boundingRect(cnt) for cnt in contours]
    rects = sorted(rects,key=lambda  x:x[2]*x[3],reverse=True)

    for rect in rects:
        x,y,w,h = rect
        area = w * h
        aspect_ratio = w/h


        if abs(aspect_ratio - (4/3)) < 0.1 and area > 200000:
            out = image[y:y+h,x:x+w]
            # masking
            mask = np.zeros(out.shape[:2], dtype="uint8")
            cv2.rectangle(mask, (0, h-32), (125, h), 255, -1)
            mask = cv2.bitwise_not(mask)
            masked_out = cv2.bitwise_and(out,out,mask=mask)
            
            image_hash = imagehash.phash(Image.fromarray(masked_out))
            if (lastimagehash == None):
                lastimagehash = image_hash
            elif (abs(image_hash - lastimagehash) > 4):
                print('saving slide at sec ' + str(sec))
                cv2.imwrite('boxes/cropped_' + str(count) + '.jpg', out)
                lastimagehash = image_hash
            break



