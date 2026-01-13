class EventType:
    pass

class CameraSelected(EventType):
    def __init__(self, index: int):
        self.index = index
