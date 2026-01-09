from abc import ABC, abstractmethod

class Stage(ABC):
    def initialize(self):
        pass

    @abstractmethod
    def process(self, frame, state):
        pass

    def attach_ui(self):
        pass

    def dispose(self):
        pass
