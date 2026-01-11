from vision.pipeline.stages.stage_base import Stage
from vision.pipeline.state import PipelineState

class Pipeline:
    def __init__(self, stages:list[Stage]):
        self.stages:list[Stage] = stages
        self.state = PipelineState()

    def initialize(self):
        for stage in self.stages:
            stage.initialize()

    def process(self, frame):
        for stage in self.stages:
            frame, self.state = stage.process(frame, self.state)
            if frame is None:
                return None, self.state
        return frame

    def attach_ui(self):
        for stage in self.stages:
            stage.attach_ui()

    def dispose(self):
        for stage in self.stages:
            stage.dispose()
