import Tkinter
import tkFileDialog
import os
from PIL import Image, ImageTk
import math
import time
from operator import itemgetter
import sys
import ImageProcessing
import cv2

# add the tools folder to the path
sys.path.append("../Tools")
import Array

# use the filename Cropped.png unless something is specificed in the first argument
Filename = "Cropped"
FilenameIndex = 0

while (Filename + str(FilenameIndex) + ".png") in os.listdir("Processed"):
	FilenameIndex += 1

FullFilename = Filename + str(FilenameIndex) + ".png"

root = Tkinter.Tk()

# radius of the circle that is drawn
Radius = 5

def CreateCircle(canvas, Position):
	global Radius, Positions
	canvas.create_oval(Position[0]-1, Position[1]-1, Position[0]+1, Position[1]+1, fill="green", tags=("circle"))
	Positions.append([Position[0], Position[1]])
	return canvas.create_oval(Position[0]-Radius, Position[1]-Radius, Position[0]+Radius, Position[1]+Radius, tags=("circle"))

print "Select your image through the file explorer."

# open an file browsing dialogue
currdir = os.getcwd()
ImagePath = tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Select an Image File.')

# the unprocessed image is the original
# put it in greyscale
UnprocessedImage = Image.fromarray(cv2.imread(ImagePath)).convert('L')
UnprocessedImagePixels = UnprocessedImage.load()

# save image which has outlines of letter, which automatically converts it to greyscale
ImageProcessing.Outlines(cv2.imread(ImagePath), "Processed/" + FullFilename)

OriginalImage = Image.open("Processed/" + FullFilename)
OriginalImagePixels = OriginalImage.load()

# resize the image so that the height is 400
Multiplier = 600.0 / OriginalImage.size[1] 
TextImage = OriginalImage.resize((int(OriginalImage.size[0] * Multiplier), int(OriginalImage.size[1] * Multiplier)), Image.ANTIALIAS)
TextImagePixels = TextImage.load()

# set the canvas size to match the image
canvas = Tkinter.Canvas(root, width=TextImage.size[0], height=TextImage.size[1])
# draw the image to the canvas
photo = ImageTk.PhotoImage(TextImage)
canvas.create_image(0, 0, image=photo, anchor="nw")

# declare some globals
Circles = []
Positions = []

print "Click at the top left corner of the text."

def CropImage():
	global Positions, OriginalImagePixels, OriginalImage, Multiplier, root, UnprocessedImagePixels

	# multiply all of the positions by the scale that we used to resize the image
	for i in range(0, len(Positions)):
		for p in [0, 1]:
			Positions[i][p] = math.floor(Positions[i][p] / Multiplier)

	# create a new image of the proper size
	PartiallyCroppedImage = Image.new('L', OriginalImage.size, 255)
	PartiallyCroppedImagePixels = PartiallyCroppedImage.load()

	CroppedImage = Image.new('L', OriginalImage.size, 255)
	CroppedImagePixels = CroppedImage.load()

	def YBounding():
		SlopeOne = (Positions[0][1] - Positions[1][1]) / (Positions[0][0] - Positions[1][0])
		YIntOne = Positions[0][1] - Positions[0][0] * SlopeOne

		SlopeTwo = (Positions[2][1] - Positions[3][1]) / (Positions[2][0] - Positions[3][0])
		YIntTwo = Positions[3][1] - Positions[3][0] * SlopeTwo

		XLower = sorted(Positions, key = itemgetter(0))[0][0]
		XUpper = sorted(Positions, key = itemgetter(0), reverse = True)[0][0]

		for x in range(int(XLower), int(XUpper)):
			YLower = SlopeOne * x + YIntOne
			YUpper = SlopeTwo * x + YIntTwo

			for y in range(int(YLower), int(YUpper)):
				PartiallyCroppedImagePixels[x, y] = UnprocessedImagePixels[x, y]

	def XBounding():
		# initialize all of the varaibles
		SlopeOne, SlopeTwo, YIntOne, YIntTwo, XUpper, XLower = 0, 0, 0, 0, 0, 0
		OneVertical, TwoVertical = False, False

		# if the slope is undefined, bound differently
		try:
			SlopeOne = (Positions[1][1] - Positions[2][1]) / (Positions[1][0] - Positions[2][0])
			YIntOne = Positions[1][1] - Positions[1][0] * SlopeOne
		except ZeroDivisionError:
			OneVertical = True

		try:
			SlopeTwo = (Positions[0][1] - Positions[3][1]) / (Positions[0][0] - Positions[3][0])
			YIntTwo = Positions[3][1] - Positions[3][0] * SlopeTwo
		except ZeroDivisionError:
			TwoVertical = True

		YLower = sorted(Positions, key = itemgetter(1))[0][1]
		YUpper = sorted(Positions, key = itemgetter(1), reverse = True)[0][1]

		for y in range(int(YLower), int(YUpper)):
			# if the special vertical bound is enabled
			if OneVertical:
				XUpper = Positions[1][0]
			else:
				XUpper  = (y - YIntOne) / SlopeOne

			# if the special vertical bound is enabled
			if TwoVertical:
				XLower = Positions[0][0]
			else:
				XLower = (y - YIntTwo) / SlopeTwo

			for x in range(int(XLower), int(XUpper)):
				CroppedImagePixels[x, y] = PartiallyCroppedImagePixels[x, y]

	print Positions

	# these need to happen in this order
	YBounding()
	XBounding()

	# crop the image so that there isn't extra white space
	CroppedImage = Array.CropImageAroundBlack(CroppedImage)
	
	CroppedImage.save("Processed/" + FullFilename)

	print "Image successfully cropped and saved."

	root.destroy()


def MouseClick(event):
	global canvas, root

	Circles.append(CreateCircle(canvas, (event.x, event.y)))

	if len(Circles) == 1:
		print "Click at the top right corner of	 the text."
	elif len(Circles) == 2:
		print "Click at the bottom right corner of the text."
	elif len(Circles) == 3:
		print "Click at the bottom left corner of the text."
	if len(Circles) == 4:
		# crop and save the image
		CropImage()



# bind the mouse click to the function
root.bind('<Button-1>', MouseClick)

canvas.pack()
root.mainloop()