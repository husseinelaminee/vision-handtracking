from app.app import Application
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline
from core.pipeline.stages.mock_camera_stage import MockCameraStage
from core.pipeline.stages.hand_detection_stage import HandDetectionStage
def launch():
    pipeline = Pipeline([
        MockCameraStage(),
        HandDetectionStage(draw=True)

    ])
    app = Application(pipeline, Renderer())
    app.initialize()
    app.run()

# LAUNCH
launch()