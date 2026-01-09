from vision.pipeline.stages.stage_base import Stage

class Pipeline:
    def __init__(self, stages:list[Stage]):
        self.stages:list[Stage] = stages

    def initialize(self):
        for stage in self.stages:
            stage.initialize()

    def process(self, frame, state):
        for stage in self.stages:
            frame, state = stage.process(frame, state)
            if frame is None:
                return None, state
        return frame, state

    def attach_ui(self):
        for stage in self.stages:
            stage.attach_ui()

    def dispose(self):
        for stage in self.stages:
            stage.dispose()
