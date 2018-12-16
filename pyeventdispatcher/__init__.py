from pyeventdispatcher.event_dispatcher import (
    dispatch_global,
    PyEventDispatcher,
    PyEvent,
    PyEventDispatcherException,
    PyEventSubscriber,
    listen,
    register_global_listener,
)

__version__ = "0.1.0-alpha"

register = register_global_listener
dispatch = dispatch_global
