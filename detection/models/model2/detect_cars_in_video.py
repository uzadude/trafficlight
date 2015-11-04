# From: http://python.developermemo.com/106_23244752/
import cv2
import numpy as np
#backsub = cv2.BackgroundSubtractorMOG()
backsub = cv2.createBackgroundSubtractorMOG2()
#capture = cv2.VideoCapture('../../imgs/VID_20150916_165227.avi')
capture = cv2.VideoCapture('../../imgs/VID_20151104_114549.mp4')

best_id = 0
i = 0
if capture:
    while True:
    
        ret, frame0 = capture.read()

        frame0 = cv2.transpose(frame0)
        #print frame0.shape
        frame2 = np.array(frame0[800:1500:1,400:1080:1])

        #cv2.imshow("Track", frame2)

        if ret:
        
            fgmask = backsub.apply(frame2, None, 0.01)
            
            #_, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            _, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            try: hierarchy = hierarchy[0]
            except: hierarchy = []
            for contour, hier in zip(contours, hierarchy):
                (x, y, w, h) = cv2.boundingRect(contour)
                if w > 20 and h > 20:
                    # figure out id
                    best_id += 1
                    cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame2, str(best_id), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(best_id)        
            cv2.imshow("Track", frame2)
            cv2.imshow("background sub", fgmask)
           
            
        key = cv2.waitKey(10)
        if key == ord('q'):
                break
