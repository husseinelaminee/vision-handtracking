from vision.pipeline.pipeline import Pipeline
from vision.pipeline.state import PipelineState
from vision.pipeline.stages.dummy_stage import DummyStage

def test_pipeline_runs_stages():
    stage = DummyStage()
    pipeline = Pipeline([stage])
    frame = pipeline.process("frame")
    assert stage.called is True