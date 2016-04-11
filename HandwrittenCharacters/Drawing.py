from Tkinter import *
from PIL import Image, ImageDraw
from os import listdir

# set the globals
w = None
master = None
DrawingsPerLetter = None
QuitProgram = False

def OneDimensionalImage(Img):
	if Img.size[0] != 10 or Img.size[1] != 16:
		raise Exception('image error', 'input image was the wrong size')

	# this is the 1d array that we will fill with image values
	# values read from right to left
	ImageArray = []

	for y in range(0, Img.size[1]):
		for x in range(0, Img.size[0]):
			Pixel = Img.getpixel((x, y))

			# white has value 0 and black has value 1 
			ImageArray.append(1.0 - ((Pixel[0] + Pixel[1] + Pixel[2]) / (255 * 3.0)))

	return ImageArray

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

def LetterWidthOffset(Image):
	Size = Image.size
	RGBImage = Image.convert('RGB')
	for XIndex in range(0, Size[0]):
		Value = 0
		for YIndex in range(0, Size[1]):
			# only bother getting the red component
			Value += RGBImage.getpixel((XIndex, YIndex))[0]
		if Value - 255 * Size[1] != 0:
			return XIndex

def Quit(event):
	global QuitProgram

	QuitProgram = True

def DrawLetter(Folder, Filename):
	global Image, ImageDraw, w, master, PNGDrawing, QuitProgram
	#sets up the canvas
	master = Tk()
	w = Canvas(master)

	# make it cover the entire screen
	width, height = master.winfo_screenwidth(), master.winfo_screenheight()
	master.overrideredirect(1)
	master.geometry("%dx%d+0+0" % (width, height))

	# set the focus to the widget
	master.focus_set()

	# quit when escape is pressed
	master.bind("<Escape>", Quit)

	# create text on the canvas according to which letter shoudl be written now
	w.create_text((80, 20), text=("draw " + str(Folder) + "; 'esc' when done"))

	# create a rectangle that the user should draw in
	w.create_rectangle(5, 5, 155, 155, outline = 'Black')


	#sets up the image drawing
	PNGCanvas = Image.new("RGB", (160, 160), (255, 255, 255))
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

	# save the file
	HeightOffset = LetterHeightOffset(PNGCanvas)
	WidthOffset = LetterWidthOffset(PNGCanvas)

	# crop the canvas image
	PNGCanvas = PNGCanvas.crop((0 + WidthOffset, 0, PNGCanvas.size[0], HeightOffset))

	# create a blank, white image and past the other cropped image into it
	WhiteImage = Image.new('RGB', (100, 160), (255,255,255))
	WhiteImage.paste(PNGCanvas, (0, 160 - PNGCanvas.size[1]))
	
	# resize the image to 8x8
	WhiteImage = WhiteImage.resize((10, 16), Image.ANTIALIAS)
	
	# save it
	WhiteImage.save("Letters/" + Folder + "/" + Filename)