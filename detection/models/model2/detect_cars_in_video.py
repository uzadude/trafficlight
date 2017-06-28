# From: http://python.developermemo.com/106_23244752/
import cv2
import numpy as np
import datetime
#capture = cv2.VideoCapture('../../imgs/VID_20150916_165227.mp4')
capture = cv2.VideoCapture('../../imgs/VID_20151104_114549.mp4')
#capture = cv2.VideoCapture('../../imgs/VID_20151104_140110.mp4')

avg = None

def simpleBGSubtruct(frame2):
    global avg
    
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)
     
    # if the average frame is None, initialize it
    if avg is None:
        print "[INFO] starting simple background model..."
        avg = gray.copy().astype("float")
        #rawCapture.truncate(0)
        return
     
    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    
    # threshold the delta image, dilate the thresholded image to fill
    # in holes, then find contours on thresholded image
    thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 500:
            continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # draw the text and timestamp on the frame
    timestamp = datetime.datetime.now()
    #ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    #cv2.putText(frame2, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.putText(frame2, ts, (10, frame2.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
    cv2.imshow("Simple", frame2)
    #cv2.imshow("Simple mask", thresh)



#backsub = cv2.BackgroundSubtractorMOG()
backsub = cv2.createBackgroundSubtractorMOG2()
#backsub = cv2.createBackgroundSubtractorKNN()
best_id = 0

def advancedBGSubtruct(frame2):
    global best_id
    fgmask = backsub.apply(frame2, None, 0.01)
    
    #_, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try: hierarchy = hierarchy[0]
    except: hierarchy = []
    for contour, hier in zip(contours, hierarchy):
        (x, y, w, h) = cv2.boundingRect(contour)
        if w > 20 and h > 20:
            # figure out id
            #best_id += 1
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #cv2.putText(frame2, str(best_id), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    #print(best_id)        
    cv2.imshow("Advanced", frame2)
    cv2.imshow("background sub", fgmask)    
    
i = 0
if capture:
    while True:
    
        ret, frame0 = capture.read()

        #frame0 = cv2.transpose(frame0)
        #print frame0.shape
        frame2 = np.array(frame0[800:1500:1,100:800:1])
        #frame2 = frame0

        if ret:
        
            #simpleBGSubtruct(frame2.copy())
            advancedBGSubtruct(frame2.copy())
           
            
        key = cv2.waitKey(10)
        if key == ord('q'):
                break
 
