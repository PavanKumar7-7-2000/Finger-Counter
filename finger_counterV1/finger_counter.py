import os
import cv2
import mediapipe as mp
from load_images import loadImages
from camera_specs import CameraSpecs
from hand_tracking import handDetector
from load_images import loadBlankImage
from  fps_calculator import FPS_CALCULATOR
from left_hand import LeftHandFingerCount as LHFC
from right_hand import RightHandFingerCount as RHFC



def main():
    ##  Camera Handle  ##
    camera = CameraSpecs().getCam()

    ##  Instantiating handDetector ##
    detector = handDetector(maxHands = 1) 

    ## Instantiating FPS_CALCULATOR  ##
    FPS = FPS_CALCULATOR()
    
    ##  Loading Blank Image  ##
    blank_image = loadBlankImage()

    ## Image List of 0-5 images ##
    images = loadImages()

    ## Getting the Image size  ##
    height, width, channels = images[0].shape

    while True:

        ##  Read frames fron the camera  ##
        success, img = camera.read()

        ##  If  reading frame successfully  ##
        if success :    
            
            ##  finding landmarks  ##
            detector.findHands(img)

            ## drawing connections  ##
            img = detector.drawHands(img)

            ##  Finding Position  of the landmarks on the screen  ##
            handData = detector.findPostion(img)
            
            ##  finding type of hands  ##
            handsType = detector.findType()

            if len(handData) > 0:
                ##  Count of fingers  ##
                count = 0
                
                for hand,handType in zip(handData,handsType):
                    if handType=='Right':
                        count+= RHFC(hand, handType)
                    if handType=='Left':
                        count+= LHFC(hand, handType)
                       
                
                cv2.rectangle(img,(20, 255),(170, 425),(0, 255, 0),cv2.FILLED)
                cv2.putText(img, str(count), (45, 400), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)

                img[0 : height, 0 : width] = images[count%6]

            else:
                img[0 : height, 0 : width] = blank_image
                cv2.rectangle(img,(20, 225),(170, 425),(0, 0, 255),cv2.FILLED)

            ##  Calculate FPS  ##
            fps = FPS.calculate()

            ##  Put fps on the image  ##
            cv2.putText(img, "FPS:" + str(int(fps)), (450,40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

            ##   Display the result  ##
            cv2.imshow("image",img)

        ##  Break out of the loop when 'q' if pressed  ##
        if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q') :
            break 

    camera.release()


if __name__ == "__main__" :
    main()