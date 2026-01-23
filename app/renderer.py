import cv2
import numpy as np
import dearpygui.dearpygui as dpg
import time
import threading

from core.event.publisher import Publisher
from core.event.event_type import Quit

class Renderer(Publisher):

    def __init__(self, width=1920, height=1080, headless=False):
        super().__init__()
        self.tex_w = width
        self.tex_h = height
        self.win_w = width
        self.win_h = height
        self.headless = headless
        self.quit = False
        self.latest_frame = None
        self._frame_lock = threading.Lock()
        self._last_fps_time = time.time()
        self._frames = 0
        self.fps = 0


        self._aspect_ratio = 4/3

    def set_aspect_ratio(self, mode):
        if mode == "Libre":
            self._aspect_ratio = None
        elif mode == "16:9":
            self._aspect_ratio = 16/9
        elif mode == "4:3":
            self._aspect_ratio = 4/3
        elif mode == "1:1":
            self._aspect_ratio = 1.0

    def start(self):
        if self.headless:
            return

        dpg.create_context()

        with dpg.handler_registry():
            dpg.add_key_press_handler(key=dpg.mvKey_Escape, callback=self._quit)

        empty = np.zeros((self.tex_h * self.tex_w * 3,), dtype=np.float32)
        with dpg.texture_registry():
            dpg.add_raw_texture(
                self.tex_w, self.tex_h, empty,
                tag="video_texture",
                format=dpg.mvFormat_Float_rgb
            )

        with dpg.window(tag="MainWindow", label="Viewer"):
            dpg.add_image("video_texture", tag="video_image")
        
        with dpg.window(label="Aspect Ratio", pos=(self.win_w - 220, 20), width=200):
            dpg.add_text("Select Aspect Ratio")
            dpg.add_combo(
                items=["Libre", "16:9", "4:3", "1:1"],
                default_value="4:3",
                callback=lambda s, a: self.set_aspect_ratio(a)
            )

        dpg.create_viewport(title="Camera Viewer",
                            width=self.win_w, height=self.win_h)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def update(self, frame):
        if self.headless or frame is None:
            return
        
        self.resize()

        # crop selon aspect ratio
        if self._aspect_ratio is not None:
            h, w, _ = frame.shape
            r = w / h
            if r > self._aspect_ratio:
                new_w = int(h * self._aspect_ratio)
                x = (w - new_w) // 2
                frame = frame[:, x:x+new_w]
            else:
                new_h = int(w / self._aspect_ratio)
                y = (h - new_h) // 2
                frame = frame[y:y+new_h]

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (self.tex_w, self.tex_h))
        frame_rgb = frame_rgb.astype(np.float32) / 255.0

        dpg.set_value("video_texture", frame_rgb.flatten())

    def resize(self):
        win_w = dpg.get_viewport_client_width()
        win_h = dpg.get_viewport_client_height()

        if win_w <= 0 or win_h <= 0:
            return

        if win_w != self.win_w or win_h != self.win_h:
            self.win_w = win_w
            self.win_h = win_h

            dpg.set_item_width("MainWindow", self.win_w)
            dpg.set_item_height("MainWindow", self.win_h)

            tex_w = self.tex_w
            tex_h = self.tex_h

            # ratio texture modifié si aspect forcé
            if self._aspect_ratio is not None:
                tex_ratio = self._aspect_ratio
            else:
                tex_ratio = tex_w / tex_h

            win_ratio = self.win_w / self.win_h

            if win_ratio > tex_ratio:
                disp_h = self.win_h
                disp_w = int(disp_h * tex_ratio)
            else:
                disp_w = self.win_w
                disp_h = int(disp_w / tex_ratio)

            offset_x = (self.win_w - disp_w) // 2
            offset_y = (self.win_h - disp_h) // 2

            dpg.set_item_pos("video_image", [offset_x, offset_y])
            dpg.set_item_width("video_image", disp_w)
            dpg.set_item_height("video_image", disp_h)

    def render_frame(self):
        frame = self.get_latest()
        if frame is not None:
            self.update(frame)  # keep your existing update logic

        if not self.headless:
            dpg.render_dearpygui_frame()

            self._frames += 1
            now = time.time()
            if now - self._last_fps_time >= 1.0:
                self.fps = self._frames
                self._frames = 0
                self._last_fps_time = now
                print(f"[RENDERER] {self.fps} fps")


    def update_latest(self, frame):
        with self._frame_lock:
            self.latest_frame = frame

    def get_latest(self):
        with self._frame_lock:
            return self.latest_frame

    def running(self):
        return (not self.headless) and (not self.quit) and dpg.is_dearpygui_running()

    def _quit(self):
        dpg.stop_dearpygui()
        self.event_bus.emit(Quit("User pressed on ESC"))

    def close(self):
        if not self.headless:
            dpg.destroy_context()
