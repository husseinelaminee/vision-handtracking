from app.app import Application
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline
from core.pipeline.stages.camera_source_stage import CameraSourceStage
from core.pipeline.stages.hand_detection_stage import HandDetectionStage
from core.pipeline.stages.four_fingers_hull_stage import FourFingersHullStage
def launch():
    pipeline = Pipeline([
        CameraSourceStage(
        mirror=True
        ),
        HandDetectionStage(draw=True),
        FourFingersHullStage()
    ])
    app = Application(pipeline, Renderer())
    app.initialize()
    app.run()

# ENTRYPOINT
if __name__ == "__main__":
    launch()