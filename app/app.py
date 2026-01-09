from app.renderer import Renderer
from vision.pipeline.pipeline import Pipeline
class Application:
    def __init__(self, pipelines:list[Pipeline], renderer: Renderer):
        self.pipelines = pipelines
        self.renderer = renderer
        for p in self.pipelines:
            p.initialize()
        


    def run(self, frames=0):
        self.renderer.start()
        for p in self.pipelines:
            p.attach_ui()
        

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

    def _update_once(self):
        frame = None
        state = {}

        for p in self.pipelines:
            frame, state = p.process(frame, state)

        self.renderer.update(frame)
