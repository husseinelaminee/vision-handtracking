class EventType:
    pass

class CameraSelected(EventType):
    def __init__(self, index: int):
        self.index = index

class Quit(EventType):
    def __init__(self, reason: str):
        self.reason=reason
