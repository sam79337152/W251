# code just used for testing the camera 

import numpy as np
import cv2 as cv
import pickle

facealg = cv.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")

cap = cv.VideoCapture(1)

while(True):

    #read image in gray scale
    ret, frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)

    cv.imshow('frame', gray)

    #detect a face
    faces = facealg.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        
        #cut the face from the frame
        roi_gray = gray[y:y+h, x:x+w]
    
        #encode and public message
        rc,png = cv.imencode('.png', roi_gray)
        msg = roi_gray.tobytes()
    
    #quit capturing
    if cv.waitKey(1) & 0xFF == ord('q'):
        #print(type(roi_gray))
        #print(roi_gray.shape)
        #print(roi_gray[0,0])
        #print(type(roi_gray[0,0]))
        #print(roi_gray.dtype)
        
        #print("\n\n\nRAW:", roi_gray)    
        #enc = roi_gray.tobytes()
        #print("\n\n\nENC", enc)
        #dec = np.frombuffer(enc, np.uint8)
        #print("\n\n\nDEC", dec)
        #imdec = cv.imdecode(dec, 0)


        
        cv.imwrite('original.png', pickle.loads(pickle.dumps(roi_gray)))
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

