import cv2
import numpy as np
import dearpygui.dearpygui as dpg

class Renderer:
    def __init__(self, width=1920, height=1080, headless=False):
        # taille fixe de la texture
        self.tex_w = width
        self.tex_h = height

        # taille du viewer dynamique
        self.win_w = width
        self.win_h = height

        self.headless = headless
        self.quit = False

    def start(self):
        if self.headless:
            return

        dpg.create_context()

        with dpg.handler_registry():
            dpg.add_key_press_handler(key=dpg.mvKey_Escape, callback=self._quit)

        # create a fixed texture
        empty = np.zeros((self.tex_h * self.tex_w * 3,), dtype=np.float32)
        with dpg.texture_registry():
            dpg.add_raw_texture(
                self.tex_w, self.tex_h, empty,
                tag="video_texture",
                format=dpg.mvFormat_Float_rgb
            )

        # window + image widget
        with dpg.window(tag="MainWindow", label="Viewer"):
            dpg.add_image("video_texture", tag="video_image")

        dpg.create_viewport(title="Camera Viewer",
                            width=self.win_w, height=self.win_h)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def update(self, frame):
        if self.headless or frame is None:
            return
        
        self.resize()

        # convert frame into fixed texture resolution
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

            # mettre la fenêtre à la taille du viewport
            dpg.set_item_width("MainWindow", self.win_w)
            dpg.set_item_height("MainWindow", self.win_h)

            # --- CALCUL LETTERBOXING ---
            tex_w = self.tex_w
            tex_h = self.tex_h

            win_ratio = self.win_w / self.win_h
            tex_ratio = tex_w / tex_h

            if win_ratio > tex_ratio:
                # fenêtre trop large → bandes verticales
                disp_h = self.win_h
                disp_w = int(disp_h * tex_ratio)
            else:
                # fenêtre trop haute → bandes horizontales
                disp_w = self.win_w
                disp_h = int(disp_w / tex_ratio)

            # offsets pour centrer l'image
            offset_x = (self.win_w - disp_w) // 2
            offset_y = (self.win_h - disp_h) // 2

            # placer l'image correctement
            dpg.set_item_pos("video_image", [offset_x, offset_y])
            dpg.set_item_width("video_image", disp_w)
            dpg.set_item_height("video_image", disp_h)

    def render_frame(self):
        if not self.headless:
            dpg.render_dearpygui_frame()

    def running(self):
        return (not self.headless) and (not self.quit) and dpg.is_dearpygui_running()

    def _quit(self):
        self.quit = True

    def close(self):
        if not self.headless:
            dpg.destroy_context()
