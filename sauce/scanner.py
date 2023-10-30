import cv2
import pytesseract
import re
import argparse
import numpy
import imutils
from imutils.object_detection import non_max_suppression

#Top-down view
def eagleEye(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (1,1), 0.5)
    edges = cv2.Canny(blurred, 100, 150)
    cv2.imshow('edged', edges)
    cv2.imshow('edgedd', blurred)
    cv2.waitKey(0)

def scan():
    #Norm!
    image = cv2.imread('testReceipts/ginosMark.jpeg')
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