from vision.pipeline.stages.stage_base import Stage
from vision.pipeline.state import PipelineState
from vision.camera.camera_manager import CameraManager
import dearpygui.dearpygui as dpg

class CameraSourceStage(Stage):
    def __init__(self, mirror=True):
        self.manager = CameraManager(mirror=mirror)
        self.ui_ready = False

    def initialize(self):
        names = self.manager.get_camera_names()
        if names:
            # Use the last detected camera as intended by default
            self.manager.request_change(-1)


    def attach_ui(self):
        if self.ui_ready:
            return
        self.ui_ready = True

        names = self.manager.get_camera_names()
        index = 0 if self.manager.name_index is None else self.manager.name_index
        with dpg.window(label="Camera Controls", pos=(20, 60), width=200, height=100):
            dpg.add_text("Select Camera")
            dpg.add_combo(
                items=names,
                default_value=names[index] if names else "",
                callback=self._on_camera_selected,
            )

    def _on_camera_selected(self, sender, app_data, user_data):
        try:
            idx = int(app_data.split()[-1])
        except:
            return
        self.manager.request_change(idx)

    def process(self, frame, state: PipelineState):
        frame = self.manager.get_frame()
        state.camera_index = self.manager.current_index
        return frame, state
