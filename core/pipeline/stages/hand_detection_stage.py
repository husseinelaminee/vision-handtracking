from core.pipeline.stages.stage_base import Stage
from core.pipeline.state import PipelineState
import mediapipe as mp
import numpy as np

class HandDetectionStage(Stage):
    def __init__(self, draw=True):
        self.draw = draw
        self.mp_hands = None
        self.mp_draw = None

    def initialize(self):
        self.mp_hands = mp.solutions.hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame, state: PipelineState):
        if frame is None:
            return None

        rgb = frame[:, :, ::-1]  # BGR → RGB
        results = self.mp_hands.process(rgb)

        state.hand_detected = False
        state.landmarks = None
        state.handedness = None

        if results.multi_hand_landmarks:
            state.hand_detected = True

            hand_lm = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0].classification[0].label

            state.handedness = handedness
            state.landmarks = [
                (lm.x, lm.y, lm.z) for lm in hand_lm.landmark
            ]

            if self.draw:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_lm,
                    mp.solutions.hands.HAND_CONNECTIONS
                )

        return frame
