from Engine import *
import Drawing
from os import listdir
from PIL import Image, ImageDraw

def Sort(Array):
	TempArray = []

	while len(Array) > 0:
		Index = 0
		LargestItem = {"Value": 0}
		for i in range(0, len(Array)):
			if Array[i]["Value"] > LargestItem["Value"]:
				LargestItem = Array[i]
				Index = i

		# remove from the original array, add to new array
		Array.pop(Index)
		TempArray.append(LargestItem)

	return TempArray

def RankingsFromFile(Folder, Filename, NetworkName):
	return Rankings(Image.open("Letters/" + Folder + "/" + Filename), NetworkName)

def Rankings(Img, NetworkName):
	Net = LoadNetwork(NetworkName)
	Values = Net.ForwardPass(Drawing.OneDimensionalImage(Img))["Outputs"]
	Letters = listdir("./Letters")

	CompleteData = []

	for i in range(0, len(Values)):
		CompleteData.append({"Letter": Letters[i], "Value": Values[i]})

	# sort the array with the function
	CompleteData = Sort(CompleteData)

	#for i in range(0, 2):
	#	print str(CompleteData[i]["Value"]) + "%" + " chance letter " + CompleteData[i]["Letter"]

	return CompleteData