from vision.pipeline.stages.stage_base import Stage
from vision.camera.camera_manager import CameraManager
import dearpygui.dearpygui as dpg

class CameraSourceStage(Stage):
    def __init__(self, mirror=True):
        self.manager = CameraManager(mirror=mirror)
        self.ui_ready = False

    def initialize(self):
        names = self.manager.get_camera_names()
        if names:
            self.manager.request_change(0)

    def attach_ui(self):
        if self.ui_ready:
            return
        self.ui_ready = True

        names = self.manager.get_camera_names()

        with dpg.window(label="Camera Controls", pos=(20, 60), width=200, height=100):
            dpg.add_text("Select Camera")
            dpg.add_combo(
                items=names,
                default_value=names[0] if names else "",
                callback=self._on_camera_selected,
            )

    def _on_camera_selected(self, sender, app_data, user_data):
        try:
            idx = int(app_data.split()[-1])
        except:
            return
        self.manager.request_change(idx)

    def process(self, frame, state):
        frame = self.manager.get_frame()
        state["camera_index"] = self.manager.current_index
        return frame, state
