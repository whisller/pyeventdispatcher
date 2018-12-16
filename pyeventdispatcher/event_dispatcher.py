import functools
from collections import defaultdict


class PyEventDispatcherException(Exception):
    pass


class PyEvent:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.stop = False


class PyEventSubscriber:
    EVENTS = {}


class GlobalMemoryRegistry:
    _LISTENERS = defaultdict(list)

    @staticmethod
    def register(name, listener, position):
        GlobalMemoryRegistry._LISTENERS[name].append(
            {"listener": listener, "position": position}
        )

    @staticmethod
    def get(name):
        return (
            GlobalMemoryRegistry._LISTENERS[name]
            if name in GlobalMemoryRegistry._LISTENERS
            else []
        )


registry = GlobalMemoryRegistry


class PyEventDispatcher:
    def __init__(self):
        self._local_listeners = defaultdict(list)

    def register_local(self, event_name, listener, position=0):
        _validate_registration(listener, position)

        self._local_listeners[event_name].append(
            {"listener": listener, "position": position}
        )

    def dispatch(self, event, to_global=True):
        local_listeners = self._local_listeners.get(event.name, [])
        gloabl_listeners = registry.get(event.name)

        all_listeners = sorted(
            local_listeners + gloabl_listeners, key=lambda x: x["position"]
        )

        for info in all_listeners:
            if not event.stop:
                info["listener"](event)


def dispatch_global(event):
    for info in registry.get(event.name):
        if not event.stop:
            info["listener"](event)


def register_global_listener(event_name, listener, position=0):
    _validate_registration(listener, position)

    registry.register(event_name, listener, position)


def register_event_subscribers():
    for subscriber_class in PyEventSubscriber.__subclasses__():
        for event_name, options in subscriber_class.EVENTS.items():
            if type(options) is tuple:
                method_name = options[0]
                position = options[1]
            else:
                method_name = options
                position = 0

            listener = getattr(subscriber_class, method_name)
            register_global_listener(event_name, listener, position)


def listen(*args):
    def decorator_listener(func):
        for arg in args:
            if type(arg) == tuple:
                event_name = arg[0]
                position = arg[1]
            else:
                event_name = arg
                position = 0
            register_global_listener(event_name, func, position)

        @functools.wraps(func)
        def wrapper_listener(*_args, **kwargs):
            return func(*_args, **kwargs)

        return wrapper_listener

    return decorator_listener


def _validate_registration(listener, position):
    if not callable(listener):
        raise PyEventDispatcherException(f'"{listener}" is not callable.')

    try:
        float(position)
    except (ValueError, TypeError):
        raise PyEventDispatcherException(f'"{position}" is not numeric.')
