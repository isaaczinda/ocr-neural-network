from PIL import Image, ImageDraw

def OneDimensionalImage(Image):
	# this is the 1d array that we will fill with image values
	# values read from right to left
	ReturnArray = []
	ImageArray = Image.load()

	for y in range(0, Image.size[1]):
		for x in range(0, Image.size[0]):
			Pixel = ImageArray[x, y]

			# white has value 0 and black has value 1 
			ReturnArray.append(1.0 - (Pixel / 255.0))

	return ReturnArray