import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math
import numpy
from operator import itemgetter
import sys
from os import listdir
import os
import cv2
import numpy as np
import glob

# add the tools folder to the path
sys.path.append("../Tools")
import Array
import Statistics

img = cv2.imread("Lines/3.png")

# compute the raw array
RawArray = Array.VerticalArrayFromImage(Image.fromarray(img))

# calculate filter and smooth sizes based on how big the image is
YFilterSize = Statistics.RoundToOdd(len(img) / 40)
XFilterSize = Statistics.RoundToOdd(len(img[0]) / 40)

# get the line height
LineHeight = 0
with open('SharedData/LineHeight.txt', 'r') as content_file:
    LineHeight = int(float(content_file.read()))

# use the line height, and make the smoothing size 1/2 of that 
SmoothSize = Statistics.RoundToEven(LineHeight / 2.0)
print "smooth size", SmoothSize

# use the recomended standard deviation
blur = cv2.GaussianBlur(img,(XFilterSize, XFilterSize), 0)

BlurredImageArray = Array.HorizontalArrayFromImage(Image.fromarray(blur))
RegularImageArray = Array.HorizontalArrayFromImage(Image.fromarray(img))

MeanArray = Array.MeanArray(RegularImageArray, SmoothSize)
MeanArrayBlurred = Array.MeanArray(BlurredImageArray, SmoothSize)


fig, ((ax1, ax2)) = plt.subplots(2, 1, sharex=False, sharey=False)


LocalMaxes = Array.FindAllLocalMaxes(BlurredImageArray)

# sets how different maximums from the 'same' point can be
# this may be incorrect and will FUCK us
NewMinimumThreshold = 5

# make sure that clusters of data are treated as one individual point
FilteredLocalMaxes = []
# add the first point because it automatically counts
FilteredLocalMaxes.append(LocalMaxes[0])

for i in range(1, len(LocalMaxes)):
	# the current crop point is set here
	CurrentCropPoint = FilteredLocalMaxes[len(FilteredLocalMaxes) - 1]

	# create an array of difference values between the two crop points
	ValueOffsetArray = BlurredImageArray[CurrentCropPoint:LocalMaxes[i]]

	TempArray = []
	for Item in ValueOffsetArray:
		TempArray.append(abs(Item - BlurredImageArray[CurrentCropPoint]))

	# check to see if the current min has other mins that should also be counted
	if sorted(TempArray, reverse=True)[0] <= NewMinimumThreshold:
		pass
	else:
		FilteredLocalMaxes.append(LocalMaxes[i])

# look at the difference between max values
DifferencesBetweenMaxesTemp = []
for i in range(1, len(FilteredLocalMaxes) - 1):
	FirstOffset = BlurredImageArray[FilteredLocalMaxes[i]] - BlurredImageArray[FilteredLocalMaxes[i - 1]]
	SecondOffset = -(BlurredImageArray[FilteredLocalMaxes[i + 1]] - BlurredImageArray[FilteredLocalMaxes[i]])
	DifferencesBetweenMaxesTemp.append([FirstOffset + SecondOffset, FilteredLocalMaxes[i]])

DifferencesBetweenMaxes = []
for i in range(1, len(FilteredLocalMaxes) - 1):
	FirstOffset = BlurredImageArray[FilteredLocalMaxes[i]] - BlurredImageArray[FilteredLocalMaxes[i - 1]]
	SecondOffset = -(BlurredImageArray[FilteredLocalMaxes[i + 1]] - BlurredImageArray[FilteredLocalMaxes[i]])
	DifferencesBetweenMaxes.append(FirstOffset + SecondOffset)

Mean = sum(DifferencesBetweenMaxes) / float(len(DifferencesBetweenMaxes))

SpaceDifferenceThreshold = 10
NumberOfSpaces = 0
for Item in DifferencesBetweenMaxes:
	if Item >= SpaceDifferenceThreshold:
		NumberOfSpaces += 1

print NumberOfSpaces, "spaces, mean", Mean
print DifferencesBetweenMaxes
#for i in range(0, DifferencesBetweenMaxes):


# create a temp arrays for visualizing
TempArray = []
# add the first stuff
for i in range(0, DifferencesBetweenMaxesTemp[0][1]):
	TempArray.append(0)

for i in range(0, len(DifferencesBetweenMaxesTemp) - 1):
	for q in range(DifferencesBetweenMaxesTemp[i][1], DifferencesBetweenMaxesTemp[i + 1][1]):
		TempArray.append(DifferencesBetweenMaxesTemp[i][0])

TempArray2 = []
for i in range(0, len(BlurredImageArray)):
	if i in FilteredLocalMaxes:
		TempArray2.append(100)
	else:
		TempArray2.append(0)

ax1.imshow(img)

ax2.plot(BlurredImageArray, color="green")
ax2.plot(TempArray)
ax2.plot(TempArray2)
#ax2.plot(Array.MeanArray(TempArray, 50))

# ax2.plot(BlurredImageArray, color="green")

# ax2.plot(BlurredImageArray, color="green")
# ax2.plot(MeanArray, color="red")
# ax3.imshow(blur)
# ax4.imshow(img)
	

plt.show()
