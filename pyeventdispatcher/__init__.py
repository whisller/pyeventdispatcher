from pyeventdispatcher.event_dispatcher import (
    PyEventDispatcher,
    PyEvent,
    PyEventDispatcherException,
    PyEventSubscriber,
    listen
)

__version__ = "0.1.0-alpha"

register = PyEventDispatcher.register
dispatch = PyEventDispatcher.dispatch_global
