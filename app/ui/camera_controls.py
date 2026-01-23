import dearpygui.dearpygui as dpg
from core.event.event_type import CameraSelected
from core.event.event_bus import EventBus
from core.event.publisher import Publisher
from vision.camera.camera_manager import CameraManager

class CameraControls(Publisher):
    def __init__(self, camera_manager:CameraManager):
        super().__init__()
        self.camera_manager:CameraManager = camera_manager

    def build(self):

        names = self.camera_manager.get_camera_names()
        current = self.camera_manager.current_index or -1


        with dpg.window(label="Camera Controls", pos=(20, 60), width=200):
            dpg.add_text("Select Camera")
            dpg.add_combo(
                items=names,
                default_value=names[current],
                callback=lambda s, a: self.event_bus.emit(CameraSelected(self.camera_manager.list_indices_once()[names.index(a)])),
            )
        self.event_bus.emit(CameraSelected(current))