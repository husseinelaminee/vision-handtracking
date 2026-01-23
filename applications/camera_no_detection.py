from app.app import Application
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline
from core.pipeline.stages.camera_source_stage import CameraSourceStage
def launch():
    pipeline = Pipeline([
        CameraSourceStage(
        mirror=True
        )
    ])
    app = Application(pipeline, Renderer())
    app.initialize()
    app.run()

# ENTRYPOINT
if __name__ == "__main__":
    launch()