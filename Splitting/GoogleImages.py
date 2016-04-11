import json
import os
import time
import requests
from PIL import Image
from StringIO import StringIO
from requests.exceptions import ConnectionError


APIKey = "2272375-eb01a43a6da913d9e7120560c"
URL = "https://pixabay.com/api/?key=" + APIKey + "&q=book%20text&image_type=photo&per_page=200"

# download the image
try:
  PageJSON = requests.get(URL).content
  PageObject = json.loads(PageJSON)
  Items = PageObject["hits"]

  print Items

  #for 

except ConnectionError, e:
  print 'could not download %s' % URL



# # get the filename
# Filename = "Image"
# FilenameIndex = 0
# while (Filename + str(FilenameIndex) + ".png") in os.listdir(Folder):
#   FilenameIndex += 1
# FullFilename = Filename + str(FilenameIndex) + ".png"

# try:
#   Image.open(StringIO(image_r.content)).save(Folder + "/" + FullFilename)
#   print "saved", FullFilename
# except IOError, e:
#   # Throw away some gifs...blegh.
#   print 'could not save %s' % FullFilename

# # Example use
# URLs = ["http://ccnmtl.columbia.edu/enhanced/images/from_platos_apology.png", "http://www.techpin.com/wp-content/uploads/2010/01/cool-text.jpg", "http://2.bp.blogspot.com/_1mY5w9ZnXCs/TG0CegNAQrI/AAAAAAAABhA/u7ZEavDHpNY/s1600/text-small-animated.gif", "https://upload.wikimedia.org/wikipedia/commons/7/75/Southern_Life_in_Southern_Literature_text_page_322.jpg", "https://vllg.s3.amazonaws.com/news_posts/images/120/original/vllg_Klim_News_FGT.jpg?1377998242", "http://www.pws-ltd.com/images/articles/justified-text.gif", "https://upload.wikimedia.org/wikipedia/commons/7/75/Dan%27l_Druce,_Blacksmith_-_Illustrated_London_News,_November_18,_1876_-_text.png", "https://www.kirupa.com/flash/images/single_column_text.png"]

# for URL in URLs:
#   Download(URL, 'DownloadedImages')