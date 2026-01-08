import cv2

class Camera:
    def __init__(self, device_index=0):
        self.device_index = device_index
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.device_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera with index {self.device_index}")

    def read(self):
        if self.cap is None:
            raise RuntimeError("Camera not opened. Call open() first.")

        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None
