import cv2
import platform

def list_cameras(max_test=10):
    available = []
    system = platform.system()

    for index in range(max_test):
        if system == "Linux":
            cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
        else:
            cap = cv2.VideoCapture(index)

        if cap.isOpened():
            available.append(index)
            cap.release()

    return available
