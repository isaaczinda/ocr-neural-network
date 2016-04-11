from Tkinter import *
from PIL import Image, ImageDraw
from os import listdir

# set the globals
QuitProgram = False
w = None
master = None
PNGDrawing = None
Width = 500
Height = 200

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


def FindSpaces(Img):
	ImageWidth = Img.size[0]
	ImageHeight = Img.size[1]

	Values = []

	# sum the number of 
	for x in range(0, ImageWidth):
		Sum = 0
		for y in range(0, ImageHeight):
			Sum += Img.getpixel((x, y))[0]

		Values.append(Sum)


	Return = []
	Status = "Blank"

	# this is a state machine that parses where characters are
	for index in range(0, len(Values)):
		if Status == "Blank" and Values[index] < 255 * ImageHeight:
			Status = "Character"
			Return.append(index)
		elif Status == "Character" and Values[index] == 255 * ImageHeight:
			Status = "Blank"
			Return.append(index)

	return Return

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

# extract the characters from the word
Characters = []
CharacterLocations = FindSpaces(PNGCanvas)

# iterate through and add to the characters array
for i in range(0, len(CharacterLocations), 2):
	Characters.append(PNGCanvas.crop((CharacterLocations[i], 0, CharacterLocations[i + 1], PNGCanvas.size[1])))

for index in range(0, len(Characters)):
	HeightOffset = LetterHeightOffset(Characters[index])

	Characters[index].crop((0, 0, Characters[index].size[0], HeightOffset)).save(str(index) + ".png")