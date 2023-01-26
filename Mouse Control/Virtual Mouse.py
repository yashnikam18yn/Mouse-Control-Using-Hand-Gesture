import cv2
import numpy as np
import time
import HandTracking as ht
import autopy
import pyautogui
####################
width=648
height=480
smoothening= 5

plocx,plocy=0,0
clocx,clocy=0,0

Wscr,hscr=autopy.screen.size()
print(Wscr,hscr)

cap=cv2.VideoCapture(0)

cap.set(3,width)
cap.set(4,height)

detector=ht.handDetector(maxHands=1)

while True:
    success, img=cap.read()
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)

    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        #print(x1,y1,x2,y2)

        fingers=detector.fingersUp()
        #print(fingers)

        #only inndex up
        if fingers[1]==1 and fingers[2]==0:
            
            x3=np.interp(x1,(0,width),(0,Wscr))
            y3=np.interp(y1,(0,height),(0,hscr))
            
            clocx=plocx+(x3-plocx)/smoothening
            clocy=plocy+(y3-plocy)/smoothening

            autopy.mouse.move(Wscr-clocx,clocy)
            cv2.circle(img,(x1,y1),15,(25,0,255),cv2.FILLED)
            plocx,plocy=clocx,clocy
        
        

        
        #both fingers are up 
        if fingers[1]==1 and fingers[2]==1:

            length,img,_ =detector.findDistance(8,12,img)
            #print(length)

            if length<20:
                cv2.circle(img,(x1,y1),15,(225,255,255),cv2.FILLED)

                pyautogui.click()
                #autopy.mouse.rightclick()
                #pyautogui.click(button='right')
        
        #three fingers are up for right click
        if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]== 0:
            
           
            cv2.circle(img,(x1,y1),15,(215,25,240),cv2.FILLED)
            pyautogui.click(button='right')
        
        if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 :
            cv2.circle(img,(x1,y1),15,(22,25,24),cv2.FILLED)
            pyautogui.scroll(10)
          
        


    cv2.imshow("Image", img)
    cv2.waitKey(1) 
