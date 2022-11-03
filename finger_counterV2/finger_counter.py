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

    # cam width and height  ##
    wCam = 640
    hCam = 480 

    ##  videoSource = 0 meaning webcam  ##
    videoSource = 0
    ##  Camera Handle  ##
    camera = CameraSpecs(videoSource, wCam = wCam, hCam = hCam).getCam()

    ##  Instantiating handDetector ##
    detector = handDetector(maxHands = 2) 

    ## Instantiating FPS_CALCULATOR  ##
    FPS = FPS_CALCULATOR()
    
    ##  Loading Blank Image  ##
    blank_image = loadBlankImage()

    ##  Left hand images  ##
    right_images = loadImages("right_hand")

    ##  Right hand images  ##
    left_images = loadImages("left_hand")

    ## Getting the Image size  ##
    height, width, channels = 200,200,3  #images[0].shape

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
                right_count = 0
                left_count = 0
                right_hand_not_detected = True
                left_hand_not_detected = True
                for hand,handType in zip(handData,handsType):
                    if handType=='Right' and right_hand_not_detected:
                        right_count+= RHFC(hand, handType)
                        right_hand_not_detected = False
                    if handType=='Left' and left_hand_not_detected :
                        left_count+= LHFC(hand, handType)
                        left_hand_not_detected = False
                       
                
                cv2.rectangle(img,(20, 255),(170, 425),(0, 255, 0),cv2.FILLED)
                cv2.putText(img, str(left_count + right_count), (45,375), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 25)
                if not right_hand_not_detected:
                    img[0 : height, wCam-width : wCam] = right_images[right_count]
                else:
                    img[0 : height, wCam-width : wCam] = blank_image

                if not left_hand_not_detected:
                    img[0 : height, 0 : width] = left_images[left_count]
                else:
                    img[0 : height, 0 : width] = blank_image

            else:
                img[0 : height, 0 : width] = blank_image
                img[0 : height, wCam-width : wCam] = blank_image
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