from app.app import Application
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline
from core.pipeline.stages.camera_source_stage import CameraSourceStage
from core.pipeline.stages.hand_detection_stage import HandDetectionStage
def launch():
    pipeline = Pipeline([
        CameraSourceStage(
        mirror=True
        ),
        HandDetectionStage(draw=True)

    ])
    app = Application(pipeline, Renderer())
    app.initialize()
    app.run()

# LAUNCH
launch()