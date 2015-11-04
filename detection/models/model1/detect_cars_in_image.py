
"""

From: http://www.chioka.in/build-your-own-real-time-traffic-data-feed/

Author: Eric Chio <ckieric[at]gmail[dot]com>
Date: 2014/03/08
Project: Macau Real Time Traffic Data Feed
Website: http://www.chioka.in/

Idea:
- Loads an image sequence
- Crop the image to only areas of interest (no sea, just roads, and nearby
roads)
- Create a cascade classifier with cars3.xml
- Use cascade classifier to detect cars, tune parameters accordingly.

Note, cars3.xml do not detect motorbikes.
"""

import numpy as np
import cv2

# Loads the data as a VideoCapture format, which is really just
# an image sequence.
image_sequence = [r'../../imgs/IMG_20150816_154758_X_10.jpg']
cap = cv2.VideoCapture(image_sequence[0])

# Load our cascade classifier from cars3.xml
car_cascade = cv2.CascadeClassifier(r'cars3.xml')

# Reduce frame number of tests.
number_of_frames_to_load = len(image_sequence)
for frame_id in xrange(number_of_frames_to_load):
    ret, image = cap.read()
    
    # Crop so that only the roads remain, eliminatives the distraction.
    #image = image[120:,:-20]
    print image.shape
    image = np.array(image[1000:2000:1,800:1600:1])
    print image.shape
    
    # Use Cascade Classifier to detect cars, may have to tune the
    # parameters for less false positives.
    cars = car_cascade.detectMultiScale(image, 1.01, 10)
    for (x,y,w,h) in cars:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
    
    print 'Processing %d : cars detected : [%s]' % (frame_id, len(cars))

    cv2.imshow('frame', image)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
