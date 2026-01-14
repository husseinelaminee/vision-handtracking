from app.app import Application
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline
from core.pipeline.stages.mock_camera_stage import MockCameraStage

def test_app_headless():
    pipeline = Pipeline([
        MockCameraStage()
    ])
    app = Application(pipeline, Renderer(headless=True))
    app.initialize()
    app.run(steps=5)
