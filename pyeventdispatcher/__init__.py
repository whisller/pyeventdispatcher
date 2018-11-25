from collections import defaultdict


class PyEventDispatcherException(Exception):
    pass


class PyEvent:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class PyEventDispatcher:
    def __init__(self):
        self._listeners = defaultdict(list)

    def register(self, event_name, listener, position=0):
        if not callable(listener):
            raise PyEventDispatcherException(f'"{listener}" is not callable.')

        try:
            float(position)
        except (ValueError, TypeError):
            raise PyEventDispatcherException(f'"{position}" is not numeric.')

        self._listeners[event_name].append({"listener": listener, "position": position})

    def dispatch(self, event):
        if event.name in self._listeners:
            for info in sorted(
                self._listeners[event.name], key=lambda x: x["position"]
            ):
                info["listener"](event)
