from core.event.event_type import EventType

class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._subscribers: dict[type, list[callable]] = {}

        return cls._instance
        

    def register_subscriber(self, subscriber):
        from core.event.subscriber import Subscriber
        # Check interface
        if not isinstance(subscriber, Subscriber):
            raise TypeError(
                f"Subscriber must implement 'Subscriber' interface, got: {type(subscriber).__name__}"
            )
        
        subscriber.event_bus = self

        # Validate `events` attribute
        if not hasattr(subscriber, "events"):
            raise AttributeError(
                f"Subscriber {subscriber} must define an 'events' property."
            )

        event_list = subscriber.events

        if not isinstance(event_list, (list, tuple)):
            raise TypeError(
                f"'events' must be a list or tuple of EventType classes, got {type(event_list)}"
            )

        # Validate entries inside events list
        for event_type in event_list:
            if not isinstance(event_type, type) or not issubclass(event_type, EventType):
                raise TypeError(
                    f"Invalid event type '{event_type}' in subscriber.events. "
                    f"Must be a subclass of EventType."
                )

        # Validate handler
        if not hasattr(subscriber, "handle_event"):
            raise AttributeError(
                f"Subscriber {subscriber} must define a 'handle_event(event)' method."
            )

        handler = subscriber.handle_event
        if not callable(handler):
            raise TypeError(
                f"'handle_event' must be callable on {subscriber}."
            )

        # Register
        for event_type in event_list:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(handler)

    def emit(self, event: EventType):
        if not isinstance(event, EventType):
            raise TypeError(f"emit() requires an EventType instance, got {type(event).__name__}")

        etype = type(event)

        if etype in self._subscribers:
            for handler in self._subscribers[etype]:
                handler(event)
