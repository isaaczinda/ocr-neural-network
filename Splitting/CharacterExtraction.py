import matplotlib.pyplot as plt
from PIL import Image
import math
import numpy
from operator import itemgetter
from os import listdir
import os
import sys
import cv2
import json
import glob

# add the tools folder to the path
sys.path.append("../Tools")
import Array
import Statistics
import ImageManipulation

# delete all characters in the Characters folder before we create new ones
print len(glob.glob('Characters/*')), "character file(s) deleted"
files = glob.glob('Characters/*')
for f in files:
    os.remove(f)

# these are all of the key values that need to be tuned
DifferenceThreshold = 55
NewMinimumThreshold = 25 # change in y that allows us to call something a 'new' point
MaxSpacing = 1.5 # if spacing more than twice line height is detected, it will be assumed a mistake and corrected

# read the line height from the file
LineHeight = 0
with open('SharedData/LineHeight.txt', 'r') as content_file:
    LineHeight = int(float(content_file.read()))

print "line height", LineHeight


for p in range(0, len(listdir("Lines"))):
	Filename = listdir("Lines")[p]
	#Filename = "14.png"

	TextImage = Image.open("Lines/" + Filename).convert('L')
	TextImagePixels = TextImage.load()

	DifferenceArray = []

	for x in range(0, TextImage.size[0]):
		ImageSlice = []
		for y in range(0, TextImage.size[1]):
			# discount everything that's completely white 
			if TextImagePixels[x, y] != 255:
				ImageSlice.append(TextImagePixels[x, y])

		Difference = 0
		SecondDifference = 0
		if len(ImageSlice) > 2:
			Difference = sorted(ImageSlice, reverse=True)[0] - sorted(ImageSlice)[0]

		DifferenceArray.append(Difference)

	# find all of the local mins
	LocalMins = Array.FindAllLocalMins(DifferenceArray)
	Slope = Array.FindSlope(DifferenceArray)

	# make sure that clusters of data are treated as one individual point
	UnfilteredCropPoints = []
	# add the first point because it automatically counts
	UnfilteredCropPoints.append(LocalMins[0])

	for i in range(1, len(LocalMins)):
		# the current crop point is set here
		CurrentCropPoint = UnfilteredCropPoints[len(UnfilteredCropPoints) - 1]

		# create an array of difference values between the two crop points
		ValueOffsetArray = DifferenceArray[CurrentCropPoint:LocalMins[i]]

		# compute the 
		TempArray = []
		for Item in ValueOffsetArray:
			TempArray.append(abs(Item - DifferenceArray[CurrentCropPoint]))

		# check to see if the current min has other mins that should also be counted
		if sorted(TempArray, reverse=True)[0] <= NewMinimumThreshold:
			pass
		else:
			UnfilteredCropPoints.append(LocalMins[i])


	# reset the crop points array
	CropPoints = []
	# shift any min from UnfilteredCropPoints to CropPoints that has a low DifferenceThreshold value
	for Min in UnfilteredCropPoints:
		if DifferenceArray[Min] < DifferenceThreshold:
			CropPoints.append(Min)

	# create a temp arrays for visualizing
	TempArray = []
	for i in range(0, len(DifferenceArray)):
		if i in CropPoints:
			TempArray.append(100)
		else:
			TempArray.append(0)

	# put the crop points into a buffer
	CropPointsBuffer = json.loads(json.dumps(CropPoints))

	# if two crop points are too far apart, search for lowest point in between
	for i in range(0, len(CropPointsBuffer) - 1):
		# if the difference is more than twice LineHeight 
		if CropPointsBuffer[i + 1] - CropPointsBuffer[i] > LineHeight * MaxSpacing:
			
			# check if there is are any local min between the two indeces
			MinsToCheck = []

			# use the crop points where similar values have already been removed 
			for LocalMin in UnfilteredCropPoints:
				if LocalMin > CropPointsBuffer[i] and LocalMin < CropPointsBuffer[i + 1]:
					# index of minimum, value of minimum
					MinsToCheck.append([LocalMin, DifferenceArray[LocalMin]])

			# find the local min from MinsToCheck that has the lowest value
			LowestValueMinIndex = sorted(MinsToCheck, key=itemgetter(1))[0][0]

			print "between", i, "and", i + 1, "checking", MinsToCheck, "chose", LowestValueMinIndex

			# add to the real crop points not the buffer
			CropPoints.append(LowestValueMinIndex)

	# sort the CropPoints so that it's smallest to largest
	CropPoints = sorted(CropPoints)

	TempArray2 = []
	for i in range(0, len(DifferenceArray)):
		if i in CropPoints:
			TempArray2.append(100)
		else:
			TempArray2.append(0)


	fig, ((ax1, ax2)) = plt.subplots(2, 1, sharex=False, sharey=False)

	ax1.plot(TempArray2, color="red")
	ax1.plot(TempArray, color="blue")
	ax1.plot(DifferenceArray, color="green")
	#ax2.plot(TempArray2)
	#ax2.plot(DifferenceArray)

	ax2.imshow(TextImage)
		

	plt.show()

	# do the actual cropping
	for i in range(1, len(CropPoints)):
		# crop based on the left-right crop points
		CroppedCharacter = TextImage.crop((CropPoints[i - 1], 0, CropPoints[i], TextImage.size[1]))

		# replace all white so that it won't be detected by edge detection
		CroppedCharacter = ImageManipulation.ReplaceColorWithMedian(CroppedCharacter)

		# get the median color before we crop and ruin a lot of the data
		# ignore all instances of the color 255 in the data
		FillColor = ImageManipulation.MedianImageColor(CroppedCharacter, Ignore=255)

		# crop the image so that only the letter is in the frame 
		CroppedCharacter = ImageManipulation.CropImageAroundEdges(CroppedCharacter)

		# create a new blank image that will serve as the background
		# set the blank image background to the median color of the character 
		BlankImage = Image.new('L', (LineHeight, LineHeight), FillColor)

		# paste the character in the center of the blank image
		XOffset = int(BlankImage.size[0] / 2.0 - CroppedCharacter.size[0] / 2.0)
		YOffset = int(BlankImage.size[1] / 2.0 - CroppedCharacter.size[1] / 2.0)
		BlankImage.paste(CroppedCharacter, (XOffset, YOffset))
		
		# resize the image so that the network can take it
		BlankImage = BlankImage.resize((32, 32), Image.ANTIALIAS)

		# save
		BlankImage.save("Characters/" + str(p) + "-" + str(i) + ".png")

	break