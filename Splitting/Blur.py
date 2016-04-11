import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import sys
import math

# add the tools folder to the path
sys.path.append("../Tools")
import Array
import Statistics

# blur the image
img = cv2.imread('Processed/Cropped5.png')
YFilterSize = Statistics.RoundToOdd(len(img) / 20)
XFilterSize = Statistics.RoundToOdd(len(img[0]) / 20)

SmoothSize = Statistics.RoundToEven(len(img) / 20)

print "smooth size", SmoothSize

# use the recomended standard deviation
blur = cv2.GaussianBlur(img,(XFilterSize, YFilterSize), 0)
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=False, sharey=False)

BlurredImageArray = Array.VerticalArrayFromImage(Image.fromarray(blur), BandPercentage=.5)
MeanArray = Array.MeanArray(BlurredImageArray, SmoothSize)
MedianArray = Array.MedianArray(BlurredImageArray, SmoothSize)
MeanMedianArray = Array.MedianArray(MeanArray, SmoothSize)

ax1.plot(MeanMedianArray)
ax1.set_title("Blurred then Mean then Median")
ax2.plot(BlurredImageArray)
ax2.set_title("Blurred")
ax3.plot(MeanArray)
ax3.set_title("Blurred and Mean")
ax4.plot(Array.VerticalArrayFromImage(Image.fromarray(img), BandPercentage=.5))
ax4.set_title("unprocessed")
ax5.plot(MedianArray)
ax5.set_title("Blurred then Median")
plt.show()