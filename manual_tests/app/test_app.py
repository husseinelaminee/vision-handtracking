from app.app import Application
from app.renderer import Renderer
from vision.pipeline.pipeline import Pipeline
from vision.pipeline.stages.camera_source_stage import CameraSourceStage
from vision.pipeline.stages.hand_detection_stage import HandDetectionStage
from vision.pipeline.stages.hand_tracking_stage import HandTrackingStage
# from vision.pipeline.stages.hand_tracking_render_stage import HandTrackingRenderStage
def test_app():
    pipelines = [Pipeline([
        CameraSourceStage(mirror=True),
        HandDetectionStage(draw=True),
        HandTrackingStage(smoothing=0.8),
    ])]
    app = Application(pipelines, Renderer())

    app.run()
test_app()