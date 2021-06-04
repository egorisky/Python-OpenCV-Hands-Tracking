import cv2
import time


class HandsConnect:

    def __init__(self, vc, pTime, cTime, tracker):
        self.vc = vc
        self.pTime = pTime
        self.cTime = cTime
        self.tracker = tracker


    def drawBox(self):
        x, y, w, h = int(self.bbox[0]),int(self.bbox[1]),int(self.bbox[2]),int(self.bbox[3])
        cv2.rectangle(self.frame, (x,y), ((x+w), (y+h)), (255,255,255),2,1)

        cv2.putText(self.frame, str('Tracking!'), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)


    def start(self):
        try:
            self.vc = cv2.VideoCapture(1)
        except:
            print("the web Camera is not enabled!")

        if self.vc.isOpened():  # try to get the first frame
            self.rval, self.frame = self.vc.read()
        else:
            self.rval = False

        self.rval, self.frame = self.vc.read()
        self.bbox = cv2.selectROI("preview", self.frame, True)
        self.tracker.init(self.frame, self.bbox)

        while True:
            #web camera
            self.rval, self.frame = self.vc.read()

            self.rval, self.bbox = self.tracker.update(self.frame)
            # print(self.bbox)
            if self.rval:
                self.drawBox()
            else:
                cv2.putText(self.frame, str('Lost!'), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
            #web camera


            #FPS
            self.cTime = time.time()
            fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(self.frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
            #FPS

            cv2.imshow("preview", self.frame)


HandsConnect_ON=HandsConnect(cv2.VideoCapture(0), 0, 0, cv2.legacy_TrackerMOSSE.create())
HandsConnect_ON.start()

# After connecting your webcam you need to activate the code
# After activating the code you must mark the object you want to track
# Then press Enter!