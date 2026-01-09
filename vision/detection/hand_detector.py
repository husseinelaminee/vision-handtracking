import cv2
import mediapipe as mp

class HandDetector:
    """
    Simple wrapper around MediaPipe Hands.
    Responsibilities:
    - Runs detection + internal tracking
    - Returns landmarks, handedness, and an annotated frame if needed
    """

    def __init__(self,
                 max_hands=1,
                 min_detection_conf=0.6,
                 min_tracking_conf=0.6,
                 draw=False):
        self.draw = draw

        self.mp_hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=min_tracking_conf
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame_rgb):
        """
        Input:
            frame_rgb: numpy RGB image (uint8)
        Output:
            {
                "annotated": RGB image (if draw=True)
                "landmarks": list of 21x( x,y,z )
                "handedness": "Left" | "Right" | None
            }
        """
        results = self.mp_hands.process(frame_rgb)

        output = {
            "annotated": frame_rgb.copy() if self.draw else frame_rgb,
            "landmarks": [],
            "handedness": None
        }

        if not results.multi_hand_landmarks:
            return output

        # Only take the first hand for now
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness_label = results.multi_handedness[0].classification[0].label

        # Extract landmarks
        landmark_list = [
            (lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark
        ]

        output["landmarks"] = landmark_list
        output["handedness"] = handedness_label

        # Optionally draw
        if self.draw:
            self.mp_draw.draw_landmarks(
                output["annotated"],
                hand_landmarks,
                mp.solutions.hands.HAND_CONNECTIONS
            )

        return output
