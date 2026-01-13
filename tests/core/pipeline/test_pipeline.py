from core.pipeline.pipeline import Pipeline
from core.pipeline.state import PipelineState
from core.pipeline.stages.dummy_stage import DummyStage

def test_pipeline_runs_stages():
    stage = DummyStage()
    pipeline = Pipeline([stage])
    frame = pipeline.process("frame")
    assert stage.called is True