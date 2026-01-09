import cv2
import numpy as np
from dearpygui import dearpygui as dpg

from vision.camera.camera import Camera
from vision.camera.camera_utils import list_cameras

MIRROR_IMAGE = True
ASPECT_RATIO=4/3
class Viewer:
    def __init__(self, width=800, height=600,  headless=False,timeout=None):
        self.cam = None
        self.headless = headless
        self.timeout = timeout
        self.width = width
        self.height = height
        self.last_size = (width, height)

        self._pending_camera_index = None

        dpg.create_context()

        with dpg.texture_registry(show=False):
            empty = np.zeros((height * width * 3,), dtype=np.float32)
            dpg.add_raw_texture(width, height, empty,
                                format=dpg.mvFormat_Float_rgb,
                                tag="video_texture")

        with dpg.window(tag="MainWindow", label="Camera Viewer"):
            dpg.add_image("video_texture", tag="video_image")

        cams = list_cameras()
        names = [f"Camera {i}" for i in cams]

        if not names:
            print("⚠️ No cameras detected.")
            names = ["No camera found"]
            self._pending_camera_index = None
            self.cam = None


        with dpg.window(tag="Overlay", pos=(20, 20)):
            dpg.add_text("Select Camera")
            dpg.add_combo(items=names, default_value=names[0],
                          tag="camera_list", width=150,
                          callback=self.request_camera_change)

        self.request_camera_change()

        if not self.headless:
            dpg.create_viewport(title="Camera Viewer", width=width, height=height)
            dpg.setup_dearpygui()
            dpg.show_viewport()


    def request_camera_change(self, sender=None, app_data=None):
        selected = dpg.get_value("camera_list")
        try:
            index = int(selected.split()[-1])
        except:
            return
        self._pending_camera_index = index


    def apply_camera_change(self):
        index = self._pending_camera_index
        if index is None:
            return

        if self.cam:
            self.cam.release()

        cam = Camera(index)
        cam.open()
        self.cam = cam

        self._pending_camera_index = None
        print(f"Camera switched to index {index}")

    def resize_everything(self, w, h):
        self.width = w
        self.height = h

        dpg.set_item_width("MainWindow", w)
        dpg.set_item_height("MainWindow", h)
        dpg.configure_item("MainWindow", autosize=False)

        if dpg.does_item_exist("video_image"):
            dpg.delete_item("video_image")

        if dpg.does_item_exist("video_texture"):
            dpg.delete_item("video_texture")

        empty = np.zeros((h * w * 3,), dtype=np.float32)

        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                w, h,
                empty,
                format=dpg.mvFormat_Float_rgb,
                tag="video_texture"
            )

        dpg.add_image("video_texture", tag="video_image", parent="MainWindow",
                    width=w, height=h)

        print(f"[Resize] texture={w}x{h}")




    def update_frame(self):
        
        if not self.headless:
            vw = dpg.get_viewport_width()
            vh = dpg.get_viewport_height()

            if (vw, vh) != self.last_size:
                self.resize_everything(vw, vh)
                self.last_size = (vw, vh)

        if self._pending_camera_index is not None:
            self.apply_camera_change()

        if not self.cam:
            return

        frame = self.cam.read()
        if frame is None:
            return
        

        if MIRROR_IMAGE:
            frame = cv2.flip(frame, 1)

        image_w = self.width
        image_h = int(self.width / ASPECT_RATIO)

        if image_h > self.height:
            image_h = self.height
            image_w = int(self.height * ASPECT_RATIO)


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (image_w,image_h))
        frame = frame.astype(np.float32) / 255.0
        
        canvas = np.zeros((self.height, self.width, 3), dtype=np.float32)
                
        x = (self.width - image_w) // 2
        y = (self.height - image_h) // 2
        canvas[y:y+image_h, x:x+image_w] = frame
        if not self.headless:
            dpg.set_value("video_texture", canvas.flatten())
        return frame


    def run(self):
        if self.headless:
            if self.timeout:
                for _ in range(max(self.timeout,1000)):
                    self.update_frame()
            else:
                while True:
                    self.update_frame()
        while dpg.is_dearpygui_running():
            self.update_frame()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()
