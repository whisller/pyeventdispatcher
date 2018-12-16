PyEventDispatcher
---

[![Build Status](https://travis-ci.org/whisller/pyeventdispatcher.svg?branch=master)](https://travis-ci.org/whisller/pyeventdispatcher)
---

PyEventDispatcher allows your application components to communicate with each
other by sending events and listening to them.
Inspiration for this library was Symfony's [event-dispatcher](https://symfony.com/doc/current/components/event_dispatcher.html) component.

## Disclaimer
Library is in very early stage of development. A lot of things can change, which includes breaking changes.

## Easiest example
```python
from pyeventdispatcher import dispatch, Event, register

register("foo.bar", lambda event: print(f"{event.name}::{event.data}"))
dispatch(Event("foo.bar", "some data"))
# foo.bar::some data
```

## Installation
```bash
pip install pyeventdispatcher
```

## Listeners
Any [callable](https://docs.python.org/3/library/functions.html#callable) can be registered as listener,
the only requirements is that it takes one parameter, `event`.

Below function is simplest example of listener you can define:
```python
def my_listener(event):
    print(event.name)
```

## Registering global listener
There is several ways of registering your global listener, you can mix styles or keep one across whole application.

### `register` function
```python
from pyeventdispatcher import register

def my_func(event):
    print(event.name)

register("foo.bar", my_func)
register("bar.foo", my_func, -100)
```

### `listen` decorator
```python
from pyeventdispatcher import listen

@listen("foo.bar", ("bar.foo", -100))
def my_func(event):
    print(event.name)
```

### By extending `EventSubscriber` class
```python
from pyeventdispatcher import EventSubscriber, register_event_subscribers

class MySubscriber(EventSubscriber):
    EVENTS = {"foo.bar": "execute_one", "bar.foo": ("execute_two", -100)}

    @staticmethod
    def execute_one(event):
        print(event.name)

    @staticmethod
    def execute_two(event):
        print(event.name)

register_event_subscribers() # Register your classes
```

## Local listeners
In most of the cases your application will only need one global registration of listeners that is used across
whole application.

Buf if you need, you can initialise as many instances of EventDispatcher as you wish. Everyone of them will have
local registry of listeners.

```python
from pyeventdispatcher import EventDispatcher, register

# Register listener in  global registry
register("foo.bar", lambda event: print("global listener"))

# Initialise instances of local EventDispatcher
py_event_dispatcher_1 = EventDispatcher()
py_event_dispatcher_1.register("foo.bar", lambda event: print("event dispatcher 1"))

py_event_dispatcher_2 = EventDispatcher()
py_event_dispatcher_2.register("foo.bar", lambda event: print("event dispatcher 2"))
```

## Registering listeners with execution priority
Listeners are executed in order of priority parameter's value, which by default is set to "0".

You can change priority of registered listener to define in which order it will be executed.

```python
from pyeventdispatcher import register

register("foo.bar", lambda event: print("second"))
register("foo.bar", lambda event: print("first "), -100)
# first second
```

## Dispatching an event
When you dispatch your event, every registered listener that listens for occurrence of specified event,
will be called with event object as parameter.

### Dispatching global event
```python
from pyeventdispatcher import dispatch, Event, register

register("foo.bar", lambda event: print(event.name))

dispatch(Event("foo.bar", {"id": 1}))
```

### Dispatching local event
```python
from pyeventdispatcher import EventDispatcher, Event, register

register("foo.bar", lambda event: print(f"{event.name}::global"))

# Initialise separated instance
py_event_dispatcher = EventDispatcher()
py_event_dispatcher.register("foo.bar", lambda event: print(f"{event.name}::local"))

# Dispatch event to both global and local listeners
py_event_dispatcher.dispatch(Event("foo.bar"))
# foo.bar::global
# foo.bar::local

# Dispatch event to local listeners only
py_event_dispatcher.dispatch(Event("foo.bar"), False)
# foo.bar::local
```

## Stopping propagation
Sometimes you might want to stop propagation of event, for that you just have to set `event.stop` to `True`,

In example below only `first_listener` will be executed.

```python
from pyeventdispatcher import register

def first_listener(event):
    event.stop = True
    print("first_listener")

def second_listener(event):
    print("first_listener")

register("foo.bar", first_listener)
register("foo.bar", second_listener)
# first_listener
```