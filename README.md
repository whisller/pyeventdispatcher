PyEventDispatcher
---

[![Build Status](https://travis-ci.org/whisller/pyeventdispatcher.svg?branch=master)](https://travis-ci.org/whisller/pyeventdispatcher)
---

PyEventDispatcher allows your application components to communicate with each
other by sending events and listening to them.

Inspiration for that was Symfony's [event-dispatcher](https://symfony.com/doc/current/components/event_dispatcher.html) component.

**Disclaimer**

Application is in very early stage of development. Quite a lot of things might change in interface :)

## Installation
```bash
pip install pyeventdispatcher
```

## Listeners
Listener must be valid [callable](https://docs.python.org/3/library/functions.html#callable) that takes one parameter, `event`.

Below function is simplest listener you can define:
```python
def my_listener(event):
    print(event.name)
``` 

## Global and local listeners
In most of the cases your application will need only one instance of PyEventDispatcher to distribute events.

But you can register as many instances as you wish.

```python
from pyeventdispatcher import PyEventDispatcher

# By default we register all listeners globally
# so they are shared across all instances
PyEventDispatcher.register("foo.bar", lambda event: print("global listener"))

# But you can have several instances
# By default they dispatch to global listeners as well
py_event_dispatcher_1 = PyEventDispatcher()
py_event_dispatcher_1.register_local("foo.bar", lambda event: print("event dispatcher 1"))

# But you can disable global listeners with `disable_global` config
py_event_dispatcher_2 = PyEventDispatcher({"disable_global": True})
py_event_dispatcher_2.register_local("foo.bar", lambda event: print("event dispatcher 2"))
```

## Registering listener
There is several ways of registering your listener, you can mix styles or keep one across whole application.

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
from pyeventdispatcher import PyEventSubscriber

class MySubscriber(PyEventSubscriber):
    EVENTS = {"foo.bar": "execute_one", "bar.foo": ("execute_two", -100)}

    @staticmethod
    def execute_one(event):
        print(event.name)

    @staticmethod
    def execute_two(event):
        print(event.name)
```

## Registering listeners with execution priority
Listeners are executed in order of priority parameter's value, which by default is set to "0".

You can change priority of registered listener to define in which order it will be executed.

```python
from pyeventdispatcher import PyEventDispatcher

PyEventDispatcher.register("foo.bar", lambda event: print("second"))
PyEventDispatcher.register("foo.bar", lambda event: print("first "), -100)
# first second
```

## Dispatching an event

```python
from pyeventdispatcher import PyEventDispatcher, PyEvent

PyEventDispatcher.register("foo.bar", lambda event: print(event.name))

py_event_dispatcher = PyEventDispatcher()
py_event_dispatcher.dispatch(PyEvent("foo.bar"))
# foo.bar
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