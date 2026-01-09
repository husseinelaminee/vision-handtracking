from app.app import Application
from app.renderer import Renderer
from vision.pipeline.pipeline import Pipeline
from vision.pipeline.stages.camera_source_stage import CameraSourceStage
def test_app():
    pipelines = [Pipeline([CameraSourceStage(
        mirror=True
    )])]
    app = Application(pipelines, Renderer())

    app.run()
test_app()