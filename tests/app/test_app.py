from app.app import Application
from app.renderer import Renderer
from vision.pipeline.pipeline import Pipeline
from vision.pipeline.stages.mock_camera_stage import MockCameraStage

def test_app_headless():
    pipelines = [Pipeline([MockCameraStage()])]
    app = Application(pipelines, Renderer(headless=True))

    app.run(frames=5)
