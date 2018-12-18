from pyeventdispatcher.event_dispatcher import (
    dispatch_global_event,
    listen,
    EventDispatcher,
    Event,
    EventDispatcherException,
    EventSubscriber,
    register_global_listener,
    register_event_subscribers,
)

__version__ = "0.2.0a0"

register = register_global_listener
dispatch = dispatch_global_event
