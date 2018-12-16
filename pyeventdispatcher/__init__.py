from pyeventdispatcher.event_dispatcher import (
    dispatch_global_event,
    listen,
    EventDispatcher,
    Event,
    EventDispatcherException,
    EventSubscriber,
    register_global_listener,
    register_event_subscribers
)

__version__ = "0.1.0-alpha"

register = register_global_listener
dispatch = dispatch_global_event
