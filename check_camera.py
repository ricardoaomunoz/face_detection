import cv2

def check_cameras(max_range=10):
    available_cameras = []
    for index in range(max_range):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"Camera found at index: {index}")
            available_cameras.append(index)
            cap.release()
    return available_cameras

if __name__ == "__main__":
    cameras = check_cameras()
    print(f"Available cameras: {cameras}")