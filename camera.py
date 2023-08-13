from threading import Thread
import cv2
    
class Webcam:
    def __init__(self):
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        print("Init done!")

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        print("start done!")
        t.start()
        return self

    def update(self):
        print("capture entry", self.stream)
        if self.stream is None:
            self.stream = cv2.VideoCapture(0, cv2.CAP_V4L2)
            self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            print("capture entry", self.stream)
        print("salio if")
        while True:
            print("before read", self.stopped)
            if self.stopped:
                return
            (result, image) = self.stream.read()
            #print(f'result {result} image {image} read')
            if not result:
                self.stop()
                return
            self.lastFrame = image
                
    def read(self):
        return self.lastFrame

    def stop(self):
        self.stopped = True

    def width(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH )

    def height(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT )
    
    def ready(self):
        return self.lastFrame is not None