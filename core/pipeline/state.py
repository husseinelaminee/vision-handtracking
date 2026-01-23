from dataclasses import dataclass
from typing import Optional

@dataclass
class PipelineState:
    camera_index: Optional[int] = None
    pending_camera_index: Optional[int] = None
    hand_detected = False
    landmarks = None
    handedness = None
    landmarks_filtered=None
    hand_3d=None
    depth_map=None
    hand_3d_points=None
    hand_3d_centroid=None
    four_fingers_points = None
    four_fingers_hull = None
    four_fingers_hull_area = 0.0
    four_fingers_hull_centroid = None
    midi_cc_area = None
    midi_cc_pinch = None

