from core.event.event_bus import EventBus
from core.event.subscriber import Subscriber
from core.pipeline.state import PipelineState
from core.pipeline.stages.stage_base import Stage

class Pipeline:
    def __init__(self, stages: list[Stage]) -> None:
        self.stages = stages
        self.state = PipelineState()

    def initialize(self):
        for stage in self.stages:
            stage.initialize()

    def process(self, frame=None):
        for stage in self.stages:
            frame = stage.process(frame, self.state)
        return frame
