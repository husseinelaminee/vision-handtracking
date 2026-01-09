from vision.pipeline.stages.stage_base import Stage

class IdentityStage(Stage):
    def process(self, frame, state):
        return frame, state
