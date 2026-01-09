from vision.pipeline.stages.stage_base import Stage

class HandTrackingStage(Stage):
    def __init__(self, smoothing=0.7):
        self.smoothing = smoothing
        self.prev_landmarks = None
        self.prev_time = None

    def initialize(self):
        self.prev_landmarks = None
        self.prev_time = None

    def process(self, frame, state):
        lm = state.get("landmarks")

        # If no hand detected, reset tracking
        if lm is None:
            self.prev_landmarks = None
            state["landmarks_filtered"] = None
            state["velocity"] = None
            return frame, state

        # First detection → no smoothing yet
        if self.prev_landmarks is None:
            self.prev_landmarks = lm
            state["landmarks_filtered"] = lm
            state["velocity"] = None
            return frame, state

        alpha = self.smoothing

        # Exponential smoothing
        filtered = [
            (
                alpha * p_old[0] + (1 - alpha) * p_new[0],
                alpha * p_old[1] + (1 - alpha) * p_new[1],
                alpha * p_old[2] + (1 - alpha) * p_new[2],
            )
            for p_old, p_new in zip(self.prev_landmarks, lm)
        ]

        # Velocity vector (optionnel)
        velocity = [
            (
                filtered[i][0] - self.prev_landmarks[i][0],
                filtered[i][1] - self.prev_landmarks[i][1],
                filtered[i][2] - self.prev_landmarks[i][2],
            )
            for i in range(len(filtered))
        ]

        self.prev_landmarks = filtered
        state["landmarks_filtered"] = filtered
        state["velocity"] = velocity

        return frame, state

    def attach_ui(self):
        pass  # optional later: slider for smoothing
