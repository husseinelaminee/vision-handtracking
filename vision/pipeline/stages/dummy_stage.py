from vision.pipeline.stages.stage_base import Stage

class DummyStage(Stage):
    def __init__(self):
        self.called = False

    def process(self, frame, state):
        self.called = True
        return frame, state
