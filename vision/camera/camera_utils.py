import cv2


def list_cameras(max_test=10):
    available = []
    for index in range(max_test):
        try:
            cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
            if cap.isOpened():
                available.append(index)
                cap.release()
        except:
            continue
    return available
