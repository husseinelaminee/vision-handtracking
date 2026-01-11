import cv2
from vision.camera.camera import Camera
from vision.camera.camera_utils import list_cameras

class CameraManager:
    def __init__(self, mirror=True):
        self.mirror = mirror
        self.camera = None
        self.current_index = None
        self.pending_index = None
        self.name_index = None

    def list_indices(self):
        return list_cameras()

    def get_camera_names(self):
        return [f"Camera {i}" for i in self.list_indices()]

    def request_change(self, index):
        if index == -1:
            index = self.list_indices()[-1]
            self.name_index = max(0,len(self.list_indices())-1)
        else:
            for index_key, index_val in enumerate(self.list_indices()):
                index_val == index
                self.name_index = index_key
        self.pending_index = index

    def apply_change(self):
        if self.pending_index is None:
            return

        if self.camera:
            self.camera.release()

        self.camera = Camera(self.pending_index)
        self.camera.open()
        self.current_index = self.pending_index
        print(f"[CameraManager] switched to camera {self.current_index}")

        self.pending_index = None

    def get_frame(self):
        self.apply_change()

        if not self.camera:
            return None

        frame = self.camera.read()
        if frame is None:
            return None

        if self.mirror:
            frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        if self.camera:
            self.camera.release()
            self.camera = None
