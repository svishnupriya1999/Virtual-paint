import cv2
import HandTrackingModule as htm 
import numpy as np


cap =cv2.VideoCapture(0)
detector = htm.handDetector()
draw_color =(0,0,255)
img_canvas = np.zeros((720,1280,3),np.uint8)

while True:
     success,frame = cap.read()
     frame = cv2.resize(frame,(1280,720))
     frame=cv2.flip(frame,1)
     
     cv2.rectangle(frame,pt1=(23,32),pt2=(258,128),color=(0,0,255),thickness=-1)
     cv2.rectangle(frame,pt1=(267,32),pt2=(505,127),color=(255,255,0),thickness=-2)
     cv2.rectangle(frame,pt1=(516,32),pt2=(744,127),color=(255,0,0),thickness=-3)
     cv2.rectangle(frame,pt1=(758,32),pt2=(1004,127),color=(0,255,255),thickness=-4)
     cv2.rectangle(frame,pt1=(1017,32),pt2=(1259,127),color=(255,255,255),thickness=-4)

     cv2.putText(frame,text='Eraser',org=(1058,89),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=1,color=(0,0,0),thickness=3)

#find hands
     frame= detector.findHands(frame)
     lmlist=detector.findPosition(frame)
    #  print(lmlist)
     if len(lmlist)!=0:
      x1,y1=lmlist[8][1:]
      x2,y2=lmlist[12][1:]
     #  print(x1,y1)
#check if finger is up
      fingers = detector.fingersUp()
      print(fingers)
#selection mode - index and middle finger is up
      if fingers[1] and fingers[2] :
         print('selection mode')

         xp,yp = 0,0

         if y1 < 127:
            if 23 <x1 <258:
               print("red")
               draw_color = (0,0,255)
            elif 267 <x1 <505:
               print("sky blue")
               draw_color = (255,255,0)
            elif 516 <x1 <744:
               print("Blue")
               draw_color = (255,0,0)
            elif 758 <x1 <1004:
               print("Yellow")
               draw_color = (0,255,255)
            elif 1017 < x1 < 1259:
               print("Eraser")
               draw_color = (0,0,0)

         cv2.rectangle(frame,(x1,y1),(x2,y2),draw_color,cv2.FILLED)      

#drawing mode - only index is up
      if (fingers[1] and not fingers[2]):
         print('drawing mode')

         if xp == 0 and yp == 0:

            xp = x1
            yp = y1
         if draw_color==(0,0,0):
         #eraser size
          cv2.line(frame,(xp,yp),(x1,y1),color=draw_color,thickness=50)
          cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=50)
         else:
         #all other color size 
            cv2.line(frame,(xp,yp),(x1,y1),color=draw_color,thickness=10)
            cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)

         xp,yp = x1,y1
         
      img_gray= cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
      _,img_inv = cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)
      img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)

      frame= cv2.bitwise_and(frame,img_inv)
      frame = cv2.bitwise_or(frame,img_canvas)

         #to merge
      frame = cv2.addWeighted(frame,1,img_canvas,0.5,0)



     
       
     


     cv2.imshow('virtual painting',frame)
    
     if cv2.waitKey(1) & 0xFF==27:
       break
cap.release()
cv2.destroyAllWindows()
