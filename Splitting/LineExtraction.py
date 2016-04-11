import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math
import numpy
from operator import itemgetter
import sys
from os import listdir
import cv2
import numpy as np

# add the tools folder to the path
sys.path.append("../Tools")
import Array
import Statistics

def PixelSumOnLine(Pixels, PointOne, PointTwo):
	ChangeX = abs(PointTwo[0] - PointOne[0])
	ChangeY = abs(PointTwo[1] - PointOne[1])
	Slope = (PointTwo[1] - PointOne[1]) / (PointTwo[0] - PointOne[0])
	XDirection = numpy.sign(ChangeX)
	YDirection = numpy.sign(ChangeY)

	x = PointOne[0]
	y = PointOne[1]

	Sum = 0
	try:
		while abs(x - PointOne[0]) < ChangeX:
			Sum += Pixels[math.floor(x), math.floor(y)]
			# add to x and y
			x += 1
			y += Slope
	# if it is out of range, return 255 we don't force the line from the side
	except IndexError:
		return 255

	# divide sum by number of samples taken
	return Sum / ChangeX


# look at the first file in the folder
FileName = listdir("Processed")[0]
#FileName = "Cropped4.png"

# open the text image
TextImage = Image.open("Processed/" + FileName)
# convert it to a grayscale image and remove alpha
TextImage = TextImage.convert('L')
# load the pixels
TextPixels = TextImage.load()

def CalculateCropPoints(LineHeight, ShowGraphs=False):
	global FileName 

	# do the gaussian smoothing that enables us to find the crop points
	# blur the image
	img = cv2.imread("Processed/" + FileName)

	# calculate filter and smooth sizes based on how big the image is
	YFilterSize = Statistics.RoundToOdd(len(img) / 20)
	XFilterSize = Statistics.RoundToOdd(len(img[0]) / 20)
	SmoothSize = Statistics.RoundToEven(len(img) / 20)

	# use the line height, and make the smoothing size 1/2 of that 
	SmoothSize = Statistics.RoundToEven(LineHeight / 2.0)

	print "smooth size", SmoothSize

	# use the recomended standard deviation
	blur = cv2.GaussianBlur(img,(XFilterSize, YFilterSize), 0)

	RawArray = Array.VerticalArrayFromImage(Image.fromarray(img))
	BlurredImageArray = Array.VerticalArrayFromImage(Image.fromarray(blur), BandPercentage=.5)
	MeanArray = Array.MeanArray(BlurredImageArray, SmoothSize)
	MedianArray = Array.MedianArray(BlurredImageArray, SmoothSize)

	# get the crop points by finding local maxes
	CropPoints = Array.FindAllLocalMaxes(MeanArray)

	# check to see if there should be any extra crop points added
	SlopeArray = Array.FindSlope(MeanArray)
	# if the initial slope is less than 0
	if SlopeArray[0] < 0:
		# insert 0 at position 0
		CropPoints.insert(0, 0)
	# if the final slope is more than 0 or 0
	if SlopeArray[len(SlopeArray) - 1] >= 0:
		CropPoints.append(len(MeanArray) - 1)

	if ShowGraphs:
		# graph / visualize some stuff
		TempArray = []
		for i in range(0, len(MeanArray)):
			if i in CropPoints:
				TempArray.append(255)
			else:
				TempArray.append(150)

		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=False, sharey=False)		
		ax1.set_title("Blurred then Mean")
		ax1.plot(MeanArray)
		ax1.plot(RawArray)
		ax2.plot(BlurredImageArray)
		ax2.plot(RawArray)
		ax2.set_title("Blurred")
		ax3.imshow(img)
		ax3.set_title("Image")
		ax4.imshow(blur)
		ax4.set_title("Blur Image")
		plt.show()

	return CropPoints

# calculate the crop point, guessing line height 80
PreliminaryCropPoints = CalculateCropPoints(80)

Spacing = Array.AverageSpacing(PreliminaryCropPoints)

# calculate crop points again using the new line height
CropPoints = CalculateCropPoints(Spacing, ShowGraphs=True)
#print "new spacing", Array.AverageSpacing(CropPoints)

# get the image drawing canvas ready 
Drawing = ImageDraw.Draw(TextImage)

# number of segments that will be used to segment
# each segment is 10 pixels wide
NumberOfSegments = int(TextImage.size[0] / 10.0) 

# this is a list of the line segments that the image needs to be cropped between
CropField = []	

InitialLineLengthPercentage = .1

# do segmentation for each crop point
for CropPoint in CropPoints:
	# create a new array for each point in CropPoints
	CropField.append([])

	# calculate the change in x for each line segment
	# make sure that deltax is computed with the initial length subtracted off
	DeltaX = math.floor(TextImage.size[0] * (1 - InitialLineLengthPercentage) / float(NumberOfSegments))
	# use the preset y coordinate which is already white space
	YCoordinate = CropPoint
	# start the x coordinate at 0
	XCoordinate = 0

	# setup the crop field so that there is a flat line at the beginning
	CropField[len(CropField) - 1].append([XCoordinate, YCoordinate])

	# add 10% of the width to x, don't change y
	XCoordinate += TextImage.size[0] * InitialLineLengthPercentage

	for i in range(0, NumberOfSegments):
		PixelSumArray = []

		# change in y varies based on the size of the image
		for DeltaY in range(-int(DeltaX / 1), int(DeltaX / 1) + 1):
			# check farther out than the line will actually be. This leads to no short-sighted behavior 
			# however, sometimes there is a long-term path that is actually much better and not flat
			ExtraLength = 4
			XCheckDistance = DeltaX * ExtraLength

			# make sure that the check distance is never too far
			DistanceFromEdge = abs(XCoordinate - (TextImage.size[0] - 1))
			if DistanceFromEdge < XCheckDistance:
				XCheckDistance = DistanceFromEdge

			# multiply by extra length to ensure that angle is preserved
			Sum = PixelSumOnLine(TextPixels, (XCoordinate, YCoordinate), (XCoordinate + XCheckDistance, YCoordinate + int(DeltaY * ExtraLength)))

			# add the sum and the DeltaY
			PixelSumArray.append([Sum, DeltaY])

		# sort pixelsummary to find value with highest average number
		PixelSumArray = sorted(PixelSumArray, key=itemgetter(0), reverse=True)

		# average all of the values that are the same 
		DeltaYAverage = 0
		NumberOfValues = 0

		# this is the lowest value
		TargetValue = PixelSumArray[0][0]

		for Item in PixelSumArray:
			if Item[0] == TargetValue:
				# add the deltay to the average
				DeltaYAverage += Item[1]
				NumberOfValues += 1

		DeltaYAverage /= NumberOfValues

		# this prevents the lines from ever leaving the image
		if YCoordinate + DeltaYAverage < 0:
			DeltaYAverage = YCoordinate
			
		# draw a nice line on the image
		Drawing.line((XCoordinate, YCoordinate, XCoordinate + DeltaX, YCoordinate + DeltaYAverage), fill=128)

		# add the current coordinates to the CropField before they change
		CropField[len(CropField) - 1].append([XCoordinate, YCoordinate])

		# add to the x coordinate
		XCoordinate += DeltaX
		# add the selected change in y
		YCoordinate += DeltaYAverage
	# append to the crop field here to make sure we get the last one
	CropField[len(CropField) - 1].append([XCoordinate, YCoordinate])
	# append here because for the deltax calculations we are rounding down and there will be some extra space
	CropField[len(CropField) - 1].append([TextImage.size[0], CropField[len(CropField) - 1][len(CropField[len(CropField) - 1]) - 1][1]])

for p in range(0, len(CropField) - 1):
	# make a copy of the text image
	LineImage = TextImage.copy()

	# find the bounds with which we shall crop the image
	SmallestY = sorted(CropField[p], key=itemgetter(1), reverse=False)[0][1]
	LargestY = sorted(CropField[p + 1], key=itemgetter(1), reverse=True)[0][1]

	# crop the image
	LineImage = LineImage.crop((0, SmallestY, LineImage.size[0], LargestY))

	# load the line image into pixels
	LineImagePixels = LineImage.load()

	Row = CropField[p]
	for i in range(0, len(Row) - 1):
		Slope = float(Row[i][1] - Row[i + 1][1]) / float(Row[i][0] - Row[i + 1][0])

		# iterate through all x values
		y = Row[i][1] - SmallestY

		for x in range(int(Row[i][0]), int(Row[i + 1][0])):
			for tempy in range(0, int(math.ceil(y))):
				LineImagePixels[x, tempy] = 256

			# add slope to y because x always changes by 1
			y += Slope

	Row = CropField[p + 1]
	for i in range(0, len(Row) - 1):
		Slope = float(Row[i][1] - Row[i + 1][1]) / float(Row[i][0] - Row[i + 1][0])

		# iterate through all x values
		y = Row[i][1] - SmallestY

		for x in range(int(Row[i][0]), int(Row[i + 1][0])):
			for tempy in range(int(math.floor(y)), LineImage.size[1]):
				LineImagePixels[x, tempy] = 256

			# add slope to y because x always changes by 1
			y += Slope

	LineImage.save("Lines/" + str(p) + ".png")


TextImage.save("lines.png")