from collections import defaultdict


class PyEvent:
    def __init__(self, name, data):
        self.name = name
        self.data = data


class PyEventDispatcher:
    def __init__(self):
        self._listeners = defaultdict(list)

    def register(self, event_name, listener):
        self._listeners[event_name].append(listener)

    def dispatch(self, event):
        if event.name in self._listeners:
            for listener in self._listeners[event.name]:
                listener(event)
