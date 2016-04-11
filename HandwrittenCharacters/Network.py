from Engine import *
import Drawing
import json
from os import listdir
from PIL import Image, ImageDraw

# sets up the timing stuff
PreviousTime = 0

def TimeCheck():
	global PreviousTime
	Time = time.time()

	if PreviousTime != 0:
		print "time", (Time - PreviousTime) * 1000  

	PreviousTime = Time

SamplesPerLetter = 0

# find the max number of samples per one letter
for Character in listdir("./Letters"):
	Samples = len(listdir("./Letters/" + Character))
	if Samples > SamplesPerLetter:
		SamplesPerLetter = Samples

print "choosing", SamplesPerLetter, "samples per character"

# declare the global arays that will store the data
CharacterData = []

# import image files from folders
for CharacterIndex in range(0, len(listdir("./Letters"))):
	Character = listdir("./Letters")[CharacterIndex] 	

	for i in range(0, SamplesPerLetter):

		# makes sure the count doesn't exceed 30
		NumberOfSamples = len(listdir("./Letters/" + Character)) 
		File = listdir("./Letters/" + Character)[i % NumberOfSamples]

		# set the array to the number of characters
		Array = [0 for i in range(len(listdir("./Letters")))]
		# set the approptiate character index to 1
		Array[CharacterIndex] = 1

		# actually append the array to the master
		CharacterData.append([File, Array, Drawing.OneDimensionalImage(Image.open("Letters/" + Character + "/" + File))])

# add the blank character data
# do it  the same number of times as the other samples
for x in range(0, len(listdir("./Letters/a"))):
	CharacterData.append([" ", [0 for i in range(len(listdir("./Letters")))], [0 for i in range(0, 8*8)]])

# this sets up the network for 16x16 images
# this line creates a new network
# Net = NeuralNet(16*10, 20, len(listdir("./Letters")))

# this line loads an old one
Net = LoadNetwork("FullCharacterRecognition")

PreviousError = 1000
Error = 1000

NumberOfLetters = len(listdir("./Letters"))
TargetError = len(CharacterData) * NumberOfLetters * .01

print "Target Error", TargetError

# loop until the error becomes low
while Error > TargetError: 

	TimeCheck()

	# set the previous error
	PreviousError = Error

	Error = 0

	for index in range(0, len(CharacterData)):
		SetError = Net.ForwardPass(CharacterData[index][2], target=CharacterData[index][1])["Error"]
		Error += SetError
		Net.Backpropogate()

	Change = PreviousError - Error

	# print out the error and the change in error
	print "Error", round(Error, 3), "Change", round(Change, 3), "Bias"
	TimeCheck()


print "VALID SOLUTION REACHED: Error = ", Error
print "REVEL IN THE GLORY"

StoreNetwork("FullCharacterRecognition", Net)