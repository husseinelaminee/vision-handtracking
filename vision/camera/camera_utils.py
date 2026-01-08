import cv2

def list_cameras(max_test=2):
    available = []
    for index in range(max_test):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available.append(index)
            cap.release()
    return available
