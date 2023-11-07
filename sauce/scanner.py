import cv2
import pytesseract
import re
import numpy
import imutils
from imutils.object_detection import non_max_suppression

def eagleEye(image): #Top-down view
    #pre-process image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilated = cv2.dilate(blurred, kernel)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=3)
    cv2.imshow('closed', closing)
    edges = cv2.Canny(closing, 75, 200)
    cv2.imshow('edged', edges)
    cv2.waitKey(0)
    #find receipt contour
    receiptContour = None
    contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=lambda c: cv2.arcLength(c, True), reverse=True)
    for c in contours:
        output = image.copy()
        perimeter = cv2.arcLength(c, True)
        print(cv2.contourArea(c))
        print(perimeter)
        approx = cv2.approxPolyDP(c, 3, True)
        print(approx)

        cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)
        cv2.imshow("sequencce", output)

        rectangle = cv2.boundingRect(approx)
        rectX, rectY, rectWidth, rectHeight = rectangle
        print(rectangle, rectX, rectY, rectWidth, rectHeight)
        cv2.waitKey(0)
        rectArea = rectWidth * rectHeight
        if rectArea > 5000: #arbitrary size that should narrow most false rectangles
            hull = cv2.convexHull(c)


    if receiptContour is None:
        print("receipt not found")
    #troubleshooting visualization
    output = image.copy()
    cv2.drawContours(output, [receiptContour], -1, (0, 255, 0), 2)
    cv2.imshow("outline", output)
    cv2.waitKey(0)
        



def scan(image):
    #Norm!
    originalImage = image.copy()
    newDimensions = numpy.zeros((originalImage.shape[0], originalImage.shape[1]))
    normie = cv2.normalize(originalImage, newDimensions, 0, 255, cv2.NORM_MINMAX)
    eagleEye(normie)

#Scaling


#Noise Reduction


#Skeletor


#Fifty Shades of Grey


#Thresholding


#ROI Selection