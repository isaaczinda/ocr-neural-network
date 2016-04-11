oimport Drawing
from os import listdir
import sys
import Analysis
import os

# set these globals
Filename = ""
Folder = ""

def SaveAsUnusedName():
	global Filename, Folder

	# code cycles through all of the available nubmers to create a unique filename
	Index = 0
	Filename = str(Index) + ".png"
	while Filename in listdir("./Letters/" + Folder):
		Index += 1
		Filename = str(Index) + ".png"

	# actually do the drawing
	Drawing.DrawLetter(Folder, Filename)

# if there are three arguments set the file and folder name
if len(sys.argv) == 3:
	if sys.argv[1] == "alphabet":
		DrawingsPerLetter = int(sys.argv[2])
		for Item in listdir("./Letters/"):
			for i in range(0, DrawingsPerLetter):
				Folder = Item
				SaveAsUnusedName()
	elif sys.argv[1] == "analyze":
		# actually do the drawing
		Folder = sys.argv[2]
		SaveAsUnusedName()
		# get the analytics data
		AnalysisData = Analysis.RankingsFromFile(Folder, Filename, "FullCharacterRecognition")

		for i in range(0, 3):
			print AnalysisData[i]["Value"], "letter", AnalysisData[i]["Letter"]

		if AnalysisData[0]["Letter"] == Folder:
			os.remove("Letters/" + Folder + "/" + Filename)
			print "removing reduntant sample."

	else:
		Filename = sys.argv[2]
		Folder = sys.argv[1]

		# actually do the drawing
		Drawing.DrawLetter(Folder, Filename)

# if there are two arguments set the folder and get the right filename
elif len(sys.argv) == 2:
		Folder = sys.argv[1]
		SaveAsUnusedName()
# allow the user to add more than one letter of one type at once
elif len(sys.argv) == 4:
	if sys.argv[1] == "series":
		# set the folder
		Folder = sys.argv[2]
		
		for i in range(0, int(sys.argv[3])):
			SaveAsUnusedName()

		