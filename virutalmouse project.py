import cv2
import numpy as np
import HandTrackingModule as ht
import time
import pyautogui

wcam, hcam=1080,480
frameR=100
smoothening = 1
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
plocx,plocy=0,0
clocx,clocy=0,0
detector=ht.handDetector(maxHands=1)
wscr,hscr=pyautogui.size()
#print(wscr,hscr)
while True:
    #1.Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox =detector.findPosition(img)


    #2.Get the tip of the index and middle fingers
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        #print(x1,y1,x2,y2)
        #3.check which fingers are up
        fingers=detector.fingersUp()
        #print(fingers)
        #cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255,), 2)
        #4.only index finger: moving mode
        if fingers[1]==1 and fingers[2]==0:

        #5.convert coordinates

            x3=np.interp(x1,(frameR,wcam-frameR),(0,wscr))
            y3=np.interp(y1,(frameR,hcam-frameR),(0,hscr))

        #6.Smoothen Values
            clocx=plocx+(x3-plocx)/smoothening
            clocy=plocy+(y3-plocy)/smoothening
        #7.Move mouse
            pyautogui.moveTo(wscr-clocx,clocy)

            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocx,plocy = clocx,clocy

        #8.Both Index and middle fingers are :clicking mode
        if fingers[1]==1 and fingers[2]==1:
            # 9.Find distance between fingers
            length,img,lineInfo=detector.findDistance(8,12,img)
            print(length)
            # 10
            # .click mouse if distance is short
            if length<50:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0,255, 0), cv2.FILLED)
                pyautogui.click()


    #11.frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
               (255, 0, 0), 3)

    #12.display
    cv2.imshow("Image", img)
    cv2.waitKey(1)


