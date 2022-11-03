import cv2

class CameraSpecs():

    def __init__(self, videoSource = 0, wCam = 640, hCam = 480):

        self.setCamWidth(wCam)
        self.setCamHeight(hCam)
        self.setCam(videoSource)
        
    def setCamWidth(self, wCam):
        self.wCam = wCam
        
    def setCamHeight(self, hCam):
        self.hCam = hCam

    def getCamWidth(self):
        return self.wCam

    def getCamHeight(self):
        return self.hCam
    
    def setCam(self, videoSource):
        self.cap = cv2.VideoCapture(videoSource)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)

    def getCam(self):
        return self.cap
