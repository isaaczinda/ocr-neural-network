import math
import random
import time
import json

def StoreNetwork(Filename, Network):
	StoragObject = {}

	# set the network dimensions
	StoragObject["Dimensions"] = {"InputNodes": Network.InputNumber, "HiddenNodes": Network.HiddenNumber, "OutputNodes": Network.OutputNumber}

	# set the biases
	StoragObject["OutputBias"] = Network.OutputBias
	StoragObject["HiddenBias"] = Network.HiddenBias

	# initialize blank arrays
	StoragObject["InputWeights"] = []
	StoragObject["HiddenWeights"] = []

	# conver the dictionaries to arrays and then store them, which can be stored with JSON
	for Key in Network.InputWeights:
		StoragObject["InputWeights"].append([Key, Network.InputWeights[Key]])
	for Key in Network.HiddenWeights:
		StoragObject["HiddenWeights"].append([Key, Network.HiddenWeights[Key]])

	# convert to string
	ObjectString = json.dumps(StoragObject)

	#write to disk
	with open('Data/' + Filename + '.json', 'w') as datafile:
		datafile.write(ObjectString)

def LoadNetwork(Filename):
	ObjectString = open('Data/' + Filename + '.json', 'r').read()
	StorageObject = json.loads(ObjectString)

	# create a neural net object
	Network = NeuralNet(StorageObject["Dimensions"]["InputNodes"], StorageObject["Dimensions"]["HiddenNodes"], StorageObject["Dimensions"]["OutputNodes"])

	# set all of the network's biases
	Network.OutputBias = StorageObject["OutputBias"]
	Network.HiddenBias = StorageObject["HiddenBias"]

	# reset these weights, then set them again from stored data
	Network.InputWeights = {}
	Network.HiddenWeights = {}

	# convert the keys from arrays to tuples because JSON has stored them improperly
	for Value in StorageObject["InputWeights"]:
		Network.InputWeights[(Value[0][0], Value[0][1])] = Value[1]
	for Value in StorageObject["HiddenWeights"]:
		Network.HiddenWeights[(Value[0][0], Value[0][1])] = Value[1]

	return Network

class NeuralNet:
	# this is the training data, and is completely temporary
	Inputs = []
	Targets = []
	HiddenNets = []
	HiddenOutputs = []
	OutputNets = []
	OutputOutputs = []

	# value to initialize all of the arrays with
	InputWeights = {}
	HiddenWeights = {}

	# the higher this number, the more the network will change after each training cycle
	LearningRate = .2
	BiasLearningRate = .1

	def __init__(self, InputNumber, HiddenNumber, OutputNumber):
		self.InputNumber = InputNumber
		self.HiddenNumber = HiddenNumber
		self.OutputNumber = OutputNumber

		# network bias values
		self.OutputBias = [random.random() for i in range(OutputNumber)]
		self.HiddenBias = [random.random() for i in range(HiddenNumber)]

		# input layer weights
		for InputIndex in range(0, self.InputNumber):
			for HiddenIndex in range(0, self.HiddenNumber):
				self.InputWeights[(InputIndex, HiddenIndex)] = random.random()

		# hidden layer weights
		for OutputIndex in range(0, self.OutputNumber):
			for HiddenIndex in range(0, self.HiddenNumber):
				self.HiddenWeights[(HiddenIndex, OutputIndex)] = random.random()

	def ActivationFunction(self, X):
		Value = 1 / (1 + math.pow(math.e, -X))
		return Value

	def ForwardPass(self, InputValues, target=None):
		# the target value is not mandatory, None is passed by default
		if target != None:
			self.Targets = target

		self.Inputs = InputValues

		# initialize temporary one dimensional arrays
		self.HiddenNets = [0] * self.HiddenNumber
		self.HiddenOutputs = [0] * self.HiddenNumber
		self.OutputNets = [0] * self.OutputNumber
		self.OutputOutputs = [0] * self.OutputNumber

		# calculate the HiddenNets
		for HiddenIndex in range(0, len(self.HiddenNets)):
			for InputIndex in range(0, len(self.Inputs)):
				self.HiddenNets[HiddenIndex] += self.Inputs[InputIndex] * self.InputWeights[(InputIndex, HiddenIndex)]
			#multiply by the bias
			self.HiddenNets[HiddenIndex] += self.HiddenBias[HiddenIndex]

		# calculate the HiddenOutputs
		for HiddenIndex in range(0, len(self.HiddenNets)):
			# we use the logistic function because its easily differntiable
			self.HiddenOutputs[HiddenIndex] = self.ActivationFunction(self.HiddenNets[HiddenIndex])

		# calculate the OutputNets
		for OutputIndex in range(0, len(self.OutputNets)):
			for HiddenIndex in range(0, len(self.HiddenOutputs)):
				self.OutputNets[OutputIndex] += self.HiddenOutputs[HiddenIndex] * self.HiddenWeights[(HiddenIndex, OutputIndex)]
			#multiply by the bias
			self.OutputNets[OutputIndex] += self.OutputBias[OutputIndex]

		# calculate the Outputs
		for OutputIndex in range(0, len(self.OutputNets)):
			# we use the logistic function because its easily differntiable
			self.OutputOutputs[OutputIndex] = self.ActivationFunction(self.OutputNets[OutputIndex])


		RealError = 0

		# if there is a target, compute the error
		if target != None:
			# calculate the total error
			for OutputIndex in range(0, len(self.OutputOutputs)):
				RealError +=  abs(self.OutputOutputs[OutputIndex] - self.Targets[OutputIndex])

		# if there is no error, return 0 for error
		return {"Error": RealError, "Outputs": self.OutputOutputs}

	def Backpropogate(self):

		# BACK PROPOGATE

		# back propogate the first layer weights
		# do this first so that weight changes don't effect the second layer
		for InputIndex in range (0, len(self.Inputs)):
			for HiddenIndex in range(0, len(self.HiddenOutputs)):

				Sum = 0

				# here we do a bit of summation
				for OutputIndex in range(0, len(self.OutputOutputs)):
					etotal_output = (self.OutputOutputs[OutputIndex] - self.Targets[OutputIndex])
					outout_netout = self.OutputOutputs[OutputIndex] * (1 - self.OutputOutputs[OutputIndex])
					weight = self.HiddenWeights[(HiddenIndex, OutputIndex)]

					Sum += etotal_output * outout_netout * weight

				outhidden_nethidden = self.HiddenOutputs[HiddenIndex] * (1 - self.HiddenOutputs[HiddenIndex])

				etotal_weight = Sum * outhidden_nethidden * self.Inputs[InputIndex]

				self.InputWeights[(InputIndex, HiddenIndex)] -= etotal_weight * self.LearningRate

		# back propogate the first layer biases
		for HiddenIndex in range(0, len(self.HiddenOutputs)):
			Sum = 0

			# here we do a bit of summation
			for OutputIndex in range(0, len(self.OutputOutputs)):
				etotal_output = -(self.Targets[OutputIndex] - self.OutputOutputs[OutputIndex])
				outout_netout = self.OutputOutputs[OutputIndex] * (1 - self.OutputOutputs[OutputIndex])
				weight = self.HiddenWeights[(HiddenIndex, OutputIndex)]

				Sum += etotal_output * outout_netout * weight

			outhidden_nethidden = self.HiddenOutputs[HiddenIndex] * (1 - self.HiddenOutputs[HiddenIndex])
			etotal_weight = Sum * outhidden_nethidden

			self.HiddenBias[HiddenIndex] -= etotal_weight * self.BiasLearningRate

		# here we back propogate the second layer weights
		for OutputIndex in range(0, len(self.OutputOutputs)):
			for HiddenIndex in range(0, len(self.HiddenOutputs)):

				etotal_outoutput = -(self.Targets[OutputIndex] - self.OutputOutputs[OutputIndex])
				outo1_outputnet = self.OutputOutputs[OutputIndex] * (1 - self.OutputOutputs[OutputIndex])
				neto1_weight = self.HiddenOutputs[HiddenIndex]
				self.HiddenWeights[(HiddenIndex, OutputIndex)] -= etotal_outoutput * outo1_outputnet * neto1_weight * self.LearningRate

		# here we backpropogate the second layer bias
		for OutputIndex in range(0, len(self.OutputOutputs)):
			etotal_outoutput = -(self.Targets[OutputIndex] - self.OutputOutputs[OutputIndex])
			outo1_outputnet = self.OutputOutputs[OutputIndex] * (1 - self.OutputOutputs[OutputIndex])

			self.OutputBias[OutputIndex] -= etotal_outoutput * outo1_outputnet * self.BiasLearningRate