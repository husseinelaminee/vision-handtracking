import cv2
from vision.pipeline.stages.stage_base import Stage

class HandTrackingRenderStage(Stage):
    def __init__(self, color=(0, 255, 0), radius=4, thickness=2):
        self.color = color
        self.radius = radius
        self.thickness = thickness

        # MediaPipe connections (21 points) manually defined
        self.connections = [
            (0,1),(1,2),(2,3),(3,4),         # Thumb
            (0,5),(5,6),(6,7),(7,8),         # Index
            (0,9),(9,10),(10,11),(11,12),    # Middle
            (0,13),(13,14),(14,15),(15,16),  # Ring
            (0,17),(17,18),(18,19),(19,20)   # Pinky
        ]

    def process(self, frame, state):
        lm = state.get("landmarks_filtered")
        if lm is None:
            return frame, state

        h, w = frame.shape[:2]

        # Convert normalized coords → pixel coords
        pts = [(int(x * w), int(y * h)) for (x, y, z) in lm]

        # Draw connections
        for a, b in self.connections:
            cv2.line(frame, pts[a], pts[b], self.color, self.thickness)

        # Draw landmarks
        for (x, y) in pts:
            cv2.circle(frame, (x, y), self.radius, self.color, -1)

        return frame, state
