# PyEventDispatcher
PyEventDispatcher allows your application components to communicate with each
other by sending events and listening to them.

## Listeners
Listeners are just callables, lambdas, functions, object functions.

## Registering local listeners
In your application you can have multiple instances of PyEventDispatcher
all of them can have different listeners and events dispatched.

```python
from pyeventdispatcher import PyEventDispatcher

class MyListener:
    def on_event(self, event):
        print("MyListener.on_event")

def on_event(event):
    print("on_event")

py_event_dispatcher = PyEventDispatcher()
py_event_dispatcher.register("foo.bar", MyListener().on_event)
py_event_dispatcher.register("foo.bar", on_event)
py_event_dispatcher.register("foo.bar", lambda event: print("lambda"))
```

## Registering global listeners
Sometimes you might want to register listeners across all your PyEventDispatcher
instances.

```python
from pyeventdispatcher import PyEventDispatcher

PyEventDispatcher.register_global("foo.bar", lambda event: print("global listener"))

py_event_dispatcher_1 = PyEventDispatcher()
py_event_dispatcher_1.register("foo.bar", lambda event: print("lambda"))

py_event_dispatcher_2 = PyEventDispatcher()
py_event_dispatcher_2.register("foo.bar", lambda event: print("lambda"))
```
