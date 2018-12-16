PyEventDispatcher
---

[![Build Status](https://travis-ci.org/whisller/pyeventdispatcher.svg?branch=master)](https://travis-ci.org/whisller/pyeventdispatcher)
---

PyEventDispatcher allows your application components to communicate with each
other by sending events and listening to them.

Inspiration for that was Symfony's [event-dispatcher](https://symfony.com/doc/current/components/event_dispatcher.html) component.

**Disclaimer**

Library is in very early stage of development. A lot of things can change, which includes breaking changes.

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

## Global and local listeners
In most of the cases your application will only need one  global registration of listeners that is used across
whole application.

But you might want to have different instances of PyEventDispatcher in your application. 
For that you can use concept of "local" listeners and dispatchers.

```python
from pyeventdispatcher import PyEventDispatcher, register

# By default we register all listeners in  global registry
register("foo.bar", lambda event: print("global listener"))

# But you can have several instances of event dispatcher
py_event_dispatcher_1 = PyEventDispatcher()
py_event_dispatcher_1.register("foo.bar", lambda event: print("event dispatcher 1"))

py_event_dispatcher_2 = PyEventDispatcher()
py_event_dispatcher_2.register("foo.bar", lambda event: print("event dispatcher 2"))
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

### By extending `PyEventSubscriber` class
```python
from pyeventdispatcher import PyEventSubscriber, register_event_subscribers

class MySubscriber(PyEventSubscriber):
    EVENTS = {"foo.bar": "execute_one", "bar.foo": ("execute_two", -100)}

    @staticmethod
    def execute_one(event):
        print(event.name)

    @staticmethod
    def execute_two(event):
        print(event.name)

register_event_subscribers()
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
As mentioned before you have global  registry of listeners but also you can initialise manually instance of
PyEventDispatcher. 

When dispatching an event you have options, either you will dispatch event to global registry or your local instance, 
which in fact can also dispatch event to global registry. 

I know that it might sound complicated, but let's have a look at an example :)

```python
from pyeventdispatcher import dispatch, PyEventDispatcher, PyEvent, register

# Register global listener
register("foo.bar", lambda event: print(f"{event.name}::global"))

# Initialise separated instance of PyEventDispatcher
py_event_dispatcher = PyEventDispatcher()
py_event_dispatcher.register("foo.bar", lambda event: print(f"{event.name}::local"))

# Dispatch event to global listeners only
dispatch(PyEvent("foo.bar"))
# Output: 
# foo.bar::global

# Dispatch event to both global and local listeners
py_event_dispatcher.dispatch(PyEvent("foo.bar"))
# Output: 
# foo.bar::global
# foo.bar::local

# Dispatch event to local listeners only
py_event_dispatcher.dispatch(PyEvent("foo.bar"), False)
# Output:
# foo.bar::local
```

## Stopping propagation
Sometimes you might want to stop propagation of event, for that you just have to set `event.stop` to `True`,

In example below only `first_listener` will be executed.

```python
from pyeventdispatcher import PyEventDispatcher

def first_listener(event):
    event.stop = True
    print("first_listener")

def second_listener(event):
    print("first_listener")

py_event_dispatcher = PyEventDispatcher()
py_event_dispatcher.register("foo.bar", first_listener)
py_event_dispatcher.register("foo.bar", second_listener)
# first_listener
```