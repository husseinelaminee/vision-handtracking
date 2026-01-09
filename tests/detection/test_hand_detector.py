import cv2
from vision.detection.hand_detector import HandDetector

def load_rgb(path):
    img = cv2.imread(path)
    assert img is not None, f"Image not found: {path}"
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def test_detect_hand_on_image():
    detector = HandDetector(draw=False)
    img = load_rgb("data/snapshots/hand1.png")

    out = detector.detect(img)

    assert len(out["landmarks"]) > 0
    assert out["handedness"] in ["Left", "Right"]


def test_no_hand_detected():
    detector = HandDetector(draw=False)
    img = load_rgb("data/snapshots/no_hand.png")

    out = detector.detect(img)

    assert len(out["landmarks"]) == 0
    assert out["handedness"] is None

