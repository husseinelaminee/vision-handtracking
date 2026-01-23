from core.pipeline.stages.stage_base import Stage
from core.pipeline.state import PipelineState
from vision.camera.camera_manager import CameraManager
from core.event.event_type import CameraSelected
from core.event.subscriber import Subscriber
from app.ui.camera_controls import CameraControls

class CameraSourceStage(Stage, Subscriber):
    def __init__(self, mirror: bool = True) -> None:
        super().__init__()
        self._manager = CameraManager(mirror=mirror)

    @property
    def events(self):
        return [CameraSelected]

    def handle_event(self, event: CameraSelected):
        self._manager.request_change(event.index)

    def initialize(self) -> None:
        CameraControls(self._manager).build()

    def process(self, frame, state: PipelineState):
        frame = self._manager.get_frame()
        state.camera_index = self._manager.current_index
        return frame