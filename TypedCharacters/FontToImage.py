from os import listdir
import sys
from PIL import Image, ImageDraw
import subprocess
import cv2
import numpy
import math

def invert(image):
    image = 255 - image
    return image

# save the character files as JPEGs
#for CharacterFile in listdir("./Fonts"):
for CharacterFile in ["calibri.ttf", "times.ttf"]:
	if ".ttf" in CharacterFile.lower():
		FontName = CharacterFile[0:len(CharacterFile) - 4]
		print "converting", FontName
		subprocess.call("convert -kerning 80 -background white -fill black -font \"./Fonts/" + FontName + ".ttf\" -pointsize 300 label:\"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\" \"./Sheets/" + FontName + ".png\"", shell=True)

print "detecting outlines"


for File in listdir("Sheets"):
	gray = cv2.imread("Sheets/" + File, cv2.IMREAD_GRAYSCALE)
	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
	cv2.imwrite("Sheets/" + File, invert(edges))