from abc import ABC, abstractmethod
from core.event.event_type import EventType
from core.event.event_bus import EventBus

class Publisher(ABC):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
