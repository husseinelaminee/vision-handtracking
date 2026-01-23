import cv2
import threading
import platform
from vision.camera.camera_utils import list_cameras
class CameraManager:
    def __init__(self, mirror=True):
        self.mirror = mirror
        self.cap = None
        self.current_index = None
        self.pending_index = None
        self.indices = None

        self.frame = None
        self.running = False
        self.thread = None

    def list_indices_once(self):
        if self.indices is None:
            self.indices = list_cameras()
        return self.indices

    def get_camera_names(self):
        return [f"Camera {i}" for i in self.list_indices_once()]

    def request_change(self, index):
        indices = self.list_indices_once()
        if index == -1:
            index = indices[-1]
        if index not in indices:
            print(f"[CameraManager] Invalid OS camera index: {index}")
            return
        self.pending_index = index

    def apply_change(self):
        if self.pending_index is None:
            return

        if self.cap:
            self.running = False
            # time.sleep(0.1)
            self.cap.release()

        # Open camera
        if platform.system() == "Linux":
            self.cap = cv2.VideoCapture(self.pending_index, cv2.CAP_V4L2)
        else:
            self.cap = cv2.VideoCapture(self.pending_index)


        # Force MJPEG + 30 FPS
        # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        # self.cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

        self.current_index = self.pending_index
        self.pending_index = None
        print(f"[CameraManager] switched to camera {self.current_index}")

    def _capture_loop(self):
        """Thread: lit en continu la caméra à 30 FPS."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if self.mirror:
                    frame = cv2.flip(frame, 1)
                self.frame = frame
            # else:
            #     time.sleep(0.005)

    def get_frame(self):
        self.apply_change()
        return self.frame  # retourne immédiatement la dernière frame

    def release(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
