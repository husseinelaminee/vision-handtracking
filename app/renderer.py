import cv2
import numpy as np
import dearpygui.dearpygui as dpg

class Renderer:
    def __init__(self, width=800, height=600, headless=False):
        self.width = width
        self.height = height
        self.headless = headless

    def start(self):
        if self.headless:
            return

        dpg.create_context()

        empty = np.zeros((self.height * self.width * 3,), dtype=np.float32)
        with dpg.texture_registry():
            dpg.add_raw_texture(
                self.width, self.height, empty,
                tag="video_texture",
                format=dpg.mvFormat_Float_rgb
            )

        with dpg.window(tag="MainWindow", label="Viewer"):
            dpg.add_image("video_texture")

        dpg.create_viewport(
            title="Camera Viewer", width=self.width, height=self.height
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def update(self, frame):
        if self.headless or frame is None:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (self.width, self.height))
        frame_rgb = frame_rgb.astype(np.float32) / 255.0

        dpg.set_value("video_texture", frame_rgb.flatten())

    def render_frame(self):
        if not self.headless:
            dpg.render_dearpygui_frame()

    def running(self):
        return False if self.headless else dpg.is_dearpygui_running()

    def close(self):
        if not self.headless:
            dpg.destroy_context()
