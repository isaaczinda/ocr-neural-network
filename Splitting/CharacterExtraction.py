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

# intentional error
# find the max and min values for each column. Use the difference between these to understand if space is white or not. also maybe use SD?
# then split big things, becuase we know roughly what the biggest letter is 

Filename = "10.png"
TextImage = Image.open("Lines/" + Filename).convert('L')
TextImagePixels = TextImage.load()

MedianArray = []
StandardDeviationArray = []
DifferenceArray = []

for x in range(0, TextImage.size[0]):
	ImageSlice = []
	for y in range(0, TextImage.size[1]):
		# discount everything that's completely white 
		if TextImagePixels[x, y] != 255:
			ImageSlice.append(TextImagePixels[x, y])
	
	print x, ImageSlice

	Difference = 0
	SecondDifference = 0
	if len(ImageSlice) > 2:
		Difference = sorted(ImageSlice, reverse=True)[0] - sorted(ImageSlice)[0]

	StandardDeviationArray.append(numpy.std(ImageSlice))
	DifferenceArray.append(Difference)



fig, ((ax1, ax2)) = plt.subplots(2, 1, sharex=False, sharey=False)	


ax1.plot(DifferenceArray)
ax2.imshow(TextImage)

plt.show()

# for p in range(0, len(listdir("Lines"))):

# 	#Filename = listdir("Lines")[p]
# 	Filename = "0.png"

# 	# load the text image
# 	TextImage = Image.open("Lines/" + Filename).convert('L')
# 	TextImagePixels = TextImage.load()

# 	# do the gaussian smoothing that enables us to find the crop points
# 	img = cv2.imread("Lines/" + Filename)

# 	# calculate filter and smooth sizes based on how big the image is
# 	YFilterSize = Statistics.RoundToOdd(len(img) / 20)
# 	XFilterSize = Statistics.RoundToOdd(len(img[0]) / 20)

# 	SmoothSize = 10

# 	Raw = Array.HorizontalArrayFromImage(Image.fromarray(img))
# 	Median = Array.MedianArray(Raw, SmoothSize)
# 	Mean = Array.MeanArray(Raw, SmoothSize)

# 	# calculate the crop points by finding local maxes
# 	CropPoints = Array.FindAllLocalMaxes(Mean)


# 	TempArray = []
# 	for i in range(0, len(Mean)):
# 		if i in CropPoints:
# 			TempArray.append(255)
# 		else:
# 			TempArray.append(150)

# 	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=False, sharey=False)		
# 	ax1.set_title("Mean")
# 	ax1.plot(TempArray)
# 	ax1.plot(Mean)

# 	ax2.plot(Median)
# 	ax2.set_title("Median")

# 	ax3.plot(Raw)
# 	ax3.plot(TempArray)
# 	ax3.set_title("Raw")

# 	ax4.imshow(img)
# 	ax4.set_title("Image")	

# 	plt.show()

# 	for i in range(1, len(CropPoints)):
# 		CroppedCharacter = TextImage.crop((CropPoints[i - 1], 0, CropPoints[i], TextImage.size[1]))
# 		CroppedCharacter.save("Characters/" + str(p) + "-" + str(i) + ".png")

# 	break