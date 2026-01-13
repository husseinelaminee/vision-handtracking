from abc import ABC, abstractmethod
from core.event.event_type import EventType

class Subscriber(ABC):
    
    def __init__(self):
        super().__init__()
        self.event_bus: "EventBus" = None
        
    @property
    @abstractmethod
    def events(self) -> list[type[EventType]]:
        """List of event types this subscriber listens to"""
        pass

    @abstractmethod
    def handle_event(self, event: EventType):
        """Handle the incoming event"""
        pass
