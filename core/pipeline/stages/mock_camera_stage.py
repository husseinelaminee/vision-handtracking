from utils.path import SNAPSHOT_DIR
from core.pipeline.stages.stage_base import Stage
import cv2, random

class MockCameraStage(Stage):
    def __init__(self):
        self.paths = [
            SNAPSHOT_DIR / "hand1.png",
            SNAPSHOT_DIR / "no_hand.png",
        ]
        self.frames = [cv2.imread(str(p)) for p in self.paths]

    def process(self, frame, state):
        frame = random.choice(self.frames)
        return frame
