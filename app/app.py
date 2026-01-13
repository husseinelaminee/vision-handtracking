from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline

class Application:
    def __init__(self, pipeline: Pipeline, renderer: Renderer):
        self.pipeline = pipeline
        self.renderer = renderer
        self._initialized = False

    def run(self, frames=0):
        if not self._initialized:
            raise Exception("Application should be initialized before run")
        if self.renderer.headless:
            limit = frames or 1
            for _ in range(limit):
                self._update_once()
            self.renderer.close()
            return

        while self.renderer.running():
            self._update_once()
            self.renderer.render_frame()

        self.renderer.close()

    def initialize(self):
        self._initialized = True
        self.renderer.start()
        self.pipeline.initialize()

    def _update_once(self):
        frame = None
        frame = self.pipeline.process(frame)
        self.renderer.update(frame)
