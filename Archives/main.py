import math
import random

#contants
learningrate = 1

###THESE ARE THE STARTING VALUES
#biases
b1=0
b2=0

#weights
w1=1
w2=1
w3=1
w4=1
w5=1
w6=1
w7=1
w8=1

#declare total error for the while loop
etotal = 1

#inputs
i1=.05
i2=.1

#target outputs
targeto1=.01
targeto2=.99

while etotal > .001:
	# CHOOSE THE INPUT

	### FORWARD PASS
	h1net=w1*i1 + w2*i2 + b1
	h2net=w3*i1 + w4*i2 + b1

	h1out=1/(1+math.pow(math.e, -h1net))
	h2out=1/(1+math.pow(math.e, -h2net))

	o1net=w5*h1out + w6*h2out + b2
	o2net=w7*h1out + w8*h2out + b2

	o1out=1/(1+math.pow(math.e, -o1net))
	o2out=1/(1+math.pow(math.e, -o2net))

	eo1=.5*math.pow(targeto1-o1out, 2)
	eo2=.5*math.pow(targeto2-o2out, 2)
	etotal=eo1+eo2

	### BACKPROPAGATE

	#backpropogate w5
	etotal_outo1 = -(targeto1 - o1out)
	outo1_neto1 = o1out * (1 - o1out)
	neto1_w5 = h1out
	etotal_w5 = etotal_outo1 * outo1_neto1 * neto1_w5

	#backpropogate w6
	neto1_w6 = h2out
	etotal_w6 = etotal_outo1 * outo1_neto1 * neto1_w6

	#backpropogate w8
	etotal_outo2 = -(targeto2 - o2out)
	outo2_neto2 = o2out * (1 - o2out)
	neto2_w8 = h2out
	etotal_w8 = etotal_outo2 * outo2_neto2 * neto2_w8

	#backpropogate w7
	neto2_w7 = h1out
	etotal_w7 = etotal_outo2 * outo2_neto2 * neto2_w7

	outh1_neth1 = h1out * (1 - h1out)
	outh2_neth2 = h2out * (1 - h2out)

	etotal_w1 = ((etotal_outo1 * outo1_neto1 * w5) + (etotal_outo2 * outo2_neto2 * w7)) * outh1_neth1 * i1
	etotal_w2 = ((etotal_outo1 * outo1_neto1 * w5) + (etotal_outo2 * outo2_neto2 * w7)) * outh1_neth1 * i2

	etotal_w3 = ((etotal_outo1 * outo1_neto1 * w6) + (etotal_outo2 * outo2_neto2 * w8)) * outh2_neth2 * i1
	etotal_w4 = ((etotal_outo1 * outo1_neto1 * w6) + (etotal_outo2 * outo2_neto2 * w8)) * outh2_neth2 * i2


	#actually change the weights now, after the hidden layer has been back propogated
	w1 -= learningrate * etotal_w1
	w2 -= learningrate * etotal_w2
	w3 -= learningrate * etotal_w3
	w4 -= learningrate * etotal_w4
	w5 -= learningrate * etotal_w5
	w6 -= learningrate * etotal_w6
	w7 -= learningrate * etotal_w7
	w8 -= learningrate * etotal_w8

	print etotal


print "Final Weights:", w1, w2, w3, w4, w5, w6, w7, w8