import matplotlib.pyplot as plt
from PIL import Image
import math
import numpy
from operator import itemgetter
from os import listdir
import sys
import cv2

# add the tools folder to the path
sys.path.append("../Tools")
import Array
import Statistics

Verbose = False

if len(sys.argv) > 1:
	if sys.argv[1] == "verbose":
		Verbose = True

for p in range(0, len(listdir("Lines"))):

	# load the text image
	TextImage = Image.open("Lines/" + listdir("Lines")[p]).convert('L')
	TextImagePixels = TextImage.load()

	# do the gaussian smoothing that enables us to find the crop points
	img = cv2.imread("Lines/" + listdir("Lines")[p])

	# calculate filter and smooth sizes based on how big the image is
	YFilterSize = Statistics.RoundToOdd(len(img) / 20)
	XFilterSize = Statistics.RoundToOdd(len(img[0]) / 20)

	SmoothSize = 10

	# use the recomended standard deviation
	blur = cv2.GaussianBlur(img,(XFilterSize, YFilterSize), 0)

	Raw = Array.HorizontalArrayFromImage(Image.fromarray(img))
	Median = Array.MedianArray(Raw, SmoothSize)
	Mean = Array.MeanArray(Raw, SmoothSize)

	# calculate the crop points by finding local maxes
	CropPoints = Array.FindAllLocalMaxes(Mean)

	# add a crop point at the end and beginning
	#CropPoints.insert(0, 0)
	#CropPoints.append(TextImage.size[0] - 1)

	TempArray = []
	for i in range(0, len(Mean)):
		if i in CropPoints:
			TempArray.append(255)
		else:
			TempArray.append(150)

	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=False, sharey=False)		
	ax1.set_title("Mean")
	ax1.plot(TempArray)
	ax1.plot(Mean)

	ax2.plot(Median)
	ax2.set_title("Median")

	ax3.plot(Raw)
	ax3.plot(TempArray)
	ax3.set_title("Raw")

	ax4.imshow(img)
	ax4.set_title("Image")	

	plt.show()

	for i in range(1, len(CropPoints)):
		CroppedCharacter = TextImage.crop((CropPoints[i - 1], 0, CropPoints[i], TextImage.size[1]))
		CroppedCharacter.save("Characters/" + str(p) + "-" + str(i) + ".png")