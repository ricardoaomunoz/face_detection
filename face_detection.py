import time
from camera import Webcam
import cv2
import mediapipe as mp
from utilities import draw_landmarks_on_image
import math

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class FaceDetection:
    def __init__(self):
        self.BaseOptions = mp.tasks.BaseOptions
        self.FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.FaceLandmarker = mp.tasks.vision.FaceLandmarker
        self.FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
        self.running = True
        self.i = 0
        '''GAME XD'''
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        pygame.init()
        '''#############'''
        
        self.initialize()
        
    def initialize(self):
        self.movement = 0
        self.webcam = Webcam().start()
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = self.start_time
        self.options = self.FaceLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task'),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.print_result)
        self.player = Player()
        
    def loop(self):
        with self.FaceLandmarker.create_from_options(self.options) as self.landmarker:
            while self.running:
                self.i += 1
                print(f'camera ready: {self.webcam.ready()}')
                if not self.webcam.ready():
                    continue
                time = pygame.time.get_ticks()
                delta_time = time - self.last_frame_time
                self.last_frame_time = time
                self.process_camera()
                self.game_loop(delta_time)
                
                
    def game_loop(self, delta_time):
        # Look at every event in the queue
        for event in pygame.event.get():
            #Did the user hit a key?
            if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    self.running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                self.running = False
                
        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
        self.player.update(self.movement, delta_time)
        
        # Fill the screen with white
        self.screen.fill((0, 0, 0))
        # Create a surface and pass in a tuple containing its length and width
        self.screen.blit(self.player.surf, self.player.rect)

        pygame.display.flip()
                            
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
                    min_degrees = 70
                    max_degrees = 110
                    degree_range = max_degrees - min_degrees
                    
                    if degrees < min_degrees: degrees = min_degrees
                    if degrees > max_degrees: degrees = max_degrees

                    self.movement = ( ((degrees-min_degrees) / degree_range) * 2) - 1
                    degrees = round(degrees)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(self.image, 'Angulo: ' + str(self.movement), (90, 110), font, 3, (0,0,0), 4)
                    
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
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        
    def update(self, movement, delta_time):
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        self.rect.move_ip(-1 * movement * delta_time, 0)
        # if pressed_keys < 0:
        #     self.rect.move_ip(-5, 0)
        # if pressed_keys > 0:
        #     self.rect.move_ip(5, 0)
            
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT
            
        
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