from Tkinter import *
from PIL import Image, ImageDraw
from os import listdir
import math
import Analysis

# set the globals
QuitProgram = False
w = None
master = None
PNGDrawing = None
Width = 500
Height = 160
DifferenceConstant = 5

def Quit(event):
	global QuitProgram

	QuitProgram = True

def PaintShape(X, Y):
	global w, master, PNGDrawing

	# draw to canvas and image file
	w.create_oval(X, Y, X + 10, Y + 10, outline='black', fill='black')
	PNGDrawing.ellipse((X, Y, X + 10, Y + 10), (0, 0, 0))
	
	master.update()

def MouseClick(event):
	PaintShape(event.x, event.y)

def MouseMove(event):
	PaintShape(event.x, event.y)

def LetterHeightOffset(Image):
	Size = Image.size
	RGBImage = Image.convert('RGB')
	for YIndex in range(Size[1] - 1, -1, -1):
		Value = 0
		for XIndex in range(0, Size[0]):
			# only bother getting the red component
			Value += RGBImage.getpixel((XIndex, YIndex))[0]
		if Value - 255 * Size[0] != 0:
			return YIndex

def Combine(PixleGroupings):
	global DifferenceConstant

	# there are likely some things that can be further grouped
	for j in range(0, len(PixleGroupings)):
		for x in range(0, len(PixleGroupings)):
			for i in range(0, len(PixleGroupings[j])):
				for p in range(0, len(PixleGroupings[x])):
					if abs(PixleGroupings[j][i][0] - PixleGroupings[x][p][0]) < DifferenceConstant and abs(PixleGroupings[j][i][1] - PixleGroupings[x][p][1]) < DifferenceConstant and j != x:
						# add the groupings together
						PixleGroupings[j] += PixleGroupings[x]

						print "group", j, "and", x

						# delete the old grouping
						del PixleGroupings[x]

						# exit the loop
						return PixleGroupings
	return None

def IsolateLetters(Img):
	global DifferenceConstant

	ImageWidth = Img.size[0]
	ImageHeight = Img.size[1]

	Groups = []

	for pixleindex in range(0, len(ImageWidth)):
		if Img.getpixel((ImageHeight / 2, pixleindex)):


	print "converting to values list"

	for pointindex in range(len(Values) - 1, -1, -1):

		print pointindex, "remaining"

		Similarity = -1

		# this detects if there is a similarity between the current point and any grouping point
		for groupingindex in range(0, len(PixleGroupings)):
			for groupingpointindex in range(0, len(PixleGroupings[groupingindex])):
				if abs(Values[pointindex][0] - PixleGroupings[groupingindex][groupingpointindex][0]) < DifferenceConstant and abs(Values[pointindex][1] - PixleGroupings[groupingindex][groupingpointindex][1]) < DifferenceConstant:
					# add to whatever grouping worked
					Similarity = groupingindex

		if Similarity == -1:
			PixleGroupings.append([Values[pointindex]])
		else:
			PixleGroupings[Similarity].append(Values[pointindex])

		# delete the value from the Values list
		del Values[pointindex]


	print "starting to combine"

	# iterate until there were no changes made
	Result = PixleGroupings

	while Result != None:
		PixleGroupings = Result
		Result = Combine(PixleGroupings)

	print "fully combined"

	return PixleGroupings

#sets up the canvas
master = Tk()
w = Canvas(master, width=Width, height=Height)

# set the focus to the widget
master.focus_set()

# quit when escape is pressed
master.bind("<Escape>", Quit)

#sets up the image drawing
PNGCanvas = Image.new("RGB", (Width, Height), (255, 255, 255))
PNGDrawing = ImageDraw.Draw(PNGCanvas)

# bind the mouse events
master.bind('<B1-Motion>', MouseMove)
master.bind('<Button-1>', MouseClick)

# get the canvas ready
w.pack()

# while escape has not been pressed
while QuitProgram == False:
	master.update()

# reset quit program variable to False
QuitProgram = False

# we will eventually store the characters in here
Characters = []

for Points in IsolateLetters(PNGCanvas):
	# start with these odd values so that the first comparison goes through
	BoundingBox = [1000, 1000, 0, 0]

	# size the boxes
	for Point in Points:
		if Point[0] < BoundingBox[0]:
			BoundingBox[0] = Point[0]
		if Point[1] < BoundingBox[1]:
			BoundingBox[1] = Point[1]
		if Point[0] > BoundingBox[2]:
			BoundingBox[2] = Point[0]
		if Point[1] > BoundingBox[3]:
			BoundingBox[3] = Point[1]

	BrushWidth = 10

	ImageWidth = BoundingBox[2] - BoundingBox[0] + BrushWidth
	ImageHeight = BoundingBox[3] - BoundingBox[1] + BrushWidth

	# create the new image canvas
	PNGCanvas = Image.new("RGB", (ImageWidth, ImageHeight), (255, 255, 255))
	PNGDrawing = ImageDraw.Draw(PNGCanvas)

	# draw onto the image for each point
	for Point in Points:
		# normalize the points
		X = Point[0] - BoundingBox[0]
		Y = Point[1] - BoundingBox[1]
		PNGDrawing.ellipse((X, Y, X + BrushWidth, Y + BrushWidth), (0, 0, 0))

	Characters.append(PNGCanvas)

for index in range(0, len(Characters)):
	# create a blank, white image and past the other cropped image into it
	WhiteImage = Image.new('RGB', (100, 160), (255,255,255))

	# paste the character onto the white image
	WhiteImage.paste(Characters[index], (0, 160 - Characters[index].size[1]))

	WhiteImage.save("Output/" + str(index) + "test.png")

	# resize the image to 8x8
	WhiteImage = WhiteImage.resize((10, 16), Image.ANTIALIAS)

	WhiteImage.save("Output/" + str(index) + ".png")

	# save it
	print Analysis.Rankings(WhiteImage, "FullCharacterRecognition")[0]
	