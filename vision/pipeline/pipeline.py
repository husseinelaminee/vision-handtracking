from core.event.event_bus import EventBus
from core.event.subscriber import Subscriber
from vision.pipeline.state import PipelineState
from vision.pipeline.stages.stage_base import Stage

class Pipeline:
    def __init__(self, stages: list[Stage]) -> None:
        self.stages = stages
        self.state = PipelineState()
        self.events = EventBus()

    def initialize(self):
        for stage in self.stages:
            if isinstance(stage, Subscriber):
                self.events.register_subscriber(stage)
            stage.initialize()

    def process(self, frame):
        for stage in self.stages:
            frame, self.state = stage.process(frame, self.state)
        return frame
