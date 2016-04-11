from os import listdir
import sys
from PIL import Image, ImageDraw
import subprocess
import cv2

# add the tools folder to the path
sys.path.append("C:\Users\SAAS Student\Google Drive\Programming\Neural Network\Tools")
import Array

for SheetName in listdir("./Sheets"):
	try:
		# can be 'reading' or 'scanning'
		Status = "scanning"
		CropPoints = []

		print "converting", SheetName

		CharacterSheet = Image.open("Sheets/" + SheetName).convert('RGB')

		for x in range(0, CharacterSheet.size[0]):
			# get the value of a column of pixels
			PixelSum = 0

			for y in range(0, CharacterSheet.size[1]):
				PixelSum += 255 - CharacterSheet.getpixel((x, y))[2]


			Threshold = 0

			if PixelSum <= Threshold and Status == "reading":
				CropPoints.append(x)
				Status = "scanning"
			elif PixelSum > Threshold and Status == "scanning":
				CropPoints.append(x)
				Status = "reading"

		# after we've iterated, add the last letter
		CropPoints.append(CharacterSheet.size[0])

		# cycle through the crop points and pick out individual letters
		for i in range(0, len(CropPoints) - 1, 2):
			# this is an RGB file
			Letter = CharacterSheet.crop((CropPoints[i], 0, CropPoints[i + 1], CharacterSheet.size[1])).convert('RGB')
			
			Pixels = Letter.load()

			Rows = []

			# cycle through each letter and see store its sum into columns
			for y in range(Letter.size[1]):
				Rows.append(0)
				for x in range(Letter.size[0]):
					Rows[y] += Pixels[x, y][0]

			# find the last row with writing in it
			LastRow = Letter.size[1]
			for p in range(0, len(Rows)):
				if Rows[p] != 255 * Letter.size[0]:
					LastRow = p

			# find the first row with writing in it
			FirstRow = 0
			for p in range(len(Rows) - 1, -1, -1):
				if Rows[p] != 255 * Letter.size[0]:
					FirstRow = p
			
			# crop the letter
			Letter = Letter.crop((0, FirstRow, Letter.size[0], LastRow))

			# resize the letter to height 300
			ChangeHeight = 400.0 / Letter.size[1]
			Letter = Letter.resize((int(Letter.size[0] * ChangeHeight), 400), Image.ANTIALIAS)
		

			# create a new white image
			FinalImage = Image.new('L', (600, 400), 255)

			# paste the letter onto the new white canvas
			FinalImage.paste(Letter, (0, 400 - Letter.size[1]))

			# resize the image to 30x20
			FinalImage = FinalImage.resize((30, 20), Image.ANTIALIAS)

			FinalImage = Array.BlackAndWhite(FinalImage, Threshold=10)

			FolderName = listdir("./Letters")[(i / 2) % 26]

			# cycle through filenames in an attempt to find empty ones
			FileName = 0
			while str(FileName) + ".png" in listdir("./Letters/" + FolderName):
				FileName += 1

			# save that shit
			FinalImage.save("Letters/" + FolderName + "/" + str(FileName) + ".png")
	except IndexError:
		print "error parsing", SheetName, "font"