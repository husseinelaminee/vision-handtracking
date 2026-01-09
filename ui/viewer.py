import cv2
import numpy as np
import dearpygui.dearpygui as dpg

from vision.pipeline.pipeline import Pipeline
from vision.pipeline.stages.camera_source_stage import CameraSourceStage
from vision.pipeline.stages.identity_stage import IdentityStage

ASPECT_RATIO = 4/3
SAVE_DIR = "data/snapshots"

class Viewer:
    def __init__(self, width=800, height=600, headless=False, timeout=None):
        self.headless = headless
        self.timeout = timeout
        self.width = width
        self.height = height
        self.last_size = (width, height)
        self.should_capture = False

        # In headless, replace camera stage with dummy static frame generator
        if headless:
            from vision.pipeline.stages.mock_camera_stage import MockCameraStage
            camera_stage = MockCameraStage()
        else:
            camera_stage = CameraSourceStage(mirror=True)

        self.pipelines = [
            Pipeline([camera_stage]),
            Pipeline([IdentityStage()]),
        ]

        if not self.headless:
            dpg.create_context()

            with dpg.texture_registry(show=False):
                empty = np.zeros((height * width * 3,), dtype=np.float32)
                dpg.add_raw_texture(
                    width, height, empty, tag="video_texture",
                    format=dpg.mvFormat_Float_rgb
                )

            with dpg.window(tag="MainWindow", label="Camera Viewer"):
                dpg.add_image("video_texture", tag="video_image")

        # Attach UI only if not headless
        if not self.headless:
            for pipeline in self.pipelines:
                pipeline.attach_ui()

        for pipeline in self.pipelines:
            pipeline.initialize()

        if not self.headless:
            dpg.create_viewport(title="Camera Viewer", width=width, height=height)
            dpg.setup_dearpygui()
            dpg.show_viewport()

    def update_frame(self):
        frame = None
        state = {}

        for pipeline in self.pipelines:
            frame, state = pipeline.process(frame, state)
            if frame is None:
                return

        # In headless, skip UI
        if self.headless:
            return frame

        # UI path
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = frame_rgb.astype(np.float32) / 255.0
        frame_rgb = cv2.resize(frame_rgb, (self.width, self.height))

        dpg.set_value("video_texture", frame_rgb.flatten())

    def run(self):
        if self.headless:
            # Headless stops after timeout frames
            limit = self.timeout if self.timeout else 1
            for _ in range(limit):
                self.update_frame()
            return

        # UI loop
        while dpg.is_dearpygui_running():
            self.update_frame()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()
