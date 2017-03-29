import cv2
import numpy as np

#read the data from the file
with open("test.png", 'rb') as infile:
    buf = infile.read()

print(buf[-1])
print(type(buf))

#use numpy to construct an array from the bytes
x = np.fromstring(buf, dtype='uint8')

#decode the array into an image
img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)

#show it
cv2.imshow("some window", img)
cv2.waitKey(0)
