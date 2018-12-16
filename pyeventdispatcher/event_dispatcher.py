import functools
from collections import defaultdict


class EventDispatcherException(Exception):
    pass


class Event:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.stop = False


class EventSubscriber:
    EVENTS = {}


class MemoryRegistry:
    def __init__(self):
        self._listeners = defaultdict(list)

    def register(self, name, listener, position):
        self._listeners[name].append({"listener": listener, "position": position})

    def __getitem__(self, name):
        return self._listeners[name]


global_registry = MemoryRegistry()


class EventDispatcher:
    def __init__(self):
        self._local_registry = MemoryRegistry()

    def register(self, event_name, listener, position=0):
        _validate_registration(listener, position)

        self._local_registry[event_name].append(
            {"listener": listener, "position": position}
        )

    def dispatch(self, event, to_global=True):
        local_listeners = self._local_registry[event.name]

        if to_global:
            global_listeners = global_registry[event.name]
        else:
            global_listeners = []

        all_listeners = sorted(
            local_listeners + global_listeners, key=lambda x: x["position"]
        )

        for info in all_listeners:
            if not event.stop:
                info["listener"](event)


def dispatch_global_event(event):
    for info in global_registry[event.name]:
        if not event.stop:
            info["listener"](event)


def register_global_listener(event_name, listener, position=0):
    _validate_registration(listener, position)

    global_registry.register(event_name, listener, position)


def register_event_subscribers():
    # @TODO do it automatically?
    for subscriber_class in EventSubscriber.__subclasses__():
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
        raise EventDispatcherException(f'"{listener}" is not callable.')

    try:
        float(position)
    except (ValueError, TypeError):
        raise EventDispatcherException(f'"{position}" is not numeric.')
