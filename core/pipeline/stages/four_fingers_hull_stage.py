# vision/stages/four_fingers_hull_stage.py
from core.pipeline.stages.stage_base import Stage
from core.pipeline.state import PipelineState
import numpy as np
import cv2

THUMB_TIP = 4
INDEX_TIP = 8

class FourFingersHullStage(Stage):
    def __init__(self, require_two_hands: bool = True, draw: bool = True):
        self.require_two_hands = require_two_hands
        self.draw = draw

    def initialize(self):
        pass

    def process(self, frame, state: PipelineState):
        state.four_fingers_points = None
        state.four_fingers_hull = None
        state.four_fingers_hull_area = 0.0
        state.four_fingers_hull_centroid = None

        if frame is None or not getattr(state, "hand_detected", False):
            return frame
        if not state.landmarks or not state.handedness:
            return frame

        h, w = frame.shape[:2]

        points_by_hand = {}
        for handedness, lms in zip(state.handedness, state.landmarks):
            if lms is None or len(lms) <= max(THUMB_TIP, INDEX_TIP):
                continue

            tx, ty, _ = lms[THUMB_TIP]
            ix, iy, _ = lms[INDEX_TIP]

            thumb_xy = (int(tx * w), int(ty * h))
            index_xy = (int(ix * w), int(iy * h))

            points_by_hand[handedness] = {"thumb": thumb_xy, "index": index_xy}

        state.four_fingers_points = points_by_hand

        if self.require_two_hands and (("Left" not in points_by_hand) or ("Right" not in points_by_hand)):
            if self.draw:
                self._draw_points(frame, points_by_hand)
            return frame

        pts = []
        for side in ("Left", "Right"):
            if side in points_by_hand:
                pts.append(points_by_hand[side]["thumb"])
                pts.append(points_by_hand[side]["index"])

        if len(pts) < 3:
            if self.draw:
                self._draw_points(frame, points_by_hand)
            return frame

        pts_np = np.array(pts, dtype=np.int32).reshape(-1, 1, 2)
        hull = cv2.convexHull(pts_np)  # (N,1,2)

        hull_xy = hull.reshape(-1, 2)
        state.four_fingers_hull = [(int(x), int(y)) for x, y in hull_xy]

        area = float(cv2.contourArea(hull))
        state.four_fingers_hull_area = area

        if area > 1e-6:
            M = cv2.moments(hull)
            if abs(M["m00"]) > 1e-6:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                state.four_fingers_hull_centroid = (cx, cy)

        if self.draw:
            self._draw_points(frame, points_by_hand)
            self._draw_hull(frame, hull_xy, centroid=state.four_fingers_hull_centroid)

        return frame

    def _draw_points(self, frame, points_by_hand):
        # Thumb/index points + small labels
        for side, pts in points_by_hand.items():
            for name, (x, y) in pts.items():
                cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)
                cv2.putText(frame, f"{side[0]}-{name[0]}", (x + 8, y - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    def _draw_hull(self, frame, hull_xy, centroid=None):
        # Draw polygon outline + translucent fill
        poly = hull_xy.astype(np.int32).reshape(-1, 1, 2)

        overlay = frame.copy()
        # cv2.fillPoly(overlay, [poly], (255, 0, 0))
        cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)

        cv2.polylines(frame, [poly], isClosed=True, color=(255, 0, 0), thickness=2)

        if centroid is not None:
            cx, cy = centroid
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, "centroid", (cx + 8, cy - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
