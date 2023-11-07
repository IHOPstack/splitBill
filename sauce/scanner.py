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
    edges = cv2.Canny(closing, 50, 200)
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
        approx = cv2.approxPolyDP(c, .02*perimeter, True)
        print(len(approx))
        cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)
        cv2.imshow("sequencce", output)
        cv2.waitKey(0)
        if len(approx) == 4:
            receiptContour = approx
            print(receiptContour)
            break
    if receiptContour is None:
        print("receipt not found")
    #troubleshooting visualization
    output = image.copy()
    cv2.drawContours(output, [receiptContour], -1, (0, 255, 0), 2)
    cv2.imshow("outline", output)
    cv2.waitKey(0)
    #find rectangle lengths
    (A, B, C, D) = receiptContour
    print(A, B, C, D)
    dx1 = numpy.linalg.norm(A-D)
    dx2 = numpy.linalg.norm(B-C)
    width = int(max(dx1, dx2))
    dy1 = numpy.linalg.norm(A-B)
    dy2 = numpy.linalg.norm(D-C)
    height = int(max(dy1, dy2))
    inpoints = numpy.float32(receiptContour)
    outpoints = numpy.float32([[0, 0], [0, height-1], [width-1, height-1], [width-1, 0]])
    canvas = cv2.getPerspectiveTransform(inpoints, outpoints)
    topDown = cv2.warpPerspective(image, canvas, (width, height), flags = cv2.INTER_LINEAR)
    cv2.imshow("top", topDown)
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