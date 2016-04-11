import cv2
import numpy as np
from os import listdir
from PIL import Image, ImageDraw
import ImageProcessing
import sys

# add the tools folder to the path
sys.path.append("../Tools")
import Array

RotationArray = []
Lines = []

for ImageName in listdir("./Processed"):
	# load the image into memory
	img = cv2.imread('Processed/' + ImageName)

	# invert the image so that the non-zero numbers (white) are the character outlines
	edges = ImageProcessing.invert(img)
	edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)

	# perform the canny operation
	Threshold = 150
	lines = cv2.HoughLinesP(edges, 1, np.pi / 180, Threshold, minLineLength=20, maxLineGap=100)

	AngleSum = 0
	NumberOfLines = 0

	# iterate through lines
	for line in lines:
		for x1, y1, x2, y2 in line:
			print x1, y1, x2, y2
			AngleSum += np.arctan2(x2 - x1, y2 - y1)
			NumberOfLines += 1
			Lines.append([x2, y1, x2, y2])

	# get the mean angle
	AngleSum /= NumberOfLines
	# convert to degrees
	AngleSum = (AngleSum / (np.pi * 2)) * 360

	RotationArray.append([ImageName, AngleSum])

for Object in RotationArray:
	print "rotate", Object[0], "by", Object[1], "degrees"

	ToRotate = Image.open("Processed/" + Object[0])

	# draw some lines on it
	# Drawing = ImageDraw.Draw(ToRotate)
	# for points in Lines:
	# 	Drawing.line((points[0], points[1], points[2], points[3]), fill=128)

	# rotate it
	ToRotate = ToRotate.convert('RGBA').rotate(-Object[1] + 90, expand=1)


	Final = Image.new('RGBA', ToRotate.size, (255, 255, 255, 255))
	Final = Image.composite(ToRotate, Final, ToRotate)

	# crop the image so that there's no white space showing at the edges
	Final = Array.CropImageAroundBlack(Final)

	Final.convert('L').save('Rotated/' + Object[0])