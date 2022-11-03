import cv2
import mediapipe as mp


class handDetector():
    def __init__(self,static_image_mode = False ,maxHands = 2, model_complexity=1, detectionCon = 0.5 ,trackCon = 0.5):

        self.static_image_mode = static_image_mode
        self.maxHands = maxHands
        self.model_complexity=model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        ##  File Object for hands  ##
        self.mpHands = mp.solutions.hands

        ##  Object to the Hand class  ##
        self.handObject = self.mpHands.Hands(
                                        self.static_image_mode,
                                        self.maxHands,
                                        self.model_complexity,
                                        self.detectionCon,
                                        self.trackCon)

        ##  File Object for drawing_utils  ##
        self.mpDraw = mp.solutions.drawing_utils

        ##  sets landmarks color and other specs##
        self.landmark_drawing_spec = self.mpDraw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)

        ##  sets connections color and other specs ##
        self.connections_drawing_spec = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
    

    def findHands(self, img):

        ##  Convert the color of image to RGB  ##
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        ##  Get the Land Marks  ##
        self.results = self.handObject.process(imgRGB)


    
    def drawHands(self, img, draw = True):
        
        ##  If results !== None  means hands detected  ##
        if self.results.multi_hand_landmarks:

            ##  results.multi_hand_landmarks is a list of hands each hand in  is a list of landmarks that contains 21 landmarks  ##
            for hand in self.results.multi_hand_landmarks:

                ##  draw  ##
                if draw:

                    ##  draw landmarks and connect lines  ##
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS, self.landmark_drawing_spec, self.connections_drawing_spec)  
        
        return img

    def findPostion(self, img): 

        ##  landmark List  ##
        myHands = []

        ## setting image dimensions  ##
        height, width, channels = img.shape

        ##  If results !== None  means hands detected  ##
        if self.results.multi_hand_landmarks:

            ##  multi_hand landmarks contains all the hands in the image  ##
            for handLandMarks in self.results.multi_hand_landmarks:

                ##  Holds landmarks for each hand temporarily  ##
                myHand = []

                ##  looping through hands all hands one at a time  ##
                for landMark in handLandMarks.landmark:

                    ## convert ratios into pixels  ##
                    xCordinate, yCordinate =  int(landMark.x * width), int(landMark.y * height)

                    ## appending the 21 landmarks x, y coordinates  ##
                    myHand.append([xCordinate, yCordinate])

                ##  appending myHand to myHands  ##
                myHands.append(myHand)

        return myHands

    def findType(self):

        ## list of handTypes  ##
        handsType = []

        ##  If results !== None  means hands detected  ##
        if self.results.multi_hand_landmarks:

            ## Checking Hand Type Left or Right  ##
            for hand in self.results.multi_handedness:
                
                handType = hand.classification[0].label
                handsType.append(handType)

        return handsType

