import sys
sys.path.append("/usr/local/lib/python3.5/dist-packages")
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/Desktop/python/webapp6")
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import time
import argparse
import datetime
from tables import User
from emailsending import EmailSend

class MotionDetection(object):
    
    def __init__(self):
        self.avg = None
        self.key=None;
        self.lastUploaded = datetime.datetime.now()
        self.motionCounter = 0
        self.frame=None
        self.text="MovementDetected"
        self.period=False;
        self.detected=False;
        self.x=0
        self.y=0
        self.w=0
        self.h=0
        self.email=EmailSend()
        self.to=[]
        self.time=0
        self.fps=0
        
    def UpdateUsers(self):
        users=User.query.all()
        self.to.clear()
        for u in users:
            self.to.append(u.email)
        
            
            
    def setFrame(self,Frame):
        self.frame=Frame
        
    def setTime(self):
        self.lastUploaded = datetime.datetime.now()
        
    def detect(self):
        #print("FPS: ", 1.0 / (time.time() - self.fps))
        #self.fps=time.time()
        
        #return cv2.imencode('.jpg', self.frame)[1].tobytes()
        
        # resize the frame, convert it to grayscale, and blur it
        #frame=cv2.resize(frame, (500, 500))
        self.period= not self.period
        if self.period:
         if self.detected:
            #send email to users:
            #print("detected")
            currenttime=time.time()
            if (currenttime-self.time)>1000:
                self.time=currenttime
                self.UpdateUsers()
                cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)
                cv2.putText(self.frame, "{}".format(self.text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                img=self.frame
                
                #self.email.Send(self.to,img)
                
                print(self.to)
                return self.frame,self.detected
            
            # 
            cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)
            self.text = "MovementDetected" 
           	# draw the text and timestamp on the frame 
            cv2.putText(self.frame, "{}".format(self.text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)       
         return self.frame,self.detected
        timestamp = datetime.datetime.now()
        small = cv2.resize(self.frame, None, fx = 0.5, fy = 0.5, interpolation = cv2.INTER_LINEAR)
        
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15, 15), 0)
        
        # if the average frame is None, initialize it
        
        if self.avg is None:
         print("[INFO] starting background model...")
         self.avg=gray.copy().astype("float")
         
         return self.frame , self.detected
         
          
        
        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
      
        thresh = cv2.threshold(frameDelta,5, 255,cv2.THRESH_BINARY)[1]
        kernel = np.ones((9,9),np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)
       
        cnts = cnts[1] 
    
        # loop over the contours
        self.detected=False;
        for c in cnts:
 	# if the contour is too small, ignore it
            if cv2.contourArea(c) < 2500:
              continue
             # compute the bounding box for the contour, draw it on the frame,
             # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            
            self.x=x*2
            self.y=y*2
            self.w=w*2
            self.h=h*2
            
            cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)
            self.detected=True;
            self.text = "MovementDetected"
 
           	 # draw the text and timestamp on the frame
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv2.putText(self.frame, "{}".format(self.text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.putText(self.frame, ts, (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        
        
        return self.frame, self.detected
    
    
    
    
    
    
    
    
    
    
    
    