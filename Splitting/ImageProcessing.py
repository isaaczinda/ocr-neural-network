import cv2
import numpy as np
from os import listdir
from PIL import Image

def invert(image):
    image = 255 - image
    return image

# return the image if there is no output path
def Outlines(InputImage, OutputPath=None):
	gray = cv2.cvtColor(InputImage, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

	if OutputPath != None:
		cv2.imwrite(OutputPath, invert(edges))
	else:
		return invert(edges)