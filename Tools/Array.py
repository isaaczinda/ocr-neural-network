from PIL import Image, ImageDraw
import math
import numpy
import Statistics

def BlackAndWhite(InputImage, Threshold=0):
	InputImagePixels = InputImage.load()

	# make sure that the image is entirely black
	for x in range(0, InputImage.size[0]):
		for y in range(0, InputImage.size[1]):
			if InputImagePixels[x, y] < (255 - Threshold):
				InputImagePixels[x, y] = 0
	
	return InputImage

def CropImageAroundBlack(InputImage):
	CharacterHorizontalArray = HorizontalArrayFromImage(InputImage)
	CharacterVerticalArray = VerticalArrayFromImage(InputImage)

	YMin = 0
	YMax = 0
	XMin = 0
	XMax = 0

	# find the min and max for y
	for i in range(0, len(CharacterVerticalArray)):
		if CharacterVerticalArray[i] != 255:
			YMin = i
			break
	for i in range(InputImage.size[1] - 1, -1, -1):
		if CharacterVerticalArray[i] != 255:
			YMax = i
			break

	# find the min and max for x
	for i in range(0, len(CharacterHorizontalArray)):
		if CharacterHorizontalArray[i] != 255:
			XMin = i
			break
	for i in range(InputImage.size[0] - 1, -1, -1):
		if CharacterHorizontalArray[i] != 255:
			XMax = i
			break

	# +1's are to compensate for how crop function works
	InputImage = InputImage.crop((XMin, YMin, XMax + 1, YMax + 1))
	return InputImage

def HorizontalArrayFromImage(InputImage):
	ReturnArray = []

	# convert to black and white only
	InputImage = InputImage.convert('L')

	TextPixels = InputImage.load()

	for x in range(0, InputImage.size[0]):
		PixelSum = 0
		for y in range(0, int(InputImage.size[1])):
			PixelSum += TextPixels[x, y]

		PixelSum /= float(InputImage.size[1])
		ReturnArray.append(math.ceil(PixelSum))

	return ReturnArray

def EliminateArrayNoise(Array, SegmentSize):
	NumberOfSegments = int(math.floor(len(Array) / float(SegmentSize)))
	#SegmentSize = int(math.floor(len(Array) / float(NumberOfSegments)))
	# makes an array with all of the points in it
	Points = [[SegmentSize * SegmentNumber, Array[SegmentSize * SegmentNumber]] for SegmentNumber in range(0, NumberOfSegments)]
	# adds the last element manually because of rounding
	Points.append([len(Array) - 1, Array[len(Array) - 1]])

	ReturnArray = []

	for i in range(0, len(Points) - 1):
		Slope = float(Points[i][1] - Points[i + 1][1]) / float(Points[i][0] - Points[i + 1][0])

		y = Points[i][1]
		for x in range(Points[i][0], Points[i + 1][0]):
			# multiply by slope becasue we always change x by 1
			y += Slope
			ReturnArray.append(y)


	# add one last item beacuse it wasn't covered
	ReturnArray.append(Points[len(Points) - 1][1])

	return ReturnArray

def FindLocalMaxes(Array, NumberToFind):
	SegmentSize = len(Array) / float(NumberToFind)
	LocalMaxes = []
	for Segment in range(0, NumberToFind):
		SegmentArray = Array[int(Segment * SegmentSize):int(Segment * SegmentSize + SegmentSize - 1)]
		LocalMaxes.append(sorted(SegmentArray, reverse=True)[0])

	return LocalMaxes

def FindSlope(Array):
	NewArray = []
	for i in range(0, len(Array) - 1):
		NewArray.append(round(Array[i + 1], 3) - round(Array[i], 3))
	# add an extra element so the lengths match
	NewArray.append(round(NewArray[len(NewArray) - 1], 3))

	return NewArray

def EliminateArrayNoise(Array, SegmentSize):
	NumberOfSegments = int(math.floor(len(Array) / float(SegmentSize)))
	#SegmentSize = int(math.floor(len(Array) / float(NumberOfSegments)))
	# makes an array with all of the points in it
	Points = [[SegmentSize * SegmentNumber, Array[SegmentSize * SegmentNumber]] for SegmentNumber in range(0, NumberOfSegments)]
	# adds the last element manually because of rounding
	Points.append([len(Array) - 1, Array[len(Array) - 1]])

	ReturnArray = []

	for i in range(0, len(Points) - 1):
		Slope = float(Points[i][1] - Points[i + 1][1]) / float(Points[i][0] - Points[i + 1][0])

		y = Points[i][1]
		for x in range(Points[i][0], Points[i + 1][0]):
			# multiply by slope becasue we always change x by 1
			y += Slope
			ReturnArray.append(y)


	# add one last item beacuse it wasn't covered
	ReturnArray.append(Points[len(Points) - 1][1])

	return ReturnArray

def SmoothArray(Array, SampleSize):
	return MeanArray(Array, SampleSize)

def MeanArray(Array, SampleSize, FillerValue=255):
	if SampleSize % 2 != 0:
		raise ValueError("SampleSize must be even.")

	ReturnArray = []

	for i in range(0, len(Array)):
		ReturnArray.append(0)

		# we keep the array the same size, so sometimes the sample size will be smaller
		HalfSampleSize = int(SampleSize / 2.0)

		# +1 because of how range() works
		for p in range(-HalfSampleSize, HalfSampleSize + 1):
			if (i + p) < 0 or (i + p) >= len(Array):
				ReturnArray[i] += FillerValue / float(SampleSize) 
			else:
				ReturnArray[i] += (Array[i + p]) / float(SampleSize)

	return ReturnArray

def AverageSpacing(Array):
	Spacing = 0

	for i in range(0, len(Array) - 1):
		Spacing += (Array[i + 1] - Array[i]) / float(len(Array) - 1)

	return Spacing

def MedianArray(Array, SampleSize, FillerValue=255):
	if SampleSize % 2 != 0:
		raise ValueError("SampleSize must be even.")

	ReturnArray = []
	ValuesArray = []

	for i in range(0, len(Array)):
		ValuesArray.append([])

		# we keep the array the same size, so sometimes the sample size will be smaller
		HalfSampleSize = int(SampleSize / 2.0)

		# +1 because of how range() works
		for p in range(-HalfSampleSize, HalfSampleSize + 1):
			if (i + p) < 0 or (i + p) >= len(Array):
				ValuesArray[i].append(FillerValue)
			else:
				ValuesArray[i].append(Array[i + p])

	for Items in ValuesArray:
		ReturnArray.append(Statistics.Median(Items))	

	return ReturnArray


def VerticalArrayFromImage(InputImage, BandPercentage=1):
	ReturnArray = []

	# convert to black and white only
	InputImage = InputImage.convert('L')

	TextPixels = InputImage.load()

	for y in range(0, InputImage.size[1]):
		PixelSum = 0
		for x in range(0, int(InputImage.size[0] * BandPercentage)):
			PixelSum += TextPixels[x, y]

		PixelSum /= float(InputImage.size[0]) * BandPercentage
		ReturnArray.append(math.ceil(PixelSum))

	return ReturnArray



def FindAllLocalMaxes(Array):
	Array = FindSlope(Array)

	Return = []

	for i in range(0, len(Array) - 1):
		# one is >= other is < so its fine if it hovers around 0
		# round so that slight floating point errors can't create a fake max
		if round(Array[i], 3) >= 0 and round(Array[i + 1], 3) < 0:
			Return.append(i)

	return Return