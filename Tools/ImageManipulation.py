from PIL import Image, ImageDraw
import math
import numpy
import Statistics
import cv2
import Array
import Statistics
import json

# only works for cv2 images
def InvertColor(InputImage):
    InputImage = 255 - InputImage
    return InputImage

def BlackAndWhite(InputImage, Threshold=0):
	InputImagePixels = InputImage.load()

	# make sure that the image is entirely black
	for x in range(0, InputImage.size[0]):
		for y in range(0, InputImage.size[1]):
			if InputImagePixels[x, y] < (255 - Threshold):
				InputImagePixels[x, y] = 0
	
	return InputImage

def PILToCV2(InputImage):
	# convert the input image to RGB
	InputImage = InputImage.convert('RGB')
	OpenCVImage = cv2.cvtColor(numpy.array(InputImage), cv2.COLOR_RGB2BGR)
	return OpenCVImage

def MedianImageColor(InputImage, Ignore=None):
	InputImage = InputImage.convert('L')
	InputImagePixels = InputImage.load()

	# flatten the image so that we can take the median
	ColoredImage = PILToCV2(InputImage)
	GreyImage = cv2.cvtColor(ColoredImage, cv2.COLOR_BGR2GRAY)
	FlatImage = GreyImage.flatten()

	if Ignore != None:
		PrunnedImage = []
		for Item in FlatImage:
			if Item != Ignore:
				PrunnedImage.append(Item)
		return Statistics.Median(PrunnedImage)
	else:
		# take the median
		return Statistics.Median(FlatImage) 

def ReplaceColorWithMedian(InputImage, Color=255, Print=False):
	# make sure image is grey
	InputImage = InputImage.convert('L')
	InputImagePixels = InputImage.load()


	# take the median
	MedianValue = MedianImageColor(InputImage, Ignore=255)
	if Print:
		print "median", MedianValue

	for x in range(0, InputImage.size[0]):
		for y in range(0, InputImage.size[1]):
			if InputImagePixels[x, y] == Color:
				InputImagePixels[x, y] = MedianValue
		

	return InputImage


def CropImageAroundEdges(InputImage):
	# convert the input image to black
	InputImage = InputImage.convert('L')

	# extract the edges of the letters
	RawImage = PILToCV2(InputImage)
	GrayImage = cv2.cvtColor(RawImage, cv2.COLOR_BGR2GRAY)
	# convert back to a PIL image
	ImageEdges = Image.fromarray(InvertColor(cv2.Canny(GrayImage, 50, 150, apertureSize = 3)))


	CharacterHorizontalArray = Array.HorizontalArrayFromImage(ImageEdges)
	CharacterVerticalArray = Array.VerticalArrayFromImage(ImageEdges)

	YMin = 0
	YMax = 0
	XMin = 0
	XMax = 0

	# find the min and max for y
	for i in range(0, len(CharacterVerticalArray)):
		if CharacterVerticalArray[i] != 255:
			YMin = i
			break
	for i in range(ImageEdges.size[1] - 1, -1, -1):
		if CharacterVerticalArray[i] != 255:
			YMax = i
			break

	# find the min and max for x
	for i in range(0, len(CharacterHorizontalArray)):
		if CharacterHorizontalArray[i] != 255:
			XMin = i
			break
	for i in range(ImageEdges.size[0] - 1, -1, -1):
		if CharacterHorizontalArray[i] != 255:
			XMax = i
			break

	# +1's are to compensate for how crop function works
	InputImage = InputImage.crop((XMin, YMin, XMax + 1, YMax + 1))
	return InputImage