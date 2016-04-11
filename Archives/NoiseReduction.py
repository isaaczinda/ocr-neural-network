from os import listdir
import sys
from PIL import Image, ImageDraw
import math


# finds the ideal threshold using math
def FindThreshold(Histogram, PixelCount):
    sum = 0;
    for i in range(0, len(Histogram)):
        sum += i * Histogram[i]

    sumB = 0
    wB = 0
    wF = 0
    mB = None
    mF = None
    max = 0.0
    between = 0.0
    threshold1 = 0.0
    threshold2 = 0.0

    for i in range(0, len(Histogram)):
        wB += Histogram[i]
        if wB == 0:
            continue
        wF = PixelCount - wB
        if wF == 0:
            break

        sumB += i * Histogram[i]
        mB = sumB / wB
        mF = (sum - sumB) / wF
        between = wB * wF * (mB - mF) * (mB - mF)

        if between >= max:
            threshold1 = i
            if between > max:
                threshold2 = i
            max = between            

    return ( threshold1 + threshold2 ) / 2.0


# cycle through all images in folder
for File in listdir("./Images"):
	Letters = Image.open("./Images/" + File).convert('L')
	LettersPixels = Letters.load()

	# create a new blank image with the same size
	Output = Image.new('L', Letters.size, 255)
	OutputPixels = Output.load()

	print "computing", File

	# this is the quadrant size
	SampleSize = 15
	
	for SampleBoxOffset in [(0, 0), (Letters.size[0] - math.floor(Letters.size[0] / SampleSize) * SampleSize, Letters.size[1] - math.floor(Letters.size[1] / SampleSize) * SampleSize)]:

		# declare the arrays for each different box location
		LocalMinimum = []
		LocalMaximum = []
		StandardDeviation = []

		for xm in range(0, int(math.floor(Letters.size[0] / SampleSize))):
			for ym in range(0, int(math.floor(Letters.size[1] / SampleSize))):
				# calculate the mean
				Mean = 0
				for x in range(0, SampleSize):
					for y in range(0, SampleSize):
						Mean += LettersPixels[xm * SampleSize + x + SampleBoxOffset[0], ym * SampleSize + y + SampleBoxOffset[1]]
				Mean /= SampleSize * SampleSize

				# calcualate the local min / max and SD
				LocalMin = 255
				LocalMax = 0
				LocalStandardDeviation = 0	

				for x in range(0, SampleSize):
					for y in range(0, SampleSize):
						Value = LettersPixels[xm * SampleSize + x + SampleBoxOffset[0], ym * SampleSize + y + SampleBoxOffset[1]]

						# set the local min / max
						if Value < LocalMin:
							LocalMin = Value
						if Value > LocalMax:
							LocalMax = Value

						# calculate SD
						LocalStandardDeviation += math.pow(Value - Mean, 2)

				# finish the SD calculation
				LocalStandardDeviation = int(math.sqrt(float(LocalStandardDeviation) / float(SampleSize * SampleSize - 1)))

				# add local data to lists
				StandardDeviation.append(LocalStandardDeviation)
				LocalMinimum.append(LocalMin)
				LocalMaximum.append(LocalMax)

		# IdealThreshold = FindThreshold(Letters.histogram(), Letters.size[0] * Letters.size[1])	

		# average the SD
		AverageStandardDeviation = 0
		for Point in StandardDeviation:
			AverageStandardDeviation += Point
		AverageStandardDeviation /= len(StandardDeviation) 

		for x in range(0, int(math.floor(Letters.size[0] / SampleSize) * SampleSize + SampleBoxOffset[0])):
			for y in range(0, int(math.floor(Letters.size[1] / SampleSize) * SampleSize + SampleBoxOffset[1])):
				# calculate the index in the array where the data for this quadrant is kept
				Index = int(math.floor((x - SampleBoxOffset[0]) / SampleSize) * math.floor(Letters.size[1] / SampleSize)) + int(math.floor((y - SampleBoxOffset[1]) / SampleSize))

				ExtremaAverage = (LocalMinimum[Index] + LocalMaximum[Index]) / 2

				Threshold = ExtremaAverage

				Difference = abs(LocalMinimum[Index] - LocalMaximum[Index])
				# print Difference
				Value = LettersPixels[x, y]

				# default color is white so ignore coloring non-text pixels
				if Value < Threshold and StandardDeviation[Index] > AverageStandardDeviation:
					if (SampleBoxOffset[0] != 0 or SampleBoxOffset[1] != 0) and OutputPixels[x, y] != 0:
						OutputPixels[x, y] = 0
					else:
						OutputPixels[x, y] = 0


	Output.save("NoiseReduction/" + File[0:(len(File) - 4)] + ".png")