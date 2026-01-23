from abc import ABC, abstractmethod
from core.event.event_type import EventType

class Subscriber(ABC):
    
    def __init__(self, event_bus=None):
        super().__init__()
        from core.event.event_bus import EventBus
        self.event_bus: EventBus = event_bus or EventBus()
        self.event_bus.register_subscriber(self)
        
    @property
    @abstractmethod
    def events(self) -> list[type[EventType]]:
        """List of event types this subscriber listens to"""
        pass

    @abstractmethod
    def handle_event(self, event: EventType):
        """Handle the incoming event"""
        pass
