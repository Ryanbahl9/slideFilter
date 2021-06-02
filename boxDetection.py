from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imagehash
import sys


args = []
if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        args.append(arg)

for i in args:
    print(i)
videoFile = str(args[1])

destDir = str(args[2])

filterLevel = int(args[3])

vidcap = cv2.VideoCapture(videoFile)
lastimagehash = None
success,image = vidcap.read()

method = cv2.TM_SQDIFF_NORMED

sec = 0
frameRate = 0.5
count = -1
while success:
    count += 1
    if (count % 100 == 0):
        print ("count: " + str(count))
    sec += frameRate
    sec = round(sec, 2)
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    success,image = vidcap.read()


    # Read the images from the file
    im_key = cv2.imread('key_1')
    result = cv2.matchTemplate(im_key, image, method)
    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    # MPx,MPy = mnLoc

    # # Step 2: Get the size of the template. This is the same size as the match.
    # trows,tcols = im_key.shape[:2]

    # # Step 3: Draw the rectangle on large_image
    # cv2.rectangle(image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)

    # # Display the original image with the rectangle around the match.
    # cv2.imwrite('matched.png',image)

    if (mn < 0.005):
        continue

    # Read the images from the file
    im_key = cv2.imread('key_2')
    result = cv2.matchTemplate(im_key, image, method)
    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    if (mn < 0.005):
        continue

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
            elif (abs(image_hash - lastimagehash) > filterLevel):
                print('saving slide at sec ' + str(sec))
                cv2.imwrite(destDir + 'cropped_' + str(count) + '.jpg', out)
                # cv2.imwrite('boxes/cropped_' + str(sec) + '.jpg', image)
                lastimagehash = image_hash
            break



