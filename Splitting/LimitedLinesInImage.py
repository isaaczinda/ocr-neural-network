import tensorflow as tf
from PIL import Image
import numpy
import sys
import math
import random
import matplotlib.pyplot as plt

# add the tools folder to the path
sys.path.append("../Tools")
import Array

sess = tf.InteractiveSession()

MaxLines = 40

def ArrayFromNumber(Number):
  global MaxLines

  Array = [0] * MaxLines
  Array[Number] = 1

  return Array

Object = {"Images": [], "Labels": [15, 27, 13, 33, 15, 14, 21, 14, 25, 11, 5, 11]}

for i in range(0, len(Object["Labels"])):
  Object["Labels"][i] = ArrayFromNumber(Object["Labels"][i])

ImageSize = (200, 200)
# last image has 11 (Cropped11.png)

# put the data in an array
for i in range(0, len(Object["Labels"])):
  PILImage = Image.open("DownloadedImages/ProcessedImages/Cropped" + str(i) + ".png").convert('L')
  PILImage = PILImage.resize(ImageSize)
  NumpyArray = Array.VerticalArrayFromImage(PILImage)

  plt.plot(NumpyArray)
  plt.show()

  for p in range(0, len(NumpyArray)):
  	NumpyArray[p] /= 255

  Object["Images"].append(NumpyArray)

# for item in Object["Images"][0]:
# 	print item

x = tf.placeholder(tf.float32, [None, ImageSize[0]])
y_ = tf.placeholder(tf.float32, [None, MaxLines])
W = tf.Variable(tf.zeros([ImageSize[0], MaxLines]))
b = tf.Variable(tf.zeros([MaxLines]))

sess.run(tf.initialize_all_variables())

y = tf.nn.softmax(tf.matmul(x, W) + b)
cross_entropy = -tf.reduce_sum(y_*tf.log(y))

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)


for i in range(1000):
  print i

  Top = int(math.ceil(random.random() * 6))

  XObjects = Object["Images"][0:Top]
  YObjects = Object["Labels"][0:Top]

  train_step.run(feed_dict={x: XObjects, y_: YObjects})

TestXObjects = Object["Images"][6:11]
TestYObjects = Object["Labels"][6:11]

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(accuracy.eval(feed_dict={x: TestXObjects, y_: TestYObjects}))