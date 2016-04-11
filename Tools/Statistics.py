import math

def Median(Array):
	SortedArray = sorted(Array)
	MedianValue = None

	# if the array is odd
	if len(SortedArray) % 2 != 0:
		# use floor not ceil because all arrays start at 0
		MedianValue = SortedArray[int(math.floor(len(Array) / 2.0))]
	# if the array is even
	else:
		# MedianValue = (SortedArray[len(Array) / 2] + SortedArray[(len(Array) / 2) + 1]) / 2.0
		MedianValue = SortedArray[(len(Array) / 2) + 1]

	return MedianValue


def RoundToOdd(Number):
  Floor = int(math.floor(Number))
  Ceil = int(math.ceil(Number))

  if Floor % 2 != 0:
    return Floor
  elif Ceil % 2 != 0:
      return Ceil
  else:
    return Floor + 1

def RoundToEven(Number):
  Floor = int(math.floor(Number))
  Ceil = int(math.ceil(Number))

  if Floor % 2 == 0:
    return Floor 
  elif Ceil % 2 == 0:
      return Ceil
  else:
    return Floor + 1