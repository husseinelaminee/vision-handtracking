import time
import threading
from app.renderer import Renderer
from core.pipeline.pipeline import Pipeline

class Application:
    def __init__(self, pipeline: Pipeline, renderer: Renderer):
        self.pipeline = pipeline
        self.renderer = renderer
        self._initialized = False
        self._running = False

        self._last_time = time.time()
        self._steps = 0
        self.steps_per_second = 0

    def initialize(self):
        self._initialized = True
        self.renderer.start()
        self.pipeline.initialize()

    def run(self):
        if not self._initialized:
            raise Exception("Call initialize() before run()")

        self._running = True
        
        # Start background thread for pipeline
        t = threading.Thread(target=self._pipeline_loop, daemon=True)
        t.start()

        # Main thread → rendering loop
        while self.renderer.running() and self._running:
            self.renderer.render_frame()

        self._running = False
        self.renderer.close()

    def _pipeline_loop(self):
        while self._running and self.renderer.running():

            frame = self.pipeline.process(None)

            # Store latest frame in renderer
            self.renderer.update_latest(frame)

            # PPS measurement
            self._steps += 1
            now = time.time()
            if now - self._last_time >= 1.0:
                self.steps_per_second = self._steps
                self._steps = 0
                self._last_time = now
                print(f"[PIPELINE] {self.steps_per_second} steps/s")
