from collections import defaultdict

__version__ = "1.0.0"


class PyEventDispatcherException(Exception):
    pass


class PyEvent:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class PyEventDispatcher:
    _GLOBAL_LISTENERS = defaultdict(list)

    def __init__(self):
        self._listeners = defaultdict(list)

    def register(self, event_name, listener, position=0):
        PyEventDispatcher._validate(listener, position)

        self._listeners[event_name].append({"listener": listener, "position": position})

    @staticmethod
    def register_global(event_name, listener, position=0):
        PyEventDispatcher._validate(listener, position)

        PyEventDispatcher._GLOBAL_LISTENERS[event_name].append(
            {"listener": listener, "position": position}
        )

    def dispatch(self, event):
        local_listeners = self._listeners.get(event.name, [])
        gloabl_listeners = PyEventDispatcher._GLOBAL_LISTENERS.get(event.name, [])

        all_listeners = sorted(
            local_listeners + gloabl_listeners, key=lambda x: x["position"]
        )

        for info in all_listeners:
            info["listener"](event)

    @staticmethod
    def _validate(listener, position):
        if not callable(listener):
            raise PyEventDispatcherException(f'"{listener}" is not callable.')

        try:
            float(position)
        except (ValueError, TypeError):
            raise PyEventDispatcherException(f'"{position}" is not numeric.')
