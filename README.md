# PyEventDispatcher
PyEventDispatcher allows your application components to communicate with each
other by sending events and listening to them.

Inspiration for that was Symfony's [event-dispatcher](https://symfony.com/doc/current/components/event_dispatcher.html) component.

## Listeners
Listeners must be valid callables. So any lambdas, functions, object functions are fine.

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

## Registering local listeners
In your application you can have multiple instances of PyEventDispatcher
all of them can have different listeners and events dispatched.

```python
from pyeventdispatcher import PyEventDispatcher

py_event_dispatcher = PyEventDispatcher()
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

## Registering listeners with execution priority
Listeners are executed by priority value, which by default is set to "0".

You can change priority of registered listener to define in which order it will be executed.

```python
from pyeventdispatcher import PyEventDispatcher

py_event_dispatcher = PyEventDispatcher()
py_event_dispatcher.register("foo.bar", lambda event: print("second"))
py_event_dispatcher.register("foo.bar", lambda event: print("first"), -100)
```

## Dispatching an event

```python
from pyeventdispatcher import PyEventDispatcher, PyEvent

py_event_dispatcher = PyEventDispatcher()
py_event_dispatcher.register("foo.bar", lambda event: print(event.name))

py_event_dispatcher.dispatch(PyEvent("foo.bar", {}))
# foo.bar
```