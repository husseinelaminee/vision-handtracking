# vision/stages/midi_publisher_stage.py
from core.pipeline.stages.stage_base import Stage
from core.pipeline.state import PipelineState
import time
import math

# deps: pip install mido python-rtmidi
import mido

def _clamp(x, a, b):
    return a if x < a else (b if x > b else x)

def _map01_to_127(x01: float) -> int:
    return int(_clamp(x01, 0.0, 1.0) * 127)

class MidiPublisherStage(Stage):
    """
    Publishes 2 continuous controls to Ableton as MIDI CC:
      - CC_A (default 74): mapped from hull area (state.four_fingers_hull_area)
      - CC_B (default 71): mapped from pinch distance (thumb-index of Right hand if available)
    Requires: HandDetectionStage + FourFingersHullStage earlier in pipeline.

    Ableton:
      Preferences -> Link/Tempo/MIDI -> find "HandTracking CC" -> Remote ON
      Click MIDI (top right) -> click parameter -> move hand -> mapped.
    """
    def __init__(
        self,
        port_name: str = "HandTracking CC 1",
        cc_area: int = 74,
        cc_pinch: int = 71,
        channel: int = 0,
        hz: float = 60.0,
        # calibration ranges (pixels^2 for area, pixels for pinch)
        area_min: float = 200.0,
        area_max: float = 15000.0,
        pinch_min: float = 10.0,
        pinch_max: float = 220.0,
        smoothing: float = 0.2,   # 0=no smoothing, 1=very slow
        virtual: bool = True,
    ):
        self.port_name = port_name
        self.cc_area = cc_area
        self.cc_pinch = cc_pinch
        self.channel = channel
        self.hz = hz
        self.period = 1.0 / max(1e-6, hz)

        self.area_min = area_min
        self.area_max = area_max
        self.pinch_min = pinch_min
        self.pinch_max = pinch_max

        self.smoothing = _clamp(smoothing, 0.0, 0.99)
        self.virtual = virtual

        self._out = None
        self._t_last = 0.0
        self._area_f = None
        self._pinch_f = None
        self._last_sent = (None, None)

    def initialize(self):
        # Windows: use loopMIDI port (no virtual ports)
        self._out = mido.open_output(self.port_name)  # no virtual kw
        self._t_last = 0.0


    def process(self, frame, state: PipelineState):
        now = time.time()
        if (now - self._t_last) < self.period:
            return frame
        self._t_last = now

        # --- Read features from state ---
        area = float(getattr(state, "four_fingers_hull_area", 0.0) or 0.0)

        pinch = None
        pts = getattr(state, "four_fingers_points", None)
        if isinstance(pts, dict):
            # Prefer Right hand pinch; fallback Left if only one hand
            for side in ("Right", "Left"):
                if side in pts and "thumb" in pts[side] and "index" in pts[side]:
                    (tx, ty) = pts[side]["thumb"]
                    (ix, iy) = pts[side]["index"]
                    pinch = math.hypot(ix - tx, iy - ty)
                    break

        # If nothing detected, don't spam zeros (optional)
        if area <= 0.0 and pinch is None:
            return frame

        # --- Normalize ---
        area01 = (area - self.area_min) / max(1e-6, (self.area_max - self.area_min))
        pinch01 = 0.0
        if pinch is not None:
            pinch01 = (pinch - self.pinch_min) / max(1e-6, (self.pinch_max - self.pinch_min))

        # --- Smooth ---
        if self._area_f is None:
            self._area_f = _clamp(area01, 0.0, 1.0)
        else:
            self._area_f = (1 - self.smoothing) * _clamp(area01, 0.0, 1.0) + self.smoothing * self._area_f

        if self._pinch_f is None:
            self._pinch_f = _clamp(pinch01, 0.0, 1.0)
        else:
            self._pinch_f = (1 - self.smoothing) * _clamp(pinch01, 0.0, 1.0) + self.smoothing * self._pinch_f

        v_area = _map01_to_127(self._area_f)
        v_pinch = _map01_to_127(self._pinch_f)

        # --- Send only if changed (reduces MIDI spam) ---
        last_a, last_p = self._last_sent
        if v_area != last_a:
            self._out.send(mido.Message("control_change", control=self.cc_area, value=v_area, channel=self.channel))
        if v_pinch != last_p:
            self._out.send(mido.Message("control_change", control=self.cc_pinch, value=v_pinch, channel=self.channel))
        self._last_sent = (v_area, v_pinch)

        # Expose for debug UI if you want
        state.midi_cc_area = v_area
        state.midi_cc_pinch = v_pinch
        return frame
