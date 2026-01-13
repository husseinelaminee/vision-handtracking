from dataclasses import dataclass
from typing import Optional

@dataclass
class PipelineState:
    camera_index: Optional[int] = None
    pending_camera_index: Optional[int] = None
