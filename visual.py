import cv2
from utilities import draw_landmarks_on_image

#img = cv2.imread("image.jpg")
#cv2.imshow('Imagen', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
FaceLandmarker = mp.tasks.vision.FaceLandmarker

#create a face landmarker instance with the live strem mode
def print_result(result: vision.FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('face landmark result: {}'.format(result))
    annotated_image = draw_landmarks_on_image(imgRGB, result)
    image_result = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    cv2.imshow("frame", image_result)
    cv2.waitKey(1)
    
# STEP 2: Create an FaceLandmarker object.

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

#base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
#options = vision.FaceLandmarkerOptions(base_options=base_options,
#                                       output_face_blendshapes=True,
#                                       running_mode=vision.RunningMode.LIVE_STREAM,
#                                       output_facial_transformation_matrixes=True,
#                                       num_faces=1,
#                                       result_callback=print_result)
#detector = vision.FaceLandmarker.create_from_options(options)

# STEP 3: Load the input image in this case video.qqqqqqqqqq
i = 0
with FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    while True:
        i += 1
        ret, frame = cap.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        landmarker.detect_async(mp_image, i)
        print("i: %d", i)
    #annotated_image = draw_landmarks_on_image(imgRGB, detection_result)
    

    #cv2.imshow('frame', annotated_image)
    #landmarker.detect_async(mp_image, i)

    #if cv2.waitKey(1) == ord('q'):
     #   break
cap.release()
cv2.destroyAllWindows()

#image = mp.Image.create_from_file("image.jpg")
#mp_image = mp.Image(image_fort=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)
# STEP 4: Detect face landmarks from the input image.
#detection_result = detector.detect(image)
#detector.detect_async(mp_image, frame_timestamp_ms)
# STEP 5: Process the detection result. In this case, visualize it.
#annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
#cv2_imshow(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

#cv2.imshow('Imagen', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
#cv2.waitKey(0)
#cv2.destroyAllWindows()
