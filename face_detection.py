import time
from camera import Webcam
import cv2
import mediapipe as mp
from utilities import draw_landmarks_on_image
import math


class FaceDetection:
    def __init__(self):
        self.BaseOptions = mp.tasks.BaseOptions
        self.FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.FaceLandmarker = mp.tasks.vision.FaceLandmarker
        self.FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
        self.running = True
        self.i = 0
        
        self.initialize()
        
    def initialize(self):
        self.webcam = Webcam().start()
        self.options = self.FaceLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task'),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result)
        
    def loop(self):
        with self.FaceLandmarker.create_from_options(self.options) as self.landmarker:
            while self.running:
                self.i += 1
                print(f'camera ready: {self.webcam.ready()}')
                if not self.webcam.ready():
                    continue
                self.process_camera()
                
    def process_camera(self):
        self.image = self.webcam.read()
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=self.image)
            self.landmarker.detect_async(mp_image, self.i)
            if hasattr(self, 'current_landmarks') and self.current_landmarks is not None:
                #annotated_image = draw_landmarks_on_image(self.image, self.current_landmarks)
                face_landmarks_list = self.current_landmarks.face_landmarks
                for idx in range(len(face_landmarks_list)):
                    print(f'idx!!!! {idx}')
                    face_landmarks = face_landmarks_list[idx]
                    h, w, c = self.image.shape
                    x = int(face_landmarks[1].x * w)
                    y = int(face_landmarks[1].y * h)
                    nose = self.get_point(face_landmarks[1])
                    top = self.get_point(face_landmarks[10])
                    bottom = self.get_point(face_landmarks[152]) 
                    #print(f'NOSE!!!! {face_landmarks}')
                    #nose = (int(face_landmarks[1].x))
                    #print(f'NOSE!!!! {nose}')
                    cv2.circle(self.image, top, 8, (0,0,255), -1) 
                    cv2.circle(self.image, bottom, 8, (0,0,255), -1)  
                    cv2.line(self.image, top, bottom, (0,255,0))  
                    radians = math.atan2(bottom[1] - top[1], bottom[0] - top[0])
                    degrees = math.degrees(radians)
                    degrees = round(degrees)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(self.image, 'Angulo: ' + str(degrees), (90, 110), font, 3, (0,0,0), 4)
                    
                #self.image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
            #annotated_image = draw_landmarks_on_image(self.image, result)
            #self.image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
            cv2.imshow("frame", self.image)
            k = cv2.waitKey(1) & 0xFF

    def print_result(self, result: 'FaceDetection.FaceLandmarkerResult', output_image: mp.Image, timestamp_ms: int):
        print('face landmark result: {}'.format(result))
        self.current_landmarks = result
        
    def get_point(self, landmark_point):
        h, w, c = self.image.shape
        x = int(landmark_point.x * w)
        y = int(landmark_point.y * h)
        return ((x,y))
        
            
        
face = FaceDetection().loop()

# cap = Webcam().start()
# time.sleep(2)
# while True:
#     frame = cap.read()
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()