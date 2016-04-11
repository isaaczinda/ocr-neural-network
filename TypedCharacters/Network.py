from Engine import *
import Drawing
import json
from os import listdir
from PIL import Image, ImageDraw
import sys
import atexit

# sets up the timing stuff
PreviousTime = 0

# get the network name from the command-line
NetworkName = sys.argv[1]

# set the global network variable
Net = None 

# sets the dimensions of the network 
ImageWidth = 30
ImageHeight = 20

def TimeCheck():
	global PreviousTime
	Time = time.time()

	if PreviousTime != 0:
		print "time", (Time - PreviousTime) * 1000  

	PreviousTime = Time

# on shutdown, store the network
def Shutdown():
	print "saving the network to Data/" + NetworkName + ".json"
	StoreNetwork(NetworkName, Net)

# find the max number of samples per one letter
SamplesPerLetter = 0
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

if (NetworkName + ".json") in listdir("./Data"):
	# leave off the '.json' beacuse this is handled by the function
	Net = LoadNetwork(NetworkName)
else:
	# create a new network with the given dimensions 
	Net = NeuralNet(ImageHeight * ImageWidth, 20, len(listdir("./Letters")))


PreviousError = 10000
Error = 10000

# setup the learning rate
Net.LearningRate = .1
Net.BiasLearningRate = .1

NumberOfLetters = len(listdir("./Letters"))

# set the target error to .01 for each image
TargetError = len(CharacterData) * NumberOfLetters * .02

# when the program exits, save the network
atexit.register(Shutdown)
print "shutdown function bound to program exit"

print "Starting up the network with target error ", TargetError

# loop until the error becomes low
while Error > TargetError: 
	# set the previous error
	PreviousError = Error

	Error = 0

	for index in range(0, len(CharacterData)):
		SetError = Net.ForwardPass(CharacterData[index][2], target=CharacterData[index][1])["Error"]
		Error += SetError
		Net.Backpropogate()

	Change = PreviousError - Error

	# print out the error and the change in error
	print "Error", round(Error, 3), "Change", round(Change, 3)
	TimeCheck()


print "VALID SOLUTION REACHED: Error = ", Error
print "REVEL IN THE GLORY"

StoreNetwork(NetworkName, Net)