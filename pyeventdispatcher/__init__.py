from pyeventdispatcher.event_dispatcher import (
    PyEventDispatcher,
    PyEvent,
    PyEventDispatcherException,
    PyEventSubscriber,
    listen
)

__version__ = "1.0.0"

register = PyEventDispatcher.register
dispatch = PyEventDispatcher.dispatch_global
