from vision.pipeline.pipeline import Pipeline
from vision.pipeline.stages.stage_base import Stage

class DummyStage(Stage):
    def process(self, frame, state):
        state["called"] = True
        return frame, state

def test_pipeline_runs_stages():
    pipeline = Pipeline([DummyStage()])
    frame, state = pipeline.process("frame", {})
    assert state["called"] is True
