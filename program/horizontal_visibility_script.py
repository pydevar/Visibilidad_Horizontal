#!/usr/bin/env python

__version__ = "Version 1.0"
__copyright__ = "Copyright 2015, PydevAr"
__email__ = "pydev.ar@gmail.com"

# Libraries
import cv2
import sys
import os
import csv

from config import *

def store_data():
    global writer, csvfile
    csvfile = open(FILENAME, 'wb')
    if not os.path.isfile(FILENAME):
        print "Error: file %s doesn't exist." % FILENAME
    csvfile.write("sep=,\n")  # For excel compatibility
    FIELDNAMES = ['ID Baliza',
                  'Coordenada X',
                  'Coordenada Y',
                  'Valor Pixel',
                  'Valor Referencia',
                  'Seleccionado',
                  'Distancia']
    writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
    writer.writeheader()

try:
    store_data()
except:
    print "Problem writing csv file."

def save_coord(id, cx, cy, pixel):
    global writer
    try:
        writer.writerow({
            'ID Baliza': id,
            'Coordenada X': int(cx) + refPt[0][0],
            'Coordenada Y': int(cy) + refPt[0][1],
            'Valor Pixel': pixel,
            'Valor Referencia': ' ',
            'Seleccionado': ' ',
            'Distancia': ' '
            })
    except:
        print "Problem writing file."

def average_value(image, cx, cy):
    global refPt
    image1, image2, image3 = [0, 0, 0]
    # print "cx:", cx, "cy:", cy
    counter = 0.0
    for x in range(cx-2, cx+3):
        for y in range(cy-2, cy+3):
            counter += 1.0
            # print x, y, image[y][x]
            image1 += image[y][x][0]
            image2 += image[y][x][1]
            image3 += image[y][x][2]
    ret = [round(image1 / counter, 1), round(image2 / counter, 1), round(image3 / counter, 1)]
    # print "returns", ret
    return ret

print "OpenCV Version:", cv2.__version__, "\n"

# Reading image
img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_UNCHANGED)
clone = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

try:
    img.shape
except:
    print "The image could not be loaded."
    sys.exit()
# -----------------------------------------------------
print "-"*5, "Information of the image", "-"*5
print "Image Shape:", img.shape
print "Total number of pixels:", img.size
print "Image data type:", img.dtype
# -----------------------------------------------------


# display the image resized
# original = cv2.resize(img, SIZE)
# cv2.imshow("original", original)


roi = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
# cv2.imshow("ROI", roi)

clone = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
# cv2.imshow("clone", clone)

_dummy, b_clone = cv2.threshold(clone, 200, 255, cv2.THRESH_BINARY)
# cv2.imshow("b_clone", b_clone)
# cv2.waitKey(0)

cv2.imshow("original", roi.copy())
contours, _h = cv2.findContours(b_clone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# print contours

dict_values = dict()
id = 0
for blob in contours:

    # finding centroids of best_cnt and draw a rectangle there
    if blob is not None:
        x, y, w, h = cv2.boundingRect(blob)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 3)

    M = cv2.moments(blob)
    if M['m00'] != 0:
        cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #print id, cx, cy, roi[cy][cx]
        #save_coord(id, cx, cy, average_value(roi, cx, cy))
        dict_values[id] = [cx, cy, average_value(roi, cx, cy)]
        id += 1
cv2.imshow("roi", roi)
# cv2.imshow("clone", clone)
cv2.waitKey(0)


def save_values():
    for i in range(len(dict_values.keys())):
        save_coord(i, *dict_values[i])
    csvfile.close()

save_values()