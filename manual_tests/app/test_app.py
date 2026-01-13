from app.app import Application
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline
from core.pipeline.stages.camera_source_stage import CameraSourceStage
def test_app():
    pipeline = Pipeline([
        CameraSourceStage(
        mirror=True
        )
    ])
    app = Application(pipeline, Renderer())
    app.initialize()
    app.run()
test_app()